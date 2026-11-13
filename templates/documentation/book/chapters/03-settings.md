---
id: C-003
title: Settings
type: reference
doc_id: book-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-11-13
---

# Settings {#sec-settings}

## Files and responsibilities

| File | What you change |
|---|---|
| `_quarto.yml` | Title, language, parts, chapter order, imprint and PDF filename |
| `_brand.yml` | Accent colour, text colour and font families |
| `chapters/*.md` | The text, tables, links and pictures readers will use |
| `_extensions/em-book/typst-template.typ` | Margins, headings, running head and title pages |

## Options in `_quarto.yml`

| Option | Effect | Default |
|---|---|---|
| `document-kind` | Label above the title and on the imprint page | "Manual", German "Handbuch" |
| `part-label` | Word before the part number on a part title page | "Part", German "Teil" |
| `imprint` | Version, date, organisation and author on the back of the title page | No imprint |
| `image-max-height` | Tallest picture in millimetres before it is narrowed | 118 |
| `image-widths` | Fixed width for a named picture file | None |

## Pictures

A tall screenshot rarely fits the rest of a page and leaves it half empty. The
template therefore narrows a PNG until it is at most `image-max-height` tall.
Set a fixed width for one file when a chapter would otherwise end with a few
lines on a new page.

::: {.callout-warning icon=false}
Copy the template into a new directory. Do not replace the configuration or
the chapters of an existing manual without inspecting them first.
:::
