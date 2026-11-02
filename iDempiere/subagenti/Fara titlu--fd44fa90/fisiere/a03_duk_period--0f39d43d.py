from a03_exec_runner import *
import shutil
root=tmp/'duk'; jar=next(j for j in root.rglob('*.jar') if 'DUKIntegrator_AnLunaUI' in j.name)
fx=plug/'test/fixtures/t16/D406_sintetic.xml';xml=etree.parse(str(fx));start=xml.xpath('//*[local-name()="SelectionStartDate"]/text()')[0]; yy,mm,_=map(int,start.split('-'))
cases=[]
for n in ['positive','negative']:
 doc=etree.parse(str(fx));p=root/('A03_'+n+'_D406.xml')
 if n=='positive':shutil.copyfile(fx,p)
 else:
  node=doc.xpath('//*[local-name()="Header"]')[0];node.getparent().remove(node);doc.write(str(p),encoding='UTF-8',xml_declaration=True)
 args=[java/'java.exe','-Djava.security.manager','-Djava.security.policy=='+(tmp/'no-net-2.policy').as_uri(),'-Djava.awt.headless=true','-jar',jar.name,'-v','D406',p,'$','$',f'an={yy}',f'luna={mm}']
 r=cmd(args,cwd=jar.parent,timeout=30);txt=r.stdout+r.stderr;lg=o/(n+'_D406_DUK.txt');lg.write_text(txt,encoding='utf8');errfile=P.Path(str(p)+'.err.txt');errtxt=errfile.read_text(encoding='utf-8',errors='replace') if errfile.exists() else None
 cases.append(dict(case=n,source_fixture_sha256=dig(fx),test_fixture_sha256=dig(p),period_start=start,argv=[str(z) for z in args],rc=r.returncode,marker_no_error='Validare fara erori' in txt,error_file_present=errfile.exists(),error_file_contents=(errtxt or '')[:650],log=lg.name,log_sha256=dig(lg),duk_jar_sha256=dig(jar),input_change='nicio schimbare' if n=='positive' else 'Header obligatoriu eliminat dintr-o copie sintetică',timestamp=now()))
dump('D406_duk_matched_period.json',{'official_kit':read('d406_duk_fullkit.json')['source'],'official_kit_sha256':read('d406_duk_fullkit.json')['zip_sha256'],'date':'Republicare ANAF 19.02.2026','cases':cases,'prior_attempt_note':'Primul test DUK a folosit exemplul an2025/luna8. Fişierul declară februarie2026. Aceste două probe repetă validarea cu perioada efectivă din Header.','limit':'Confirmă acceptarea/respigerea acestor fișiere sintetice de către validatorul oficial local. Nu confirmă depunerea, generarea din documente ERP sau completitudinea sumelor.'})
