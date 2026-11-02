import unittest, tempfile, json
from pathlib import Path
from server import create_app, Archive, allowed, digest

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.app=create_app(self.tmp.name,'test-secret',False);self.client=self.app.test_client()
        self.s={'id':'42','contact':'Acme / test','messages':[{'key':'m1','text':'<script>alert(1)</script>','sender':'self'}],'attachments':[],'unresolved':[]}
    def tearDown(self): self.tmp.cleanup()
    def request(self,path,method='GET',data=None,**headers):
        return self.client.open(path,method=method,json=data,base_url='http://127.0.0.1:8765',headers={'X-Archive-Key':'test-secret',**headers})
    def test_persistence_merge_identity(self):
        self.assertEqual(self.request('/api/capture','POST',self.s).status_code,200)
        self.s['messages']=[{'key':'m2','text':'Second'}];self.request('/api/capture','POST',self.s)
        self.request('/api/capture','POST',self.s)
        a=Archive(self.tmp.name,False);self.assertEqual(len(a.docs['42']['messages']),2)
        rendered=(a.folder(a.docs['42'])/'conversation.html').read_text('utf-8')
        self.assertNotIn('<script>',rendered);self.assertIn('&lt;script&gt;',rendered)
        self.s['id']='43';self.request('/api/capture','POST',self.s)
        self.assertEqual(len(self.app.archive.docs),2)
        self.assertNotEqual(self.app.archive.docs['42']['folder'],self.app.archive.docs['43']['folder'])
    def test_access(self):
        self.assertEqual(self.client.get('/api/status',base_url='http://127.0.0.1:8765').status_code,401)
        self.assertEqual(self.request('/api/status',Origin='https://evil.example').status_code,403)
        self.assertEqual(self.client.get('/',base_url='http://evil.example:8765').status_code,403)
        self.assertEqual(self.request('/api/capture','POST',{'id':'x','messages':[]}).status_code,400)
        self.assertEqual(self.request('/files/x/../../config.json?key=test-secret').status_code,404)
    def test_attachments_restart_dedup(self):
        self.s['attachments']=[{'key':'file1','url':'https://x.alicdn.com/a.jpg','kind':'image','name':'../test.jpg','messageKey':'m1'}]
        a=self.app.archive;a.capture(self.s);d=a.docs['42'];f=d['attachments'][0]
        path=a.folder(d)/f['localPath'];path.parent.mkdir();path.write_bytes(b'image fixture');f['status']='complete';a.persist(d)
        a.capture(self.s);self.assertEqual(len(d['attachments']),1);self.assertEqual(f['status'],'complete')
        result=self.request('/api/conversation/42').get_json();self.assertNotIn('url',result['attachments'][0])
        response=self.client.get('/files/42/'+digest('file1')+'?key=test-secret',base_url='http://127.0.0.1:8765')
        self.assertEqual(response.data,b'image fixture');response.close()
        a=Archive(self.tmp.name,False);self.assertEqual(a.docs['42']['attachments'][0]['status'],'complete')
    def test_allowlist(self):
        for url in ['http://alibaba.com/a','https://evilalibaba.com/a','https://alibaba.com.evil.example/a','file:///x','https://127.0.0.1/x','https[CREDENTIAL_REDACTED]alibaba.com/x']:self.assertFalse(allowed(url))
        self.assertTrue(allowed('https://clouddisk.alibaba.com/file?id=1'))
    def test_legacy_overlap(self):
        a=self.app.archive
        self.s['messages']=[{'key':'legacy:1','text':'2026-10-23 09:00 Hello'}]
        a.capture(self.s)
        self.s['messages']=[{'key':'content:new','text':'2026-10-23 09:00 Hello','sender':'partner'}]
        a.capture(self.s)
        self.assertEqual(len(a.docs['42']['messages']),1)
        self.assertEqual(a.docs['42']['messages'][0]['sender'],'partner')
        a.capture(self.s);self.assertEqual(len(a.docs['42']['messages']),1)
    def test_worker_failure_retry(self):
        import threading
        a=self.app.archive
        self.s['attachments']=[{'key':'file1','url':'https://x.alicdn.com/a.jpg','kind':'image','name':'a.jpg','messageKey':'m1'}]
        a.download=lambda url,path: (_ for _ in ()).throw(ValueError('mock failure'))
        threading.Thread(target=a.work,daemon=True).start();a.capture(self.s);a.jobs.join()
        self.assertEqual(a.docs['42']['attachments'][0]['status'],'failed')
        def download(url,path):path.parent.mkdir(exist_ok=True);path.write_bytes(b'fixture')
        a.download=download;a.retry();a.jobs.join()
        self.assertEqual(a.docs['42']['attachments'][0]['status'],'complete')

if __name__=='__main__':unittest.main()
