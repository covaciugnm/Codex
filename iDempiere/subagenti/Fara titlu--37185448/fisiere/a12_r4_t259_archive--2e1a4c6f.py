from a12_r3_survey import *
import subprocess as sp
o=E/'R4/T259_ZK';s="""import json,subprocess as sp,re,hashlib
root='/home/saga-server/Documents/EvA-Contab';base='Documentatie/echipa-2026-10-09/T259-contracte-tip-coloana/';sha='6df998aee0e514d30856c461962afe99ebd0d113';rootfiles=['dovezi-04-cod/scripturi/proba_t259.py','dovezi-05-audit-cod/05_C3_din_buton.txt','dovezi-05-audit-cod/c3/jurnal_proba_auditor.txt','dovezi-05-audit-cod/04_C2_clona.txt','dovezi-05-audit-cod/04b_C2_clona_randuri.txt'];out=[]
def git(*x):return sp.run(['git',*x],cwd=root,capture_output=True)
for name in rootfiles:
 path=base+name;z=git('show',sha+':'+path);b=z.stdout;lines=b.decode('utf8',errors='replace').splitlines();oid=git('rev-parse',sha+':'+path).stdout.decode().strip();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\\0'+b).hexdigest()==oid
 if name.endswith('.py'):
  hits=[[i,l[:320]]for i,l in enumerate(lines,1)if re.search('^def (tab_tipuri|randuri|creeaza_tip|dezactiveaza|n_sql)|^(\\([123]\\))',l)][:10]
 else:
  hits=[]
  for i,l in enumerate(lines,1):
   if not re.search('N\\+1|\\bOK\\b|\\bFAIL\\b|\\bPAS\\b|PASS|randuri[=: ]+\\d|rânduri[=: ]+\\d|[0-9]+real|RESULTAT|REZULTAT|eroare.=|N_A|C3-\\d|N SQL|N=',l,re.I) or len(l)>600 or re.search('password|bearer|token|CUI',l,re.I):continue
   if re.search(r'\\[\\[|\\[\\{|\\|.*\\|.*\\|',l)and not re.search('PASS|OK|FAIL|REZULTAT',l,re.I):continue
   ms=re.findall(r'\\b(?:N\\+1|N\\s*=\\s*\\d+|\\d+\\s+(?:OK|FAIL)|(?:PASS|FAIL|REZULTAT|OK|fără eroare|zero erori))\\b',l,re.I);hits.append([i,ms]); 
 out.append({'path':path,'git_oid':oid,'file_sha256':hashlib.sha256(b).hexdigest(),'line_count':len(lines),'selected_evidence':hits[:40]})
print(json.dumps(out,ensure_ascii=False))
""";pr=sp.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=s.encode(),capture_output=True,check=True,timeout=30);a=json.loads(pr.stdout);wr(o/'test_original_versionat.json',a);print([(x['path'].split('/')[-1],len(x['selected_evidence']))for x in a])

