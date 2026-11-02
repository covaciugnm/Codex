from pathlib import Path
import json, hashlib, datetime
from decimal import Decimal as D
from collections import Counter

base=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie')
cut=Path('D:/CodexWork/eva-audit-p01-readonly-20261102')
native=Path('D:/CodexWork/eva-audit-secondary-20261102/native')
target=base/'R4_zone/A05/A05_raport.json'
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def body(f): return json.loads(f.read_text(encoding='utf-8-sig'))
def atomic(fn,d):
    fn.parent.mkdir(parents=True,exist_ok=True)
    with fn.open('x',encoding='utf-8',newline='\n') as stream:json.dump(d,stream,ensure_ascii=False,indent=2);stream.write('\n')
manifest={}
def proof(key,name,expected=None):
    f=base/name
    actual=sha(f)
    if expected: assert actual==expected,(key,actual)
    manifest[key]={'file':str(f.relative_to(base)).replace('\\','/'),'sha256':actual,'bytes':f.stat().st_size}
    return body(f) if f.suffix=='.json' else None
prev=proof('R3','R3_zone/A05/A05_raport.json','3986fd91b4f4f5d5079fa0002c23f3e05b63b11ca1233e719f9af7ed0b6c27af')
rv=proof('A11_R3','A11_control_consolidari_A05_A06_A09_R3.json')['reports']['A05']
assert rv['R3_quality']==7 and rv['source'] == 'R3_zone/A05/A05_raport.json' and rv['sha256']==manifest['R3']['sha256']
proof('R2','R2_zone/A05_raport.json','fd871b4a22b753ea42d25ecb6935426d4612f76ed05a531d4aa97b9e189f9a26')
chain=proof('R6_CHAIN','Reverificare_Flux_S1_aviz_retur_R6.json','1a2e23d14bd8a85105153e2ca951290f712bea83b6a6936bdbfcf7122d026033')
contrast=proof('R6_T337','Reverificare_T337_setare_si_val.json','7231faed8f1c3281ba76808ca5020407e757830f488326375bab8db3e8bf5bcc')
raw,ret=[proof(key,path.removeprefix('executie/'),h) for key,(path,h) in zip(('W1_RAW','RMA_RAW'),chain['inputs'].items())]
alt,conf=[proof(key,'R6_pregatire/ERP/wms3/'+path,h) for key,(path,h) in zip(('W2_RAW','W2_SOURCE'),contrast['source_hashes'].items())]
site=proof('SITE_EX05','supliment_CESIRO1/probe/EX05.json','ccef80210b8570ca094c5249704e74141e7dfe49a0b8534205105303a352073b')
peer=proof('SITE_PEER','supliment_CESIRO1/probe/EX05_peer_A05.json','65c4105e490b49d103ac17a6b276856a9a4c57b0e11b0f33b0f721145c692834')
a11=proof('A11_SITE','A11_control_CESIRO1_EX01_EX08.json')
sx=a11['cases']['EX05']
assert sx['quality_score']==6.8 and sx['verified_subchecks']==34 and sx['out_of']==50
assert sx['sha256_consumer']==manifest['SITE_PEER']['sha256'] and sx['sha256_report']==manifest['SITE_EX05']['sha256']
proof('RECIPE_R2','R2_zone/A05/recipe-cost-cycle.json')
proof('HELPER','R5_pregatire/A05_S1_pick_aviz_RMA.py','3de836f60ece2a925e65c0a9284b5959adff56288191d528a4972b84e76b310c')
proof('OWNERSHIP','R6_pregatire/ERP/Harta_apeluri_proprietar_comanda.json')
cleanup=proof('CLEANUP','R6_pregatire/ERP/Restituire_clona_R6.json')
assert not cleanup['containers_left'] and not cleanup['networks_left']
for h in prev['evidence_manifest']: assert sha(base/'R2_zone'/h['file'])==h['sha256']
for h in prev['revision_consolidated']['evidence']: assert sha(base/h['file'])==h['sha256']
for h in prev['lineage']['legacy_proofs']: assert sha(base/h['relative_path'])==h['sha256']
assert len(prev['controls'])==29 and len(prev['pipelines'])==7 and len(prev['findings'])==11
for f in prev['findings']:
    for cid in f['control_ids']:
        assert f['finding_id'] in next(c for c in prev['controls'] if c['control_id']==cid)['findings']
for c in prev['controls']:
    for fid in c['findings']:
        assert c['control_id'] in next(f for f in prev['findings'] if f['finding_id']==fid)['control_ids']

s=raw['states'];initial,packed,reserved,unpacked,prepared,refused,shipped,authorized,ip=s
assert raw['id']=='R5W99513d7c' and raw['ids']==chain['case_ids']
assert [x[3] for x in packed['wms_events'] if x[1]=='AMBALARE']==['1002675']*3
assert [x[3] for x in unpacked['wms_events'] if x[1]=='DEZAMBALARE']==['1002711']*3
assert all(x[5]=='' and x[12]=='' for x in unpacked['wms_events'] if x[1] in ('AMBALARE','DEZAMBALARE'))
assert initial['g1_lot_locator']==packed['g1_lot_locator']==unpacked['g1_lot_locator']
assert initial['cost']==packed['cost']==unpacked['cost'] and initial['facts']==packed['facts']==unpacked['facts']
assert len(packed['cost'])==4 and len(packed['facts'])==8
assert prepared['pc']==refused['pc'] and prepared['wms_events']==refused['wms_events']
assert shipped['wms_events'][-1][1]=='IESIRE' and shipped['wms_events'][-1][11]=='Y'
assert all(x[1]!='CULEGERE' for x in shipped['wms_events']) and not shipped['t337_erp_staging_link']
assert shipped['so_and_reservation']==[['1000000','CO','1000000','1','0.0','1.0']]
sxso=ret['snap'];assert sxso==chain['native_return_after_confirm']
assert sxso['01_initial_IP']['moves']==sxso['02_SC_completed']['moves']==[] and not sxso['02_SC_completed']['fact']
assert sxso['03_receipt_completed']['moves'][0][3]=='1.0' and sxso['04_linked_reversal']==sxso['05_retry_reversal']
assert [D(x[3]) for x in sxso['04_linked_reversal']['moves']]==[D(1),D(-1)]
assert all(x[1:3]==['RE','Y'] for x in sxso['04_linked_reversal']['receipt']) and sxso['04_linked_reversal']['receipt'][0][3]==sxso['04_linked_reversal']['receipt'][1][0]
assert all(D(x[3])==D(x[4]) for x in sxso['04_linked_reversal']['fact'])
assert sum(D(x[4]) for x in sxso['04_linked_reversal']['cost'] if x[2]=='200000')==D('.0025')
assert alt['id']=='R5Wc3b5373b' and alt['ids']['SO']!=raw['ids']['SO']
assert conf['native_creation']['http']==201 and not alt['states'][4]['t337_erp_staging_link']
assert contrast['observed'][0]['http']==200 and contrast['observed'][0]['process_error']
sourceanchors=[]
def anchor(root,f,ranges):
    path=root/f; lines=path.read_text(encoding='utf8').splitlines()
    assert all(1<=x[0]<=x[1]<=len(lines) for x in ranges)
    sourceanchors.append({'tree':'EVA' if root==cut else 'iDempiere release-13','file':f,'sha256':sha(path),'lines':ranges})
prefix='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'
for f,r in [('wms/NotaSetWms.java',[[82,85],[164,165],[188,195]]),('corelare/NotaSetWmsProces.java',[[49,51],[209,225]]),('corelare/Culegere.java',[[104,107],[330,337]]),('corelare/ValideazaComenzi.java',[[589,604],[998,1015],[1036,1056]]),('corelare/PreiaDinSite.java',[[330,350],[427,457]])]:anchor(cut,prefix+f,r)
for f,r in [('MInOut.java',[[1160,1212],[1536,1536],[1615,1620],[2696,2710]]),('MInOutConfirm.java',[[394,414]]),('MRMALine.java',[[39,47]])]:anchor(native,'org.adempiere.base/src/org/compiere/model/'+f,r)
g={}
def gap(k,cs,p,ev,status,expected,observed,limit):
    g[k]={'controls':['A05-C'+i for i in cs.split(',')],'pipelines':['A05-P'+i for i in p.split(',')],'proofs':ev.split(','),'verdict':status,'expected':expected,'observed':observed,'limit_or_next':limit}
gap('G01','09,10,11,12','03','W1_RAW,R6_CHAIN,RECIPE_R2','CONFIRMAT_COMPONENTĂ; F01/F02 MENȚINUTE','S1 reversibil ocupă numai G2, componentele rămân contabile; fiecare operație are o singură consecință economică.','BOM 1000000: P123 + P124 tratat ca ambalaj obișnuit. Pe G2 1000003, P123/124 trec 1→0 și S1 devine 1 pe raft 1000004. În G1 rămân câte 1 și nu apare stoc contabil S1. Soldurile sursă, cele 4 costuri și cele 8 fapte contabilizate exclusiv pentru inventarele inițiale legate rămân identice până la dezambalare.','Nu se testează aici S1=6×P1/P2/P3, S2, componenta lipsă, set cumpărat sau preț/cost de 0,5 h. Proba R2 pe ambalaj CO și retry a dublat evenimentul. C12 rămâne FAIL.')
gap('G02','09,11,12,16','03,04','W1_RAW,R6_CHAIN','CONFIRMAT_SOLD; LEGĂTURĂ_NOTĂ_SO_NEDEMONSTRATĂ','Toate bucățile disponibile sunt împachetate; după comanda pentru CPP se dezambalează și se găsesc înainte de pick pe locatorul corect.','SO 1000000/linia 1000000 CO rezervă 1 CPP când G2 avea 0 CPP liber. Notele AD_PInstance 1002675/1002711 se deduc din Record_ID al celor 3+3 mișcări, chiar dacă răspunsul API nu a expus ID. Pe locator 1000004 setul scade 1→0 iar CPP și ambalaj cresc 0→1.','Același locator al setului (nou față de zona Neamplasat); nu s-a testat mutarea separată după dezasamblare. C_Order_ID și mișcarea inversată sunt nule pe ambele note. Ordinea în timp nu dovedește legătură nativă note→SO sau anulare/reversare documentară a notei de ambalare.')
gap('G03','11,14,16,26','03,04,06','W1_RAW,W2_RAW,W2_SOURCE,R6_T337','NEGATIVE_AMBELE_CONFIRMATE; POZITIV_T337_NEDEMONSTRAT','Garda trebuie să refuze când vânzările sunt oprite sau când livrarea nu are exact un val de site al firmei. Un val real autorizat trebuie să scrie CULEGERE și să urmeze documentele aceleiași comenzi.','G1/SO 1000000 aviz/PC 1000001: HTTP 200, process_error=true, vânzări oprite, zero mutații PC/jurnal. Caz SEPARAT cu sursa creată prin API 201, vânzări pornite și scriere externă oprită: SO 1000001, aviz 1000004, PC 1000003, fără staging, HTTP 200/process_error=true, «Livrarea nu aparține unui singur val de comenzi din site». Sursa sintetică a fost dezactivată la final.','Separați garda conformă de defectul de ingestie. Nu s-au scanat mobil linii sau confirmat un val real T22; nu declarați defect T337 ori întrerupere pentru toate comenzile.')
gap('G04','14,16,17,26,28','04,06,07','W1_RAW,R6_CHAIN','CONFIRMAT_PCȘIAVIZ_NATIVE; T337/SCAN/AWB_NEACOPERITE','Confirmarea și avizul trebuie să aibă aceeași comandă, linie și cantitate, apoi predarea fizică și curierul trasabili.','PC 1000001 (target=confirmed=1) trece DR→CO. Aviz 1000001/linie 1000001 leagă SO/linie 1000000; IP→CO, Posted=Y. Linia SO trece rezervat 1→0/livrat 0→1. Mișcarea G2 1000008 = IESIRE, C_Order_ID=1000000, EVA_FaraCulegere=Y, P123 −1 în G1 și G2.','Flux intern de 1/1 ASI 0, fără T337 CULEGERE, rotație lot, scan, expediere parțială, AWB sau livrare la client. Nu declarați completarea P04.')
gap('G05','05,16,27,28,29','02,04,05,07','RMA_RAW,W1_RAW,R6_CHAIN','CONFIRMAT_DOCUMENTAR_ÎN_FIXTURE','Recepția fizică presupune primirea unei confirmări native și o mișcare a stocului; RMA aprobat singur are efect fizic zero.','RMA 1000002/linie 1000002 la linia aviz 1000001: CO și QtyDelivered 0. Recepția 1000002/linie 1000002, IP/N, confirmare SC 1000002 DR. După SC CO, tot IP/N, 0 M_Transaction și 0 Fact_Acct. După finalizarea recepției CO/Y, M_Transaction 1000004, +1 P123 pe locator 1000000; QtyDelivered al liniei RMA 1.','Se confirmă 1 din 1 fără identificator lot și fără etapă distinctă de calitate comercială. Etapa de vandabilitate/rebut, retur parțial, factura, viramentul și rambursarea nu au fost observate.')
gap('G06','07,12,27,28,29','02,03,05,07','RMA_RAW,R6_CHAIN','CONFIRMAT_STORNO_RECEPȚIE; F01_DESCHIS','Un RC creează inversa legată de înregistrarea inițială, stoc ±1, sume contabilizate pe scheme și replay fără efect suplimentar.','M_InOut 1000002 ↔ 1000003 (Reversal_ID reciproc), ambele RE/Y. M_Transaction 1000004 +1 și 1000005 −1. Fiecare dintre cele două documente are câte 2 rânduri în schema 101 (Dr=Cr=51,45) și 2 în schema 200000 (Dr=Cr=43,73). M_CostDetail 101 +51,4500/−51,45; 200000 +43,7325/−43,73, diferență de precizie +0,0025 în aceste rânduri. QtyDelivered RMA revine la 0. După al doilea RC întregul snapshot (ID, cantități, fapte, cost) este identic.','Readback-ul de întoarcere agregă Fact_Acct pe schemă. Nu atestă reciprocitate rând-la-rând per cont, oglinda G2 după retur/storno, sau lipsa unui cost de rotunjire. Acesta este RC al recepției returului, nu storno al notei sau înregistrare a manoperei.')
gap('G07','01,13,14,16,17,23','01,04,06','SITE_EX05,SITE_PEER,A11_SITE,OWNERSHIP','C→ANTET_CONFIRMAT; DOCUMENT_COMERCIAL_BLOCAT','Originea de site trebuie să producă în mod idempotent liniile văzute la checkout și documentele aceleiași vânzări, cu drepturi de firmă și canal.','Q-COM-01 UUID 04255ef2-38dd-446f-89a7-d369a1a67335 în C: 2 linii, EXT7×2 / EXT8×1, ambele cotă 0,21, 87,88 RON față de 87,87 oracol. ERP 1000006, EVA_Proprie=N, 0 linii, EXCLUS și FK C_Order/M_InOut/C_Invoice nule. 8 antete (7A,1B), 7 UUID-uri în subsetul urmărit, doar 1 validat. 8 ordine și 308 fapte globale înainte/după; 2 rânduri rezervări exclusiv IsSOTrx=N, qty total 0. W=111,80 cu propriul ID, lookup în C 404. Evenimentul semnat PRIMIT/replay este frontieră separată.','Două canale sursă în aceeași firmă ERP, nu două cabinete; încrederea comisionarului și anularea de site fără comandă ERP nu au fost probate. A11 a recompilat propriul driver; nici W1, nici W2 nu provin din Q. Matricea Java acoperă 1043 fișiere, fără a exclude mecanisme dinamice/extensii.')
gap('G08','09,11,12,28','03,07','RECIPE_R2,W1_RAW,R6_CHAIN','FAIL_CUTIE_PE_CAZUL_TESTAT; MANOPERĂ_ȘI_STORNO_NOTĂ_DESCHISE','O cutie și 0,5 h per operație, consum/cost o singură dată în G1, fără stoc contabil adițional S1, reluare și anulare legate.','În fixture R6, cutia ca articol CO rămâne contabil 1 și după ambalare și după dezambalare; nu există linie de muncă. În R2 original/retry/operație nouă au produs 1/2/3 CPA în G2; dezambalarea compensatoare a lăsat 2 fără referință la original. În R6 stornarea recepției are cost real, dar privește alt document.','F01/F02 rămân deschise. Nu deduceți costul de muncă zero din absența articolului în fixture. Reutilizați documentul nativ pentru consumul fizic/centrele de cost, cu politică salarială A03, identificați evenimentul economic inițial și testați simultan anulare/retry.')
controls=[]
for i,c in enumerate(prev['controls']):
    t={k:c[k] for k in ['control_id','title','expected','status','findings','pipeline_ids','task_links','source_symbols','native_anchors','regression_steps']}
    t.update(prior_pointer=f"R3_zone/A05/A05_raport.json#/controls/{i}",prior_observation=c.get('R2_observed') or c['observed'],prior_limit=c['scope_limit'])
    t['r4_tests']=[k for k,d in g.items() if c['control_id'] in d['controls']]
    t['r4_coverage']='MARTORI_NOI_PARȚIALI' if t['r4_tests'] else 'RELUAT_DIN_R3_FĂRĂ_NOUĂ_EXECUȚIE'
    controls.append(t)
pipes=[]
for i,p in enumerate(prev['pipelines']):
    key=p['pipeline_id']
    v={k:p[k] for k in ['pipeline_id','business_outcome','expected','status','cross_zone_owners']}
    v.update(r3_pointer=f"R3_zone/A05/A05_raport.json#/pipelines/{i}",controls=[c['control_id'] for c in controls if key in c['pipeline_ids']],r4_tests=[k for k,d in g.items() if key in d['pipelines']])
    v['status_basis']= 'Păstrează verdictul integral R3, inclusiv ramurile încă neprobate; R4 creditează numai subtestele nominale.'
    pipes.append(v)
findings=[]
for i,f in enumerate(prev['findings']):
    t={k:f[k] for k in ('finding_id','title','severity','status','classification','control_ids','native_first_remediation','regression_test')}
    t['impact']=f.get('impact') or 'Cu un ASI nativ eligibil funcțional dar fără marcajul T329, endpointul mobil refuză în fixture poziția; limita depinde de politica aprobată.'
    t['r3_pointer']=f'R3_zone/A05/A05_raport.json#/findings/{i}'
    t['r4_related_tests']={'A05-F01':['G01','G02','G06','G08'],'A05-F02':['G01','G08'],'A05-F03':['G01','G02'],'A05-F05':['G04','G07'],'A05-F07':['G02'],'A05-F04':['G05','G06'],'A05-F10':['G01'],'A05-F06':['G01']}.get(f['finding_id'],[])
    findings.append(t)
report={'schema':'eva.audit.zone.execution.r4','zone_id':'A05','revision':'R4','reviewer':'A11','submitted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PARȚIAL_CU_RAMURI_FUNCȚIONALE_BLOCATE','cutoff_sha':prev['cutoff_sha'],'native_baseline':'da0730aec42f3e9f5f671e81a70ff71e24d5e534','plan_manifest':prev['plan_manifest'],'audit_quality_score':None,'product_score':None,
'scope':'Consolidare executată de A05 din R3, contraproba coordinatorului din cabinetul GardenWorld și EX05 cu peer și auditor separat. R4 revalidează hashurile și rezultatele brute. Nu a fost recreată clona sau accesată producția. Notele istorice A11 califică versiunile indicate.',
'independent_reviews':{'R1_A05':5.8,'R2_A05':6.8,'R3_A05':{'quality_score':rv['R3_quality'],'source':'A11_R3#/reports/A05','r3_hash':rv['sha256'],'A11_residual_at_R3':rv['residual']},'EX05_component':{'source':'A11_SITE#/cases/EX05','peer':'SITE_PEER','quality':sx['quality_score'],'verified_subchecks':34,'out_of':50,'disposition':sx['A11_disposition'],'supplement_gate':a11['gate'],'not_transferable_to_A05_R4':True},'R4_A05':'PENDING_A11'},
'versioned_lineage':{'r3':'R3','r2':'R2','r2_evidence_rehashed':len(prev['evidence_manifest']),'r3_supplement_rehashed':len(prev['revision_consolidated']['evidence']),'legacy_rehashed':len(prev['lineage']['legacy_proofs']),'source_paths':'Căile evidence_manifest R4 sunt relative la executie/. Căile moștenite se rezolvă la ediția indicată în fiecare pointer.'},
'counts':{'controls':len(controls),'pipeline_count':len(pipes),'finding_count':len(findings),'controls_by_status':dict(Counter(c['status'] for c in controls)),'pipelines_by_status':dict(Counter(p['status'] for p in pipes)),'controls_with_new_boundary_evidence':sum(bool(c['r4_tests']) for c in controls),'new_boundary_tests':len(g),'physical_origins':{'warehouse_native_W1':'SO 1000000', 'warehouse_native_W2':'SO 1000001','site_CQ':'UUID 04255ef2-38dd-446f-89a7-d369a1a67335, fără SO'}},
'controls':controls,'pipelines':pipes,'findings':findings,'r4_boundary_results':g,'evidence_manifest':manifest,'code_and_native_anchors':sourceanchors,
'A11_residual_disposition':[{'item':'F11','verdict':'CORECȚIE NOMINALĂ CONFIRMATĂ ÎN R3, RECONTROLATĂ R4; F11 limită condiționată de politica T329-8','proof':'controls C15/C20/C24 ↔ F11'}, {'item':'F10','verdict':'MENȚINUT FAIL numai la suprapunerea 18/20; martori seriali 18/18. Nu se generalizează la producție.','proof':'R2 + A11_R3'}, {'item':'F01 + manoperă','verdict':'Dublarea economică rămâne deschisă; anularea recepției are FK, anularea notei economice nu este dovedită; componentă de manoperă absentă.','proof':'G01,G02,G06,G08'}, {'item':'E9','verdict':'Menținute separate: 0011/0012 CO cu E fără cost pe acel produs; 0021 AVD a rămas DR 20/18, fără stoc/GL.','proof':'R3#/revision_consolidated/evidence'}, {'item':'E2E','verdict':'Legături documentare SO→PC→aviz→RMA→SC→recepție→inversă probate pe W1. Intrarea de site Q și T337 nu sunt același lanț; nu există scanare confirmată pentru W1.','proof':'G03–G07'}],
'next_regressions':['A06 + A05: un singur UUID într-un canal autorizat, CUI de vânzător vizibil, 2 linii persistate cu identități CPP/CPA, adresă de livrare și facturare distincte, costuri și TVA. Validați, reluați, anulați și verificați la nivelul IDs; proba unui alt SO rămâne distinctă.','A05 + A09: pe exact acea livrare și un singur val T22, scanare dispatcher autorizat pe locator/ASI, PC țintă/confirmată, jurnal G2 CULEGERE apoi LIVRARE, dublu click, scan duplicat, rol străin și cantitate parțială; AWB și moment de facturare prin A07.','A05 + A03: 1 cutie și 0,5 h, eveniment semantic unic, reîncercare după commit și anulare parțială cu FK la nota inițială, cost și facte pe fiecare schemă, separarea cheltuielii salariale de alocarea internă; prioritar mecanismele existente de document, cost și BOM.','Pe retur configurați ASI real, control calitate accept/rebut, o fracțiune a livrării și reconciliere pe cont/schemă/monedă; obțineți readback G2 după recepție și stornare, plus vânzabilitate. Verificați rotunjirea diferenței 0,0025 față de precizia schemei înainte de a eticheta un defect.'],
'constraints':'Raportul nu echivalează acoperirea celor 29 controale și 7 fluxuri cu certificarea execuției complete. Rezultatele sunt pentru versiunea și rutele testate. Noile probe nu acordă PASS funcțional global; A11 decide nota raportului R4.'}
atomic(target,report)
print(target,sha(target),report['counts'])
