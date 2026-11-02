import hashlib,json,re,subprocess,os
from pathlib import Path
root=Path('D:/CodexWork/eva-audit-p01-readonly-20261102/idempiere/plugins/com.eva.ro.contab')
here=Path(__file__).resolve().parent
deps=Path('D:/CodexWork/eva-audit-secondary-20261102')
jdk=Path('C:/Program Files/Java/jdk-21/bin')
cp=';'.join([str(here/'classes'),str(deps/'com.eva.ro.contab_13.0.0.jar'),str(deps/'org.adempiere.base_13.0.0.202603090043.jar'),str(deps/'org.adempiere.base.process_13.0.0.202603090043.jar'),'D:/CodexWork/a05-support-jars/*'])
results=[]
for suite in 'TestT316CanalB2B TestT214VanzariPeCanal TestT22FisaCanal TestT211Garda TestT354Set TestT354Disponibil TestT35Canale'.split():
 f=root/'test'/f'{suite}.java';pkg=re.search(r'^package ([^;]+);',f.read_text(encoding='utf8'),re.M)
 c=subprocess.run([jdk/'javac.exe','-encoding','UTF-8','-cp',cp,'-d',here/'classes',f],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
 r=subprocess.run([jdk/'java.exe','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,(pkg[1]+'.' if pkg else '')+suite],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=32) if c.returncode==0 else None
 raw=c.stdout+(r.stdout if r else b'');log=(here/(suite+'.txt'));log.write_bytes(raw)
 text=raw.decode('utf8','replace');d={'test':suite,'source':str(f.relative_to(root)).replace('\\','/'),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'compile_exit':c.returncode,'run_exit':r.returncode if r else None,'ok':len(re.findall(r'^\s*OK\s',text,re.M)),'fail':len(re.findall(r'^\s*FAIL\s',text,re.M)),'diagnostics':[v.strip()[:500] for v in text.splitlines() if re.match(r'^\s*(?:FAIL|Exception in thread|Error:)',v) or 'error:' in v][:10],'sha256':hashlib.sha256(raw).hexdigest()}
 print(json.dumps(d,ensure_ascii=True));results.append(d)
(here/'suite.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')

