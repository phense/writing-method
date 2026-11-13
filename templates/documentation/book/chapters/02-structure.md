---
id: C-002
title: Parts and chapters
type: concept
doc_id: book-example
readers: [R1]
status: reviewed
version: Quarto 1.10.18
last_reviewed: 2026-11-13
---

# Parts and chapters {#sec-structure}

## How the book is divided

A long manual serves several groups of readers. A part collects the chapters
for one group or one subject, so that a reader can find and print their share.

Each part contributes three things to the PDF:

- a coloured title page that lists its chapters with page numbers,
- a heading in the table of contents,
- a grey label in the running head of every page of its chapters.

## Where the parts come from

Parts are not written in the chapters. List them in `book.chapters` in
`_quarto.yml`, each with a title and its chapter files. Chapters listed outside
a part, such as a preface, appear without a label.

> A chapter always opens on a right-hand page. The left-hand page before it
> stays empty when the previous chapter ends on a right-hand page.

## Running head and page numbers

The running head shows the part, the chapter number and the chapter title. The
page number stands at the outer edge, where a thumb finds it. A page that opens
a chapter has no running head; its page number stands in the footer.
