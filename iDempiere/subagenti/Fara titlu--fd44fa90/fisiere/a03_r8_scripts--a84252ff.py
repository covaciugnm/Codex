from a03_r8_base import *
w=(work/'remote.txt').read_text(); commands={}
p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab';g='python3 -I '+path('T159','dovezi-10/generator_hardcodari.py');tr=path('T159','dovezi-10/triaj.tsv');d2=path('T186','dovezi-20-plan');iv=path('T186','20a_inventar.tsv');vv=f'python3 -I {d2}/verifica_inventar_t186.py {p} {iv} {d2}/20d_amprente_T0.tsv'
def R(k,v,t=180):commands[k]=[v,t]
for a in ['A','B','C','E']:
 for mode in ['ramase','chei-lipsa']:
  R('159-'+mode+'-'+a,f'{g} {mode} {sha} {tr} {a}')
R('159-readers',f'{g} cititori {sha}');R('159-reclass',f'{g} reclasificate <(git show b7e563428c:{tr}) {tr}');R('159-rules','python3 -I '+path('T159','dovezi-10/reguli_triaj.py')+' --verifica '+sha+' '+path('T159','dovezi-10/decizii_triaj.tsv')+' '+tr,220)
R('159-central',f'{g} inventar {sha} <({g} ramas <(git show b7e563428c:{tr}))'); R('159-doc','git ls-tree -r --name-only '+sha+' -- '+path('T159','dovezi-30-proba')+" | awk '/\\.txt$/{n++} END{print n+0}'")
s=doc(path('T159','12_spec.md'));cmd=re.search(r'C-27: `([^`]+)`',s)[1].replace('<v>',sha); R('159-writes',cmd)
for nm,sc in [('055','dovezi-52-auditor/test_clasa_LR-7.sh'),('059','dovezi-51-auditor/test_clasa_LR-1.sh'),('060','dovezi-13-poarta1/scanare_trx_poarta.sh'),('061','dovezi-52-auditor/test_clasa_LR-1b.sh'),('062','dovezi-13-poarta1/generator_inventare.py')]:
 R('58-'+nm,('python3 -I '+path('T58',sc)+' verifica ' if nm=='062' else 'bash '+path('T58',sc)+' ')+sha)
R('58-079',f"git show {sha}:{p}/fiscal/InchidereLuna.java|grep -c 'simularea și driverele rămân libere'")
R('156-core','bash '+path('T156','dovezi-02-plan/scripturi/t0_criterii.sh')+' '+sha)
R('186-006',f"""awk -F'\t' 'NR>1&&$11=="d"{{n++; if (length($13)<20||$13~/^tratarea auditată/||$13~/^eliberarea unei resurse după ce/||$13~/^JavaScript trimis clientului ZK/) bad++}} END{{print "clasa_d="n ", motive_neconforme="bad+0}}' {iv}""")
for ns in ['32_test_clasa_r1','36_test_clasa_r2']:R('186-'+ns,'python3 -I '+path('T186',ns+'.py')+' '+w+' --doar LR-3')
R('186-012',f"""git grep -c -E 'class AvertismentUnic|LOG_VAZUT|LOG_DEJA|JurnalUnic|primaOara' {sha} -- 'idempiere/plugins/*/src/**' """)
for lot in ['LA','LB','LB2','all']: R('186-KCLS-'+lot,vv+(' '+lot if lot!='all' else ''),260)
R('186-kinv',f'python3 -I {d2}/kinv_partial_contraproba_t186.py {p} {d2}/20s_metode_cflux.tsv',220)
R('186-merge',f'git merge-tree --write-tree {sha} {sha}; echo rc=$?')
R('256-kstatic','bash tools/teste/t256/k_static.sh '+w+' '+sha)
R('256-raw',f"""git show {sha}:{p}/anaf/GenD394.java | grep -cF "substring(COALESCE(i.description,'') from 'nr=([^·]+)')" """)
R('256-015',f"""git diff 1ba1029296 {sha} -- {p}/fiscal/D394Reguli.java | grep -cE '^[-+].*(poreference|documentno|nr=)'; git diff --stat 1ba1029296 {sha} -- idempiere/plugins/com.eva.ro.contab/test/fixtures/t180/""")
R('256-018',f"""python3 -c 'import re, pathlib; rows=[r.split("|") for r in pathlib.Path("{path('T256','02_plan.md')}").read_text().splitlines() if re.match(r"^\| M[0-9A-Za-z-]+ \|",r)]; print(len(rows),sum(bool(re.search(r":[0-9]+",r[3]) and re.search(r":[0-9]+",r[4])) for r in rows))'""")
R('256-024',f"""git ls-tree {sha}:{path('T256','dovezi-05/auto-verificare')} | wc -l""")
R('254-afara','python3 -I '+path('T254','dovezi-02-plan/inventar_fara_catch.py')+' '+sha+' | tail -3')
R('11-style',f"""grep -c 'setStyle(' {p}/form/WEvaRegesAplicatieForm.java {p}/form/reges/*.java""")
def run(it):
 k,(script,tm)=it
 try:
  rr=ssh('cd '+w+' && bash -s',('export LC_ALL=C.UTF-8\n'+script+'\n').encode(),timeout=tm)
  b=rr.stdout+rr.stderr; text=b.decode('utf8',errors='replace').splitlines()
  full=out/'log'/f'{k}.txt';full.parent.mkdir(exist_ok=True);full.write_bytes(b)
  obj={'id':k,'utc':UTC(),'sha':sha,'command':script,'rc':rr.returncode,'raw':str(full.relative_to(out)),'sha256':H(b),'tail':text[-3:],'line_count':len(text)}
 except sp.TimeoutExpired as x:obj={'id':k,'utc':UTC(),'command':script,'error':'timeout','seconds':tm}
 print(k,str(obj.get('rc','-')),str(obj.get('tail',[]))[:310],flush=True);return obj
if __name__=='__main__':
 ll=[]
 with ft.ThreadPoolExecutor(max_workers=3) as pool:
  for a in pool.map(run,commands.items()):ll.append(a);J(out/'Scripturi_fixate.json',{'sha':sha,'results':ll,'role':'Scripturi executate în export temporar izolat, cu jurnal și argumente; artefactele istorice care le motivează nu extind verdictul la data predării.'}) 

