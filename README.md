---
type: reference
audience: Authors and maintainers familiar with their coding assistant and Git
version: 0.4.0
---
# Writing Method

Writing Method provides reader-oriented writing, documentation planning, review, local PDF delivery and narrated tutorial videos for Claude, Codex and OpenCode. A separate, experimental family of skills supports story writing; see [Story writing (experimental)](#story-writing-experimental). Install it on its own or alongside [Engineering Method](https://github.com/phense/engineering-method). Both bundle shared support from [Method Core](https://github.com/phense/method-core); no sibling checkout is needed at runtime.

The three repositories remain under `phense`, share the `agent-methods` topic and have independent Issues and pull requests. Report a writing behavior here, an engineering behavior in Engineering Method, and shared adapter/state/playbook behavior in Method Core.

## Included skills

| Purpose | Skills |
|---|---|
| Plan, write and review | documentation-planning, documentation-authoring, documentation-review |
| Produce reviewed PDFs | documentation-pdf |
| Explain and instruct | explaining-concepts, writing-procedures, empathic-troubleshooting |
| Keep prose and documents consistent | human-prose-drafting, terminology-guard, visual-placeholders |
| Script, produce and review narrated tutorial videos | tutorial-video-scripting, presentation-video-production, presentation-video-review |
| Write stories (experimental, separate family) | story-bootstrap, story-worldbuilding, story-characters, story-architecture, story-drafting, story-canon-review, story-voice-review, story-craft-research, story-video-scripting |
| Shared support from Core | project-backlog, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, dispatching-parallel-agents, playbook-authoring, playbook-review |

Describe the outcome to your assistant. A small wording edit needs focused editing; a standalone document uses authoring and self-review; a coherent document set uses planning, authoring and review. PDF generation follows content review and offers two layouts: a single-sided one for short documents and a book layout with parts, mirrored pages and a running head for long manuals. A tutorial video is scripted, produced and reviewed in that order; see [Narrated tutorial videos](#narrated-tutorial-videos). Playbooks support concrete publication/export operations when their decisions or recovery needs warrant one; ordinary writing does not automatically create one.

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

## Story writing (experimental)

The **story family** is a second set of skills, for fiction: long serials, light novels and short pieces. Think of two workbenches in one workshop. Documentation is built at one and stories at the other, and the tools of one bench are not carried to the other. The reason is that the two kinds of text want opposite things. A how-to guide should be plain, complete and predictable. A chapter may use fragments, repetition and withheld information on purpose.

Each story lives in its own directory with its own Git repository, called a **story vault**. The vault holds the brief, the **voice sheet** (how this story's prose sounds: viewpoint, tense, distance, tone), the world and character notes, the plans and the manuscript.

| Purpose | Skill |
|---|---|
| Start or resume a story vault | story-bootstrap |
| Build the world, its history and institutions | story-worldbuilding |
| Design characters and their voice cards | story-characters |
| Plan the whole story, arcs, volumes and chapters | story-architecture |
| Draft chapters, in-world documents and paratext | story-drafting |
| Check a chapter against the accepted canon | story-canon-review |
| Judge chapters against the voice sheet | story-voice-review |
| Study craft sources and existing works | story-craft-research |
| Script a narrated video from an accepted chapter | story-video-scripting |

### Which rules apply to which text

The rule set is chosen for each piece of text, not for the session or the subject. Talking about a story is still an ordinary reply.

| Text | Mode | Governed by |
|---|---|---|
| Story prose, in-world text such as a letter or manual inside the story, afterword and blurb, a listening edition, the narration of a story video | manuscript | The story's voice sheet, then the story rules. Nothing from the documentation skills. |
| Any other note in a story vault or study vault: brief, world entry, chapter card, review, study note | working note | The story skills. Plain notes without the story's voice and without didactic structure. |
| Everything else: every reply to you, a vault's `README.md`, documentation, tutorial videos | reader-oriented | The rules of the sections above, unchanged |

The full rule, including how a vault is recognized and when drafting is permitted, is in [writing mode](shared/policies/writing-mode.md).

### Start a story

1. Copy the vault starter `templates/story-vault/` from this plugin to a new directory outside the plugin.
2. Run `git init` in the new directory.
3. Open your assistant in that directory and ask it to start a story with your premise.

The assistant marks the vault as a story, gives it a story ID and asks for the form (long or short) and the publication profile, which may stay unset. Check: the frontmatter of `00-project/brief.md` now reads `kind: story`. Drafting starts only after viewpoint, tense and distance are set in `00-project/voice.md`; until then the assistant leads you to a voice trial instead of writing a chapter.

### Narrated story videos

An accepted chapter, a range of chapters or a short piece can become a narrated video: an audiobook with pictures. The work is split by who owns what. The story family owns the text: `story-video-scripting` turns the accepted manuscript into the script of a video project. `presentation-video-production` and `presentation-video-review` voice, render and check that script and never restyle it.

The narration comes in one of two **editions**. A `verbatim` edition reads the accepted manuscript word for word, only cut into scenes and lines at sentence boundaries. A `listening` edition contains additions or changes for the ear; each one is your decision, and it is stored beside the manuscript, which stays unchanged. A video that explains a story's world to its readers is a tutorial video and stays with `tutorial-video-scripting`.

No video has been produced with this path. How invented names are pronounced and where the pictures come from are not designed yet: the existing pronunciation list is used as it is, and a scene's picture is a plain description in the script.

### Limits

- **Routing is statistical.** The tests prove that names, exclusion sentences and links are in place. Whether an assistant then picks the right family for a request is a probability, not a guarantee.
- **Produced text is not measured.** No check reads a chapter for documentation habits, or a reply for a story's voice.
- **No story pilot exists.** The skills are structurally checked and have not been proven on a real story. Light-novel figures such as volume length are left unset, not asserted.
- **No story video exists.** The script check and the routing expectations for story videos are tested; nothing has been voiced or rendered from a story script.
- **Host routing is checked once, not measured as a rate.** The twelve story routing cases under `evals/shared/triggers/` pass on Claude and Codex after two corrections; the record, including the two expectations changed after the first run, is in `docs/specs/WM-003-story-family/rehearsal.md`. With the story family present, eight of the nine earlier documentation and video cases pass on both hosts; `presentation-video-production` fails, as it already does on Codex without the story family. The two story video cases added later, `story-video-script` and `story-video-production`, have not been run on a host. OpenCode was not exercised.

The family originated in a private research workspace. That workspace's research notes and its studies of existing works are not part of this plugin.

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

Restart the assistant session after installation and inspect its plugin inventory for `writing-method` 0.4.0. An installed listing proves discovery; a live authoring request is separate behavior evidence. With both methods installed, use the invoking method's namespace for shared support, such as `writing-method:playbook-authoring`, and run one copy.

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

These checks cover installed-relative resources, source integrity, state behavior, isolated package use and OpenCode coexistence. PDF generation additionally needs the tools/fonts described by `documentation-pdf`; this plugin does not install them automatically. Video tests that need `ffmpeg` are skipped where it is absent; the timing, script-check and pronunciation logic is tested without it. A rendered sample video and a provider run are separate evidence, recorded in `docs/specs/WM-001-presentation-video/rehearsal.md`. Source tests and native plugin installation do not prove model routing, content quality or provider availability. The story family is experimental; its limits are listed under [Story writing (experimental)](#limits). No live Claude result is claimed during an outage.

Original code uses the [MIT License](LICENSE). Adapted Humanizer material is listed in [third-party notices](THIRD_PARTY_NOTICES.md); shared adaptations retain [Core notices](CORE_NOTICES.md). The project is independent of the named assistant providers.
