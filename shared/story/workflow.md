# Long-fiction workflow

This is a repeatable path through a story, with return loops. It was written for long web serials and is being extended to other long forms; the story family is experimental and unpiloted. The category order reflects the maintainer's brief; later discoveries may revise earlier proposals. Ordinary drafting does not need repeated permission. Ask only for consequential missing author decisions or a change outside the established scope.

Apply [storytelling rule #1](rules.md#1-storytelling-rule-therefore--but) throughout: connect major beats with a meaningful "therefore" consequence or "but" complication and response. Check this connection when building the story spine, arc/chapter cards and prose, and repair missing links before line polishing. This is the first structural check, including for quiet developments; it does not prescribe literal connective words in the manuscript.

| Stage | Questions and output | Ready to proceed when |
| --- | --- | --- |
| 1. Idea and reader promise | Premise, intended audience, genre, emotional experience, central conflict, prose language, content boundaries, ending strategy, form and publication profile in the story brief | The next design choice has a clear purpose; undecided items are explicit |
| 2. World foundation | Geography/space, ecology, physical assumptions, magic/technology, institutions, everyday life | Important constraints produce usable choices and consequences |
| 3. World history | A chronological chain of events, migrations, discoveries, catastrophes and institutional change | Present tensions have causes; dates and causal ordering are plausible |
| 4. Species and peoples | Biology, habitats, needs, cultures, factions, internal variation and contact | Characters can belong to several groups without becoming stereotypes |
| 5. Pre-story interactions | Alliances, debts, betrayals, inherited conflicts, discoveries and secrets | Each necessary opening condition has a cause and someone who knows about it |
| 6. Distinctive features | A small set of defining mechanisms with consequences for work, status, family, conflict and sensory experience | Removing the feature would materially change this story |
| 7. Characters | Main/supporting cast, goals, fears, contradictions, voice card, relationships, competencies, constraints and development | Their competing choices can drive the planned conflict |
| 8. Whole-story arc | Central dramatic question, major irreversible changes, antagonist trajectory, promises and eventual payoff | The story has direction or a deliberate discovery strategy |
| 9. Sub-story arcs | Local dramatic question, stakes, reversal, climax, resolution and carryover; approximately 100 chapters each under the web-serial profile only | Each arc changes the long story and also provides a satisfying local movement |
| 10. Sequences and chapter cards | Break the nearest arc into manageable movements; chapter POV, time, place, desire, obstacle, turn, dependencies and ending effect | The next chapter has enough context to draft without guessing accepted facts |
| 11. Draft and revise | Scene prose, structural revision, voice/line pass, canon review, voice review, proposed canon changes | No blocking causal or canon problem remains within the reviewed scope |
| 12. Accept and maintain | Record the author's acceptance; update character state, history, open threads and chapter summary; refresh a source-linked retrieval derivative where a memory tool is used | Next session can resume from current files; accepted and published versions are distinguishable |

## Guided conversation

For execution from a minimal idea, follow [guided story development](story-development.md). It defines the next useful artifact, which missing decisions require a question, delegated choices, resumable state and manuscript completion. The stage table above remains the category map; the guided passes may revisit or combine stages.

## Form and storage

The brief's frontmatter field `form` decides where prose lives. The storage rule is what makes a path say whether a text is manuscript or a working note.

| Form | Prose | Everything else about the unit |
| --- | --- | --- |
| `long-form` | One prose-only file per chapter, `06-manuscript/chapters/<chapter-id>.md`, from the [chapter prose template](../../templates/story-vault/90-templates/chapter-prose.md) | The chapter card `05-plot/chapters/<chapter-id>.md` from the [chapter card template](../../templates/story-vault/90-templates/chapter.md): context packet, beats, summary, canon delta and review |
| `short-form` | Under the heading `## Manuscript` of one note per piece in `06-manuscript/pieces/`, from the [short piece template](../../templates/story-vault/90-templates/short-piece.md) | The same note, outside that heading; everything outside the heading is a working note |

Afterword, author note and blurb are manuscript too and live in `06-manuscript/paratext/`. A document that exists inside the story, such as a letter, report or manual, is manuscript wherever it appears in a prose file. The manuscript index `06-manuscript/index.md` lists, per chapter, the chapter ID, prose file, card file, arc, volume, POV and accepted revision; do not rely on filesystem sorting for order.

Working notes are plain notes. They follow neither the voice sheet nor any instructional document structure.

## Publication profile and volumes

The brief's frontmatter field `publication_profile` takes `unset`, `web-serial`, `light-novel` or `both`. It may stay `unset` while the story is being developed. Planning reads it before any length is discussed:

- `web-serial`: the maintainer's default of approximately 100 chapters per sub-story arc applies as a planning default, not a quality law.
- `light-novel` and `both`: this method asserts no volume length, chapter length or illustration count. Those are fields of the [volume template](../../templates/story-vault/90-templates/volume.md) that the author fills, from researched source cards or from the author's own decision.
- `unset`: plan arcs by their causal movements and leave length figures open.

A volume is a packaging unit beside the arc, not a level inside it. An arc may span several volumes, and a volume may close before its arc does. Plan the story in arcs and movements; then decide where volume boundaries fall and what each volume needs to feel complete. Record a volume's arc coverage in its volume note and the volume of each chapter in the manuscript index.

## Planning resolution

Keep the whole-story spine short enough to reread. Outline the current arc at sequence level, and only the next few chapters in scene detail. The exact look-ahead is a project choice. A 100-chapter arc can contain several smaller movements; neither their count nor their length is fixed by this method. Every movement needs a change in knowledge, relationships, objectives or conditions. Quiet chapters can supply that change without combat or a cliffhanger.

Subplots may cross arc boundaries. Each has its own owner, opening, development, payoff and dependencies; a subplot is not automatically a 100-chapter unit. Track romantic, political, mystery and character threads independently from the publishing arc and volume structure.

## The chapter context packet

Before drafting, assemble the story brief and voice sheet, current arc and chapter card, relevant accepted world/character notes, prior chapter ending, current physical and knowledge state, and due setups/payoffs. List exact files and revisions in the card. The packet also names the voice sheet revision in force and the voice cards of the characters who speak in the unit; see [voice and tone](voice-and-tone.md). Load original text for conflicts and pivotal details; summaries are navigation aids.

Keep the packet within the available context budget. Select by dependency and current scene, not by dumping the entire vault or trusting a generic retrieved summary. When a required fact is missing, consult the vault, mark it unknown or propose it openly. Do not borrow canon from another story.

The packet is written so that drafting can start from it alone. Where the host allows, the draft is written from the packet in a fresh sub-agent or session, so that rules loaded for other kinds of writing earlier in the conversation are not in context.

After drafting, record a concise chapter summary and a proposed delta: new facts, changed locations, injuries, possessions, knowledge, relationship shifts, planted/paid promises and elapsed time. Resolve conflicts before accepting the delta. Draft revisions can invalidate both summaries and retrieval derivatives; see the [retrieval contract](retrieval.md).

## Narrated video after acceptance

An accepted chapter, chapter range or short piece can optionally be delivered as a narrated video, an audiobook with pictures. This is a delivery step after stage 12, not a writing stage, and it is experimental.

- **Verbatim by default.** The narration is the accepted manuscript at a named revision, only segmented into scenes and lines at sentence boundaries. No word is added, dropped or changed.
- **Listening edition by author decision.** A derived edition with changes for the ear is stored prose-only in `06-manuscript/editions/listening/<chapter-id>.md`, from the [listening edition template](../../templates/story-vault/90-templates/listening-edition.md). Every difference from the manuscript is a recorded author decision. The edition is manuscript and follows the voice sheet; it is not canon and changes none.
- **The written manuscript is not changed.** Neither edition edits a prose file, a chapter card or a canon delta. A change the story itself needs goes through drafting, canon review and a new accepted revision first.

The script is written by [story video scripting](../../skills/story-video-scripting/SKILL.md) into a video project outside `06-manuscript/`, at a path the author names. Voicing and rendering belong to the form skill `presentation-video-production`, which never restyles the text. Delivery as an e-book stays future work.

## Expansion and retcons

New history can fill an uncommitted gap. If it changes an accepted fact, enumerate the affected scenes, character knowledge and later payoffs, propose the smallest coherent revision, and record the decision. Published text needs an explicit author decision about errata, revised edition or an intentional in-world explanation. An unreliable narrator is an explanation only when supported by the work, not an automatic repair.

## Pilot before scaling

Start with one chosen premise, a small world slice, three differentiated characters, one arc skeleton and three consecutive chapters. Review whether voice survives, world features cause action, state changes are preserved and an intentional contradiction is found. Extend to an arc only after this works. A three-chapter pilot cannot establish 100-chapter reliability; retain periodic arc-level reviews and eventual long-run evaluation.
