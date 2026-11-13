# Presentation video project

This folder is one video. It was copied from the project template of Writing
Method and carries its own tools, so it can be rendered again long after the
plugin has changed.

Replace this page with the record of your video when it is delivered; the
section **Project record** at the end shows what belongs in it.

## Terms

| Term | Meaning |
|---|---|
| Line | One narration line: a sentence or two short ones, spoken and shown as a caption |
| Scene | One picture with one message and an ordered list of lines |
| Manifest | `src/audio-manifest.json`: length and edge silence of every sound file |
| Timeline | `src/timeline.json`: when every line starts and ends, derived from the manifest |
| Profile | `video-profile.json`: the house choices shared by all videos of a project |
| Check still | One rendered frame per line, used to inspect the picture |

## What you need

- Python 3.11 or newer, Node 20 or newer with npm, `ffmpeg` and `ffprobe`.
- A video profile. Copy `video-profile.example.json` to `video-profile.json`
  in this folder or, for several videos, in their common parent folder. Set
  language, provider, voice and the languages the voice speaks. The voice
  must speak the target language and English.
- Provider access: for Azure AI Speech an env file (see the method's
  `env/README.md`); for ElevenLabs the authorized connector in your assistant.

Install once:

```sh
npm install
python3 tools/profile.py        # prints the profile in effect, or names what is missing
```

## Files you write

| File | Content |
|---|---|
| `video.json` | Identifier, title, one audience, form of address, goal, `recreated`, `stale_when` |
| `script/script.md` | The script as a person reviews it: audience, goal, chapters, sources, what is invented |
| `src/scenes.json` | Scene order with key (lowercase letters, digits, `_`), chapter, message and sources |
| `src/narration.json` | Lines per scene |
| `pronunciation.json` | Fixed spoken forms; copy `pronunciation.example.json` |
| `src/scenes/*.tsx` | The picture of each scene, registered in `src/scenes/index.tsx` |

A narration line:

```json
{"text": "Open the `Settings` page.", "speak": "Open the settings page.", "min": 4, "show": true, "notice": false}
```

Only `text` is required. `speak` is the spoken form when it differs in
spelling. `min` is the least time in seconds the line stays on screen, for a
picture that needs longer than the sentence. `show: false` speaks the line
without a caption. `notice: true` marks the line that tells the viewer that
interfaces are recreated.

### Story videos

A video that narrates a story (an accepted chapter, range or short piece read
aloud over pictures) is marked in `video.json`:

```json
{"purpose": "story", "edition": "verbatim", "story_id": "<story id>",
 "based_on": [{"chapter_id": "<chapter id>", "revision": "<manuscript revision>"}]}
```

- `purpose` is `tutorial` when absent. With `story`, the narration is the
  author's accepted text and no tool or step may reword it.
- `edition` is `verbatim` (the accepted manuscript, only cut into scenes and
  lines at sentence boundaries) or `listening` (a derived text with changes for
  the ear that the author approved; the written manuscript stays unchanged).
- `based_on` names every chapter or piece narrated and the manuscript revision
  it was taken from. A changed manuscript makes the script stale.

The script check then requires `edition` and `based_on`, asks for no source
table and no `sources` per scene, and raises no sentence-length warning; every
other check stays. A scene's `message` is a working note of what happens in
the scene and is not spoken; the picture is a plain description in
`script/script.md`, where the section Tone is left out and the sections
Sources and Evidenced, approximated, invented may be left out unless
interfaces are recreated. `script/script.md` also names the paths of the
texts narrated and, for a listening edition, its `edition_revision`. `audience` and
`address` stay required (the listener; `address` may be `none`).

## From script to file

Run every command from this folder.

1. Check the script. Errors block voicing.

   ```sh
   python3 tools/check_script.py
   ```

2. Preview timing without sound and build the scenes.

   ```sh
   python3 tools/timeline.py --draft
   npm run studio
   ```

   Anchor animations to line starts: `const {T, line} = useLines('steps')`,
   then `T(2)` is the frame at which line 2 starts. Do not write seconds.

3. Verify the key terms before voicing everything.

   ```sh
   python3 tools/verify_speech.py --samples
   python3 tools/voice_azure.py --only <the list it printed>
   ```

   Listen to those lines. Correct a wrong term in `pronunciation.json`.

4. Voice the narration.

   ```sh
   python3 tools/voice_azure.py --check     # access, nothing is charged
   python3 tools/voice_azure.py             # only changed lines are requested
   ```

   For ElevenLabs, see **Per-scene voicing** below.

5. Derive the timeline and measure the pace.

   ```sh
   python3 tools/timeline.py
   python3 tools/measure.py pace
   ```

6. Render check stills and look at every one.

   ```sh
   node tools/stills.mjs stills
   ```

   Mark each entry in `stills/stills.json` as `"inspected": true` after
   looking at it, and write any defect into its `"finding"`. Then:

   ```sh
   python3 tools/check_review.py
   ```

   It exits with an error while a still of the current timeline is missing,
   not inspected or carries a finding.

7. Render and measure the file.

   ```sh
   tools/render.sh                          # or tools/render-remote.sh [host]
   python3 tools/measure.py all out/<video id>.mp4
   ```

   Expected last line: `PASSED`. The measurement covers resolution, frame
   rate, duration, loudness, peak and the audible pause between lines.

8. Optional opening sequence, named in the profile:

   ```sh
   tools/prepend.sh out/<video id>.mp4
   python3 tools/timeline.py --caption-offset <opening length>
   python3 tools/measure.py all out/<video id>-with-opening.mp4 --offset <opening length>
   ```

Captions are in `out/captions.vtt`, chapter marks in `out/chapters.txt`.

### Changing one sentence

Edit the line in `src/narration.json` and repeat steps 4 to 7. One request is
sent; every later line moves by itself.

### Per-scene voicing (ElevenLabs connector)

Set `"provider": "elevenlabs"` and `"mode": "scene"` in the profile.

1. `python3 tools/split_takes.py prompts` prints the passage for each scene.
2. Generate each passage once through the connector and store the result at
   once as `takes/<scene>-take1.mp3`. A generation costs credits: on an error
   or timeout check its status; do not start it again.
3. Transcribe each take to `takes/<scene>-take1.words.json`, a list of
   `{"word", "start", "end"}`.
4. `python3 tools/split_takes.py` cuts the takes into lines and writes the
   manifest. A take that skipped or changed a sentence is rejected.

## When something fails

| Message | Cause | What to do |
|---|---|---|
| `video-profile.json not found` | No profile here or in a parent folder | Copy `video-profile.example.json` |
| `speech.voice must be multilingual` | `voice_languages` lacks the target language or English | Choose a multilingual voice and list its languages |
| `no credential file` | No env file found | Follow `env/README.md` of the method |
| `still rate limited after N waits; stopped at <scene>:<line>` | Provider limit | Run the same command again later; finished lines are kept |
| `the text changed after voicing` | A line was edited after voicing | Voice again, then `tools/timeline.py` |
| `src/timeline.json is a draft` | Rendering without sound | Voice the script, then `tools/timeline.py` |
| `pace … OUT OF RANGE` | Scene too fast or slow for the profile | Shorten or loosen the wording, or adjust the pause; measure again |
| `pauses … outside` | Audible pause differs from the timeline | Run `tools/timeline.py` and render again |
| `key term not recognized` | The voice mispronounces a key term | Correct it in `pronunciation.json`, voice and verify again |
| `line N was not heard in the take` | The take dropped or changed a sentence | Request a new take; the scene's existing sound is untouched |
| `id may contain only lowercase letters, digits and hyphens` | `video.json` id is used in file names and commands | Rename the id |
| `a story video must name its edition` | `video.json` has `"purpose": "story"` without `edition` | Set `verbatim` or `listening` |
| `a story video must list the manuscript it narrates` | `based_on` is missing, empty or lacks `chapter_id` or `revision` | Name each narrated chapter with its manuscript revision |
| An empty box or missing symbol in a still | The fonts cover Latin and Latin Extended only | Draw the mark as a shape or add a font that has it |

## Fonts

The template loads Inter and JetBrains Mono with the Latin and Latin Extended
ranges. Arrows, check marks, emoji and other symbols are not included and
show as an empty box or not at all. Nothing reports this automatically: it is
found by looking at the check stills.

## Project record

When the video is delivered, this page records:

- title, audience, length and date;
- chapters with time marks (from `out/chapters.txt`);
- sources with the date read;
- what is evidenced, approximated and invented in the picture;
- voice, provider and mode;
- where the delivered file is stored;
- what change in the real world makes the video stale.
