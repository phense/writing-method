---
id: C-004
title: Check the finished PDF
type: task
doc_id: book-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-11-13
---

# Check the finished PDF {#sec-check}

## Run the checker

The checker reads the PDF and reports what a reader would stumble over. It
needs Python with PyMuPDF.

1. Render the book as described in @sec-start.
2. Run `python3 tools/check-pdf.py _book/manual.pdf`.
3. Read the list under `errors`. An empty list and exit status 0 mean that the
   checks passed.

## What it checks

The checker covers the following points:

- Every chapter opens on a right-hand page, with its heading visible there.
- Every page carries a page number, except the title page, its back, part
  title pages and empty left-hand pages.
- Each entry in the table of contents names the page that its link opens.
- No text or picture runs into the margins, and no lines overlap.
- No chapter ends with only a few lines on its last page.

## Look at the pages

A checker does not judge appearance. Look at the title page, one part title
page, one chapter opening, a table and the last page before you pass the PDF
on.
