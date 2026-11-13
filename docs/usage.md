---
type: reference
audience: Authors using Writing Method
version: 0.4.1
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
worked). The draft is written under writing rule #1 (natural prose), which
`human-prose-drafting` applies to documentation from the first sentence, so
no humanizing pass follows. A recorded self-review and fresh link
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

For a long manual grouped into parts, or one that is printed on both sides,
ask for the book layout:

> Build this handbook as a book PDF with parts, for duplex printing.

`documentation-pdf` then copies the [book template](../templates/documentation/book/DESIGN.md),
lists the parts and chapters in `book.chapters`, and renders with
`quarto render --to em-book-typst`. Chapters open on right-hand pages and the
running head names the part and the chapter. Run `python3 tools/check-pdf.py`
in the copy to check page numbers, contents entries, margins and chapter
openings.

## Make a narrated tutorial video

> Make a tutorial video that shows new staff how to request leave in the HR
> portal. Source: docs/leave.md. We have no video profile yet.

`tutorial-video-scripting` asks for what it cannot infer (language, speech
provider, voice and the languages it speaks) and writes `video-profile.json`.
It copies the project template, then writes the script: one audience, one
message per scene, narration in short spoken sentences, a source for every
claim, and the key terms in the pronunciation list. `python3
tools/check_script.py` must report no errors, and you accept the script,
before anything is voiced.

`presentation-video-production` first voices one line per key term so you can
hear them, then the rest. `python3 tools/timeline.py` derives every start time
from the measured sound, `node tools/stills.mjs stills` renders one still per
line, and `tools/render.sh` produces the file. `python3 tools/measure.py all
out/<id>.mp4` ends with `PASSED` when resolution, loudness and the pause
between sentences match the profile.

`presentation-video-review` looks at every still, listens to the video once
and records its findings in `review.md`. The video is ready when no Critical
or Important finding is open.

## Correct one sentence in a finished video

> In the leave video, the sentence about the approval step names the wrong
> button. Fix it.

`presentation-video-production` edits the line in `src/narration.json` and
runs voicing again: one request is sent, because every other line is reused.
The timeline moves all later lines by itself. The stills of that scene, the
render and the measurement are repeated, and the review checks the changed
scene.

## Draft a chapter in a story vault

The story family is experimental. It applies inside a story vault: a directory
copied from `templates/story-vault/` whose `00-project/brief.md` reads
`kind: story`.

> Draft chapter 12 from its chapter card.

`story-drafting` first checks the vault: the kind must be `story`, and
viewpoint, tense and distance must be set in `00-project/voice.md`. It then
reads the chapter card in `05-plot/chapters/` and writes prose only, into
`06-manuscript/chapters/`. The voice sheet decides how the prose sounds.
`explaining-concepts`, `writing-procedures`, `empathic-troubleshooting` and
`human-prose-drafting` do not apply to it: a chapter gets no analogy, no
numbered steps and no smoothing of deliberate fragments. If one of the three
voice fields is still `unset`, no chapter is drafted and you are led to a
voice trial first. The chapter is complete when `story-canon-review` has
reviewed it at a named revision and you have accepted it; your acceptance is a
decision, not a command result.

## Turn an accepted chapter into a narrated video

> Turn chapter 11 into a narrated video. Read it exactly as it is written.

`story-video-scripting` checks the vault as `story-drafting` does, then checks
that the chapter is accepted at a named revision. It copies the video project
template to the directory you name, outside `06-manuscript/`, and writes the
script files. `video.json` records `"purpose": "story"`, `"edition":
"verbatim"` and the chapter with its revision. Every narration line is the
manuscript text, cut at sentence boundaries; no word is added, dropped or
changed. A scene's picture is a plain description in `script/script.md`.
`python3 tools/check_script.py` must report no errors; a story script needs no
source table. The script is ready when you have accepted it.

If the text should differ for the ear, ask for a listening edition instead.
Each difference from the manuscript is then your decision and is recorded in
an edition file under `06-manuscript/editions/listening/`. The chapter itself
stays unchanged.

`presentation-video-production` then voices and renders the accepted script as
it is, and `presentation-video-review` checks each narration line against the
named edition. A finding about wording returns to `story-video-scripting` and
to you, never to a rewrite during production. This path is experimental: no
video has been produced with it, and the pronunciation of invented names and
the origin of the pictures are not designed yet.

## Ask a question inside a story vault

> Why does chapter 11 feel slow, and what should I look at first?

This is a reply to you, so it stays an ordinary reader-oriented reply even
though the session is inside a story vault and the subject is the story. The
answer explains plainly, names what to check first and does not imitate the
story's voice. The voice sheet styles manuscript files only. If the reply
contains a draft passage, the passage stands apart in a fenced block or a
prose file and follows the voice sheet, and the text around it does not. The
rule for each kind of text is in
[writing mode](../shared/policies/writing-mode.md).
