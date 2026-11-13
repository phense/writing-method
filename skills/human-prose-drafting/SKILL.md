---
name: human-prose-drafting
description: "Use whenever prose for people is written or revised and no other writing skill covers it: an email, announcement, post, notice, commit or pull-request description; and as a supporting skill within documentation-authoring for medium and large texts. Applies writing rule #1, natural prose without machine patterns, from the first sentence, with a brief check before delivery. Not a separate rewrite phase or a reason to change facts, code, quotations or required document structure. Not for story manuscripts or in-world text."
---

# Human Prose Drafting

Not for story manuscripts or in-world text: when the target is manuscript, stop and use the story family under [writing mode](../../shared/policies/writing-mode.md).

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Write for the defined reader and subject from the first sentence. Apply
[writing rule #1](../../shared/policies/natural-prose.md) while choosing words and organizing each paragraph. The writing
lifecycle includes a short check of each chunk, with no separate humanizing phase.

Adapted from blader/humanizer (MIT); patterns trace to Wikipedia's "Signs of AI
writing" maintained by WikiProject AI Cleanup. See the third-party notices.
The pattern catalogue itself lives in writing rule #1, which applies to every
text; this skill applies it to documentation and to short texts that no
other skill covers.

## Trigger

Use for a short standalone text a person will read that no other writing
skill covers: an email, an announcement, a post, a notice, a commit or
pull-request description. For such a text read the rule, write, and run its
delivery check once; nothing is recorded. A document, also a release note,
belongs to `documentation-authoring`, and this skill supports it there. An
ordinary reply belongs to the didactic skills.

Use inside `documentation-authoring` for every chunk or standalone document at
the medium or large scale, and inside `documentation-review` as one check.
The didactic skills decide what to say and in what order; this skill decides
how the sentences may not be built.

## Do not use for

- Code blocks, inline code, commands, paths, YAML frontmatter, data tables,
  link targets and quoted material: leave them unchanged.
- Changing claims. A name, number, date, quote, citation or fact comes from
  verified source material, never from this skill; when a sentence needs a
  missing detail, write a simpler sentence or record the gap.
- Small-scale edits inside existing text that keep the surrounding voice.
- Story manuscripts or in-world text; the story family owns them, under
  [writing mode](../../shared/policies/writing-mode.md).

## Two rules while drafting

1. Give each sentence a purpose for the reader. Omit sentences that only
   signal importance, echo a heading or repeat a conclusion. Keep useful
   teaching recaps and required warnings.
2. Choose for the defined reader. Vary sentence length as speech does; name
   the actor; use the number of items the meaning has; pick the plain word.

## The patterns

Read [writing rule #1](../../shared/policies/natural-prose.md) before the first
sentence. It holds the patterns in five groups, the reasons readers recognize
them, the exceptions and the scope. Use it as contextual guidance, not as a
string blacklist: the staged forms of its group A are a defect on one
occurrence, and a pattern it marks as weak needs context before you change
anything. User instructions, required templates, glossary terms, source
fidelity and project style take precedence over its style preferences.

Documentation adds these to the rule:

- **Name the actor.** "You do not need a configuration file", not "No
  configuration file needed". Procedures already require this.
- **Bold only for interface labels** as `writing-procedures` requires, and
  for the first words of a list item when the reader scans by them.
- **Sentence-case headings.** Preserve required headings, anchors and
  template title structure.
- **No heading repeated in the first sentence** below it.
- **Hyphenate only where grammar needs it**: "a high-quality report", "the
  report is high quality".
- **Straight quotation marks** unless the project's style guide says
  otherwise.
- **No writing about the previous version** except in release notes,
  changelogs and migration guides. Describe current behavior.

## Voice for documentation

Concept, task, reference and troubleshooting text stays neutral and plain,
addresses the reader as "you", and keeps the project's glossary terms. The
plan or project contract decides the language of the text; the patterns of the rule have
equivalents in every language and are treated the same. Do not add opinions,
humor or asides to documentation; those belong to personal writing.

## Chunk check

Before marking a chunk drafted, read it once for the seven patterns of the
rule's delivery check: a contrast with nothing, a one-line closer, a list of
three, a participle phrase at a sentence end, a stock word, a bold label, a
line addressed to the person who asked. Assess each in context, including the exceptions below.
Correct unnecessary rhetoric within the chunk; retain useful structure. Confirm the fix dropped no fact, step, warning or
claim. This check is part of authoring the chunk and adds no separate
humanizing stage or extra output artifact.

## When not to act

Leave a watched phrase alone inside a quotation, a title, a product or
interface name, or a passage that discusses the phrase rather than uses it.
Keep scope statements, legal and safety notices, and real corrections. A
specific unusual detail, a stated limit or an honest "we do not know" is not a
tell; it is what a person would write.

## Completion

A chunk is complete when the contextual check finds no unresolved prose
problem and preserves facts, steps, uncertainty, warnings, glossary terms and
required structure. Record the check in the existing self-review or review
report; update `last_reviewed` only when the full chunk review is complete.
A literal word match alone is not a failure.
