# Story vault: instructions for agents

This file is the authority for agents working in this vault. `CLAUDE.md` only imports it. The `story-bootstrap` skill of the Writing Method plugin writes and refreshes both files when it sets up or resumes a vault; put lasting story decisions in `00-project/`, not here. The plugin's story skills are experimental.

## Which rules govern which text

Manuscript files follow 00-project/voice.md and nothing from documentation or didactic writing rules. Other vault notes are plain working notes. Replies to the author stay reader-oriented; the voice sheet never styles a reply.

`README.md`, `START.md`, `AGENTS.md` and `CLAUDE.md` are written for a reader, like a reply.

## Vault kind

Read `kind` and `story_id` from the frontmatter of `00-project/brief.md` and `00-project/voice.md`. These two files decide; no other note carries these fields, and a value found in any other note is stale.

| `kind` | Meaning | What is allowed |
| --- | --- | --- |
| `starter` | The unchanged template | No drafting. Use `story-bootstrap` to set the vault up first. |
| `story` | One story's own vault, with a set `story_id` | Manuscript drafting, once the voice sheet is ready |
| `study` | An analysis vault for an existing work | Study notes only. Never draft against the studied work's canon. |

Drafting also needs `viewpoint`, `tense` and `distance` set in the frontmatter of `00-project/voice.md`. While one of them is `unset`, run the voice trial first.

`story_id` lives only in frontmatter. It is set once and never changes.

## Form and where manuscript text lives

`form` in `00-project/brief.md` is `long-form` or `short-form`.

| Form | Manuscript | Working notes for the same unit |
| --- | --- | --- |
| `long-form` | `06-manuscript/chapters/<chapter-id>.md`, prose only. Afterword, author note and blurb in `06-manuscript/paratext/`. | Chapter card in `05-plot/chapters/<chapter-id>.md`: context packet, beats, summary, canon delta, review |
| `short-form` | The text under the heading `## Manuscript` of one note per piece in `06-manuscript/pieces/` | Everything outside that heading in the same note |

Afterword, author note and blurb live in `06-manuscript/paratext/` in both forms. In-world documents, such as a letter, a report or a manual that exists inside the story, are manuscript. `06-manuscript/index.md` gives the order; do not rely on file names.

`publication_profile` in the brief is `unset`, `web-serial`, `light-novel` or `both`. It may stay unset. The only default the method supplies is about 100 chapters per sub-arc under `web-serial` (see `90-templates/arc.md`); otherwise do not assume lengths, chapter counts or illustration counts for a profile, and use only figures the author has recorded.

## Before you write

1. Read `START.md`, then `00-project/development.md` and `00-project/decisions.md`. Resume from what exists; do not restart the interview.
2. Pick the plugin skill that matches the requested work: `story-bootstrap`, `story-worldbuilding`, `story-characters`, `story-architecture`, `story-drafting`, `story-canon-review`, `story-voice-review` or `story-craft-research`. If the plugin is not installed, say so; this file does not replace it.
3. Resolve story paths from this vault's root.

## Canon and decisions

This vault owns its manuscript and its accepted canon. Keep proposed, accepted, published and superseded material distinct. Cite the original passages when you report a contradiction. Do not invent story facts to fill a template, and do not treat an unanswered question as acceptance.

A chapter is complete when a canon review exists at a named revision and the author's acceptance is recorded. That is the author's decision, not the result of a command. This vault has no backlog; its state lives in `00-project/development.md` and `00-project/decisions.md`.

## Retrieval

If a memory or retrieval tool is available, follow `00-project/retrieval.md`: the vault is the authority, a retrieved result is advisory, and the scope is this vault's Git root. If no such tool is available, skip retrieval entirely and read the files.
