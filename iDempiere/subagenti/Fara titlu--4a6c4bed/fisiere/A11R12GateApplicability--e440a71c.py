import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P=R/'executie/R12_plan_delta'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
old=R/'executie/delta/2026-11-02T22-49-25-027Z/00_STATUS_TASKURI.json'
new=R/'executie/delta/2026-11-02T23-15-23-444Z/00_STATUS_TASKURI.json'
delta=R/'executie/delta/2026-11-02T23-15-23-444Z/Delta.json'
a=read(old);b=read(new)
am={(x.get('proiect'),x['id']):x for x in a};bm={(x.get('proiect'),x['id']):x for x in b}
assert len(am)==len(a)==len(bm)==len(b)==996
assert am.keys()==bm.keys()
changes=[]
for k in am:
    if am[k]!=bm[k]:
        fields={f:{'old':am[k].get(f),'new':bm[k].get(f)} for f in sorted(am[k].keys()|bm[k].keys()) if am[k].get(f)!=bm[k].get(f)}
        changes.append({'project':k[0],'technical':k[1],'fields':fields})
assert len(changes)==1 and changes[0]['technical']=='T343'
assert set(changes[0]['fields'])=={'observatii','procent','ultima_actualizare'}
assert len([x for x in b if x.get('proiect')=='P01'])==693
assert am['P01','T240']==bm['P01','T240']
plan=P/'Plan_delta_R12_v2.json'; annex=P/'Plan_instrumente_noi_A10_v2.json'; verdict=P/'A11_verdict_plan_delta_R12_v2.json'
assert sha(plan)=='4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276'
assert sha(annex)=='e8775e62af6d3cd71861a2dd65c20d7a09892a95e0b846abbb88156a81047104'
assert sha(verdict)=='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
assert read(delta)['github_master_at_capture']==read(plan)['candidate']=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
manifest=read(P/'Manifest_sources_lues.json'); sources={x['path']:x for x in manifest['rows']}
checked=[]
for item in read(annex)['items']:
    if item['audit_control_id'] not in ('R12-I18','R12-I19'):continue
    s=item['source']; m=sources[s['path']]; f=pathlib.Path(m['local']);data=f.read_bytes()
    oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert sha(f)==s['sha256']==m['sha256'] and oid==s['git_object']==m['new_oid']
    checked.append({'id':item['audit_control_id'],'source':s,'frozen_copy':ref(f),'git_blob_recomputed':oid})
assert len(checked)==2
out={
 'schema':'A11.R12.gate_applicability.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'author':'A11 independent','mode':'Citire și comparație; zero execuții de produs în această verificare.',
 'inputs':[ref(x) for x in (old,new,delta,plan,annex,verdict)],
 'candidate':read(plan)['candidate'],'population':{'all':996,'P01':693,'added':0,'removed':0,'changed_tasks':1},
 'changes_recomputed':changes,'T240_row_unchanged':True,'T240_sources_rehashed':checked,
 'gate_decision':'APLICABIL lotului R12-I18/R12-I19, după preflight efectiv al executorului, pe copia identificată și nemodificată a candidatului.',
 'native_claim':{
   'text':'C-2.2 amendat la nativ: C_Order IP pe drumul T22/T216; T-NOU normalizare.',
   'status':'AFIRMAȚIE NOUĂ DE VERIFICAT. Nu este probă de execuție și nu închide cerințe.',
   'direct_contract':'D05 — T216 integritatea comenzii de canal până la aviz',
   'linked_contracts':['D01 — context, autorizare și roluri pe canal','D10 — UX/stări afișate versus native'],
   'followup':'A12 anexează impactul nominal; înaintea probelor dependente, fixează sursa cerinței C-2.2, actorul, starea C_Order IP observată, tranziția nativă T22/T216 și normalizarea T-NOU. Contraprobe de rol/context/stare, persistare, reluare și anulare rămân obligatorii.',
   'claimed_test_counts_credited':False,'contracts_closed':0},
 'os_hypothesis_erratum':{
   'target':'Plan_instrumente_noi_A10_v2.json /items R12-I18 /limit și comunicarea A11 anterioară despre numele «NU: …».',
   'previous_assertion':'Numele cu două puncte este invalid pe Windows.',
   'correction':'Aceasta este o ipoteză neconfirmată pentru calea și filesystemul concret. Pe NTFS colonul poate desemna un flux ADS. Se încearcă originalul în scratch după preflight și se înregistrează ce obiect/flux s-a creat și cum este găsit/șters. Nu se aplică adaptor preventiv.',
   'decision_rule':'Rezultatul observat decide dacă originalul rulează integral sau există o limită de mediu. Comparatorul/adaptorul, dacă devin necesare, au identitate și rezultat separat. Eroarea de mediu nu devine defect de produs și trecerea originalului nu dovedește browserul nativ.',
   'original_artifacts_modified':False,'plan_oracles_and_gate_unchanged':True},
 'limits':['HEAD este susținut de captura read-only a coordonatorului la 23:15, nu de un nou fetch A11.','Copiile surselor I18/I19 sunt rehashuite independent și legate de OID, nu s-a executat încă produsul în acest supliment.','Nota 10/10 privește planul v2; nu se atribuie notă produsului sau execuției integrale.'],
 'resources_created':'Numai documentul de audit și metoda; nicio clonă/serviciu/sesiune de produs.',
 'method':{'local_path':str(pathlib.Path(__file__)),'sha256':sha(pathlib.Path(__file__))}
}
dest=P/'Addendum_A11_aplicabilitate_gate_T240_T343_v1.json'
assert not dest.exists(), 'Nu suprascrie supliment sigilat'
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
seal=P/'Sigiliu_A11_aplicabilitate_gate_T240_T343_v1.json'
assert not seal.exists()
seal.write_text(json.dumps({'utc':out['utc'],'artifact':ref(dest),'method':out['method'],'parent_verdict':ref(verdict)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'addendum':ref(dest),'seal':ref(seal)},ensure_ascii=False))
