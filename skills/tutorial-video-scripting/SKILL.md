---
name: tutorial-video-scripting
description: "Use when a narrated tutorial video must be scripted from source material: a video that teaches a concept or walks through a procedure for one named audience. Writes the script with chapters, scenes, narration lines written for listening, sources and the pronunciation list, and runs the automatic script check until it passes. Not for producing or rendering the video (use presentation-video-production), reviewing a finished video (use presentation-video-review), marketing or social clips, filmed material or screen recordings, or written documentation. Not for story manuscripts or in-world text."
---

# Tutorial Video Scripting

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Write the script of a tutorial video: what is said, in which order, and what
the viewer sees while it is said. The script is finished when a person has
reviewed it and the script check passes. Nothing is voiced in this phase.

A **presentation video** is composed from designed scenes and synthesized
narration; nothing is filmed. **Tutorial** names its purpose. This skill owns
the purpose; [presentation-video-production](../presentation-video-production/SKILL.md)
owns the form.

## Recovery preamble

Follow the [recovery gate](../project-backlog/SKILL.md#recovery-gate) and the
[operational handoffs](../project-backlog/SKILL.md#operational-handoffs) of the
backlog skill directly. No documentation skill is part of the video lifecycle.
A single video whose project backlog tracks no stable work ID needs no run:
record the verified-absent discovery in the reply and treat the committed
script as the checkpoint.

## Trigger

A request for a tutorial, training, onboarding or explainer video for a named
audience, or for a change to the content of an existing one.

## Do not use for

- Voicing, building scenes or rendering; use `presentation-video-production`.
- The acceptance review of a finished script or video; use
  `presentation-video-review`.
- Marketing or social clips, filmed material, screen recordings.
- A written guide on the same subject; use `documentation-authoring`.
- Story manuscripts or in-world text; the story family owns them, under
  [writing mode](../../shared/policies/writing-mode.md).

## Consumes

- Topic, audience, form of address and learning goal. Ask for what is missing;
  do not invent an audience.
- Source material, inspected directly: the product, its documentation, its
  code or screenshots. Record the date read.
- The video profile of the target project (`video-profile.json`). If none
  exists, create it from the
  [example](../../templates/presentation-video/video-profile.example.json),
  ask only for values that cannot be inferred (language, provider, voice and
  its languages), and use it from then on.
- [Writing for listening](../../shared/media/spoken-style.md).

## Produces

In the video project (a copy of the
[project template](../../templates/presentation-video/README.md), created by
this skill if absent):

| File | Content |
|---|---|
| `video.json` | Identifier, title, one audience, form of address, goal, whether interfaces are recreated, what makes the video stale |
| `script/script.md` | For the human reviewer: audience, goal, tone, chapters and scenes, sources, what is evidenced, approximated and invented, key terms |
| `src/scenes.json` | Scene order; per scene its key (lowercase letters, digits, `_`), chapter, one message and sources |
| `src/narration.json` | Per scene the narration lines: `text`, optional `speak`, `show`, `min`, `notice` |
| `pronunciation.json` | Terms with a fixed spoken form; key terms flagged |

## Workflow

1. **Fix the frame.** One audience, one form of address, one learning goal.
   Two audiences mean two scripts; they may share scenes in one project.
2. **Collect and date the sources.** Read the subject itself. List each
   source in `script/script.md` with an ID (`S1`, `S2`, ...). A claim without
   a source is marked unverified, never stated as fact.
3. **Outline chapters and scenes.** Each scene carries exactly one message
   and names what is on screen. Order follows the viewer's task, not the
   product's menu. Apply `explaining-concepts` to concept scenes and
   `writing-procedures` to step scenes.
4. **Write the narration** with
   [writing for listening](../../shared/media/spoken-style.md) and
   `human-prose-drafting` from the first sentence: one thought per line,
   friendly and moderately positive, numbers and abbreviations in speakable
   form. Let `terminology-guard` hold one term per thing.
5. **Be honest about the picture.** If interfaces are recreated or people and
   data invented, set `"recreated": true`, flag one early line as
   `"notice": true`, and fill the evidenced / approximated / invented list.
   Never put a secret, a live credential or a real person's private data
   into narration or picture.
6. **Fix pronunciation once.** Enter abbreviations, product names and foreign
   words in `pronunciation.json`. Flag as `key` every term the video depends
   on, starting with the term in its title.
7. **Run the script check** from the video project:

   ```sh
   python3 tools/check_script.py
   ```

   It reports each violation with scene and line and estimates the length.
   Errors block voicing; resolve them and decide each warning.
8. **Length.** There is no target length for a tutorial video. Only when the
   estimate exceeds the profile's maximum (default 45 minutes) does the check
   demand a split; it proposes a chapter boundary. Make each part complete on
   its own, with its own opening and closing scene.
9. **Hand the script to the author for review** before voicing: voicing costs
   money and a changed script costs it again.

## Completion

The script check exits without errors, every warning is decided, the author
has accepted `script/script.md`, and the key terms are listed.

## Next phase

`presentation-video-production`

## Supporting skills

- `explaining-concepts`, `writing-procedures`, `human-prose-drafting`,
  `terminology-guard` while writing.
- `project-backlog` when the video is tracked under a work ID.
