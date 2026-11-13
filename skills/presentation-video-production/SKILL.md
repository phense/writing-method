---
name: presentation-video-production
description: "Use when an accepted video script must become a rendered presentation video: verifying key-term pronunciation, voicing the narration with Azure AI Speech or the ElevenLabs connector, deriving the timeline from the measured sound, building scenes, taking check stills and rendering, or when one sentence of an existing video changed. Not for writing or changing the script's content (use tutorial-video-scripting), the acceptance review (use presentation-video-review), filmed material, screen recordings or short-form social video."
---

# Presentation Video Production

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Turn an accepted script into a rendered video. Every step produces a file the
next step reads; nothing about timing is entered by hand. Commands run from
the video project, a copy of the
[project template](../../templates/presentation-video/README.md).

Read [speech synthesis](../../shared/media/speech-synthesis.md) before the
first request to a provider.

## Recovery preamble

Follow the recovery preamble and the operational state handoffs of
[documentation-authoring](../documentation-authoring/SKILL.md#recovery-preamble).
For an untracked single video, the files on disk are the state: completed
sound is reused, so every step can be run again after an interruption.

## Trigger

An accepted script (script check passed, author agreed), or a correction to a
video that already exists.

## Do not use for

- Deciding what the video says; use `tutorial-video-scripting`.
- The acceptance decision; use `presentation-video-review`.
- A script that has not passed the script check.

## Consumes

- The video project with `video.json`, `script/script.md`, `src/scenes.json`,
  `src/narration.json`, `pronunciation.json`.
- `video-profile.json` of the target project: provider, voice, pauses, pace
  range, loudness, opening sequence, render and delivery location.
- Provider access: an env file for Azure, or the authorized ElevenLabs
  connector. See [credential examples](../../env/README.md).
- External tools, checked and named when missing, never installed silently:
  Node with npm, `ffmpeg` and `ffprobe`, Python 3.11 or newer.

## Produces

| Step | Result |
|---|---|
| Voicing | `public/audio/<scene>-<nn>-<hash>.mp3`, `src/audio-manifest.json` |
| Timeline | `src/timeline.json`, `out/captions.vtt`, `out/chapters.txt` |
| Check stills | `stills/<scene>-<nn>.png`, `stills/stills.json` (inspection list) |
| Render | `out/<video id>.mp4`, with an opening sequence `…-with-opening.mp4` |
| Measurement | `out/measure.json` |

## Workflow

1. **Gate.** Run `python3 tools/check_script.py`. Stop on errors.
2. **Design the picture before paying.** `python3 tools/timeline.py --draft`
   estimates lengths without sound. Build the scenes under `src/scenes/`,
   register them in `src/scenes/index.tsx`, and anchor every animation to a
   line start with `useLines` (`T(i)`), never to a second. Size text with
   `MIN_FONT` or larger and place it with `MARGIN` (both come from the
   profile through the timeline), and never change a text while it is being
   read.
3. **Check the access.** Azure: `python3 tools/voice_azure.py --check`.
   ElevenLabs: confirm the connector answers by listing voices.
4. **Verify key terms first.** `python3 tools/verify_speech.py --samples`
   names one line per key term. Voice only those
   (`python3 tools/voice_azure.py --only <list>`), listen, and run the
   read-back on them. A wrong term is corrected in `pronunciation.json`
   (phonetic notation or respelling, then a language mark, then another
   voice) and sampled again. Only then voice the rest.
5. **Voice.**
   - Azure, per line: `python3 tools/voice_azure.py`. Only changed lines are
     requested. On a rate limit it waits; if it stops, run it again: completed
     files are reused.
   - ElevenLabs, per scene: `python3 tools/split_takes.py prompts` prints the
     passage per scene. Generate each passage **once** through the connector,
     poll its status until done, and store the file at once as
     `takes/<scene>-take1.mp3`. On a failure or timeout check the existing
     generation; do not start another without the author's decision.
     Transcribe the take to `takes/<scene>-take1.words.json`, then run
     `python3 tools/split_takes.py`. A rejected take skipped or changed a
     sentence: request a new one.
6. **Probe settings before relying on them.**
   `python3 tools/probe_settings.py rate=+10%` voices a sample twice with and
   twice without the setting. Keep a setting only if it reports EFFECTIVE.
7. **Timeline.** `python3 tools/timeline.py`. It refuses sound that no
   longer matches the text. Then `python3 tools/measure.py pace`: a scene
   outside the profile's range is adjusted through wording, an effective
   provider setting, or the pause value, and measured again.
8. **Read-back.** `python3 tools/verify_speech.py` over all lines. An
   unrecognized key term blocks delivery; lines below the similarity
   threshold are listened to.
9. **Check stills.** `node tools/stills.mjs stills` renders one still per
   line. Look at every one; see
   [presentation-video-review](../presentation-video-review/SKILL.md) for
   what to look for. Mark each inspected still in `stills/stills.json`;
   correct and re-render the affected scenes
   (`node tools/stills.mjs stills <scene>`) until
   `python3 tools/check_review.py` passes.
10. **Render.** `tools/render.sh` locally, or `tools/render-remote.sh` on the
    profile's render machine. Voicing is complete before the project is
    copied, so no credential leaves the authoring machine.
11. **Opening sequence.** If the profile names one:
    `tools/prepend.sh out/<id>.mp4`. Matching stream formats are joined
    without re-encoding. Pass the printed opening length as
    `--caption-offset` to `tools/timeline.py` and as `--offset` to the
    measurement.
12. **Measure the file.** `python3 tools/measure.py all out/<file>.mp4`
    checks resolution, frame rate, duration, loudness, peak and the audible
    pause between lines. A render that exited cleanly is not evidence; this
    measurement is.
13. **Record.** Update the project `README.md`: chapters with time marks from
    `out/chapters.txt`, sources, voice and provider, what makes the video
    stale.

### One sentence changed

Edit the line in `src/narration.json`, then repeat steps 5, 7, 8, the stills
of that scene, and steps 10 to 12. Per-line voicing sends one request; all
later lines move by themselves.

## Playbook

Producing and delivering a video crosses machines and paid services and must
be resumable. A target project that produces videos regularly keeps the
playbook `PB-WM-VIDEO-001`, instantiated from the
[template](../../templates/presentation-video/playbook.md) with
`playbook-authoring` and checked with `playbook-review`.

## Completion

The rendered file exists and `tools/measure.py all` passes for it. This is
not acceptance: the delivery gate belongs to the review.

## Next phase

`presentation-video-review`

## Supporting skills

- `verification-before-completion` before any "rendered" or "ready" claim.
- `playbook-authoring`, `playbook-review` for the production playbook.
- `project-backlog` when the video is tracked under a work ID.
