from pathlib import Path
import json,hashlib,datetime,shutil
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A10_Instrumente_ramase_lot03')
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
findings=load(O/'Constatari.json')
patterns={
 'A10-L03-F01':{'garzi.sh':['merge-tree --write-tree']},
 'A10-L03-F02':{'reteta_L6.sh':['pas()','pas 4_proba','pas 5_verifica','pas 6_contraproba','pas 7_masca','pas 10_foi']},
 'A10-L03-F03':{'reteta_L6.sh':['pas 8_retea','pas 9_md5']},
 'A10-L03-F04':{'reteta_L6.sh':['trap ','SL=$(','elibereaza','opreste >']},
 'A10-L03-F05':{'reteta_L6.sh':['grep -c "rc=0"','pas 6_contraproba']},
 'A10-L03-F06':{'verifica_integrare_L1.sh':['def m(p)','i.filename: i.CRC','print(f"părinte']},
 'A10-L03-F07':{'verifica_integrare_L1.sh':['verifica_rulator.sh','garda rc=','secrete rc='],'garzi.sh':['r=$?; echo','rm -rf "${SP:?}"']},
 'A10-L03-F08':{'proba_buton.py':["const campuri =", "h3: [...c.querySelectorAll"]},
 'A10-L03-F09':{'proba_buton.py':['const w =','o = pg.evaluate(JS_FEREASTRA']},
 'A10-L03-F10':{'proba_buton.py':['def citeste_e','def png','def capitole','def premise','def ruleaza','self.limba(\'ro\')    # A']},
}
for f in findings:
 f.pop('lines',None);f['line_refs']={}
 for path,ps in patterns[f['id']].items():
  lines=(O/'sources'/path).read_text().splitlines();f['line_refs'][path]=[{'line':n,'source':s.strip()} for n,s in enumerate(lines,1) if any(p in s for p in ps)]
put(O/'Constatari.json',findings)
ds=load(O/'Fise_4_surse.json')
for d in ds:
 id=d['id'].replace('R12-','');d['counterexamples']=[f for f in findings if id in f['file'].split('/')];d['lab_resource_cleanup']='REFUZAT_AUTOMAT; fixture rămase în D:/CodexWork/a10-r12-l03; arhivă verificată, fără ocolire';put(O/('Fisa_'+id+'.json'),d)
put(O/'Fise_4_surse.json',ds)
put(O/'Cleanup_laborator.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resolved_own_root':'D:/CodexWork/a10-r12-l03','before_files':4215,'reparse_points':0,'attempted':'Native PowerShell Remove-Item -LiteralPath exact verified own root -Recurse -Force; archive SHA check included','result':'REJECTED_BY_AUTOMATIC_POLICY','stated_reason':'blocked by policy; no more detailed reason returned','command_executed':False,'bypass_or_retry':False,'retained_root_exists':Path('D:/CodexWork/a10-r12-l03').exists(),'retained_harness_scripts':[str(p) for p in Path('D:/CodexWork').glob('a10_l03_*.py')],'retained_other_fixture_untouched':'D:/CodexWork/p01-r12-masini-dates','archive_sha256':sha(O/'Dovezi_complete_lot03.zip'),'browser_contexts_closed':True,'operational_resources_created':0,'lab_cleanup_complete':False,'product_cleanup_credit':False,'required_next_action':'Curățare ulterioară prin mecanism autorizat; nu condiționează lectura/recepția dovezilor, dar blochează afirmația zero resturi.'})
p=O/'Raport_A10_instrumente_lot03.html';s=p.read_text();s=s.replace('</html>','<div class="note"><b>Resturi de laborator:</b> Controlul automat a refuzat ștergerea rădăcinii proprii D:/CodexWork/a10-r12-l03 cu motivul «blocked by policy». Nu s-a încercat ocolirea. Cele4215 fișiere sintetice și scripturile harness rămân; arhiva este verificată și browserul este închis. Nu au fost create resurse operaționale. Nu se acordă recepție pentru curățarea completă. <a href="Cleanup_laborator.json">Dovadă și inventar</a>.</div></html>').replace('Cele4215','Cele 4215');p.write_text(s,encoding='utf-8')
for p in Path('D:/CodexWork').glob('a10_l03_*.py'):shutil.copy2(p,O/'harness'/p.name)
manifest={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lot':'A10_Instrumente_ramase_lot03','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','plan_sha256':'4aeeaf61d73efa1a1155e9eecbbcc5564ddfeee4cda918fa5fa04c97f2ef7276','preflight_sha256':'23e2a6d93d137c47cd81f6be930fbf67de4c26357a181d95f858af525e687824','protocol_sha256':'13727927b40b797257ee4f483233638649df6bc9c205317759af093425379284','verdict_executor':'PARTIAL_CANDIDATE_A11; resurse locale reținute după refuz automat','sources':4,'cases_unique_interpretable':73,'commercial_tasks_closed':0,'native_or_business_credit':0,'A11_reception_pending':True,'files':{str(p.relative_to(O)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='Manifest_lot03.json'}}
put(O/'Manifest_lot03.json',manifest)
print(json.dumps({'manifest_sha256':sha(O/'Manifest_lot03.json'),'file_count':len(manifest['files']),'root_retained':Path('D:/CodexWork/a10-r12-l03').exists()}))
