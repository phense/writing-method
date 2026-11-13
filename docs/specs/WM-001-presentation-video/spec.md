# Feature Specification: Narrated presentation videos

## Stable work ID

- Feature ID: `WM-001`
- Artifact path: `docs/specs/WM-001-presentation-video/spec.md`
- Status: Draft
- Source request: Formalize in Writing Method how narrated tutorial videos are
  scripted, voiced, produced and reviewed, so that future videos reach a
  higher and repeatable quality. Ship credential examples without real keys.
  Name the parts so that other video forms can be added later without
  renaming.

## Terms

| Term | Meaning |
|---|---|
| Presentation video | A video composed programmatically from designed scenes and synthesized narration. It contains no camera footage and no screen recording. |
| Tutorial video | A presentation video whose purpose is to teach: it explains a concept or walks through a procedure. |
| Script | The reviewed text of a video: chapters, scenes and narration lines. |
| Narration line | One spoken sentence or short sentence group, with the on-screen caption it belongs to. The smallest unit of voicing, timing and checking. |
| Scene | A visual unit that carries one message and owns an ordered list of narration lines. |
| Check still | A single rendered frame, taken while a given narration line is spoken, used to inspect the picture without rendering the video. |
| Video profile | A file in the target project that records its house choices: voice, speech provider, branding, opening sequence, render location and delivery location. |
| Speech provider | A text-to-speech service. Azure AI Speech and ElevenLabs are the two supported ones. |
| Recreated interface | A drawn imitation of a real application window, used in place of a screenshot. |

**Purpose** and **form** are separate axes. `tutorial` names a purpose and stays
a writing concern. `presentation-video` names a form and owns production. A
later form (for example short vertical marketing clips) adds its own
form-bound skills and reuses the provider-neutral speech guidance.

## Evidence base

Eleven existing projects (October to November 2026) were inspected: nine
tutorial videos between 4 and 36 minutes, one opening sequence and one
template. Practices that held up, and failures that occurred, are the source of
the requirements below.

| Observation | Source | Effect on this specification |
|---|---|---|
| Hand-written start times drifted whenever a sentence changed. Deriving the timeline from the measured audio lengths removed the problem. | Earliest project versus all later ones | FR-010 |
| Marker frames and special characters were missing in the picture and were only noticed after a full render. | Several projects | FR-014, FR-021 |
| Voicing per line with a content-addressed cache made a one-sentence change cost one request. | Azure path, nine projects | FR-007 |
| Voicing a whole scene in one request gave a more natural delivery, but a one-sentence change forced the whole scene to be re-voiced and re-split, and the download links expired. | ElevenLabs path, one project | FR-008, edge cases |
| Pronunciation overrides were kept per line and repeated inconsistently across scenes. | Largest project | FR-005 |
| The free speech tier answered with rate-limit errors during long runs. | Azure path | FR-009 |
| Rendered sound was quiet and uneven between videos until loudness was normalized. | Render scripts | FR-016 |
| Viewers could mistake recreated interfaces and invented people for real ones. | Project notes | FR-004, FR-019 |
| One project needed two audiences and was split into two videos late. | Password-safe project | FR-001 |
| Joining an opening sequence re-encoded the video until stream formats were matched. | Opening-sequence project | FR-017 |
| The pause between sentences (a fixed 0.6 s plus a start delay and the silence inside each sound file) felt slightly long; the maintainer wants it shorter, not removed, for a crisper rhythm. | Maintainer feedback, 2026-11-13 | FR-030 |
| A multilingual voice repeatedly mispronounced a plain target-language word that is central to the video ("Tresor" in a German video). A multilingual model alone does not guarantee correct pronunciation; it can read a native word as foreign. | Password-safe project; maintainer feedback, 2026-11-13 | FR-033, FR-034 |
| The speaking-rate setting used so far relies on markup that the provider documents as unsupported for its high-definition voices; whether it had any effect was never measured. | Provider documentation, read 2026-11-13 | FR-035 |
| Research recommends learning videos of six to nine minutes. The maintainer decided that this does not apply to tutorial videos here: length follows the content, with one upper limit. | Brame 2016; maintainer decision, 2026-11-13 | FR-036 |
| The narration sounded neutral. The maintainer wants somewhat more friendliness and positive energy, without overdoing it. | Maintainer feedback, 2026-11-13 | FR-031 |

## User scenarios

### US-001: Script a tutorial video from source material (Priority: P1)

An author states the topic, audience and source material. The assistant
produces a reviewed script: chapters, scenes with one message each, narration
lines written for listening, and a list of every claim with its source.

- Why this priority: every later step consumes the script, and most quality
  defects found so far were script defects (wrong audience, unsupported claim,
  sentence too long to follow by ear).
- Independent test: given a short source document and a named audience, the
  assistant delivers a script that passes the script checks in FR-006 without
  any production tooling installed.

### US-002: Produce a video from an accepted script (Priority: P1)

The assistant turns an accepted script into a rendered video: it voices the
narration, derives the timeline from the audio, builds the scenes, inspects
check stills and renders.

- Why this priority: this is the deliverable the user asked for.
- Independent test: starting from the bundled sample script and the project
  template, with one configured speech provider, a short video is rendered
  and its measured properties satisfy FR-016.

### US-003: Review a video before delivery (Priority: P1)

A reviewer, human or assistant, checks the script, the check stills, the sound
and the rendered file against a fixed checklist and records findings.

- Why this priority: the requested gain in quality comes from gates that are
  applied every time, not from better tooling.
- Independent test: a prepared project containing five seeded defects (missing
  character, caption differs from speech, unsupported claim, unmarked recreated
  interface, loudness out of range) yields five findings.

### US-004: Change one sentence without redoing the video (Priority: P2)

The author corrects a single narration line. Only that line is voiced again,
all later timings follow by themselves, and only the affected check stills are
inspected again.

- Why this priority: videos are maintained for months; a costly correction
  path means errors stay in.
- Independent test: after editing one line, the number of provider requests is
  one, and no hand-written time value was edited.

### US-005: Set up credentials safely (Priority: P2)

A new user copies an example file, enters a key and runs a check that reports
whether the provider answers, without the key appearing in output, logs or the
repository.

- Why this priority: the method is published; a leaked key or an unusable
  first run both harm trust.
- Independent test: from a fresh clone, following only the written steps, the
  credential check passes, and a repository-wide search finds no key value.

### US-006: Apply house choices without changing the method (Priority: P2)

A project records its voice, branding, opening sequence, render location and
delivery location once in its video profile. Every later video follows it
without being told again.

- Why this priority: keeps organization-specific facts out of the public
  method while preserving consistency between videos.
- Independent test: two projects with different profiles produce videos that
  differ in voice and opening sequence, using an unchanged plugin.

## Acceptance criteria

- AC-001 — Given a topic, an audience and source material, when the author asks
  for a tutorial video script, then the script names exactly one audience,
  gives each scene one stated message, and lists a source for every factual
  claim or marks it as unverified.
- AC-002 — Given a script with a narration line longer than the configured
  limit, a term used in two spellings, or a caption that differs in meaning
  from its spoken form, when the script check runs, then each is reported with
  scene and line.
- AC-003 — Given an accepted script and a configured provider, when production
  runs, then one sound file exists per narration line, the timeline is derived
  from the measured lengths, and no start time was entered by hand.
- AC-004 — Given a voiced project, when one line changes and production runs
  again, then only that line is requested from the provider (per-line mode) or
  only its scene (per-scene mode), and unused sound files are removed.
- AC-005 — Given a provider that answers with a rate-limit error, when
  production runs, then it waits as instructed and continues; after the retry
  budget is spent it stops, keeps completed files and reports the line reached.
- AC-006 — Given a voiced project, when check stills are requested, then one
  still per narration line is produced, and the review cannot be recorded as
  passed until each still is marked inspected.
- AC-007 — Given a rendered video, when delivery checks run, then resolution,
  frame rate, loudness, peak level and duration are measured from the file and
  compared with the profile; any deviation blocks the "ready" claim.
- AC-008 — Given a script that uses recreated interfaces or invented persons
  and data, when the script check runs, then it requires one spoken or visible
  notice near the start and a written list of what is evidenced, approximated
  and invented.
- AC-009 — Given a fresh clone, when the repository is searched, then it
  contains example credential files with variable names and comments only.
  Real credential files are ignored by version control; packaging ships
  tracked files only, and a test fails if any credential file is tracked.
- AC-010 — Given no credential file, an empty key or a rejected key, when the
  credential check runs, then it names the missing file or variable, never
  prints a key, and exits with failure before any paid request.
- AC-011 — Given a project without a video profile, when a video is requested,
  then the assistant creates the profile from the template, asks only for
  values it cannot infer, and uses it from then on.
- AC-013 — Given two consecutive narration lines in a rendered video, when the
  silence between them is measured, then it equals the profile's pause within
  a stated tolerance and is greater than zero.
- AC-014 — Given the ElevenLabs path, when a generation fails or times out,
  then the procedure checks the existing generation's status and does not
  start a second paid generation without the author's decision.
- AC-015 — Given a script whose key term the voice mispronounces, when the
  pronunciation check runs before full voicing, then the term is reported,
  and after a correction is entered in the pronunciation list every
  occurrence in the voiced result is recognized correctly.
- AC-016 — Given a profile naming a voice that does not cover both the target
  language and English, when the profile is checked, then it is rejected with
  the reason.
- AC-017 — Given a script whose estimated length exceeds the profile's
  maximum, when the script check runs, then it blocks voicing and proposes a
  split at a chapter boundary; a script below the maximum is never reported
  for its length.
- AC-018 — Given a profile with a rate setting that the voice ignores, when
  the setting is checked, then the measured pace with and without it is
  shown and the setting is reported as ineffective.
- AC-012 — Given a request for a marketing clip, a screen recording or a
  filmed video, when routing happens, then none of the three new skills
  claims it.

## Functional requirements

Scripting (`tutorial-video-scripting`):

- FR-001: A script must record one audience, one form of address, the learning
  goal and the estimated length. A second audience requires a second script.
- FR-002: A script must be organized as chapters containing scenes; each scene
  must state its single message and what the viewer sees while it is spoken.
- FR-003: Narration must be written for listening and must apply the existing
  prose, explanation, procedure and terminology skills from the first draft.
  Spoken limits must be stated. Sentence and line length, abbreviations and
  numbers without a spoken form are checked automatically; "one new term per
  line" is checked by the reviewer at the first gate.
- FR-004: Every factual claim must be traceable to a recorded source with its
  date, or be marked unverified. The script must list what in the picture is
  evidenced, approximated and invented, and must carry a notice to the viewer
  when interfaces are recreated.
- FR-005: Pronunciation overrides must be kept once per project in a
  pronunciation list and applied to every occurrence. A caption and its spoken
  form may differ in spelling, never in meaning.
- FR-006: A script check must run before any paid voicing and report
  violations of FR-001 to FR-005 with scene and line. Secrets, personal data of
  real people and live credentials must not appear in narration or picture.

Voicing (`shared/media/speech-synthesis.md`, used by production):

- FR-007: Per-line voicing must store each line under a name derived from its
  exact spoken content and voice settings, reuse existing files, and remove
  files no longer referenced.
- FR-008: Per-scene voicing must be supported for providers that deliver more
  natural speech from longer passages. It must split the result into lines at
  measured word boundaries, verify that the recognized words match the script
  above a stated threshold, and reject a take that does not.
- FR-009: Provider errors must be handled explicitly: wait and retry on rate
  limits within a budget, stop on authentication or quota errors, keep
  completed work, and report characters voiced so cost is visible.
- FR-030: The pause between narration lines must be a single profile value
  that already accounts for silence contained in the sound files, so the
  audible pause equals the stated one. It must be shorter than in the existing
  videos and must never be zero. A longer pause may be set at chapter and
  scene changes.
- FR-031: The narration must sound friendly and moderately positive. The
  script contributes wording (direct address, encouragement where a step
  succeeds, no hype and no exclamation chains); the profile contributes the
  provider's voice-style settings. The tone must stay the same across scenes
  and across videos of one profile.
- FR-032: ElevenLabs must be used through its connector in the assistant
  session, not through a stored API key. The procedure must cover choosing the
  voice from the connector's list or the profile, starting a generation once,
  waiting for completion, storing the result immediately and never repeating
  a generation call as a retry.
- FR-033: The voice named in a profile must be multilingual: it must speak
  the target language and English, because narration regularly contains
  English product names and technical terms. A voice that covers only one
  language must be rejected when the profile is checked.
- FR-034: Pronunciation must be verified before full voicing and after it.
  Before: the recurring key terms of the script (title term, product names,
  abbreviations, foreign words) are voiced in short sample sentences with the
  profile's voice and checked. After: every voiced line is transcribed by
  speech recognition and compared with its spoken form; a key term that is
  not recognized is reported with scene and line. A failing term is corrected
  in this order: pronunciation list entry (phonetic spelling or the
  provider's pronunciation markup), explicit language marking, a different
  voice. The working correction is recorded in the pronunciation list so it
  holds for every later occurrence and video.
- FR-035: Speaking pace must be measured on the voiced result as words per
  minute per scene and compared with the profile's range. A provider setting
  for rate, pause or style counts as effective only after its effect was
  measured once for the profile's voice; a setting the voice ignores must be
  reported, not silently kept. Where the voice offers no pace control, pace
  is adjusted through wording and the pause between lines.
- FR-036: A tutorial video has no recommended length; brevity targets from
  learning research are not applied. The profile sets one maximum length
  (default 45 minutes). The script check estimates the length from the word
  count and the profile's pace; a script above the maximum must be split into
  two or more videos at a chapter boundary, each complete on its own, before
  voicing. Every video must carry chapter marks.
- FR-010: The measured length of every sound file must be recorded in a
  manifest. All timing must derive from this manifest. A line may declare a
  minimum display time; no other time value is authored.

Production (`presentation-video-production`):

- FR-011: A project template must provide a working minimal video: narration
  data, timeline derivation, a scene frame with chapter display, a caption
  component, check-still tooling and a render command.
- FR-012: Scenes must synchronize their animations to line starts, not to
  absolute times.
- FR-013: The picture must meet stated legibility rules: minimum text size at
  the delivery resolution, minimum contrast, a safe margin, and no line of
  on-screen text that changes while it is being read. Resolution, minimum
  size and margin are profile values that the composition reads; the
  template's own frame and caption obey them. Whether a scene obeys them, and
  contrast, is checked by eye on the check stills, not by a tool.
- FR-014: Check stills must be produced per narration line, late in the line's
  display time, at reduced size, for all scenes or a named subset. A single
  frame at a named second must also be obtainable.
- FR-015: Rendering must be possible locally and on a separate render machine.
  Voicing must complete before transfer so that credentials never leave the
  authoring machine.
- FR-016: The delivered file must meet the profile's resolution, frame rate,
  integrated loudness and peak level. These must be measured after rendering.
- FR-017: An opening sequence named in the profile must be placed in front
  without re-encoding when stream formats match, and the video must never be
  encoded twice on the standard path.
- FR-018: A caption file with line timings must be produced from the same
  timeline, so that subtitles never drift from speech.
- FR-019: Each project must keep a short record beside the video: chapters
  with time marks, sources, the evidenced/approximated/invented list, voice
  and provider used, and what change in the real world makes the video stale.

Review (`presentation-video-review`):

- FR-020: Review must have two gates. Before voicing: script check and source
  check. Before delivery: check stills, listening check, measured file
  properties.
- FR-021: The still inspection must look for missing characters, missing
  markers, clipped or overlapping text, a pointer or highlight on the wrong
  element, and a picture that contradicts the spoken line.
- FR-022: The listening check must cover mispronounced terms, wrong emphasis,
  audible cuts between lines, speaking pace outside the stated range, pauses
  that feel long or missing, and a tone that is flat or exaggerated.
- FR-023: Findings must be recorded with severity, scene, line and evidence. A
  video is not ready while a Critical or Important finding is open.

Configuration and credentials:

- FR-024: The repository must contain `env/azure-speech.env.example` with
  variable names, purpose, where to obtain the value and no values, and
  `env/elevenlabs.env.example` with the non-secret settings of that provider
  (voice, model, style) and a note that access runs through the connector. Real credential files must be ignored by version
  control and excluded from packaging.
- FR-025: The location of the credential file must be configurable; the
  default must not assume any particular project or home directory layout.
- FR-026: A video profile template must cover: provider and voice, voice
  style, speaking rate, pause between lines, language, pace range, maximum length, resolution and frame rate, loudness target, branding,
  opening sequence, render location, delivery location and retention of
  intermediate files.

Method integration:

- FR-027: The three skills must be registered as method skills, appear in the
  plugin inventory and documentation, and carry trigger descriptions that
  exclude one another and the existing documentation skills.
- FR-028: Trigger cases must cover: tutorial video from sources, production
  from an accepted script, review of a finished video, a one-line correction,
  and the negative cases in AC-012.
- FR-029: Organization-specific facts (voice names in use, host names, storage
  paths, opening sequences) must not appear in the plugin; they belong in the
  target project's video profile.

## Compatibility boundaries

- Existing behavior that must remain unchanged: the ten existing writing
  skills, their triggers and artifacts; all Core-managed files and the core
  lock; installation and coexistence with Engineering Method.
- Migration and rollback expectations: the eleven existing projects are not
  migrated by this feature. The template must be able to host one of them
  with changes limited to configuration, shown once as evidence. Rollback is
  removal of the new skills, templates and examples; no state format changes.
- Data, security, performance, and platform constraints: no credential, key
  fragment or provider response containing one may be written to the
  repository, logs or events. Paid requests happen only after the script gate.
  External tools (composition framework, media tools, speech providers) are
  dependencies the plugin names and checks for, and does not install.
  Supported hosts are those Writing Method already supports.

## Interface contracts

| Contract ID | Boundary | Inputs | Outputs | Errors or invariants |
|---|---|---|---|---|
| IC-001 | Script artifact | Audience, goal, sources | Chapters, scenes, narration lines with caption, optional spoken form, optional caption-hidden flag, optional minimum display time | One audience; every scene has one message; line order is stable |
| IC-002 | Pronunciation list | Term, spoken form or pronunciation markup, language, key-term flag | Applied spoken form for every occurrence; sample sentences for key terms; per-line recognition result | One entry per term; conflicts are an error; a key term failing recognition blocks the delivery gate |
| IC-003 | Voicing | Narration lines, pronunciation list, profile, credential file | One sound file per line, manifest of measured lengths, count of characters voiced | Same input yields no new request; failure keeps completed files; never prints credentials; the connector path never repeats a generation as a retry |
| IC-004 | Timeline | Narration data, manifest | Start and length per line, length per scene and video, caption file | Pure function of its inputs; no authored start times |
| IC-005 | Check stills | Scene subset or all, output directory | One image per line, named by scene and line | Fails if manifest is missing or stale |
| IC-006 | Delivery check | Rendered file, profile | Measured resolution, frame rate, loudness, peak, duration; pass or fail | Measures the file, never trusts the render exit status |
| IC-007 | Video profile | Target project | House choices listed in FR-026 | Absent profile triggers creation; unknown keys are reported |
| IC-008 | Credential examples | Fresh clone | Example files, written setup steps, credential check | No values in the repository; real files ignored and unpackaged |
| IC-009 | Review record | Script, stills, file measurements | Findings with severity, scene, line, evidence; gate status | Ready only with no open Critical or Important finding |

## Edge cases

- A line's animation needs longer than its speech: the minimum display time
  extends the slot; later lines shift.
- A provider mispronounces a term despite an override: the listening check
  records it; the override is corrected in the pronunciation list, not in the
  line.
- Per-scene voicing returns a take that skips or repeats a sentence: the match
  threshold rejects it and a new take is requested; the stored download is
  kept because provider links expire.
- A font lacks a character used on screen: the still inspection must catch it;
  the template states which character ranges its fonts cover.
- The render machine is unreachable: local rendering remains available and is
  slower; no partial file is reported as a result.
- A video serves two audiences: two scripts and two outputs may share one
  project and its scenes.
- The source system changes after delivery: the project record names the
  trigger; the correction path is US-004.
- Both providers are configured: the profile decides; the choice is recorded
  per video.
- A sound file exists but its line was deleted: it is removed on the next run.
- The opening sequence has a different stream format: it is re-encoded once
  and the user is told why.

## Assumptions and unresolved decisions

- The reference composition framework is Remotion with ffmpeg for
  measurement and joining, because all eleven projects use it. Requirements
  are written so another framework could satisfy them. Effect: planning may
  bind the template to these tools.
- ElevenLabs is reached through its connector in the assistant session
  (maintainer decision, 2026-11-13); no ElevenLabs key is stored by this
  method. Consequence: that path needs an interactive session with the
  connector authorized, while the Azure path can run unattended. Whether the
  connector's own timing data can replace separate speech recognition for
  splitting is left to planning.
- Default speaking pace, pause between lines, sentence-length limit, minimum
  text size and loudness target will be proposed in planning from measurements of the existing
  videos (current practice: integrated loudness near −16 LUFS, 1920×1080 at
  30 frames per second). Effect: numeric gates are profile values with
  defaults, not constants.
- GitHub Issues of this repository are the canonical backlog (maintainer
  decision, 2026-11-13). `WM-001` is its first work ID.
- The folder for credential examples is `env/` (maintainer decision,
  2026-11-13).
- Out of scope: marketing and short-form video, filmed material, screen
  recording, music composition, publishing to video platforms, automatic
  installation of tools, migration of existing projects.

## Success measures

- SC-001: A person who has not built a video before produces the sample video
  from a fresh clone by following the written steps only.
- SC-002: Correcting one sentence in a finished ten-minute video takes one
  provider request and no manual timing change.
- SC-003: The seeded-defect project of US-003 yields all five findings.
- SC-004: Three consecutive videos from one profile measure within the
  loudness tolerance of each other.
- SC-005: A repository-wide and package-wide search for credential values
  finds none.
- SC-006: None of the existing trigger cases changes its selected skill.

## Playbook obligations

| ID | Class | Scenario and trigger | Source | Audience | Acceptance criteria |
|---|---|---|---|---|---|
| `PB-WM-VIDEO-001` | System | Produce and deliver a presentation video from an accepted script, including resumption after interrupted voicing, an interrupted render, a rejected take and a failed delivery check | US-002, US-004, AC-005, AC-007 | An author or assistant who has the project and a configured provider, without knowledge of earlier videos | Delivered as a template that a target project instantiates with its video profile; covers decisions (provider mode, local or separate render), failure paths and verification; reviewed with `playbook-review`; rehearsed once end to end on the sample video |

Credential setup (US-005) is a short linear procedure with a built-in check
and needs no playbook. Scripting and review are ordinary skill use and need
none. Development-operation playbooks are assessed in planning. Policy:
[shared playbooks](../../../shared/policies/playbooks.md).
