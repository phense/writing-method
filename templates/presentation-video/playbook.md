# PB-WM-VIDEO-001: Produce and deliver a presentation video

Template. Copy it to `docs/playbooks/system/PB-WM-VIDEO-001.md` in the target
project, fill the instantiation inputs listed under Inputs, leave the run-time
variables as written, and remove this paragraph. Review it with
`playbook-review` and rehearse it once on the sample video before relying on
it.

## Contents

- Identity and scope
- When to use / when not to use
- Inputs
- Before starting
- Decision paths and actions
- Interruption, recovery and rollback
- Escalation and preserved evidence
- Completion
- Maintenance and sources

## Identity and scope

- Class: system
- Origin: Writing Method, specification WM-001 (US-002, US-004)
- Audience and owner: an author or assistant with the video project and a
  configured speech provider, without knowledge of earlier videos; owner
  <owner role>
- Target: one video project, authoring machine <authoring machine>, render
  machine <render machine or "none">, speech provider <azure | elevenlabs>
- Readiness deadline: before the first video is delivered from this project
- Last edited: <last edited>
- Review and rehearsal evidence: <relative link>

## When to use / when not to use

Use when an accepted script is to become a delivered video, or when a
delivered video is corrected. Do not use to write the script or to decide
whether a video is acceptable: those belong to `tutorial-video-scripting`
(tutorial), to the story scripting skill and the author (story video:
`"purpose": "story"` in `video.json`) and to `presentation-video-review`.

Outcome: a file at <delivery location> whose measurement passed and whose
review gate 2 is recorded as passed.

## Inputs

Instantiation inputs, filled once when the playbook is copied into a project:

| Input | Source |
|---|---|
| <owner role>, <channel> | The project: who decides and how that person is reached |
| <authoring machine>, <render machine or "none">, <host> | The project; <host> is `render.host` in the profile |
| Speech provider and mode | `speech.provider` and `speech.mode` in the profile |
| <delivery location> | `delivery.location` in the profile |
| <file name> | The project's naming rule for a delivered file |
| <copy command>, <checksum command> | The commands that copy to <delivery location> and compute a checksum there |
| <transcription command> | `transcribe` in the profile |
| <connector status check> | ElevenLabs only: how the connector reports an existing generation and fetches its result |
| <last edited>, <relative link> | Date of the last edit, and the review and rehearsal record |

An input the project cannot name is a blocker for the step that uses it, not
a value to guess.

Run-time variables, left as written:

| Variable | Value |
|---|---|
| `<scene>`, `<line>` | As printed by the tools |
| `<id>` | `python3 tools/profile.py --get video.id` |
| `<file>` | `out/<id>.mp4`, or `out/<id>-with-opening.mp4` after P7a |
| `<length>` | The seconds printed by `tools/prepend.sh` as `opening length` |
| `<date>`, `<name>`, `<languages>`, `<take>`, `<code>`, `<N>`, lists | As printed by the tools or written in `review.md` |
| `<value>` | The rate to probe, for example `+10%` |
| `<render.remote_dir>` | `python3 tools/profile.py --get render.remote_dir` |

## Before starting

Run from the video project. Each check must succeed before step P1; of the
two provider rows, the one for the profile's `speech.provider`.

| Check | Command | Expected |
|---|---|---|
| Profile | `python3 tools/profile.py` | Prints the profile; no error |
| Python | `python3 --version` | 3.11 or newer |
| Script | `python3 tools/check_script.py` | `0 error(s)` |
| Review gate 1 | Open `review.md` | `Gate 1: passed on <date>`, and "Script revision reviewed" names the current script |
| Media tools | `ffmpeg -version && ffprobe -version && node --version` | Each command prints its version and exits without error |
| Node packages | `npm ls remotion` | A version, no `missing` |
| Scenes | `python3 tools/timeline.py --draft && node tools/stills.mjs out/draft-stills`, then look at one still per scene in `out/draft-stills/` | No still shows `PLACEHOLDER`. `stills/` and `stills/stills.json` are not touched. `src/timeline.json` is now a draft; it is replaced in P3 |
| Transcription | `python3 tools/profile.py --get transcribe` | Prints a command containing `{audio}`. Empty: stop; P4 and P2b cannot run |
| Delivery location | `python3 tools/profile.py --get delivery.location` | The path named in this playbook. Empty: stop |
| Provider (Azure) | `python3 tools/voice_azure.py --check` | `credentials accepted` and a line `voice <name>: <languages>`. A line starting `note:` is corrected in the profile first |
| Provider (ElevenLabs) | List voices through the connector | A voice list that contains the profile's voice |
| Render machine, if used | The command below | Five version lines. Fails: not a stop; P6 then takes P6b |

```sh
ssh <host> 'export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH; node --version && npm --version && python3 --version && rsync --version | head -1 && ffmpeg -version | head -1'
```

Story video: the narration is voiced as it is. No step of this playbook
changes wording, tone or order; a wrong name or term is corrected only in
`pronunciation.json` or in the line's `speak`.

Authority and impact: voicing spends provider quota or credits; rendering
uses the render machine's processor for minutes. P6a creates and synchronizes
the folder `<render.remote_dir>/<id>` on the render machine (files there that
are not in the project are deleted) and installs the Node packages there.
Delivery replaces `<delivery location>/<file name>` in P10b; that is the only
step that changes a delivered file.

## Decision paths and actions

| Step | Actor and target | Condition / action | Expected evidence | Failure / next step |
|---|---|---|---|---|
| P1 | Author, project | `python3 tools/verify_speech.py --samples`. No line `voice them first:` printed: go to P2. Azure: `python3 tools/voice_azure.py --only <list it printed>`; a person listens to each of these lines (an assistant hands the file names under `public/audio/` to the author and waits); then `python3 tools/verify_speech.py --only <same list>`. ElevenLabs: no sample voicing exists; go to P2; P4 is the first key-term check | Each key term heard correctly; `0 with an unrecognized key term` | Wrong term: correct `pronunciation.json`, repeat P1. Lines `below similarity`: a person listens to each; wrong: correct `pronunciation.json`, repeat P1; right: note the line in `review.md` |
| P2 | Author, project | Decision: `python3 tools/profile.py --get speech.provider` and `python3 tools/profile.py --get speech.mode` | `azure` and `line`: P2a. `elevenlabs` and `scene`: P2b | Any other pair: stop; correct the profile; repeat Before starting |
| P2a | Author, Azure | `python3 tools/voice_azure.py` | `N lines, … new` | Stops with `stopped at <scene>:<line>`: go to R1 |
| P2b | Author, connector | `python3 tools/split_takes.py prompts`; for each scene without a stored take, generate the printed passage once through the connector with the profile's voice, wait until it is done, and store it at once as `takes/<scene>-take1.mp3`; transcribe each take to `takes/<scene>-take1.words.json` (a list of `{"word", "start", "end"}`) with <transcription command>; `python3 tools/split_takes.py` | `<scene>: <take> (match 0.90 or higher), N lines` per scene | Generation error or timeout: go to R2. Take rejected: go to R3 |
| P3 | Author, project | `python3 tools/timeline.py && python3 tools/measure.py pace` | `PASSED` | `text changed after voicing` or missing sound: repeat P2. `OUT OF RANGE`: go to R6 |
| P4 | Author, project | `python3 tools/verify_speech.py` | `0 with an unrecognized key term` | Unrecognized key term: correct `pronunciation.json`, repeat from P2. Lines `below similarity`: a person listens to each; wrong: correct `pronunciation.json`, repeat from P2; right: note the line in `review.md`. ElevenLabs (P2b), instead of repeating from P2: the stored take keeps the wrong sound, and only a respelling (`speak` in `pronunciation.json` or in the line) changes the passage. After the correction and after the author agrees (it is charged), generate one new take of the affected scene from `python3 tools/split_takes.py prompts <scene>`, store it as `takes/<scene>-take<N+1>.mp3`, transcribe it to `takes/<scene>-take<N+1>.words.json`, run `python3 tools/split_takes.py <scene>` (see the take rule under Correction of a delivered video), delete that scene's read-back word files `public/audio/<scene>-*.words.json`, then P3 and P4. Still wrong after that: stop and escalate |
| P5 | Author, project | `node tools/stills.mjs stills`; look at every still; set `"inspected": true` for it in `stills/stills.json`, or write the defect into its `"finding"`; `python3 tools/check_review.py` | `N of N stills inspected without finding` | Defect: correct the scene, `node tools/stills.mjs stills <scene>`, repeat P5 for it |
| P6 | Author | Decision: `python3 tools/profile.py --get render.host` | Prints a host and the render-machine check of Before starting succeeded: P6a. Empty, or the check fails: P6b | |
| P6a | Author, render machine | `tools/render-remote.sh` | `done in … s: out/<id>.mp4` | Interrupted or unreachable: go to R4 |
| P6b | Author, authoring machine | `tools/render.sh` | `rendered: out/<id>.mp4` | Interrupted: go to R4 |
| P7 | Author | Decision: `python3 tools/profile.py --get opening` | Prints a path: P7a. Empty: P8 | |
| P7a | Author, authoring machine | `tools/prepend.sh out/<id>.mp4`, then `python3 tools/timeline.py --caption-offset <length>` | `joined without re-encoding: out/<id>-with-opening.mp4` and `opening length: <length> s` | `stream formats differ` followed by `joined with one encode`: not a failure, continue. `opening sequence not found`: correct `opening` in the profile, repeat P7 |
| P8 | Author, file | `python3 tools/measure.py all <file> [--offset <length>]` | `PASSED` | Go to R5 |
| P8b | Author, project | Update the project `README.md`: title, audience, length and date; chapters with time marks from `out/chapters.txt`; sources with the date read (story video: the edition and the manuscript revisions instead); what is evidenced, approximated and invented; voice, provider and mode; <delivery location>; what makes the video stale | All seven items present | Item missing: complete it before P9 |
| P9 | Reviewer | Gate 2 of `presentation-video-review` | `review.md`: `Gate 2: passed on <date>` | Picture, sound or file finding: return to the step P1 to P8 that owns it. Wording finding, tutorial: stop; `tutorial-video-scripting`; start again at Before starting. Wording finding, story: stop; the story scripting skill and the author, never `tutorial-video-scripting`; the changed line arrives from there; start again at Before starting |
| P10 | Author, <delivery location> | Copy the file measured in P8 to `<delivery location>/<file name>.new` with <copy command>; compute <checksum command> on the local file and on the copy | Both checksums equal | Not equal: delete the `.new` copy and copy once more. Not equal again: stop and escalate; the delivered file is untouched |
| P10b | Author, <delivery location> | Rename an existing `<file name>` to `<file name>.previous`, then `<file name>.new` to `<file name>` | `<file name>` has the checksum from P10 | Rename fails: rename `.previous` back; stop |
| P11 | Author, <delivery location> | Compute <checksum command> on `<delivery location>/<file name>` | Equals the local checksum | Not equal: restore `.previous` (first delivery, none exists: rename `<file name>` to `<file name>.failed`); stop and escalate |

No step deletes working files other than the read-back word files named in
the take rule. `public/audio/`, `src/audio-manifest.json`,
`src/timeline.json`, `takes/`, `out/captions.vtt`, `out/chapters.txt` and
`review.md` are kept: a later correction reuses them.

### Correction of a delivered video

The changed line arrives accepted (tutorial: `tutorial-video-scripting`;
story: the story scripting skill and the author), and `review.md` records gate 1
for it. Run Before starting, then P2 to P11.

- P2a requests only the changed line.
- P2b: after the author agrees, one new take of that scene, stored under the
  next free number `takes/<scene>-take<N+1>.mp3` with its own word file. Never
  overwrite an existing take: its word file would no longer match the sound.
  The line `split_takes.py` prints for the scene must name the new take. If
  it names an older take, move that scene's older takes with their word files
  to `takes/superseded/` (the tool reads only `takes/<scene>-take*.mp3`) and
  run `python3 tools/split_takes.py <scene>` again. Before P4, delete that
  scene's read-back word files `public/audio/<scene>-*.words.json`: an
  unchanged line keeps its file name, and `verify_speech.py` does not
  transcribe a sound file again while a word file with its name exists.
- P5: `node tools/stills.mjs stills <scene>` and inspect that scene's stills.
  A run without a scene resets every inspection mark.

## Interruption, recovery and rollback

Completed work is recognized by its files. P2a and P3 to P8 may be run again;
P2a requests only lines without a file. P2b is charged per generation: a
scene with a file `takes/<scene>-take<N>.mp3` is never generated again in a
rerun; repeat only the transcription and `python3 tools/split_takes.py`.

| ID | Situation | Recognize | Action |
|---|---|---|---|
| R1 | Voicing stopped | Message names the scene and line reached; finished files are in `public/audio/` | `still rate limited`: wait, run P2a again; finished lines are not requested again. `provider not reachable`: check the network, run P2a again. `the provider rejected the key` or `provider answered HTTP <code>`: run `python3 tools/voice_azure.py --check`; still rejected: escalate. `credentials accepted`: run P2a once more; it stops again at the same line with the same message: stop and escalate with the output |
| R2 | Connector generation failed or timed out | No file stored for the scene | Use <connector status check> to find the existing generation and fetch its result. Start a new generation only after the author agrees: each one is charged |
| R3 | Take rejected | `match` below the profile's threshold, or `line N was not heard` | The scene's existing sound is untouched. Listen to the take. After the author agrees (it is charged), request one new take, store it under the next free number as `takes/<scene>-take<N+1>.mp3` (never overwrite a take) and transcribe it to `takes/<scene>-take<N+1>.words.json` with <transcription command>; `python3 tools/split_takes.py <scene>` chooses the better one. Second take rejected too: stop and escalate. Do not lower the threshold to pass |
| R4 | Render interrupted | The command ended without its last line (`rendered: …` or `done in …`). An `out/<id>.mp4` from an earlier render is not the result | Delete `out/raw.mp4` and any earlier `out/<id>.mp4` and `out/<id>-with-opening.mp4`, then run P6 again; after P6a, first repeat the render-machine check of Before starting (it fails: P6b). No partial file is a result |
| R5 | Delivery measurement failed | Last line `FAILED`; the failing row shows `FAIL` (file), `OUT OF RANGE` (pace) or `N outside ±` (pauses) | Pace: R6. Resolution or frame rate: correct `picture` in the profile, `python3 tools/timeline.py`, then P5 and P6. Duration or pauses: `python3 tools/timeline.py`, then P6 and P7. Loudness or peak: P6 once. Sound track: R4. With an opening: `python3 tools/measure.py all out/<id>.mp4`. If `out/<id>.mp4` passes and only the file with the opening fails, the opening sequence is the cause: correct that file, then P7. The same row fails a second time: stop and escalate; do not change a profile limit to pass |
| R6 | Pace out of range | `pace <scene> … OUT OF RANGE [low, high]` in the output of `tools/measure.py` | Story video: never change wording, tone or order of a line. Azure: `python3 tools/probe_settings.py rate=<value>` (short paid requests); keep the setting under `speech.settings` in the profile only if its last line is exactly `EFFECTIVE` (a line starting `NOT EFFECTIVE` means: do not keep it); then repeat P2 and P3 (a changed setting voices every line again). ElevenLabs: no pace setting is defined; stop and escalate. Tutorial only: a changed wording is produced by `tutorial-video-scripting`, then start again at Before starting (script check and gate 1 for the changed script). Story line that needs other words, or no effective setting: stop and return to the story scripting skill and the author. The pause value does not change the pace measurement. Changing `pace_wpm` in the profile or under `overrides` in `video.json` is an owner decision recorded in the project `README.md`, not a fix the operator chooses |

Rollback: no delivered file at <delivery location> is changed before P10b
(P10 only adds `<file name>.new`). Locally P2
replaces the sound of changed lines, the Scenes check, P3 and P7a rewrite `src/timeline.json`,
`out/captions.vtt` and `out/chapters.txt`, and P6 and P7a overwrite
`out/<id>.mp4` and `out/<id>-with-opening.mp4`. After P10b the previous
delivered file is `<file name>.previous`; keep it until P11 has passed. After P11 it stays until the next delivery
replaces it; removing it earlier is the owner's decision.

## Escalation and preserved evidence

Escalate to <owner role> through <channel> when `--check` still reports a
rejected key, when P2a stops twice at the same line although `--check`
accepts the credentials, when P2a stops with `still rate limited` on three separate
runs, when a second take is rejected, when a copy mismatches twice, when the delivered file mismatches in P11,
when a pace range cannot be met in R6 without an owner decision, when the
same measurement row fails twice, when a line is still wrong in P4 after one
new take (ElevenLabs), or when a key term stays wrong after a
phonetic entry, a language mark and a second voice. Preserve: the command
output of the failed step, `out/measure.json`, the rejected take and its word
file. Never include the env file or a key.

## Completion

Success: the file at <delivery location> has the checksum of the local file,
`review.md` records gate 2 as passed, and the project record is complete.
Stop state: a step that fails before P10b leaves the delivered file
untouched; a failure in P10b or P11 is undone by restoring `.previous`.

## Maintenance and sources

Reassess when the provider, the voice, the render machine, the delivery
location or the tools change. Sources: this project's `README.md`, the
method's speech-synthesis guide and the skills `presentation-video-production`,
`presentation-video-review` and `tutorial-video-scripting`, and the story
scripting skill for a story video.
