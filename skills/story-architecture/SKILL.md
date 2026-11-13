---
name: story-architecture
description: "Use when the structure of a long story must be outlined: whole-story direction, sub-arcs, smaller causal movements, volumes as packaging units, chapter cards, subplots and setups with payoffs, read against the story's form and publication profile. Not for drafting chapters, or for outlining every chapter of a long story at once. Not for session replies, documentation or presentation videos."
---

# Story architecture

Mode check first, under [writing mode](../../shared/policies/writing-mode.md): find the nearest ancestor of the target file that holds 00-project/brief.md and 00-project/voice.md. Only kind story permits manuscript drafting; kind study permits study notes only; kind starter routes to story-bootstrap.

No run state: this skill has no recovery preamble and hands off to no backlog or run-tracking skill. A story or study vault keeps no backlog and no run directory; its state lives in 00-project/development.md and 00-project/decisions.md.

Outlines, arc notes, volume notes and chapter cards are working notes: plain notes that follow neither the voice sheet nor any instructional document structure.

Read the story brief, accepted cast/world constraints and [workflow](../../shared/story/workflow.md). Use the [arc](../../templates/story-vault/90-templates/arc.md), [volume](../../templates/story-vault/90-templates/volume.md), [chapter card](../../templates/story-vault/90-templates/chapter.md) and [foreshadow](../../templates/story-vault/90-templates/foreshadow.md) templates.

Read `form` and `publication_profile` from the brief's frontmatter before discussing any length. `form` decides whether the units are chapters with cards or short pieces. `publication_profile` decides which defaults exist at all; if the next planning step needs it and it is `unset`, ask the author instead of assuming one.

Use [guided development](../../shared/story/story-development.md) when major choices remain unresolved. Offer concrete alternatives with consequences; preserve agreed discovery writing rather than forcing a fixed ending. Use the story lenses in [quality review](../story-drafting/references/story-and-prose-quality.md) to distinguish a plausible outline from a compelling manuscript.

Establish the whole-story dramatic question, character trajectories, major irreversible changes and intended ending or discovery strategy. Trace how antagonistic action and protagonist choices cause later events. Keep unresolved options visible.

Apply [storytelling rule #1](../../shared/story/rules.md#1-storytelling-rule-therefore--but) before other structural refinements: connect major beats of the spine, arcs and nearest chapters through "therefore" consequences or "but" complications that change the next choice. For a connection that amounts only to "and then", repair the underlying events or motivation. Test the causal sequence separately from reveal order; quiet relationship or knowledge changes count.

## Arcs

Design sub-story arcs around local questions and material changes. Under the `web-serial` profile the maintainer's default is approximately 100 chapters per arc; it is a planning default, not a quality law, and it applies to that profile only. Where the author has set a chapter length, estimate total words from it and check the resulting scope. Record justified deviations and avoid padding to reach a number.

Break the current arc into smaller causal movements. Each movement changes conditions, knowledge, relationships or objectives and contributes to the arc. Track subplots separately; they may cross arc boundaries. Track promises from planting to development to payoff, including intended reader knowledge and latest useful payoff window.

## Volumes

A volume is a packaging unit beside the arc, not a level inside it. An arc may span several volumes, and a volume may end before its arc does. Plan arcs and movements first; then, where the profile is `light-novel` or `both`, decide where volume boundaries fall and what each volume opens and closes.

Apart from the web-serial arc default above, this method asserts no volume length, chapter length, chapters per volume or illustration count for any profile. Those are fields of the volume template, unset in the starter, and the author fills them: from researched source cards, or as the author's own recorded decision. Do not supply a figure from memory, and do not present an unset field as a default. If the author wants researched conventions, that is a task for `story-craft-research`.

Record in each volume note which arcs it covers and where an arc crosses its boundary, and record each chapter's volume in the manuscript index.

## Chapter cards

Detail only the nearest chapters. Each card names viewpoint, place, story time, starting state, desire, obstacle, meaningful change, relevant canon dependencies, setups/payoffs and ending effect. In a long-form vault the card lives in `05-plot/chapters/<chapter-id>.md` and links the prose file `06-manuscript/chapters/<chapter-id>.md`; the card holds no manuscript text. Quiet chapters can develop relationships or consequences; not every chapter requires a cliffhanger or disaster.

## Studying and reviewing structure

When studying an existing serial, preserve its explicit act boundaries separately from your analytical groupings. Do not impose the target chapter count on a reference work. At an arc boundary distinguish local closure, changed resources or relationships, and the question that carries forward; an ending can be emotionally complete while leaving a larger task open.

Review escalation for repetition, power inflation, stalled subplots, accidental resets and implausible travel/time. Let consequences carry across arcs. Preserve room for discoveries without moving established payoffs indefinitely.

Return an outline usable for the next drafting step, scope estimates where the author's figures allow them, and identified structural risks. A 100-row chapter list is not evidence of 100 chapters of compelling story. Do not publish or schedule output automatically. The outline remains proposed until the author accepts it; `verification-before-completion` applies only to checks that have a command, such as link checks or template integrity.

Status: experimental. This skill has not been piloted on a story and makes no claim about reader effect.
