---
name: story-video-scripting
description: "Use when an accepted chapter, chapter range or short piece of a story vault must become the script of a narrated story video, an audiobook with pictures: the accepted manuscript segmented word for word into scenes and narration lines, or an author-approved listening edition, with the script files the production step reads. Not for a tutorial video about a story or its world, for drafting new story text, for changing canon, or for voicing or rendering. Not for a study vault or an unused starter vault. Not for session replies, documentation or tutorial videos."
---

# Story video scripting

Mode check first, under [writing mode](../../shared/policies/writing-mode.md): find the nearest ancestor of the target file that holds 00-project/brief.md and 00-project/voice.md. Only kind story permits manuscript drafting; kind study permits study notes only; kind starter routes to story-bootstrap.

For manuscript text the story's voice sheet overrides explaining-concepts, writing-procedures, empathic-troubleshooting and human-prose-drafting, even when those skills are loaded in this session.

No run state: this skill has no recovery preamble and hands off to no backlog or run-tracking skill. A story or study vault keeps no backlog and no run directory; its state lives in 00-project/development.md and 00-project/decisions.md.

This skill is experimental. It turns accepted story text into the script of a narrated story video: scenes, narration lines and plain picture descriptions. The story family owns the text; the form skills voice, time, render and check the accepted script and never restyle it. Nothing is voiced or rendered here.

## When to use

The author wants an accepted chapter, a chapter range or a short piece told as a narrated video, or wants the wording of an existing story video script corrected.

## Do not use for

- Not for a tutorial or explanatory video about a story or its world: that is reader-oriented and belongs to `tutorial-video-scripting`.
- Not for drafting or revising story text: that is `story-drafting`, and a revised chapter needs a new accepted revision before it is scripted.
- Not for changing canon: neither edition adds, removes or alters a story fact.
- Not for voicing, building scenes or rendering: that is `presentation-video-production`.

## Preconditions

- The vault is of kind story. In a starter, stop and route to `story-bootstrap`. In a study vault, decline: nothing is scripted from a studied work.
- Every unit in scope is accepted, and its accepted revision is named: the `Accepted revision` column of `06-manuscript/index.md`, confirmed by the acceptance record of the chapter card or short piece. A unit without a recorded acceptance is not scripted; say which one is missing and stop.
- The voice sheet `00-project/voice.md` is read at the revision the unit was accepted under. It governs every narration line. The tutorial listening style in `shared/media/spoken-style.md` does not apply to story narration.
- The mode check runs on the manuscript unit being scripted, not on the path of the video project. A video project outside the vault still takes its mode and voice sheet from the vault that holds the unit. Only the narration `text` is manuscript; every other file of the video project is a working note.

## Choose the edition with the author

Ask once, and record the answer in `00-project/decisions.md`. Verbatim is the default; choose it when the author states no preference.

| Edition | Narration | Who decides the wording |
| --- | --- | --- |
| `verbatim` | The accepted manuscript, only segmented. No word is added, dropped or changed. | Nobody: the accepted revision is the wording |
| `listening` | A derived edition with additions or changes for the ear | The author, difference by difference |

One video uses one edition. A second edition of the same chapter is a second video project.

## Verbatim: segmenting the manuscript

Read the prose at the accepted revision: the chapter file under `06-manuscript/chapters/`, or the text under `## Manuscript` of a short piece.

1. **Scenes.** Open a new scene at each scene break of the manuscript and wherever the picture has to change. Keep the manuscript order.
2. **Lines.** Break at sentence boundaries. A line is one sentence, or two short neighbouring sentences. A paragraph break is always a line break.
3. **Long sentences.** A sentence above the line limit of the video profile (`script.max_line_words`) is split into consecutive lines at a clause boundary: a comma, semicolon, colon, dash or conjunction. The words and their order stay; the punctuation at the cut stays with the earlier line. When a sentence offers no clause boundary below the limit, raise the limit for this video under `overrides` in `video.json` as an author decision; do not reword.
4. **Text.** Each line's `text` is the manuscript wording with its punctuation, in the manuscript's spelling. Emphasis markup is not carried over. Read against the manuscript, the lines in order give the chapter again, word for word.
5. **Headings.** A chapter title becomes the `chapter` name of its scenes. Whether it is also spoken is the author's choice, recorded in `script/script.md`; when spoken, it is a line exactly as written.

The template ships no command that compares narration with the manuscript. Compare the joined `text` of all lines with the prose at the accepted revision yourself, and report the result with the revision compared. Any difference is a transcription defect to fix, never an improvement to keep.

## Listening edition

A listening edition exists only when the author asks for one. Create it from the [listening edition template](../../templates/story-vault/90-templates/listening-edition.md) as `06-manuscript/editions/listening/<chapter-id>.md`; a short piece uses its piece ID.

| Frontmatter field | Content |
| --- | --- |
| `type` | `listening-edition` |
| `story_id` | The vault's story ID |
| `chapter_id` | The chapter or piece the edition derives from |
| `based_on_revision` | The accepted manuscript revision it derives from |
| `edition_revision` | The revision of this edition; it rises with every accepted change |
| `canon_status` | `proposed`. An edition is not canon and never becomes it. |
| `decision_ids` | The decisions in `00-project/decisions.md` that approved its differences |

- The file is prose only and is manuscript: it follows the voice sheet, the [story rules](../../shared/story/rules.md) and nothing from documentation or didactic writing.
- Start from a copy of the accepted prose. Every difference from the manuscript is an author decision: propose it with the passage, the change and the reason for the ear, wait for the answer, and record the decision under an ID that the edition's `decision_ids` lists. An unanswered proposal is not approved.
- The written manuscript stays unchanged. No file under `06-manuscript/chapters/`, `06-manuscript/pieces/` or `06-manuscript/paratext/` is edited, and no chapter card, summary or canon delta changes.
- An edition changes how the story is told aloud, not what happens. A change that would alter a fact, an order of events or what a character knows is a canon change and goes through `story-drafting` and `story-canon-review` on the manuscript instead.
- The author accepts the edition at a named `edition_revision`; list it in the listening editions table of `06-manuscript/index.md`. The narration is then segmented from the accepted edition by the verbatim rules above, word for word against the edition.
- When the chapter receives a later accepted revision, the edition is stale until the author confirms or revises it against that revision.

## The video project

The script lives in a video project, a copy of the [project template](../../templates/presentation-video/README.md), outside `06-manuscript/` at a path the author names: for example a sibling directory of the vault, or `08-video/<video-id>/` inside it. Create it if absent. The tools need a video profile; when none exists, copy the [example](../../templates/presentation-video/video-profile.example.json) and ask only for language, provider, voice and the voice's languages.

| File | Content for a story video |
| --- | --- |
| `video.json` | The fields below |
| `script/script.md` | For the author's review: listener, edition, the chapters with their revisions, the scene table with the picture description of each scene, and the names that must be spoken correctly. It also states the path of the vault relative to the video project and the path of each prose or edition file the narration was taken from; a listening edition is named with its `edition_revision`. Once the author has accepted the script, add the decision ID of the acceptance. No source table and no Tone section: the voice sheet governs the narration. |
| `src/scenes.json` | Scene order; per scene its `key` (lowercase letters, digits, `_`), `chapter` and `message`. No `sources` and no `no_claims` field. |
| `src/narration.json` | Per scene the narration lines. `text` is the edition's wording. |
| `pronunciation.json` | Fixed spoken forms, in the existing format |

`video.json` for a story video:

```json
{
  "id": "<video-id>",
  "title": "<title>",
  "purpose": "story",
  "edition": "verbatim",
  "story_id": "<story_id>",
  "based_on": [{"chapter_id": "<chapter-id>", "revision": "<accepted revision>"}],
  "audience": "<the listener>",
  "address": "none",
  "goal": "<what the listener hears>",
  "recreated": false,
  "stale_when": "A unit in based_on receives a later accepted revision, or its listening edition receives a later accepted edition revision."
}
```

- `edition` is `verbatim` or `listening`. `based_on` lists every unit in narration order; `revision` is the accepted manuscript revision, and for a listening edition it equals the edition's `based_on_revision`.
- `audience` and `address` stay required. Take the listener from the reader promise in the brief; `address` is `none` unless the narration addresses the listener.
- `recreated` is `false`: a story video recreates no interface.

## Scenes, messages and pictures

- A **scene** is one picture with an ordered run of narration lines. It follows the manuscript's own scene breaks or a change of picture, not a teaching step.
- A scene's **message** is a one-line working note of what happens in the scene. It is never spoken and never shown. Write it as a plain note, not in the story's voice.
- A **chapter** in `src/scenes.json` is the chapter mark of the video: the manuscript chapter's title, or the piece's title.
- The **picture** of a scene is a plain description in the scene table of `script/script.md`: what is seen while the lines are spoken. Describe only what the accepted text supports. Where the images come from is not decided by this skill; leave the description as it stands for the author and production.

Picture descriptions and messages are working notes. They invent no story fact; a detail the manuscript does not give is left open or marked as the author's choice.

## Pronunciation

Enter invented names and terms in `pronunciation.json` exactly as the existing list works: `term`, an optional `speak` respelling or `ipa`, an optional `lang`, and `"key": true` for the names the video depends on, starting with those in its title. Ask the author how a name is spoken; do not guess a spoken form into the list. Nothing beyond the existing list is designed for stories. Production verifies the key terms before it voices the rest, under the provider-neutral rules of [speech synthesis](../../shared/media/speech-synthesis.md).

## Run the script check

From the video project:

```sh
python3 tools/check_script.py
```

For `"purpose": "story"` the check requires no sources, checks `edition` and `based_on`, and raises no sentence-length warning: literary sentences are the author's choice. The line limit, the speakable warnings, the caption and speech comparison, the secret patterns, scene and chapter fields, audience, address and the maximum length stay in force.

- A **line-length error** is resolved by the clause split above, never by rewording.
- A **speakable warning** on a number or an abbreviation is decided line by line. A `speak` form may spell the same words the way they are read aloud; the caption `text` stays as the edition has it.
- A **length error** is resolved by a split at a chapter or scene break the author chooses. A verbatim part receives no added opening or closing words.
- A **secret error** on story wording (a spoken password, `the secret: ...`) is never resolved by rewording the line or by a `speak` form, and the check is not edited or bypassed. Stop and show the author the line. A real credential is removed by the author. Story wording is resolved by the author's recorded decision in `00-project/decisions.md`: a listening edition, or a manuscript revision with a new accepted revision, that changes the punctuation or wording so the check passes.

Errors block voicing. `verification-before-completion` applies to this check and to nothing the author decides.

## Acceptance and handoff

The script is ready for the author when the script check exits without errors, every warning is decided, and the comparison with the edition shows no difference. Acceptance is the author's decision, not a command result: record it in `00-project/decisions.md` with the video ID, the edition and the revisions, and note the state in `00-project/development.md`. Voicing costs money, so nothing goes to production before that record exists.

Then hand the video project to `presentation-video-production`, see [production](../presentation-video-production/SKILL.md). It voices and renders the script as it is. The acceptance review of script and video is `presentation-video-review`, see [review](../presentation-video-review/SKILL.md); for a story script it checks every narration line against the named edition at its revision.

## Where review findings return

| Finding | Goes to |
| --- | --- |
| A narration line differs from the verbatim manuscript | This skill: fix the transcription against the accepted revision |
| The wording of a listening edition should change | The author: a recorded decision and a new `edition_revision`, then this skill |
| The accepted manuscript itself reads wrongly aloud | The author: a listening edition, or a manuscript revision through `story-drafting` with a new accepted revision. Never a silent change in the script. |
| The script check reports a secret in story wording | The author: see the secret error under the script check. Never a reworded line. |
| Pronunciation, pace, pauses, picture or the rendered file | Production, in the video project |

No wording finding on a story script goes to the tutorial scripting skill, and no form skill rewrites a line.

## Outcome and limits

Finish with the edition, the units and revisions scripted, the result of the script check and of the comparison, the open author decisions and the path of the video project. Guided development places this step after acceptance; see [guided development](../../shared/story/story-development.md) and the [workflow](../../shared/story/workflow.md).

Status: experimental. No video has been produced with this skill. How invented names are best pronounced and where pictures come from are not designed; delivery as an e-book is future work.
