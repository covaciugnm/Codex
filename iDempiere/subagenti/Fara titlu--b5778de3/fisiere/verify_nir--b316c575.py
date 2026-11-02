import sys,json,hashlib,datetime
from pathlib import Path
import fitz
from bs4 import BeautifulSoup
d=Path(__file__).resolve().parent
def meta(path): return {"path":str(path.relative_to(d)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size}
def ej(p):return json.loads(p.read_text(encoding='utf-8-sig'))
o=ej(d/'run3/obs.json');r=ej(d/'runtime.json');conf=ej(d/'config.json');initial=ej(d.parent/'nir-document-source.json')
assert not conf['before'] and len(conf['after'])==1 and r['period_settings']==[] and r['guards']==[['0','System'],['11','GardenWorld']] and r['active_schedulers']=='0'
assert r['bundles']==[{'path':'/opt/idempiere/plugins/com.eva.ro.contab_13.0.0.jar','sha256':'00f261462636475c1612a5d4afde76515d7ed8c8dab0dd53e19fd6811cecbee2'}]
assert r['doc_post_preview'][0][0]=='1000002' and r['doc_post_preview'][0][2]=='CO' and float(r['doc_post_preview'][0][3])==570
cases=[]
for case in o['cases']:
 label=case['id'];inp=case['field_readback'];q=(7,3) if label=='control' else (3,5)
 expected='370,00';actual='370,00' if label=='control' else '530,00'
 html=d/'run3'/(label+'.html');pdf=d/'run3'/(label+'.pdf');png=d/'run3'/(label+'.png')
 assert meta(html)['sha256']==case['html_sha256'] and meta(pdf)['sha256']==case['pdf_sha256']
 soup=BeautifulSoup(html.read_text(encoding='utf8'),'html.parser');rows=[[c.get_text(' ',strip=True) for c in tr.find_all('td',recursive=False)] for tr in soup.select('table tr')]
 productrows=[row for row in rows if len(row)==7 and row[0] in ('1','2')];assert len(productrows)==2 and [int(y[4]) for y in productrows]==list(q)
 with fitz.open(pdf) as doc:
  assert len(doc)==1;text=doc[0].get_text()
 assert actual in text and 'Azalea Bush' in text and 'Elm Tree' in text and 'PREVIZUALIZARE' in text
 cases.append({'case':label,'input_exact':inp,'rows_HTML':productrows,'total_HTML':actual,'total_PDF':actual,'expected':expected if label!='invalid' else 'Mesaj de respingere sau corecție fără transferul cantității între linii','delta_against_control_lei':0 if label=='control' else 160,'artifacts':[meta(p) for p in (html,pdf,png)],'pdf_pages':1})
out={'schema':'eva.A04.NIR.R6.after_configuration','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finding':'A04-F01','code_cutoff':'6df998aee0e514d30856c461962afe99ebd0d113','image_id':r['image_id'],'bundle':r['bundles'][0],'native_window':'com.eva.ro.contab.form.WSagaIntrariForm / Intrări - lei → NIR-P01-R6-002 (C_Invoice_ID=1000002) → Documente… → NOTĂ DE RECEPȚIE ȘI CONSTATARE DE DIFERENȚE (14-3-1A) → Previzualizez','actor':'GardenAdmin, rol 102, organizația 11, clientul sintetic GardenWorld. Scheduler-e inactive, fără rută la parteneri.','setup':'Flag sintetic explicit EVA_SETARI_FIRMA_MIGRAT=Y, AD_SysConfig_ID 2000095005 pentru clientul 11/org 0, singura modificare de configurare. Zero rânduri EVA_SetareFirmaPerioada. Cache reîncărcat prin callback-ul normal din WSagaSetariFirmaPerioadeForm (SetariFirma.dupaCommit și reset AD_SysConfig) la încheierea încercării de migrare refuzate în clientul demo. Fanionul nu provine dintr-o migrare executată cu succes.','cases':cases,'document_source':initial,'source_after':r['doc_post_preview'],'execution_result':'POSTCONFIGURARE ZK REPRODUS. Control 7/3 emite previzualizare 370 lei; gol/3 și invalida/3 afișează ambele 530 lei și atribuie diferența primului articol.','impact':'Diferență de 160 lei în previzualizarea documentului. Factura-sursă rămâne CO și 570 lei cu cantitățile 7 și 5. Nu a fost exercitat butonul Emit și tipăresc sau dovedită o mișcare eronată de stoc/contabilitate. PDF reprezintă imprimarea Chromium a previzualizării generate de ERP.','quality_review':None,'artifacts':[meta(d/p) for p in ['config.json','runtime.json','run3/obs.json','run3/form.png','run3/callback.png','seed_config.py','nir_post_ui.py']]}
(d/'rezultat.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(meta(d/'rezultat.json'))
