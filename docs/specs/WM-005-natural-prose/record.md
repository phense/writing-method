# WM-005: Writing rule #1, natural prose

Maintainer requirement of 2026-11-13: no text this method produces may read as
machine-written, and this ranks first among the writing rules.

## What was built

- `shared/policies/natural-prose.md`: the rule, five causes, five pattern
  groups, what to write instead, the delivery check, exceptions, scope by
  writing mode, limits and sources.
- Every skill of the family map that writes or judges text refers to it. The
  story skills reach it through `shared/story/rules.md`, below the voice
  sheet; fragments and repetition stay devices of prose.
- `human-prose-drafting` holds the documentation additions and is selected
  for a short standalone text that no other skill covers.

## Evidence

- `python3 -m unittest discover -s tests -t .`: 318 tests, OK.
  `tests/test_natural_prose.py` derives the carriers from the family map.
- Two independent reviews with verification of each finding (13 findings,
  then 8), all applied. The last edits were not reviewed again.
- Unscripted routing on Claude, coordinator model, 3 runs per case, at
  `88f2b07`: 10 of 10 cases pass with 30 of 30 hits. The new case
  `team-announcement` loaded `human-prose-drafting` in 3 of 3 runs.
- Unscripted routing on Codex against the installed 0.5.0, 3 runs per case:
  9 of 10 cases pass with 29 of 30 hits. `team-announcement`: 3 of 3. One
  run of `tutorial-video` loaded `human-prose-drafting` and
  `writing-procedures` in place of `tutorial-video-scripting`. Whether the
  wider description of `human-prose-drafting` caused this is not known; the
  case was not rerun.
- Published: release `v0.5.0` with a reproducible archive; the downloaded
  archive matches `SHA256SUMS`. Installed on Claude and Codex.

## Limits

- The rule is carried by skills. A reply for which no skill loads is not
  reached; the shared-core skills do not refer to it.
- No check measures whether produced text is free of the patterns.
