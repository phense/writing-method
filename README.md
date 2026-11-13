---
type: reference
audience: Authors and maintainers familiar with their coding assistant and Git
version: 0.1.0
---
# Writing Method

Writing Method provides reader-oriented writing, documentation planning, review and local PDF delivery for Claude, Codex and OpenCode. Install it on its own or alongside [Engineering Method](https://github.com/phense/engineering-method). Both bundle shared support from [Method Core](https://github.com/phense/method-core); no sibling checkout is needed at runtime.

The three repositories remain under `phense`, share the `agent-methods` topic and have independent Issues and pull requests. Report a writing behavior here, an engineering behavior in Engineering Method, and shared adapter/state/playbook behavior in Method Core.

## Included skills

| Purpose | Skills |
|---|---|
| Plan, write and review | documentation-planning, documentation-authoring, documentation-review |
| Produce reviewed PDFs | documentation-pdf |
| Explain and instruct | explaining-concepts, writing-procedures, empathic-troubleshooting |
| Keep prose and documents consistent | human-prose-drafting, terminology-guard, visual-placeholders |
| Shared support from Core | project-backlog, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, dispatching-parallel-agents, playbook-authoring, playbook-review |

Describe the outcome to your assistant. A small wording edit needs focused editing; a standalone document uses authoring and self-review; a coherent document set uses planning, authoring and review. PDF generation follows content review. Playbooks support concrete publication/export operations when their decisions or recovery needs warrant one; ordinary writing does not automatically create one.

## Terms

A **method** is this plugin's workflow and supporting skills. A **host adapter** maps shared operations to a coding assistant. **Core** is the shared source copied into the plugin. A **core lock** records that copy's revision, hashes and executable modes. A **work ID** identifies persistent project work. A **playbook** is a scenario-bound procedure whose draft, review and rehearsal are separate evidence.

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

Restart the assistant session after installation and inspect its plugin inventory for `writing-method` 0.1.0. An installed listing proves discovery; a live authoring request is separate behavior evidence. With both methods installed, use the invoking method's namespace for shared support, such as `writing-method:playbook-authoring`, and run one copy.

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

These checks cover installed-relative resources, source integrity, state behavior, isolated package use and OpenCode coexistence. PDF generation additionally needs the tools/fonts described by `documentation-pdf`; this plugin does not install them automatically. Source tests and native plugin installation do not prove model routing, content quality or provider availability. No live Claude result is claimed during an outage.

Original code uses the [MIT License](LICENSE). Adapted Humanizer material is listed in [third-party notices](THIRD_PARTY_NOTICES.md); shared adaptations retain [Core notices](CORE_NOTICES.md). The project is independent of the named assistant providers.
