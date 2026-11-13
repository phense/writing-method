# Voice and tone of a story

This file belongs to the experimental story family. It describes how one story's voice is decided, recorded, changed and checked. It sets no style of its own: the author's voice sheet decides how a manuscript sounds, and nothing here ranks one voice above another.

## Scope

In scope: manuscript text of a vault of kind story, which is story prose, in-world documents and paratext such as an afterword or a blurb.

Out of scope: tone for documents. Documentation, session replies, vault instruction files and narrated explanatory videos are not manuscript; the [writing mode](../policies/writing-mode.md) policy names what governs them. Working notes in a vault are plain notes, and the voice sheet does not style them.

The narration of a story video is manuscript, not an explanatory video: it is the accepted manuscript or an accepted listening edition, and the sheet governs it. A listening edition follows the sheet revision its chapter was accepted under. Voicing and rendering do not restyle it.

## Two records

| Record | Where | What it decides |
| --- | --- | --- |
| Voice sheet | [`00-project/voice.md`](../../templates/story-vault/00-project/voice.md) of the vault | How the narration sounds: the narration contract per viewpoint, tone palette, language conventions, anchor passages, deliberate exceptions, paratext register |
| Character voice card | The voice card section of each [character note](../../templates/story-vault/90-templates/character.md) | How one character sounds in dialogue and, as a viewpoint, what the narration attends to |

For manuscript text the voice sheet comes first, then the [story rules](rules.md) and the defaults named in [story drafting](../../skills/story-drafting/SKILL.md). A default applies only where the sheet is silent, and a review that relies on one labels it "method default, not sheet".

## Lifecycle of the voice sheet

1. **V0, no voice yet.** The starter's sheet carries `voice_revision: V0` and `viewpoint`, `tense` and `distance` set to `unset`. Drafting is not permitted in this state.
2. **Trial.** Pass E of [guided development](story-development.md) writes a short scene that does a real job in the story, if needed in two treatments of the same beat. The author says which passage matches the intended experience and why. Trial prose stays proposed as manuscript and as canon: choosing a passage accepts it as a voice reference only.
3. **V1.** The author's choice is recorded as the accepted sheet: the three frontmatter fields, the narration contract, the tone palette, the language conventions and the first deliberate exceptions. Acceptance sets `voice_revision: V1` in the frontmatter and adds the first change-log row with its decision ID; a sheet with all three fields set never stays at `V0`. The trial passages the author chose are recorded as the first anchor passages, at least two of them, each referenced by the voice trial record and its revision. Once accepted chapters exist, their passages replace or supplement the trial anchors.
4. **Revisions.** Every later change is an author decision, recorded in the sheet's change log and in the vault's decisions note, and raises the revision. No agent changes the sheet on its own, and no sheet is changed to make a review pass.

Chapters keep the revision they were accepted under. A chapter card or short piece records that revision in its `voice_revision` field: until acceptance the field holds the sheet revision the unit was drafted under, and at acceptance it is confirmed or set to the sheet revision in force when the author accepted the unit. A later review judges the chapter against it. A new revision reopens accepted chapters only when the author decides so and names the scope.

## The parts of the sheet

- **Narration contract per viewpoint.** Viewpoint, tense, distance and the permitted shifts, one entry per viewpoint the story uses. The main contract is also readable in the frontmatter.
- **Tone palette.** The baseline tone; the permitted excursions, each with what triggers it and how the prose returns; and the tones the reader promise excludes. An excursion without a return is a change of baseline and needs a decision.
- **Language conventions.** The prose language and variant, dialogue and thought punctuation, names and invented terms, numbers and emphasis.
- **Anchor passages.** Two to four accepted passages, referenced by chapter ID or voice trial record, and revision. A trial passage is accepted as a voice reference, not as canon or manuscript.
- **Deliberate exceptions.** Departures the author wants, each with where it applies and its intended effect.
- **Paratext register.** How afterword, author note and blurb sound; they need not match the narration.
- **Change log.** Revision, date, change, decision and the chapter from which it applies.

## Anchor passages are references, not a phrase bank

An anchor shows the voice doing its work in context, so that a later passage can be compared with it. It is cited by location and is not copied into the sheet. Do not harvest its wording, images or sentence shapes for reuse: a voice that repeats its anchors has become a set of signature phrases. When an anchored chapter is revised, the author confirms the anchor at the new revision or replaces it.

## Character voice cards

A card is filled for every character who speaks or carries a viewpoint, scaled to the role. The [story characters](../../skills/story-characters/SKILL.md) skill maintains it.

| Field | Content |
| --- | --- |
| Register | Formality, sentence length, directness, and how these shift with the listener |
| Habitual attention | What the character notices first and what they overlook |
| Expertise vocabulary | The fields they can name precisely, and where that knowledge comes from |
| Limits | What they would not say, cannot articulate or get wrong |
| Tic cap | An author-set limit on how often a verbal tic may appear. The method supplies no number; the field stays unset until the author sets it. |

Dialogue examples on a card reference accepted passages. A card distinguishes characters by what they notice, choose and withhold, not by a catchphrase.

## Checking the voice

The [story voice review](../../skills/story-voice-review/SKILL.md) skill judges a chapter or a range against the sheet and the cards and reports findings in four classes: unintended deviation, deliberate exception, sheet gap and candidate sheet change. It needs at least two anchor passages and a filled tone palette; without them it routes back to the trial, which can supply both. An anchor may be a trial passage. It uses no banned-word list and no universal style standard, and it does not edit accepted prose.

A voice review is one input to the author's acceptance of a chapter. It is not a measurement of quality, and passing it proves nothing about how readers will respond.
