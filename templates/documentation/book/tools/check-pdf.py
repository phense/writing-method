#!/usr/bin/env python3
"""Check a PDF rendered with the em-book layout. Requires PyMuPDF.

Usage: python3 tools/check-pdf.py [_book/manual.pdf] [--json report.json] [--min-fill 0.1]

Exit status 1 when a check fails. A chapter that ends with a nearly empty page is
reported under `short_last_pages` and fails only with --strict-fill.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import pymupdf as fitz

MARGIN = 45          # points; nothing may come closer to the paper edge than this
HEAD, FOOT = 85, 80  # points; bands in which the page number stands
TOP, BOTTOM = 85, 77 # points; text block of the layout (30 mm and 27 mm margins)


def normalize(text):
    return re.sub(r'[^\w]', '', text).casefold()


def check(pdf, min_fill=0.1):
    doc = fitz.open(pdf)
    chapters = [entry for entry in doc.get_toc() if entry[0] == 1]
    errors, overflows, overlaps, unnumbered, empty_pages, part_pages = [], [], [], [], [], []
    internal = external = toc_links = 0
    fill = {}
    for n, page in enumerate(doc, 1):
        textpage = page.get_textpage()
        text = page.get_text(textpage=textpage)
        words = page.get_text('words', textpage=textpage)
        # Page number: at the outer edge of the running head, or in the footer of a page
        # that opens a chapter or the table of contents.
        edge = [w[4] for w in words if w[3] < HEAD or w[1] > page.rect.height - FOOT]
        numbered = str(n) in edge
        empty = not text.strip() and not page.get_images()
        # A part title page is filled with the accent colour and has no page number.
        part = not numbered and not empty and n > 2 and any(
            d.get('fill') and d['rect'].width >= page.rect.width - 1 and d['rect'].height >= page.rect.height - 1
            for d in page.get_drawings())
        if part:
            part_pages.append(n)
        if empty:
            empty_pages.append(n)
            if n % 2:
                errors.append(f'Empty right-hand page: {n}')
        if n == 1 and numbered:
            errors.append('The title page carries a page number')
        if n > 2 and not part and not empty and not numbered:
            unnumbered.append(n)
        for link in page.get_links():
            if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                internal += 1
                target = link.get('page', -1)
                if not 0 <= target < len(doc):
                    errors.append(f'Invalid internal link target on page {n}')
                if chapters and n < chapters[0][2] and not part and link['from'].height > 0:
                    toc_links += 1
                    label = page.get_textbox(link['from'], textpage=textpage)
                    numbers = re.findall(r'\d+', label)
                    if not numbers or int(numbers[-1]) != target + 1:
                        errors.append(f'Contents entry with a wrong page number on page {n}: {label.strip()}')
            elif link['kind'] == fitz.LINK_URI:
                external += 1
                if '.md' in link.get('uri', ''):
                    errors.append(f'Unresolved Markdown link on page {n}')
            elif link['kind'] == fitz.LINK_GOTOR:
                errors.append(f'Link to another file on page {n}')
        lines, lowest = [], 0.0
        for block in page.get_text('dict', flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                x0, y0, x1, y1 = line['bbox']
                content = ''.join(span['text'] for span in line['spans']).strip()
                if not content:
                    continue
                lines.append((line['bbox'], content))
                if TOP <= y0 and y1 <= page.rect.height - BOTTOM:
                    lowest = max(lowest, y1)
                if not part and (x0 < MARGIN or x1 > page.rect.width - MARGIN or y0 < 10 or y1 > page.rect.height - 12):
                    overflows.append({'page': n, 'bounds': [round(v, 1) for v in line['bbox']], 'text': content[:110]})
        for i, (a, first) in enumerate(lines):
            for b, second in lines[i + 1:]:
                vertical = min(a[3], b[3]) - max(a[1], b[1])
                horizontal = min(a[2], b[2]) - max(a[0], b[0])
                if vertical > min(a[3] - a[1], b[3] - b[1]) * 0.5 and horizontal > 1:
                    overlaps.append({'page': n, 'first': first[:80], 'second': second[:80]})
        for item in page.get_images():
            for rect in page.get_image_rects(item):
                lowest = max(lowest, min(rect.y1, page.rect.height - BOTTOM))
                if rect.x0 < MARGIN or rect.x1 > page.rect.width - MARGIN or rect.y0 < MARGIN or rect.y1 > page.rect.height - 55:
                    overflows.append({'page': n, 'image_bounds': [round(v, 1) for v in rect]})
        fill[n] = max(0.0, lowest - TOP) / (page.rect.height - TOP - BOTTOM)
    if unnumbered:
        errors.append(f'Pages without a page number: {unnumbered}')
    if overlaps:
        errors.append(f'Overlapping text lines: {len(overlaps)}')
    if not chapters:
        errors.append('The PDF has no chapter bookmarks')
    for _, title, start in chapters:
        if start % 2 == 0:
            errors.append(f'Chapter opens on a left-hand page: {title}')
        if normalize(re.sub(r'^\d+\s*', '', title)) not in normalize(doc[start - 1].get_text()):
            errors.append(f'Chapter bookmark without a visible heading: {title}')
    if chapters and chapters[0][2] <= 2:
        errors.append('The first chapter is not separated from the title page and contents')
    # Last page of a chapter: the last filled page before the next chapter or part opens.
    short = []
    starts = [start for _, _, start in chapters] + [len(doc) + 1]
    for (_, title, start), following in zip(chapters, starts[1:]):
        last = following - 1
        while last > start and (last in empty_pages or last in part_pages):
            last -= 1
        if last > start and fill[last] < min_fill:
            short.append({'chapter': title, 'page': last, 'fill': round(fill[last], 3)})
    return {
        'pdf': str(pdf), 'sha256': hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),
        'pymupdf': fitz.VersionBind, 'pages': len(doc), 'chapters': len(chapters),
        'part_pages': part_pages, 'empty_pages': empty_pages, 'internal_links': internal,
        'toc_links': toc_links, 'external_links': external, 'errors': errors,
        'possible_overflows': overflows, 'text_overlaps': overlaps, 'short_last_pages': short,
        'outline': chapters,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('pdf', nargs='?', default='_book/manual.pdf')
    parser.add_argument('--json', type=Path, help='also write the full report to this file')
    parser.add_argument('--min-fill', type=float, default=0.1,
                        help='smallest filled share of the last page of a chapter (default 0.1)')
    parser.add_argument('--strict-fill', action='store_true', help='fail on short last pages')
    args = parser.parse_args()
    result = check(args.pdf, args.min_fill)
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'outline'}, ensure_ascii=False, indent=2))
    failed = result['errors'] or result['possible_overflows'] or (args.strict_fill and result['short_last_pages'])
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
