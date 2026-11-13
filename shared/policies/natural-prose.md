# Writing rule #1: natural prose

**No text this method produces may read as machine-written.** The rule comes
before every other writing rule and covers every text a person reads: replies,
documentation, messages, commit and pull-request descriptions, review comments,
video narration and story manuscript. Its position as rule #1 is a maintainer
requirement of 2026-11-13.

A reader who recognizes the patterns below stops trusting the text and often
stops reading it. The facts in it no longer count, because the reader assumes
that nobody checked them.

This file is neutral: every skill family may link it, and it links into none.

## Contents

- Why readers recognize machine text
- The patterns
- What to write instead
- Check before delivery
- What is not a pattern
- Scope by writing mode
- Limits
- Sources

## Why readers recognize machine text

| Cause | Effect in the text |
|---|---|
| A language model continues with the most probable words. The result moves toward the average of everything it has read. | A specific fact gives way to a general statement that would fit any subject. Wikipedia calls this regression to the mean. |
| Training rewards answers that most people find agreeable. | Praise, inflated importance, caution in every sentence, and an opening that includes every possible reader. |
| A sentence form that promises insight is cheaper than an insight. | Contrasts with a position nobody held, lists of three, ranges "from X to Y", and a participle phrase that adds a meaning the fact does not have. |
| The same forms appear in every text and at an even rhythm. | A reader who has met them a few times recognizes them at once. Outside group A one form alone proves little, and several in one paragraph prove much. |
| The text was written as an answer in a chat. | Greetings, offers of further help, and remarks about the request or about missing information stay in the text. |

## The patterns

The staged forms in group A are a defect on one occurrence. A pattern marked
*weak alone* counts only together with others. The word lists hold examples and
change with every model generation.

### A. Staged insight

- **Contrast with nothing.** "Not X, but Y", "not just X, it's Y", "not only X
  but also Y", "Y rather than X" as a reveal, and the split form "This does not
  mean X. It means Y." Keep a contrast only when the reader holds the belief
  that the first half corrects.
- **False range.** "From small cafés to starred restaurants" names two ends to
  suggest that everything between them was covered.
- **Opening for everyone.** "Whether you are a beginner or an expert, …" fits
  any reader and tells none of them anything.
- **One-line closer.** A short last sentence that restates the paragraph or
  gives it weight: "That is the real win."
- **Fragment row.** "No setup. No waiting. Just results."
- **Run-up.** "Here's the thing", "Let's dive in", "Here is what you need to
  know", "It's important to note that".
- **Sayings as depth.** "At its core", "the real question is", "X is the
  language of Y".
- **Arguing with no one.** "You might think", "To be clear", "This isn't
  about".

### B. Even rhythm

- **Lists of three** where the meaning does not have three parts: three
  adjectives, three short phrases, three examples and a lesson.
- **One sentence form repeated**: statement after statement of the same
  length, or the same opening several times in a row.
- **A participle phrase at the end of the sentence**: "…, highlighting its
  importance", "…, ensuring a smooth process", "…, reflecting broader trends".
  It claims a consequence or meaning the sources do not show.
- **Formal connectors as glue**: "Moreover", "Furthermore", "Additionally",
  "However" at the start of the sentence, or a semicolon followed by one.
  *Weak alone.*
- **Dashes in chains.** *Weak alone.* Avoiding every dash and writing only
  commas and short sentences has become a pattern of its own: choose
  punctuation by meaning.
- **A synonym for every mention** of the same thing. One term per concept.
  *Weak alone.*
- **Caution in every sentence**: "may", "often", "can potentially", "in many
  cases" where the writer knows the answer. Keep a stated limit and a real
  "we do not know".

### C. Inflation in place of fact

- **Stock vocabulary**: additionally, align with, crucial, cutting-edge, deep
  dive, delve, embark, enhance, foster, garner, intricate, journey (figurative),
  key (adjective), landscape (abstract), meticulous, nuanced, pivotal, realm,
  robust (figurative), seamless, showcase, tapestry, testament, underscore,
  valuable, vibrant. Keep the precise technical sense, glossary terms and
  interface names.
- **Inflated importance**: "marks a pivotal moment", "plays a key role",
  "stands as a testament", and a closing paragraph about challenges and a
  bright future.
- **Fine words for "is" and "has"**: "serves as", "stands as", "features",
  "boasts", "offers"; "authored" for "wrote".
- **Vague connection**: "associated with", "in connection with", "linked to"
  where the actual relationship is known.
- **Borrowed authority**: "experts say", "observers note", "industry reports",
  a list of outlets in place of what one of them said.
- **Sales language**: breathtaking, nestled, renowned, rich (figurative),
  powerful, "in the heart of". Newer models produce it less; it stays a
  defect.
- **Many words, no content**: a paragraph that can be deleted without the
  reader losing a fact, a step or a decision.

### D. Formatting as decoration

- Bold for emphasis; a list in which every item is a bold label, a colon and
  a sentence that repeats the label.
- Title Case In Headings, emoji before headings or list items, decorative
  rules and arrows.
- A summary at the end of a section: "In summary", "Overall", "In conclusion".
- Markup that the destination does not render, such as Markdown asterisks in
  a plain-text field.
- A list or headings where three sentences of prose would do.

### E. Left over from the chat

- "Great question", "Certainly!", "I hope this helps", "Let me know if",
  "Would you like me to"; in a message, "I hope this email finds you well".
- Statements about missing information followed by a guess: "specific details
  are limited", "based on available information", "likely"; a caution that
  a source "does not by itself establish" something nobody claimed.
- In a commit message, pull-request description or review comment: an
  assurance of compliance ("adheres to the guidelines", "carefully reviewed"),
  a list of what was "preserved" or "retained", and a customer-service tone.
  Say what changed and why.
- Traces of the tool: `utm_source=` parameters in links and citation markers
  such as `oaicite`.
- An unfilled placeholder: `[Name]`, `2025-XX-XX`, `INSERT_URL_HERE`.
- Text about the previous version or about the request, outside release
  notes, changelogs and migration guides.

## What to write instead

1. Write the fact that only this subject has: the name, the number, the place,
   the command, the date. When no such fact exists, delete the sentence.
2. Use "is" and "has", the plain word, and the term the reader already uses.
3. Give a list as many items as the meaning has. Let sentence length follow
   the content: a short sentence for a short thought.
4. State a limit once, where it applies. State what is unknown as unknown.
5. Begin with the point and end on the last fact.

Removing a pattern never removes a fact, a step, a warning or a stated
uncertainty. Delete a sentence that is empty without its pattern.

## Check before delivery

The catalogue is the measure. As a last pass, read the finished text once
for the seven that survive drafting most often: a contrast with nothing, a
one-line closer, a list of three, a participle phrase at a sentence end, a
stock word, a bold label, a line addressed to the person who asked. Correct
each one that the exceptions below do not cover. For a reply of a few lines
the check is one reading, with no record.

## What is not a pattern

- A watched phrase inside a quotation, a title, a product or interface name,
  code, or a passage that discusses the phrase.
- Scope statements, legal and safety notices, real corrections of a belief
  the reader holds, and a recap that a learner needs.
- Correct grammar, a formal register, or a transition word by itself.
- Three items when there are three.
- Bold for the statement of a rule, for an interface label, and for the first
  words of a list item that the reader scans by.
- A structure that a template, a glossary, a source or the person's own
  instruction requires. These take precedence over this rule's style
  preferences.

## Scope by writing mode

| Mode | How the rule applies |
|---|---|
| Reader-oriented text, including every reply | In full |
| Working notes | In full; notes are short, so groups C and E matter most |
| Manuscript: story prose and in-world text | The story's voice sheet decides the voice. A device the voice sheet names, such as fragments, a repeated opening or a list of three used for rhythm, is the author's choice. Where the sheet is silent, groups A, C and E are findings in narration, and group B is a finding where several of its patterns stand in one passage; a character may speak in any way that the character's voice card supports. Group D does not apply to prose. |
| Narration of a video | The mode of its script: tutorial narration in full, story narration as manuscript |
| Machine-read output, code, commands, data | Not covered |

## Limits

- The catalogue describes how text is recognized. A text without these
  patterns can still be empty or wrong. The cure is content that only this
  subject has.
- People recognize machine text unreliably, and detection tools err in both
  directions. The catalogue is a writing aid and no proof of who wrote a text.
- The patterns drift. Words and forms that marked one model generation fade,
  and their replacements become the next markers. Reassess this file when
  that shows.
- An invented reference, a dead link or a wrong number is a matter of
  verification and is not covered here.
- The two playbook skills come from the shared core and do not refer to this
  file. `documentation-pdf` and `presentation-video-production` write no
  text.
- Whether a host follows the rule is not measured. No host loads a policy file
  before it selects a skill, so a reply for which no skill of this method
  loads is not reached by it.

## Sources

Read on 2026-11-13. The grouping, the wording and the scope by writing mode
are this method's own.

- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup):
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Stryng, "Common sentence structures in AI-generated text":
  https://stryng.io/common-sentence-structures-in-ai-generated-text/
- Michelle Kassorla, "Recognizing AI structures in writing":
  https://michellekassorla.substack.com/p/recognizing-ai-structures-in-writing
- The pattern groups A to E were first adapted from Humanizer (MIT) in
  `human-prose-drafting`; see the third-party notices.
