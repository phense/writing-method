"""Writing rule #1 (natural prose) is present and every prose skill carries it."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULE = "shared/policies/natural-prose.md"
# Skills that write or judge prose for a reader, and the files that carry the rule for the story family.
CARRIERS = [
    "skills/explaining-concepts/SKILL.md",
    "skills/writing-procedures/SKILL.md",
    "skills/empathic-troubleshooting/SKILL.md",
    "skills/documentation-authoring/SKILL.md",
    "skills/documentation-review/SKILL.md",
    "skills/human-prose-drafting/SKILL.md",
    "skills/tutorial-video-scripting/SKILL.md",
    "shared/media/spoken-style.md",
    "shared/policies/reader-oriented-output.md",
    "shared/policies/writing-depth.md",
    "shared/story/rules.md",
    "README.md",
]
STORY_CARRIERS = ["skills/story-drafting/SKILL.md", "skills/story-voice-review/SKILL.md"]
LINK = re.compile(r"\]\(([^)#\s]+)")


def links(path: Path) -> set[str]:
    return {str((path.parent / target).resolve().relative_to(ROOT)) for target in LINK.findall(path.read_text())
            if "://" not in target and (path.parent / target).resolve().is_relative_to(ROOT)}


class NaturalProse(unittest.TestCase):
    def test_the_rule_states_its_rank_its_groups_and_its_scope(self) -> None:
        text = (ROOT / RULE).read_text()
        self.assertTrue(text.startswith("# Writing rule #1: natural prose"))
        for heading in ("## Why readers recognize machine text", "### A. Staged insight", "### B. Even rhythm",
                        "### C. Inflation in place of fact", "### D. Formatting as decoration",
                        "### E. Left over from the chat", "## What to write instead", "## Check before delivery",
                        "## What is not a pattern", "## Scope by writing mode", "## Limits", "## Sources"):
            self.assertIn(heading, text)
        for mode in ("Reader-oriented text, including every reply", "Working notes", "Manuscript"):
            self.assertIn(f"| {mode}", text)

    def test_the_rule_is_neutral_and_links_into_no_family(self) -> None:
        self.assertEqual(set(), links(ROOT / RULE))

    def test_every_prose_carrier_links_the_rule(self) -> None:
        for carrier in CARRIERS:
            with self.subTest(carrier=carrier):
                self.assertIn(RULE, links(ROOT / carrier))

    def test_story_skills_reach_the_rule_through_the_story_rules(self) -> None:
        for carrier in STORY_CARRIERS:
            with self.subTest(carrier=carrier):
                self.assertIn("rules.md#1-prose-rule-natural-prose", (ROOT / carrier).read_text())
        self.assertIn("## #1 prose rule: natural prose", (ROOT / "shared/story/rules.md").read_text())

    def test_the_prose_skill_is_selected_for_short_texts_without_another_skill(self) -> None:
        text = (ROOT / "skills/human-prose-drafting/SKILL.md").read_text()
        description = next(line for line in text.splitlines() if line.startswith("description:"))
        for word in ("email", "announcement", "commit or pull-request description", "writing rule #1"):
            self.assertIn(word, description)


if __name__ == "__main__":
    unittest.main()
