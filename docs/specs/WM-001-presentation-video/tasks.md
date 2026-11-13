# Tasks: Narrated presentation videos

## Stable work ID

- Feature ID: `WM-001`
- Specification: `docs/specs/WM-001-presentation-video/spec.md`
- Plan: `docs/specs/WM-001-presentation-video/plan.md`
- Artifact path: `docs/specs/WM-001-presentation-video/tasks.md`

Template root below: `T/` = `templates/presentation-video/`.
Test file: `tests/test_presentation_video.py`.

## Architecture findings

| Finding | Affected interface | Resolution task |
|---|---|---|
| AF-001 duplicated timing rule | IC-004 | T008 |
| AF-002 audible pause twice the configured one | IC-003, IC-004, IC-006 | T007, T008, T011 |
| AF-003 provider settings without effect | IC-003 | T012 |
| AF-004 packaging is Core-managed | IC-008 | T021 |
| AF-005 fifth seeded defect not automatic | IC-009 | T018, T026 |
| AF-006 hard-coded issue label in Core | none | T030 (report only) |

## Tests

Command for all slices: `python3 -m unittest discover -s tests -t . -v`, plus
`python3 scripts/validate-plugin` and `python3 scripts/sync-core --check`.
Each slice writes its failing tests first and ends green.

## Implementation slices

### Slice S1: Profile, pronunciation list, script format and script check

- [x] T001 [US-006] [FR-026] [IC-007] Tests then implementation of profile loading and validation: required keys, unknown keys, defaults from research, multilingual voice rule — files: `T/tools/profile.py`, `T/video-profile.example.json`, `T/video.json`; catches: missing key, monolingual voice (AC-016)
- [x] T002 [FR-005] [IC-002] Tests then implementation of the pronunciation list: merge project and video lists, conflicts, application to spoken text, provider markup — files: `T/tools/speech.py`, `T/pronunciation.example.json`; catches: term corrected in one place only; depends on: T001
- [x] T003 [US-001] [FR-001–FR-006] [FR-036] [AC-001] [AC-002] [AC-008] [AC-017] Tests then implementation of the script check: one audience, scene message, line and sentence limits, caption against spoken form, sources, recreated-interface notice, secrets pattern, estimated length and split proposal — files: `T/tools/check_script.py`, `T/script/script.md`, `tests/fixtures/presentation-video/`; depends on: T001, T002

### Slice S2: Voicing, manifest, timeline, captions

- [x] T004 [US-005] [AC-010] [IC-008] Tests then implementation of credential loading and the credential check (no key in output, configurable location) — files: `T/tools/voice_azure.py`; catches: key echoed in an error
- [x] T005 [US-002] [US-004] [FR-007] [FR-009] [AC-003] [AC-004] [AC-005] Tests then implementation of per-line voicing against a fake provider: content-addressed names, reuse, stale removal, retry budget, character count — files: `T/tools/voice_azure.py`; depends on: T002, T004
- [x] T006 [FR-010] Manifest with measured length — files: `T/tools/voice_azure.py`, `T/tools/audio.py`; depends on: T005
- [x] T007 [AF-002] [FR-030] Tests then implementation of silence measurement per file — files: `T/tools/audio.py`; catches: pause differing by provider; depends on: T006
- [x] T008 [AF-001] [FR-010] [FR-012] [FR-018] [FR-030] [IC-004] Tests then implementation of the timeline tool and caption file: silence accounting, minimum slot, scene pauses, chapter marks, stale-manifest refusal — files: `T/tools/timeline.py`; catches: caption drift, hand timing; depends on: T007

### Slice S3: Measurement, probing, read-back, take splitting

- [x] T009 [FR-035] [AC-018] Tests then implementation of pace per scene — files: `T/tools/measure.py`; depends on: T008
- [x] T010 [FR-016] [AC-007] [IC-006] Tests then implementation of file measurement (resolution, frame rate, duration, loudness, peak) against the profile — files: `T/tools/measure.py`; catches: trusting the render exit status
- [x] T011 [AF-002] [AC-013] Tests then implementation of pause measurement in rendered sound against the timeline — files: `T/tools/measure.py`; depends on: T008
- [x] T012 [AF-003] [FR-035] [AC-018] Tests then implementation of the setting probe (two runs with, two without, effect beyond spread) — files: `T/tools/probe_settings.py`; depends on: T005
- [x] T013 [FR-034] [AC-015] Tests then implementation of read-back verification from word-timing files and key-term sample sentences — files: `T/tools/verify_speech.py`; depends on: T002
- [x] T014 [FR-008] [FR-032] Tests then implementation of take splitting with match threshold — files: `T/tools/split_takes.py`; catches: skipped or repeated sentence accepted; depends on: T007

### Slice S4: Template composition and sample video

- [x] T015 [FR-011] [FR-012] [FR-013] Composition reading `timeline.json`: root, scene frame with chapters, caption, audio track, sample scenes, legibility constants — files: `T/src/`, `T/package.json`, `T/tsconfig.json`; depends on: T008
- [x] T016 [FR-014] [AC-006] [IC-005] Check-still and single-frame tools with inspection list — files: `T/tools/stills.mjs`, `T/tools/frame.mjs`; depends on: T015
- [x] T017 [FR-015] [FR-016] [FR-017] Render locally and on a render machine, loudness normalization, opening sequence without re-encoding — files: `T/tools/render.sh`, `T/tools/render-remote.sh`, `T/tools/prepend.sh`; depends on: T015
- [x] T018 [US-003] [AF-005] [SC-003] Seeded-defect fixture and its automatic findings — files: `tests/fixtures/presentation-video/defects/`; depends on: T003, T010

### Slice S5: Skills, guides, routing, credentials

- [x] T019 [FR-003] [FR-031] [FR-032] [FR-033] Shared guides — files: `shared/media/speech-synthesis.md`, `shared/media/spoken-style.md`
- [x] T020 [FR-027] [FR-020–FR-023] Three skills — files: `skills/tutorial-video-scripting/SKILL.md`, `skills/presentation-video-production/SKILL.md`, `skills/presentation-video-review/SKILL.md`; depends on: T019
- [x] T021 [AF-004] [US-005] [FR-024] [FR-025] [AC-009] [SC-005] Credential examples, ignore rule, test that examples hold no values and real files are ignored — files: `env/`, `.gitignore`
- [x] T022 [FR-027] [FR-028] [AC-012] [SC-006] Method registration, handoff graph, inventory test, trigger matrix and evaluation cases — files: `method.json`, `shared/policies/lifecycle-handoffs.md`, `shared/policies/lifecycle-selection.md`, `tests/test_writing_contracts.py`, `tests/fixtures/trigger-cases/matrix.json`, `evals/`; depends on: T020
- [x] T023 [FR-029] Test that no organization-specific fact appears in skills, guides, templates and examples; depends on: T020

### Slice S6: Documentation, review record, playbook

- [x] T024 [FR-019] [IC-009] Review record and project record templates — files: `T/review.md`, `T/README.md`
- [x] T025 [PB-WM-VIDEO-001] Author the playbook template — files: `T/playbook.md`; depends on: T017, T020
- [x] T026 [AF-005] Document the still inspection for missing characters and the fonts' coverage — files: `skills/presentation-video-review/SKILL.md`, `T/README.md`
- [x] T027 README, usage, version 0.2.0 in six places, plugin keywords — files: `README.md`, `docs/usage.md`, `method.json`, `pyproject.toml`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`

## Dependencies

| Work ID | Depends on | Reason | Parallel-safe with |
|---|---|---|---|
| S2 | S1 | Tools read the profile and pronunciation list | none |
| S3 | S2 | Measures the manifest and timeline | none |
| S4 | S2 | Composition reads the timeline | S3 |
| S5 | S1–S4 | Skills describe the finished tools | none |
| S6 | S5 | Documents the whole | none |

## Final integration

### Slice S7: Rehearsal and integrated verification

- [x] T028 [SC-001] [SC-002] [PB-WM-VIDEO-001] Rehearse the playbook end to end on the sample video: voice with Azure, timeline, stills, render, measurements, captions; change one line and confirm one request — evidence: `docs/specs/WM-001-presentation-video/rehearsal.md`
- [x] T029 [FR-032] [AC-014] Voice one scene through the ElevenLabs connector, split it, verify — evidence: same file
- [x] T030 [AF-006] Fix the hard-coded issue label in Method Core and sync the fix — evidence: https://github.com/phense/method-core/pull/1
- [x] T031 Run one existing project with the new tools using configuration changes only; compare the measured pause before and after — evidence: same file
- [x] T032a Independent review of the change; twelve findings corrected with tests (plan AF-007)
- [ ] T032b Review the playbook template with `playbook-review` at the committed revision

### Slice S8: Convergence and final verification handoff

- [ ] T033 Run convergence, resolve every actionable finding, capture fresh verification, update `FEATURES.md` and the issue.

## Playbook obligations

`PB-WM-VIDEO-001` (system): authored in T025, rehearsed in T028 and T029,
reviewed in T032. Its readiness blocks reporting the feature complete.
