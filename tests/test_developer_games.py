import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('updater',Path(__file__).resolve().parents[1]/'tools/update_developer_games.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class DeveloperGamesTests(unittest.TestCase):
    def setUp(self):
        self.cat={'schema':1,'items':[{'id':'curated','title':'Keep this','urls':['https://example.test/game.pkg']} ]}
        self.release={'tag_name':'v1.0','html_url':'https://github.com/dev/game/releases/tag/v1.0','assets':[{'id':1,'name':'IV0000-TEST00001_00-GAME.pkg','size':4096,'digest':'sha256:'+'a'*64,'browser_download_url':'https://github.com/dev/game/releases/download/v1.0/game.pkg'}]}
    def test_adds_asset_without_losing_curated_entries(self):
        m.merge_release(self.cat,'dev/game','Game','games',self.release)
        self.assertEqual(self.cat['items'][0]['id'],'curated')
        self.assertEqual(self.cat['items'][1]['title_ids'],['TEST00001'])
        self.assertEqual(self.cat['items'][1]['sha256'],'a'*64)
    def test_repeat_preserves_curated_changes(self):
        m.merge_release(self.cat,'dev/game','Game','games',self.release)
        self.cat['items'][1]['note']='Reviewed note'
        before=copy.deepcopy(self.cat)
        m.merge_release(self.cat,'dev/game','Game','games',self.release)
        self.assertEqual(self.cat,before)
    def test_missing_digest_stays_unknown(self):
        self.release['assets'][0]['digest']=None
        m.merge_release(self.cat,'dev/game','Game','games',self.release)
        self.assertEqual(self.cat['items'][1]['sha256'],'')
    def test_rejects_wrong_host_and_estimated_size(self):
        for field,value in [('browser_download_url','https://archive.org/game.pkg'),('size','15GB')]:
            r=copy.deepcopy(self.release);r['assets'][0][field]=value
            with self.assertRaises(ValueError):m.merge_release(copy.deepcopy(self.cat),'dev/game','Game','games',r)

    def test_emulator_assets_have_distinct_names_and_exclude_unknown_platforms(self):
        r=copy.deepcopy(self.release)
        r['assets']=[]
        for index,title_id in enumerate(['PFBN00001','PGBA00001','UNKNOWN01']):
            r['assets'].append({'id':index+1,'name':'IV0001-'+title_id+'_00-TEST.pkg','size':4096,'browser_download_url':'https://github.com/Cpasjuste/pemu/releases/download/v1/test'+str(index)+'.pkg'})
        m.merge_release(self.cat,'Cpasjuste/pemu','pEMU','emulators',r)
        self.assertEqual(len(self.cat['items']),3)
        self.assertNotEqual(self.cat['items'][1]['title'],self.cat['items'][2]['title'])
        self.assertTrue(all(x['category']=='emulators' for x in self.cat['items'][1:]))
