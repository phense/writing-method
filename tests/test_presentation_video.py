"""Presentation-video tools: script check, voicing, timeline, measurements."""
import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "presentation-video"
sys.path.insert(0, str(TEMPLATE / "tools"))
import audio  # noqa: E402
import check_review  # noqa: E402
import check_script  # noqa: E402
import measure  # noqa: E402
import probe_settings  # noqa: E402
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402
import split_takes  # noqa: E402
import timeline  # noqa: E402
import verify_speech  # noqa: E402
import voice_azure  # noqa: E402

FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
PROFILE = TEMPLATE / "video-profile.example.json"


def sample():
    prof = profile_mod.load(TEMPLATE, PROFILE)
    return (prof, profile_mod.load_video(TEMPLATE), project.load_scenes(TEMPLATE),
            project.load_narration(TEMPLATE), (TEMPLATE / "script" / "script.md").read_text())


def rules(findings, severity="error"):
    return {f["rule"] for f in findings if f["severity"] == severity}


class Profile(unittest.TestCase):
    def write(self, data):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder)
        (folder / "video-profile.json").write_text(json.dumps(data))
        return folder

    def base(self):
        return json.loads(PROFILE.read_text())

    def test_example_profile_is_valid_and_defaults_apply(self):
        prof = profile_mod.load(TEMPLATE, PROFILE)
        self.assertEqual(0.65, prof["pause"]["line"])
        self.assertEqual(45, prof["script"]["max_minutes"])
        self.assertEqual(8, prof["speech"]["retry_budget"])

    def test_pace_range_defaults_by_language_unless_the_profile_sets_it(self):
        data = self.base(); del data["pace_wpm"]
        self.assertEqual([140, 180], profile_mod.load(self.write(data))["pace_wpm"])
        data["language"] = "de-DE"
        self.assertEqual([120, 155], profile_mod.load(self.write(data))["pace_wpm"])
        data["pace_wpm"] = [100, 130]
        self.assertEqual([100, 130], profile_mod.load(self.write(data))["pace_wpm"])

    def test_profile_is_found_in_a_parent_folder(self):
        folder = self.write(self.base())
        (folder / "videos" / "one").mkdir(parents=True)
        self.assertEqual(folder / "video-profile.json", profile_mod.find_profile(folder / "videos" / "one"))

    def test_missing_and_unknown_keys_are_named(self):
        data = self.base(); del data["language"]
        with self.assertRaisesRegex(profile_mod.ProfileError, "language"):
            profile_mod.load(self.write(data))
        data = self.base(); data["speach"] = {}
        with self.assertRaisesRegex(profile_mod.ProfileError, "unknown key: speach"):
            profile_mod.load(self.write(data))

    def test_monolingual_voice_is_rejected_with_reason(self):
        data = self.base(); data["language"] = "de-DE"; data["speech"]["voice_languages"] = ["de-DE"]
        with self.assertRaisesRegex(profile_mod.ProfileError, "multilingual.*en"):
            profile_mod.load(self.write(data))
        data["speech"]["voice_languages"] = ["en-US"]
        with self.assertRaisesRegex(profile_mod.ProfileError, "lacks de"):
            profile_mod.load(self.write(data))

    def test_values_that_reach_a_shell_are_validated(self):
        data = self.base(); data["loudness"]["lufs"] = "-16; rm -rf ~"
        with self.assertRaisesRegex(profile_mod.ProfileError, "loudness.lufs must be a number"):
            profile_mod.load(self.write(data))
        data = self.base(); data["render"]["remote_dir"] = "render/$(id)"
        with self.assertRaisesRegex(profile_mod.ProfileError, "render.remote_dir"):
            profile_mod.load(self.write(data))
        folder = self.write(self.base())
        video = json.loads((TEMPLATE / "video.json").read_text())
        for bad in ("x'; id", "Sample Video", "$(id)"):
            (folder / "video.json").write_text(json.dumps({**video, "id": bad}))
            with self.assertRaisesRegex(profile_mod.ProfileError, "id may contain only"):
                profile_mod.load_video(folder)

    def test_pause_between_lines_can_never_be_zero(self):
        data = self.base(); data["pause"]["line"] = 0
        with self.assertRaisesRegex(profile_mod.ProfileError, "greater than zero"):
            profile_mod.load(self.write(data))


class Pronunciation(unittest.TestCase):
    def lists(self, *contents):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder)
        paths = []
        for i, content in enumerate(contents):
            path = folder / f"{i}.json"
            path.write_text(json.dumps(content))
            paths.append(path)
        return paths

    def test_one_entry_applies_to_every_occurrence(self):
        entries = speech.load_pronunciation(*self.lists([{"term": "IT", "speak": "I T"}]))
        line = {"text": "Die IT hilft. Frag die IT, nicht ITler."}
        self.assertEqual("Die I T hilft. Frag die I T, nicht ITler.", speech.spoken_plain(line, entries))

    def test_markup_for_phonetic_and_language_entries_is_escaped(self):
        entries = speech.load_pronunciation(*self.lists([
            {"term": "Tresor", "ipa": "tʁeˈzoːɐ̯", "key": True}, {"term": "Commit", "lang": "en-US"}]))
        body = speech.spoken_ssml({"text": "Der Tresor & ein `Commit` < fertig"}, entries)
        self.assertIn('<phoneme alphabet="ipa" ph="tʁeˈzoːɐ̯">Tresor</phoneme>', body)
        self.assertIn('<lang xml:lang="en-US">Commit</lang>', body)
        self.assertIn("&amp;", body); self.assertIn("&lt;", body); self.assertNotIn("`", body)
        self.assertEqual(["Tresor"], speech.key_terms(entries))

    def test_project_and_video_lists_merge_and_conflicts_fail(self):
        a, b = self.lists([{"term": "IT", "speak": "I T"}], [{"term": "ORSY", "speak": "Orsi"}])
        self.assertEqual({"IT", "ORSY"}, {e["term"] for e in speech.load_pronunciation(a, b)})
        a, b = self.lists([{"term": "IT", "speak": "I T"}], [{"term": "IT", "speak": "Eitie"}])
        with self.assertRaisesRegex(speech.PronunciationError, "conflicting"):
            speech.load_pronunciation(a, b)

    def test_hash_changes_with_text_pronunciation_voice_and_settings(self):
        line = {"text": "Der Tresor ist offen."}
        def prof(language="de-DE", voice="v", settings=None):
            return {"language": language, "speech": {"voice": voice, "settings": settings or {}}}
        base = speech.text_hash(line, [], prof())
        self.assertEqual(base, speech.text_hash(dict(line), [], prof()))
        self.assertNotEqual(base, speech.text_hash({"text": "Der Tresor ist zu."}, [], prof()))
        self.assertNotEqual(base, speech.text_hash(line, [{"term": "Tresor", "speak": "Tre-sor"}], prof()))
        self.assertNotEqual(base, speech.text_hash(line, [], prof(voice="w")))
        self.assertNotEqual(base, speech.text_hash(line, [], prof(settings={"rate": "+10%"})))
        self.assertNotEqual(base, speech.text_hash(line, [], prof(language="de-AT")))

    def test_scene_file_pattern_does_not_claim_a_scene_with_the_same_prefix(self):
        own = speech.scene_file("setup")
        self.assertTrue(own.fullmatch("setup-00-0123456789.mp3"))
        self.assertFalse(own.fullmatch("setup-check-00-0123456789.mp3"))
        self.assertFalse(own.fullmatch("setup-00-0123456789.mp3.part"))


class ScriptCheck(unittest.TestCase):
    def run_check(self, mutate=None):
        prof, video, scenes, narration, script = sample()
        state = {"prof": copy.deepcopy(prof), "video": video, "scenes": scenes, "narration": narration, "script": script}
        if mutate:
            mutate(state)
        return check_script.check(state["video"], state["scenes"], state["narration"], state["script"], state["prof"], [])

    def test_sample_script_passes(self):
        self.assertEqual(set(), rules(self.run_check()))

    def test_two_audiences_need_two_scripts(self):
        def two(s): s["video"]["audience"] = ["staff", "IT"]
        self.assertIn("audience", rules(self.run_check(two)))

    def test_scene_without_message_or_source_is_reported_with_scene(self):
        def strip(s):
            s["scenes"][1].pop("message"); s["scenes"][1].pop("sources")
        findings = self.run_check(strip)
        self.assertLessEqual({"message", "sources"}, rules(findings))
        self.assertTrue(all(f["scene"] == "steps" for f in findings if f["rule"] in ("message", "sources")))

    def test_unlisted_source_and_missing_source_table(self):
        def bad(s): s["scenes"][1]["sources"] = ["S9"]
        self.assertIn("sources", rules(self.run_check(bad)))
        def none(s): s["script"] = s["script"].replace("| S1 |", "| x |")
        self.assertIn("sources", rules(self.run_check(none)))

    def test_long_line_is_an_error_and_long_sentence_a_warning(self):
        def long(s): s["narration"]["steps"][0]["text"] = " ".join(["word"] * 29) + "."
        findings = self.run_check(long)
        hit = next(f for f in findings if f["rule"] == "line-length")
        self.assertEqual(("steps", 0), (hit["scene"], hit["line"]))
        self.assertIn("sentence-length", rules(findings, "warning"))

    def test_caption_and_speech_must_keep_the_same_meaning(self):
        def spell(s): s["narration"]["intro"][1]["speak"] = "Nothing here is filmed. Every picture is drawn from a skript."
        self.assertNotIn("caption-speech", rules(self.run_check(spell)))
        def differ(s): s["narration"]["intro"][1]["speak"] = "Please subscribe to our channel today."
        self.assertIn("caption-speech", rules(self.run_check(differ)))

    def test_abbreviation_without_spoken_form_is_a_warning(self):
        def abbr(s): s["narration"]["intro"][1]["text"] = "Ask the IT team."
        self.assertIn("speakable", rules(self.run_check(abbr), "warning"))

    def test_number_not_written_as_spoken_is_a_warning(self):
        def number(s): s["narration"]["intro"][1]["text"] = "The video lasts 8:54 min."
        self.assertIn("speakable", rules(self.run_check(number), "warning"))
        def spoken(s): s["narration"]["intro"][1].update(text="The video lasts 8:54 min.", speak="The video lasts about nine minutes.")
        self.assertNotIn("speakable", rules(self.run_check(spoken), "warning"))

    def test_scene_key_must_be_safe_for_file_names(self):
        def key(s):
            s["scenes"][1]["key"] = "Steps-2"; s["narration"]["Steps-2"] = s["narration"].pop("steps")
        self.assertIn("scenes", rules(self.run_check(key)))

    def test_secrets_never_reach_narration(self):
        def leak(s): s["narration"]["intro"][1]["text"] = "Use password: hunter2secret to sign in."
        self.assertIn("secret", rules(self.run_check(leak)))

    def test_recreated_interfaces_need_notice_and_evidence_list(self):
        def recreated(s): s["video"]["recreated"] = True
        self.assertIn("notice", rules(self.run_check(recreated)))
        def noticed(s):
            s["video"]["recreated"] = True; s["narration"]["intro"][1]["notice"] = True
        self.assertNotIn("notice", rules(self.run_check(noticed)))
        def unlisted(s):
            noticed(s); s["script"] = s["script"].split("## Evidenced")[0]
        self.assertIn("evidence-list", rules(self.run_check(unlisted)))

    def test_length_is_only_reported_above_the_maximum_with_a_split(self):
        self.assertNotIn("length", rules(self.run_check()) | rules(self.run_check(), "warning"))
        def tiny(s): s["prof"]["script"]["max_minutes"] = 0.2
        hit = next(f for f in self.run_check(tiny) if f["rule"] == "length")
        self.assertEqual("error", hit["severity"])
        self.assertRegex(hit["message"], r"split before chapter '(The four steps|Next)'")

    def test_narration_without_scene_entry_is_reported(self):
        def orphan(s): s["narration"]["extra"] = [{"text": "Hello."}]
        self.assertIn("scenes", rules(self.run_check(orphan)))

    @staticmethod
    def as_story(s):
        s["video"].update(purpose="story", edition="verbatim", story_id="sample-story",
                          based_on=[{"chapter_id": "ch-01", "revision": "r3"}])
        for scene in s["scenes"]:
            scene.pop("sources", None); scene.pop("no_claims", None)
        s["script"] = s["script"].replace("| S1 |", "| x |")

    def test_story_script_passes_without_sources(self):
        self.assertEqual([], self.run_check(self.as_story))
        def listening(s):
            self.as_story(s); s["video"]["edition"] = "listening"
        self.assertEqual([], self.run_check(listening))

    def test_story_script_must_name_edition_and_manuscript_revision(self):
        def no_edition(s):
            self.as_story(s); s["video"].pop("edition")
        self.assertEqual({"edition"}, rules(self.run_check(no_edition)))
        def other_edition(s):
            self.as_story(s); s["video"]["edition"] = "abridged"
        self.assertEqual({"edition"}, rules(self.run_check(other_edition)))
        for bad in (None, [], "ch-01", [{"chapter_id": "ch-01"}], [{"chapter_id": "ch-01", "revision": "r3"}, {"revision": "r3"}]):
            def based(s, bad=bad):
                self.as_story(s); s["video"]["based_on"] = bad
            with self.subTest(based_on=bad):
                self.assertEqual({"based-on"}, rules(self.run_check(based)))

    def test_story_sentence_length_is_the_authors_choice_but_lines_stay_limited(self):
        def long_sentence(s):
            self.as_story(s); s["narration"]["steps"][0]["text"] = " ".join(["word"] * 27) + "."
        self.assertEqual([], self.run_check(long_sentence))
        def long_line(s):
            self.as_story(s); s["narration"]["steps"][0]["text"] = " ".join(["word"] * 29) + "."
        findings = self.run_check(long_line)
        self.assertEqual({"line-length"}, rules(findings))
        self.assertEqual(set(), rules(findings, "warning"))

    def test_story_script_keeps_the_other_checks(self):
        def broken(s):
            self.as_story(s)
            s["video"].update(audience=["listeners", "pupils"], recreated=True)
            s["scenes"][1].pop("message")
            s["narration"]["intro"][1]["text"] = "Use password: hunter2secret to sign in."
            s["narration"]["close"][0].update(text="Ask the IT team.", speak="Please subscribe to our channel today.")
            s["narration"]["steps"][1]["text"] = "Ask the IT team."
            s["prof"]["script"]["max_minutes"] = 0.2
        findings = self.run_check(broken)
        self.assertEqual({"audience", "message", "secret", "caption-speech", "notice", "length"}, rules(findings))
        self.assertEqual({"speakable"}, rules(findings, "warning"))

    def test_tutorial_behaviour_is_unchanged_by_the_purpose_field(self):
        def defects(s):
            s["scenes"][1].pop("sources"); s["scenes"][2]["sources"] = ["S9"]
            s["narration"]["steps"][0]["text"] = " ".join(["word"] * 27) + "."
            s["script"] = s["script"].replace("| S1 |", "| x |")
        def named(s):
            defects(s); s["video"]["purpose"] = "tutorial"
        plain = self.run_check(defects)
        self.assertEqual({"sources"}, rules(plain))
        self.assertEqual({"sentence-length"}, rules(plain, "warning"))
        self.assertEqual(3, sum(f["rule"] == "sources" for f in plain))
        self.assertEqual(plain, self.run_check(named))
        # the story fields alone change nothing: only the purpose switches the rules
        def fields_only(s):
            defects(s); s["video"].update(edition="verbatim", based_on=[{"chapter_id": "ch-01", "revision": "r3"}])
        self.assertEqual(plain, self.run_check(fields_only))

    def test_unknown_purpose_is_an_error(self):
        def marketing(s): s["video"]["purpose"] = "marketing"
        findings = self.run_check(marketing)
        self.assertEqual({"purpose"}, rules(findings))
        def story_like(s):
            self.as_story(s); s["video"]["purpose"] = "Story"
        self.assertLessEqual({"purpose", "sources"}, rules(self.run_check(story_like)))

    def test_video_file_accepts_the_story_fields_and_still_rejects_unknown_keys(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder)
        video = json.loads((TEMPLATE / "video.json").read_text())
        story = {**video, "purpose": "story", "edition": "listening", "story_id": "sample-story",
                 "based_on": [{"chapter_id": "ch-01", "revision": "r3"}]}
        (folder / "video.json").write_text(json.dumps(story))
        self.assertEqual(story, profile_mod.load_video(folder))
        (folder / "video.json").write_text(json.dumps({**story, "editon": "verbatim"}))
        with self.assertRaisesRegex(profile_mod.ProfileError, "unknown key in video.json: editon"):
            profile_mod.load_video(folder)


class Credentials(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, self.dir)

    def test_missing_file_and_empty_variable_are_named_without_the_key(self):
        with self.assertRaisesRegex(voice_azure.CredentialError, "not found"):
            voice_azure.load_credentials(self.dir / "none.env")
        path = self.dir / "a.env"
        path.write_text("# comment\nAZURE_SPEECH_KEY=topsecretvalue123\nAZURE_SPEECH_REGION=\n")
        with self.assertRaises(voice_azure.CredentialError) as caught:
            voice_azure.load_credentials(path)
        self.assertIn("AZURE_SPEECH_REGION", str(caught.exception))
        self.assertNotIn("topsecretvalue123", str(caught.exception))

    def test_env_file_is_found_upward_or_named_explicitly(self):
        (self.dir / "env").mkdir(); (self.dir / "env" / "azure-speech.env").write_text("x")
        deep = self.dir / "videos" / "one"; deep.mkdir(parents=True)
        self.assertEqual(self.dir / "env" / "azure-speech.env", voice_azure.find_env(deep, None, {}))
        self.assertEqual(Path("/somewhere/else.env"), voice_azure.find_env(deep, "/somewhere/else.env", {}))
        self.assertEqual(Path("/from/profile.env"), voice_azure.find_env(deep, None, {"env_file": "/from/profile.env"}))

    def test_voice_lookup_is_exact_never_a_name_that_only_starts_the_same(self):
        voices = [{"ShortName": "de-DE-AnnaNeural", "Locale": "de-DE"},
                  {"ShortName": "de-DE-Anna:HD-2", "Locale": "de-DE", "SecondaryLocaleList": ["en-US"]}]
        self.assertEqual(["en-US"], voice_azure.find_voice(voices, "de-DE-Anna:HD-2")["SecondaryLocaleList"])
        self.assertIsNone(voice_azure.find_voice(voices, "de-DE-Anna"))

    def test_no_env_file_explains_how_to_create_one(self):
        with self.assertRaisesRegex(voice_azure.CredentialError, "azure-speech.env.example"):
            voice_azure.find_env(self.dir, None, {})


class Voicing(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, self.dir)
        self.prof = profile_mod.load(TEMPLATE, PROFILE)
        self.narration = {"a": [{"text": "One."}, {"text": "Two."}], "b": [{"text": "Three."}]}
        self.calls = []

    def synth(self, document):
        self.calls.append(document)
        return b"sound:" + document.encode()

    def run_voice(self, narration=None, synth=None, **kw):
        return voice_azure.voice(narration or self.narration, [], self.prof, self.dir, synth or self.synth,
                                 measure=lambda p: {"duration": 1.0, "lead_silence": 0.0, "trail_silence": 0.3},
                                 sleep=lambda s: None, report=lambda m: None, **kw)

    def test_one_file_per_line_and_no_request_for_unchanged_input(self):
        first = self.run_voice()
        self.assertEqual(3, first["new"]); self.assertEqual(3, len(list(self.dir.glob("*.mp3"))))
        self.assertEqual(len("One.Two.Three."), first["characters"])
        second = self.run_voice()
        self.assertEqual((0, 3), (second["new"], len(self.calls)))
        self.assertEqual(first["manifest"], second["manifest"])
        self.assertEqual({"file", "hash", "words", "duration", "lead_silence", "trail_silence"},
                         set(first["manifest"]["a"][0]))

    def test_one_changed_line_costs_one_request_and_removes_the_stale_file(self):
        self.run_voice()
        changed = copy.deepcopy(self.narration); changed["a"][1]["text"] = "Two, corrected."
        result = self.run_voice(changed)
        self.assertEqual(1, result["new"]); self.assertEqual(4, len(self.calls))
        self.assertEqual(3, len(list(self.dir.glob("*.mp3"))))

    def test_foreign_files_in_the_audio_folder_are_left_alone(self):
        (self.dir / "jingle.mp3").write_bytes(b"x")
        self.run_voice()
        self.assertTrue((self.dir / "jingle.mp3").exists())

    def test_rate_limit_waits_then_continues(self):
        waits, state = [], {"n": 0}
        def flaky(document):
            state["n"] += 1
            if state["n"] in (1, 2):
                raise voice_azure.RateLimited(7)
            return b"ok"
        result = voice_azure.voice(self.narration, [], self.prof, self.dir, flaky,
                                   measure=lambda p: {"duration": 1.0}, sleep=waits.append, report=lambda m: None)
        self.assertEqual(3, result["new"]); self.assertEqual([7, 7], waits)

    def test_spent_retry_budget_stops_keeps_files_and_reports_the_line(self):
        self.prof["speech"]["retry_budget"] = 2
        state = {"n": 0}
        def limited(document):
            state["n"] += 1
            if state["n"] > 1:
                raise voice_azure.RateLimited(1)
            return b"ok"
        with self.assertRaisesRegex(voice_azure.ProviderError, r"stopped at a:1 after 1 new line.*kept"):
            self.run_voice(synth=limited)
        self.assertEqual(1, len(list(self.dir.glob("*.mp3"))))

    def test_interrupted_write_leaves_no_file_that_would_be_reused(self):
        def boom(document):
            raise voice_azure.ProviderError("connection lost")
        with self.assertRaises(voice_azure.ProviderError):
            self.run_voice(synth=boom)
        self.assertEqual([], list(self.dir.glob("*.mp3")) + list(self.dir.glob("*.part")))
        self.run_voice()
        self.assertEqual([], list(self.dir.glob("*.part")))

    def test_only_rejects_unknown_lines_and_malformed_values(self):
        with self.assertRaisesRegex(voice_azure.ProviderError, "no such narration line: zz:0"):
            self.run_voice(only={("zz", 0)})
        with self.assertRaisesRegex(voice_azure.ProviderError, "scene:index"):
            voice_azure.parse_only("intro")
        self.assertEqual({("a", 0), ("b", 3)}, voice_azure.parse_only("a:0, b:3"))

    def test_only_selected_lines_are_voiced_and_nothing_is_removed(self):
        self.run_voice()
        changed = copy.deepcopy(self.narration); changed["b"][0]["text"] = "Three, new."
        result = self.run_voice(changed, only={("b", 0)})
        self.assertEqual(1, result["new"]); self.assertEqual(4, len(list(self.dir.glob("*.mp3"))))

    def test_document_carries_voice_language_and_only_effective_rate(self):
        doc = voice_azure.ssml_document("Hi", "voice-x", "de-DE", {})
        self.assertIn('xml:lang="de-DE"', doc); self.assertIn('name="voice-x"', doc); self.assertNotIn("prosody", doc)
        self.assertIn('<prosody rate="+20%">', voice_azure.ssml_document("Hi", "v", "de-DE", {"rate": "+20%"}))


def manifest_for(narration, duration=2.0, lead=0.0, trail=0.0):
    return {k: [{"file": f"audio/{k}-{i}.mp3", "duration": duration, "lead_silence": lead,
                 "trail_silence": trail, "words": project.words(l["text"])} for i, l in enumerate(ls)]
            for k, ls in narration.items()}


class Timeline(unittest.TestCase):
    def setUp(self):
        self.prof, _, self.scenes, self.narration, _ = sample()

    def test_audible_pause_equals_the_profile_value_despite_file_silence(self):
        for lead, trail in ((0.0, 0.0), (0.02, 0.31), (0.05, 0.09)):
            tl = timeline.build(self.scenes, self.narration, manifest_for(self.narration, 2.0, lead, trail), self.prof)
            lines = tl["scenes"][1]["lines"]
            for a, b in zip(lines, lines[1:]):
                self.assertAlmostEqual(0.65, b["speech_start"] - a["speech_end"], places=2)
            self.assertAlmostEqual(0.5, lines[0]["speech_start"], places=2)

    def test_minimum_display_time_extends_the_slot_and_shifts_later_lines(self):
        plain = copy.deepcopy(self.narration); plain["intro"][0].pop("min")
        short = timeline.build(self.scenes, plain, manifest_for(plain, 1.0), self.prof)["scenes"][0]["lines"]
        long = timeline.build(self.scenes, self.narration, manifest_for(self.narration, 1.0), self.prof)["scenes"][0]["lines"]
        self.assertGreaterEqual(long[0]["slot"], 3.0)
        self.assertGreater(long[1]["at"], short[1]["at"])

    def test_scene_ends_after_the_scene_pause_and_frames_do_not_drift(self):
        tl = timeline.build(self.scenes, self.narration, manifest_for(self.narration, 2.0, 0, 0.3), self.prof)
        first = tl["scenes"][0]
        self.assertAlmostEqual(first["lines"][-1]["speech_end"] + 1.0, first["length"], delta=1 / 30)
        self.assertEqual(tl["total_frames"], sum(s["frames"] for s in tl["scenes"]))
        self.assertEqual(tl["scenes"][2]["start_frame"], tl["scenes"][0]["frames"] + tl["scenes"][1]["frames"])

    def test_picture_limits_of_the_profile_reach_the_composition(self):
        self.prof["picture"] = {"width": 1280, "height": 720, "fps": 30, "min_font_px": 24, "margin_px": 40}
        tl = timeline.build(self.scenes, self.narration, manifest_for(self.narration), self.prof)
        self.assertEqual(self.prof["picture"], tl["picture"])
        theme = (TEMPLATE / "src" / "theme.ts").read_text()
        for constant in ("picture.width", "picture.height", "picture.min_font_px", "picture.margin_px"):
            self.assertIn(constant, theme)
        for component in ("Caption.tsx", "SceneFrame.tsx"):
            self.assertNotRegex((TEMPLATE / "src" / "components" / component).read_text(), r"(top|bottom): \d+,")

    def test_chapter_marks_start_with_their_first_scene(self):
        tl = timeline.build(self.scenes, self.narration, manifest_for(self.narration), self.prof)
        self.assertEqual(["Start", "The four steps", "Next"], [c["title"] for c in tl["chapters"]])
        self.assertEqual([s["start"] for s in tl["scenes"]], [c["start"] for c in tl["chapters"]])

    def test_missing_or_stale_sound_is_refused(self):
        manifest = manifest_for(self.narration); manifest["steps"].pop()
        with self.assertRaisesRegex(timeline.StaleManifest, "steps"):
            timeline.build(self.scenes, self.narration, manifest, self.prof)
        manifest = manifest_for(self.narration)
        for sounds in manifest.values():
            for s in sounds: s["hash"] = "old"
        with self.assertRaisesRegex(timeline.StaleManifest, "text changed"):
            timeline.build(self.scenes, self.narration, manifest, self.prof,
                           timeline.current_hashes(self.narration, [], self.prof))

    def test_captions_follow_the_timeline_and_skip_hidden_lines(self):
        narration = copy.deepcopy(self.narration); narration["intro"][1]["show"] = False
        tl = timeline.build(self.scenes, narration, manifest_for(narration), self.prof)
        vtt = timeline.captions(tl, offset=7.0)
        self.assertTrue(vtt.startswith("WEBVTT"))
        self.assertEqual(sum(len(v) for v in narration.values()) - 1, vtt.count("-->"))
        self.assertNotIn("Nothing here is filmed", vtt)
        first = tl["scenes"][0]["lines"][0]
        self.assertIn(timeline._stamp(7.0 + first["at"]) + " -->", vtt)
        self.assertEqual("0:07 Start", timeline.chapter_list(tl, 7.0).splitlines()[0])


class Measurements(unittest.TestCase):
    def setUp(self):
        self.prof, _, self.scenes, self.narration, _ = sample()

    def test_pace_is_measured_on_pure_speech_and_compared_with_the_range(self):
        manifest = {"ok": [{"duration": 30.6, "lead_silence": 0.1, "trail_silence": 0.5, "words": 65}],
                    "slow": [{"duration": 30.0, "lead_silence": 0, "trail_silence": 0, "words": 40}],
                    "fast": [{"duration": 30.0, "lead_silence": 0, "trail_silence": 0, "words": 90}],
                    "tiny": [{"duration": 1.0, "lead_silence": 0, "trail_silence": 0, "words": 9}]}
        self.prof["pace_wpm"] = [120, 155]
        rows = {r["scene"]: r for r in measure.pace(manifest, self.prof)}
        self.assertEqual(130.0, rows["ok"]["wpm"])
        self.assertEqual([True, False, False, True], [rows[k]["ok"] for k in ("ok", "slow", "fast", "tiny")])

    def test_file_check_blocks_on_each_deviation(self):
        good = {"width": 1920, "height": 1080, "fps": 30.0, "duration": 60.2, "has_audio": True}
        loud = {"lufs": -16.4, "true_peak": -1.8}
        self.assertTrue(all(r["ok"] for r in measure.file_check(good, loud, self.prof, 60.0)))
        cases = [({**good, "width": 1280, "height": 720}, loud, "resolution"), ({**good, "fps": 25.0}, loud, "frame rate"),
                 (good, {"lufs": -23.0, "true_peak": -1.8}, "loudness (LUFS)"), (good, {"lufs": -16.0, "true_peak": -0.2}, "true peak (dBTP)"),
                 ({**good, "duration": 55.0}, loud, "duration (s)"), ({**good, "has_audio": False}, loud, "sound track")]
        self.assertTrue(all(r["ok"] for r in measure.file_check(good, {"lufs": -16.0, "true_peak": -1.45}, self.prof, 60.0)))
        for props, level, what in cases:
            failed = [r["what"] for r in measure.file_check(props, level, self.prof, 60.0) if not r["ok"]]
            self.assertEqual([what], failed)

    def test_pause_check_matches_gaps_and_rejects_long_missing_or_zero(self):
        tl = timeline.build(self.scenes, self.narration, manifest_for(self.narration, 2.0, 0.02, 0.3), self.prof)
        expected = measure.expected_pauses(tl, offset=5.0)
        self.assertEqual(sum(len(v) - 1 for v in self.narration.values()), len(expected))
        exact = [(g["start"], g["end"]) for g in expected]
        self.assertTrue(all(r["ok"] for r in measure.pause_check(expected, exact, 0.15)))
        long = [(g["start"] - 0.3, g["end"] + 0.3) for g in expected]
        self.assertFalse(any(r["ok"] for r in measure.pause_check(expected, long, 0.15)))
        rows = measure.pause_check(expected, exact[1:], 0.15)
        self.assertEqual((False, 0.0), (rows[0]["ok"], rows[0]["measured"]))

    def test_setting_counts_only_beyond_the_spread_of_identical_runs(self):
        # measured on a real voice: +7 % inside the spread, +25 % beyond it
        self.assertFalse(probe_settings.judge([8.04, 7.13], [7.54, 7.60])["effective"])
        strong = probe_settings.judge([8.04, 7.13], [5.86, 5.90])
        self.assertTrue(strong["effective"]); self.assertLess(strong["change_percent"], -20)


class ReadBack(unittest.TestCase):
    def test_key_term_must_be_heard_where_the_caption_has_it(self):
        line = {"text": "Öffnen Sie den Tresor und wählen Sie Ihren Ordner."}
        good = "Öffnen Sie den Tresor und wählen Sie Ihren Ordner.".split()
        bad = "Öffnen Sie den Trezor und wählen Sie Ihren Ordner.".split()
        key = [{"term": "Tresor", "key": True}, {"term": "Ordner"}]
        self.assertTrue(verify_speech.verify_line(line, good, key, 0.8)["ok"])
        result = verify_speech.verify_line(line, bad, key, 0.8)
        self.assertEqual((False, ["Tresor"]), (result["ok"], result["missing_terms"]))
        self.assertTrue(verify_speech.verify_line({"text": "Guten Tag."}, ["Guten", "Tag."], key, 0.8)["ok"])

    def test_short_term_is_matched_as_a_whole_word_not_inside_another(self):
        key = [{"term": "IT", "key": True}]
        line = {"text": "Die IT hilft mit allem."}
        wrong = verify_speech.verify_line(line, "Die Ei hilft mit allem.".split(), key, 0.5)
        self.assertEqual(["IT"], wrong["missing_terms"])
        self.assertTrue(verify_speech.verify_line(line, "Die IT hilft mit allem.".split(), key, 0.5)["ok"])

    def test_respelled_term_passes_in_either_recognized_form(self):
        key = [{"term": "IT", "speak": "I T", "key": True}]
        line = {"text": "Die IT hilft mit allem."}
        for heard in ("Die I T hilft mit allem.", "Die IT hilft mit allem.", "Die I.T. hilft mit allem."):
            self.assertEqual([], verify_speech.verify_line(line, heard.split(), key, 0.5)["missing_terms"], heard)

    def test_garbled_line_fails_on_similarity_alone(self):
        line = {"text": "Then each sentence is voiced, and its length is measured."}
        self.assertFalse(verify_speech.verify_line(line, "completely different words here".split(), [], 0.8)["ok"])

    def test_transcribe_command_keeps_a_path_with_spaces_as_one_argument(self):
        folder = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, folder)
        sound = folder / "my video" / "line one.mp3"; sound.parent.mkdir(); sound.write_bytes(b"x")
        writer = folder / "t.py"
        writer.write_text("import sys, pathlib\nassert len(sys.argv) == 2, sys.argv\n"
                          "pathlib.Path(sys.argv[1]).with_suffix('.words.json').write_text('[]')\n")
        verify_speech.transcribe(sound, f"{sys.executable} {writer} {{audio}}")
        self.assertTrue(verify_speech.words_file(sound).is_file())

    def test_samples_pick_the_first_line_of_each_key_term(self):
        narration = {"a": [{"text": "Hello."}, {"text": "Der Tresor."}], "b": [{"text": "Tresor und Commit."}]}
        self.assertEqual({"Tresor": ("a", 1), "Commit": ("b", 0)}, verify_speech.samples(narration, ["Tresor", "Commit", "Unused"]))


def words_for(sentences, gap=0.5, per_word=0.3):
    out, t = [], 0.0
    for sentence in sentences:
        for w in sentence.split():
            out.append({"word": w, "start": round(t, 2), "end": round(t + per_word, 2)}); t += per_word
        t += gap
    return out, t


class TakeSplitting(unittest.TestCase):
    SPOKEN = ["First you write the script.", "Then each sentence is voiced.", "Last, the video is rendered."]

    def test_cuts_fall_into_the_pause_after_each_line(self):
        words, total = words_for(self.SPOKEN)
        parts = split_takes.cuts(self.SPOKEN, words, total)
        self.assertEqual(3, len(parts)); self.assertEqual(0.0, parts[0][0]); self.assertEqual(total, parts[-1][1])
        end_first = [w for w in words if w["word"] == "script."][0]["end"]
        self.assertTrue(end_first < parts[0][1] < end_first + 0.5)

    def test_take_with_a_skipped_sentence_is_rejected(self):
        full, _ = words_for(self.SPOKEN)
        skipped, _ = words_for([self.SPOKEN[0], self.SPOKEN[2]])
        self.assertGreater(split_takes.score(self.SPOKEN, full), 0.99)
        with self.assertRaisesRegex(split_takes.TakeRejected, "request a new take"):
            split_takes.choose(self.SPOKEN, [(Path("a-take1.mp3"), skipped)], 0.9)
        ratio, path, _ = split_takes.choose(self.SPOKEN, [(Path("a-take1.mp3"), skipped), (Path("a-take2.mp3"), full)], 0.9)
        self.assertEqual("a-take2.mp3", path.name)

    def test_take_that_drops_the_short_last_line_is_rejected_not_crashed(self):
        spoken = self.SPOKEN + ["Bye now."]
        words, total = words_for(self.SPOKEN)
        self.assertGreater(split_takes.score(spoken, words), 0.9)   # the overall score alone would accept it
        with self.assertRaisesRegex(split_takes.TakeRejected, "line 3 was not heard"):
            split_takes.cuts(spoken, words, total)

    def test_prompt_is_one_line_per_narration_line_with_one_tone_tag(self):
        lines = [{"text": "Die IT hilft."}, {"text": "Danke!"}]
        text = split_takes.prompt(lines, [{"term": "IT", "speak": "I T"}], "[warm]")
        self.assertEqual("[warm] Die I T hilft.\nDanke!", text)


@unittest.skipUnless(FFMPEG, "ffmpeg and ffprobe are required")
class WithMediaTools(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, self.dir)

    def tone(self, name, parts, volume=0.5):
        """parts: [('tone'|'silence', seconds), ...] -> sound file"""
        inputs, labels = [], []
        for i, (kind, seconds) in enumerate(parts):
            source = f"sine=frequency=440:sample_rate=48000:duration={seconds}" if kind == "tone" \
                else f"anullsrc=r=48000:cl=mono:d={seconds}"
            inputs += ["-f", "lavfi", "-i", source]; labels.append(f"[{i}:a]")
        path = self.dir / name
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex",
                        "".join(labels) + f"concat=n={len(parts)}:v=0:a=1,volume={volume}[a]", "-map", "[a]", str(path)], check=True)
        return path

    def test_edge_silence_of_a_sound_file_is_measured(self):
        path = self.tone("line.wav", [("silence", 0.2), ("tone", 1.0), ("silence", 0.3)])
        lead, trail = audio.edge_silence(path)
        self.assertAlmostEqual(0.2, lead, delta=0.03); self.assertAlmostEqual(0.3, trail, delta=0.03)
        self.assertAlmostEqual(1.5, audio.duration(path), delta=0.02)

    def test_rendered_pause_is_compared_with_the_timeline(self):
        path = self.tone("mix.wav", [("tone", 1.0), ("silence", 0.65), ("tone", 1.0), ("silence", 1.3), ("tone", 1.0)])
        expected = [{"scene": "a", "line": 0, "start": 1.0, "end": 1.65, "expected": 0.65},
                    {"scene": "a", "line": 1, "start": 2.65, "end": 3.30, "expected": 0.65}]
        rows = measure.pause_check(expected, audio.silences(path, min_len=0.2), 0.15)
        self.assertEqual([True, False], [r["ok"] for r in rows])
        self.assertAlmostEqual(1.3, rows[1]["measured"], delta=0.05)

    def test_quiet_file_fails_the_delivery_check(self):
        prof = profile_mod.load(TEMPLATE, PROFILE)
        quiet = self.dir / "quiet.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:r=30:d=4",
                        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4", "-af", "volume=0.02",
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", str(quiet)], check=True)
        rows = measure.file_check(audio.video_properties(quiet), audio.loudness(quiet), prof, 4.0)
        failed = [r["what"] for r in rows if not r["ok"]]
        self.assertEqual(["loudness (LUFS)"], failed)


class ReviewGate(unittest.TestCase):
    def setUp(self):
        prof, _, scenes, narration, _ = sample()
        self.timeline = timeline.build(scenes, narration, manifest_for(narration), prof)
        self.stills = [{"file": f"{s['key']}-{i:02d}.png", "inspected": True, "finding": None}
                       for s in self.timeline["scenes"] for i in range(len(s["lines"]))]

    def test_gate_stays_open_until_every_current_still_is_inspected(self):
        self.assertEqual([], check_review.check(self.timeline, self.stills))
        self.stills[2]["inspected"] = False
        self.assertEqual(["steps-00.png: not inspected"], check_review.check(self.timeline, self.stills))
        self.stills[2]["inspected"] = "yes"
        self.assertEqual(1, len(check_review.check(self.timeline, self.stills)))

    def test_missing_still_open_finding_and_draft_keep_the_gate_open(self):
        self.assertEqual(["intro-00.png: no still rendered"], check_review.check(self.timeline, self.stills[1:]))
        self.stills[0]["finding"] = "arrow missing"
        self.assertIn("open finding: arrow missing", check_review.check(self.timeline, self.stills)[0])
        self.stills[0]["finding"] = None
        self.assertTrue(check_review.check({**self.timeline, "draft": True}, self.stills))


class SeededDefects(unittest.TestCase):
    """US-003: the planted defects are found; the fifth is visual by design."""
    DEFECTS = ROOT / "tests" / "fixtures" / "presentation-video" / "defects"

    def findings(self):
        prof = profile_mod.load(TEMPLATE, PROFILE)
        return check_script.check(json.loads((self.DEFECTS / "video.json").read_text()),
                                  project.load_scenes(self.DEFECTS), project.load_narration(self.DEFECTS),
                                  (self.DEFECTS / "script" / "script.md").read_text(), prof, [])

    def test_three_script_defects_are_reported_with_their_place(self):
        found = {(f["rule"], f["scene"], f["line"]) for f in self.findings() if f["severity"] == "error"}
        self.assertEqual({("caption-speech", "open", 1), ("sources", "sync", None), ("notice", None, None)}, found)

    def test_fourth_defect_is_a_loudness_failure_of_the_file(self):
        prof = profile_mod.load(TEMPLATE, PROFILE)
        props = {"width": 1920, "height": 1080, "fps": 30.0, "duration": 10.0, "has_audio": True}
        rows = measure.file_check(props, {"lufs": -27.5, "true_peak": -9.0}, prof, 10.0)
        self.assertEqual(["loudness (LUFS)"], [r["what"] for r in rows if not r["ok"]])

    def test_fifth_defect_is_documented_as_a_visual_check(self):
        readme = (self.DEFECTS / "README.md").read_text()
        self.assertIn("no tool reports it", readme)
        self.assertIn("\u2192", project.load_narration(self.DEFECTS)["open"][0]["text"])
        review = (ROOT / "skills" / "presentation-video-review" / "SKILL.md").read_text()
        self.assertIn("missing characters", review)


class RepositoryRules(unittest.TestCase):
    OWNED = ["skills/tutorial-video-scripting", "skills/presentation-video-production", "skills/presentation-video-review",
             "shared/media", "templates/presentation-video", "env"]

    def texts(self):
        for folder in self.OWNED:
            for path in sorted((ROOT / folder).rglob("*")):
                if path.is_file() and "node_modules" not in path.parts and path.suffix != ".mp3":
                    yield path, path.read_text(errors="replace")

    def test_credential_examples_hold_names_but_no_values(self):
        examples = sorted((ROOT / "env").glob("*.env.example"))
        self.assertEqual(["azure-speech.env.example", "elevenlabs.env.example"], [p.name for p in examples])
        for path in examples:
            for line in path.read_text().splitlines():
                if line.strip() and not line.startswith("#"):
                    name, _, value = line.partition("=")
                    self.assertRegex(name, r"^[A-Z_]+$"); self.assertEqual("", value, f"{path.name}: {name} has a value")
        self.assertNotIn("KEY=", (ROOT / "env" / "elevenlabs.env.example").read_text().replace("# ", ""))

    def test_real_credential_files_are_ignored_and_never_packaged(self):
        for repo_path in ("env/azure-speech.env", "templates/presentation-video/env/azure-speech.env"):
            result = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", repo_path])
            self.assertEqual(0, result.returncode, f"{repo_path} is not ignored")
        # the packager ships tracked files only: no *.env may be tracked anywhere,
        # not even force-added
        tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
        self.assertEqual([], [p for p in tracked if p.endswith(".env")])

    def test_render_machine_never_receives_credentials_or_a_draft(self):
        remote = (ROOT / "templates" / "presentation-video" / "tools" / "render-remote.sh").read_text()
        for needed in ("--exclude env", "--exclude '*.env'", '"draft": true'):
            self.assertIn(needed, remote)
        self.assertIn('"draft": true', (ROOT / "templates" / "presentation-video" / "tools" / "render.sh").read_text())

    def test_no_secret_and_no_organization_specific_fact_in_the_method(self):
        banned = re.compile(r"(?i)neufeld|\\\\s?ndf|\bmac[12]\b|klaus|MAI-Voice|UgBBYS2s|\.nwb\.|claude-it\b")
        token = re.compile(r"\b[A-Za-z0-9]{32,}\b")
        for path, text in self.texts():
            self.assertIsNone(banned.search(text), f"{path}: organization-specific fact")
            if path.suffix in (".example", ".json", ".md", ".sh") and "package-lock" not in path.name:
                self.assertIsNone(token.search(text), f"{path}: token-like string")

    def test_template_ships_no_generated_or_installed_files(self):
        template = ROOT / "templates" / "presentation-video"
        for name in ("node_modules", "out", "stills", "video-profile.json", "pronunciation.json"):
            self.assertFalse((template / name).exists(), name)
        self.assertEqual([], list((template / "public" / "audio").glob("*.mp3")))
        self.assertTrue(json.loads((template / "src" / "timeline.json").read_text())["draft"])

    def test_skills_exclude_each_other_and_other_video_forms(self):
        for name, others in (("tutorial-video-scripting", ["presentation-video-production", "presentation-video-review"]),
                             ("presentation-video-production", ["tutorial-video-scripting", "presentation-video-review"]),
                             ("presentation-video-review", ["tutorial-video-scripting", "presentation-video-production"])):
            head = (ROOT / "skills" / name / "SKILL.md").read_text().split("---")[1]
            self.assertIn("Not for", head)
            for other in others:
                self.assertIn(other, head)
        scripting = (ROOT / "skills" / "tutorial-video-scripting" / "SKILL.md").read_text().split("---")[1]
        for form in ("marketing", "filmed", "screen recordings"):
            self.assertIn(form, scripting)


if __name__ == "__main__":
    unittest.main()
