import json,pathlib,hashlib,datetime,functools
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';V=B/'A12/Val_05';O=B/'A11/Val05_preflight'
@functools.lru_cache(None)
def raw(p):return pathlib.Path(p).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
@functools.lru_cache(None)
def j(p):return json.loads(raw(p).decode('utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(raw(p))}
def vh(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
checks=[];refs=[];pointers=[]
def ck(n,b,d=None):checks.append({'check':n,'ok':bool(b),'details':d});assert b,(n,d)
def resolve(x):
 p=pathlib.Path(x['path']);p=p if p.is_absolute() else R/p
 assert sha(p)==x['sha256'],x
 if 'bytes'in x:assert len(raw(p))==x['bytes'],x
 refs.append(x)
 if 'pointer' not in x:return None
 z=j(p)
 for k in x['pointer'].removeprefix('#').split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');z=z[int(k)] if isinstance(z,list) else z[k]
 pointers.append(x);return z
def walk(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:resolve(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
mp=V/'MANIFEST_preflight_Val05_0245_v2.json';m0=V/'MANIFEST_preflight_Val05_0245.json';sp=V/'Supliment_populatie_0245.json';hp=V/'Handoff_preflight_Val05_v2.json'
for p,h in [(mp,'40b3bab9c238b67fe1130ce04e887f99fabf91ba26266f0dfac90737699e4bdf'),(m0,'ddb532e29613c72143fbe69ed70fa0bdfc9ccc8ac6542b9743a7e897d439ebd1'),(hp,'31646917b0f282dae86030915177550d26f92991ecc98f29556140454f341a1d'),(sp,'a5ef9b8ff5529c21ab6c1f7a2728ed58c3b523b6fbf728988bc03df72a80fbbf')]:ck('Sigiliu fix '+p.name,sha(p)==h)
for p in [mp,m0]:
 m=j(p);walk(m)
 for x in m['files']:
  if x['path'].endswith('.json'):walk(j(R/x['path']))
ck('12 ieșiri inițiale și 2 aditive',len(j(m0)['files'])==12 and len(j(mp)['files'])==2)
c=j(V/'Comparatie_997_randuri.json');old=j(R/c['before']['path']);new=j(R/c['after']['path']);key=lambda x:(x.get('proiect'),x['id'])
ck('997 rânduri unice înainte/după',len(old)==len(new)==len(c['rows'])==len({(x['project'],x['id']) for x in c['rows']})==997)
dif=[]
for x in c['rows']:
 a=old[int(x['before_pointer'][1:])];b=new[int(x['after_pointer'][1:])];assert key(a)==key(b)==(x['project'],x['id'])
 assert vh(a)==x['before_value_sha256'] and vh(b)==x['after_value_sha256']
 fs=[k for k in sorted(a.keys()|b.keys()) if (k in a)!=(k in b) or a.get(k)!=b.get(k)]
 assert fs==x['changed_fields'] and (a==b)==x['entire_row_equal']
 assert a['stare_generala']==b['stare_generala']==x['before_state']==x['after_state']
 if fs:dif.append(x)
ck('Diferență unică T343 și nicio stare schimbată',len(dif)==1 and dif[0]['id']=='T343' and not c['added'] and not c['removed'])
s=j(sp);f=s['focus_requirement_equality'];unequal=[]
ck('19 taskuri și 171 de predicate normative',len(f)==19 and sum(len(x['normative_fields']) for x in f)==171)
for x in f:
 a=resolve(x['before']);b=resolve(x['after']);assert a['id']==b['id']==x['alias'];assert b['stare_generala']==x['current_state']
 for n in x['normative_fields']:
  k=n['field'];eq=(k in a)==(k in b) and a.get(k)==b.get(k)
  assert n['equal']==eq and n['before_present']==(k in a) and n['after_present']==(k in b)
  assert n['before_value_sha256']==vh(a.get(k)) and n['after_value_sha256']==vh(b.get(k))
  if not eq:unequal.append({'alias':x['alias'],'field':k})
 assert x['entire_row_equal']==(a==b) and x['new_execution_credit']==0
ck('Singurul predicat schimbat este proveniența documentară T343',unequal==[{'alias':'T343','field':'documente_produse'}])
da=j(V/'Analiza_document_nou_T343_0245.json');doc=R/da['document']['path'];lines=raw(doc).decode('utf8').splitlines()
ck('Document cu blob autentic',hashlib.sha1(b'blob '+str(len(raw(doc))).encode()+b'\0'+raw(doc)).hexdigest()==da['verified_blob_oid']=='be0fad64d8c4475d0af2fb290e7bcc4c875608a3')
for name,a in da['anchors'].items():
 expected='\n'.join(lines[a['line_start']-1:a['line_end']]);ck('Ancoră exactă '+name,expected==a['exact_text'])
ck('Documentul este numai proveniență',da['new_product_executions']==da['new_full_acceptances']==0 and da['score'] is None and all(x['new_execution_credit']==0 for x in da['semantic_dispositions']))
z=j(V/'Dispozitii_10_zone_preflight_Val05.json');ck('10 zone fără credit nou',len(z['rows'])==len({x['owner'] for x in z['rows']})==10 and all(x['new_executions']==0 and not x['peer_performed_inferred'] for x in z['rows']))
for x in z['rows']:
 p=resolve(x['source']);assert p['assigned_files']==x['assigned_files_unchanged']
ck('6728 rutări păstrate',sum(x['assigned_files_unchanged'] for x in z['rows'])==6728)
h=j(hp);counts=h['counts_preserved'];expected={'bounded_evidence_source_identities':44,'original_component_or_method_primary':33,'shell_comparator_primary':5,'record_or_type_primary':2,'fixture_binding_metadata_primary':4,'event_pairs':50,'historic_R11_reference_only':116,'technical_identities':6728,'historical_task_dossiers':652,'historical_criteria':2619,'full_files':0,'full_tasks':0,'full_contracts':0,'open_contracts':17,'new_coverage_from_this_preflight':0}
ck('Metrici fără echivalare sau credit nou',counts==expected and h['new_product_execution_credit']==0 and h['score'] is None)
ck('V2 separă aplicabilitatea de recepția nominală',h['A11_applicability_pending'] is False and h['A11_A12_supplement_reception_pending'] is True and j(mp)['A11_limited_applicability_confirmed'] is True)
out={'schema':'A11.R12.Val05.A12.preflight.receipt.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','method':'Citire locală și rehash al manifestelor v1/v2, fișierelor și pointerilor lor; recalcul independent pentru toate cele 997 de rânduri și 171 de predicate normative. Ancorele documentului T343 comparate cu octeții Git și interpretarea proprie A11 deja sigilată. Nu s-a executat runnerul A12 sau vreo comandă citată de document.',
'manifest':ref(mp),'initial_manifest_preserved':ref(m0),'supplement':ref(sp),'handoff':ref(hp),'checks':checks,'reference_instances_checked':len(refs),'pointer_instances_checked':len(pointers),'unique_reference_paths':len({x['path'] for x in refs}),
'decision':'ACCEPTAT LIMITAT: recepție nominală a preflightului Val05, fără recepție de implementare sau transfer între versiuni.',
'dispositions':['Populația este aceeași 997/694. Cele 997 de stări sunt identice; T240 și T386 sunt identice integral.','T343 păstrează starea audit; procentul 56 este progres declarat. documente_produse s-a schimbat și este tratat explicit, fără afirmația falsă că toate câmpurile normative sunt egale.','Documentul T343 este autentic ca blob și atribuit altei revizii/copie de site. LR-6/B16, nota 9/10 și rezultatele declarate nu sunt rezultate ale campaniei df85.','V2 corectează numai eticheta stării porții: aplicabilitatea generală era deja primită; recepția nominală A12 era încă pending. Prima ediție rămâne intactă.','44 = 33 + 5 + 2 + 4 sunt niveluri de observație diferite, nu 44 de fișiere validate. Cele 50 de perechi cale/eveniment, 116 referințe R11, 652 de fișe și 2619 criterii rămân numărători separate.','Cele 17 contracte și toate recepțiile integrale rămân deschise. Protocoalele concrete au porți distincte; această recepție nu autorizează automat execuția DocAction ori generatorului.','HEAD operațional c594a93a este exclus; nicio scriere operațională sau rerulare inutilă. Cele șase rădăcini cu cleanup refuzat nu au fost atinse.'],
'product_score':None,'audit_global_score':None,'product_executions':0,'operational_writes':0,'resources_created':'Numai verdictul și runnerul A11.'}
op=O/'Verdict_A11_receptie_preflight_A12_0245_v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');rp=O/'Runner_A11_receptie_preflight_A12_0245_v1.py';assert not rp.exists();rp.write_bytes(pathlib.Path(__file__).read_bytes());seal=O/'SIGILIU_A11_receptie_preflight_A12_0245_v1.json';assert not seal.exists();seal.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[ref(op),ref(rp)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'verdict':ref(op),'seal':ref(seal),'refs':len(refs),'pointers':len(pointers)},ensure_ascii=False))
