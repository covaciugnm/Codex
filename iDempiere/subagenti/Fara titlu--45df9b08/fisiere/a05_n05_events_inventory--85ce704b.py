from pathlib import Path
import re,os,json,subprocess,hashlib
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_N05_lot03')
G='D:/CodexWork/eva-audit-p01-src-20261101';H='df85d33c1648ce2b2df130a60a05ef696e2e5480'
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
names=re.findall(r'new com\.eva\.ro\.contab\.component\.(\w+Events)\(', (O/'surse_df85/EvaActivator.java').read_text(encoding='utf8'))
out=[]
for n in names:
 p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/component/'+n+'.java'
 key=subprocess.check_output(['git','-C',G,'rev-parse',H+':'+p],env=env).decode().strip();b=subprocess.check_output(['git','-C',G,'cat-file','blob',key],env=env)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==key
 dst=O/'surse_df85/component'/ (n+'.java')
 if dst.exists():assert dst.read_bytes()==b
 else:dst.write_bytes(b)
 s=b.decode();lines=s.splitlines()
 relevant=[]
 for i,l in enumerate(lines):
  if 'initialize()'in l or 'registerTableEvent'in l or 'registerEvent'in l or 'Table_Name'in l or 'M_Product' in l or 'PP_Product' in l:
   relevant.append({'line':i+1,'text':' '.join(lines[max(0,i-1):i+3])})
 out.append({'class':n,'path':p,'oid':key,'sha256':hashlib.sha256(b).hexdigest(),'subscription_excerpt':relevant,'owner':'A05','peer':['A03','A11'],'role':'inventarul static al handlerelor globale pentru excluderi justificate; fara credit executie','requirement':'N05 / G03 validatori efectivi','normal_path':'EvaActivator.start → bindEventManager','positive':'observare domeniu de subscribere','counterexample':'handler pe tabela atinsa omis din bootstrap','persistent_effect':'niciunul; lectura Git','limit':'nu echivaleaza auditarea intregii clase'})
dest=O/'Inventar_subscriptii_EvaActivator_v1.json';assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for r in out:
 print(r['class'], *[x['text']for x in r['subscription_excerpt'] if 'registerTableEvent'in x['text'] or 'registerEvent'in x['text']],sep=' | ')
print('total',len(out),'sha256',hashlib.sha256(dest.read_bytes()).hexdigest())
