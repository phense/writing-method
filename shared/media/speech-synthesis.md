# Speech synthesis

Provider-neutral rules for turning narration into sound. They hold for every
video form; the commands live in the project template.

## Terms

| Term | Meaning |
|---|---|
| Line | One narration line: the unit of voicing, timing and checking |
| Manifest | The record of every sound file: length and the silence at its start and end |
| Timeline | Start and end of every line, derived from the manifest |
| Take | One generation of a whole scene by a provider that is voiced per scene |
| Read-back | Transcribing the voiced sound with speech recognition and comparing it with the text |
| Key term | A term that carries the video and must be pronounced correctly |

## Rules that do not depend on the provider

1. **Check the script before paying.** No request is sent before the script
   check passes.
2. **The voice is multilingual.** It speaks the target language and English,
   because narration contains English product names and technical terms. The
   profile lists the voice's languages; a voice without both is rejected.
3. **A multilingual voice still mispronounces.** It can read a plain word of
   the target language as foreign. Verify key terms before voicing the whole
   video (sample lines) and after it (read-back).
4. **Fix pronunciation once.** A correction goes into the pronunciation list,
   never into a single line. Try in this order: phonetic notation or a
   respelling, an explicit language mark, a different voice.
5. **Timing comes from measured sound.** The pause between lines is a
   timeline value. It already accounts for silence inside the sound files, so
   the audible pause equals the profile value. Do not try to set pauses
   through provider markup.
6. **Measure, do not trust.** A provider setting (rate, style, pause) counts
   only after its effect was measured for this voice. Pace is measured on the
   result in words per minute per scene.
7. **Keep accepted sound.** Providers are not deterministic: the same text
   can come back several percent longer or shorter. A sound file that was
   accepted is kept and reused; only a changed line is voiced again.
8. **Credentials stay on the authoring machine.** Voice first, then copy the
   project to a render machine. No key in the repository, in logs or in a
   command line.

## Measured behaviour

Measured on 2026-11-13; repeat the probe for your voice, do not copy these.

| Observation | Consequence |
|---|---|
| Sound files carried 0.3 s of trailing silence with one provider and 0.1 s with another; with a fixed gap the audible pause was 1.2 s and 1.0 s against a configured 0.6 s | The timeline subtracts file silence |
| One high-definition voice ignored a pause instruction of 1.5 s, rejected a style request and showed no measurable effect for a rate change of 7 %; a rate change of 25 % worked | Probe every setting; own pauses in the timeline |
| The same text varied by 11 % in length between two identical requests | A setting is effective only beyond that spread |
| A multilingual voice mispronounced a central word of the target language throughout a video | Sample lines before voicing, read-back after |

## Azure AI Speech (per line, unattended)

- Access: key and region in an env file (`env/azure-speech.env.example` shows
  the variables). The credential check lists the voices and proves key and
  region without synthesizing.
- One request per line. Files are named by content, voice and settings; a
  rerun requests only what changed. Rate-limit answers are waited out within
  the profile's retry budget; other errors stop the run, and completed files
  are kept.
- Pronunciation list entries become phonetic markup, a respelling or a
  language mark. Which markup a voice honours differs by voice family; verify
  by ear and by read-back.

## ElevenLabs (per scene, through the connector)

- Access: the ElevenLabs connector in the assistant session. This method
  stores no ElevenLabs key. `env/elevenlabs.env.example` holds only non-secret
  settings. The path needs an interactive session with the connector
  authorized.
- **A generation costs credits. Start it once.** If a call fails or times
  out, check the status of the existing generation; never repeat the call as
  a retry. A second generation needs the author's decision.
- Voice a whole scene in one generation: the delivery is more natural than
  line by line. Choose the voice from the profile; if none is named, pick one
  from the connector's voice list and record it in the profile. Never invent a
  voice identifier.
- Store every take in the project at once; provider links expire.
- Split the take into lines at measured word boundaries. A take whose
  recognized words match the script below the profile's threshold skipped,
  repeated or changed a sentence: reject it.
- Current models take no pause markup. Pace follows punctuation and line
  breaks. Avoid ellipses: they add hesitation.
- Tone: at most one mild tag at the start of a scene passage, named in the
  profile and tested on a sample first. No tags per sentence.
- Changing one sentence means a new take of that scene.

## Choosing the mode

| Situation | Mode |
|---|---|
| Frequent corrections, unattended runs, long videos | Per line |
| Delivery matters most, text is final, an interactive session is available | Per scene |

The profile decides and the choice is recorded per video.
