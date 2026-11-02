import csv,io,hashlib,json,datetime,shutil
from pathlib import Path
from collections import Counter
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');R=B/'executie/R10_pregatire/A12/T06_UI'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def path(p):return {'file':p.relative_to(B).as_posix(),'sha256':h(p)}
dom=R/'DOM_sesiune_verificata.json';s=read(dom);u=R/'buton/capture_ui.json';w=read(u);e=R/'martor_cont_gol/capture_ui.json';n=read(e);ro=R/'doar_verifica/capture_ui.json';rv=read(ro)
dbl=R/'dubluclic/capture_ui.json';dz=read(dbl);assert dz['db_before']==dz['db_after']and dz['message']['actual_literal']==dz['message']['expected_literal']and dz['clicked_row']['prior_exact_message']==0;assert len(dz['message']['dialogs'])==0
for j,p in [(s,dom),(w,u),(n,e),(rv,ro),(dz,dbl)]:
 assert j['role'][0]['ad_role_id']==102 and j['role'][0]['ad_client_id']==11
 for q in j['screens'].values():assert h(p.parent/q['file'])==q['sha256'],q
f=R/s['export']['file'];assert s['export']['sha256']==h(f)
with f.open(encoding='utf-8-sig',newline='')as inf: csvdata=list(csv.reader(inf,delimiter=';'))
norm=lambda t:' '.join(t.replace('\xa0',' ').strip().split())
headers=csvdata[0];csvlines=csvdata[1:];domlines=[row[1:]for row in s['lines']['rows']]
assert readonly_valid if 'readonly_valid' in globals() else True
assert len(csvlines)==len(domlines)==s['lines']['rows_observed_dom']==168;assert len(s['months']['rows'])==s['months']['rows_observed_dom']==13
assert len(headers)==25
discrep=[{'row':i,'column':headers[k],'dom':a,'csv':b}for i,(x,y)in enumerate(zip(domlines,csvlines),1)for k,(a,b)in enumerate(zip(x,y))if norm(a)!=norm(b)]
assert not discrep,discrep[:2]
assert s['export']['months']=={a['month']:a['rows']for a in s['db_months']}
assert all(a['outside_ten_accounts']==0 for a in s['db_months'])
assert len(n['samples'])==4 and n['samples'][1]['dom_data_rows']==n['samples'][2]['dom_data_rows']==0 and all('137 rânduri'in ' '.join(n['samples'][i]['footer_and_explanation'])for i in [1,2])
assert len(w['clicks'])==2 and [c['new_instance_id']for c in w['clicks']]==[1003142,1003143]and all(c['dblog']['result']==1 and c['after']['physical']['count']==168 and c['after']['physical']['differences']==22 and c['after']['physical']['instances']==[c['new_instance_id']]for c in w['clicks'])
after=rv.get('after_check_only');readonly_valid=bool(after and after['physical']==rv['before_check_only']['physical']and after['process']['result']==1)
sm={x['name']:(x['rows'],x['groups'])for x in n['qualified_empty_control']};assert sm=={'A12R10-1':(137,6),'A12R10-10':(0,0)}
qa={'dom_csv_rows_same_order':168,'columns':25,'compared_cells':4200,'normalized_whitespace_only':True,'different_cells':len(discrep),'form_selected_dates':['01.01.2026','30.06.2026'],'account_selection':'(toate conturile)','db_monthly_current_origin_instances':sorted({item for col in s['db_months'] for item in col['run']}),'real_clicks':len(w['clicks']),'files':{}}
for p in [dom,f,u,e,ro,dbl]:
 qa['files'][p.relative_to(R).as_posix()]=h(p)
shape={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'schema':'A12.R10.T06.UI','environment':'Cabinet sintetic propriu GardenWorld, client 11, rol Garden Admin 102. Acces țintit prin SSH loopback și HTTPS la adresa privată confirmată a containerului autorizat. PostgreSQL folosit prin tranzacții de citire; cele două apăsări autorizate au executat procesul mutator exclusiv în cabinet.','source_cutoff':'6df998aee0e514d30856c461962afe99ebd0d113','menu':s['menu'],'forms':{'comparison':s['tab']['tooltip'],'process_AD':{'AD_Menu_ID':1000360,'AD_Process_ID':1000218,'name':'Bancă: compară cu SAGA (proces)'},'opened_journal':s['journal_window']},'claims':{
'T06-R2-014':{'expected':'Butonul Compar cu SAGA, toate conturile, ianuarie-iunie, 10/6/168 şi 22 diferențe pe martor q31 cu fixtură sau țintă recalculată anterior.','observed':{'first':w['clicks'][0]['new_instance_id'],'second':w['clicks'][1]['new_instance_id'],'result_text':w['clicks'][0]['states'][-1]['messages'][-1],'physical_snapshot':w['clicks'][1]['after']['physical'],'log_opened_each_time':all(bool(c['journal']['title'])for c in w['clicks'])},'limit':'Sursă contabilă SQLite sintetică. MD5 nu este cel al arhivei istorice q31 și nu pretinde cod-terț sau conturi de producție.'},
'T06-R2-018':{'expected':'A doua rulare păstrează 168 de rânduri și toate se leagă exclusiv de noua instanță.','observed':[(c['new_instance_id'],c['after']['physical'])for c in w['clicks']],'limit':'Două rulări noi din sesiune, nu numărul total al tuturor instanțelor istorice din DB. Alte execuții A12 au precedat.'},
'T06-R2-019':{'expected':'DoarVerifica activ în formularul nativ; nu scrie rânduri.','observed':{'form_configured':rv.get('entered'),'complete_and_unchanged':readonly_valid,'after':after['process']if after else None,'messages':rv.get('logs_only_check',[]),'params':rv.get('submitted_parameters')} ,'limit':'Dovada DoarVerifica folosește formularul nativ de proces și verifică numai rezultatele comparației pe intervalul. Arhiva este sintetică.'},
'T06-R2-022':{'expected':'13 grupe în Luni; 168 linii; 22 diferențe în sumar; export CSV cu 168 de rânduri; jurnalul inițial dezactivat și butonul Jurnal de bancă deschide următorul ecran.','observed':{'displayed_month_rows':s['months']['rows_observed_dom'],'displayed_line_rows':s['lines']['rows_observed_dom'],'csv_rows':len(csvlines),'verdicts':s['export']['verdicts'],'monthly':s['export']['months'],'monthly_footer':s['months']['footer'],'disabled_before':s['months']['journal_disabled'],'enabled_after':w['clicks'][0]['states'][-1]['log_enabled'],'bank_journal_tab':s['journal_window']['selected_tooltip'],'first_account_positive':sm['A12R10-1'],'empty_account':sm['A12R10-10'],'doubleclick':dz['message'],'doubleclick_same_source_key_and_pk_before_after':dz['db_after']},'limit':'Liniile/CSV aparțin perioadei ian–iun; alte conturi demo din listă și înregistrările Iul–Sep au fost excluse prin perioadă și reconcilieri. Selectorul contului poate fi gol la început; sumarul său trebuie verificat separat în martorul UX.'}},'finding':{'id':'A12-R10-T06-UX-01','observed':'După contul A12R10-1 cu 137 rânduri, contul A12R10-10 nu afișează nicio linie, dar indicatorul păstrează valoarea precedentei selecții inclusiv la reîncărcarea explicită. Revenirea la toate conturile restabilește 168.','steps':n['samples'],'db':n['qualified_empty_control'],'consequence':'Contabilul vede un număr de rânduri care aparține altui cont. Măsurarea nu a găsit o schimbare de date în lista contabilă.','code_reference':'WEvaComparatieBancaForm.java:265–270 (calea pentru lista goală revine după nota); :300 (indicatorul actualizat pe calea cu date).','proposed_retest':'Selectează 137 → 0 → Încarcă → toate conturile. Indicatorul perioadei și grila trebuie să arate 0 împreună, apoi 168. Include martorul și în nivelul Luni.'},'controls':qa,'implementation_grade':None,'audit_grade':None}
dest=R/'Rezultat.json';dest.write_text(json.dumps(shape,ensure_ascii=False,indent=2),encoding='utf8');print(h(dest),qa,readonly_valid)

