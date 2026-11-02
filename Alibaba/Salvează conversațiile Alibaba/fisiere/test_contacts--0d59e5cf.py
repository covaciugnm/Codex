import tempfile,json,unittest
from pathlib import Path
from contacts import Contacts
from launcher import create_launcher

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.folder=self.root/'Example';self.folder.mkdir()
        self.d={'id':'42','contact':'Original name','updatedAt':'2099-01-01','profile':{'company':'Example Ltd','alibabaCategory':'Machinery'},'messages':[{'key':'a','text':'2025-02-01 09:30 Șurub inox info@example.com','sender':'partner'},{'key':'b','text':'2024-01-01 10:20 My email me@private.example','sender':'self'},{'key':'c','text':'timeless notice','sender':'unknown'}]}
        self.write();self.store=Contacts(self.root);self.store.scan(True)
    def write(self):(self.folder/'conversation.json').write_text(json.dumps(self.d),encoding='utf-8')
    def tearDown(self):
        if hasattr(self,'app'):self.app.contacts.db.close()
        self.store.db.close();self.temp.cleanup()
    def test_dates_and_evidence(self):
        c=self.store.get('42');self.assertEqual(c['source']['lastMessageAt'],'2025-02-01T09:30');self.assertEqual(c['source']['facts'][0]['value'],'info@example.com');self.assertEqual(len(c['source']['facts']),1)
    def test_personal_survives_new_capture_and_restart(self):
        self.store.update('42',{'alias':'Furnizor șuruburi','tag':'Prioritar','company':'Verificată'})
        self.d['contact']='Updated original';self.d['messages'].append({'key':'d','text':'2026-01-01 01:02 New'});self.write();self.store.scan(True)
        other=Contacts(self.root)
        try:
            c=other.get('42');self.assertEqual(c['personal']['tag'],'Prioritar');self.assertEqual(c['original'],'Updated original');self.assertEqual(c['source']['company'],'Example Ltd')
        finally:other.db.close()
    def test_search_and_clear(self):
        self.assertEqual(self.store.search('surub')[0]['messageKey'],'a')
        self.store.update('42',{'tag':'Important'});self.assertEqual(self.store.search('important')[0]['count'],0)
        self.store.update('42',{'tag':''});self.assertEqual(self.store.search('important'),[])
        with self.assertRaises(ValueError):self.store.update('42',{'original':'Overwrite'})
    def test_api_auth_and_identity(self):
        app=create_launcher('fixture',root=self.root);self.app=app;client=app.test_client();url='http://127.0.0.1:8766'
        self.assertEqual(client.post('/crm/contact/42',base_url=url,json={'alias':'bad'}).status_code,401)
        self.assertEqual(client.post('/crm/contact/42',base_url=url,json={'alias':'bad'},headers={'X-Archive-Key':'fixture','Origin':'https://evil.example'}).status_code,403)
        r=client.post('/crm/contact/42',base_url=url,json={'alias':'My name'},headers={'X-Archive-Key':'fixture'});self.assertEqual(r.status_code,200);self.assertEqual(r.json['original'],'Original name')

if __name__=='__main__':unittest.main()
