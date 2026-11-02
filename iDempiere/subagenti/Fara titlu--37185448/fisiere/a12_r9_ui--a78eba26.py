from a12_r9_publish import *
import sys,functools,threading
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
def test(dest):
 class Local(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 srv=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Local,directory=str(dest)));th=threading.Thread(target=srv.serve_forever,daemon=True);th.start();rs=[]
 try:
  with sync_playwright()as pw:
   b=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--disable-background-networking','--disable-extensions','--disable-sync'])
   for width,height in [(390,844),(1366,768)]:
    p=b.new_page(viewport={'width':width,'height':height});p.route('**/*',lambda req:req.continue_()if req.request.url.startswith('http://127.0.0.1:')else req.abort());p.goto('http://127.0.0.1:'+str(srv.server_port)+'/Audit_individual_P01_R9.html',wait_until='load');start=p.locator('tbody tr').count();dims=p.evaluate('''() => ({viewport:innerWidth, document:document.documentElement.scrollWidth, table_view:document.querySelector(".sc").clientWidth, table_body:document.querySelector(".sc").scrollWidth})''');assert start==652 and dims['document']==width
    p.locator('#search').fill('T354');assert p.locator('tbody tr:not([hidden])').count()==1;p.locator('tbody tr:not([hidden]) a').click();detail=p.evaluate('''() => ({width:innerWidth, body:document.documentElement.scrollWidth, count:document.querySelectorAll("section").length})''');assert detail['width']==detail['body']==width and detail['count']==27
    rs.append({'width':width,'height':height,'rows':start,'screen':dims,'query':'T354','matching_rows':1,'detail':detail});p.close()
   b.close()
 finally:srv.shutdown();srv.server_close();th.join(4)
 f=dest/'Verificare_UX_R9.json';wr(f,{'utc':now(),'source_hash':H(dest/'Audit_individual_P01_R9.html'),'measurements':rs,'scope':'Browser Chromium cu profil temporar, distribuire numai prin bucla locală.'});print(H(f))
if __name__=='__main__':test(R9)

