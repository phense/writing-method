---
type: reference
audience: Authors using Writing Method
version: 0.1.0
---
# Writing examples

These examples apply to Writing Method. Shared state and playbooks are bundled from Method Core.

## Write one document

> Write a how-to guide that shows an administrator how to rotate an API key.
> One reader group; no other documentation exists yet.

The writing-depth policy places this at the medium scale. `documentation-authoring`
runs in standalone mode: it defines the reader and version, uses the task
skeleton from the chunk template, and applies `writing-procedures` (goal,
prerequisites, blocks of three to five imperative steps, a check that it
worked). The draft is written under `human-prose-drafting` from the first
sentence, so no humanizing pass follows. A recorded self-review and fresh link
check close the work. No plan directory is created.

## Build a documentation set

> Create the complete user manual: about twelve chapters for administrators,
> end users and support staff, with shared terminology and screenshots.

Several readers, shared terms and images and many sessions place this at the
large scale. `documentation-planning` records the scale decision and writes
`docs/writing/<doc-id>/plan.md` with readers, information architecture and a
chunk manifest, plus `glossary.md` and `assets.md`. `documentation-authoring`
then writes one Markdown file per chunk with frontmatter, using
`explaining-concepts`, `writing-procedures` and `empathic-troubleshooting`
per content type, `human-prose-drafting` for sentence-level constraints while
writing, `terminology-guard` for terms and `visual-placeholders` for image
callouts. `documentation-review` checks the set at a named revision
and returns findings to authoring; acceptance needs zero open Critical or
Important findings and fresh verification.

## Explain, instruct or troubleshoot in a reply

> Why does the retry queue drop messages after a restart, and what should I
> check first?

Outside documentation projects, the reader-oriented output policy applies the
same skills to ordinary replies: the explanation opens with an everyday
analogy and avoids undefined jargon, the next steps are numbered imperative
actions with exact locations and a visible result, and help with a failure
starts from the symptom the user sees. Evidence and verification rules do not
change.

## Export reviewed Markdown to PDF

> Build one PDF from these accepted chapters, in plan order, with the manual
> design, table of contents and page numbers.

`documentation-pdf` uses Quarto and its bundled Typst engine after content
review. Copy the [manual template](../templates/documentation/pdf/DESIGN.md)
to a new documentation root, map the accepted manifest rows to `book.chapters`
in `_quarto.yml`, and set title, language, output name and `_brand.yml`.
From that directory, run `quarto render --to em-manual-typst`. The default
result is `_book/manual.pdf`. Inspect the actual contents links, page totals
and page layout before delivery. This export preserves Markdown sources and
does not publish remotely or re-run Humanizer over the finished text.
