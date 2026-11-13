---
type: reference
audience: Authors and maintainers familiar with their coding assistant and Git
version: 0.2.0
---
# Writing Method

Writing Method provides reader-oriented writing, documentation planning, review, local PDF delivery and narrated tutorial videos for Claude, Codex and OpenCode. Install it on its own or alongside [Engineering Method](https://github.com/phense/engineering-method). Both bundle shared support from [Method Core](https://github.com/phense/method-core); no sibling checkout is needed at runtime.

The three repositories remain under `phense`, share the `agent-methods` topic and have independent Issues and pull requests. Report a writing behavior here, an engineering behavior in Engineering Method, and shared adapter/state/playbook behavior in Method Core.

## Included skills

| Purpose | Skills |
|---|---|
| Plan, write and review | documentation-planning, documentation-authoring, documentation-review |
| Produce reviewed PDFs | documentation-pdf |
| Explain and instruct | explaining-concepts, writing-procedures, empathic-troubleshooting |
| Keep prose and documents consistent | human-prose-drafting, terminology-guard, visual-placeholders |
| Script, produce and review narrated tutorial videos | tutorial-video-scripting, presentation-video-production, presentation-video-review |
| Shared support from Core | project-backlog, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, dispatching-parallel-agents, playbook-authoring, playbook-review |

Describe the outcome to your assistant. A small wording edit needs focused editing; a standalone document uses authoring and self-review; a coherent document set uses planning, authoring and review. PDF generation follows content review. A tutorial video is scripted, produced and reviewed in that order; see [Narrated tutorial videos](#narrated-tutorial-videos). Playbooks support concrete publication/export operations when their decisions or recovery needs warrant one; ordinary writing does not automatically create one.

## Terms

A **method** is this plugin's workflow and supporting skills. A **host adapter** maps shared operations to a coding assistant. **Core** is the shared source copied into the plugin. A **core lock** records that copy's revision, hashes and executable modes. A **work ID** identifies persistent project work. A **playbook** is a scenario-bound procedure whose draft, review and rehearsal are separate evidence.

## Narrated tutorial videos

A **presentation video** is composed from designed scenes and synthesized narration; nothing is filmed. A **tutorial video** is a presentation video that teaches. Marketing clips, filmed material and screen recordings are out of scope.

| Phase | Skill | Result |
|---|---|---|
| Script | tutorial-video-scripting | A reviewed script: one audience, one message per scene, narration written for listening, a source for every claim. The script check must pass before anything is voiced. |
| Produce | presentation-video-production | Voiced narration, a timeline derived from the measured sound, check stills, the rendered file and its measurement |
| Review | presentation-video-review | Two gates: before voicing, and before delivery (every still, a listening check, the measured file) |

Each video is a copy of the [project template](templates/presentation-video/README.md), which carries its own tools. House choices (voice, pauses, loudness, opening sequence, render and delivery location) live once in a `video-profile.json` of the target project, never in this plugin. Rules that hold for every provider are in [speech synthesis](shared/media/speech-synthesis.md); rules for the wording are in [writing for listening](shared/media/spoken-style.md).

Two speech providers are supported. Azure AI Speech is voiced line by line with a key from an env file and can run unattended. ElevenLabs is voiced scene by scene through its connector in the assistant session; this method stores no ElevenLabs key. [Credential examples](env/README.md) contain variable names only.

What the method enforces, from measurements of earlier videos:

- No time is entered by hand. The pause between sentences is one profile value (default 0.65 s) and is measured in the rendered file.
- The voice must speak the target language and English. Key terms are voiced and verified before the whole video is voiced, and read back by speech recognition afterwards.
- A provider setting counts only after its effect was measured for the voice.
- A tutorial video has no target length; above the profile's maximum (default 45 minutes) the script is split at a chapter boundary.
- Resolution, frame rate, loudness and peak are measured on the delivered file.

The video tools need Node with npm, `ffmpeg` and `ffprobe` in addition to Python. They are checked and named when missing, not installed.

## Installation

Prerequisites: a supported Claude or Codex CLI, Git, and Python 3.11 or newer for state tools. Clone this repository to a retained directory. These commands register the local checkout as a marketplace; run the pair for your host:

```sh
codex plugin marketplace add /absolute/path/to/writing-method --json
codex plugin add writing-method@writing-method --json
```

```sh
claude plugin marketplace add /absolute/path/to/writing-method
claude plugin install writing-method@writing-method
```

For a session-scoped Claude test use `claude --plugin-dir /absolute/path/to/writing-method`. For OpenCode, run `python3 scripts/install-opencode --check` from this checkout, inspect the proposed path, then repeat without `--check`. It installs an owned `writing-method.js` loader pointing to this retained directory. Gemini support is deferred until its adapter is verified.

Restart the assistant session after installation and inspect its plugin inventory for `writing-method` 0.2.0. An installed listing proves discovery; a live authoring request is separate behavior evidence. With both methods installed, use the invoking method's namespace for shared support, such as `writing-method:playbook-authoring`, and run one copy.

## Project state and updates

Backlog and continuity commands run with the target project as their working directory. Resolve their absolute paths from the installed `skills/project-backlog/SKILL.md`; do not assume the project contains `scripts/`. For compatibility, both methods keep the `engineering_method` Python import and `.engineering-method/` state directory. Existing work IDs and backlog data remain intact.

To update shared files, follow [Core's update procedure](https://github.com/phense/method-core#updating-a-consumer). Change Core first, commit it, synchronize the selected revision, then commit this repository's copied files and `method-core.lock.json` together. `python3 scripts/sync-core --check` checks the installed copy offline. Sync refuses changed managed files or unowned conflicts. After an interrupted transaction, fix any reported disk/permission problem and run `python3 scripts/sync-core --recover`; backups stay available until restoration succeeds. Sync and recovery serialize access with a persistent `.method-core-sync.lock` file. Roll back with the prior committed Core revision using `--revision`; review local edits through Git before retrying. Reinstall the plugin after updating its checkout because host caches can contain copies.

## Verification and limits

From this checkout:

```sh
python3 scripts/sync-core --check
python3 scripts/validate-plugin
python3 -m unittest discover -s tests -t . -v
```

These checks cover installed-relative resources, source integrity, state behavior, isolated package use and OpenCode coexistence. PDF generation additionally needs the tools/fonts described by `documentation-pdf`; this plugin does not install them automatically. Video tests that need `ffmpeg` are skipped where it is absent; the timing, script-check and pronunciation logic is tested without it. A rendered sample video and a provider run are separate evidence, recorded in `docs/specs/WM-001-presentation-video/rehearsal.md`. Source tests and native plugin installation do not prove model routing, content quality or provider availability. No live Claude result is claimed during an outage.

Original code uses the [MIT License](LICENSE). Adapted Humanizer material is listed in [third-party notices](THIRD_PARTY_NOTICES.md); shared adaptations retain [Core notices](CORE_NOTICES.md). The project is independent of the named assistant providers.
