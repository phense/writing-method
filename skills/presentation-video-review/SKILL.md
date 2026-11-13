---
name: presentation-video-review
description: "Use when a finished script of a tutorial or a story video needs its acceptance review before money is spent on voicing, or a produced presentation video must be accepted before delivery: confirming sources and honesty of a tutorial script or the match of a story script with its named edition, every check still, a listening check for pronunciation, pace, pauses and tone, and the measured properties of the rendered file. Records findings with severity, scene and line. Not for writing or correcting the script (use tutorial-video-scripting; a story script returns to the story family), voicing, producing or re-rendering the video (use presentation-video-production), marketing clips or filmed material, or reviewing written documentation or code."
---

# Presentation Video Review

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

[Writing rule #1](../../shared/policies/natural-prose.md) is a criterion at gate 1 for a tutorial script, and applies to the findings this skill writes.

Check a video as its least experienced viewer would meet it, and as the
person who must stand behind every statement in it. Record findings; do not
fix them. Corrections return to scripting or production.

## Recovery preamble

Follow the [recovery gate](../project-backlog/SKILL.md#recovery-gate) and the
[operational handoffs](../project-backlog/SKILL.md#operational-handoffs) of the
backlog skill directly. No documentation skill is part of the video lifecycle.
For an untracked single video the review record on disk is the state.
A story video keeps no run state. Skip this preamble; see [Story scripts](#story-scripts).

## Trigger

A script that is about to be voiced (gate 1), or a rendered video that is
about to be delivered (gate 2).

## Do not use for

- Writing or correcting narration; use `tutorial-video-scripting`, or `story-video-scripting` for a story script.
- Voicing, stills or rendering; use `presentation-video-production`.
- Written documentation (`documentation-review`) or code.

## Consumes

- The video project: script files, `stills/`, `out/measure.json`, the
  rendered file, `video-profile.json`.
- The subject itself, to verify claims against it. For a story script
  instead: the manuscript or listening edition at the revisions named in
  `video.json` and, for a listening edition, the `edition_revision` named in
  `script/script.md`. The vault and the edition file are found from the paths
  in `script/script.md`.

## Produces

`review.md` in the video project, from the
[review template](../../templates/presentation-video/review.md): the state of
both gates and every finding with severity, scene, line and evidence.

Severity: **Critical** – wrong or harmful (false statement, exposed secret,
unmarked recreated interface, unintelligible key term). **Important** – the
viewer is misled or loses the thread (picture contradicts speech, missing
character, term changes, pace or loudness out of range). **Minor** – polish.

## Gate 1: before voicing

Step 1 applies to every script. Steps 2 to 5 judge a tutorial script; a story
script takes the checks under [Story scripts](#story-scripts) in their place.

1. Run `python3 tools/check_script.py`; record errors and undecided warnings.
2. Sources: open each cited source and confirm the claims of its scenes.
   A claim that cannot be confirmed is a finding, not a rewording task.
3. Audience and tone: one audience, one form of address throughout; friendly
   and moderately positive, no hype
   ([writing for listening](../../shared/media/spoken-style.md)).
4. Honesty: recreated interfaces announced near the start; the evidenced /
   approximated / invented list is complete; no secret, credential or private
   data of a real person in text or planned picture.
5. Terms: one term per thing; at most one new term per line, explained
   where it first appears; key terms flagged in the pronunciation list.

The script check is run by scripting as it writes; this gate is the reading
by a second pair of eyes that no tool replaces.

Gate 1 passes with no open Critical or Important finding.

## Gate 2: before delivery

1. **Every check still.** Open each image listed in `stills/stills.json`.
   Mark it `"inspected": true` only after looking at it; write a defect into
   its `"finding"`. `python3 tools/check_review.py` then confirms that every
   line of the current timeline has an inspected still without a finding. The
   gate cannot pass while it exits with an error. Look for:
   - missing characters: an empty box, a gap or a fallback glyph where an
     arrow, symbol or accented letter should be. The template's fonts cover
     Latin and Latin Extended only; any other mark must be drawn or supplied
     by an added font.
   - missing markers: a highlight frame, pointer or badge the line refers to;
   - clipped or overlapping text, text outside the margin or below the
     minimum size, and weak contrast (at least 4.5:1 against the background;
     judged by eye, no tool measures it);
   - a pointer or highlight on the wrong element;
   - a picture that contradicts or lags behind the spoken line;
   - placeholder scenes.
2. **Listening check.** Listen to the whole video once without reading along.
   Note mispronounced terms, wrong emphasis, audible cuts between lines,
   pauses that feel long or missing, a pace that tires or drags, and a tone
   that is flat or exaggerated. Then confirm `python3 tools/verify_speech.py`
   reports no unrecognized key term. Read-back catches a misread word; it
   does not catch a slightly wrong emphasis, which is why the listening
   check is not optional.
3. **Measured file.** `python3 tools/measure.py all <file>` must pass for the
   file that will be delivered, including the version with an opening
   sequence (`--offset`). Do not accept the render's exit status instead.
4. **Captions and chapters.** `out/captions.vtt` exists and its first and
   last cue match the speech; chapter marks are in the project record.
5. **Project record.** The project `README.md` names chapters with time
   marks, sources, voice and provider, and what makes the video stale.

Gate 2 passes when `tools/check_review.py` and `tools/measure.py all` both
exit without error and no Critical or Important finding is open.

## Story scripts

`video.json` with `"purpose": "story"` marks a story video. Its narration is
accepted manuscript (`"edition": "verbatim"`) or an accepted listening edition
(`"edition": "listening"`); see
[writing mode](../../shared/policies/writing-mode.md). The review never judges
or changes its wording, tone or order.

- **Gate 1** replaces the source, tone, honesty and term checks with one
  comparison: every narration line matches the named edition at its
  revision, in order and without gaps. Verbatim: word for word against the
  manuscript at the `revision` under `based_on`; only the cut into scenes and
  lines may differ. Listening: word for word against the edition file named
  in `script/script.md`, at the `edition_revision` named there; the edition's
  `based_on_revision` must equal the `revision` under `based_on`. An edition
  file at another revision than the one `script/script.md` names makes the
  script stale: an Important finding. The comparison is on the caption
  `text`. Every `speak` form is read against its `text`: it may respell the
  same words for the voice, never add, drop, replace or reorder a word; the
  script check's similarity threshold does not prove this. A difference is a
  finding, Critical when words were changed, added or dropped. Also confirm one audience and
  form of address in `video.json`, that invented names and other key terms
  are in the pronunciation list, and that no secret or private data of a real
  person is in text or planned picture. The checks for recreated interfaces
  apply only when `recreated` is set.
- **Gate 2** is unchanged except for the listening check: judge
  pronunciation, pace, pauses and audible cuts, not style. A tone or a
  sentence the reviewer would have written differently is not a finding.
  Re-read every `speak` form added or changed since gate 1 against its
  `text` under the same rule. The
  project record names the edition and the manuscript revisions in place of
  sources.
- Wording findings return to `story-video-scripting` and the author: a
  transcription error is fixed against the manuscript; any other change is an
  author decision. They never go to `tutorial-video-scripting`.
- The tutorial listening style in `shared/media/spoken-style.md` does not apply to story narration.
- The review record takes the story rows named in the review template in
  place of the source and tone rows, and records no tone judgement.
- A story video keeps no run state. Do not open the backlog skill and create no run
  directory; the review record in the video project is the state.

## Completion

`review.md` records both gates. Return actionable findings to the owning
phase; after corrections, review the affected scenes again and re-run the
measurement on the new file.

## Next phase

`verification-before-completion` when gate 2 has passed; otherwise back to
`tutorial-video-scripting` (content of a tutorial script),
`story-video-scripting` (wording of a story script) or
`presentation-video-production` (picture, sound, file).

## Supporting skills

- `terminology-guard` for term consistency of a tutorial script.
- `verification-before-completion` for the final ready claim.
