---
name: presentation-video-review
description: "Use when a finished tutorial video script needs its acceptance review before money is spent on voicing, or a produced presentation video must be accepted before delivery: confirming sources and honesty of the script, every check still, a listening check for pronunciation, pace, pauses and tone, and the measured properties of the rendered file. Records findings with severity, scene and line. Not for writing or correcting the script (use tutorial-video-scripting), voicing, producing or re-rendering the video (use presentation-video-production), marketing clips or filmed material, or reviewing written documentation or code."
---

# Presentation Video Review

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Check a video as its least experienced viewer would meet it, and as the
person who must stand behind every statement in it. Record findings; do not
fix them. Corrections return to scripting or production.

## Recovery preamble

Follow the [recovery gate](../project-backlog/SKILL.md#recovery-gate) and the
[operational handoffs](../project-backlog/SKILL.md#operational-handoffs) of the
backlog skill directly. No documentation skill is part of the video lifecycle.
For an untracked single video the review record on disk is the state.

## Trigger

A script that is about to be voiced (gate 1), or a rendered video that is
about to be delivered (gate 2).

## Do not use for

- Writing or correcting narration; use `tutorial-video-scripting`.
- Voicing, stills or rendering; use `presentation-video-production`.
- Written documentation (`documentation-review`) or code.

## Consumes

- The video project: script files, `stills/`, `out/measure.json`, the
  rendered file, `video-profile.json`.
- The subject itself, to verify claims against it.

## Produces

`review.md` in the video project, from the
[review template](../../templates/presentation-video/review.md): the state of
both gates and every finding with severity, scene, line and evidence.

Severity: **Critical** – wrong or harmful (false statement, exposed secret,
unmarked recreated interface, unintelligible key term). **Important** – the
viewer is misled or loses the thread (picture contradicts speech, missing
character, term changes, pace or loudness out of range). **Minor** – polish.

## Gate 1: before voicing

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

## Completion

`review.md` records both gates. Return actionable findings to the owning
phase; after corrections, review the affected scenes again and re-run the
measurement on the new file.

## Next phase

`verification-before-completion` when gate 2 has passed; otherwise back to
`tutorial-video-scripting` (content) or `presentation-video-production`
(picture, sound, file).

## Supporting skills

- `terminology-guard` for term consistency.
- `verification-before-completion` for the final ready claim.
