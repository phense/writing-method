"""Writing-owned contracts and installed artifacts, independent of Engineering."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from scripts.validate_plugin import validate_repository
ROOT=Path(__file__).resolve().parents[1]
READER={'documentation-planning','documentation-authoring','documentation-review','documentation-pdf','human-prose-drafting','explaining-concepts','writing-procedures','empathic-troubleshooting','terminology-guard','visual-placeholders','tutorial-video-scripting','presentation-video-production','presentation-video-review'}
# The story family (WM-003, experimental). tests/test_writing_mode.py checks its separation from the reader family.
STORY={'story-bootstrap','story-worldbuilding','story-characters','story-architecture','story-drafting','story-canon-review','story-craft-research','story-voice-review'}
WRITING=READER|STORY
SHARED={'project-backlog','verification-before-completion','dispatching-parallel-agents','using-git-worktrees','requesting-code-review','receiving-code-review','playbook-authoring','playbook-review'}

class WritingContracts(unittest.TestCase):
    def test_exact_owned_and_shared_inventory_and_resource_validation(self):
        self.assertEqual(WRITING|SHARED,{p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')})
        self.assertEqual([],validate_repository(ROOT))
    def test_review_retry_preserves_chunks_and_blocks_unresolved_findings(self):
        text=(ROOT/'shared/policies/lifecycle-handoffs.md').read_text()
        graph=json.loads(re.search(r'```json\n(.*?)\n```',text,re.S).group(1))
        self.assertEqual({'documentation':'documentation-authoring','presentation-video':'presentation-video-production'},graph['executors'])
        self.assertEqual({'from':'documentation-review','to':'documentation-authoring','condition':'actionable findings returned for affected chunks','artifact':'docs/writing/<doc-id>/review.md findings','preserves':'accepted chunks and stable chunk IDs'},graph['retry_transitions'][0])
        self.assertEqual({('documentation-review','documentation-authoring'),('presentation-video-review','presentation-video-production'),('presentation-video-review','tutorial-video-scripting')},{(r['from'],r['to']) for r in graph['retry_transitions']})
        edge=next(e for e in graph['edges'] if e['from']=='documentation-review')
        self.assertEqual('verification-before-completion',edge['to'])
        self.assertIn('no open Critical or Important',edge['completion_guard'])
        self.assertNotIn('speckit-specify',graph['nodes'])
    def test_writing_lifecycles_keep_recovery_and_state_handoffs(self):
        for name in ['documentation-planning','documentation-authoring','documentation-review']:
            text=(ROOT/'skills'/name/'SKILL.md').read_text()
            for heading in ['Trigger','Do not use for','Consumes','Produces','Completion','Next phase','Supporting skills','Recovery preamble','Operational state handoffs']:
                self.assertIn('\n## '+heading+'\n',text)
            for contract in ['host-observed live agent IDs','--live-agents','before any canonical or backlog mutation','../project-backlog/SKILL.md#transition-to-event-ordering','continuity-state event','continuity-state checkpoint','playbook-review']:
                self.assertIn(contract," ".join(text.split()))
    def test_routing_scenarios_use_only_available_primary_and_supporting_skills(self):
        matrix=json.loads((ROOT/'tests/fixtures/trigger-cases/matrix.json').read_text())
        self.assertEqual({'standalone-document','documentation-set','existing-documentation-plan','documentation-pdf','tutorial-video-script','presentation-video-production','presentation-video-review','video-one-line-correction',
                          # Story-positive cases: a story skill is primary and the reader prose skills are prohibited.
                          'story-chapter-draft','story-new-vault','story-canon-review','story-voice-review','story-in-world-manual','story-beta-feedback',
                          # Study vault: story-craft-research is primary and declines the request; story-drafting is prohibited.
                          'study-vault-draft-request',
                          # Negative cases: every story skill is prohibited.
                          'story-vault-readme','docs-release-note','story-world-tutorial-video','story-method-documentation','vault-parent-session'},{c['id'] for c in matrix})
        self.assertEqual(len(matrix),len({c['id'] for c in matrix}))
        story_primary={c['id'] for c in matrix if c['primary'] in STORY}
        self.assertEqual({'story-chapter-draft','story-new-vault','story-canon-review','story-voice-review','story-in-world-manual','story-beta-feedback','study-vault-draft-request'},story_primary)
        reader_prose={'explaining-concepts','writing-procedures','empathic-troubleshooting','human-prose-drafting','documentation-authoring','documentation-planning','documentation-review','tutorial-video-scripting'}
        new_cases=[c for c in matrix if c['id'].startswith(('story-','study-','vault-','docs-release'))]
        self.assertEqual(12,len(new_cases))
        for case in new_cases:
            if case['primary'] in STORY:
                # Story work never loads the reader prose skills, review-feedback handling or a backlog.
                self.assertTrue(reader_prose|{'requesting-code-review','receiving-code-review','project-backlog'} <= set(case['prohibited']),case['id'])
                self.assertFalse(set(case['supporting'])-STORY-{'verification-before-completion'},case['id'])
            elif case['id']=='story-method-documentation':
                # Documenting the method may read story skills as source material; the two that govern or judge manuscript text stay prohibited.
                self.assertEqual({'native-focused-edit','story-drafting','story-voice-review'},set(case['prohibited']),case['id'])
            else:
                self.assertTrue(STORY <= set(case['prohibited']),case['id'])
            if case['id']=='study-vault-draft-request':
                self.assertIn('story-drafting',case['prohibited'])
        # Both hosts expect the same selection for every routing case that has a trigger file.
        triggers={json.loads(p.read_text())['id'] for p in (ROOT/'evals/shared/triggers').glob('*.json')}
        expected={host:json.loads((ROOT/'evals'/host/'expected.json').read_text()) for host in ('claude','codex')}
        self.assertEqual(expected['claude'],expected['codex'])
        self.assertEqual(triggers,set(expected['claude']))
        for case in new_cases:
            routed=expected['claude'][case['id']]
            self.assertEqual(case['primary'],routed['primary'])
            # The matrix lists one entry no host can invoke; beyond it the lists are equal, so no prohibition can be dropped.
            self.assertEqual(set(case['prohibited'])-{'native-focused-edit'},set(routed['prohibited']),case['id'])
            self.assertTrue(set(routed['supporting']) <= set(case['supporting']),case['id'])
            self.assertEqual(['decision.md'],routed['artifacts'])
        for case in matrix:
            self.assertIn(case['primary'],WRITING)
            self.assertTrue(set(case['supporting']) <= WRITING|SHARED)
            self.assertNotIn(case['primary'],case['prohibited'])
    def test_copied_package_runs_state_tools_without_sibling_repositories(self):
        # Broken relative imports, cwd assumptions, or hidden sibling links fail here.
        with tempfile.TemporaryDirectory(prefix='writing-installed-') as directory:
            base=Path(directory);installed=base/'moved package'
            shutil.copytree(ROOT,installed,ignore=shutil.ignore_patterns('.git','.engineering-method','__pycache__','dist'))
            self.assertEqual([],validate_repository(installed))
            project=base/'target';project.mkdir()
            def run(*args):
                return subprocess.run([sys.executable,str(installed/'scripts/project-state'),*args],cwd=project,capture_output=True,text=True,timeout=20)
            result=run('backlog','init','--project-key','WM');self.assertEqual(0,result.returncode,result.stderr)
            result=run('backlog','add','--id','WM-001','--title','Write handbook','--priority','P1');self.assertEqual(0,result.returncode,result.stderr)
            self.assertIn('WM-001',(project/'BACKLOG.md').read_text())
            # The book layout ships complete: a copy without its filter or checker cannot be rendered or verified.
            book=installed/'templates/documentation/book'
            for name in ['_quarto.yml','_brand.yml','index.md','DESIGN.md','tools/check-pdf.py','_extensions/em-book/_extension.yml','_extensions/em-book/typst-template.typ','_extensions/em-book/typst-show.typ','_extensions/em-book/book-structure.lua','_extensions/em-book/chunk-title.lua']:
                self.assertTrue((book/name).is_file(),name)
            listed=re.findall(r'^\s+- (chapters/.+\.md)$',(book/'_quarto.yml').read_text(),re.M)
            self.assertEqual(sorted(p.name for p in (book/'chapters').glob('*.md')),sorted(Path(n).name for n in listed))
            self.assertIn('em-book-typst',(installed/'skills/documentation-pdf/SKILL.md').read_text())
            template=installed/'templates/documentation/pdf/DESIGN.md';template.unlink()
            self.assertTrue(any('DESIGN.md' in e for e in validate_repository(installed)))
    def test_attribution_covers_current_adaptations_and_original_writing(self):
        lock=json.loads((ROOT/'third-party/sources.lock.json').read_text())
        self.assertEqual({'humanizer','source-sans-3'},{s['id'] for s in lock['sources']})
        for source in lock['sources']:
            for mapping in source['files']:
                if mapping['modification_status'] in ('adapted','unmodified'):
                    self.assertEqual(mapping['destination_sha256'],hashlib.sha256((ROOT/mapping['destination_path']).read_bytes()).hexdigest())
        notices=(ROOT/'THIRD_PARTY_NOTICES.md').read_text()
        self.assertIn('https://github.com/blader/humanizer.git',notices)
        self.assertIn('Permission is hereby granted',notices)
        # Bundled fonts must travel with their licence text, in the notices and beside the files.
        self.assertIn('SIL OPEN FONT LICENSE',notices.upper())
        self.assertTrue((ROOT/'templates/documentation/book/fonts/LICENSE-SourceSans3.md').is_file())
if __name__=='__main__': unittest.main()
