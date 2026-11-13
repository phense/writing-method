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
WRITING={'documentation-planning','documentation-authoring','documentation-review','documentation-pdf','human-prose-drafting','explaining-concepts','writing-procedures','empathic-troubleshooting','terminology-guard','visual-placeholders','tutorial-video-scripting','presentation-video-production','presentation-video-review'}
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
        self.assertEqual({'standalone-document','documentation-set','existing-documentation-plan','documentation-pdf','tutorial-video-script','presentation-video-production','presentation-video-review','video-one-line-correction'},{c['id'] for c in matrix})
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
