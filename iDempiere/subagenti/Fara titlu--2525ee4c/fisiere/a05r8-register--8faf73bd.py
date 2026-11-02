from pathlib import Path
import json,re,hashlib,collections,datetime,sys
base=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
out=base/'executie/R8_pregatire/A05'; scratch=Path('D:/CodexWork/a05r8')
def j(f):return json.loads(f.read_text(encoding='utf-8-sig'))
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
queue=base/'Coada_reverificari_P01.json'; qs=[i for i in j(queue)['rows'] if i['owner']=='A05' and i['category']=='FIXTURĂ_EXECUTABILĂ']
cut='6df998aee0e514d30856c461962afe99ebd0d113'; oracles=j(scratch/'oracles.json');history=j(scratch/'history-corpus.json')
named=j(out/'T163_nativ_2.json'); docs=j(out/'T163_ZK_progres.json')
scripts=j(out/'Executie_scripturi_originale.json')
results=[]; refs={}
def ev(f):
 f=Path(f); f=f if f.is_absolute() else out/f
 key=f.relative_to(base).as_posix(); refs[key]=sha(f);return {'path':key,'sha256':refs[key]}
def origin(r):
 p=r['source']; task=r['task']; t=history['tasks'][task];o={'registered_path':p['source_file'],'position':p['source_position'],'registered_hash':p['sha_or_git_blob'],'dated_snapshot':t['dated_master_snapshot'],'declared_closure':t['date']}
 if p['source_file'].startswith('Documentatie/'):
  plan=oracles['plans'][task];n=int(p['source_position']);v=plan['lines_current'][n-1]
  o.update(source_blob_at_cutoff=plan['current_oid'],source_blob_at_dated_snapshot=plan['historic_oid'],literal_line_at_cutoff=v,registered_blob_match=p['sha_or_git_blob']==plan['current_oid'])
 else:
  f=Path(p['source_file']); assert sha(f)==p['sha_or_git_blob'],f; n=int(p['source_position'].split('/')[2]);o['manual_oracle']=j(f)['rz_mapping'][n]['original'];o['manual_source_sha_verified']=True
 return o
# Exact condition selectors over human-readable assertion output. Each matching line is verified by location/hash,
# not inferred from the name of a test or the green total of a suite.
rules={
'T163':{'C-13':('TestT163ArticoleDiverse',r'linii.*(plus|minus|scriptic)|pozitii.*dou'), 'C-14':('TestT163ArticoleDiverse','r10_cost0|cost_lipsa'), 'C-15':('TestT163ArticoleDiverse','r9_doc_deschis|lacăt|lacatele'), 'C-17':('TestT163ArticoleDiverse','rp_nepostat|garanția'), 'C-18':('TestT163ArticoleDiverse','rp_nepostat|cost_lipsa'), 'C-19':('TestT163ArticoleDiverse','scriptic_schimbat'), 'C-20':('TestT163Ecran','607|6588|7588'), 'C-21':('TestT163Ecran','pasul 4|Deschid documentul'), 'C-22':('TestT163Ecran','C-22|ajutor'), 'C-24':('TestT163ArticoleDiverse','stornare|RE.*CO|devalidez'), 'C-25':('TestT163ArticoleDiverse','global_valorica|perioada'), 'C-27':('TestT163ArticoleDiverse','original.*nepostat|stornare'), 'C-29':('TestT163ArticoleDiverse','Devalidez|document_invalid|storn'), 'C-31':('TestT163ArticoleDiverse','ri1_in|document_invalid')},
'T326':{'K-04':('TestListaPicking','OK +T15 |OK +T18 '),'K-06':('TestListaPicking','6 P1|6 din fiecare|0 seturi ambalate|0 ambalat'),'K-08':('TestListaPicking','LIPSA P3|P3.*LIPSA|P3.*1 bucat'),'K-09':('TestListaPicking','nevalidat|validat'),'K-10':('TestListaPicking','nevalidat|validat'),'K-11':('TestListaPicking','K-11|nevalidat'),'K-13':('TestListaPicking','OK +T08 '),'K-14':('TestListaPicking','OK +T14 '),'K-17':('TestListaPicking','OK +T02 |OK +T04 '),'K-18':('TestListaPicking','OK +T03 '),'K-19':('TestListaPicking','OK .+K-19'),'K-20':('TestListaPickingEcran','PDF|rezultat text|tipărirea'),'K-21':('TestListaPickingEcran','drept|refuz|Refuzat'),'K-22':('TestListaPickingEcran','etichetele|Ajutor|RO/EN'),'K-23':('TestListaPicking','K-38|Rulare'),'K-26':('TestListaPicking','K-26|dezactiv'),'K-28':('TestListaPickingEcran','print|tipărir'),'K-32':('TestT29Catalog','culegere|Culegere'),'K-34':('TestListaPicking','bytecode|emiteVal'),'RZ-4.1':('TestListaPicking','OK +T14 |OK +T15 '),'RZ-4.2':('TestListaPicking','OK +T08 ')},
'T329':{'C-2':('TestLoturi',r'ensureT329|marcaj'),'C-5':('TestLoturi',r'DDL|UX_MEDIU|migrare'),'C-6':('TestLoturiEcrane',r'NIR|recepți|K1'),'C-7':('TestLoturi',r'lot_obligatoriu|refuzLot'),'C-8':('TestLoturiEcrane',r'K3|bonul facturii|ieșir'),'C-10':('TestLoturi',r'storno|invers|reactiv'),'C-11':('TestLoturi',r'CMP|60,00|60.0'),'C-12':('TestLoturiEcrane',r'Transfer|K4'),'C-13':('TestLoturiEcrane',r'Inventar|faptic'),'C-14':('TestLoturiEcrane',r'5 ecrane|K1|K2|K3|K4'),'C-15':('TestLoturiEcrane',r'K15|K17|K10'),'C-17':('TestLoturi','OK +'), 'C-18':('TestLoturi',r'fără lot|nemarcat|B0'), 'C-21':('TestLoturi','OK +'), 'C-26':('TestLoturiEcrane',r'modific|refac|revers'),'RZ-7.1':('TestLoturi',r'M_Lot|createLot|Lot')},
'T330':{'C-4':('TestFefo','LB|K3|factur'),'C-5':('TestFefo','LB|transfer'),'C-9':('TestFefo','LD|expirat'), 'C-11':('TestFefo','avert|expirat'), 'C-15':('TestFefo','Pe loturi|stoc final|ST5'), 'C-17':('TestFefo','urmărire|dezactiv|ascuns'), 'C-18':('TestT40L2Motor','fără lot|CMP|FIFO'), 'C-25':('TestFefo','OK +'),'RZ-8.2':('TestFefo','Expiră|30 zile|expiră')},
'T354':{'C-1':('TestT354Disponibil','bifa|component'), 'C-2':('TestT354Set','stocabil|IsStocked'), 'C-6':('TestT354Set','cererea seturilor|cerereComponenta|20.*18'), 'C-8':('TestT354Set','fără set|B0'), 'C-9':('TestT354Set','FEFO|lot'), 'C-11':('TestT354Set','T337|confirm'), 'C-14':('TestT354Set','IsVerified|verif'), 'C-16':('TestT354Set','OK +'), 'C-22':('TestT354Set','storn|factură'), 'C-24':('TestT354Disponibil','istoric|documente|retur')},
'T325':{'K-02':('TestListaAmplasare','WMS|contabil|registru'), 'K-09':('TestListaAmplasare','Fact_Acct|strat'), 'K-17':('TestListaAmplasare','Fact_Acct|cost'), 'RZ-3.2':('TestListaAmplasare','Amplas|NIR'), 'RZ-3.3':('TestListaAmplasare','contab|Fact_Acct')},
'T323':{'RZ-1.2':('TestT323Pozitii',r'1 și 3|apariții|aparițiile'), 'RZ-1.4':('TestT323Pozitii','Fact_Acct|contabil')},'T324':{'RZ-2.2':('TestImportFapticLocatieLot','fără.*coloan|regresi|vechi')},'T327':{'RZ-5.1':('TestT327Etichete','citire|citite|ZXing'),'RZ-5.2':('TestT327Etichete','EAN|cifra'),'RZ-5.3':('TestT327Etichete','CatalogTiparire|număr')},
'T331':{'RZ-9.1':('TestRegulaLegaturaWms','Fact_Acct|fără contabil'), 'RZ-9.2':('TestRegulaLegaturaWms','registru|validare'), 'RZ-9.4':('TestRegulaLegaturaWms','comand|ofert'), 'RZ-9.6':('TestRegulaLegaturaWms','rezerv|sursă'), 'RZ-9.7':('TestT331Oglinda','fără pereche'), 'RZ-9.8':('TestRegulaLegaturaWms','inventar'), 'RZ-9.10':('TestRegulaLegaturaWms','M_Movement|mișcare')},
'T333':{'C-12':('TestT333Acces','EVA_AplicatieMobila|E3'), 'C-14':('TestT333Acces','Gestionar|AD_PInstance'), 'RZ-11.3':('TestT333Acces','E3|E4'),'RZ-11.4':('TestT333Acces','ensure')},'T334':{'RZ-12.2':('TestApiMobilInventar','Fact_Acct|scrier|M_StorageOnHand')},'T337':{'RZ-15.3':('TestConfirmarePickVal','oprit|implicit|B0')},
'T339':{'RZ-17.1':('TestT339ValidareWms','t05_contul|contul plusului'), 'RZ-17.2':('TestT339Motor','CMP'), 'RZ-17.3':('TestT339ValidareWms','t17_stornarea|t18_aDinNou'), 'RZ-17.4':('TestT339Motor','FIFO|LIFO|CMP'), 'RZ-17.5':('TestT339Motor','reface|reconstr'), 'RZ-17.6':('TestT339ValidareWms','preț|preţ|CurrentCostPrice|fără strat'), 'RZ-17.7':('TestT339ValidareWms','t16_inventarDeschis|t21_faraCost|global'), 'RZ-17.8':('TestT339Ecran','drept|buton')},
}
def logref(suite,pat):
 paths=[out/'JVM_service'/(suite+'.txt'),out/'JVM'/(suite+'.txt')]
 ret=[]
 for f in paths:
  if not f.exists():continue
  lines=f.read_text(encoding='utf8').splitlines();hits=[]
  for n,line in enumerate(lines,1):
   if re.search(pat,line,re.I) and re.match(r'^\s*(OK\b|==|FAIL\b|REZULTAT)',line,re.I):hits.append([n,line.strip()[:225]])
  if hits:
   ret.append({**ev(f),'suite':suite,'selector':pat,'matches_total':len(hits),'matches':hits[:5],'suite_tail':next((s[:202] for s in reversed(lines) if re.search(r'REZULTAT|teste:.*FAIL|FAIL precondiție',s,re.I)),None)})
 return ret[:1]
def histlinks(task,k):
 h=[]
 for p,v in history['signals'].items():
  if '/'+task+'-' not in p:continue
  marks=[(n,codes,states,s) for n,codes,states,s in v['signals'] if k in codes]
  if not marks:continue
  quality=(4 if '/dovezi' in p.lower() else 0)+(2 if p.endswith('.txt') else 0)+(1 if any(i[2] for i in marks) else 0)
  h.append((quality,p,marks[0],v['oid']))
 return [{'path':p,'blob_oid_at_cutoff':oid,'line':line[0],'line_sha256':line[3],'recorded_markers':line[2],'role':'index istoric, nu execuție actuală și nu dovedește autoacceptarea taskului'} for _,p,line,oid in sorted(h,key=lambda x:(-x[0],x[1]))[:2]]
def T(k):return re.match(r'(C-\d+|K-\d+|RZ-\d+\.\d+)',k).group()
def add(item,mode,res,proof):item['observations'].append({'layer':mode,'observed':res,'proof':ev(proof)})
def build():
 for raw in qs:
  tid=raw['task'];crit=raw['criterion']; key=T(raw['source']['text']);o=origin(raw)
  row={'criterion':crit,'task':tid,'canonical':raw['project_task'],'marker':key,'oracle':raw['source']['text'],'source':o,'historical_documents':histlinks(tid,key),'observations':[],'full_criterion_reexecuted':False,'product_score':None}
  rule=rules.get(tid,{}).get(key)
  if rule:
   for ref in logref(*rule):row['observations'].append({'layer':'JVM_SOURCE/COMPILED; aucune attribution à UI/SQL','suite_log':ref,'observed':'Reluare locală a aserțiunilor selectate, pe codul și configurația JAR indicate. Logul distinge aserțiunea de întreaga suită.'})
  if tid=='T163' and key in ['C-1','C-2','C-3','C-4','C-6','C-7','C-8','C-9','C-10']:
   for s in scripts:
    if s['task']!=tid:continue
    f=out/s['file'];hit=next(x for x in f.read_text(encoding='utf8').splitlines() if x.startswith(key+' '));add(row,'ORIGINAL_GIT_'+s['tag'],{'rev':s['rev'],'base':s['base'],'script_oid':s['script_oid'],'metric':hit},f)
   if key=='C-3':add(row,'MUTANT','0→1 istoric și curent la injecția unui UPDATE; outputul scriptului este un numărător, rc=0 chiar și în contraproba roșie.','Mutanti_si_atribuire.json')
   if key=='C-6':add(row,'MUTANT/BLAME','În C-6 pragul este zero; 0 la squash și 3 în diff cumulat la cutoff (nu 3 defecte originale). T36TexteChei local 97/97. Marcaje actuale în WInventarForm, două linii identice din fișier fac atribuirea exactă pe diff ambiguă.','Mutanti_si_atribuire.json')
   row['full_criterion_reexecuted']=True
  if tid=='T333' and key=='C-24':
   add(row,'ORIGINAL_STATIC/MUTANT','Istoric C24-a/b: baza=0, mutanți=1/1, rc=0. Curent: baza=20, mutanți=21/21, rc=1. Garda istorică era pentru schelet; ramurile autorizate ulterior ale jurnalului mobil nu se pot declara defect din diferența aceasta.','Mutanti_si_atribuire.json');row['full_criterion_reexecuted']=True
  if (tid,key) in [('T163','C-30'),('T326','K-29'),('T330','C-26'),('T354','C-10')]:
   f=out/'Garda_parteneri_POSIX.json'
   if f.exists():add(row,'STATIC_ORIGINAL_POSIX',j(f)['summary']+'; corpus 11294 fișiere, nicio scriere. Acest scanner nu măsoară traficul runtime.',f);row['full_criterion_reexecuted']=(tid=='T163')
  if tid in ('T329','T330') and key in ('C-22','C-23','RZ-7.3','RZ-8.3'):
   histmark='T329_closure' if tid=='T329' else 'T330_closure'
   n='57' if tid=='T329' else '92';matrix=j(out/'Matrice_T40.json')
   add(row,'CITIRE_DOCUMENTARĂ_ISTORIC/CURENT',{'historical':matrix[histmark]['lines'][n],'current':matrix['cut']['lines'][n],'file':matrix['cut']['file'],'current_line':n,'other_relevant_row_92':matrix['cut']['lines']['92']},'Matrice_T40.json')
   row['full_criterion_reexecuted']=True
  if tid=='T163' and key in ('C-13','C-14','C-15','C-17','C-18','C-19','C-20','C-21','C-24','C-25','C-28'):
   nt={'C-13':'Două sesiuni prin procesul autentic; un DR ID 1000004, createdby=101, două linii 10→12 și 10→9, zero M_Transaction/Fact_Acct în DR.','C-14':'După deschiderea perioadei prin proces nativ, articol fără cost: HTTP200/isError=true, mesaj nominal cost, 0 documente noi.','C-15':'Două tokenuri distincte GardenAdmin trimise la barieră. Un proces a creat un DR, cealaltă cerere n-a creat al doilea document. Concurența între doi utilizatori sau două JVM și al doilea clic de validare cer dovezi separate.','C-17':'După CO ID 1000004: două mișcări +2 și −1, 8 fapte. După RC încă −2 și +1 și 16 fapte în total; reluarea RC nu le dublează.','C-18':'Sunt distincte refuzul inițial de pregătire fără cost și lipsa costului provocată exact după DR.','C-19':'Proba de bază ține stocul constant; regula scriptic schimbat este exercitată independent de suita JVM.','C-20':'În UI: minus 607/plus 7588 pe documentul ghidului. Documentul următor fără charge nu se deduce din acest caz.','C-21':'Screenshot după pregătire și deschiderea exactă a documentului în Documente de inventar; după validare UI CO/Y.','C-24':'Secvența inițială are +2 și −1 pe două articole în ACELAȘI document. Aceasta nu echivalează cu trei operații succesive pe același articol.','C-25':'Data 2101 din afara perioadei deschise este refuzată; 0 documente în readback. Ramura GV se evaluează separat.','C-28':'Query larg pe AMERP returnează șase procese salarizare/factură/plată; niciunul din rezultate nu reactivează producția. Plus interogarea exactă Q9 dacă prezentă.'}[key]
   add(row,'NATIVE_APPLICATION/POSTGRES',nt,'T163_nativ_2.json')
   if key in ('C-13','C-14','C-17','C-20','C-21'):add(row,'ZK',{'C-13':'GardenAdmin clicks, document 1000006 with two rows prepared through guide (distinct from ERP race).','C-14':'Article without cost, UI message and zero new docs.','C-17':'Deschid documentul, Validez, DocStatus CO/Y.','C-20':'Visible fields minus 607/plus 7588.','C-21':'WArticoleDiverseForm opened, action and target WInventarForm ID linked.'}[key],'T163_ZK_progres.json')
  if tid=='T326' and (out/'T326_nativ_progres.json').exists():
   rowsj=j(out/'T326_nativ_progres.json')
   marker={'K-04':'K-04','K-09':'K-09','K-10':'K-10','K-13':'AMPR','K-14':'K-03/K-14','K-23':'K-23','RZ-4.1':'K-03/K-14','RZ-4.2':'AMPR'}.get(key)
   if marker:
    for phase in rowsj:
     hits=[line for line in phase.get('lines',[]) if marker in line]
     if hits:add(row,'ERP_NATIVE_T22_FIXTURE_STAGING',{'stage':phase['case'],'rc':phase['rc'],'rows':hits},'T326_nativ_progres.json')
  if tid=='T354' and (out/'T354_nativ.json').exists():
   for rec in j(out/'T354_nativ.json'):
    hits=[s for s in rec.get('lines',[]) if re.match(r'^CRIT '+re.escape(key)+r'(?:[ (:/]|$)',s)]
    if hits:add(row,'ERP_NATIVE_T22_FIXTURE_STAGING',{'stage':rec['label'],'rc':rec['rc'],'lines':hits},'T354_nativ.json')
  row['classification']='REEXECUTAT_CRITERIU_DOCUMENTAR' if row['full_criterion_reexecuted'] and 'manual_oracle' in o else 'REEXECUTAT_CRITERIU' if row['full_criterion_reexecuted'] else 'COMPONENTĂ_REEXECUTATĂ_REST_NEEXECUTAT' if row['observations'] else 'DOAR_DOCUMENT_ISTORIC_FĂRĂ_PROBĂ_ACTUALĂ' if row['historical_documents'] else 'NEEXECUTAT'
  row['remaining']=None if row['full_criterion_reexecuted'] else ('Conservă condițiile și nivelul din oracolul textual. Probe numai pentru subcondițiile de mai sus; ' + (str(o['manual_oracle']['target']) if 'manual_oracle' in o else raw['source']['text'].split('|')[-1].strip()) + '. Rolul, comparația de JAR, scanarea, documentele ori condițiile neexercitate rămân explicit deschise.')
  results.append(row)
if __name__=='__main__':
 build();assert len(results)==135 and len({r['criterion'] for r in results})==135
 brief={'utc':utc(),'schema':'eva.audit.A05.R8.nominal.progress','cut':cut,'input_sha256':sha(queue),'criteria':len(results),'counts':dict(collections.Counter(r['classification'] for r in results)),'by_task':dict(collections.Counter(r['task'] for r in results)),'no_self_score':True,'rows':results,'referenced_proofs':refs}
 f=out/'Registru_nominal_progres_A05.json';tmp=f.with_suffix('.tmp');tmp.write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf8');tmp.replace(f);print(len(results),brief['counts'],len(refs),sha(f))
