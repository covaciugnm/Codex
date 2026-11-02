from lab import *
import glob,re
from playwright.sync_api import sync_playwright
assert sql("SELECT count(*) FROM adempiere.ad_scheduler WHERE isactive='Y'")=='0'
assert rows("select ad_client_id,name from adempiere.ad_client order by 1")==[['0','System'],['11','GardenWorld']]
d=json.loads((W/'native_inventory_2.json').read_text());i=d['ids']
import os
os.environ.update(APP=AP,PGC=PG,GEST=str(i['wh']),X='123',Y='124',N=str(i['no_cost']),GEST_COD=i['tag'])
import proba_A9 as historic
historic.CL=11
artifact=W/'zk_r8';artifact.mkdir(exist_ok=True)
summary={'utc':now(),'tag':i['tag'],'method':'Playwright on ZK GardenAdmin, private allowlist; historical UI selectors reused, GardenWorld scope/client 11. No click outside cabinet or network capability toward other hosts.','runs':[]}
def result(what,value):summary['runs'].append({'step':what,'result':value,'utc':now()});save('ui_t163.json',summary)
def query(k):
 v=rows(f"SELECT i.m_inventory_id,i.docstatus,i.posted,i.createdby,i.reversal_id,l.m_inventoryline_id,l.m_product_id,l.qtybook,l.qtycount FROM adempiere.m_inventory i LEFT JOIN adempiere.m_inventoryline l USING(m_inventory_id) WHERE i.m_warehouse_id={i['wh']} AND i.ad_client_id=11 ORDER BY 1,6");result(k,v);return v
class Driver(historic.C.P):
 def __init__(self,pg):
  self.pg=pg;self.out=str(artifact);self.jurnal=[];self.valori=[]
 def asteapta_final(self,conditie=None,max_s=180,eticheta=''):
  return super().asteapta_final(conditie,min(max_s,14),eticheta)
 def captura(self,nume):
  self.pg.screenshot(path=str(artifact/(nume+'.png')));result('capture '+nume,{'body':self.pg.locator('body').inner_text()[-1800:],'png':nume+'.png'})
 def meniu(self,top,*cale):
  target=cale[-1];box=self.pg.locator('.z-bandbox-input:visible').first;box.fill('');box.press_sequentially(target,delay=36);pop=self.pg.locator('.z-bandpopup:visible').first
  hit=pop.get_by_text(re.compile(r'^\s*'+re.escape(target)+r'\s*$',re.I));hit.first.wait_for(timeout=9000);hit.first.click();self.pg.wait_for_timeout(650)
def login(pg):
 pg.goto(ROOT+'/webui/',wait_until='domcontentloaded',timeout=60000);p=pg.locator('input[type=password]:visible').first;p.wait_for(timeout=50000)
 pg.locator('input.z-textbox:visible').first.fill('GardenAdmin');p.fill('GardenAdmin');pg.locator("button:has-text('OK'):visible").first.click()
 for _ in range(9):
  try:pg.locator('.z-bandbox-input:visible').first.wait_for(timeout=2200);break
  except Exception:
   go=pg.locator("button:has-text('OK'):visible")
   if go.count() and not pg.locator('input[type=password]:visible').count():go.first.click()
 assert pg.locator('.z-bandbox-input:visible').count();result('authenticated GardenAdmin',True)
with sync_playwright() as pw:
 paths=sorted(glob.glob(str(pathlib.Path.home()/'.cache/ms-playwright/chromium-*/chrome-linux*/chrome')))
 br=pw.chromium.launch(headless=True,executable_path=paths[-1] if paths else None,args=['--no-sandbox','--disable-dev-shm-usage','--proxy-server=direct://'])
 ctx=br.new_context(ignore_https_errors=True,viewport={'width':1480,'height':990})
 ctx.route('**/*',lambda route:route.continue_() if route.request.url.startswith(ROOT+'/') else route.abort())
 pg=ctx.new_page();pg.set_default_timeout(10000)
 try:
  login(pg);drv=Driver(pg);p=historic.Proba(drv,str(artifact));p.ghid();drv.captura('guide');result('selects',pg.locator('.z-center:visible select').evaluate_all('(xs)=>xs.map(x=>[...x.options].map(o=>o.textContent))'))
  codes=[sql(f"SELECT value FROM adempiere.m_product WHERE ad_client_id=11 AND m_product_id={x}") for x in (123,124,i['no_cost'])]
  query('baseline');did,res=p.pas_document(codes[2],1,'no-cost');query('after no-cost click');result('no cost UI',{'did':did,'summary':res[:900]});p.inchid_mesaje()
  did,res=p.pas_document(codes[0],2,'two-lines',codes[1],-1);query('after prepare by button');result('DR via UI',{'did':did,'summary':res[:750]})
  if did:
   p.deschid();drv.captura('inventory-detail');result('native draft cost fields',p.casete());p.buton_inv('Validez',did,'CO');drv.captura('after-validation');query('after validate by button')
 except Exception as e:
  result('limit',str(e)[:650]);pg.screenshot(path=str(artifact/'stop.png'));result('visible UI at stop',pg.locator('body').inner_text()[-1500:])
 finally:ctx.close();br.close()
