from a12_r9_read import *
from urllib.parse import quote
import hashlib,html,collections,shutil,os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
R9=E/'R9'
def enc(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def e(s):return html.escape(s if isinstance(s,str)else json.dumps(s,ensure_ascii=False),quote=True)
@lru_cache(maxsize=3000)
def H(p):return sha(p)
def S(p):return{'path':p.relative_to(B).as_posix(),'sha256':H(p)}
@lru_cache(maxsize=160)
def read(p):return rd(p)
def ptr(obj,p):
 for field in p.strip('/').split('/')if p else []:obj=obj[int(field)]if isinstance(obj,list)else obj[field.replace('~1','/').replace('~0','~')]
 return obj
def node_file(c,f,p):
 return S(f)|{'pointer':p,'criterion':c}
def make(c,typecode,kind,ref,expect,seen,limit,ctrl=None,extent=None):
 row={'criterion':c,'relation':typecode,'kind':kind,'ref':ref,'expected':expect,'observed':seen,'limit':limit,'negative':ctrl,'extent':extent};return ('EV9-'+hashlib.sha256(enc(row).encode()).hexdigest()[:23],row)
def add(m,c,z):m[c].append(z)
def collect(preview=False):
 f=P9/'A12_receptii_R9_faza1.json';allr=rd(f)['receipts'];retval=collections.defaultdict(list)
 for c,raw in allr.items():
  for i,v in enumerate(raw):
   fp=B/v['proof']['file'];assert H(fp)==v['proof']['sha256'];vv=ptr(read(fp),v['pointer'])if fp.suffix=='.json'else fp.read_bytes();assert vv is not None
   typ='R9_incorporated_prior_subcondition'if v['epoch']=='previously_measured_post_R8'else'R9_document_recomputed'if v['epoch']=='documentary_today'else'R9_runtime_or_script'
   add(retval,c,make(c,typ,v['kind'],node_file(c,f,'/receipts/'+c+'/'+str(i)),v['expected'],v['observed'],v['limitation'],v['negative_or_control'],v['extent']))
 independent=E/'A11_control_suplimente_R9_A03_177_CESIRO1.json';ind=rd(independent);assert H(independent)=='5b393c7775d1b527f2d29fc5a78b6c69dc40be4c2cefa1922b0cb63eec4003e2'
 for cid,key,expected,limit in [('T159-R2-050','T159_overlap_with_current','Recalcul explicit al intersecției cu cele 302 identități inițiale.','Nu se transferă concluzia la conservarea celor 302 decizii. Doar trei înlocuiri funcționale sunt urmărite până acum.'),('T156-R2-010','T156_two_archive_snapshots','Două fotografii datate și rândurile nominale ale mutării.','Controlul documentar al soldurilor sau al jurnalului nu este o execuție nouă în cabinet.'),('T04.06-R3-001','runtime_actual_and_image_direct','Confirmarea distribuirii exacte a imaginii și a limitei redirecturilor din simulator.','Sursa CESIRO1 diferă de pluginul eMAG și de o tranzacție pe un partener real.')]:
  group='CESIRO1'if cid=='T04.06-R3-001'else'A03';data=ind[group][key];add(retval,cid,make(cid,'R9_independent_control', 'A11_PREAUDIT_LIMITAT',node_file(cid,independent,'/'+group+'/'+key),expected,data,limit,None,'independent_control_not_duplicate'))
 a5dir=E/'R9_pregatire/A05';a5file=a5dir/'Registru_R9_A05.json'
 aliases=P9/'Relectura_882_addendum_aliasuri.json';ax=rd(aliases);assert H(aliases)=='7f2b096b4d55e4d97585b562902c38480828b7ce8525b0e6f202dd02de1a9fa5'
 v882f=E/'A11_control_R9_882_pointeri.json';v882=rd(v882f);assert H(v882f)=='56c63710546f928b002de9478ac535d4d80c684de111561e8233148db0e14c23'
 for i,v in enumerate(v882['identity_checks']['differences']):
  c=v['criterion'];add(retval,c,make(c,'R9_alias_independent_control','A11_ID_NEOMOGEN_DOCUMENTAT',node_file(c,v882f,'/identity_checks/differences/'+str(i)),'Verifică dacă forma din registru este aceeași identitate numerică sau un alias explicit.',v['adjudication'], 'Identitate de sursă. Nicio verificare de funcționare și nicio schimbare a ID-ului P01 din registru.',None,'source_only'))
 for i,z in enumerate(ax['audited_rows']):
  cid=z['criterion'];add(retval,cid,make(cid,'R9_alias_provenance_only','GENEALOGIE_DOCUMENTATĂ',node_file(cid,aliases,'/audited_rows/'+str(i)),'Egalitate id_vechi cu identificatorul din rândul vechi, titlu şi contexte temporale separate.',{'historic_alias':z['historic_row']['key'],'current_id':z['effective_id'],'current_row_pointer':z['captured_row']['pointer'],'explicit_id_vechi':True},z['evidence_scope'],None,'identity_only'))
 if a5file.exists():
  a5=rd(a5file)
  man=a5dir/'Manifest_R9_A05.json';b=rd(man);assert H(a5file)=='9d98a0081daadd5400bdb69a6a0739eb0f1b10880c3c37ad65fab79ec8995a5a' and H(man)=='f560be6987ff3bdd9b6af305f7a36f76bff33f14605fd8bb75f36db445318f30'
  for item in b['evidence']:assert H(a5dir/item['file'])==item['sha256'],item['file']
  for i,z in enumerate(a5['rows']):
   c=z['criterion'];obs=z.get('observed_explicit',{'bytecode':z.get('diff_clase'),'bundles':z.get('bundles')});add(retval,c,make(c,'R9_runtime_or_script',z['disposition'],node_file(c,a5file,'/rows/'+str(i)),z['oracle'],obs,' '.join(z['limits'])+' '+('Coloana M_AttributeSetInstance_ID există în Fact_Acct r57; valorile ei nu au fost selectate în acest experiment.'if c=='T329-R2-012'else''),z.get('method',z.get('severity')),'subcase'))
  a11f=E/'A11_control_supliment_A05_R9.json';d=rd(a11f);assert H(a11f)=='388f566748234367673b48dd112b58d424ef40463c29f7b66371d3e645110a9c'
  for c,key in [('T329-R2-012','independent_cost_observation'),('T329-R2-012','ASI_attribution'),('T330-R2-025','jar_compare'),('T330-R2-025','tests_rerun_and_hashed')]:
   add(retval,c,make(c,'R9_independent_control','A11_VERIFICARE_NOMINALĂ_A05',node_file(c,a11f,'/'+key),'Distinge rezultatul măsurat nativ de configurația şi exportul nerealizate.',d[key],d['gate'],None,'independent_control_not_duplicate'))
 elif not preview:raise ValueError('A05 final pending')
 return retval
def decide(prior,c,nowrows):
 content=[r for _,r in nowrows if r['relation']in ['R9_runtime_or_script','R9_document_recomputed','R9_incorporated_prior_subcondition']]
 if not content:return prior
 if c=='T159-R2-050':return 'CLI_VID_302_TRASE_ISTORIC_MIGRARE_PARȚIALĂ_R9'
 if c=='T04.06-R3-001':return 'CONTRACT_REDIRECT_SEPARAT_EMAG_ȘI_CESIRO1_R9'
 if c=='T35.08-R3-001':return 'ACORD_DOCUMENTAR_2_PĂRȚI_PE_ACELAȘI_TEXT_CONFIRMAT_R9'
 if c=='T35.09-R3-001':return '31_OBIECTE_GIT_30_CELULE_T10_RECONFIRMATE_R9'
 if any(z['relation']=='R9_incorporated_prior_subcondition'for z in content):return 'SUBCONDIȚIE_A06_PREEXISTENTĂ_REVERIFICATĂ_A11_R9'
 if c=='T06-R2-003':return 'SCRIPT_LIMITĂ_DIFF_ISTORIC_REEXECUTAT_R9'
 if c=='T314-R2-027':return '14_CĂI_ÎN_EXPORT_VS_ZERO_ÎN_FIXTURA_PLAN_R9'
 if c in ['T329-R2-012','T330-R2-025']:return 'REVERIFICARE_A05_LA_STRATUL_NOMINAL_R9'
 return 'SUBCAZ_INDIVIDUAL_RULAT_R9'
def dos_html(w):
 from urllib.parse import quote
 out=[]
 for c in criteria(w):
  r=c['R9'];det=r['observations'];ss=[]
  for id,v in det:
   if v['relation']in ['R9_plan','R9_external_boundary','R9_retained_partial','R9_source_location']:continue
   href='../../'+quote(v['ref']['path'].removeprefix('executie/'),safe='/')
   ss.append('<li><b>'+e(v['kind'])+'</b><br>Etalon. '+e(v['expected'])+'<br>Observat. '+e(str(v['observed'])[:1200])+'<br>Limită. '+e(v['limit'])+'<br><a href="'+href+'">Probă</a> <code>'+e(v['ref']['pointer'])+'</code></li>')
  out.append('<section id="'+e(c['id'])+'"><h2>'+e(c['id'])+'</h2><p>'+e(c['normative_content'])+'</p><dl><dt>Stare R8</dt><dd>'+e(r['prior'])+'</dd><dt>Stare R9</dt><dd>'+e(r['effective_status'])+'</dd><dt>Pas rămas</dt><dd>'+e(r['next'])+'</dd></dl>'+('<ul>'+''.join(ss)+'</ul>'if ss else'')+'</section>')
 css='*{box-sizing:border-box}body{max-width:1030px;margin:32px auto;padding:0 18px;font:16px/1.56 system-ui;color:#16374e;overflow-wrap:anywhere}section{border-top:1px solid #c6d9e1;padding:15px 0}dt{font-weight:bold}dd{margin:0 0 .6rem}li{margin:10px 0}a{color:#145884}@media(max-width:575px){body{padding:0 12px;margin:16px auto}ul{padding-left:24px}}'
 return '<!doctype html><html lang="ro"><meta charset="utf-8"><meta name=viewport content="width=device-width, initial-scale=1"><title>'+e(w['task'])+' · Audit R9</title><style>'+css+'</style><nav><a href="../Audit_individual_P01_R9.html">Indexul P01</a> · <a href="../taskuri/Fisa_'+e(w['task'])+'.json">Date și probe</a></nav><h1>'+e(w['task'])+' · '+e(w['title'])+'</h1><p>'+e(w['canonical'])+' · '+e(w['state_at_new_capture'])+'</p>'+''.join(out)+'</html>'
def indexer(recs,remaining):
 rows=''.join('<tr><td><a href="'+e(z['html'])+'">'+e(z['task'])+'</a></td><td>'+e(z['canonical'])+'</td><td>'+e(z['title'])+'</td><td>'+e(z['state'])+'</td><td>'+str(z['criteria'])+'</td><td>'+str(z['r9_measured_or_document'])+'</td><td>'+str(z['unexecuted'])+'</td></tr>'for z in recs)
 css='*{box-sizing:border-box}body{font:16px/1.5 system-ui;max-width:1390px;margin:28px auto;padding:0 16px;color:#18364b;overflow-wrap:anywhere}.sc{max-width:100%;overflow-x:auto;overscroll-behavior:contain}table{width:100%;min-width:740px;border-collapse:collapse}td,th{padding:6px 8px;text-align:left;border-bottom:1px solid #d0dce2}th{background:#f0f5f7;position:sticky;top:0}input{font:inherit;padding:.5em;max-width:100%;width:25em}@media(max-width:575px){body{padding:0 12px;margin:16px auto}input{width:100%}}'
 return '<!doctype html><html lang="ro"><meta charset=UTF-8><meta name=viewport content="width=device-width, initial-scale=1"><title>Audit P01 R9 · 652 fișe</title><style>'+css+'</style><h1>Audit P01 · Runda 9</h1><p>652 de taskuri și 2.619 criterii. Registrul separă probele de implementare, documentele istorice și cazurile încă nedemonstrate; '+str(remaining)+' criterii poartă încă starea NEEXECUTAT.</p><p><a href="A12_raport.json">Raport</a> · <a href="Registru_reexecutare_R9.json">Registru nominal</a> · <a href="Dovezi_criterii.json">Dovezi și legături inverse</a> · <a href="Verificare_R9.json">QA</a></p><label>Caută taskul sau capitolul <input type=search id=search></label><p id=n>652 fișe</p><div class=sc role=region tabindex=0 aria-label="Tabelul taskurilor P01"><table><thead><tr><th>Fișă</th><th>ID P01</th><th>Nume</th><th>Stare portal</th><th>Criterii</th><th>Probă R9</th><th>Neexecutate</th></tr></thead><tbody>'+rows+'</tbody></table></div><script>const f=document.querySelector("#search"),rows=[...document.querySelectorAll("tbody tr")];f.addEventListener("input",()=>{let n=0;for(let r of rows){r.hidden=!r.textContent.toLocaleLowerCase("ro").includes(f.value.toLocaleLowerCase("ro"));if(!r.hidden)n++}document.querySelector("#n").textContent=n+" fișe"})</script></html>'
def main(preview=False):
 dest=Path('D:/CodexWork/a12-r9-preview')if preview else R9;(dest/'taskuri').mkdir(parents=True,exist_ok=True);(dest/'fise_html').mkdir(exist_ok=True)
 parent=rd(R8/'A12_raport.json');prior_ev=rd(R8/'Dovezi_criterii.json');ev=prior_ev['evidence'];rev=prior_ev['inverse_task_requirement_links'];observations=collect(preview)
 plan=P9/'Repartizare_177_R9.json';pd=rd(plan);reread=P9/'Relectura_882_pointeri.json';rdc=rd(reread)['rows'];q38={z['criterion']for z in pd['38_external_only_linked_to_original_tasks']};q1={z['criterion']for z in pd['assigned_cases']};q218={z['criterion']for z in pd['separate_218_partial']};q882={z['criterion']for z in rdc};assert not q218&q1 and len(q38&q1)==2
 def meta(rows,relation,field,file,pu,limit):
  for i,v in enumerate(rows):
   c=v['criterion']
   add(observations,c,make(c,relation,field,node_file(c,file,pu+str(i)),field,{'pointer_accepted_as_source_only':True,'task':v['task']},limit,None,'no_product_credit'))
 meta(pd['assigned_cases'],'R9_plan','Repartizarea nominală și cazul propus.',plan,'/assigned_cases/','Planificare. Nu este probă de execuție.')
 meta(pd['separate_218_partial'],'R9_retained_partial','Subcazul R8 rămâne distinct de 1.226 neexecutate.',plan,'/separate_218_partial/','Nu se primește o a doua acceptare pentru aceeași probă.')
 meta(pd['38_external_only_linked_to_original_tasks'],'R9_external_boundary','Componenta externă numai pentru criteriul identificat.',plan,'/38_external_only_linked_to_original_tasks/','Suprapunere parțială cu alte loturi, nu o categorie adunată.')
 meta(rdc,'R9_source_location','Verificare SHA, obiect și pointer înainte de căutarea etalonului.',reread,'/rows/','Originea identificată singură nu validează o obligație sau execuția produsului.')
 counts=collections.Counter();by=collections.Counter();types=collections.Counter();scopevals=collections.Counter();docs=[];register=[];allc=set()
 for rr in parent['records']:
  p=R8/rr['file'];assert H(p)==rr['sha256'];w=rd(p);assert w['task']==rr['task'];w['schema']='A12.R9';w['immutable_R8_parent']=S(p);w['scoring_authority_R9']='Independent A11, în așteptare.';cz=criteria(w);execs=0;unp=0
  for c in cz:
   id=c['id'];allc.add(id);pr=c['R8']['effective_status'];oo=observations.get(id,[]);st=decide(pr,id,oo);qual=[v for k,v in oo if v['relation']in ['R9_runtime_or_script','R9_document_recomputed','R9_incorporated_prior_subcondition']];own=r8map[id].get('owner');scopevals['q177_exercised']+=int(id in q1 and bool(qual));scopevals['q882_exercised']+=int(id in q882 and bool(qual));scopevals['q218_with_new']+=int(id in q218 and bool(qual));scopevals['all_r9_criteria_measured']+=int(bool(qual));scopevals['prior_unexecuted_measured']+=int(bool(qual)and pr=='NEEXECUTAT');counts[st]+=1;execs+=bool(qual);unp+=st=='NEEXECUTAT';nex=c['R8']['next_action']
   if qual:nex=' '.join(dict.fromkeys(str(v['limit'])for v in qual if v['limit']))
   rels=list(c['R8']['effective_evidence_links'])
   for eid,v in oo:
    assert eid not in ev;ev[eid]=v;rev.setdefault(eid,[]).append({'criterion':id,'task':w['task'],'relation':v['relation']});rels.append({'id':eid,'relation':v['relation']});types[v['relation']]+=1
   c['R9']={'prior':pr,'effective_status':st,'observations':oo,'effective_evidence_links':rels,'next':nex,'no_grade':True}
   register.append({'task':w['task'],'canonical':w['canonical'],'criterion':id,'owner':own,'text':c['normative_content'],'R8':pr,'R9':st,'cohorts':{'earlier_177':id in q1,'separate_partial_218':id in q218,'external_38':id in q38,'without_oracle_R8_882':id in q882},'individual_evidence_or_plan':[v[0]for v in oo],'measured_or_documentary_or_previous_supplement':bool(qual),'next':nex})
  docs.append((w,rr,execs,unp))
 assert set(observations)<=allc and len(allc)==2619
 def write(t):
  w,rr,x,u=t;f=dest/rr['file'];z=dest/rr['html'];wr(f,w);z.write_text(dos_html(w),encoding='utf8');return{'task':w['task'],'title':w['title'],'state':rr['state'],'canonical':w['canonical'],'file':rr['file'],'html':rr['html'],'parent_R8_sha256':rr['sha256'],'sha256':H(f),'html_sha256':H(z),'criteria':rr['criteria'],'r9_measured_or_document':x,'unexecuted':u}
 with ThreadPoolExecutor(max_workers=8)as px:ix=list(px.map(write,docs))
 catalog=dest/'Dovezi_criterii.json';wr(catalog,{'schema':'A12.R9','R8_parent':S(R8/'Dovezi_criterii.json'),'evidence':ev,'inverse_task_requirement_links':rev})
 wreg=dest/'Registru_reexecutare_R9.json';wr(wreg,{'schema':'A12.R9','population_652':len(ix),'criteria_2619':len(register),'rows':register,'open_NEEXECUTAT':[v['criterion']for v in register if v['R9']=='NEEXECUTAT']})
 page=dest/'Audit_individual_P01_R9.html';page.write_text(indexer(ix,counts['NEEXECUTAT']),encoding='utf8')
 inp=[E/'A11_control_A12_R8.json',E/'A11_control_suplimente_R9_A03_177_CESIRO1.json',E/'A11_control_A06_oracole_postR8.json',E/'A11_dispozitii_C03_C10_R8.json',E/'R9_pregatire/EVA_Export/Runtime_CESIRO1_izolat.json',E/'R9_pregatire/A03/A03_raport_R9.json',E/'R9_pregatire/A05/A05_raport_R9.json',plan,reread,P9/'A12_receptii_R9_faza1.json',P9/'T04_07_08_parser_oracles.json',P9/'T04_09_reconcilieri.json',P9/'T35_08_acord_bilateral.json',P9/'T35_09_predare_commituri.json',P9/'T220_detector_PG.json',P9/'T314_final_integrare_A.log',P9/'T204_07_clasificator_ferestre.log',P9/'T220_validator_documentar.log',P9/'R9_scripturi_Git_T06_T204_T314.log',P9/'Dictionar_T04_CESIRO.json']
 inp.extend([E/'R9_pregatire/A05/Registru_R9_A05.json',E/'R9_pregatire/A05/Manifest_R9_A05.json',P9/'Relectura_882_addendum_aliasuri.json',E/'A11_control_R9_882_pointeri.json',E/'A11_control_supliment_A05_R9.json'])
 cfg={'utc':now(),'schema':'A12.R9.P01','independent_grade':None,'product_grade':None,'immutable_parent':S(R8/'MANIFEST_R8.json'),'quality_R8_by_A11':6.4,'under_independent_audit':True,'counts':{'cases':len(ix),'criteria':len(register),'R8_NEEXECUTAT':1226,'R9_NEEXECUTAT':counts['NEEXECUTAT'],'states':counts,'earlier_177':177,'partial_218_separate':218,'partial_external_38_nonadditive':38,'overlap_177_38':2,'previous_oracle_missing_882':882,'individually_located_sources':882,'comparator_recovered_not_just_locator':9,'exercised':scopevals,'relations_by_type_added_in_R9':types,'total_relations':sum(map(len,rev.values()))},'R8_Q3_and_Q5':'Q, P93 și cele două comenzi de staging sunt origini diferite. Un document C_Invoice ori un test de motor nu sunt suficiente pentru a atribui plata, returul sau vizualizarea acelui document unei alte origini. La T329 identificarea ASI în tranzacția de stoc rămâne distinctă de câmpul M_AttributeSetInstance_ID din Fact_Acct.','limits':['Localizarea celor 882 poziții nu creează etaloane pentru toate cazurile.','31 commituri T35 enumerate au obiect valid, toate apar în log și 30 au hash direct în celula de commit.','Fără scoring autonom al auditului sau produsului; o abatere a gărzii are sens numai în versiunea și la stratul probat.','Cohorta de 218 rămâne parțială până la o probă explicită asupra restului cerinței.'],'input_files':{p.relative_to(B).as_posix():H(p)for p in inp if p.exists()},'assets':{p.name:H(p)for p in [catalog,wreg,page]},'records':ix}
 cfg['882_identity_and_scope']={'physical_positions':858,'historical_git_rows_with_blob_different_from_cutoff':68,'explicit_id_vechi_pairs':{'T22.15':'T22.1','T36.18':'T36.7'},'source':S(P9/'Relectura_882_addendum_aliasuri.json'),'effect_on_functional_score':None}
 cfg['Q3_outstanding_cases']=[{'target':'T354-R2-021','already_measured':'staging două comenzi ord=0, A=6/5 şi 4 componente; CO pentru a treia la 6','still_due':'două C_Order persistate, overlap de tranzacții pe rezervă plus retry pentru aceleași documente și loturi; urmărește costul și două G1.'},{'target':'T216-R2-002/005/006','already_measured':'Q exclusă, P93 validată şi facturată numai în originea ei istorică','still_due':'păstrează cheile aceleiași origini eligibile în două ramuri SO→pick→aviz→AWB→factură→încasare şi SO→retur; verifică seria şi numărul în DOM pentru aceeași factură și comisionarul autorizat.'}]
 wr(dest/'A12_raport.json',cfg);print('R9',preview,H(dest/'A12_raport.json'),counts['NEEXECUTAT'],scopevals,types)
if __name__=='__main__':main(os.environ.get('A12_R9_PREVIEW')=='1')

