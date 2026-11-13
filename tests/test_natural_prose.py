"""Writing rule #1 (natural prose) is present and every skill that writes or judges text carries it."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULE = "shared/policies/natural-prose.md"
STORY_ANCHOR = "rules.md#1-prose-rule-natural-prose"
# Skills of the family map that write no text: one renders a PDF, one voices and renders a video.
NO_TEXT = {"documentation-pdf", "presentation-video-production"}
SHARED_CARRIERS = [
    "shared/media/spoken-style.md",
    "shared/policies/reader-oriented-output.md",
    "shared/policies/writing-depth.md",
    "shared/policies/lifecycle-selection.md",
    "shared/story/rules.md",
    "README.md",
]
SEVEN = ["a contrast with nothing", "a one-line closer", "a list of three", "a stock word", "a bold label"]
LINK = re.compile(r"\]\(([^)#\s]+)")


def links(path: Path) -> set[str]:
    return {str((path.parent / target).resolve().relative_to(ROOT)) for target in LINK.findall(path.read_text())
            if "://" not in target and (path.parent / target).resolve().is_relative_to(ROOT)}


def families() -> dict[str, list[str]]:
    hub = (ROOT / "shared/policies/writing-mode.md").read_text()
    return json.loads(hub[hub.index("```json") + 7:hub.rindex("```")])["families"]


class NaturalProse(unittest.TestCase):
    def test_the_rule_states_its_rank_its_groups_and_its_scope(self) -> None:
        text = (ROOT / RULE).read_text()
        self.assertTrue(text.startswith("# Writing rule #1: natural prose"))
        self.assertIn("comes\nbefore every other writing rule", text)
        headings = [line[3:] for line in text.splitlines() if line.startswith("## ") and line != "## Contents"]
        contents = text[text.index("## Contents"):text.index("## Why readers")]
        self.assertEqual(headings, [line[2:] for line in contents.splitlines() if line.startswith("- ")])
        for group in ("### A. Staged insight", "### B. Even rhythm", "### C. Inflation in place of fact",
                      "### D. Formatting as decoration", "### E. Left over from the chat"):
            self.assertIn(group, text)
        for mode in ("Reader-oriented text, including every reply", "Working notes", "Manuscript",
                     "Narration of a video", "Machine-read output"):
            self.assertIn(f"| {mode}", text)

    def test_the_rule_links_into_no_family(self) -> None:
        self.assertEqual(set(), links(ROOT / RULE))

    def test_every_skill_of_the_family_map_that_writes_text_carries_the_rule(self) -> None:
        map_ = families()
        for name in map_["reader"] + map_["form"]:
            if name in NO_TEXT:
                continue
            with self.subTest(skill=name):
                self.assertIn(RULE, links(ROOT / "skills" / name / "SKILL.md"))
        for name in map_["story"]:
            with self.subTest(skill=name):
                self.assertIn(STORY_ANCHOR, (ROOT / "skills" / name / "SKILL.md").read_text())

    def test_shared_files_and_the_readme_link_the_rule(self) -> None:
        for carrier in SHARED_CARRIERS:
            with self.subTest(carrier=carrier):
                self.assertIn(RULE, links(ROOT / carrier))
        self.assertIn("## #1 prose rule: natural prose", (ROOT / "shared/story/rules.md").read_text())

    def test_the_story_files_name_the_same_groups_for_narration(self) -> None:
        for path in (RULE, "shared/story/rules.md", "skills/story-drafting/SKILL.md", "skills/story-voice-review/SKILL.md"):
            with self.subTest(path=path):
                text = " ".join((ROOT / path).read_text().split())
                self.assertRegex(text, r"groups A, C and E")
                self.assertRegex(text, r"(?i)group B.{0,40}where several of its patterns stand in one passage")

    def test_the_delivery_check_is_the_same_in_the_rule_and_the_prose_skill(self) -> None:
        for path in (RULE, "skills/human-prose-drafting/SKILL.md"):
            text = " ".join((ROOT / path).read_text().split())
            for item in SEVEN + ["a participle phrase at a sentence end", "a line addressed to the person who asked"]:
                with self.subTest(path=path, item=item):
                    self.assertIn(item, text)

    def test_the_prose_skill_description_names_short_texts_and_its_limits(self) -> None:
        text = (ROOT / "skills/human-prose-drafting/SKILL.md").read_text()
        description = next(line for line in text.splitlines() if line.startswith("description:"))
        for part in ("no other writing skill covers it", "email", "announcement", "commit or pull-request description",
                     "writing rule #1", "supporting skill within documentation-authoring",
                     "Not for story manuscripts or in-world text."):
            self.assertIn(part, description)
        self.assertNotIn("release note", description)


if __name__ == "__main__":
    unittest.main()
