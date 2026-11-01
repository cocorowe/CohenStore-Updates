import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LinkedSourceTests(unittest.TestCase):
 def test_exact_source_metadata(self):
  c=json.loads((ROOT/'catalog/catalog.json').read_text())['items']
  links=json.loads((ROOT/'catalog/library-links.json').read_text())['items']
  source={x['id']:x for x in links}
  groups=[x for x in c if 'linked_source_id' in x]
  self.assertEqual(len(c),207)
  self.assertEqual(len(links),18046)
  self.assertEqual(len(groups),7)
  self.assertEqual(len({x['linked_source_id'] for x in groups}),7)
  for direct in groups:
   with self.subTest(direct=direct['id']):
    self.assertTrue(direct.get('urls'))
    other=source[direct['linked_source_id']]
    self.assertFalse(other.get('urls'))
    self.assertTrue(other.get('source_url'))
    self.assertEqual(other['category'],direct['category'])
