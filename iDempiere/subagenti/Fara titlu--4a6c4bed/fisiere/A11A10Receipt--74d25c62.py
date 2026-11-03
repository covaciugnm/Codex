import pathlib,json,hashlib,zipfile,ast,re,collections,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere');B=R/'A10_Instrumente_ramase_lot03';O=R/'A11/Val03_loturi'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((B/n).read_text(encoding='utf-8-sig'))
def ref(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
checks=[]
def ck(label,value):
 checks.append({'check':label,'ok':bool(value)})
 if not value:raise AssertionError(label)
def save(n,x):
 p=O/n;assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return ref(p)
m=load('Manifest_lot03.json');ck('manifest signature',sha((B/'Manifest_lot03.json').read_bytes())=='7b3289641e6321eeccbac23e3fb9d03ebc570f9906928e9902b3aea5ff41724d')
for n,v in m['files'].items():
 b=(B/n).read_bytes();ck('manifest '+n,sha(b)==v['sha256'] and len(b)==v['bytes'])
f=load('Fise_4_surse.json');ck('four sources',len(f)==4)
for e in f:
 s=e['source'];b=(B/'sources'/pathlib.PurePosixPath(s['path']).name).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 ck('source SHA/OID '+e['id'],sha(b)==s['sha256'] and oid==s['git_object']==e['OID_rehashed'])
pure=load('Rezultate_I17_pure_28.json');dom=load('Rezultate_I17_DOM_18.json');shell=load('Rezultate_shell_27_cazuri.json')
ids=[c['id'] for c in pure+dom]+[c['case'] for c in shell]
ck('73 disjoint cases 28+18+27',len(pure)==28 and len(dom)==18 and len(shell)==27 and len(ids)==len(set(ids))==73)
ck('shell families',collections.Counter(c['case'][:3] for c in shell)=={'I01':8,'I04':14,'I10':5})
with zipfile.ZipFile(B/'Dovezi_complete_lot03.zip') as z:
 names=z.namelist();inv=load('Inventar_final_fixture.json');ck('4215 zip and inventory exact names',len(names)==len(set(names))==4215 and set(names)==set(inv))
 for n,v in inv.items():
  b=z.read(n);ck('zip inventory '+n,sha(b)==v['sha256'] and len(b)==v['bytes'])
 for folder,expected in [('shell','7122b2c62f52a47b0517076809e42a165624712f49f3c99f4dd7f68b9c6d3506'),('shell_v2','9c28c424f0121bf274c50a47fb97d05c7c5941a6dd045ad957f12ca03ce3053a')]:
  b=z.read(folder+'/Preparation_manifest.json');ck('preexecution manifest '+folder,sha(b)==expected)
  for n,h in json.loads(b).items():ck('preexecution case '+folder+'/'+n,sha(z.read(folder+'/'+n.replace('\\','/')))==h)
 for c in shell:
  d=c['evidence_directory_in_zip'];p=json.loads(z.read(d+'/Case_preflight.json'));script=z.read(d+'/comparator.sh')
  ck('stdout '+c['case'],sha(z.read(d+'/stdout.txt'))==c['stdout_sha256']);ck('stderr '+c['case'],sha(z.read(d+'/stderr.txt'))==c['stderr_sha256'])
  ck('preflight '+c['case'],sha(z.read(d+'/Case_preflight.json'))==c['case_preflight_sha256']);ck('comparator '+c['case'],sha(script)==p['comparator_sha256'])
  ck('diff '+c['case'],sha(z.read(d+'/source.diff'))==p['diff_sha256'])
  for n,v in p['fixtures_and_shims'].items():
   if n.startswith(('bin/','guard/')) or n in ('dispatch.py','queue.sh','comparator.sh','config.json'):
    ck('shim immutable '+d+'/'+n,sha(z.read(d+'/'+n))==v['sha256'])
  diff=z.read(d+'/source.diff').decode();removed=[x[1:] for x in diff.splitlines() if x.startswith('-') and not x.startswith('---')]
  if c['case'].startswith('I04'):ck('I04 changes only QB '+c['case'],len(removed)==1 and 'QB=/home/' in removed[0])
  elif c['case'].startswith('I10'):ck('I10 changes only R/SP '+c['case'],len(removed)==2 and 'R=/home/' in removed[0] and removed[1].startswith('SP=/tmp/'))
  else:
   # Five fixed historical refs are the only substitutions, including labels and filenames.
   original=(B/'sources/verifica_integrare_L1.sh').read_text();ss=script.decode();refs=['b1a127f4175','01619179149','934a1345228','681970daa3c','8acd3311a13']
   head=re.search(r'^I=([0-9a-f]+); V=([0-9a-f]+); A=([0-9a-f]+)$',ss,re.M).groups();old1=re.search(r'echo "([0-9a-f]+)\.\.\$V în afara',ss).group(1);old2=re.search(r'echo "([0-9a-f]+)\.\.\$I~1 pe perimetrul',ss).group(1)
   for old,new in zip(refs,[*head,old1,old2]):original=original.replace(old,new)
   ck('I01 only five refs '+c['case'],original==ss)
 for n,out in [('pure/Results.json',pure),('dom/Results.json',dom)]:ck('results exact archive '+n,json.loads(z.read(n))==out)
 boundary=json.loads(z.read('dom/Boundaries.json'));tree=ast.parse((B/'sources/proba_buton.py').read_text());js=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='JS_FEREASTRA' for t in n.targets))
 ck('original JS exact hash',sha(js.encode())==boundary['original_js_sha256']);ck('no observed HTTP/context closed',boundary['http_requests_observed']==[] and boundary['contexts_closed'])
 log=z.read('shell/I04_normal/stdout.txt').decode();ck('normal denominator fourteen vs fifteen',len(re.findall(r'^   rc=\d+$',log,re.M))==14 and '14 pași rc 0 din 15' in log)
 for key in ['hidden_row','stack_order']:ck('screenshot '+key,sha(z.read('dom/'+key+'.png'))==sha((B/(key+'.png')).read_bytes()))
qa=save('QA_A11_A10_lot03_v1.json',{'checks':checks,'count':len(checks),'issues':[],'scope':'rehash integral manifest/ZIP, toate cele 27 comparatoare/diffuri, shims selectate structural, 73 identități, 4 surse SHA/Git OID; nu 73 PASS-uri de produs'})
dispositions=[
 {'id':'F01','verdict':'ACCEPTAT P2 propus pentru raportarea conflictului','reason':'Git real local rc1 versus etichetă rc0; martor A11 separat confirmă mecanismul substituției. Nu se transferă la checkout operațional.'},
 {'id':'F02','verdict':'ACCEPTAT P2 propus pentru contractul consumatorului de exit code','reason':'Dependențe sintetice refuzate, statusurile textuale există dar rc final0. Nu este dovadă de PASS explicit ori de defect comercial.'},
 {'id':'F03','verdict':'ACCEPTAT constatare pe pașii 8/9, impact condiționat','reason':'Acești pași afișează false/hashuri diferite fără aserție. I17 are guardă separată; nu generaliza la absența oricărei izolări în pipeline real.'},
 {'id':'F04','verdict':'ACCEPTAT P2 propus, lifecycle sintetic','reason':'Mesaj slot eliberat după rc72 și release pe stdout nevid din acquire rc4. Nu sunt sloturi reale eliberate sau păstrate de proba comparatorului.'},
 {'id':'F05','verdict':'ACCEPTAT P3 propus','reason':'14 linii de statut, numitor15 din textul comenzii. Numitor verificat independent din logul brut.'},
 {'id':'F06','verdict':'ACCEPTAT limită a comparatorului; P2 condiționat de folosirea ca atestare integrală','reason':'Dublurile sunt pierdute. A11 adaugă separat patru martori BytesIO, inclusiv payload corupt cu CRC central neschimbat acceptat de funcția m; nu se afirmă selecție de clasă JVM.'},
 {'id':'F07','verdict':'ACCEPTAT limită de contract diagnostic; fără severitate automată','reason':'Statusele individuale sunt vizibile; efectul asupra unei porți presupune consumator dovedit. Comparatorul rm este no-op și nu atestă cleanup real.'},
 {'id':'F08','verdict':'ACCEPTAT P2 propus pentru colector, nu defect ZK demonstrat','reason':'JS original numără rândul display:none și heading ascuns. Imaginea executorului a fost inspectată independent de A11; DOM sintetic.'},
 {'id':'F09','verdict':'ACCEPTAT P2 propus pentru colector, condiție de UI neprobată','reason':'Ultima fereastră DOM diferă de frontmost în fixture. Captura arată Front, valoarea returnată Back. panou() are propriile refuzuri; nu se echivalează metodele.'},
 {'id':'F10','verdict':'ACCEPTAT grup eterogen de limite, nu zece defecte ori defect runtime unic','reason':'Intrări invalide/manual duplicate încalcă invariantul. Regex comentarii, PNG parțial și chei numerice duplicate au probe componente. CLI exit și restaurare limbă sunt lectură/logică, fără execuție CLI completă sau preferință nativă salvată.'}]
report=save('Verdict_A11_A10_lot03_v1.json',{
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','head':m['head'],'disposition':'ACCEPTAT LIMITAT pe cele patru fișiere; zero recepții integrale',
 'manifest_executor':ref(B/'Manifest_lot03.json'),'qa':qa,'independent_evidence':[ref(O/'Control_A11_Bash_exit_substitution_v1.json'),ref(O/'Proba_A11_CRC_I01_lot03_v1.json')],
 'counts':{'sources':4,'I17_original_pure_cases':28,'I17_original_JS_or_panou_on_synthetic_DOM_cases':18,'shell_comparator_cases':27,'executor_unique_cases':73,'excluded_shell_infrastructure_attempts':13,'excluded_preexecution_SyntaxError':1,'A11_additional_CRC_cases':4,'A11_prior_Bash_controls':2},
 'files':[{'id':e['id'],'path':e['source']['path'],'OID':e['source']['git_object'],'sha256':e['source']['sha256'],'accepted_scope':'COMPONENTE_ORIGINALE_PURE_SI_DOM_SINTETIC' if e['id']=='R12-I17' else 'COMPARATOR_ORCHESTRARE_CU_REMAPARI_SI_DEPENDENTE_SINTETICE','verdict':'PARTIAL','integral':False} for e in f],
 'finding_dispositions':dispositions,
 'rejected_claims':['Nu sunt 73 teste comerciale trecute.','Nicio execuție completă originală a celor trei scripturi Bash pe infrastructura lor normală.','Nicio recepție UI/ZK, browser cu rol/login, preferință persistentă, Docker, coadă, AD_Form sau pipeline L6.','Niciun transfer de acoperire la serverHEAD1687; numai df85 pentru identitatea surselor.','Nu se închid fișiere/taskuri/C03/C10 și niciunul din cele 17 contracte.'],
 'boundary_limits':['Audit hook Python cooperativ, nu sandbox OS; ramura descriptor int este permisă în harnessul pure al executorului și nu primește atestare de izolare generală.','Interceptarea HTTP(S) în context nou Chromium și zero cereri observate nu sunt o probă generală asupra oricărui trafic posibil al procesului browser.','Shims declarate, canari inerti și Git local verifică numai căile inspectate; nu se creditează gărzile comerciale înlocuite de stub.'],
 'cleanup':{'executor':'Refuz automat Remove-Item pe D:/CodexWork/a10-r12-l03; 4215 fișiere păstrate, fără reîncercare. Browserul închis conform artifactului. Nicio atestare zero-resturi.','A11':'Martorii CRC folosesc BytesIO și raport; nu creează scratch suplimentar. Directoarele A11 anterioare refuzate rămân păstrate.'},
 'next_checklist':['Prioritate recepției N05 pe proces/binding/schema/commit/concurență/rollback real în clona sintetică.','Apoi DocAction/Fact_Acct și ZK cu rol, cu G1/G2/G3, CPP/CPA distincte, costuri o singură dată și stoc comun.','Pentru ajutoare, adaptează capturarea rc și observatorul existente; cere registru structurat numitor/rezultat/proveniență și refuz ambiguitate, fără motor nou.','A12 va corela distinct cele 19 instrumente parțiale în R12; niciun criteriu istoric automat îndeplinit.','Restituirea scratchurilor refuzate rămâne dependență explicită, fără încercare de ocolire.'],
 'global_score':None,'open_contracts':17})
seal=save('SIGILIU_A11_A10_lot03_v1.json',{'algorithm':'SHA256','immutable':True,'files':[report,qa,ref(O/'Proba_A11_CRC_I01_lot03_v1.json'),ref(O/'Control_A11_Bash_exit_substitution_v1.json')],'executor_manifest':ref(B/'Manifest_lot03.json')})
print(json.dumps({'report':report,'seal':seal,'QA_count':len(checks)},ensure_ascii=False))
