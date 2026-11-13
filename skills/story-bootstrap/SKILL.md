---
name: story-bootstrap
description: "Use when a story project must be started or resumed: creating a story's own Markdown/Obsidian vault from the starter, setting its kind, story ID, form and publication profile, recording the story brief and first voice decisions, or picking up an existing vault. Not for inventing a story during method research, for an analysis vault of an existing work, or for drafting chapters. Not for session replies, documentation or presentation videos."
---

# Story bootstrap

Mode check first, under [writing mode](../../shared/policies/writing-mode.md): find the nearest ancestor of the target file that holds 00-project/brief.md and 00-project/voice.md. Only kind story permits manuscript drafting; kind study permits study notes only; kind starter routes to story-bootstrap.

No run state: this skill has no recovery preamble and hands off to no backlog or run-tracking skill. A story or study vault keeps no backlog and no run directory; its state lives in 00-project/development.md and 00-project/decisions.md.

Read [workflow](../../shared/story/workflow.md) and [rules](../../shared/story/rules.md). Read the [retrieval contract](../../shared/story/retrieval.md) only if a memory or retrieval tool is available. Paths in this skill resolve from its own folder; story paths resolve from the selected vault.

For a minimal idea or a resumed development conversation, use [guided story development](../../shared/story/story-development.md). Read `00-project/development.md` and `00-project/decisions.md` when they exist; update them from the conversation rather than requiring the author to fill forms. Ask only the next consequential unresolved question and preserve prior delegation.

Inspect the requested destination first. Resume an existing story without overwriting its artifacts. For a new story, copy the [vault starter](../../templates/story-vault/START.md) and its whole directory into a unique story path outside the installed plugin and outside any other vault. Keep the template source untouched. Never draft in a vault whose kind is still `starter`: the starter is a template, and a copy stays a starter until the steps below are done.

## Set the vault marker

The frontmatter of `00-project/brief.md` and `00-project/voice.md` is the vault's marker. Set it in both files:

- `kind: story`. A vault for analysing an existing work gets `kind: study` instead and belongs to `story-craft-research`; do not set it up here as a story.
- `story_id`: one unique ID, the same in both files. It lives only in frontmatter, is set once and never changes. Use that ID in instantiated notes; template IDs remain templates.
- `form` in the brief: `long-form` or `short-form`. It decides where prose is stored; see the storage rule in the workflow.
- `publication_profile` in the brief: ask the author whether the story is meant as `web-serial`, `light-novel` or `both`. It may stay `unset`; do not choose it for the author, and do not derive lengths from it.

Loreweaver-ready templates use `type: template` plus `template_type`; on instantiation set `type` to the intended native type and remove `template_type`. Loreweaver ignores canon status when indexing.

## Write the vault instruction files

On create and on every resume, write or refresh the vault's `AGENTS.md` and `CLAUDE.md` from the starter's current [AGENTS.md](../../templates/story-vault/AGENTS.md) and [CLAUDE.md](../../templates/story-vault/CLAUDE.md). `AGENTS.md` is the authority and states which rules govern manuscript, working notes and replies; `CLAUDE.md` stays a thin adapter that imports it. If the vault's copies differ from the starter, bring the method's text up to date, keep lines the author added, and report what changed. Lasting story decisions belong in `00-project/`, not in these files.

## Brief and first voice decisions

Extract the author's premise, intended reader experience, language, genre, central conflict and ending intent. Record known decisions in `00-project/brief.md`; mark unresolved items explicitly. Ask only for information necessary to choose the next action. Offer provisional alternatives when authorized; never represent them as accepted author decisions. No mandatory interview overrides the author's instructions.

Record what the author has already decided about narrative perspective, tense, distance, register and dialogue conventions in `00-project/voice.md`, using the author's own samples when available. Set the frontmatter fields `viewpoint`, `tense` and `distance` only from an author decision. When the author's decision sets all three without a trial, that decision is the acceptance of V1: set `voice_revision: V1`, add the change-log row and record the decision in `00-project/decisions.md`. Parts of the sheet that are still empty stay marked as undecided; the anchor passages a voice review needs still come from the voice trial. While any of the three is `unset`, the sheet stays at `V0` and drafting is not permitted: route to the voice trial, pass E of guided story development, whose output is the accepted voice sheet V1 described in [voice and tone](../../shared/story/voice-and-tone.md).

Build only enough world and character context to test the premise. Route world design to `story-worldbuilding`, cast work to `story-characters`, and arc planning to `story-architecture`. The available artifact and the author's request decide the next task; do not restart a completed stage.

## Repository and retrieval

Give the vault its own Git repository, and keep its contents outside any parent repository's index. A story vault gets no backlog; its state lives in `00-project/development.md` and `00-project/decisions.md`.

If a memory or retrieval tool is available and the author wants it used, record the scope in `00-project/retrieval.md`: the vault's Git root, nothing wider. A folder alone is not story isolation. Verify the saved scope against the vault root before treating the boundary as established. If no such tool exists, leave that note unused.

## Finish

Finish with the created or resumed vault location, the marker values now set, established choices, unresolved consequential choices and the next usable artifact. Do not install community plugins, publish chapters or invent a first novel because the author only asked to build the method.

`verification-before-completion` applies only to checks that have a command, such as link checks or template integrity. Whether the brief or the voice sheet is right is an author decision.

Status: experimental. This skill has not been piloted on a story and makes no claim about reader effect.
