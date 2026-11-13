# Script: How a presentation video is built

Replace the sample content. Keep the headings: `tools/check_script.py` reads
them. The spoken text lives in `src/narration.json`, the scene list in
`src/scenes.json`; this file is what a person reviews. A story video leaves
out Tone, because the story's own voice governs the narration, and may leave
out Sources and Evidenced, approximated, invented unless interfaces are
recreated; it names the edition, the revisions and the paths of the texts
narrated instead.

## Audience

Authors who build their first video with this template. They know their
subject and have not produced a video before.

## Goal

After the video the viewer can name the four steps from script to finished
file. Estimated length: under one minute.

## Tone

Friendly and encouraging: direct address, a short confirmation where a step
succeeds, no hype.

## Chapters and scenes

| Chapter | Scene | Message | On screen |
|---|---|---|---|
| Start | intro | A video is built from a script, not recorded. | Title card |
| The four steps | steps | Script, voice, picture and render follow one another. | Four boxes that light up one by one |
| Next | close | Change one sentence and only that sentence is voiced again. | Closing card |

## Sources

Every factual claim in a scene cites one of these, or the scene is marked
`unverified` in `src/scenes.json`.

| ID | Source | Date read |
|---|---|---|
| S1 | README of this template | 2026-11-13 |

## Evidenced, approximated, invented

- Evidenced: the order of the four steps (S1).
- Approximated: nothing.
- Invented: nothing. No interface is recreated in this video.

## Key terms and pronunciation

Terms that carry the video and must be spoken correctly: timeline. Entries
live in `pronunciation.json`.
