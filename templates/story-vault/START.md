# Story vault starter

This is a reusable template, not a fictional universe. It is part of the experimental story family of the Writing Method plugin. Template notes are not accepted canon and must never be indexed as story facts.

## Set up a story

1. Copy this entire folder, including `.obsidian/`, to a new directory of its own outside the plugin.
2. Make the copy its own Git repository.
3. Open a session in the copy and ask for `story-bootstrap`. The skill sets `kind: story`, a unique `story_id`, the form and, if you have decided it, the publication profile in [[00-project/brief|the story brief]], and refreshes [[AGENTS]] and [[CLAUDE]].
4. Open the copy as a vault in Obsidian if you use it. All notes are ordinary Markdown. This starter installs and enables no community plugins.

You can tell it worked when the frontmatter of the brief and the voice sheet both show `kind: story` and the same `story_id`. Until then the vault is a starter, and nothing is drafted in it.

## Notes in this vault

- [[00-project/brief|Story brief]] and [[00-project/voice|Voice sheet]]
- [[00-project/development|Development state]] and [[00-project/decisions|Author decisions]]
- [[01-world/overview|World overview]]
- [[02-history/timeline|History and pre-story interactions]]
- [[03-peoples/index|Species, cultures and factions]]
- [[04-characters/index|Cast]]
- [[05-plot/spine|Whole-story spine, arcs and volumes]]
- [[06-manuscript/index|Manuscript order]]
- [[07-continuity/state|Current state]], [[07-continuity/threads|Open threads]], [[07-continuity/changes|Canon changes]]
- [[00-project/retrieval|Retrieval record]] (optional; used only when a memory or retrieval tool is available)

## Where text goes

The brief's `form` decides the layout.

| Form | Manuscript | Working notes |
| --- | --- | --- |
| `long-form` | One prose-only file per chapter in `06-manuscript/chapters/`, from [[90-templates/chapter-prose]]. Afterword, author note and blurb in `06-manuscript/paratext/`. | One chapter card per chapter in `05-plot/chapters/`, from [[90-templates/chapter]], under the same chapter ID |
| `short-form` | The text under `## Manuscript` in one note per piece in `06-manuscript/pieces/`, from [[90-templates/short-piece]] | Everything outside that heading in the same note |

Afterword, author note and blurb live in `06-manuscript/paratext/` in both forms.

A listening edition is an optional version of an accepted chapter for a narrated video, with changes for the ear that you approved one by one. It lives in `06-manuscript/editions/listening/`, from [[90-templates/listening-edition]], and is listed in [[06-manuscript/index|the manuscript index]]. It never changes the written chapter and is not canon. A video read word for word from the manuscript needs no edition file.

Arcs use [[90-templates/arc]] and live in `05-plot/`. A volume is a packaging unit beside the arc: use [[90-templates/volume]], also in `05-plot/`, when the publication profile calls for volumes. Its numeric fields are unset; you fill them. Reviews use [[90-templates/review]] and live in `07-continuity/`. Craft notes on a source use [[90-templates/source-card]] as their format. They are not story canon and are not kept in this vault: keep them in the research workspace the author names, and cite a card here by its source ID.

World and cast notes use [[90-templates/world-entry]], [[90-templates/event]], [[90-templates/people]], [[90-templates/character]], [[90-templates/relationship]], [[90-templates/location]], [[90-templates/organization]], [[90-templates/term]] and [[90-templates/foreshadow]].

## Skills

| Work | Skill |
| --- | --- |
| Start or resume the story | `story-bootstrap` |
| World, history, peoples | `story-worldbuilding` |
| Cast, relationships, voice cards | `story-characters` |
| Spine, arcs, volumes, chapter cards | `story-architecture` |
| Manuscript prose | `story-drafting` |
| Canon, chronology and knowledge check | `story-canon-review` |
| Check prose against the voice sheet | `story-voice-review` |
| Craft sources and studies of existing works | `story-craft-research` |
| Script of a narrated video from an accepted chapter | `story-video-scripting` |

## Instantiating a template

Instantiate only the templates the story needs. Give each new note a unique stable ID, a readable file name and the actual story ID. Where a template has `type: template`, replace it with the value of `template_type`, then remove `template_type`. Change `canon_status: template` to `proposed`; acceptance follows the author's working agreement in the decisions note. Remove instructional prompts when filling a note and keep the useful headings.

Keep accepted canon separate from manuscript draft status. Back up the vault and any later plugin configuration together.

## Loreweaver

Loreweaver 0.1.2 does not filter by `canon_status` or by folder. Active `type: character` and `type: foreshadow` notes appear even when proposed or superseded, which is why reusable templates stay `type: template`. To make a superseded note disappear from Loreweaver, set `type: archived` and `original_type`, and record that decision.
