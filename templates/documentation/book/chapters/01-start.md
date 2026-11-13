---
id: C-001
title: Build the book
type: task
doc_id: book-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-11-13
---

# Build the book {#sec-start}

## Goal

Create one PDF, set as a book, from the Markdown chapters in this directory.

## Before you start

Install Quarto 1.10.18. Copy the font files named in `_brand.yml` into the
`fonts` directory. The sample uses Source Sans 3, which is published under the
SIL Open Font License.

::: {.callout-note icon=false}
The PDF is built on your machine. You need neither a Typst account nor a
browser session.
:::

## Build the document

1. Open a terminal in the copied template directory.
2. Run the two commands below.
3. Open `_book/manual.pdf`.

```sh
quarto --version
quarto render --to em-book-typst
```

## Check that it worked

The PDF opens with a title page. The contents start on page 3, and
@sec-structure starts on a right-hand page after the title page of its part.
