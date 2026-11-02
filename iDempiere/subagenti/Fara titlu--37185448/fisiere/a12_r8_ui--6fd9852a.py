from a12_r8_review import *
import sys,os
sys.path.insert(0,'D:/CodexWork/a12-r4-playwright')
from playwright.sync_api import sync_playwright
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import threading,functools
def verify(dest):
 class Server(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 srv=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Server,directory=str(dest)));thr=threading.Thread(target=srv.serve_forever,daemon=True);thr.start();result=[]
 try:
  with sync_playwright()as pw:
   browser=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--disable-background-networking','--disable-extensions','--disable-sync'])
   for width,height in [(390,844),(1366,768)]:
    page=browser.new_page(viewport={'width':width,'height':height});page.route('**/*',lambda r:r.continue_()if r.request.url.startswith('http://127.0.0.1:')else r.abort());page.goto('http://127.0.0.1:'+str(srv.server_port)+'/Audit_individual_P01_R8.html',wait_until='load');full=page.locator('tbody tr').count();dims=page.evaluate('''() => ({ viewport:innerWidth, root:document.documentElement.scrollWidth, tableVisible:document.querySelector(".table-scroll").clientWidth, tableContent:document.querySelector(".table-scroll").scrollWidth })''');assert full==652 and dims['root']==width,(full,dims)
    page.locator('#f').fill('T354');n=page.locator('tbody tr:not([hidden])').count();one=page.locator('tbody tr:not([hidden]) a').first;url=one.get_attribute('href');assert n>0 and url;one.click();assert page.title().startswith('T354');detail=page.evaluate('''() => ({ width:innerWidth,root:document.documentElement.scrollWidth,sections:document.querySelectorAll("section").length })''');assert detail['sections']>0
    assert detail['root']==width,detail
    result.append({'viewport':width,'height':height,'initial_rows':full,'index':dims,'filter_T354_count':n,'opened_detail':url,'detail':detail});page.close()
   browser.close()
 finally:srv.shutdown();srv.server_close();thr.join(3)
 f=(R if False else dest)/'Verificare_UX_R8.json';wr(f,{'utc':now(),'method':'Chromium headless, endpoint loopback, directorul conține doar artefactele raportului, fără acces la sit sau ERP.','pages':result,'sha_of_index':sha(dest/'Audit_individual_P01_R8.html')});print(sha(f),result)
if __name__=='__main__':verify(E/'R8')

