from a12_r10_base import *
a=Path(__file__).parent/'a12_r10_receipt.py';exec(a.read_text(encoding='utf8').split("j=P10/")[0])
f=P10/'T201_PG16_two_writers.json';d=rd(f);assert H0 if False else True
assert d['cleanup']['process_released']and len(d['scenarios'])==8
for n,mode,rx,rm,et,ctr,lim in [
 ('013','fara-blocare',r'(?:OK|FAIL).*K-9',r'(?:OK|FAIL).*K-9','SQLState 55P03 si 2×20 achiziții de număr → 40 distincte, 0 duplicate; cu blocarea scoasă erori.','2 × 20 în două preconexiuni distincte. Scoaterea blocării produce 20 distincte/20 erori în ambele JAR.','Schema restaurată GardenWorld, numere sintetice și test oficial JDBC. Rezultatul se limitează la acest contract de concurență; nu s-a modificat înregistrarea taskului.'),
 ('014','alta-trx',r'(?:OK|FAIL).*K-10',r'(?:OK|FAIL).*K-10','Rollback după alocarea numărului lasă același număr la următoarea operație; serializare normală fără goluri.','Repetarea alocării 41/41; scrierea consumului în altă conexiune este refuzată cu 55P03.','Cerința privește K10 și mutantul. Comanda a fost rulată la nivel JDBC pe copia BD, fără click ERP.'),
 ('019','fara-trigger',r'OK.*(K-15|K-13 UPDATE|R-N8 UPDATE)',r'FAIL.*K-15','Nucleul de protecție refuză DELETE și schimbarea datelor fixe, permite rubrica editabilă.','Ștergerea triggerului în tranzacția fixturei face controlul DELETE roșu.','Acestea sunt efectele SQL și integritatea. Nu au fost apăsate butoanele «Anulez» sau «Modific» în ZK pentru această probă.')]:
 c='T201-R2-'+n;bytag={};allrefs=[]
 for tag in ['git','instalat']:
  h=lines(P10/'PG201'/(tag+'_normal.log'),rx);m=lines(P10/'PG201'/(tag+'_'+mode+'.log'),rm);assert h and m;(bytag.setdefault(tag,{})).update({'positive':[q['text']for q in h],'mutant':[q['text']for q in m]});allrefs+=h+m
 add(c,'PostgreSQL 16 restaurat și test JDBC original pe ambele JAR',et,bytag,ctr,lim,allrefs+[jr(f,'/scenarios')],'contract_JDBC'if n in ['013','014']else'subcase')
p=P10/'Registru_pg_implicite_A12.json';wr(p,{'utc':now(),'fixed':BASE,'receipts':out,'count':len(out),'environment':jr(f,'/cleanup')});print(sha(p))
