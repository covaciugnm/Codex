from a12_r11x_java import *
import difflib,shutil
outp=A/'calibrari';outp.mkdir(exist_ok=True)
def cal(name,j,tag,typ,fx=None):
 src=C/'test'/(name+'.java'); original=src.read_text(encoding='utf8'); content=original
 if name=='TestComparatieSaga':
  content=content.replace('Path.of("/exp/idempiere/plugins/com.eva.ro.saga.native/src")','Path.of("../com.eva.ro.saga.native/src")')
  content=content.replace('.toString(), "/x/a.sqlite");','.toString(), Path.of("/x/a.sqlite").toString());')
  content=content.replace('.toString(), "/tmp/arhive/b.sqlite");','.toString(), Path.of("/tmp/arhive/b.sqlite").toString());')
  content=content.replace('"7", "/tmp/arhive"));','"7", Path.of("/tmp/arhive").toString()));')
 elif name=='TestT257Repostare':
  content=content.replace('x.toString().contains("/src/")',"x.toString().replace(java.io.File.separatorChar, '/').contains(\"/src/\")")
 temp=scratch/('cal_'+name+'_'+tag+'_'+typ);temp.mkdir(exist_ok=True); cs=temp/(name+'.java');cs.write_text(content,encoding='utf8');diff=''.join(difflib.unified_diff(original.splitlines(True),content.splitlines(True),'candidate','harness_portable')); diffp=outp/(name+'.diff')
 if not diffp.exists():diffp.write_text(diff,encoding='utf8')
 fq=re.search(r'^package ([\w.]+);',original,re.M);cls=(fq[1]+'.'if fq else'')+name; classpath=cp(temp,j);cc=cmd([java/'javac.exe','-J-Xmx220m','-proc:none','-encoding','UTF-8','-cp',classpath,'-sourcepath',C/'test','-d',temp,cs],C)
 args=[java/'java.exe','-Xmx210m','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.io.tmpdir='+str(scratch),'-Dline.separator=\n','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',classpath,cls]+([str(fx)]if fx else[]);rr=cmd(args,C)if cc.returncode==0 else None;txt=cc.stdout+(rr.stdout if rr else'');l=outp/(name+'_'+tag+'_'+typ+'.log');l.write_text(txt,encoding='utf8');mk=[{'line':i,'value':s.strip()}for i,s in enumerate(txt.splitlines(),1)if re.search(r'^\s*(OK|FAIL)\s',s)]
 return {'suite':name,'case':typ,'jar':tag,'jar_sha':sha(j),'source_sha':sha(src),'harness_sha':sha(cs),'fixture_changed':fx is not None,'harness_diff':ref(diffp),'compile':cc.returncode,'exit':rr.returncode if rr else None,'markers_ok':sum(x['value'].startswith('OK')for x in mk),'failures':[x for x in mk if x['value'].startswith('FAIL')],'check_totals':[s.strip()for s in txt.splitlines()if 'REZULTAT'in s],'markers':mk,'log':ref(l)}
fx=C/'test/fixtures/banca';mut=scratch/'bank_mutate';mut.mkdir(exist_ok=True)
seed=(fx/'comparatie_eva_2026.tsv').read_bytes();assert b'2026-01-02\t-216.90\t'in seed
(mut/'comparatie_eva_2026.tsv').write_bytes(seed.replace(b'2026-01-02\t-216.90\t',b'2026-01-02\t-96216.90\t',1));(mut/'comparatie_saga_2026.tsv').write_bytes((fx/'comparatie_saga_2026.tsv').read_bytes())
comb=[(n,j,t,'restored_paths',None)for n in ['TestComparatieSaga','TestT201Ecrane','TestT257Repostare']for t,j in [('candidate',jar),('mounted_copy',scratch/'cesiro-contab.jar')]]+ [('TestComparatieSaga',j,t,'one_amount_mutation',mut)for t,j in [('candidate',jar),('mounted_copy',scratch/'cesiro-contab.jar')]]
with ThreadPoolExecutor(max_workers=3)as ex: results=list(ex.map(lambda q:cal(*q),comb))
f=A/'Calibrari_banca_si_registre_02.json';save(f,{'utc':now(),'head':head,'initial':ref(A/'JVM_Banca_si_registre_01.json'),'extra_git_sources':ref(A/'Sources_complement_SAGA_et_T201.json'),'oracle':'Banca 109; T201 ecrane fix original completat; T257 gardă / referințe. Se păstrează toate predicatele; numai directoarele fixture-sursă, reprezentarea căii pe platformă și separatorul de arbore se adaptează în copii ale testelor. Nu modificăm ramura sau artefactele din produs. FD Linux nu se substituie cu o valoare constantă.','counter_input':{'one_fixture_value':'-216.90 → -96216.90, prima tranzacție a fișierului sintetic; comparatorul inițial și martorul folosesc exact același test/target','original_sha':sha_bytes(seed),'mutant_sha':sha(mut/'comparatie_eva_2026.tsv'),'saga_unchanged':sha(mut/'comparatie_saga_2026.tsv')},'runs':results});print(ref(f),[(r['suite'],r['jar'],r['case'],r['compile'],r['exit'],r['markers_ok'],len(r['failures']))for r in results],flush=True)

