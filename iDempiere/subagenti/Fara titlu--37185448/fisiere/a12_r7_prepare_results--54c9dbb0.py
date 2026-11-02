from a12_r7_pg_cui import *
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict,Counter
from functools import lru_cache
import base64
ROOT=E.parent;R=E/'R7';R.mkdir(exist_ok=True)
for k in ['taskuri','fise_html','probe','metoda']:(R/k).mkdir(exist_ok=True)
old=E/'R6';input_report=old/'A12_raport.json';assert sha(input_report)=='605241436af8ba8a4030bc127b81c993b36e4cc6ce06b119fd12ebbbdef03c09';assert sha(E/'A11_control_A12_R6.json')=='becb2a61e494c79cabb44ec47ad6b7fb3baec43e9474fa14158bbbf467dfa632'
classp=RP/'Clasificare_nominala_1587.json';tri=rd(classp)['records'];cix={z['criterion']:(i,z)for i,z in enumerate(tri)}; prior=rd(input_report);od=rd(old/'Dovezi_criterii.json');ev=od['evidence'];rev=defaultdict(list);candidates=defaultdict(list);contexts=defaultdict(list)
def H(b):return hashlib.sha256(b).hexdigest()
def J(v):return H(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
@lru_cache(maxsize=512)
def jd(p):return rd(p)
@lru_cache(maxsize=4096)
def dig(p):return sha(p)
def get(v,ptr):
 if not ptr:return v
 for t in ptr[1:].split('/'):
  t=t.replace('~1','/').replace('~0','~');v=v[int(t)]if isinstance(v,list)else v[t]
 return v
def add(cid,p,ptr,expected,observed,scope,level,result,phase='current',role=None):
 src=p.relative_to(ROOT).as_posix();vv=get(jd(p),ptr);loc={'kind':'json-pointer','pointer':ptr,'canonical_value_sha256':J(vv)};eid='EV7-'+J([src,ptr,level])[:22]
 ev[eid]={'source':src,'pointer':ptr,'sha_or_oid':dig(p),'strict_primary_locators':[loc],'level':level,'content_or_observation':observed,'limit':scope}
 q={'evidence':eid,'expected':expected,'observed':observed,'qualification':scope,'result':result,'phase':phase,'actor_or_target':role};target=contexts[cid]if phase=='context' else candidates[cid]
 if not any(x['evidence']==eid for x in target):target.append(q)
P148=RP/'148_predicate_prin_stack.json';q148=rd(P148)['rows'];assert len(q148)==148
for i,q in enumerate(q148):
 k=q['evidence'];rec=q['comparison'];ev[k]['R7_runtime_source']={'file':P148.relative_to(ROOT).as_posix(),'sha':dig(P148),'pointer':'/rows/'+str(i),'result':rec['code_state'],'source_condition':rec['source_anchors'],'number_concrete_child_assertions':len(rec['child_assertions']),'observation_line':rec['trace_line'],'assigned_beyond_component':False}
 add(q['criterion'],P148,'/rows/'+str(i),'Reveniți la predicatul individual sau la grupul executat pentru mesajul din R5.',{'site':rec['stack_exact'],'status':rec['code_state'],'R5':rec['r5_actual'],'R7':rec['r7_actual'],'children':len(rec['child_assertions'])},rec['limit'],'CALLSITE_JVM_RECONSTITUIT',rec['code_state'],role=rec['target'])
q3=RP/'T03_topologie_si_lacat_PG.json';d=jd(q3)
for i,v in enumerate(d['postgres_dedicated_fixture']):add('T03-R2-039',q3,'/postgres_dedicated_fixture/'+str(i),'Cheie client/lună comună → blocare până la eliberare; alte luni/firme → acces concurent; rollback elimină scrierea inițială.',v['case']+': '+str((v['blocked_before_release'],v['B_sees_before_writing'],v['rows_final'])),d['qualification'],'PG_ADVISORY_DOUĂ_SESIUNI','URMĂ_DE_LACĂT_PERSISTENT_SEPARAT',role=[v['A'],v['B']])
add('T03-R2-039',q3,'/physical_observed_readonly','Stabilește dacă UI e o a doua JVM pe cabinetul verificat.',d['physical_observed_readonly'],d['product_conclusion'],'TOPOLOGIE_CESIRO','TOPOLOGIE_1_JVM_ȘI_RELEU',role='inspecție read-only')
cuip=RP/'T06_preconditii_Garden_PG_JAR.json'
for i,v in enumerate(jd(cuip)['rows']):add('T06-R2-020',cuip,'/rows/'+str(i),v['expected'],v['actual'],'Cititorul folosește baza GardenWorld restaurată și arhiva sintetică; REST și persistența sunt probe separate.','JAR_CUI_CALCULAT','PREDICAT_CUI',role=v['target'])
for pname in ['T06_cabinet_nativ_egal_diferit.json','T06_cabinet_nativ_168_note.json','T06_cabinet_amprenta_integrala.json']:
 p=RP/pname;d=jd(p)
 for i,z in enumerate(d['tests']):
  match=z['archive_taxid']==z['cabinet_supplier_taxid'].removeprefix('RO');expect='CUI compatibil → proces acceptat'if match else 'CUI incompatibil → refuz specific de firmă, zero modificări.'
  obs={'native':z['native'],'actual_registry_before':z['before'],'actual_registry_after':z['after'],'delta':z['delta'],'id_hash':z['ids_fingerprint_after'],'entire_content_before':z.get('content_fingerprint_before'),'entire_content_after':z.get('content_fingerprint_after')}
  for cid in ['T06-R2-020']+(['T06-R2-008']if not match else []):
   add(cid,p,'/tests/'+str(i),expect,obs,'Cabinet A12 exclusiv, rol 102; 168 poziții create de proces în proba extinsă. Totalul declarat de proces pe martor este 336, iar numărul ID persistente este 168. Acesta nu este un test de postări contabile duplicate.','ERP_CUI_ȘI_REGISTRU','REFUZ_NATIV_MĂSURAT'if not match else'MARTOR_NATIV_CUI_EGAL',role='GardenAdmin, tenant 11')
  if z['tag']=='same168':add('T06-R2-017',p,'/tests/'+str(i),'Rețeta istorică solicită rezultatele pe rând/cont/interval definite în C-17. În această rulare sunt 168 note artificiale în ianuarie.',obs,'Datele native diferă de arhiva istorică și nu dovedesc repartizarea verdictelor istorice.','ERP_CUI_ȘI_REGISTRU','DOMENIU_168_DIFERIT_DE_FIȘA_ISTORICĂ',phase='context')
  if z['tag']=='same168':add('T171-R2-001',p,'/tests/'+str(i),'Registrul compară mișcările bancare și explică diferențele; cazul sintetic este o lună, 168 note SAGA și zero linii EvA.',obs,'T171 este succesor nominal al T06. Rezultatul nu eșantionează toate mișcările din 2026, nici cursurile și explicațiile pentru alte firme.','ERP_CUI_ȘI_REGISTRU','RECONCILIERE_NUMAI_SAGA',phase='context')
p=RP/'Cazuri_locale_nominale_79.json'
for i,v in enumerate(jd(p)['records']):
 for j,z in enumerate(v['bound_results']):
  add(v['criterion'],p,'/records/'+str(i)+'/bound_results/'+str(j),v['expected_from_criterion_source']or v['branch_selector'],z['observed'],v['limit'],'ASERȚIUNE_DE_COMPONENTĂ_CU_CALLSITE','FAIL_ÎN_TEST'if z['observed'].upper().startswith('FAIL')else 'SUBCAZ_ÎN_FIȘA_ORIGINALĂ',role=v['target'])
p=RP/'SQL/Matrice_SQL_reala_R7.json';q=jd(p)
for i,v in enumerate(q['rows']):
 if 'all_markers'not in v:continue
 for cid in q['expectations_before_mutation'][v['suite']]['criteria']:
  marks=[(j,z) for j,z in enumerate(v['all_markers'])if z['value'].lstrip().startswith('FAIL')]
  if v['variant']=='original':
   # Only scopes whose own selectors actually identify the criterion; do not distribute all markers by suite.
   ids={'T159-R2-032':'armoniz|MANUAL|C-29','T190-R2-020':'SQL_NIVELURI','T190-R2-030':'firme|firma B|firma A','T331-R2-004':'SQL_FARA_NC','T331-R2-006':'sqlNecontabile|SQL_FARA_NC','T354-R2-013':'SQL_LISTE.*firma|SQL_PRODUS.*firma','T354-R2-019':'invalid|nestocabil|invalidă','T217-R2-004':'→ AWB|→ deconturi'}
   import re
   marks=[(j,z)for j,z in enumerate(v['all_markers'])if re.search(ids.get(cid,'a^'),z['value'],re.I)][:4]
  else:
   selectors={'T159-R2-032':'manual|seed|armoniz','T190-R2-020':'SQL_NIVELURI|firma A|firma B','T190-R2-030':'firma A|firma B|firme|inactivul','T331-R2-004':'SQL_FARA_NC','T331-R2-006':'SQL_FARA_NC|sqlNecontabile','T354-R2-013':'firma|firm|liste','T354-R2-019':'invalid|nestocabil','T217-R2-004':'AWB'}
   marks=[(j,z)for j,z in marks if re.search(selectors[cid],z['value'],re.I)]
  for j,z in marks:
   add(cid,p,f'/rows/{i}/all_markers/{j}',q['expectations_before_mutation'][v['suite']]['expected'],z['value'],'PG sintetic cu SQL emis din JAR, nu o operație de click sau un document contabil nativ. Starea mutantului nu este o eroare în software-ul nemodificat.','SQL_PRODUS_ȘI_MUTANT','CONTRAPROBĂ_MUTANT_DETECTATĂ'if v['variant']=='mutant'else'SUBCAZ_SQL_DE_PRODUS',role=v['target'])
h=RP/'Istoric_verdicturi_nominale.json'
for i,v in enumerate(jd(h)['records']):
 direct=[(j,x)for j,x in enumerate(v['documents_with_a_decision_line'])if not x['authority'].startswith('ancestor')]
 # Only explicitly historical activity, not arbitrary functional deliverables on the same generic task.
 if not direct or v['question_type']not in ('plan','method','documentary'):continue
 for j,z in direct[:2]:
  nominal=(v['question_type']=='plan' and 'plan' in z['title'].lower() and (z['title'].startswith('# '+v['task']+' ') or re.search(r'\b'+re.escape(v['task'])+r'\b',z['title'],re.I)))
  add(v['criterion'],h,f'/records/{i}/documents_with_a_decision_line/{j}','Planul sau metoda cerută are un document de audit nominal cu verdict; se verifică separat faza și scopul.',{'title':z['title'],'path':z['path'],'decision':z['actual_lines_with_authored_decision'][0]},'Este o urmă documentară în Git, nu reexecutarea produsului, avizul asupra altui subtask sau o atestare a identității autorului.','DOCUMENT_PRIMAR_ISTORIC','AUDIT_PLAN_NOMINAL_DOCUMENTAT'if nominal else 'DOCUMENT_DE_SFERĂ_CORELATĂ',phase='closure'if nominal else 'context')
p=E/'R4_zone/A03/dovezi/Registru_incremental_01.json';assert dig(p)=='5e7b30984f6f23da6d686764317f2e8c8f98a16a9f042d136b81cace7227cfa6'
for i,v in enumerate(jd(p)['claims']):
 assert dig(old/('taskuri/Fisa_'+v['task']+'.json'))==v['R6_case_sha256']
 for ref in v['evidence_refs']:
  assert dig(E/ref['file'])==ref['sha256'],ref['file']
 if str(v['R4_classification']).startswith('NEEXECUTAT'):continue
 add(v['criterion_id'],p,'/claims/'+str(i),v['R6_oracle'],v['observed_and_expected'],str(v['remaining'])+' Datele de control aparțin ediției și fixturii revendicate; avizul A11 asupra rezultatului individual rămâne separat.','A03_PROBE_FUNDAMENTATE_ÎN_LOGURI',v['R4_classification'],role=v['method_and_actor'])
p=E/'R4_zone/A06/probe/probe-detaliu-proprietate.json';d=jd(p)
for i,v in enumerate(d['runs']):
 for cid in ['T216-R2-001','T216-R2-002','T216-R2-005','T216-R2-006','T216-R2-007']:
  add(cid,p,'/runs/'+str(i),'Pe comanda Q, validația trebuie să poată continua către comanda ERP și apoi, în condițiile indicate de cerință, factura. Caz martor cu seller.cui completat.',v['readout'],'DOAR comanda/originea testată. DTO are două linii; persistate 0, V01 rămâne. Adăugarea seller.cui în DTO elimină V02. Niciun C_Order sau C_Invoice nu a fost atribuit manual acestei Q.','A06_Q_DOUĂ_VARIANTE','TRASEU_Q_BLOCAT_V01',role=v.get('target'))
p=E/'R7_pregatire/G3/Combinatii_CPP_S1_S2.json';assert dig(p)=='77d068975f239f73f61861e23bbd65634c49aacb9a89b5ae569eca8413e070fb';d=jd(p)
for i,v in enumerate(d['actual']):
 for cid in ['T354-R2-008','T354-R2-021','T354-R2-027']:
  add(cid,p,'/actual/'+str(i),'Pool CPP comun: 120 bucăți din fiecare, S1=6+6+6 →20, S2=3+3+3→40. Cererile concurente în spațiul combinatorial nu pot depăși poolul. Nu se acordă cazul exact al altor fixturi automate.',{'cases':v['cases'],'mismatches':v['mismatches'],'rollup':d['rollup']},'Funcțiile reale alocaGrupuri/disponibilSet, matrice de 16.632 combinații și trei ordini. Nu este o rezervare concurentă din ERP, publicare web sau probă fizică multi-G1.','G3_ALTERNATIVE_CPP_CPA','ARITMETICĂ_INDEPENDENTĂ_FĂRĂ_ERP',role=v['target'])
p=E/'R7_pregatire/JAR/Diferente_instalate_T224_T227.json';assert dig(p)=='260c0448ced970907ec99fa77c53eee706ac21eef81d8a5c83787f103163d82b'
for i,v in enumerate(jd(p)['targets']):
 for j,o in enumerate(v['classes']):
  cls=o['class'];cids=(['T227-R2-027','T227-R2-036']if cls.endswith('.VerificareImportSaga')or cls.endswith('.ParteneriSoldSql') else ['T224-R2-014']if cls.endswith('.WSagaIntrariForm')else [])
  for cid in cids:add(cid,p,f'/targets/{i}/classes/{j}','Verificare binară a clasei/simbolurilor la JAR-ul exact necesar ramurii.',{'class':cls,'present':o['present_in_this_bundle'],'symbols':o['symbol_declarations']},'Lipsa din JAR-ul instalat CESIRO nu atestă lipsa din Git, defect în toate căile sau neîndeplinirea unui task declarat nemontat.','MONTAT_VERSUS_GIT','METADATE_PE_CAZ',phase='context',role=v['target'])
ux=E/'R6_supliment/A12_UX_NIR_provenienta.json';d=jd(ux)
for cid,edges in d['by_criterion'].items():
 for j,v in enumerate(edges):add(cid,ux,'/by_criterion/'+cid+'/'+str(j),v['expected_in_this_test'],{'class':v['form_class'],'role':v['role'],'session':v['AD_Session_ID'],'result':v['observed']},'Deschiderea formei și prezența controalelor sunt confirmate pentru rol. Nu s-au executat toate efectele din cerința de business.','UI_DOM_PE_ROL','NOMINAL_NAVIGARE',phase='context',role=v['role'])
p=E/'R6_supliment/A12_T36_T36_31.json';d=jd(p)
for i,z in enumerate(d['rows']):add('T36.31-R3-001',p,'/rows/'+str(i),'Soldul facturii respectă semnul alocărilor și proiecția numerică a restului.',z['observed'],z['scope'],'SQL_REST_FACTURĂ','SUBCAZ_SQL',role=z['target'])
# Read actual source/signed status for supplemental case links; zero attribution if an EX source does not cover the original task.
ex=E/'A11_control_CESIRO1_EX01_EX08.json';exd=jd(ex)
ss=RP/'Masuratori_statice_nominale_R7.json'
for i,v in enumerate(jd(ss)['rows']):
 add(v['criterion'],ss,'/rows/'+str(i),v['expected_subcase'],v['observed_now'],v['limit'],'RECITIRE_GIT_SAU_BYTECODE_DETERMINISTĂ',v['comparison'])
for cid,fn,h,pt in [('T58-R2-005','T58_native_gate.json','eacd475b6c161289a40af690fa061f5dcdaa77a58971b0a2f2b96a83c5a8a7b1','/probes/0'),('T58-R2-006','T58_ZK.json','d9eeb704ec6e67ddb1aa17057891dc3952f701ff5d5df5464e967dfebd10cfe7','/button')]:
 src=E/'R4_zone/A03/dovezi'/fn;assert dig(src)==h;dv=jd(src)
 add(cid,src,pt,'Cu ordinea activă și amortizare încă nefăcută, validarea VC trebuie oprită înainte de scriere.',get(dv,pt),'T58-R2-005 protocoale REST native. Pentru T58-R2-006, „Validez” este dezactivat și are un tooltip, zero jurnale înainte/după; nu a existat clic sau dialog de eroare. Nu extrapola la alte perioade sau funcții.','PROBE_NATIVĂ_A03','REFUZ_EVALUAT_ÎN_CANALUL_NOMINAL',role='GardenAdmin, client 11, rol 102, organizație 11')
pp=E/'R4_zone/A03/dovezi/T58_positive_and_reverse.json'
if pp.is_file():
 assert dig(pp)=='96372c11017e17ca94b78f1ab290ff9c52e8807a282489c2198af5d8a06d422a'
 for i,o in enumerate(jd(pp)['operations']):
  cid='T58-R2-010' if o['reverse'] else 'T58-R2-009'
  add(cid,pp,'/operations/'+str(i),'Operațiile premergătoare sunt validate după aplicabilitate înainte de crearea unei singure note VC; cu VC făcută, inversarea AMORT este refuzată.',o,'Contabilitate GardenWorld cu două scheme. A_Depreciation_Exp este o fișă de amortizare, nu o factură. Difful istoric al devalidării nu este demonstrat prin această rulare.','ERP_INCHIDERE_A03','PAS_NATIV_NOMINAL',role=jd(pp)['actor'])
explan=E/'supliment_CESIRO1/Plan_CESIRO1_R3.json';exrefs={z['technical']:z['EX'] for z in jd(explan)['origin_criteria']}
wr(R/'probe/Rezultate_R7.json',{'new':dict(candidates),'context':dict(contexts),'A11_EX':{'file':ex.relative_to(ROOT).as_posix(),'sha':dig(ex),'case_reviews':{k:{'pointer':'/cases/'+k,'data':v}for k,v in exd['cases'].items()},'formal_origins':exrefs}})
print('r7 new',len(candidates),sum(map(len,candidates.values())),'contexts',len(contexts),sum(map(len,contexts.values())))

