"""Separation of the story family from the reader family, and the form family between them.

The single JSON block in ``shared/policies/writing-mode.md`` is the authority
these tests read. They prove that names, sentences, links and the vault starter
are as the policy states. The form skills voice and render an accepted script
for either family and link into neither story directory. They do not prove that a model follows the sentences:
routing is statistical and is measured by the host evaluations.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

from scripts.package_plugin import included
from scripts.validate_plugin import MARKDOWN_LINK, _validate_platform_boundary

ROOT = Path(__file__).resolve().parents[1]
HUB = "shared/policies/writing-mode.md"
VAULT = "templates/story-vault"

STORY_SKILLS = [
    "story-bootstrap",
    "story-worldbuilding",
    "story-characters",
    "story-architecture",
    "story-drafting",
    "story-canon-review",
    "story-craft-research",
    "story-voice-review",
    "story-video-scripting",
]
READER_SKILLS = [
    "documentation-planning",
    "documentation-authoring",
    "documentation-review",
    "documentation-pdf",
    "human-prose-drafting",
    "explaining-concepts",
    "writing-procedures",
    "empathic-troubleshooting",
    "terminology-guard",
    "visual-placeholders",
    "tutorial-video-scripting",
]
# Form skills voice, time, render and check an accepted script. They serve both
# families and belong to neither.
FORM_SKILLS = [
    "presentation-video-production",
    "presentation-video-review",
]
# What the Story scripts section of a form skill has to say, beyond its heading.
FORM_STORY_RULE = "wording, tone or order"
FORM_STORY_RETURN = "`story-video-scripting`"
FORM_TUTORIAL_ONLY = "adjusted through wording (tutorial scripts only)"
FORM_NO_RUN_STATE = "A story video keeps no run state."
LISTENING_STYLE_RULE = (
    "The tutorial listening style in `shared/media/spoken-style.md` does not apply to "
    "story narration."
)
STORY_VIDEO_SKILL = "story-video-scripting"
STORY_SIDE_PREFIXES = ["shared/story/", "templates/story-vault/", "skills/story-"]
PRECEDENCE_READER_SKILLS = [
    "explaining-concepts",
    "writing-procedures",
    "empathic-troubleshooting",
    "human-prose-drafting",
]
EXCLUDED_READER_SKILLS = PRECEDENCE_READER_SKILLS + [
    "documentation-authoring",
    "documentation-review",
    "terminology-guard",
    "tutorial-video-scripting",
]
PRECEDENCE_STORY_SKILLS = ["story-drafting", "story-voice-review", "story-video-scripting"]

NO_RUN_STATE = (
    "No run state: this skill has no recovery preamble and hands off to no backlog or run-tracking skill. "
    "A story or study vault keeps no backlog and no run directory; its state lives in "
    "00-project/development.md and 00-project/decisions.md."
)

# Skill names of the sibling Engineering Method plugin. Both plugins can be
# installed together, and OpenCode has one flat skill namespace.
ENGINEERING_SKILLS = {
    "architecture-modeling",
    "openspec-apply",
    "openspec-archive",
    "openspec-propose",
    "orchestrated-implementation",
    "speckit-converge",
    "speckit-plan",
    "speckit-specify",
    "speckit-tasks",
    "systematic-debugging",
    "test-driven-development",
}

# The exact sentences of the implementation contract. The policy block must
# store them unchanged; every carrier is then compared against the block.
S1 = (
    "Mode check first, under [writing mode](../../shared/policies/writing-mode.md): "
    "find the nearest ancestor of the target file that holds 00-project/brief.md and "
    "00-project/voice.md. Only kind story permits manuscript drafting; kind study "
    "permits study notes only; kind starter routes to story-bootstrap."
)
S2 = (
    "For manuscript text the story's voice sheet overrides explaining-concepts, "
    "writing-procedures, empathic-troubleshooting and human-prose-drafting, even when "
    "those skills are loaded in this session."
)
S3 = "Not for session replies, documentation or presentation videos."
# The one story skill that scripts a presentation video excludes tutorial videos instead.
S3_VIDEO = "Not for session replies, documentation or tutorial videos."
S4 = "Not for story manuscripts or in-world text."
S5 = (
    "Not for story manuscripts or in-world text: when the target is manuscript, stop "
    "and use the story family under [writing mode](../../shared/policies/writing-mode.md)."
)
S6 = (
    "Manuscript files follow 00-project/voice.md and nothing from documentation or "
    "didactic writing rules. Other vault notes are plain working notes. Replies to the "
    "author stay reader-oriented; the voice sheet never styles a reply."
)
CONTRACT_SENTENCES = {
    "story_opening": S1,
    "precedence": S2,
    "story_description_suffix": S3,
    "story_video_description_suffix": S3_VIDEO,
    "reader_description_clause": S4,
    "reader_opening": S5,
    "vault_instruction": S6,
}

# Reader-family policy files that may refer to the story side, and only by
# linking the hub.
HUB_LINKING_POLICIES = [
    "shared/policies/lifecycle-selection.md",
    "shared/policies/reader-oriented-output.md",
    "shared/policies/writing-depth.md",
]
# Repository documents written for readers of the plugin. They name both
# families, so only the link rule applies to them.
READER_DOCUMENTS = ["README.md", "docs/usage.md"]

URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
WIKI_LINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
JSON_BLOCK = re.compile(r"```json\n(.*?)\n```", re.S)
FRONTMATTER_LINE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:(?: \S.*)?$")
PRIVATE_PATH = re.compile(r"(?<![\w-])(?:research|external)/")
EXEMPT_LINE = re.compile(r"Not for|Do not use")
# Link forms beside the inline link: a reference definition and an HTML href.
REFERENCE_DEFINITION = re.compile(r"(?m)^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)")
HTML_HREF = re.compile(r"href\s*=\s*[\"']([^\"']+)[\"']")

# Package hygiene patterns. A home-relative path counts as a user path.
USER_PATH = re.compile(r"/Users/|/home/[a-z]|~/[A-Za-z]")
OWNER_NAME = re.compile(r"\bPeter\b")
MEMORY_SERVICE = re.compile(r"agentic-rag|domain=worldbuilding|mcp__")

# Exemptions from the hygiene scan, by exact path. Each one is a file that must
# hold the text; nothing is exempt by directory except the one prefix below.
# This module holds the patterns themselves.
HYGIENE_SELF = "tests/test_writing_mode.py"
# Licence, copyright, author and product-name fields carry the owner's name.
OWNER_NAME_ALLOWED = {
    HYGIENE_SELF,
    "LICENSE",                                  # copyright line
    "THIRD_PARTY_NOTICES.md",                   # copyright line
    "CORE_NOTICES.md",                          # copyright line (Method Core)
    "third-party/sources.lock.json",            # copyright field
    "third-party/core-sources.lock.json",       # copyright field (Method Core)
    ".claude-plugin/marketplace.json",          # owner field
    ".claude-plugin/plugin.json",               # author and display name
    ".codex-plugin/plugin.json",                # author, developer and display name
    "templates/documentation/book/_extensions/em-book/_extension.yml",   # author field
    "templates/documentation/pdf/_extensions/em-manual/_extension.yml",  # author field
    "FEATURES.md",                              # product name in the generated statement
    "engineering_method/features.py",           # product name (Method Core)
    "engineering_method/issues.py",             # product name (Method Core)
    "tests/test_method_identity.py",            # product name (Method Core)
}
# Method Core files, which this repository must not edit.
MEMORY_SERVICE_ALLOWED = {
    HYGIENE_SELF,
    "scripts/run_host_evals.py",                # generic tool-name prefix in the eval harness
    "shared/platform/opencode.md",              # names the service as out of scope
}
USER_PATH_ALLOWED = {HYGIENE_SELF}
# Design records keep the port table, which names source paths of the private
# workspace. They are exempt from the research/external pattern only.
PRIVATE_PATH_ALLOWED = {HYGIENE_SELF}
PRIVATE_PATH_ALLOWED_PREFIX = "docs/specs/"


# --- helpers -----------------------------------------------------------------

def read(relative: str | Path) -> str:
    path = relative if isinstance(relative, Path) else ROOT / relative
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def squash(text: str) -> str:
    """Collapse line wrapping so a sentence compares equal however it is wrapped."""
    return " ".join(text.split())


def load_policy() -> dict:
    blocks = JSON_BLOCK.findall(read(HUB))
    if len(blocks) != 1:
        raise AssertionError(f"{HUB} must contain exactly one json block, found {len(blocks)}")
    return json.loads(blocks[0])


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (frontmatter lines, body). A file without frontmatter has no lines."""
    if not text.startswith("---\n"):
        return [], text
    head, separator, body = text[4:].partition("\n---\n")
    if not separator:
        raise AssertionError("unterminated frontmatter")
    return head.split("\n"), body


def frontmatter(relative: str | Path) -> dict[str, str]:
    lines, _ = split_frontmatter(read(relative))
    fields = {}
    for line in lines:
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def skill_description(name: str) -> str:
    raw = frontmatter(f"skills/{name}/SKILL.md")["description"]
    if not (raw.startswith('"') and raw.endswith('"') and len(raw) >= 2):
        raise AssertionError(f"{name}: description must be a double-quoted scalar on one line")
    return json.loads(raw)


def paragraphs_after_h1(relative: str) -> list[str]:
    """Body paragraphs that follow the first H1, each with its wrapping collapsed."""
    _, body = split_frontmatter(read(relative))
    match = re.search(r"^# .+$", body, re.M)
    if match is None:
        raise AssertionError(f"{relative}: no H1")
    return [squash(block) for block in re.split(r"\n\s*\n", body[match.end():]) if block.strip()]


def markdown_files(*trees: str) -> list[Path]:
    found: list[Path] = []
    for tree in trees:
        found.extend(sorted((ROOT / tree).rglob("*.md")))
    return found


def story_files() -> list[Path]:
    """Every Markdown file of the story family, starter vault included."""
    skills = [p for d in sorted((ROOT / "skills").glob("story-*")) for p in sorted(d.rglob("*.md"))]
    return skills + markdown_files("shared/story", VAULT)


def reader_files(policy: dict) -> list[Path]:
    """Every Markdown file of the reader family, without the neutral hub."""
    skills = [p for name in policy["families"]["reader"]
              for p in sorted((ROOT / "skills" / name).rglob("*.md"))]
    policies = [p for p in sorted((ROOT / "shared/policies").glob("*.md")) if rel(p) != HUB]
    return skills + policies + markdown_files(
        "shared/writing", "shared/media", "templates/documentation", "templates/presentation-video")


def form_files(policy: dict) -> list[Path]:
    """Every Markdown file of the form skills."""
    return [p for name in policy["families"]["form"]
            for p in sorted((ROOT / "skills" / name).rglob("*.md"))]


def link_destination(written: str) -> str:
    """The destination of a link as written: angle brackets and a title removed."""
    written = written.strip()
    if written.startswith("<"):
        # Before any whitespace split, so a bracketed path with spaces survives.
        return written[1:].split(">", 1)[0]
    return written.split()[0] if written else ""


def link_targets_in(text: str, path: Path) -> list[tuple[str, str | None]]:
    """Targets of every link in text, resolved as if text were the file at path.

    Inline links, reference definitions and HTML href attributes all count.
    """
    written_links = (MARKDOWN_LINK.findall(text) + REFERENCE_DEFINITION.findall(text)
                     + HTML_HREF.findall(text))
    targets = []
    for written in written_links:
        link = link_destination(written)
        if not link or link.startswith("#") or URL_SCHEME.match(link):
            continue
        resolved = (path.parent / unquote(link.split("#", 1)[0])).resolve()
        inside = resolved.is_relative_to(ROOT.resolve())
        targets.append((written, resolved.relative_to(ROOT.resolve()).as_posix() if inside else None))
    return targets


def relative_link_targets(path: Path) -> list[tuple[str, str | None]]:
    """(link as written, repo-relative target or None when it leaves the repo)."""
    return link_targets_in(read(path), path)


def under(target: str, prefixes: list[str]) -> bool:
    # A link to the directory itself ("shared/story") matches its prefix "shared/story/".
    return any(target.startswith(prefix) or (target + "/").startswith(prefix)
               for prefix in prefixes)


def without_exempt_text(text: str, sentences: list[str]) -> str:
    """Drop the contract sentences and every 'Not for' / 'Do not use' line."""
    for sentence in sentences:
        text = re.sub(r"\s+".join(re.escape(word) for word in sentence.split()), " ", text)
    return "\n".join(line for line in text.split("\n") if not EXEMPT_LINE.search(line))


def backticked(names: list[str], text: str) -> list[str]:
    return [name for name in names if f"`{name}`" in text]


def hygiene_files() -> list[Path]:
    """Every file the release archive ships, whatever its type.

    The list is Git's file list passed through the packager's own inclusion
    rule. Untracked files that are not ignored are listed too: they ship with
    the next commit. Without a Git checkout the tree is walked instead.
    """
    listing = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True, timeout=30)
    if listing.returncode == 0:
        names = [name for name in listing.stdout.decode("utf-8").split("\0") if name]
    else:
        names = [rel(p) for p in ROOT.rglob("*") if p.is_file()]
    return [ROOT / name for name in sorted(set(names)) if included(name) and (ROOT / name).is_file()]


# --- policy block and family map ---------------------------------------------

class PolicyBlock(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.policy = load_policy()

    def test_policy_block_states_the_contract(self):
        policy = self.policy
        self.assertEqual(1, policy["schema_version"])
        self.assertEqual("experimental", policy["status"])
        self.assertEqual(HUB, policy["hub"])
        self.assertEqual({"story": STORY_SKILLS, "reader": READER_SKILLS, "form": FORM_SKILLS},
                         policy["families"])
        self.assertEqual((9, 11, 2), (len(STORY_SKILLS), len(READER_SKILLS), len(FORM_SKILLS)))
        # A story video is scripted from the video project template and handed to the form skills.
        self.assertEqual(
            {"prefixes": STORY_SIDE_PREFIXES + ["templates/presentation-video/"],
             "files": [HUB, "shared/policies/proportionality.md",
                       "skills/verification-before-completion/SKILL.md",
                       "skills/presentation-video-production/SKILL.md",
                       "skills/presentation-video-review/SKILL.md",
                       "shared/media/speech-synthesis.md"]},
            policy["story_link_allow"])
        self.assertEqual(STORY_SIDE_PREFIXES, policy["reader_link_deny_prefixes"])
        self.assertEqual(STORY_SIDE_PREFIXES, policy["form_link_deny_prefixes"])
        self.assertEqual(PRECEDENCE_READER_SKILLS, policy["precedence_reader_skills"])
        self.assertEqual(EXCLUDED_READER_SKILLS, policy["excluded_reader_skills"])
        self.assertEqual(PRECEDENCE_STORY_SKILLS, policy["precedence_story_skills"])
        self.assertEqual(CONTRACT_SENTENCES, policy["sentences"])

    def test_policy_block_states_the_vault_rule(self):
        self.assertEqual(
            {"markers": ["00-project/brief.md", "00-project/voice.md"],
             "kinds": ["story", "study", "starter"],
             "drafting_kind": "story",
             "drafting_requires_voice_fields": ["viewpoint", "tense", "distance"],
             "forms": ["long-form", "short-form"],
             "manuscript_paths": ["06-manuscript/chapters/", "06-manuscript/paratext/",
                                  "06-manuscript/editions/"],
             "short_form_manuscript_heading": "## Manuscript",
             "reader_files": ["README.md", "START.md", "AGENTS.md", "CLAUDE.md"]},
            self.policy["vault"])

    def test_families_partition_exactly_the_method_skills(self):
        families = self.policy["families"]
        self.assertEqual(["story", "reader", "form"], list(families))
        story, reader, form = families["story"], families["reader"], families["form"]
        everything = story + reader + form
        owned = json.loads(read("method.json"))["method_skills"]
        self.assertEqual(len(everything), len(set(everything)), "a skill is listed twice")
        self.assertEqual(set(), set(story) & set(reader))
        self.assertEqual(set(), set(form) & set(story + reader))
        self.assertEqual(len(owned), len(set(owned)), "method.json lists a skill twice")
        self.assertEqual(sorted(owned), sorted(everything))
        self.assertEqual((9, 11, 2), (len(story), len(reader), len(form)))
        for name in everything:
            self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file(), name)
            self.assertEqual(name, frontmatter(f"skills/{name}/SKILL.md")["name"])

    def test_story_names_are_prefixed_and_collide_with_nothing(self):
        lock = json.loads(read("method-core.lock.json"))
        shared = {item["path"].split("/")[1] for item in lock["files"]
                  if re.fullmatch(r"skills/[^/]+/SKILL\.md", item["path"])}
        self.assertTrue(shared, "the core lock names no shared skill")
        reader = set(self.policy["families"]["reader"]) | set(self.policy["families"]["form"])
        for name in self.policy["families"]["story"]:
            self.assertTrue(name.startswith("story-"), name)
            self.assertNotIn("continuity", name)
            self.assertNotIn(name, shared)
            self.assertNotIn(name, ENGINEERING_SKILLS)
            self.assertNotIn(name, reader)
        on_disk = {p.parent.name for p in (ROOT / "skills").glob("story-*/SKILL.md")}
        self.assertEqual(set(self.policy["families"]["story"]), on_disk)
        # A form skill is not a story skill: its name carries no story prefix.
        for name in self.policy["families"]["form"]:
            self.assertFalse(name.startswith("story-"), name)

    def test_hub_contains_no_markdown_link(self):
        # The stored sentences S1 and S5 carry link syntax, so the block is set aside.
        prose = JSON_BLOCK.sub("", read(HUB))
        self.assertEqual([], MARKDOWN_LINK.findall(prose))


# --- sentences in their carriers ---------------------------------------------

class OperativeSentences(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.policy = load_policy()
        self.sentences = self.policy["sentences"]

    def test_every_story_skill_opens_with_the_mode_check(self):
        for name in self.policy["families"]["story"]:
            with self.subTest(skill=name):
                paragraphs = paragraphs_after_h1(f"skills/{name}/SKILL.md")
                self.assertEqual(self.sentences["story_opening"], paragraphs[0])

    def test_precedence_story_skills_state_the_precedence_second(self):
        for name in self.policy["precedence_story_skills"]:
            with self.subTest(skill=name):
                paragraphs = paragraphs_after_h1(f"skills/{name}/SKILL.md")
                self.assertGreaterEqual(len(paragraphs), 2)
                self.assertEqual(self.sentences["precedence"], paragraphs[1])

    def test_every_story_skill_rules_out_run_state(self):
        # Hosts otherwise go looking for a recovery preamble and open the backlog skill in a vault.
        for name in STORY_SKILLS:
            self.assertIn(NO_RUN_STATE, paragraphs_after_h1(f"skills/{name}/SKILL.md")[:3], name)

    def test_story_video_scripting_opens_like_a_manuscript_skill(self):
        # Narration of a story video is manuscript: mode check, precedence, no run state, in this order.
        self.assertIn("story-video-scripting", self.policy["precedence_story_skills"])
        paragraphs = paragraphs_after_h1("skills/story-video-scripting/SKILL.md")
        self.assertEqual(
            [self.sentences["story_opening"], self.sentences["precedence"], NO_RUN_STATE],
            paragraphs[:3])
        description = skill_description("story-video-scripting")
        self.assertTrue(description.startswith("Use when "), description)
        # It scripts a presentation video, so it cannot end by excluding presentation videos.
        self.assertTrue(description.endswith(self.sentences["story_video_description_suffix"]), description)
        self.assertNotIn(self.sentences["story_description_suffix"], description)

    def test_form_descriptions_carry_no_family_exclusion(self):
        # A form skill serves both families, so neither family's exclusion sentence may end it.
        for name in self.policy["families"]["form"]:
            with self.subTest(skill=name):
                description = skill_description(name)
                self.assertTrue(description.startswith("Use when "), description)
                self.assertIn("story video", description)
                self.assertNotIn(self.sentences["story_description_suffix"], description)
                self.assertNotIn(self.sentences["story_video_description_suffix"], description)
                self.assertNotIn(self.sentences["reader_description_clause"], description)

    def test_every_story_description_ends_with_the_exclusion(self):
        for name in self.policy["families"]["story"]:
            with self.subTest(skill=name):
                key = ("story_video_description_suffix" if name == STORY_VIDEO_SKILL
                       else "story_description_suffix")
                self.assertTrue(skill_description(name).endswith(self.sentences[key]),
                                skill_description(name))

    def test_excluded_reader_descriptions_end_with_the_story_exclusion(self):
        for name in self.policy["excluded_reader_skills"]:
            with self.subTest(skill=name):
                description = skill_description(name)
                self.assertIn(self.sentences["reader_description_clause"], description)
                self.assertTrue(description.endswith(self.sentences["reader_description_clause"]),
                                description)

    def test_precedence_reader_skills_open_with_the_story_exclusion(self):
        for name in self.policy["precedence_reader_skills"]:
            with self.subTest(skill=name):
                paragraphs = paragraphs_after_h1(f"skills/{name}/SKILL.md")
                self.assertEqual(self.sentences["reader_opening"], paragraphs[0])

    def test_opening_links_resolve_to_the_hub(self):
        # S1 and S5 are written for a file at skills/<name>/SKILL.md.
        for sentence in (self.sentences["story_opening"], self.sentences["reader_opening"]):
            (target,) = MARKDOWN_LINK.findall(sentence)
            resolved = (ROOT / "skills/any-skill" / target).resolve()
            self.assertEqual((ROOT / HUB).resolve(), resolved)

    def test_vault_instruction_file_carries_the_mode_rule(self):
        self.assertIn(self.sentences["vault_instruction"], squash(read(f"{VAULT}/AGENTS.md")))


# --- link firewall -----------------------------------------------------------

class LinkFirewall(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.policy = load_policy()

    def test_story_family_files_exist(self):
        for name in ["rules.md", "workflow.md", "story-development.md", "retrieval.md",
                     "sources.md", "voice-and-tone.md"]:
            self.assertTrue((ROOT / "shared/story" / name).is_file(), name)
        self.assertTrue((ROOT / VAULT).is_dir())

    def test_story_links_resolve_and_stay_on_the_allow_list(self):
        allow = self.policy["story_link_allow"]
        problems = []
        for path in story_files():
            for written, target in relative_link_targets(path):
                if target is None:
                    problems.append(f"{rel(path)}: {written} leaves the repository")
                elif not (ROOT / target).is_file():
                    problems.append(f"{rel(path)}: {written} does not resolve to a file")
                elif not (under(target, allow["prefixes"]) or target in allow["files"]):
                    problems.append(f"{rel(path)}: {written} -> {target} is not on the allow list")
        self.assertEqual([], problems)

    def test_reader_files_never_link_into_the_story_family(self):
        deny = self.policy["reader_link_deny_prefixes"]
        problems = []
        for path in reader_files(self.policy) + [ROOT / name for name in READER_DOCUMENTS]:
            for written, target in relative_link_targets(path):
                if target is not None and under(target, deny):
                    problems.append(f"{rel(path)}: {written} -> {target}")
        self.assertEqual([], problems)

    def test_form_skills_never_link_into_the_story_family(self):
        # Form skills may be linked by both families and link into neither story directory.
        deny = self.policy["form_link_deny_prefixes"]
        files = form_files(self.policy)
        self.assertEqual({f"skills/{name}/SKILL.md" for name in FORM_SKILLS},
                         {rel(p) for p in files if p.name == "SKILL.md"})
        problems = []
        for path in files:
            for written, target in relative_link_targets(path):
                if target is None:
                    problems.append(f"{rel(path)}: {written} leaves the repository")
                elif under(target, deny):
                    problems.append(f"{rel(path)}: {written} -> {target}")
        self.assertEqual([], problems)

    def test_form_skills_state_the_story_script_rule(self):
        # A form skill may name skills of both families in backticks; it never restyles a story script.
        for name in self.policy["families"]["form"]:
            with self.subTest(skill=name):
                text = read(f"skills/{name}/SKILL.md")
                self.assertIn("\n## Story scripts\n", text)
                section = squash(text.split("\n## Story scripts\n", 1)[1].split("\n## ", 1)[0])
                self.assertIn(FORM_STORY_RULE, section)
                self.assertIn("never", section.lower())
                self.assertIn(FORM_STORY_RETURN, section)
                # A story video is never sent to the backlog recovery gate, in the preamble or in the section.
                self.assertIn(FORM_NO_RUN_STATE, section)
                preamble = squash(text.split("\n## Recovery preamble\n", 1)[1].split("\n## ", 1)[0])
                self.assertIn(FORM_NO_RUN_STATE, preamble)
        production = read("skills/presentation-video-production/SKILL.md")
        self.assertIn(FORM_TUTORIAL_ONLY, squash(production))
        self.assertIn("Pace is adjusted through an effective provider setting or the pause value only.",
                      squash(production.split("\n## Story scripts\n", 1)[1].split("\n## ", 1)[0]))

    def test_tutorial_listening_style_is_set_aside_for_story_narration(self):
        # The review skill links the tutorial listening style; the rule that it does not govern a story is stated where it is read.
        review = read("skills/presentation-video-review/SKILL.md")
        self.assertIn(LISTENING_STYLE_RULE,
                      squash(review.split("\n## Story scripts\n", 1)[1].split("\n## ", 1)[0]))
        self.assertIn(LISTENING_STYLE_RULE, squash(read("skills/story-video-scripting/SKILL.md")))
        self.assertIn(LISTENING_STYLE_RULE, squash(read(HUB)))

    def test_hub_decides_the_files_of_a_story_video_project(self):
        hub = read(HUB)
        row = next(line for line in hub.splitlines() if line.startswith("| 2 |"))
        self.assertIn("`src/narration.json`", row)
        self.assertIn("`purpose: story`", row)
        self.assertIn("story video project", next(line for line in hub.splitlines() if line.startswith("| 3 |")))

    def test_policy_files_refer_to_the_story_side_only_through_the_hub(self):
        story_side = self.policy["reader_link_deny_prefixes"]
        for relative in HUB_LINKING_POLICIES:
            with self.subTest(file=relative):
                targets = [target for _, target in relative_link_targets(ROOT / relative)]
                # The reference to the story side has to be there, as a link to the hub.
                self.assertIn(HUB, targets)
                beyond_hub = [t for t in targets if t is not None and under(t, story_side)]
                self.assertEqual([], beyond_hub)

    def test_firewall_helpers_catch_every_link_form(self):
        # The helpers themselves are pinned: each form below is a link into the
        # story family written in a reader skill and must be reported.
        deny = self.policy["reader_link_deny_prefixes"]
        reader_skill = ROOT / "skills/explaining-concepts/SKILL.md"
        caught = {
            "inline file link": "[r](../../shared/story/rules.md)",
            "inline link with a title": '[r](../../shared/story/rules.md "Rules")',
            "inline link with an anchor": "[r](../../shared/story/rules.md#rule-1)",
            "skill directory": "[s](../story-drafting)",
            "directory with a trailing slash": "[r](../../shared/story/)",
            "directory without a trailing slash": "[r](../../shared/story)",
            "vault starter directory": "[v](../../templates/story-vault)",
            "angle brackets": "[r](<../../shared/story/rules.md>)",
            "angle brackets around a path with a space": "[r](<../../shared/story/two words.md>)",
            "reference definition": "See [r][x].\n\n[x]: ../../shared/story/rules.md",
            "reference definition in angle brackets": "[x]: <../../shared/story/rules.md>",
            "HTML link": '<a href="../../shared/story/rules.md">r</a>',
            "HTML link in single quotes": "<a href='../../templates/story-vault/AGENTS.md'>v</a>",
        }
        for form, text in caught.items():
            with self.subTest(form=form):
                targets = [target for _, target in link_targets_in(text, reader_skill)]
                self.assertTrue(any(t is not None and under(t, deny) for t in targets), targets)
        allowed = {
            "the hub": "[writing mode](../../shared/policies/writing-mode.md)",
            "a reader policy": "[depth](../../shared/policies/writing-depth.md)",
            "a sibling whose name only starts alike": "[s](../../shared/story-notes.md)",
            "a URL": "[u](https://example.com/shared/story/rules.md)",
            "a URL in a reference definition": "[x]: https://example.com/skills/story-drafting",
            "an anchor": "[a](#shared/story/)",
        }
        for form, text in allowed.items():
            with self.subTest(form=form):
                targets = [target for _, target in link_targets_in(text, reader_skill)]
                self.assertFalse(any(t is not None and under(t, deny) for t in targets), targets)
        self.assertEqual("../a b.md", link_destination("<../a b.md>"))
        self.assertEqual("../a.md", link_destination('../a.md "title"'))

    def test_story_files_name_no_reader_skill_outside_the_contract_sentences(self):
        # Form skills are not reader skills: a story file may name them.
        sentences = list(self.policy["sentences"].values())
        reader = self.policy["families"]["reader"]
        self.assertEqual(set(), set(reader) & set(FORM_SKILLS))
        problems = {}
        for path in story_files():
            found = backticked(reader, without_exempt_text(read(path), sentences))
            if found:
                problems[rel(path)] = found
        self.assertEqual({}, problems)

    def test_reader_files_name_no_story_skill_outside_the_contract_sentences(self):
        sentences = list(self.policy["sentences"].values())
        story = self.policy["families"]["story"]
        problems = {}
        for path in reader_files(self.policy):
            found = backticked(story, without_exempt_text(read(path), sentences))
            if found:
                problems[rel(path)] = found
        self.assertEqual({}, problems)

    def test_lifecycle_graph_contains_no_story_node(self):
        self.assertNotIn("story-", read("shared/policies/lifecycle-handoffs.md"))


# --- vault starter -----------------------------------------------------------

class VaultStarter(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.policy = load_policy()
        self.vault = ROOT / VAULT

    def test_markers_declare_an_unset_starter(self):
        for marker in self.policy["vault"]["markers"]:
            with self.subTest(marker=marker):
                self.assertTrue((self.vault / marker).is_file())
                fields = frontmatter(self.vault / marker)
                self.assertEqual("starter", fields.get("kind"))
                self.assertEqual("unset", fields.get("story_id"))
                # The story ID lives in the frontmatter only.
                _, body = split_frontmatter(read(self.vault / marker))
                self.assertIsNone(re.search(r"(?i)\bstory[ _]id\b\s*:", body))

    def test_brief_declares_form_and_publication_profile(self):
        fields = frontmatter(self.vault / "00-project/brief.md")
        self.assertEqual("long-form", fields.get("form"))
        self.assertIn(fields["form"], self.policy["vault"]["forms"])
        self.assertEqual("unset", fields.get("publication_profile"))

    def test_voice_sheet_leaves_the_drafting_fields_unset(self):
        fields = frontmatter(self.vault / "00-project/voice.md")
        for field in self.policy["vault"]["drafting_requires_voice_fields"]:
            self.assertEqual("unset", fields.get(field), field)
        self.assertEqual("V0", fields.get("voice_revision"))

    def test_instruction_files_exist(self):
        self.assertIn(self.policy["sentences"]["vault_instruction"],
                      squash(read(self.vault / "AGENTS.md")))
        self.assertTrue((self.vault / "CLAUDE.md").is_file())
        # The adapter imports the authority; it does not repeat it.
        self.assertIn("AGENTS.md", read(self.vault / "CLAUDE.md"))
        for name in self.policy["vault"]["reader_files"]:
            if name != "README.md":
                self.assertTrue((self.vault / name).is_file(), name)

    def test_manuscript_directories_exist(self):
        # The policy names where manuscript prose lives; the starter has to ship those places.
        paths = self.policy["vault"]["manuscript_paths"]
        self.assertTrue(paths)
        for relative in paths:
            with self.subTest(path=relative):
                self.assertTrue(relative.endswith("/"), relative)
                self.assertTrue((self.vault / relative).is_dir(), relative)
        # Short-form pieces are one note each; the vault files name this directory.
        self.assertTrue((self.vault / "06-manuscript/pieces").is_dir())
        # A listening edition is manuscript and is kept apart from the written chapters.
        self.assertIn("06-manuscript/editions/", paths)
        self.assertTrue((self.vault / "06-manuscript/editions").is_dir())
        self.assertIn("Listening editions", read(self.vault / "06-manuscript/index.md"))

    def test_listening_edition_template_exists(self):
        template = self.vault / "90-templates/listening-edition.md"
        self.assertTrue(template.is_file())
        fields = frontmatter(template)
        self.assertEqual("template", fields.get("type"))
        self.assertEqual("listening-edition", fields.get("template_type"))

    def test_templates_for_both_forms_exist(self):
        templates = self.vault / "90-templates"
        for name in ["chapter.md", "chapter-prose.md", "short-piece.md", "volume.md", "source-card.md"]:
            self.assertTrue((templates / name).is_file(), name)
        heading = self.policy["vault"]["short_form_manuscript_heading"]
        lines = lambda name: read(templates / name).split("\n")
        # Long form keeps prose out of the chapter card; short form keeps it under one heading.
        self.assertNotIn(heading, lines("chapter.md"))
        self.assertIn(heading, lines("short-piece.md"))
        self.assertIn("Voice card", read(templates / "character.md"))
        self.assertIn("Voice review", read(templates / "review.md"))

    def test_every_wiki_link_resolves_inside_the_starter(self):
        notes = sorted(self.vault.rglob("*.md"))
        self.assertTrue(notes)
        missing = []
        for path in notes:
            for target in WIKI_LINK.findall(read(path)):
                note = target.split("#", 1)[0].strip()
                resolved = (self.vault / (note + ".md")).resolve()
                if not note or not resolved.is_relative_to(self.vault.resolve()) or not resolved.is_file():
                    missing.append(f"{rel(path)}: [[{target}]]")
        self.assertEqual([], missing)

    def test_frontmatter_is_simple_key_value_lines(self):
        problems = []
        for path in sorted(self.vault.rglob("*.md")):
            lines, _ = split_frontmatter(read(path))
            keys = [line.split(":", 1)[0] for line in lines]
            if len(keys) != len(set(keys)):
                problems.append(f"{rel(path)}: repeated key")
            problems.extend(f"{rel(path)}: {line!r}" for line in lines
                            if not FRONTMATTER_LINE.fullmatch(line))
        self.assertEqual([], problems)


# --- package hygiene ---------------------------------------------------------

class StoryPackageHygiene(unittest.TestCase):
    """Scans every file of the release archive, not only the story trees."""
    maxDiff = None

    def scan(self, pattern: re.Pattern, allowed: set[str], allowed_prefix: str | None = None) -> list[str]:
        hits = []
        for path in hygiene_files():
            name = rel(path)
            if name in allowed or (allowed_prefix is not None and name.startswith(allowed_prefix)):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # binary files, such as the bundled fonts
            hits.extend(f"{name}: {match.group(0)}" for match in pattern.finditer(text))
        return hits

    def test_scan_covers_the_package(self):
        scanned = {rel(path) for path in hygiene_files()}
        expected = {HUB, "README.md", "docs/usage.md", "THIRD_PARTY_NOTICES.md",
                    "docs/specs/WM-003-story-family/design.md",
                    "tests/fixtures/trigger-cases/matrix.json",
                    "evals/shared/triggers/story-chapter-draft.json",
                    "evals/shared/triggers/story-video-script.json",
                    "evals/shared/triggers/story-video-production.json",
                    "evals/shared/triggers/story-listening-edition.json",
                    "shared/story/rules.md", f"{VAULT}/AGENTS.md"}
        expected |= {f"skills/{name}/SKILL.md" for name in STORY_SKILLS + READER_SKILLS + FORM_SKILLS}
        self.assertEqual(set(), expected - scanned)
        # Nothing the packager leaves out is scanned, and every exemption names a shipped file.
        self.assertTrue(all(included(name) for name in scanned))
        exempt = OWNER_NAME_ALLOWED | MEMORY_SERVICE_ALLOWED | USER_PATH_ALLOWED | PRIVATE_PATH_ALLOWED
        self.assertEqual(set(), exempt - scanned)

    def test_no_absolute_or_home_relative_user_path(self):
        self.assertEqual([], self.scan(USER_PATH, USER_PATH_ALLOWED))

    def test_no_owner_name_outside_licence_and_manifest_fields(self):
        self.assertEqual([], self.scan(OWNER_NAME, OWNER_NAME_ALLOWED))

    def test_no_path_into_private_research_or_study_material(self):
        self.assertEqual([], self.scan(PRIVATE_PATH, PRIVATE_PATH_ALLOWED, PRIVATE_PATH_ALLOWED_PREFIX))

    def test_no_private_memory_service(self):
        self.assertEqual([], self.scan(MEMORY_SERVICE, MEMORY_SERVICE_ALLOWED))

    def test_shared_story_holds_no_host_syntax(self):
        # The validator scans skills, templates and shared/policies. Its own check
        # is pointed at shared/story by presenting that directory as a scanned tree.
        self.assertTrue(any((ROOT / "shared/story").glob("*.md")))
        with tempfile.TemporaryDirectory(prefix="writing-mode-") as directory:
            stage = Path(directory)
            shutil.copytree(ROOT / "shared/story", stage / "skills")
            (stage / "templates").mkdir()
            (stage / "shared/policies").mkdir(parents=True)
            errors: list[str] = []
            _validate_platform_boundary(stage, errors)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
