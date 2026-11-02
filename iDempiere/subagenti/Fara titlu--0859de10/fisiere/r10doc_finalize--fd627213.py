from pathlib import Path
import subprocess as sp,datetime as dt,gzip,json,hashlib,re
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');folder=B/'executie/R10_pregatire/A12/R10_documentar_supliment';folder.mkdir(exist_ok=True);base='6df998aee0e514d30856c461962afe99ebd0d113';source_local=Path('D:/CodexWork/A12_evidence_20261102/blobs');git='/home/saga-server/Documents/EvA-Contab';digest=lambda x:hashlib.sha256(x).hexdigest();oid=lambda raw:hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();rpath=lambda p:p.relative_to(B).as_posix()
def dump(p,data):p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
def fs(p):return {'file':rpath(p),'sha256':digest(p.read_bytes())}
def remote(cmd):
 p=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git','-C',git,*cmd],capture_output=True,timeout=70);assert not p.returncode,p.stderr;return p.stdout
reg=B/'executie/R10_pregatire/A12/Cai_nominale_873_fara_dublare.json';records=json.loads(reg.read_bytes())['records'];require={x['task']:x for x in records if x['task']in ['T04.12','T35.11','T22.15']};ex={}
def get(key,path,ob=None):
 if not ob:ob=remote(['rev-parse',base+':'+path]).decode().strip()
 raw=remote(['cat-file','blob',ob]);assert oid(raw)==ob
 ex[key]={'project_path':path,'git_blob':ob,'raw_sha256':digest(raw),'extracts':[]};return raw.decode('utf8')
def pick(k,txt,rg=None,nums=[]):
 ss=txt.splitlines()
 for n,s in enumerate(ss,1):
  if n in nums or rg and re.search(rg,s):ex[k]['extracts'].append({'lineno':n,'line_sha256':digest(s.encode()),'text':s[:780],'truncated':len(s)>780})
root='Documentatie/echipa-2026-10-09/';g=root+'T35-cadru-platforme-vanzari/';c=root+'T22-flux-comenzi-cesiro-reconciliere-incasari/';q=root+'T04-conectori-parteneri-citire/'
def norm(t):r=require[t];k='require_'+t;s=r['source_locator'];v=get(k,s['file'],s['blob_or_file_sha']);return k,v
k,t=norm('T35.11');pick(k,t,nums=[18,29,30,31,33,248,254,256,257,282,283])
l1=get('G1',g+'dovezi-11-L1a/TestT35Cadru_varf.out');l2=get('G2',g+'dovezi-11-L1a/TestT35Cadru_merge.out');assert l1==l2;pick('G1',l1,rg=r'REZULTAT|^== G8');pick('G2',l2,rg=r'REZULTAT|^== G8')
b35=get('G3',g+'dovezi-11-L1a/r2/contraproba_g8.out');pick('G3',b35,rg=r'### varianta.*REZULTAT')
rev2=get('G4',g+'dovezi-11-L1a/r2/varf-4b77dfaee1/TestT35Cadru.out');pick('G4',rev2,rg=r'REZULTAT|E8 \(E10')
diff=get('G5',g+'dovezi-11-L1a/diffclase_varf_comis_vs_construit.txt');pick('G5',diff,rg=r'intrari|doar_in|diferite')
def gcheck(s):
 m=re.findall(r'varianta (\w+):.*?REZULTAT:\s*(\d+) OK, (\d+) FAIL \| exit=(\d+)',s);return {x:tuple(map(int,v))for x,*v in m}
expected={'A_alta_metoda':(70,0,0),'B_in_ensureT35':(69,1,1),'C_r1_alta_metoda':(69,1,1)};assert gcheck(b35)==expected
bad35=b35.replace('REZULTAT: 69 OK, 1 FAIL | exit=1','REZULTAT: 70 OK, 0 FAIL | exit=0',1);assert gcheck(bad35)!=expected
assert len(re.findall(r'^\s*OK\s+',l1,re.M))==70 and len(re.findall(r'^== G\d',l1,re.M))==12
k,t=norm('T22.15');hist=json.loads(t)['ramase'][5]['copii'][0];ex[k]['extracts'].append({'pointer':'/ramase/5/copii/0','parsed':hist})
cap=B/'capturi/00_STATUS_TASKURI.json';cr=json.loads(cap.read_bytes())[111];ex['cap']={'source_file':fs(cap),'pointer':'/111','extracts':[{'id':cr.get('id'),'alias':[x.get('id')for x in cr.get('id_vechi',[]) if isinstance(x,dict)],'state':cr.get('stare'),'title_prefix':str(cr.get('titlu',cr.get('denumire','')))[:75]}]}
s22=get('T22Verdict',c+'105_A1_verdict_integrare_B.md');pick('T22Verdict',s22,nums=[19])
def decisions(h,row,s):
 return {'authenticated_historical_alias':h['id'] in [z['id']for z in row['id_vechi']if isinstance(z,dict)] and row['id']=='T22.15' and h['task']=='T22','decision':all(x in h['titlu'] for x in ['«reface»','copie durabilă','K-TEST','K-AUD-C','59d88ca'])and h['decis_la']=='15.10.2026 13:44','integration_gate_step_1_and_step_2':bool(re.search(r'039a336fec.*Pasul 2.*BLOCAT.*59d88ca',s)),'forbidden_old_hash_conflation':'039a336fec'!='59d88ca'}
dc=decisions(hist,cr,s22);assert all(dc.values()),dc;bad22=decisions({**hist,'id':'T22.2'},cr,s22.replace('rămâne BLOCAT','a trecut'));assert not bad22['authenticated_historical_alias'] and not bad22['integration_gate_step_1_and_step_2']
k,t=norm('T04.12');pick(k,t,nums=[71]);v2=get('T04v2',q+'02_manager_plan_v2.md');pick('T04v2',v2,nums=[104,106]);cc=get('T04decision',q+'11_fable_decizii_plan_v2_audit.md');pick('T04decision',cc,nums=[1,7,9])
names=re.findall(r'\x60(Test\w+)\x60',t.splitlines()[70]);assert names==['TestConectoriCitire','TestDocumentePartener','TestCorelareDecontari','TestComparatieSaga']
# A complete read-only list from the fixed commit. Matching result contains only the four contract names and corroborating separate alias candidates.
allpaths=remote(['ls-tree','-r','--name-only','-z',base]).decode('utf8').split('\0');allpaths=[s for s in allpaths if s]
def paths_four(v):return {n:[x for x in v if x.rsplit('/',1)[-1]==n+'.java']for n in names}
found=paths_four(allpaths);assert sum(map(len,found.values()))==1 and len(found['TestComparatieSaga'])==1
badset=[s for s in allpaths if s!=found['TestComparatieSaga'][0]];neg4=paths_four(badset);assert sum(map(len,neg4.values()))==0
ex['FullTree']={'cutoff':base,'command':'git ls-tree -r --name-only -z '+base,'path_count':len(allpaths),'raw_stdout_sha256':digest(('\0'.join(allpaths)+'\0').encode()),'wanted_java_filename':names,'exact_matches':found,'other_possible_classes':{n:[p for p in allpaths if p.endswith('/'+n+'.java')]for n in ['TestCorelareComenzi','TestT32D6ImportExtrasIban','TestComparatieSagaEcran']}}
tjava=get('T04cmp',found['TestComparatieSaga'][0]);pick('T04cmp',tjava,rg=r'public static void main|private static void.*[tT]0[123]|/proc/self/fd|T-03: excepție')
P=folder/'Extras_Git.json';dump(P,{'cutoff':base,'extracts':ex,'full_self_contained_quotes':'Text up to 780 characters per verified line, SHA computed on original complete decoded line before preview.'})
def xr(key):return fs(P)|{'pointer':'/extracts/'+key}
rows=[]
def add(task,expected,seen,neg,lim,refs):
 cid=require[task]['criterion'];rows.append({'criterion':cid,'normative':require[task]['norm'],'kind':'Recalcul static al documentelor sau codului, domeniu explicit','expected':expected,'observed':seen,'negative_or_control':neg,'limit':lim,'references':refs+[fs(reg)|{'pointer':'/records/'+str(next(i for i,w in enumerate(records)if w['criterion']==cid))}],'implementation_verdict':None})
jvm=folder/'JVM_T35Cadru.json'; current=[];references=[]
for z in json.loads(jvm.read_bytes()):
 lg=B/z['log']['file'];st=lg.read_text(encoding='utf8').splitlines();idx=next(i for i,w in enumerate(st,1)if w.startswith('REZULTAT:'));g8=next(i for i,w in enumerate(st,1)if 'OK'in w and 'E8 (E10:'in w);assert z['exit']==0 and '71 OK, 0 FAIL'in st[idx-1]
 current.append({'jar':z['target'],'source_sha256':z['source_sha'],'target_sha256':z['jar_sha'],'result':st[idx-1],'g8':st[g8-1]});references.extend([fs(lg)|{'line':i0,'line_sha256':digest(st[i0-1].encode())}for i0 in [idx,g8]])
add('T35.11','R1 cod și merge, R2 remediere G8 cu loc separat de integrare și probă din buton. Pentru controlul documentar G8 sunt necesare 3 rezultate distincte A=70/0/0, B și C=69/1/1.',{'archived_G8':gcheck(b35),'r1_headers':12,'r1_physical_assertions':70,'both_r1_logs_share_same_blob':True,'gate_history':'R1 cod 9/10 refuzat; R2 cod 10/10 la 4b77dfaee1. Merge simulat cu master avea conflict de etichete; probele din buton erau explicit transferate testerului 12-L1.','independent_JVM_now':current},{'mutant_B_claimed_green':gcheck(bad35),'matches_oracle':gcheck(bad35)==expected,'location':'replace only the first B red score in memory; historical file unchanged'},'Comparația statică validează cifrele din înscris, iar cele 71 de verificări curente rulează clasa din sursa fixată pe JAR Git și pe copia instalată. Rulările sunt de componentă; fără tranzacție ERP, ERP UI sau probă de partener. Nota veche aparține acelei porți istorice.',[xr(i)for i in ['require_T35.11','G1','G2','G3','G4','G5']]+references)
add('T22.15','Piste diferite: refacerea variantă (a) a B-SBE din spec pe copie durabilă, alias vechi T22.1, iar hashul de pas1 nu dovedește proba site de pas2.',{'positive_checks':dc,'date_decision':hist['decis_la'],'historical_row_state':hist['stare'],'decision_author':hist['actualizat_de'],'old_lost_hash': '59d88ca','integration_step1_hash':'039a336fec','followup_report':'105 pasul 1 apt de integrare; pasul 2 blocat de pierderea codului B.'},{'mutant_wrong_alias_and_positive_second_step':bad22,'expected_two_rejections':True},'Decizia și separarea hashurilor/pasului 2 sunt demonstrabile documentar. Nu s-a auditat sistemul de fișiere al site-ului ori codul pierdut și nu s-a dovedit în acest test că reconstrucția a avut loc ulterior.',[xr(i)for i in ['require_T22.15','cap','T22Verdict']])
plog=B/'executie/R10_pregatire/A12/JVM/git_TestComparatieSaga.log';l=plog.read_text(encoding='utf8').splitlines();qline=next(i for i,s in enumerate(l,1)if re.search(r'FAIL.*NoSuchFileException',s))
add('T04.12','Cele patru nume concrete din L9 al planului inițial; planul v2 repartizează explicit TestConectoriCitire la eMAG și TestComparatieSaga la bancă. Caută în întreaga versiune fixată, apoi separă forma numelui de atingerea funcției.',{'exact_name_matches':found,'whole_tree_entries':len(allpaths),'implementation_behavior_from_filenames':None,'B_previous_JVM':'TestComparatieSaga din R10 are o încercare Windows cu eșec T-03 /proc/self/fd; nu este un defect al motorului demonstrat.','alternatives_not_proven_equivalent':ex['FullTree']['other_possible_classes']},{'removed_only_real_sourcepath_in_in_memory_tree':found['TestComparatieSaga'],'remaining_reference_class_matches':neg4,'expected_count':0},'3 nume exacte absente din arbore; există teste cu alte nume, însă echivalența semantică a celor patru domenii nu a fost demonstrată. Recuperarea etalonului L9 și numele v2 sunt rezultate documentare, nu o execuție calificată a celor patru suite.',[xr(i)for i in ['require_T04.12','T04v2','T04decision','FullTree','T04cmp']]+[fs(plog)|{'line':qline,'line_sha256':digest(l[qline-1].encode())}])
report=folder/'Rezultat.json';dump(report,{'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'commit':base,'scope':'3 subcriterii selectate nominal din 873; martori negativi pe intrări în memorie; nicio modificare repo/producție. Detectarea unei abateri în comparator nu certifică întreaga implementare.','count':len(rows),'rows':rows,'sources':[fs(P),fs(jvm)],'score':None})
for z in rows:
 for ref in z['references']:
  pp=B/ref['file'];assert digest(pp.read_bytes())==ref['sha256'];d=json.loads(pp.read_bytes())if 'pointer'in ref else None
  if 'pointer' in ref:
   for k in ref['pointer'][1:].split('/'):d=d[int(k)]if isinstance(d,list)else d[k]
   assert d is not None
  if 'line'in ref:assert digest(pp.read_text(encoding='utf8').splitlines()[ref['line']-1].encode())==ref['line_sha256']
print('SEALED',fs(report),'rows',[(z['criterion'],len(z['references']))for z in rows])
