import importlib.util,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checks',ROOT/'tools/check_downloads.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class WorkflowPolicyTests(unittest.TestCase):
    def test_manual_event_matrix(self):
        for event in ('push','pull_request','schedule','workflow_dispatch','repository_dispatch'):
            for value in (True,False,'true','false',None,1):
                with self.subTest(event=event,value=value):
                    expected=event=='workflow_dispatch' and (value is True or value=='true')
                    self.assertEqual(m.full_transfer_requested(event,{'inputs':{'full_transfer':value}}),expected)
    def test_absent_and_malformed_inputs_are_denied(self):
        for event in ({},None,[],{'inputs':None},{'inputs':[]}):
            self.assertFalse(m.full_transfer_requested('workflow_dispatch',event))
    def test_cli_denies_push_before_opening_even_a_catalog(self):
        with tempfile.TemporaryDirectory() as folder:
            event=Path(folder)/'event.json';event.write_text('{"inputs":{"full_transfer":true}}')
            env=dict(os.environ,GITHUB_EVENT_NAME='push',GITHUB_EVENT_PATH=str(event))
            result=subprocess.run([sys.executable,str(ROOT/'tools/check_downloads.py'),'--full','--require-manual-dispatch','--catalog','does-not-exist.json'],env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertIn('no URLs were requested',result.stderr)
            self.assertNotIn('FileNotFoundError',result.stderr)
    def test_workflow_has_both_guards_and_visible_host_failures(self):
        source=(ROOT/'.github/workflows/check-downloads.yml').read_text()
        self.assertNotIn(r'if: \${{',source)
        self.assertIn("if: ${{ always() && github.event_name == 'workflow_dispatch' && inputs.full_transfer == true }}",source)
        self.assertIn('--full --require-manual-dispatch --strict-host-health',source)
        self.assertNotIn('continue-on-error',source)
    def test_publisher_file_workflow_is_only_manual_and_uses_current_checker(self):
        source=(ROOT/'.github/workflows/check-game-download.yml').read_text()
        self.assertIn('workflow_dispatch:',source)
        self.assertNotIn('  push:',source)
        self.assertNotIn('  schedule:',source)
        self.assertIn("if: ${{ github.event_name == 'workflow_dispatch' && inputs.full_transfer == true }}",source)
        self.assertIn('--full --require-manual-dispatch --strict-host-health',source)
        self.assertNotIn('CohenStore-0.5.8-Source.zip',source)
