# Design: Story writing as a separate family in Writing Method

## Stable work ID

- Feature ID: `WM-003` (next free ID after WM-001 and WM-002; no GitHub Issue opened yet)
- Artifact path: `docs/specs/WM-003-story-family/design.md`
- Status: Accepted by the owner on 2026-11-13; implemented on branch `wm-003-story-family`.
- Source request: Integrate the long-form writing, tone and related skills of the
  owner's private research workspace (called Worldbuilding below) into Writing
  Method. The project targets long stories and light novels. Story writing must stay separate
  from ordinary writing: session replies, documentation and presentations.
- Inputs: the Worldbuilding candidate 0.1.16 including its uncommitted changes as
  read on 2026-11-13; Writing Method 0.3.0 at `29752ab`; three independent
  read-only proposals; one adversarial review of draft 1 by three reviewers.
  Draft 2 incorporates that review and has not been reviewed again.

## Owner decisions of 2026-11-13

| Question | Decision |
|---|---|
| Structure | Family inside Writing Method. This supersedes the earlier decision for an independent plugin (`WB-001`; IDs starting with `WB-` name items in the private workspace's backlog). |
| Prefix | `story-`. Shared files live in `shared/story/`, the vault starter in `templates/story-vault/`. |
| Chapter storage | Prose in its own file for long-form work only. A short-form piece is one note in `06-manuscript/pieces/` with its prose under a `## Manuscript` heading. |
| Licence | The story skills, rules, study-derived references and vault starter are published under Writing Method's MIT licence. |
| Publication profile | No productive story work has started. The profile stays unset in the starter; light-novel conventions are researched before any figure is asserted. |
| Worldbuilding | Uncommitted changes committed and tagged `pre-wm-integration`; the port copies from that tagged commit. |

Where the text below still presents these points as open, the table decides.

## Terms

| Term | Meaning |
|---|---|
| Story family | The skills, rules and templates for fiction. Every skill name starts with `story-`. |
| Reader family | Everything Writing Method does today: didactic replies, documentation, PDF, presentation videos. |
| Story vault | One story's own directory and Git repository: brief, voice sheet, canon, plans, manuscript. Marked `kind: story`. |
| Study vault | An analysis vault for an existing, third-party work. Marked `kind: study`. |
| Manuscript | Story prose and in-world text (a letter, report or manual that exists inside the story), plus afterword and blurb. |
| Working note | Any other vault file: brief, world entry, character note, arc, chapter card, canon review, study note. |
| Voice sheet | `00-project/voice.md` of a story vault. It overrides every method default for how that story's manuscript sounds. |
| Writing mode | Which rule set governs one piece of output: `manuscript`, `working-note` or `reader-oriented`. |

## Findings that shape the design

1. **Two plugins share one name.** The owner's private research workspace holds a
   local, uninstalled plugin candidate also called `writing-method`. Loaded beside the published
   plugin, two skill sets share one namespace. An earlier owner decision chose an
   independent writing plugin (Worldbuilding `WB-001`, recorded in the earlier
   research note); the current request supersedes it.
2. **The didactic rules reach ordinary replies through skill descriptions.**
   `explaining-concepts`, `writing-procedures` and `empathic-troubleshooting`
   say "in documentation or an ordinary reply". They are installed in every story
   session whatever the packaging, so a separate fiction plugin would not shield
   manuscript prose from them.
3. **No policy file is loaded before a skill is chosen on Claude or Codex.** Only
   descriptions are always in context. On OpenCode the loader injects the platform
   adapter, which points to `lifecycle-selection.md`. The validator checks
   description syntax and the skill inventory; it does not check description
   content, families or the handoff graph. Those live in writing-owned tests.
4. **Documentation voice is wrong for fiction.** `human-prose-drafting` removes
   fragments, repetition, humour and asides. `fiction-drafting` (ported as
   `story-drafting`) preserves them.
5. **"Continuity" is taken.** Method Core uses it for session recovery. The
   story skill `continuity-review` means story canon.
6. **OpenCode has a flat skill namespace.** Bare names such as `worldbuilding`
   can collide.
7. **One chapter note mixes three kinds of text.** The vault template's chapter
   note holds card, manuscript and review under separate headings. A file path
   alone cannot say which rules apply.
8. **Study vaults are built from the story starter.** They would be mistaken for
   story vaults by any marker that only looks for brief and voice sheet.
9. **No story exists yet, and nothing in Worldbuilding covers light novels.** The
   seven skills are drafts without a pilot (`WB-006` waits for a premise). A search
   for light novel, volume or illustration finds nothing; the method is built for
   web serials.
10. **Parts of the method are private or machine-specific.** The research corpus
    and study vaults are private working material. Two skill references are
    derived from a studied third-party work and link to private notes. The
    retrieval contract describes a private memory service on one machine.
    Worldbuilding has no licence decision and is not published.

## Decision

Fiction becomes a **separate family inside the Writing Method plugin**, kept apart
by the layers below. Worldbuilding stops being a plugin and remains the owner's
private research and study workspace.

| Alternative | Why not |
|---|---|
| Third plugin that vendors Method Core | Does not stop the didactic rules (finding 2). Costs a third lock, repository and release line and a third copy of the eight shared skills in OpenCode. Core's tooling is identity-driven and would allow it; only its documentation names two consumers. Advantage: a hard off-switch. Kept as the fallback. |
| Keep Worldbuilding as the plugin, renamed | The above, plus an unpublished repository, no licence, a validator needing PyYAML, private study vaults beside the plugin root. |
| A fiction mode inside existing skills | The rule sets contradict each other (finding 4). |

**Fallback criterion.** On the named cross-family routing cases, the harness
reports `prohibited_skill_invoked` or `unexpected_selection`. If any such case
still fails on Claude or Codex in more than one of five runs after two rounds of
fixes, extract the family into its own plugin. The layout keeps that mechanical.

## Separation model

### Mode belongs to the output, not to the session

| Order | Condition | Mode | Governed by |
|---|---|---|---|
| 1 | The file is a reader-facing vault file: `README`, `START.md`, `AGENTS.md`, `CLAUDE.md` | `reader-oriented` | Today's rules |
| 2 | The text is story prose, in-world text, afterword or blurb: it goes into a prose file of a `kind: story` vault, or the author explicitly asks for story prose | `manuscript` | The voice sheet, then `shared/story/rules.md`. Nothing from the reader family. |
| 3 | The text is another file of a story or study vault, or a research note | `working-note` | The story skills. Plain notes: neither the voice sheet nor didactic structure. |
| 4 | Everything else, including every reply to the author | `reader-oriented` | Today's rules, unchanged |

The subject never sets the mode. Talking about a story is still a reply.

### Storage decision that makes the mode decidable

Manuscript prose gets its own file: `06-manuscript/chapters/<chapter-id>.md` holds prose
only. The chapter card, summary, canon delta and review move to a card note in
`05-plot/chapters/`. Afterword and blurb live in `06-manuscript/paratext/`. A path then
decides between manuscript and working note, and a later export reads prose files
without extraction. This changes the vault template. The owner decided it for
long-form work; the alternative, manuscript as the text under a `## Manuscript`
heading, is kept for short-form pieces only: one note per piece in
`06-manuscript/pieces/`, prose under `## Manuscript`.

### Where the rule is actually read

A policy file nobody loads protects nothing. The operative sentences therefore sit
in three places, and `shared/policies/writing-mode.md` is the authority they are
tested against:

| Carrier | Content |
|---|---|
| Opening lines of every `story-*` skill body | First step: find the nearest ancestor of the target file that is a `kind: story` (or `kind: study`) vault. For manuscript text the voice sheet overrides `explaining-concepts`, `writing-procedures`, `empathic-troubleshooting` and `human-prose-drafting`, even when those are loaded. |
| Opening lines of those four reader skill bodies, plus their descriptions | Not for story manuscripts or in-world text; when the target is manuscript, stop and use the story family. |
| Vault `AGENTS.md` (authority) and `CLAUDE.md` (adapter) | The mode rule in three sentences. `story-bootstrap` writes or refreshes both when it creates or resumes a vault. |

`writing-mode.md` is a neutral hub: both families link it directly, and it links
into neither.

### Layers and what each one proves

| Layer | What it does | Test proves |
|---|---|---|
| 1. Names | `story-` prefix; no name equals a Core, Writing or Engineering skill name or contains `continuity` | The names are as stated |
| 2. Descriptions and opening lines | Reciprocal exclusions and the precedence clause | The sentences are present and match the policy block. Whether a model follows them is statistical. |
| 3. Link firewall | Fiction skills link only into `shared/story/`, `templates/story-vault/`, other story skills, `writing-mode.md`, `proportionality.md` and `verification-before-completion`. Reader skills never link into the fiction directories. Backticked skill names are checked against the family map too. | A skill cannot pull the other family's rule files in through links |
| 4. No lifecycle graph | No `story-` name appears in `lifecycle-handoffs.md`. The story family is orchestrated only by `shared/story/story-development.md`, whose passes overlap and return; it is not a linear lifecycle. | The graph contains no fiction node |
| 5. Vault kind | A story vault is the nearest ancestor holding `00-project/brief.md` and `voice.md` with `kind: story` and a set `story_id` in the frontmatter. `kind: starter` and `kind: study` never authorise drafting. Drafting additionally needs viewpoint, tense and distance filled in the voice sheet; otherwise the work routes to the voice trial. | The template and the skills state and apply the rule |

Four layers have deterministic presence tests. That is weaker than saying the
separation is deterministic.

### Limits stated plainly

- **Both rule sets can sit in one context.** The author asks why the magic cost
  works, `explaining-concepts` loads, and the next request is "draft chapter 12".
  No link rule prevents that. The precedence clause addresses it; where the host
  allows, `story-drafting` drafts from the chapter context packet in a fresh
  sub-agent or session.
- **The harness reads skill selection, not text.** It runs one turn and stops
  before writing. Whether a chapter opens with an analogy, or a reply drifts into
  a story's voice, is unmeasured. An output-level check needs a change to Method
  Core's harness. Until it exists and passes, the family keeps the experimental
  label.
- **Core skills cannot be edited here.** `receiving-code-review` claims
  "unverified review feedback", which matches beta-reader comments. If routing
  runs show a Core description capturing story work, the fix belongs in Method
  Core.

### Mixed situations

| Situation | Disposition |
|---|---|
| A reply that discusses plot, characters or craft | `reader-oriented` |
| A reply that contains a draft passage | The passage goes into a prose file or a fenced block and is `manuscript`; the surrounding reply never restyles it |
| A draft passage requested outside any vault | `manuscript` with the method defaults; the reply states that no voice sheet applies |
| Documentation about the fiction method; a vault README | `documentation-authoring` |
| An in-world document, including an in-world how-to manual | `manuscript` under `story-drafting` |
| A story excerpt quoted in documentation | Quoted material, unchanged |
| An explanatory narrated video about a story or its world | `tutorial-video-scripting` |
| Dramatised fiction: audiobook, narrated story video | Outside the method for now |
| Beta-reader or author feedback on a chapter | `story-canon-review` or `story-voice-review`; not `receiving-code-review` |
| Notes and craft exercises in a study vault | `working-note` under `story-craft-research`; never drafting against the studied work's canon |

### Completion in the story family

A chapter is complete when a canon review exists at the named revision and the
author's acceptance is recorded. That is an author decision, not a command result,
so no story skill hands off to a pass claim. `verification-before-completion`
applies only to checks that have a command: links, template integrity, an export.
Story vaults get no backlog; state lives in `development.md` and `decisions.md`.

## What WM-003 delivers

### Part A: separation and port

| New name | Origin | Change |
|---|---|---|
| `story-bootstrap` | `story-bootstrap` | Sets `kind` and `story_id`; asks the publication profile; writes the vault instruction files |
| `story-worldbuilding` | `worldbuilding` | Rename |
| `story-characters` | `character-design` | Rename; voice fields move to the character voice card |
| `story-architecture` | `serial-architecture` | Rename; reads the publication profile; rule #1 stays the first structural check |
| `story-drafting` | `fiction-drafting` | Rename; names in-world documents; carries the precedence clause |
| `story-canon-review` | `continuity-review` | Rename (finding 5) |
| `story-craft-research` | `craft-research` | Rename; the research workspace path becomes a setting of the workspace, not a link |

All get quoted descriptions (the validator rejects the current unquoted ones).

Port table for the files that are not skills:

| File | Disposition |
|---|---|
| `shared/rules.md`, `workflow.md`, `story-development.md` | Ship in `shared/story/`; links re-pointed; rule #1 attributed as "maintainer requirement" (decision 8) |
| `shared/rag.md` | Split. The plugin ships a provider-neutral, optional retrieval contract as `shared/story/retrieval.md`: the vault is the authority, retrieval is advisory, scope is the vault's Git root, skip when no memory tool exists. The provider-specific details of a private memory service stay in the private workspace. |
| `references/science-and-institutions.md`, `serial-scene-review.md`, `sequential-fiction-study.md` | Ship; links into `research/` removed; the study path becomes a parameter |
| `references/story-and-prose-quality.md`, `action-sequences.md` | Ship with a one-line provenance statement that does not name the studied works or their authors (owner decision of 2026-11-13); links to private transfer notes replaced by an entry in the source index |
| `research/SOURCES.md` and source cards | Stay private. The plugin ships `shared/story/sources.md`, a compact index of the cited IDs, and a blank source-card template |
| `templates/story-vault/` | Ships as `templates/story-vault/` with the storage change, the `kind` marker, `AGENTS.md`, and conditional retrieval lines |

### Part B: voice and tone

Most of this already exists and is extended, not duplicated: guided-development
pass E is the voice trial with two treatments of one beat, and `story-bootstrap`
sets the basic voice fields.

- **Voice sheet template.** New sections: narration contract per viewpoint; tone
  palette (baseline, permitted excursions and their return, tones the reader
  promise excludes); language conventions for the prose language; two to four
  anchor passages; deliberate exceptions;
  paratext register; change log. A sheet change is a recorded author decision.
  Chapters keep the sheet revision they were accepted under.
- **Anchor passages.** The passages the author chose in the voice trial are the
  first anchors. They are voice references, not canon or manuscript, and are
  referenced by voice trial record and revision. Accepted chapter passages,
  referenced by chapter ID and revision, replace or supplement them later.
- **Character voice cards.** Register, habitual attention, expertise vocabulary
  and limits per speaking character, with a cap on verbal tics.
- **One new skill, `story-voice-review`.** It judges a chapter or range against
  the sheet and never edits accepted prose. A finding cites a passage and either
  a sheet or card clause, or a named default from `story-drafting`, labelled
  "method default, not sheet". Findings are classed as unintended deviation,
  deliberate exception, sheet gap or candidate for changing the sheet. Without
  two anchor passages and a filled tone palette the skill declines and routes to
  the voice trial, which records the chosen trial passages as anchors and so
  satisfies the rule before any chapter is accepted.

Tone for documents stays in `human-prose-drafting`. There is no shared tone skill.

### Part C: light-novel foundations

- **Research first.** A `story-craft-research` task produces source cards on
  light-novel conventions: volume length, chapter length, illustration count and
  placement, prologue and afterword, serialisation cadence. Nothing is asserted
  from memory.
- **Publication profile.** A field in the brief: web serial, light-novel volumes
  or both. `story-architecture` reads it. Volume becomes a planning unit beside
  the arc; an arc may span volumes. About 100 chapters per sub-arc stays the
  default for the web-serial profile only.
- **Volume template** and a light-novel reference, written from the source cards.

### Deferred, each with its gate

| Candidate | Gate |
|---|---|
| `story-revision` (ordered passes over a range) | The three-chapter pilot shows the pass order holds |
| `story-manuscript-export` (EPUB or PDF per volume) | A decision on a neutral typesetting directory shared with `documentation-pdf`, or duplicated templates |
| Illustration briefs | Light-novel source cards exist |

## Changes to the existing reader family

- `lifecycle-selection.md` and `reader-oriented-output.md`: link the mode policy
  and exclude manuscript text. `writing-depth.md`: one sentence; the scale table
  does not apply to manuscripts.
- `explaining-concepts`, `writing-procedures`, `empathic-troubleshooting`,
  `human-prose-drafting`: exclusion in the description and the opening lines.
- `documentation-authoring`, `documentation-review`, `terminology-guard`,
  `tutorial-video-scripting`: exclusion in the description.
- `third-party/sources.lock.json`: new hash for the adapted
  `human-prose-drafting`; the original-implementation path list gains the
  fiction paths; a decision whether craft sources become lock entries or prose
  attribution. `THIRD_PARTY_NOTICES.md` follows.
- `method.json`, both plugin manifests (name, version, description, keywords must
  stay identical), the Codex interface fields, both marketplace files, README,
  usage guide.
- The experimental label lives in README, the usage guide, the story skill
  bodies and the policy block. `FEATURES.md` cannot carry it: its status model
  has no such value and the file is still a placeholder; that is a separate fix.

The didactic default for replies stays, including inside a story vault.

## Verification

| Check | Kind |
|---|---|
| `tests/test_writing_mode.py`: family map, prefix, opening sentences against the policy block, link firewall incl. backticked names, hub has no outbound family links, no fiction node in the graph, vault kind rule, links resolve and no host syntax in `shared/story/` | Deterministic |
| Vault starter: wiki-links resolve, frontmatter valid, both instruction files present (ported from Worldbuilding's validator) | Deterministic |
| Package: no link or path into `research/` or `external/`, no study-vault path, no absolute user path | Deterministic |
| Existing nine routing cases unchanged | Regression |
| Routing cases, fiction-positive, each with a named primary and the reader skills plus `requesting-code-review`, `receiving-code-review` and `project-backlog` prohibited: draft a chapter; start a story in a starter vault (`story-bootstrap`); canon review; voice review; in-world how-to manual; beta-reader feedback | Paid host evals, Claude and Codex, five runs each |
| Routing cases, negative, each with all `story-*` prohibited: vault README; release note in a documentation repository; tutorial video about a story's world; documentation of the fiction method; drafting request inside a study vault; session rooted in the parent of a vault | Same |
| Not measurable today, blocked on a Method Core harness change: a reply inside a vault; two-turn leakage in both directions; voice review against two opposite sheets | Recorded as open |
| OpenCode: new names discovered without collision | Manual, discovery only |
| Worldbuilding `WB-008`: all skills exercised with realistic prompts | Gate before release |

Routing cases are added to `evals/shared/triggers/`, both `expected.json` files
and `tests/fixtures/trigger-cases/matrix.json`.

## Migration

1. Owner: commit or park the uncommitted Worldbuilding changes, back the
   repository up, tag the commit. The port copies from that commit.
2. Owner decisions 1 to 5 below. Then open the `WM-003` issue and write spec,
   plan and tasks beside this design.
3. Inventory every file that names an old skill or the launcher: the
   instruction files, README, feature list and compatibility note of the private
   workspace, the vault template's `CLAUDE.md`, and the instruction file inside
   each study repository.
4. Write the failing tests and the mode policy.
5. Add the reader-side exclusions and update the provenance lock.
6. Port per the tables above; change the vault template.
7. Part B, then the Part C research task, then the profile, volume template and
   reference.
8. Add the routing cases; run the local gate, then the host evals; run `WB-008`.
9. **Rollback point.** No plugin behaviour has changed on `main`; Worldbuilding
   has only the step-1 commit and tag. Rolling back means deleting the branch and
   closing the issue as not planned.
10. Merge and release Writing Method 0.4.0, story family labelled experimental.
11. Retire the plugin identity in Worldbuilding: remove manifests and the method
    copies (`skills/`, `shared/`, `templates/story-vault/`), reduce `validate.py`
    to the research checks, update the files from step 3. Keep the launcher as a
    thin wrapper until one study has been resumed against the installed plugin.
    Study repositories are changed and reverted one by one.
12. Re-save the method's memory derivatives under their existing IDs with the new
    source paths and hashes, or mark them superseded (open decision 6).

## Risks

| Risk | Mitigation |
|---|---|
| A host picks the wrong family | Opening-line precedence, firewall, vault kind; bidirectional cases; fallback criterion |
| Both rule sets in one context across turns | Precedence clause; fresh context for drafting where possible; stated limit |
| Leakage in produced text is unmeasured | Experimental label until the Core check exists |
| Voice and light-novel rules designed without a story | Structurally validated only; revised after the pilot; light-novel figures are overridable defaults backed by source cards |
| The voice review becomes a generic AI-tell filter | No style list; clause or named default required; refusal on thin sheets |
| Private or study-derived material enters the public package | Port table; package test; licence decision covers study-derived guidance |
| Work in the private workspace is lost | Step 1 is a precondition; copy until step 11 |
| The template change breaks existing study vaults | Study vaults keep their layout; only new story vaults use the split |
| 29 descriptions reduce trigger precision for documentation | Existing cases as regression gate |

## Open decisions for the owner

Points 1 to 5 are settled by the Owner decisions table above and point 8 by the
implementation. Points 6, 7, 9 and 10 remain open.

1. **Confirm the structure.** The request to integrate supersedes the earlier
   decision for an independent plugin (`WB-001`). Recommended: family inside
   Writing Method, with the fallback criterion. **Decided:** family inside
   Writing Method.
2. **Prefix.** `fiction-` (recommended in the draft: `fiction-drafting` keeps its
   name, and it fits the research skill) or `story-`. **Decided:** `story-`.
3. **Chapter storage.** Prose in its own file (recommended) or a heading inside
   the chapter note. **Decided:** own file for long-form work; a short-form piece
   in `06-manuscript/pieces/` keeps its prose under `## Manuscript`.
4. **Licence.** May the story skills, rules, study-derived references and vault
   starter be published under Writing Method's MIT licence? **Decided:** yes.
5. **Publication profile of the first story.** Web serial, light-novel volumes or
   both. It sets how much of Part C is needed now. **Decided:** the profile stays
   unset in the starter; light-novel conventions are researched before any
   figure is asserted.
6. **Memory derivatives.** Which repository is their source after the port.
   Open.
7. **Output-level leakage check.** Fund the harness change in Method Core. Open.
8. **Rule #1 attribution in a public plugin.** Keep the dated personal
   attribution, or "maintainer requirement". **Implemented:** "maintainer
   requirement".
9. **Timing.** Release before a pilot, labelled experimental (assumed), or wait
   for a first premise. Open.
10. **Replies inside a story vault.** Keep the full didactic default (assumed) or
    a lighter editorial register for story discussion. Open.
