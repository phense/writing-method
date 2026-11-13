# Book PDF design

Use this template for a long manual that is printed on both sides, bound, or
read by several groups of readers. For a short document without parts, use the
[single-sided template](../pdf/DESIGN.md) instead.

The layout was developed on a manual of about 70 chapters. It uses A4 pages
with mirrored margins, a dark-navy title page, a title page for each part, and
a running head that names the part, the chapter and the page. The layout and
the sample text are original.

## Contents

- When to choose it
- Build
- Parts, chapters and order
- Settings
- What the filter does to the text
- Pages that end with a few lines
- Verification
- Limits

## When to choose it

| Situation | Template |
|---|---|
| A few chapters, read on screen or printed single-sided | `templates/documentation/pdf` |
| Many chapters, grouped by reader or subject | `templates/documentation/book` |
| Duplex printing or binding | `templates/documentation/book` |
| Readers look up one chapter rather than read from start to end | `templates/documentation/book` |

A book adds pages: the back of the title page, a title page per part and an
empty left-hand page wherever a chapter ends on a right-hand page. A document
of three chapters grows from about 5 to about 13 pages. Do not use the book
layout to make a short document look larger.

## Build

Copy this directory's source files into a new documentation directory. Exclude
`_book/`, `.quarto/` and generated top-level `.typ` files when copying an
already rendered checkout; keep the `.typ` sources inside `_extensions/`. Run
from that copy:

```sh
quarto --version
quarto render --to em-book-typst
```

Open `_book/manual.pdf`. The verified baseline is Quarto 1.10.18 with its
bundled Typst. No R, LaTeX or online Typst account is needed. The plugin does
not bundle Quarto or install it implicitly. Get it from the
[official release](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.18)
and check the release's SHA-256 checksum before installing.

The sample is set in Source Sans 3 with DejaVu Sans Mono for code. The six
Source Sans 3 files (Regular, Italic, Semibold, Semibold Italic, Bold and Bold
Italic, release 3.052R) are bundled in `fonts/` with their licence, the SIL
Open Font License 1.1. `font-paths` in `_quarto.yml` passes that directory to
Typst, so the text looks the same on every machine. Keep the licence file next
to the fonts when you copy the template.

The code font is not bundled. DejaVu Sans Mono is present on most Linux
systems; on other systems name an installed monospace family in `_brand.yml`
or copy its files into `fonts/`. To use another text family, do the same. Do
not ignore a missing-font warning: Typst then sets the text in a fallback font
and every page break moves.

## Parts, chapters and order

List the parts and their chapter files in `book.chapters` in `_quarto.yml`,
with paths relative to that file:

```yaml
book:
  chapters:
    - index.md
    - part: "Employees"
      chapters:
        - employees/clock-in.md
        - employees/request-leave.md
    - part: "Administration"
      chapters:
        - administration/backup.md
```

Compare the list with the accepted chunk manifest, in row order, and include
each selected chunk exactly once. No manifest parser or filename sorting runs
implicitly. The filter `book-structure.lua` reads the parts from this list; a
chapter does not say which part it belongs to.

A chapter listed outside a part gets no part label. A book without any `part`
entry is valid: it keeps the mirrored pages, the running head and the
right-hand chapter openings, and drops the part title pages. An appendix is an
ordinary last part. Quarto's separate `appendices` key is not supported by this
layout.

Each chapter has one H1. Existing chunk frontmatter can stay: when Quarto adds
a matching title heading from that metadata, the bundled filter removes only
the generated duplicate. `index.md` carries an empty title and no text in the
sample; text placed there appears as an unnumbered chapter after the contents.
Use stable IDs such as `{#sec-start}` and references such as `@sec-start`.
Quarto also resolves a relative link to another chapter file.

## Settings

| Element | Default | Where to change it |
|---|---|---|
| Page | A4, margins 32 mm inside, 24 mm outside, 30 mm top, 27 mm bottom | `typst-template.typ` |
| Text | Source Sans 3, 11 pt, dark ink `#232A31`, left-aligned | `_brand.yml` |
| Accent | Dark navy `#173A5E` | `_brand.yml`, `color.palette.navy` |
| Title page | Navy band with document kind and title, subtitle below | `_quarto.yml`: `book.title`, `book.subtitle`, `document-kind` |
| Imprint | Version, date, organisation and author on the back of the title page | `_quarto.yml`: `imprint` |
| Contents | One line per chapter, grouped under part labels | `typst-template.typ` |
| Part title page | Navy page with "Part N", the part title and its chapters | `_quarto.yml`: `book.chapters`, `part-label` |
| Chapter opening | Right-hand page, part label, number on a navy square, 24 pt title | `typst-template.typ` |
| Running head | Part label, chapter number and title, page number at the outer edge | `typst-template.typ` |
| Tables | 9.6 pt, grey header row, horizontal rules only | `typst-template.typ` |
| Pictures | Thin grey frame; a PNG taller than 118 mm is narrowed | `_quarto.yml`: `image-max-height`, `image-widths` |

`lang: de` selects the German labels "Teil", "Inhaltsverzeichnis", "Handbuch"
and "Stand". It does not translate the content. The contents list chapters
only; `toc-depth` has no effect.

The side margins are wider on the inside so that text stays readable in a
bound copy. The text block is 154 mm wide. If you change the margins in
`typst-template.typ`, change `text_width` in `book-structure.lua` to match.

## What the filter does to the text

`book-structure.lua` changes the rendered document, never the Markdown files:

- It inserts the part title pages and moves each chapter to a right-hand page.
- It keeps a sentence that ends with a colon on the same page as the table,
  list or picture that follows it.
- It narrows a PNG that is taller than `image-max-height`, so that the picture
  fits below its introduction instead of leaving half a page empty.
- With `lang: de` it sets the closing quotation mark after an opening `„`.
  Typst would otherwise set a second opening mark when the closing mark was
  typed as `"` or `“`.

## Pages that end with a few lines

A chapter that spills three lines onto a new page wastes that page and, in a
duplex book, often an empty page after it. The checker lists such pages under
`short_last_pages`. To remove one:

1. Find a picture in that chapter.
2. Set a slightly smaller width for it under `image-widths` in `_quarto.yml`,
   for example `overview.png: "130mm"`.
3. Render again and run the checker.

Keep such a reduction below about 20 % of the regular width, so that the
picture stays readable. Shorten the text instead when the chapter has no
picture. Remove a width again when the chapter text changes; a stale entry
costs only a slightly smaller picture.

## Verification

`tools/check-pdf.py` checks the rendered PDF. It needs Python with PyMuPDF:

```sh
python3 tools/check-pdf.py _book/manual.pdf
```

It fails when a chapter opens on a left-hand page, a page lacks its page
number, a contents entry names the wrong page, a link has no target, or text
or a picture reaches into the margins. It reports short last pages without
failing; `--strict-fill` makes them fail too. `--json report.json` writes the
full report for the verification record.

The checker does not judge appearance. Look at the title page, a part title
page, a chapter opening, a page with a running head, a long table and the last
page. In the delivered PDF also confirm manifest order and unchanged Markdown
sources, as for the single-sided template.

For the template itself, run from the Writing Method checkout:

```sh
python3 tests/e2e/test-documentation-book --quarto /path/to/quarto
```

It renders the sample in English and German and a stress case with a tall
picture, a table over several pages and German quotation marks.

## Limits

The layout is A4 only. It has one contents level, no index, no list of figures
and no separately numbered appendices. A PDF that passes the checker is not
thereby accessible; no PDF/UA conformance is claimed.
