from pathlib import Path
import tempfile,datetime,json,re,subprocess,hashlib,xml.etree.ElementTree as ET
O=Path(__file__).parent;E=O.parent;D=Path('D:/CodexWork/a03-r4-runtime/dukD100');V=json.loads((E/'R4_zone/A03/dovezi/D100_officiel_R4.json').read_bytes());T=Path(tempfile.mkdtemp(prefix='a11-d100-',dir='D:/CodexWork'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert h(D/'DUKIntegrator.jar')==V['DUKIntegrator_sha256']
for z in V['jars']:assert any(h(p)==z['sha256']for p in D.rglob(z['entry']))
policy=T/'offline.policy';policy.write_text((D.parent/'DUK.policy').read_text().replace('D:/CodexWork/a03-r4-runtime/-',T.as_posix()+'/-'));java=Path('C:/Program Files/Java/jdk-21/bin/java.exe');repo=[]
for b in ['git','installed']:
 for case in ['0','150','NEG']:
  x=D/f'A03R4_{b}_{case}.xml';inp=T/(b+case+'.xml');content=x.read_bytes();inp.write_bytes(content);desc=next(t.attrib for t in ET.fromstring(content).iter() if 'cod_oblig'in t.attrib);err=T/(b+case+'.txt')
  p=subprocess.run([str(java),'-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.awt.headless=true','-jar','DUKIntegrator.jar','-v','D100',str(inp),str(err),'$'],cwd=D,capture_output=True,encoding='utf8',errors='replace',timeout=30);msg=err.read_text(encoding='utf8',errors='replace') if err.is_file()else '';match=re.search(r'R17-20.6',msg);assert bool(match)==(case=='NEG'),(b,case,msg,p.stdout[-400:]);assert 'fara erori' in p.stdout.lower()or case=='NEG' or 'fara erori' in p.stderr.lower(),p.stdout+str(p.stderr)
  repo.append({'build':b,'case':case,'hash':h(inp),'declared':desc['suma_dat'],'paid':desc['suma_plata'],'spons':desc.get('suma_spons'),'process_rc':p.returncode,'error_file_hash':h(err)if err.is_file()else None,'negative_rule_R17_20_6':bool(match),'acceptance':'XML accepted'if case!='NEG'else 'controlled xml rejected'})
(O/'DUK_reproductions.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'validator':V['jars'],'period':'2023-06','network':'Java SecurityManager with no SocketPermission; fixture only, no transmission','outputs':repo},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print([(z['case'],z['paid'],z['negative_rule_R17_20_6'])for z in repo])

