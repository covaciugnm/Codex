from a03_r4_exec import *
from lxml import etree, html
import io,zipfile,shutil,urllib.request
def d100():
 dir=work/'dukD100';source=P('D:/CodexWork/eva-a03-run-20261102/duk/duk_SAFT_an_luna/dist');shutil.copytree(source,dir,dirs_exist_ok=True);index='https://static.anaf.ro/static/10/Anaf/Declaratii_R/100.html';raw=urllib.request.urlopen(index,timeout=15).read();tr=next(r for r in html.fromstring(raw).xpath('//tr[td]') if '12/2021' in r.text_content());url=next(x.get('href') for x in tr.xpath('.//a[@href]') if '.zip' in x.get('href','')).replace('http://','https://');pkg=urllib.request.urlopen(url,timeout=18).read();z=zipfile.ZipFile(io.BytesIO(pkg))
 libs=[]
 for ent in z.infolist():
  nm=P(ent.filename).name
  if nm.lower().endswith('.jar') and ('D100' in nm):p=dir/'lib'/nm;p.write_bytes(z.read(ent));libs.append({'entry':ent.filename,'sha256':h(p)})
 results=[]
 for tag in ('git','installed'):
  for val in ('150','0','NEG'):
   f=probe/(tag+'_D100R4_2023-06_'+('150' if val=='NEG' else val)+'.log');t=f.read_text(encoding='utf8');fragment=t.split('D100_XML=',1)[1].split('</declaratie100>',1)[0]+'</declaratie100>';xml=etree.fromstring(fragment.encode());obs=dict(xml[0].attrib)
   if val=='NEG':xml[0].attrib['suma_plata']='999';fragment=etree.tostring(xml,encoding='unicode')
   mf=dir/('A03R4_'+tag+'_'+val+'.xml');mf.write_text(fragment,encoding='utf8');err=dir/(mf.stem+'.err.txt');p=P('D:/CodexWork/eva-a03-run-20261102/no-net-2.policy');policy=work/'DUK.policy'; policy.write_text(p.read_text().replace('D:/CodexWork/eva-a03-run-20261102/-',str(work).replace('\\','/')+'/-'),encoding='utf8')
   rr=sp.run([jdk/'java.exe','-Djava.security.manager','-Djava.security.policy=='+policy.as_uri(),'-Djava.awt.headless=true','-jar','DUKIntegrator.jar','-v','D100',mf,err,'$'],cwd=dir,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=25);message=err.read_text(encoding='utf8',errors='replace') if err.exists() else None
   newxml=probe/mf.name;newxml.write_bytes(mf.read_bytes());results.append({'target':tag,'case':val,'input_file':newxml.name,'input_hash':h(newxml),'generated_line':obs,'actual_validator_rc':rr.returncode,'DUK_result':message,'output_tail':(rr.stdout+rr.stderr)[-980:]})
 dump1('D100_officiel_R4.json',{'utc':now(),'case_date':'2023-06','real_company':False,'index':index,'index_sha256':hashlib.sha256(raw).hexdigest(),'selected_row':'Aplicabil din decembrie2021, inclusiv perioada de raportare iunie2023. Soft J din 17.01.2024.','official_jars_url':url,'zip_sha256':hashlib.sha256(pkg).hexdigest(),'jars':libs,'DUKIntegrator_sha256':h(dir/'DUKIntegrator.jar'),'results':results,'law':'https://legislatie.just.ro/Public/DetaliiDocumentAfis/277404','legal_context':'OUG115/2023, art.53 privind art.56 alin.(2^4),(2^5), separă tratamentul pentru 2023 de anii ulteriori. Sumele fixture-ului sunt un exemplu de contract software; nicio concluzie asupra eligibilității unui beneficiar real.','fixture_note':'Claselor efective GenD100 li s-au furnizat obligații sintetice, nu soldul unei firme reale; nu s-a depus/scris nimic la ANAF.'})
def static():
 spaths=[plug/'src/com/eva/ro/contab/documente/res/etichete.tsv',plug/'src/com/eva/ro/contab/form/reges/res/etichete.tsv'];rows=[]
 for f in spaths:
  data=f.read_text(encoding='utf-8-sig').splitlines(); vals=[];target=False;keys=[];fmt=[];missing=[];percent=[]
  for i,v in enumerate(data,1):
   if v.startswith('#'):target=bool(re.search(r'\bT159\b',v));continue
   if not v.strip():continue
   p=v.split('\t');keys.append(p[0]); 
   if len(p)!=3:fmt.append((i,len(p)));continue
   if not p[1].strip() or not p[2].strip():missing.append((i,p[0]))
   if target and re.findall(r'%(?:\d+\$)?s',p[1])!=re.findall(r'%(?:\d+\$)?s',p[2]):percent.append((i,p[0]))
  rows.append({'file':str(f.relative_to(root)).replace('\\','/'),'sha256':h(f),'keys':len(keys),'duplicates':[k for k,c in collections.Counter(keys).items() if c>1],'non3cols':fmt,'all_empty_translation_fields':missing,'T159_ro_en_placeholder_mismatch':percent,'period_of_file':'cutoff git, not automatically original integration checkpoint'})
 path=plug/'src/com/eva/ro/contab/fiscal/InchidereLuna.java';d0=path.read_text(encoding='utf8').splitlines();first=next(i for i,v in enumerate(d0) if 'public static String valideaza(Properties' in v);end=next(i for i in range(first+1,len(d0)) if d0[i]=='    }');matches=[{'line':n+1,'source':d0[n].strip()} for n in range(first,end+1) if re.search('potValida|posteaza|NotaInchidere.scrie|inregistreaza',d0[n])]
 tr= root/'tools/teste/ruleaza_teste_contab.sh';t=tr.read_text(encoding='utf8').splitlines();mark=[(n+1,v) for n,v in enumerate(t) if 'TestT256D394' in v];st=[(n+1,v) for n,v in enumerate(t) if (v.startswith('for t in ') or v.startswith('t=Test')) and n>mark[-1][0]]
 dump1('static_contracts_R4.json',{'utc':now(),'sha':sha,'labels':rows,'T58_gate_method':{'path':str(path.relative_to(root)).replace('\\','/'),'hash':h(path),'start':first+1,'end':end+1,'matches':matches,'first_contains_potValida':bool(matches and 'potValida' in matches[0]['source'])},'T256_runner':{'path':str(tr.relative_to(root)).replace('\\','/'),'sha256':h(tr),'matches':mark[:6],'later_test_blocks_count':len(st),'last_example':st[-1],'historical_guard':'Cerința „ultimul bloc” se citește separat la data predării și la SHA actual, unde au fost adăugate teste. Nu numim acest fapt regresie fiscală a produsului.'}})
def historical():
 pre='Documentatie/echipa-2026-10-09/T58-ghid-inchidere-pas-cu-pas/';fs=[pre+'12a_anexa_spec_r3.md',pre+'dovezi-2x-poarta2/clona/C-04_R-NEG.txt',pre+'dovezi-2x-poarta2/clona-r2/C-04_R-NEG.txt'];rows=[]
 for f in fs:
  r1=sp.run(['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab show '+sha+':'+f],capture_output=True,timeout=20);assert r1.returncode==0,r1.stderr; st=r1.stdout.decode('utf8',errors='replace');snippet=[v[:650] for v in st.splitlines() if re.search(r'^R-NEG|^HTTP|^stare:|^\$ SELECT|^0$',v)][:8]; rows.append({'file':f,'commit':sha,'sha256':hashlib.sha256(r1.stdout).hexdigest(),'captured_lines':snippet,'level':'HISTORICAL_REFERENCE: nu este reprobele curente A03.'})
 dump1('istoria_T58.json',{'utc':now(),'rows':rows})
if __name__=='__main__':
 {'d100':d100,'static':static,'history':historical}[sys.argv[1]]()
