# WM-001 Research: measured defaults and provider behaviour

Measured on 2026-11-13. Sources: eleven existing video projects (narration
data, sound files and length manifests) and nine short test syntheses with
Azure AI Speech. No rendered video was needed for these numbers.

## R-1 Speaking pace

Words of caption text divided by speech time (pauses between lines excluded).
German narration.

| Project (provider) | Lines | Speech | Pace | Line length median / max |
|---|---|---|---|---|
| AD basics (Azure) | 161 | 31.8 min | 116 wpm | 23 / 39 words |
| M365 basics (Azure) | 233 | 39.9 min | 119 wpm | 20 / 34 |
| Server landscape (Azure) | 45 | 7.8 min | 118 wpm | 21 / 33 |
| GitHub for IT (Azure) | 56 | 8.7 min | 123 wpm | 19 / 32 |
| Git explained (Azure) | 44 | 4.5 min | 125 wpm | 13 / 17 |
| PIM guide (Azure) | 58 | 8.3 min | 128 wpm | 18 / 29 |
| Password safe (Azure) | 117 | 15.5 min | 130 wpm | 17 / 29 |
| herdr explained (Azure) | 30 | 3.8 min | 132 wpm | 17 / 21 |
| Claude Desktop SSH (Azure) | 80 | 11.6 min | 133 wpm | 19 / 31 |
| Website guide (Azure) | 100 | 13.6 min | 138 wpm | 19 / 29 |
| Welcome to IT (ElevenLabs) | 263 | 30.6 min | 152 wpm | 18 / 32 |

- Decision: default pace range **120 to 155 words per minute** per scene,
  measured the same way. Published guidance for English gives 100 to 150 for
  presentations and about 155 for audiobooks; German words are longer, so the
  numeric range is taken from our own accepted videos, not from that guidance.
- Decision: default line limit **28 words**, sentence warning above
  **22 words**. The three slowest videos are also the ones with the longest
  lines.

## R-2 Pause between lines

All nine timeline implementations use the same constants: 0.7 s lead, 8 frames
(0.27 s) start delay, 0.6 s gap, 1.4 s tail. Silence inside the sound files
(threshold −40 dB):

| Provider path | Leading silence | Trailing silence | Audible pause between lines |
|---|---|---|---|
| Azure, per line | 0.02 s | 0.31 s | 0.31 + 0.60 + 0.27 + 0.02 ≈ **1.20 s** |
| ElevenLabs, split takes | 0.05 s | 0.09 s | 0.09 + 0.60 + 0.27 + 0.05 ≈ **1.01 s** |

- Finding: the audible pause was twice the configured gap, and differed by
  provider, because file silence and start delay were not accounted for.
- Decision: the manifest records leading and trailing silence per file. The
  timeline places the next line's first sound exactly `pause` after the
  previous line's last sound. Defaults: **0.65 s** between lines, **1.0 s**
  at a scene change, **0.5 s** before a scene's first line. The maintainer
  asked for roughly half a second less than before, never zero; a listening
  comparison (0.45 / 0.65 / 0.85 s) on the sample video confirms or adjusts
  the default during implementation.

## R-3 Azure voice behaviour (voice in current use, MAI family)

One two-sentence test text, synthesized nine times.

| Variant | Length | Finding |
|---|---|---|
| Plain, run 1 | 8.04 s | |
| Plain, run 2 | 7.13 s | Same input, 11 % shorter: output is not deterministic |
| `prosody rate="+7%"` | 7.54 s | Inside the run-to-run spread: no measurable effect |
| `prosody rate="+25%"` | 5.86 s | Effective |
| `break time="1500ms"` between sentences | 6.65 s | Ignored: pause 0.29 s instead of 1.5 s |
| `lang xml:lang` around one word | 7.80 s | Accepted |
| `phoneme alphabet="ipa"` | 7.94 s | Accepted; audible effect to be judged by ear |
| `mstts:express-as style="friendly"` | HTTP 400 | Rejected |
| Different HD family, plain | 7.22 s | Works with the same request |

- The rate setting used so far (+7 %) had no reliable effect. Small rate
  values must not be trusted; FR-035's "measure before relying" is necessary.
- Pauses cannot be set through markup with this voice. Pauses are therefore
  owned by the timeline (R-2), which is provider-independent.
- A style cannot be requested with this voice. Friendliness comes from the
  wording; the voice infers tone from the text.
- Because output varies between runs, an accepted sound file must be kept and
  never regenerated without a text change. The content-addressed cache
  already guarantees this.
- Provider documentation (read 2026-11-13) lists, for its HD voices:
  `prosody`, `emphasis`, `mstts:silence` unsupported; `phoneme`, `sub`,
  `lexicon` (alias only), `lang`, `break` supported; a `temperature` parameter
  for output variation. The test shows the documented table does not transfer
  to every voice family, which is why settings are probed per voice.

## R-4 ElevenLabs behaviour (provider documentation, read 2026-11-13)

- Current models take no SSML pauses. Pacing follows punctuation, line breaks
  and bracketed audio tags. Ellipses add hesitation and are unsuitable here.
- Tone can be directed with bracketed tags; results depend on the voice and
  must be tested. Decision: at most one mild tone tag at the start of a scene
  passage, recorded in the profile, never per sentence.
- Pronunciation: phonetic notation is supported by some models; a phonetic
  respelling is the general fallback. The provider states that words shared
  between related languages may be read with the wrong accent depending on the
  voice. This matches the recorded mispronunciation and supports sample
  sentences before full voicing (FR-034).
- Access is through the connector in the assistant session; a generation is
  started once and its status is polled, never repeated as a retry.

## R-5 Repository mechanics

- `scripts/package_plugin.py` and `scripts/validate_plugin.py` are
  Core-managed files and must not be edited here. Packaging reads files
  through Git, so an ignored `env/*.env` is not packaged. A writing-owned test
  asserts this.
- CI runs `validate-plugin` and the unit tests on a runner without media
  tools. Tests that need `ffmpeg` generate their own short sounds and are
  skipped when it is absent; all timeline, script-check and pronunciation
  logic is tested without media tools.
- The version string appears in `method.json`, `pyproject.toml`, both plugin
  manifests, `README.md` and `docs/usage.md`.
