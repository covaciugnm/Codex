from a12_r8_arch_survs import *
from collections import defaultdict,Counter
from hashlib import sha256
import base64,importlib.util,unittest.mock
repo=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');cases=defaultdict(list);rg8=rd(P/'JVM/Executii.json')
if Path('D:/CodexWork/a12-r8-morearchive/index.json').exists():a+=rd(Path('D:/CodexWork/a12-r8-morearchive/index.json'))
def ev(cid,kind,phase,method,oracle,observed,refs,limit,aggregate='subcase'):
 assert refs and observed;cases[cid].append({'kind':kind,'phase':phase,'method':method,'oracle':oracle,'observed':observed,'references':refs,'limit':limit,'coverage':aggregate})
def hist(cid,fragment,pattern,oracle,limit,maxlines=16,min1=True):
 rr=next((z for z in a if fragment in z['file'] and (cid.split('-')[0].split('.')[0]+'-') in z['file']),None)
 if rr is None:return False
 data=txt(rr);ls=data.splitlines();seen=[{'line':i,'text':l.strip()[:680],'line_sha256':sha256(l.encode()).hexdigest()}for i,l in enumerate(ls,1)if re.search(pattern,l,re.I)]
 if not seen:return False
 # historical lines are already publicly sanitized logs; output only primitive markers, no raw secret/header.
 seen=seen[:maxlines];ref={'git_commit_tree':BASE,'git_blob':rr['oid'],'repository_file':rr['file'],'data_sha256':sha256(data.encode()).hexdigest(),'matching_lines':seen}
 ev(cid,'ISTORIC_COMPARAT_CU_ARTEFACT_BRUT','historical','Recalcul SHA-1 de blob Git și citire liniară pe afirmația nominală.',oracle,[v['text']for v in seen],[ref],limit);return True
def lineproof(p,regex,maxlines=6):
 ls=p.read_text(encoding='utf8',errors='replace').splitlines();hit=[{'line':i,'text':v[:500],'sha_line':sha256(v.encode()).hexdigest()}for i,v in enumerate(ls,1)if re.search(regex,v,re.I)];return source(p)|{'lines':hit[:maxlines]}
def meas(cid,path,pat,oracle,limit,kind='STATIC_SAU_LABORATOR_EXECUTAT',k=8):
 ref=lineproof(path,pat,k);assert ref['lines'],(cid,path,pat)
 ev(cid,kind,'current','Comandă independentă pe artefact/suită fixată.',oracle,[z['text']for z in ref['lines']],[ref],limit)
def comp(cid,suite,pat,oracle,limit,per=7):
 for n in rg8:
  if n['suite']!=suite:continue
  p=B/n['log']['file'];ls=p.read_text(encoding='utf8',errors='replace').splitlines();cand=[]
  for i,l in enumerate(ls):
   if re.search(r'^\s*(OK|FAIL)\s+',l,re.I)and re.search(pat,l,re.I):
    anchor=ls[i+1]if i+1<len(ls)and ls[i+1].startswith('ANCHOR:')else''
    src=repo/n['file'];ss=src.read_text(encoding='utf8').splitlines()
    frames=re.findall(re.escape(suite)+r'\.java:(\d+):([^|]+)',anchor)
    f=[{'line':int(num),'method':m,'code':ss[int(num)-1].strip()[:500]}for num,m in frames if 1<=int(num)<=len(ss)]
    cand.append({'line':i+1,'text':l.strip(),'caller':f,'hash_line':sha256(l.encode()).hexdigest()})
  if not cand:continue
  cand=cand[:per];ev(cid,'ASERȚIUNI_COMPONENTĂ_EXECUTATE','current','JVM cu trasă la sursa reală; execuție '+n['target']+'.',oracle,[v['text']for v in cand],[{'suite':suite,'jar_variant':n['target'],'jar_sha':n['jar_sha'],'log':n['log'],'test_source':n['file'],'test_source_sha':n['source_sha'],'assertions':cand,'entire_suite_exit':n['exit']}],limit)
def sql(cid,su,pat,oracle,lim):
 for i,x in enumerate(rd(P/'SQL/Executii_SQL_r8.json')['suites']):
  if x['suite']!=su:continue
  z=[v for v in x.get('markers',[])if re.search(pat,v['output'],re.I)]
  if z:ev(cid,'PREDICAT_SQL_FIZIC_EXECUTAT','current','PostgreSQL izolat pe SQL-ul generat de implementarea '+x['target'],oracle,[v['output']for v in z],[source(P/'SQL/Executii_SQL_r8.json')|{'pointer':'/suites/'+str(i),'log':x['log'],'matching_rows':z}],lim)
def dics(cid,n,oracle,lim):
 f=P/'Dictionar_CESIRO_readonly.json';v=next((i,z)for i,z in enumerate(rd(f)['queries'])if z['name']==n);assert v[1]['exit']==0
 ev(cid,'DICȚIONAR_CESIRO_CITIT','current','SQL în tranzacție read only cu rollback',oracle,v[1]['lines']or['0 rânduri returnate'],[source(f)|{'pointer':'/queries/'+str(v[0])}],lim)
def jref(cid,p,ptr,exp,obs,lim,kind='OBSERVAȚIE_EXISTENTĂ_RECONTROLATĂ',phase='context'):
 x=rd(p)
 if ptr!='':
  for t in ptr.lstrip('/').split('/'):x=x[int(t)]if isinstance(x,list)else x[t]
 ev(cid,kind,phase,'Recitire pe cheie și SHA aferente.',exp,obs,[source(p)|{'pointer':ptr}],lim)
def lines_hist():
 loc='dovezi-40-audit/proba_finala/'
 where=['01_C-02_dictionar','14_bara','15_verdicte','16_jurnal','18_a_doua_rulare','19_doar_verifica','22_a_inainte','22_b_ecran','22_c_jurnale','25_concurenta']
 for k,c,pat,o in zip(where,[1,14,15,16,18,19,22,22,22,25],[r'^1\|40\|1\|5\|1|create unique index',r'10 conturi|13',r'^(?:IDENTIC|DE_LAMURIT|EVA_|512|542|B.7 \(5\))',r'^1\|1\|10\|60|result:',r'B.7|instan|168 rânduri',r'0 rânduri|nu s-a scris|168\|1',r'dezactivat:|rânduri:|B.7',r'^Luni:|^verdict:|^Linii:|^Export CSV:|^dublu-clic:',r'Jurnal de bancă|Taburile|dezactivat',r'^pornite:|sesiunea|^B.7|^(100578|rulările)'],['1/40/1/5/1 și index unic.','10 conturi, 6 luni, 168 înregistrări și 22 diferențe','146/5/1/16 și distribuție pe cont+luna.','1/1/10/60 și result 1','168 poziții, două instanțe și un singur id pe rând.','verificare fără scriere, total 168.','Jurnal dezactivat la deschidere.','13 luni/grupe, 168 linii, antet+168 CSV, text dublu clic.','Deschide Jurnal de bancă și tab nou.','Două sesiuni suprapuse, 168 și o singură rulare per cont/lună.']):
  hist('T06-R2-'+f'{c:03}',loc+'C-'+k+'.txt',pat,o,'Urma din verificarea istorică q31 se păstrează separat de rezultatele native ulterioare din alt cabinet.',36)
 hist('T06-R2-014',loc+'C-14_C-17_inainte.txt',r'^export_(linii|plati)\.sql','Cele două amprente acceptate la §A-8','Proveniența fixturei din această probă este q31, nu GardenWorld.')
 for c,n,pattern in [(3,'09-plan/11_test_bloc_t171',r'blocuri T171|rc=|corect|acolad'),(12,'40-audit/04_suita_varf_imbinat',r'TestComparatieSaga|109 OK|8 OK|rulator|saga[.]native')]:
  hist('T06-R2-'+f'{c:03}',n,pattern,'Garda proiectului și contraproba, respectiv două suite cu 109/8 la vârful istoric.','Jurnal primit din dosarul original. Nu reprezintă execuția independentă R8.')
 blocks={7:4,8:5,10:7,11:8,15:12,17:14,20:17,21:18,22:19,23:20,24:21,25:22,26:23,27:24}
 for cid,k in blocks.items():
  sk='13-cod'if k in [7,8,12,19]else'08-cod';f=f'dovezi-{sk}/auto-verificare/C-{k:02}'+('_final'if k==23 else '')+'.txt';rr=next((z for z in rows if z['criterion']=='T204-R2-'+f'{cid:03}'),None)
  if rr:hist(rr['criterion'],f,r'^(?:[0-9]+$|[ ]*[0-9]+ (EXC|P[0-9])|rc=|R:|R doc:|# motiv implicit|WSaga[BIJ].*(copii|ok)|.+exit=0|.+FAIL|.+ ⇒ |.*(rămase|premisă|premise|14 / 14|în UI|chei brute|capturi:|rânduri cu |rânduri N0|rândul |țintă|XLSX|stderr|nu se aplică))',rr['original_inputs_and_accepted_oracle'].get('expected')or rr['source_row']['text'],'Se separă lotul A1/A3 de HEAD; cifrele se citesc chiar dacă sunt sub ținta din plan.',16)
 # Independent recomputation, not a recognition of archived persons or business transactions.
 rr=next(z for z in a if 'T204-'in z['file']and z['file'].endswith('proba/ecrane/PB01.tsv'));tab=[l.split('\t')for l in txt(rr).splitlines()];act=tab[1:];assert len(act)==26;res=Counter(r[3]for r in act);excel=Counter(r[-1]for r in act)
 ev('T204-R2-025','RECALCUL_SURSĂ_LIVRARE','historical','Citire și numărare independentă a tuturor rândurilor TSV, coloanele 4 și 6.','26 PNG cu marcaj ok; XLSX pentru 25 și «nu se aplică» la import extras.',{'rows':len(act),'visual':res,'xlsx':excel,'exceptions':[(r[0],r[-1])for r in act if r[-1]!='ok']},[{'git_commit_tree':BASE,'git_blob':rr['oid'],'repository_file':rr['file'],'rows':'2–27'}],'Confirmă numărătoarea documentată; marcajul operatorului păstrat în sursă nu este inspecție vizuală independentă a fiecărui PNG.')
 for cid,k in [(11,7),(19,15),(24,20),(26,22),(28,24),(29,25),(33,29)]:
  sx='T201-R2-'+f'{cid:03}';r0=next(x for x in rows if x['criterion']==sx)
  choices=[z for z in a if '/T201-' in z['file'] and re.search(r'(?:^|[^\d])K[-_]?0?'+str(k)+r'(?=\D|$)',z['file'].split('/')[-1],re.I)and not re.search(r'\.sh|\.py',z['file'])]
  for z in choices[:3]:hist(sx,z['file'],r'rc=|(?:\b0\b|↔|egal|surs|refuz|TOTAL|FAIL|Rezultat|SQL|UCIS|actual|absent|roșu|^[0-9]|✓)',r0['original_inputs_and_accepted_oracle'].get('expected')or 'Criteriul nominal autorului','Citire istorică a rezultatelor front-end, DB sau gărzii indicate; diferențele istorice/retestarea HEAD se separă.',8)
 for cid,k in [(4,1),(10,7),(11,8),(12,9),(15,12)]:
  r0=next(z for z in rows if z['criterion']=='T220-R2-'+f'{cid:03}');h='dovezi-04/auto-verificare/K-'+f'{k:02}'+'.txt';hist(r0['criterion'],h,r'rc=|verdict|16|0|registru|OK |NERULAT|refuz|CONDI',r0['original_inputs_and_accepted_oracle'].get('expected')or r0['source_row']['text'],'Recalcul pe documentul istoric; separă istoricul bazei nemodificate de reexecuție.',10)
 hist('T220-R2-004','dovezi-02/defect_reprodus.txt',r'DEFECT REPRODUS:|1006416/1006417|16/16','Înainte: 16 legături T22, după: 16 resetate; facturile rămân CO.','Această probă demonstrează efectul în buildul vechi cd9ebfc994, nu bug actual.',5)
 hist('T220-R2-015','dovezi-12-k12/k12_cabinete.txt',r'^# Stare.*NERULAT','Detector executat în cabinetele indicate.','Fișierul istoric spune NERULAT pentru cabinetele reale. Reproducerea pe clonă este altă observație.')
 for cid,k in [(10,9),(12,11),(16,14),(20,18),(21,19),(22,20),(23,21),(25,23),(26,24),(27,25),(28,26),(29,27)]:
  sk='T314-R2-'+f'{cid:03}';r0=next(z for z in rows if z['criterion']==sk);h='dovezi-10a-lotA/auto-verificare/K-'+f'{k:02}';hist(sk,h,r'^[0-9]|^K-|SQL|[0-9] fiș|rc=|compar|ad_user|ad_role|## |zero|REFUZ|^[✓]|JAR|tipuri|inactiv',r0['original_inputs_and_accepted_oracle'].get('expected')or r0['source_row']['text'],'Rezultatul din dosar aparține lotului și cabinetului numit; nu este certificarea versiunii instalate.',8)
if __name__=='__main__':lines_hist();print(len(cases),sum(map(len,cases.values())))

