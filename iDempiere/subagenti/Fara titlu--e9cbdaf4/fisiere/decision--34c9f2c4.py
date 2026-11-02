from pathlib import Path
import hashlib,collections,json,datetime
from decimal import Decimal as D
O=Path(__file__).parent;E=O.parent;R=E.parent;B=E/'R4_zone/A03';G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
def read(p):return json.loads(p.read_bytes())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf8')
z=read(B/'A03_raport.json');assert h(B/'A03_raport.json')=='6ba5483f9812384eba26aae19daf1b1a35f4c9b77e3b3339ab47f8793fa8c834'
for f,a in z['evidence_manifest'].items():assert h(E/f)==a['sha256']and (E/f).stat().st_size==a['bytes'],f
bridge=read(B/'dovezi/Legaturi_401_R6_verificate.json')['rows'];assert len(bridge)==len({v['technical']for v in bridge})==401
for b in bridge:
 for k in ('R4','R6'):assert h(E/b[k+'_file'])==b[k+'_sha256_checked']
r6=read(E/'R6/Registru_reexecutare_R6.json')['records'];team={v['criterion']:v for v in r6 if v['owner']=='A03' and v['R6_state']=='NEEXECUTAT'};src=read(B/'dovezi/A03_R6_criterii.json');assert len(src)==599 and {v['id']for v in src}==set(team)
ds=[]
for a in z['criteria']:
 i=a['criterion_id'];assert i in team and h(E/a['R6_case'])==a['R6_case_sha256'];j=read(E/a['R6_case']);c=next(v for v in j['operative_criteria_and_audit_criteria']+j['R3_new_criteria']+j['R4_new_criteria']if v['id']==i);assert a['R6_requirement_verbatim']==c['normative_content'] and a['R6_oracle']==c['expected_oracle'];assert a['R6_before']==c['current']['status']
 for f in a['evidence_refs']:assert h(E/f['file'])==f['sha256']
 ds.append(dict(id=i,decision_source=a['R4_classification'],norm=c['normative_content'],scope=a['remaining'],specific_readback=a['observed_and_expected'],evidence=a['evidence_refs'],A11='ACCEPT_LA_ORACOLUL_LITERAL_ÎN_ARIA_SUITĂ/TEST'if a['R4_classification']=='PASS_ORACOL_CURENT'else a['R4_classification']))
assert len(ds)==26;counts=collections.Counter(x['decision_source']for x in ds);assert counts['PASS_ORACOL_CURENT']==18
zz=read(B/'dovezi/static_contracts_R4.json')
for f in zz['labels']:
 p=G/f['file'];assert h(p)==f['sha256'];lines=[q.split('\t')for q in p.read_text(encoding='utf8').splitlines() if q.strip()and not q.startswith('#')];assert len(lines)==f['keys'] and len({q[0]for q in lines})==len(lines);assert all(len(q)==3 and all(y.strip()for y in q)for q in lines)
race=read(B/'dovezi/T58_race_native.json');ac=collections.Counter();overlap=[]
for v in race['attempts']:
 assert v['VC_without_AMORT']==False;ac[v['first_launch']]+=1;calls=v['calls'];times=[(datetime.datetime.fromisoformat(a['start']),datetime.datetime.fromisoformat(a['finish']))for a in calls];ms=(min(b for a,b in times)-max(a for a,b in times)).total_seconds()*1000;assert ms>0;overlap.append(round(ms,2));assert len(calls)==2
assert len(race['attempts'])==10 and list(ac.values())==[5,5]
ui=read(B/'dovezi/T58_ZK.json');assert ui['button']['disabled'] and int(ui['before_count'])==int(ui['after_count'])==0 and 'pasul 5' in ui['button']['tooltip']
tree=read(B/'dovezi/T58_positive_and_reverse.json');fx=tree['facts'];sum_by=collections.defaultdict(lambda:[D(0),D(0)])
for doc,num,state,posted,fi,account,sc,dr,cr in fx:
 assert state=='CO' and posted=='Y' and sc=='200000';sum_by[num][0]+=D(dr);sum_by[num][1]+=D(cr)
assert sum_by['INCH-1']==[D(100),D(100)]and sum_by['INCH-2']==[D(220),D(220)]
assert [(v['op'],v['reverse'],v['isError'])for v in tree['operations']][-3:]==[('VC',False,False),('AMORT',True,True),('VC',True,True)]
for o in ds:
 if o['id']=='T58-R2-006':o['A11']='ACCEPT_REFUZ_UI_PREVENTIV: buton dezactivat cu motiv și numărătoare 0→0; nicio cerere forțată.'
 if o['id']in('T58-R2-013','T58-R2-014'):o['A11']='ACCEPT_10_PERECHI_OBSERVATE: 5 preferințe de pornire pe sens, intervale HTTP suprapuse; nu toate intercalările posibile în DB.'
 if o['id']=='T176.01-R3-001':o['A11']='ACCEPT_XML_D100_DIN_2023: 150 pe bază1000 și plata850, martor fără sponsor1000 și mutant999 respins. Eligibilitatea unei cheltuieli în firma reală, transmiterea și certificarea perioadelor diferite nu se deduc.'
 if o['id']=='T256-R2-017':o['A11']='PARȚIAL: 34/0 în familie; scriptul la linia722 nu mai este ultima comandă. Condiția statică „ultimul bloc” NU este atinsă la cutoff, chiar dacă restul funcționează.'
 if o['id']=='T03.05-R3-001':o['A11']='PARȚIAL: accesul la etapa DUK a eșuat în execuția nominală; validarea separată de D100 nu suplimentează acel traseu.'
 if o['id']=='T176.01-R3-002':o['A11']='NEEXECUTAT: progresul jobului în UI nu a fost măsurat.'
q3=read(E/'A11_control_consolidari_A01_A03_R3.json')['reports']['A03'];rub=read(R/'A11_rubrica_control.json');masks=['11111','00010','10001','11110','10111','10101','00111','11011','11101','11100']
notes=['36 controale și 10 fluxuri, toate 125 amprente rehash. 401 legături de task pe R4 și R6 și 599 crit./151 taskuri regăsite. Cele trei referințe la draft sunt corectate și editările istorice păstrate. QC01-R3 acum acceptat.','26 criterii nominale din 599, dintre care 18 la oracolul declarat numai. Niciuna dintre cele 573 din afara lotului nu își schimbă starea.','Deschidere ZK T58 autentică; lângă pasul VC buton dezactivat, explicație privind pasul 5 și 0→0. QC03-R1 acordat în domeniul observat. Nu sunt demonstrate toate rolurile, recuperările sau capitolele.', 'AMORT, VC și inversarea interzisă sunt măsurate. 10 perechi, cinci preferințe de lansare în fiecare sens, toate cu suprapunere HTTP și zero anomalii după rezultat. QC04-R4 acum acordat în domeniul declarat.','ERP real de test, note CO/Y cu scheme și monede. Balanța 7802,38 este suma aritmetică 4217,50 și 3584,88 în două monede; operația contabilă nu poate agrega neselectiv USD și EUR.','Sunt legături pe jurnal/închidere nativă, dar nicio certificare tuturor celor 10 fluxuri și/cazuri economice.','Un rol nominal dintr-o organizație. Comportamentele de vizibilitate pe alte roluri rămân neacoperite.','Distinge politica modelelor contabile native și urmarea ei în plugin. F05 constatată la SAGA, fără oracol aprobat care afirmă că schema secundară trebuie redusă ori păstrată pe toate firmele.', 'Independent DUK Offline pe două produse XML, pozitiv/zero și mutant, plus loguri ale ferestrei de concurență. Nu se certifică încercările extremale nepuse în probă.', 'F01–F06 rămân nominal, fără dublare NIR/scheme; pilotul UI și politica secundară sunt încă deschise.']
qc=[]
for c,m,p,n in zip(rub['criteria'],masks,q3['individual_50'],notes):
 a=[dict(id=i['id'],text=i['text'],earned=0.2 if y=='1'else 0,R3_earned=old['earned'])for i,y,old in zip(c['report_subchecks'],m,p['subchecks'])];qc.append(dict(id=c['id'],title=c['title'],earned=round(sum(v['earned']for v in a),1),subchecks=a,rationale=n))
evidence={'D100_rereproduced':read(O/'DUK_reproductions.json'),'D100_digest':h(O/'DUK_reproductions.json'),'T58_after_http_receipt_states':dict(sum_by),'UI':{'account':ui['actor'],'before':0,'after':0,'control':ui['button']},'T58_http_overlap_ms':overlap,'launch_order_frequency':dict(ac),'26_selected':counts,'remaining_outside':573,'distinct_source_evidence':125,'401_links_between_snapshots':len(bridge),'source_files_rehashed_for_401':802}
w=O/'readback_A03_R4.json';write(w,evidence)
report=dict(reviewer='A11',source='R4_zone/A03/A03_raport.json',sha256=h(B/'A03_raport.json'),gate='RELUARE; 26 criterii adjudecate, dintre care 18 oracole tehnice satisfăcute în aria exactă.',quality_score=round(sum(c['earned']for c in qc),1),verified_subchecks=sum(m.count('1')for m in masks),out_of=50,product_score=None,R3_quality=q3['R3_score'],criteria=qc,selected=ds,denominators={'R6_A03_NEEXECUTAT':599,'distinct_tasks_R6_A03':151,'historic_401_task_bridge_not_acceptance':401,'selected_results':counts,'outside_selected_lot':573,'unexecuted_in_selected':1},controls=[dict(id=c['control_id'],R4_state=c['R4_status'],scope=c['observed_R4'],open=c['still_open'],decision='ACCEPT_DOVADA_NOMINALĂ; FĂRĂ_PASS_GLOBAL')for c in z['controls']],pipelines=[dict(id=p['pipeline_id'],observation=p['R4_observation'],scope=p['tier'],full=False)for p in z['pipelines']],findings=[dict(id=f['finding_id'],result='PĂSTREZ CONSTATAREA ȘI LIMITA' if f['finding_id']not in ('A03-F05','A03-F06')else 'CONFIRMARE DELIMITATĂ ȘI RECONCILIERE CU TITULARUL',factual_r4=next(v['current']for v in z['changes_relative_R3']if v['finding']==f['finding_id'])) for f in z['prior_findings']],issues=['T256-R2-017: condiția statică „testul să fie ultimul bloc” nesatisfăcută la head. Etichetează explicit subcondiția la următoarea revizie; păstrează 34/0 drept rezultat separat al suitei.','Pentru F01/F02 rulați balanță și VC cu schema explicită per firmă și contra-moneda, cu reconciliere pe fiecare cont. Pentru F05 solicitați politica normativă, nu infereți din efectul observat.','Continuați prioritizat cele 573 netestate în lotul A03, cumulat cu registrul A12 curent, fără dublare. Pentru rolurile contabile și non-contabile exercitați revenirea din refuz în aceeași navigare și starea documentelor după proces.'],scope='T58 este identificator agregat al cerințelor istorice și T158 succesor. Acest raport validează oracolele selectate în versiunea curentă, nu stare de montare istorică. Rezumatul în lei și moneda reală EUR rămân lucruri diferite.',independent={'file':w.name,'sha':h(w),'D100':h(O/'DUK_reproductions.json'),'scripts':{p.name:h(p)for p in [O/'duk.py',O/'decision.py']}})
p=E/'A11_control_A03_R4.json';write(p,report);print(h(p),report['quality_score'],h(w))

