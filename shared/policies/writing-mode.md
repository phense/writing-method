# Writing Mode

Status: experimental. This policy separates two families of skills in one
plugin, names the form skills that serve both, and decides which rule set
governs one piece of output. It makes no
quality claim for either family and rests on no pilot evidence.

- The **story family** covers fiction: every skill whose name starts with
  `story-`, the files under `shared/story/` and the vault starter under
  `templates/story-vault/`.
- The **reader family** covers everything else this method writes: didactic
  replies, documentation, PDF delivery and tutorial-video scripts.
- The **form family** writes no text of its own: `presentation-video-production`
  and `presentation-video-review` voice, time, render and check an accepted
  video script of either family and never restyle its narration.

This file is the neutral hub and the authority for the mode rule. All three
families refer to it; it links into none. The operative sentences that skills and
vault files carry are stored in the policy block at the end and are tested
against it.

## Terms

| Term | Meaning |
|---|---|
| Story vault | One story's own directory: brief, voice sheet, canon, plans and manuscript. Marked `kind: story`. |
| Study vault | An analysis vault for an existing work by someone else. Marked `kind: study`. |
| Starter | The unchanged vault template. Marked `kind: starter`. Nothing is drafted in it. |
| Manuscript | Story prose and in-world text (a letter, report or manual that exists inside the story), plus paratext: afterword, author note and blurb. |
| Working note | Any other vault file that is neither a reader-facing vault file nor a reader-facing deliverable: brief, world entry, character note, arc, chapter card, canon review, study note. |
| Voice sheet | `00-project/voice.md` of a story vault. It overrides every method default for how that story's manuscript sounds. |
| Form skill | A skill that owns a delivery form, not a text. It takes an accepted script from the reader family (a tutorial video) or the story family (a story video) and changes no wording. |
| Edition | The text a story video narrates. `verbatim`: the accepted manuscript, only segmented into scenes and lines at sentence boundaries. `listening`: a derived text with changes for the ear, each one an author decision recorded in the edition file. The written manuscript stays unchanged; a listening edition is not canon. |
| Writing mode | The rule set that governs one piece of output: `manuscript`, `working-note` or `reader-oriented`. |

## Mode decision

The mode belongs to the output, not to the session. Test the conditions in
order and stop at the first that holds.

| Order | Condition | Mode | Governed by |
|---|---|---|---|
| 1 | The file is a reader-facing vault file (`README.md`, `START.md`, `AGENTS.md` or `CLAUDE.md`) or a reader-facing deliverable about the story or the vault, wherever it is stored: documentation or a tutorial-video script with its production files | `reader-oriented` | The reader family's rules |
| 2 | The text is story prose, in-world text or paratext: it goes into a manuscript location of a `kind: story` vault, or the author explicitly asks for story prose | `manuscript` | The voice sheet, then `shared/story/rules.md`. Nothing from the reader family. |
| 3 | The text is another file of a story or study vault, or a research note | `working-note` | The story skills. Plain notes: neither the voice sheet nor didactic structure. |
| 4 | Everything else, including every reply to the author | `reader-oriented` | The reader family's rules, unchanged |

The subject never sets the mode. A reply that talks about a story is still a
reply, and it stays reader-oriented inside a story vault as well.

## Signals

A vault is the nearest ancestor of the target file that holds both
`00-project/brief.md` and `00-project/voice.md`. Its `kind` field in the
frontmatter decides what may be written there.

| `kind` | Permits | Otherwise |
|---|---|---|
| `story` | Manuscript drafting, once `story_id` is set and the voice sheet has `viewpoint`, `tense` and `distance` filled | With one of the three fields still `unset`, the work goes to the voice trial first |
| `study` | Study notes only | A drafting request is declined; nothing is drafted against the studied work's canon |
| `starter` | Nothing | The work goes to `story-bootstrap`, which creates the story vault |

Outside any vault, a requested draft passage is still `manuscript`. The method
defaults apply, and the reply states that no voice sheet applies.

## Storage decision

A path or a heading must be able to say which mode applies, so manuscript text
has fixed locations. The vault's `form` field selects between two layouts.

| `form` | Manuscript location | Working notes |
|---|---|---|
| `long-form` | Prose-only files under `06-manuscript/chapters/`, one per chapter; afterword, author note and blurb under `06-manuscript/paratext/` | The chapter card with context packet, beats, summary, canon delta and review, under `05-plot/chapters/` |
| `short-form` | The text under the heading `## Manuscript` of the piece's single note in `06-manuscript/pieces/` | Everything outside that heading in the same note |

In both forms a listening edition is a prose-only file under
`06-manuscript/editions/listening/`, one per chapter or piece. It is manuscript
and follows the voice sheet; it names the manuscript revision it is based on.
A verbatim edition needs no file: the manuscript itself is the text.

The split into prose files applies to long-form work only. A short piece keeps
card and prose in one note, and the heading draws the line: only the text under
`## Manuscript` is manuscript, although the note lives in `06-manuscript/pieces/`.
Afterword, author note and blurb live under `06-manuscript/paratext/` in both
forms. In both layouts a later export reads manuscript text without extracting
it from notes.

## Where the rule is read

No host loads a policy file before it selects a skill; only skill descriptions
are always in context. The operative sentences therefore sit where they are
read, and this file is what they are compared with.

| Carrier | Content |
|---|---|
| Description of every story skill | Ends with the exclusion of session replies, documentation and presentation videos |
| First paragraph of every story skill body | The mode check: find the vault, read its kind |
| Second paragraph of the story skills listed under `precedence_story_skills` | The precedence sentence: the voice sheet overrides the four didactic and prose skills for manuscript text |
| Description of the eight reader skills listed under `excluded_reader_skills` | Ends with the exclusion of story manuscripts and in-world text |
| First paragraph of the four reader skill bodies listed under `precedence_reader_skills` | Stop when the target is manuscript, and use the story family |
| `AGENTS.md` of a story vault, with `CLAUDE.md` as its adapter | The mode rule in three sentences, written or refreshed by `story-bootstrap` when it creates or resumes a vault |

## Layers and what each proves

| Layer | What it does | What its test proves |
|---|---|---|
| 1. Names | Every story skill starts with `story-`; no name equals a shared, reader or engineering skill name or contains `continuity` | The names are as stated |
| 2. Descriptions and opening lines | Reciprocal exclusions and the precedence sentence | The sentences are present and equal the policy block. Whether a model follows them is statistical. |
| 3. Link firewall | Story files link only into `shared/story/`, `templates/story-vault/`, other story skills, this file, `shared/policies/proportionality.md` and `skills/verification-before-completion/SKILL.md`. For a story video they also link the video project template, the two form skills and `shared/media/speech-synthesis.md`. Reader files and form skills never link into the story directories. Backticked skill names are checked against the family map as well; form skills may be named by both families and may name skills of both. | A skill cannot pull the other family's rule files in through links |
| 4. No lifecycle graph | No story skill appears in `shared/policies/lifecycle-handoffs.md` | The graph contains no story node |
| 5. Vault kind | Only `kind: story` permits drafting, and only with the three voice fields filled | The starter and the skills state the rule |

Layers 1 to 4 have deterministic presence tests. That is a weaker statement
than "the separation is deterministic": the tests show that the text is there,
not that a host obeys it.

## Limits

- **Both rule sets can sit in one context.** The author asks why a part of the
  world works, a didactic skill loads, and the next request is a chapter draft.
  No link rule prevents that. The precedence sentence addresses it, and where
  the host allows, `story-drafting` drafts from the chapter context packet in a
  fresh sub-agent or session.
- **Routing checks read skill selection, not text.** Whether a chapter opens
  with an analogy, or a reply drifts into a story's voice, is unmeasured. The
  family keeps the experimental label until an output-level check exists and
  passes.
- **Shared skills are not edited here.** `receiving-code-review` claims
  unverified review feedback, which also describes beta-reader comments. If a
  shared description captures story work, the correction belongs in the shared
  core, not in this plugin.

## Mixed situations

| Situation | Disposition |
|---|---|
| A reply that discusses plot, characters or craft | `reader-oriented` |
| A reply that contains a draft passage | The passage goes into a manuscript location or a fenced block and is `manuscript`; the surrounding reply never restyles it |
| A draft passage requested outside any vault | `manuscript` with the method defaults; the reply states that no voice sheet applies |
| Documentation about the story method; a vault `README.md` | `reader-oriented`, under `documentation-authoring`. Story skills may be read as source material; they do not govern the document. |
| An in-world document, including an in-world how-to manual | `manuscript`, under `story-drafting` |
| A story excerpt quoted in documentation | Quoted material, unchanged |
| An explanatory narrated video about a story or its world | `reader-oriented`, under `tutorial-video-scripting` |
| A tutorial video about a story, its world or the story method | Stays with `tutorial-video-scripting`, also inside a story vault; no story skill scripts it |
| Narration of a story video (an accepted chapter, range or short piece read aloud over pictures) | `manuscript`, written by the story family under `story-video-scripting`, as a `verbatim` or a `listening` edition; voiced and rendered by the form skills, which never restyle it. Wording findings return to the story family and the author. |
| Any other dramatised fiction: an audio-only book, a performance with several voices | Outside the method for now |
| Beta-reader or author feedback on a chapter | `story-canon-review` for canon, `story-voice-review` for voice; not `receiving-code-review` |
| Notes and craft exercises in a study vault | `working-note`, under `story-craft-research`; never a draft against the studied work's canon |

## Completion in the story family

A chapter is complete when a canon review exists at a named revision and the
author's acceptance is recorded. That is an author decision, not a command
result, so no story skill hands off to a pass claim.
`verification-before-completion` applies only to checks that have a command:
links, template integrity, an export. A story vault gets no backlog; its state
lives in `00-project/development.md` and `00-project/decisions.md`.

## Orchestration

`shared/story/story-development.md` is the only orchestration authority of the
story family. Its passes overlap and return, so the family is not a linear
lifecycle and is not part of the lifecycle handoff graph.
`shared/policies/lifecycle-selection.md` sends story work to the family and
selects nothing inside it.

## Policy block

Tests compare the skills, the vault starter and the link rules with this block.
The entries under `sentences` are the exact text the carriers hold.

```json
{
  "schema_version": 1,
  "status": "experimental",
  "families": {
    "story": ["story-bootstrap", "story-worldbuilding", "story-characters", "story-architecture", "story-drafting", "story-canon-review", "story-craft-research", "story-voice-review", "story-video-scripting"],
    "reader": ["documentation-planning", "documentation-authoring", "documentation-review", "documentation-pdf", "human-prose-drafting", "explaining-concepts", "writing-procedures", "empathic-troubleshooting", "terminology-guard", "visual-placeholders", "tutorial-video-scripting"],
    "form": ["presentation-video-production", "presentation-video-review"]
  },
  "hub": "shared/policies/writing-mode.md",
  "story_link_allow": {
    "prefixes": ["shared/story/", "templates/story-vault/", "skills/story-", "templates/presentation-video/"],
    "files": ["shared/policies/writing-mode.md", "shared/policies/proportionality.md", "skills/verification-before-completion/SKILL.md", "skills/presentation-video-production/SKILL.md", "skills/presentation-video-review/SKILL.md", "shared/media/speech-synthesis.md"]
  },
  "reader_link_deny_prefixes": ["shared/story/", "templates/story-vault/", "skills/story-"],
  "form_link_deny_prefixes": ["shared/story/", "templates/story-vault/", "skills/story-"],
  "precedence_reader_skills": ["explaining-concepts", "writing-procedures", "empathic-troubleshooting", "human-prose-drafting"],
  "excluded_reader_skills": ["explaining-concepts", "writing-procedures", "empathic-troubleshooting", "human-prose-drafting", "documentation-authoring", "documentation-review", "terminology-guard", "tutorial-video-scripting"],
  "precedence_story_skills": ["story-drafting", "story-voice-review", "story-video-scripting"],
  "vault": {
    "markers": ["00-project/brief.md", "00-project/voice.md"],
    "kinds": ["story", "study", "starter"],
    "drafting_kind": "story",
    "drafting_requires_voice_fields": ["viewpoint", "tense", "distance"],
    "forms": ["long-form", "short-form"],
    "manuscript_paths": ["06-manuscript/chapters/", "06-manuscript/paratext/", "06-manuscript/editions/"],
    "short_form_manuscript_heading": "## Manuscript",
    "reader_files": ["README.md", "START.md", "AGENTS.md", "CLAUDE.md"]
  },
  "sentences": {
    "story_opening": "Mode check first, under [writing mode](../../shared/policies/writing-mode.md): find the nearest ancestor of the target file that holds 00-project/brief.md and 00-project/voice.md. Only kind story permits manuscript drafting; kind study permits study notes only; kind starter routes to story-bootstrap.",
    "precedence": "For manuscript text the story's voice sheet overrides explaining-concepts, writing-procedures, empathic-troubleshooting and human-prose-drafting, even when those skills are loaded in this session.",
    "story_description_suffix": "Not for session replies, documentation or presentation videos.",
    "reader_description_clause": "Not for story manuscripts or in-world text.",
    "reader_opening": "Not for story manuscripts or in-world text: when the target is manuscript, stop and use the story family under [writing mode](../../shared/policies/writing-mode.md).",
    "vault_instruction": "Manuscript files follow 00-project/voice.md and nothing from documentation or didactic writing rules. Other vault notes are plain working notes. Replies to the author stay reader-oriented; the voice sheet never styles a reply."
  }
}
```
