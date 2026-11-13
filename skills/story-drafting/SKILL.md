---
name: story-drafting
description: "Use when story manuscript must be drafted or revised: scenes, chapters and short pieces with controlled viewpoint, distinctive voice, dialogue, rhythm and canon dependencies, including in-world documents such as a letter, report or manual inside the story, and afterword or blurb. Not for documentation humanizing, for promises to evade AI detectors, or for judging accepted prose. Not for a listening edition of an accepted chapter for a narrated story video. Not for a study vault or an unused starter vault. Not for session replies, documentation or presentation videos."
---

# Story drafting

Mode check first, under [writing mode](../../shared/policies/writing-mode.md): find the nearest ancestor of the target file that holds 00-project/brief.md and 00-project/voice.md. Only kind story permits manuscript drafting; kind study permits study notes only; kind starter routes to story-bootstrap.

For manuscript text the story's voice sheet overrides explaining-concepts, writing-procedures, empathic-troubleshooting and human-prose-drafting, even when those skills are loaded in this session.

No run state: this skill has no recovery preamble and hands off to no backlog or run-tracking skill. A story or study vault keeps no backlog and no run directory; its state lives in 00-project/development.md and 00-project/decisions.md.

## What counts as manuscript, and where it goes

Manuscript is story prose, any document that exists inside the story (a letter, a report, a case file, an in-world how-to manual), and paratext: afterword, author note and blurb. An in-world manual is written in the voice the story gives its fictional writer, not as instructions for a real reader.

Drafting needs two things: a vault of kind story, and a voice sheet whose frontmatter fields `viewpoint`, `tense` and `distance` are all set. In a starter, stop and route to `story-bootstrap`. In a study vault, do not draft at all. When one of the three fields is `unset`, route to the voice trial, pass E of [guided development](../../shared/story/story-development.md); the trial passages it needs are the only prose written before the sheet exists, and they stay proposed as manuscript and canon; the ones the author chooses become the sheet's first anchor passages.

Write prose to the path given by `form` in the brief:

| Form | Prose goes to | Card, summary, canon delta and review go to |
| --- | --- | --- |
| `long-form` | `06-manuscript/chapters/<chapter-id>.md`, prose only, from the [chapter prose template](../../templates/story-vault/90-templates/chapter-prose.md); paratext to `06-manuscript/paratext/` | The chapter card `05-plot/chapters/<chapter-id>.md` |
| `short-form` | Under the heading `## Manuscript` of one note per piece in `06-manuscript/pieces/`, from the [short piece template](../../templates/story-vault/90-templates/short-piece.md) | The same note, outside that heading |

When the author asks for a story passage outside any vault, write it in a fenced block with the method defaults below and say that no voice sheet applies. The reply around a passage is a reply, not manuscript, and never restyles it.

Files under `06-manuscript/editions/` are created and changed by `story-video-scripting`, not here. A change that alters what happens still comes back to this skill as a manuscript revision.

## Before drafting

Read [rules](../../shared/story/rules.md), the story voice sheet and the current scene/chapter context packet described in [workflow](../../shared/story/workflow.md). Besides the files and revisions the workflow lists, the packet names the voice sheet revision in force and the voice cards of the characters who speak in this unit; see [voice and tone](../../shared/story/voice-and-tone.md). Retrieve original accepted passages for pivotal dependencies.

Where the host allows, draft from the chapter context packet in a fresh sub-agent or session, so that rules loaded earlier for other kinds of writing are not in context. Hand over the packet and this skill, not the conversation. Where the host does not allow it, draft in place; the precedence sentence above still holds.

For premise-to-pilot feedback or broad prose revision, use [story and prose quality](references/story-and-prose-quality.md). Separate narrative causality, execution of the chosen voice and author taste; select concrete questions rather than assigning a universal quality score. Consequential unresolved choices follow guided development.

## Drafting

Draft the requested unit, normally a scene or chapter. Let viewpoint determine attention, vocabulary, judgment and available knowledge. Maintain the agreed tense, distance and rules for viewpoint changes. A narrator may know more than a character only when the chosen narration permits it. Stay inside the sheet's tone palette: leave the baseline only for a permitted excursion, and return as the sheet describes.

Apply the [#1 prose rule](../../shared/story/rules.md#1-prose-rule-natural-prose) to every sentence: where the voice sheet is silent, nothing in the narration reads as machine-written.

Apply [storytelling rule #1](../../shared/story/rules.md#1-storytelling-rule-therefore--but) while drafting and as the first structural revision check: each consequential beat follows through cause and consequence or a complication that changes the response. If the passage is only an "and then" sequence, repair the story connection before polishing sentences. The causal relationship must be present in the events; the manuscript need not use the literal words "therefore" or "but". Preserve purposeful quiet consequences and intentional delayed revelation.

Ground action in concrete perceptions and decisions. Make dialogue purposeful through competing wants, omissions and subtext; distinguish speakers by experience and register, using their voice cards. Use action and reaction to show emotional change, with direct telling when it is clearer or deliberately part of the voice. Avoid explanatory lines that merely repeat what the scene already conveyed.

Choose rhythm for the moment. Preserve deliberate fragments, repeated motifs, figurative language, humor, dialect and silence. Notice generic emphasis, repeated sentence scaffolds, indiscriminate sensory lists, interchangeable banter and tidy moral conclusions. Repair them in context rather than using a banned-word list or a rigid ratio of dialogue to description.

When humor depends on misunderstanding, track each participant's intended meaning and the reader's evidence for the difference; escalation must change the situation, not merely repeat the joke louder. For a shift into drama, establish the vulnerability and allow consequences to remain after a joke. A concrete gift, task or repair can carry both practical and emotional change. These are optional craft hypotheses, not a mandatory scene formula. A quiet ending may close a relational question without adding danger.

For recurring comedy, powerful protagonists, unequal experienced time, changing self-perception, unequal romantic power, chosen rituals, resumed happy endings, viewpoint replays or transitions into drama, use the relevant questions in [serial scene review](references/serial-scene-review.md). Keep established consequences and information limits visible; the reference is optional, not a mandatory scene structure.

For danger, pursuit, combat or rescue scenes, use [action sequences](references/action-sequences.md) when tactical change, spatial orientation or surviving consequences need attention. These are provisional lenses, not a required fight formula.

## Named method defaults

These names let a draft note or a voice review point at one default. They apply where the voice sheet and the voice cards are silent; a clause of the sheet or a card always wins, and a recorded deliberate exception is not a defect. A review that relies on one of them labels the finding "method default, not sheet".

| Name | Default |
| --- | --- |
| Causal beats | Consequential beats connect through consequence or complication, not "and then" (rule #1). |
| Viewpoint-bound attention | Attention, vocabulary, judgment and knowledge come from the viewpoint; the narrator knows more only where the narration permits it. |
| Held narration | Tense, distance and the rules for viewpoint changes stay as agreed within the unit. |
| Grounded action | Action rests on concrete perceptions and decisions. |
| Purposeful dialogue | Each speaker wants, assumes or withholds something; affection and play count as purposes. |
| Distinct speakers | Speakers differ by experience and register, not by a swapped vocabulary or a catchphrase. |
| No redundant explanation | No line merely repeats what the scene already conveyed; direct telling stays where it is clearer or part of the voice. |
| Rhythm for the moment | Sentence and paragraph length serve this moment; no fixed ratio, no uniform scaffold. |
| Preserved devices | Deliberate fragments, repeated motifs, figurative language, humor, dialect and silence stay. |
| World-true detail | New detail belongs to this world and this viewpoint; nothing is added as fact merely to make prose vivid. |

There is no banned-word list and no universal style standard behind these names.

## Revision

For revision, fix causal structure and character motivation before line polish. Read for paragraph movement, spatial clarity, speaker identity and the emotional turn. Check that new detail belongs to this world and viewpoint; do not add scientific facts or accepted history merely to make prose vivid. Revise accepted prose only within the scope the author authorized.

## After the prose

Keep manuscript prose separate from editorial notes: nothing but prose in a prose file or under `## Manuscript`. After the prose, create or update a proposed canon delta and chapter summary with source locations, in the chapter card or, for a short piece, outside the manuscript heading. Record in `voice_revision` the voice sheet revision the unit was drafted under; acceptance confirms or updates it (see voice and tone). Route canon problems through `story-canon-review` and questions about whether the unit sounds like its sheet through `story-voice-review`. A draft invention does not automatically become accepted canon.

State the review scope and unresolved dependencies; never claim detector-proof or objectively human authorship. A chapter is complete when a canon review exists at a named revision and the author's acceptance is recorded; that is an author decision, and this skill does not declare it. `verification-before-completion` applies only to checks that have a command, such as link checks, template integrity or an export.

Status: experimental. This skill has not been piloted on a story and makes no claim about reader effect.
