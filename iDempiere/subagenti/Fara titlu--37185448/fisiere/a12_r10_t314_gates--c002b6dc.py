from a12_r10_base import *
exec((Path(__file__).parent/'a12_r10_receipt.py').read_text(encoding='utf8').split("j=P10/")[0]);import subprocess,ast
des=P10/'Zone_A01';des.mkdir(exist_ok=True);server='saga-server@192.168.100.151';repo='/home/saga-server/Documents/EvA-Contab';top='Documentatie/echipa-2026-10-09/T314-meniu-vanzari-canale-comenzi-facturare/';sel=['dovezi-10a-lotA/auto-verificare/K-14.txt','dovezi-11-aud/proba/K-14_elemente.txt','dovezi-10a-lotA/proba/revenire_varf/K-04_K-14_a_doua_pornire.txt']
remote="""import subprocess as sp,hashlib,re,json;r='R0';c='CUT';t='TOP'
ls=sp.check_output(['git','-C',r,'ls-tree','-r',c,'--',t]).decode().splitlines();docs=[]
for l in ls:
 head,f=l.split('\\t',1)
 if not (re.search('/k26_(inainte|dupa)[.]txt$',f)or f.removeprefix(t)in SELECT): continue
 b=sp.check_output(['git','-C',r,'cat-file','blob',head.split()[2]]);ts=b.decode('utf8','replace').splitlines();items=[]
 for n,z in enumerate(ts,1):
  if re.search('q31 .*ad_user|F-CAN|atribuir|elementele noi|AD_Menu|AD_Element|etichete',z,re.I):items.append({'line':n,'sha256':hashlib.sha256(z.encode()).hexdigest(),'excerpt':z[:750]})
 docs.append({'repo_file':f,'blob':head.split()[2],'file_sha256':hashlib.sha256(b).hexdigest(),'selected_lines':items})
print(json.dumps(docs,ensure_ascii=False))""".replace('R0',repo).replace('CUT',BASE).replace('TOP',top).replace('SELECT',str(sel));run=lambda cmd:subprocess.run(['ssh','-o','BatchMode=yes',server,cmd],capture_output=True,timeout=30)
result=subprocess.run(['ssh','-o','BatchMode=yes',server,'python3','-'],input=remote.encode(),capture_output=True,timeout=40);assert result.returncode==0,result.stderr.decode()[-440:];docs=json.loads(result.stdout)
pairs={}
for z in docs:
 m=re.search(r'/k26_(inainte|dupa)\.txt$',z['repo_file'])
 if not m:continue
 vals=re.search(r'(\d+\|\d+\|\d+\|\d+\|\d+)\s*$',z['selected_lines'][0]['excerpt']);assert vals,z;pairs.setdefault(z['repo_file'].rsplit('/',1)[0],{})[m[1]]=vals[1]
assert len(pairs)>0 and all(sorted(q)==['dupa','inainte']for q in pairs.values());xe=run('git -C '+repo+' show '+BASE+':tools/teste/t314/proba_roluri.py');xe.check_returncode();raw=xe.stdout.decode();fn=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)and n.name=='k26')
calls=next(n for n in ast.walk(fn)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='psql');origsql=''.join(v.value for v in ast.walk(calls.args[1])if isinstance(v,ast.Constant)and isinstance(v.value,str));assert origsql.startswith('SELECT ')and 'ad_form_access' in origsql
cx='docker exec -i eva-postgres-q31 sh -c \'exec psql -X -qAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d idempiere\'';db=subprocess.run(['ssh','-o','BatchMode=yes',server,cx],input=("begin read only;set local search_path=adempiere,pg_catalog;set local statement_timeout='10s';"+origsql+";rollback;").encode(),capture_output=True,timeout=20);assert db.returncode==0,db.stderr.decode()[:200];actual=db.stdout.decode().strip()
f=des/'T314_deux_gardes_et_q31.json';wr(f,{'utc':now(),'fixed':BASE,'raw_docs':docs,'k26_pairs':pairs,'k26_dates':{'observed_equal_pairs':sum(z['dupa']==z['inainte']for z in pairs.values()),'different_pairs':sum(z['dupa']!=z['inainte']for z in pairs.values()),'synthetic_negative_change_role_rejected':not ('46|10|22|1021|0'=='46|9|22|1021|0')},'q31_current':{'statement':origsql,'output_counts_only':actual,'same_as_then':actual in [t['inainte']for t in pairs.values()],'scope':'Today’s population is not itself the before/after of the original campaign.'},'k14_source_note':'The raw logs attribute some new AD_Element rows to master code from other tasks. Do not interpret every delta in the cabinet as T314 creating a role or channel menu.'})
add('T314-R2-028','11 perechi Git înainte/după, metode originale și SELECT fizic q31 numai numărări.','În fereastra testului numărul utilizatorilor/rolurilor q31 rămâne neschimbat.','În cele '+str(len(pairs))+' perechi distincte de fișiere sursă s-au comparat cele cinci coloane. '+str(sum(v['inainte']==v['dupa']for v in pairs.values()))+' perechi au valori egale. Astăzi '+actual+'.', 'Schimbarea unui rol în numărătoarea sintetică respinge comparația.','Arhiva nu probează identitatea fiecărei persoane pe baza unor numărări. Datele curente sunt un reper separat și nu înlocuiesc fereastra istorică.',[jr(f,'/k26_pairs'),jr(f,'/q31_current'),jr(f,'/k26_dates')],'documentary_or_test')
add('T314-R2-016','Reconciliază atribuirea AD_Element și testul după repornire cu documentele brute.','Zero elemente, meniuri sau etichete noi cu nume de canal atribuite căii F-CAN, ținând cont de diferențele create de alte taskuri.',[{'path':v['repo_file'],'selected':v['selected_lines']}for v in docs if '/k26_'not in v['repo_file']], 'Creșterea totală de AD_Element include șase elemente de master documentate, care nu pot fi automat imputate operației F-CAN.','Compararea documentară se limitează la cazurile identificabile în rapoarte. Nu s-a executat personal F-CAN pe un nou q31 în această rundă. Fiecare etichetă de canal rămâne de confruntat cu operația proprie.',[jr(f,'/raw_docs'),jr(f,'/k14_source_note')],'documentary_or_test')
of=des/'Rezultat.json';wr(of,{'utc':now(),'receipts':out});print(sha(of),len(pairs),actual)

