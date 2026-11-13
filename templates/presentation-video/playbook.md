# PB-WM-VIDEO-001: Produce and deliver a presentation video

Template. Copy it to `docs/playbooks/system/PB-WM-VIDEO-001.md` in the target
project, replace every `<...>` with the values of that project's video
profile, and remove this paragraph. Review it with `playbook-review` and
rehearse it once on the sample video before relying on it.

## Identity and scope

- Class: system
- Origin: Writing Method, specification WM-001 (US-002, US-004)
- Audience and owner: an author or assistant with the video project and a
  configured speech provider, without knowledge of earlier videos; owner
  <role>
- Target: one video project, authoring machine <name>, render machine
  <name or "none">, speech provider <azure | elevenlabs>
- Readiness deadline: before the first video is delivered from this project
- Last edited: <date>
- Review and rehearsal evidence: <relative link>

## When to use / when not to use

Use when an accepted script is to become a delivered video, or when a
delivered video is corrected. Do not use to write the script or to decide
whether a video is acceptable: those are scripting and review.

Outcome: a file at <delivery location> whose measurement passed and whose
review gate 2 is recorded as passed.

## Before starting

Run from the video project. Each check must succeed before step P1.

| Check | Command | Expected |
|---|---|---|
| Profile | `python3 tools/profile.py` | Prints the profile; no error |
| Script | `python3 tools/check_script.py` | `0 error(s)` |
| Media tools | `ffmpeg -version && ffprobe -version && node --version` | Three version lines |
| Provider (Azure) | `python3 tools/voice_azure.py --check` | `credentials accepted` |
| Provider (ElevenLabs) | List voices through the connector | A voice list |
| Render machine, if used | `ssh <host> 'node --version && ffmpeg -version \| head -1'` | Two version lines |

Authority and impact: voicing spends provider quota or credits; rendering
uses the render machine's processor for minutes; delivery overwrites
<delivery location>/<file name> if it exists. Nothing else is changed.

## Decision paths and actions

| Step | Actor and target | Condition / action | Expected evidence | Failure / next step |
|---|---|---|---|---|
| P1 | Author, project | `python3 tools/verify_speech.py --samples`, then voice the listed lines and listen | Each key term spoken correctly | Wrong term: correct `pronunciation.json`, repeat P1 |
| P2a | Author, Azure | Per-line mode: `python3 tools/voice_azure.py` | `N lines, … new` | Stops with `stopped at <scene>:<line>`: go to R1 |
| P2b | Author, connector | Per-scene mode: one generation per scene, store as `takes/<scene>-take1.mp3`, transcribe, `python3 tools/split_takes.py` | `<scene>: … (match 0.9x)` per scene | Generation error or timeout: go to R2. Take rejected: go to R3 |
| P3 | Author, project | `python3 tools/timeline.py && python3 tools/measure.py pace` | `PASSED` | `text changed after voicing`: repeat P2. Pace out of range: adjust wording or pause, repeat P2 and P3 |
| P4 | Author, project | `python3 tools/verify_speech.py` | `0 with an unrecognized key term` | Unrecognized key term: correct `pronunciation.json`, repeat from P2 |
| P5 | Author, project | `node tools/stills.mjs stills`; look at every still; mark it inspected; `python3 tools/check_review.py` | `N of N stills inspected without finding` | Defect: correct the scene, `node tools/stills.mjs stills <scene>`, repeat P5 for it |
| P6 | Author | Decision: render machine named in the profile and reachable? | Yes: P6a. No: P6b | |
| P6a | Author, render machine | `tools/render-remote.sh` | `done in … s: out/<id>.mp4` | Interrupted or unreachable: go to R4 |
| P6b | Author, authoring machine | `tools/render.sh` | `rendered: out/<id>.mp4` | Interrupted: go to R4 |
| P7 | Author | Decision: opening sequence in the profile? Yes: `tools/prepend.sh out/<id>.mp4`, then `python3 tools/timeline.py --caption-offset <length>` | `joined without re-encoding` | `stream formats differ`: accepted once; it is encoded once |
| P8 | Author, file | `python3 tools/measure.py all <file> [--offset <length>]` | `PASSED` | Go to R5 |
| P9 | Reviewer | Gate 2 of `presentation-video-review` | `review.md`: gate 2 passed | Findings: return to the step that owns them |
| P10 | Author, <delivery location> | Copy the file; compare size and checksum at the destination | Sizes and checksums equal | Mismatch: copy again; do not delete the local file |
| P11 | Author, project | Update the project `README.md`; remove intermediate files if the profile says so | Record complete | |

## Interruption, recovery and rollback

Completed work is recognized by its files; every step may be run again.

| ID | Situation | Recognize | Action |
|---|---|---|---|
| R1 | Voicing stopped (rate limit, network, quota) | Message names the scene and line reached; finished files are in `public/audio/` | Wait for the limit to reset, run P2a again: finished lines are not requested again. On a quota or key error fix the access first (`--check`) |
| R2 | Connector generation failed or timed out | No file stored for the scene | Check the status of the existing generation and fetch its result. Start a new generation only after the author agrees: each one is charged |
| R3 | Take rejected | `match` below the profile's threshold, or `line N was not heard` | The scene's existing sound is untouched. Listen to the take; request one new take as `-take2`; the better one is chosen. Do not lower the threshold to pass |
| R4 | Render interrupted | No `out/<id>.mp4`, or `out/raw.mp4` left behind | Delete `out/raw.mp4`, run P6 again. No partial file is a result |
| R5 | Delivery measurement failed | Line marked `FAIL` in the output | Loudness or peak: render again (P6). Duration or pauses: `tools/timeline.py`, then P6. Resolution or frame rate: correct the profile or `src/theme.ts`, then P6 |

Rollback: nothing is overwritten before P10. A delivered file is replaced
only by a file that passed P8 and P9; keep the previous delivered file until
then.

## Escalation and preserved evidence

Escalate to <owner> when the provider rejects the key, when quota is
exhausted, or when a key term stays wrong after a phonetic entry, a language
mark and a second voice. Preserve: the command output of the failed step,
`out/measure.json`, the rejected take and its word file. Never include the
env file or a key.

## Completion

Success: the file at <delivery location> matches the local file, `review.md`
records gate 2 as passed, and the project record is updated. Stop state: any
failed step leaves the previous delivered file untouched.

## Maintenance and sources

Reassess when the provider, the voice, the render machine, the delivery
location or the tools change. Sources: this project's `README.md`, the
method's speech-synthesis guide and the three video skills.
