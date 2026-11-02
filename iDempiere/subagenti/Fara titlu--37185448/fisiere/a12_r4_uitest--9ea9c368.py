from a12_r3_survey import *
import subprocess as sp
pt='^|x';sc="""import subprocess as sp,json,re
c='/home/saga-server/Documents/EvA-Contab';s='6df998aee0e514d30856c461962afe99ebd0d113';pat='WSagaContracteForm|Tipuri de contracte|Contracte \\(3 taburi\\)|TestT259|C-60_R-TE_contracte'
q=sp.run(['git','grep','-l','-I','-E',pat,s,'--','*.java','*.py','*.js','*.ts','*.spec','*.test','*.sh'],cwd=c,stdout=sp.PIPE);files=q.stdout.decode(errors='replace').splitlines();filt=[];summary=[]
for name in files:
 n=name.split(':',1)[-1]
 if not (re.search(r'(?:test|qa|prob|dovezi|fixture|spec|smoke|playwright|selenium|browser|ui_test)',n,re.I) or n.endswith('.sh')):continue
 b=sp.check_output(['git','show',s+':'+n],cwd=cwd) if False else sp.check_output(['git','show',s+':'+n],cwd=c);ls=b.decode('utf8',errors='replace').splitlines()
 ui=bool(re.search(r'playwright|selenium|webdriver|page\\.goto|page\\.locator|page\\.get_by|browser\\.launch|from playwright|puppeteer|\\.device\\(', '\\n'.join(ls),re.I))
 refs=[[i,l[:270]]for i,l in enumerate(ls,1) if re.search(pat,l,re.I)][:5]; filt.append({'file':n,'oid':sp.check_output(['git','rev-parse',s+':'+n],cwd=c).decode().strip(),'browser_driver_literal':ui,'relevant_refs':refs})
 if ui:summary.append(n)
print(json.dumps({'grep_rc':q.returncode,'total_matched_paths':len(files),'matching_testlike':filt,'browser_driver_candidates':summary},ensure_ascii=False))
""";q=sp.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','python3 -'],input=sc.encode(),capture_output=True,check=True,timeout=75);j=json.loads(q.stdout);wr(E/'R4/T259_ZK/cautare_test_versionat.json',j);print(j['total_matched_paths'],len(j['matching_testlike']),len(j['browser_driver_candidates']),j['browser_driver_candidates'][:8])

