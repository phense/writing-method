# Review: <video title>

- Video: `<video id>`
- Script revision reviewed: <commit or date>
- File reviewed: `<path>` (<length>, <date rendered>)
- Reviewer: <name or agent>

## Gate 1: before voicing

| Check | Result | Evidence |
|---|---|---|
| Script check without errors | <pass / fail> | `python3 tools/check_script.py` |
| Sources confirm the claims of their scenes | | |
| One audience, one form of address, friendly tone | | |
| Recreated interfaces announced; evidence list complete | | |
| No secret, credential or private data | | |
| Key terms flagged in the pronunciation list | | |

Gate 1: <passed / open> on <date>

## Gate 2: before delivery

| Check | Result | Evidence |
|---|---|---|
| Every check still inspected | <n of n> | `python3 tools/check_review.py` |
| Listening check, whole video | | |
| Read-back: no unrecognized key term | | `python3 tools/verify_speech.py` |
| Measured file passes | | `out/measure.json` |
| Captions and chapter marks present | | `out/captions.vtt`, `out/chapters.txt` |
| Project record complete | | `README.md` |

Gate 2: <passed / open> on <date>

## Findings

Severity: Critical (wrong or harmful), Important (misleads or loses the
viewer), Minor (polish). A video is ready only with no open Critical or
Important finding.

| ID | Severity | Scene | Line | Finding | Evidence | Status |
|---|---|---|---|---|---|---|
| F-01 | | | | | | Open |
