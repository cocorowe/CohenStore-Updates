import http.client
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checks',ROOT/'tools/check_downloads.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SourceStatusTests(unittest.TestCase):
    def test_header_is_not_complete_transfer(self):
        self.assertEqual(m.classify_download_result({'ok':True})[0],'Unverified')
    def test_full_hash_is_working_without_console_claim(self):
        self.assertEqual(m.classify_download_result({'ok':True,'full_transfer':'verified'})[0],'Working')
    def test_temporary_errors_remain_visible_and_fail_strict_host_check(self):
        for err in ('HTTP 500','HTTP 502','HTTP 429','HTTP 408','URLError','TimeoutError','RemoteDisconnected','IncompleteRead'):
            with self.subTest(err=err):
                report=m.make_report([{'ok':False,'error':err}])
                result=report['results'][0]
                self.assertEqual(result['source_status'],'Unverified')
                self.assertFalse(result['blocking_check_error'])
                self.assertEqual(report['summary']['host_failures'],1)
                self.assertEqual(m.report_exit_code(report,True),2)
    def test_missing_checked_url_does_not_mark_every_mirror_unavailable(self):
        report=m.make_report([{'ok':False,'error':'HTTP 404'},{'ok':True}])
        self.assertEqual([r['source_status'] for r in report['results']],['Unavailable','Unverified'])
    def test_integrity_errors_are_blocking_in_all_modes(self):
        for err in ('Full download SHA-256 mismatch','Invalid partial-response range','Missing or conflicting file size','Response is not the selected package/plugin format'):
            with self.subTest(err=err):
                report=m.make_report([{'ok':False,'error':err}])
                self.assertEqual(m.report_exit_code(report),1)
                self.assertEqual(m.report_exit_code(report,True),1)
    def test_source_reference_makes_no_request(self):
        result=m.probe({'id':'ref','title':'Reference','urls':[]},lambda *a,**k:self.fail('Reference was downloaded'))
        self.assertEqual(m.make_report([result])['summary']['skipped'],1)
        self.assertEqual(m.report_exit_code(m.make_report([result]),True),0)
    def test_disconnect_is_a_reported_network_failure(self):
        def disconnected(*a,**k):raise http.client.RemoteDisconnected('closed')
        result=m.probe({'id':'test','title':'Test','urls':['https://example.com/a.pkg']},disconnected)
        self.assertEqual(result['error'],'RemoteDisconnected')
        self.assertEqual(m.classify_download_result(result)[1],'temporary-network-failure')
