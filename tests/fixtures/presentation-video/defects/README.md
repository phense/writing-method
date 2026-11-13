# Seeded-defect project

A small script with five planted defects, used to prove that the review finds
them (specification WM-001, US-003).

| # | Defect | Where | Found by |
|---|---|---|---|
| 1 | Caption says something else than the spoken form | `open:1` | `tools/check_script.py`, rule `caption-speech` |
| 2 | Claim without a source | scene `sync` | `tools/check_script.py`, rule `sources` |
| 3 | Recreated interface not announced | whole video | `tools/check_script.py`, rule `notice` |
| 4 | Loudness out of range | rendered file | `tools/measure.py`, row `loudness (LUFS)`; the test generates a quiet file |
| 5 | Missing character on screen: the caption of `open:0` uses the arrow "→", which the template fonts do not contain | check still `open-00.png` | Looking at the still (review gate 2); no tool reports it |
