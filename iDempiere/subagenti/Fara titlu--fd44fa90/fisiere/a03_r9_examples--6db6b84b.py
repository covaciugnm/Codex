from a03_r9_trace import *
import ast,types
def compile_functions(b,names,globals_):
 tree=ast.parse(b.decode());selected=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names];assert len(selected)==len(names);mod=ast.Module(body=selected,type_ignores=[]);exec(compile(mod,'<functions from pinned Git>','exec'),globals_);return {z.name:(z.lineno,z.end_lineno) for z in selected}
def examples():
 rp='backend/app/routers/formulare.py'; rd='backend/app/idempiere/readdb.py';fs=[original((n,'')) for n in ['anaf/GenD100.java','fiscal/ObligatiiETva.java']];objs=batch([v+':'+p for v in (old,sha) for p in fs+[rp]]+[sha+':'+rd]);sets=[['o810 = new Obligatie(cod810, codBug, panaLa.plusMonths(1).atDay(25)','static final String COD_MICRO_IMPLICIT','return Integer.parseInt(v == null'],['o810 = new Obligatie(cod810, codBug, ziua25','static LocalDate ziua25','CalendarFiscal.termenDin("TERMEN_ZI_STANDARD"','return ParametriFiscali.valoare("D100_COD_MICRO"'],['NICIO_OBLIGATIE_DIN = LocalDate.of','FARA_SANCTIUNE_DIN = LocalDate.of','isBefore(NICIO_OBLIGATIE_DIN)'],['int cod = ParametriFiscali.valoare("ETVA_REGIM", data)','throw new IllegalArgumentException("ETVA_REGIM=']];examples=[]
 for n,p in enumerate(fs):
  for k,v in enumerate((old,sha)):
   bb=objs[v+':'+p];ls=bb[1].decode().splitlines();hits={a:[{'line':i+1,'source':l.strip()} for i,l in enumerate(ls) if a in l] for a in sets[2*n+k]};assert all(hits.values())
   examples.append({'ref':v,'path':p,'blob':bb[0],'matches':hits})
 calls=[];table={'2025-12-31':3.5,'2026-12-31':4.25}
 class MissingSyntheticKey(Exception):pass
 def value(name,date):
  calls.append([name,str(date)]);v=table.get(str(date))
  if name!='REDIRECTIONARE_IMPOZIT_PROCENT' or v is None:raise MissingSyntheticKey()
  return v
 gd={'_date':datetime.date,'_eroare':lambda *args:ValueError(args[0])};compile_functions(objs[sha+':'+rd][1],['data_din_text'],gd);new={'readdb':types.SimpleNamespace(data_din_text=gd['data_din_text'],parametru_legal=value)};g0={}; nlines=compile_functions(objs[sha+':'+rp][1],['procent_redirectionare','_d230_data'],new);olines=compile_functions(objs[old+':'+rp][1],['_d230_data'],g0); ex=[]
 for tag,rev,fn,yr,data,expected_fraction,maxtext in [('frozen_2026_default',old,g0,2026,{},3.5,'3,5%'),('registered_2025',sha,new,2025,{},3.5,'3,5%'),('registered_2026_synthetic_change',sha,new,2026,{},4.25,'4,25%'),('explicit_rate_preserved',sha,new,2026,{'procent':2},2,'4,25%'),('registry_missing',sha,new,2027,{},None,None)]:
  before=len(calls)
  try:z=fn['_d230_data'](yr,data); actual=z['redirectionare']['procent']; text_ok=maxtext in z['denumire'] and maxtext in z['nota'];status='ok';assert actual==expected_fraction and text_ok
  except MissingSyntheticKey:assert tag=='registry_missing';actual=None;text_ok=None;status='refuz_fixture_registru'
  ex.append({'id':tag,'ref':rev,'year':yr,'explicit_input_percent':data.get('procent'),'output_percent':actual,'expected_percent':expected_fraction,'expected_display_maximum':maxtext,'both_display_strings_match':text_ok,'registry_calls':calls[before:],'result':status})
 assert ex[0]['registry_calls']==[] and ex[2]['registry_calls']==[['REDIRECTIONARE_IMPOZIT_PROCENT','2026-12-31']]
 J(out/'T159_inlocuiri_si_D230.json',{'utc':UTC(),'sha':sha,'criterion':'T159-R2-050','code_comparisons':examples,'conclusions':['În GenD100, termenul nominal 25 din apelul obligației 810 a devenit ziua25(perioada) și apoi termenDin(TERMEN_ZI_STANDARD, finalul lunii). Pentru codul micro de rezervă 121, codul nou citește D100_COD_MICRO la sfârșitul perioadei. Sunt înlocuiri directe, legate de apeluri, nu simple potriviri de nume.','ObligatiiETva.obligatia stabilea regimul prin comparații cu date în cod. Acum citește ETVA_REGIM la data cerută. Echivalența juridică sau integralitatea seedurilor efective nu este evaluată.'], 'backend_D230':{'current_blob':objs[sha+':'+rp][0],'frozen_blob':objs[old+':'+rp][0],'date_parser_blob':objs[sha+':'+rd][0],'old_functions':olines,'current_functions':nlines,'trials':ex,'scope':'Corpuri reale AST din Git pentru _d230_data, procent_redirectionare și parserul de dată. Numai parametrul de registru este injectat; 4.25 pentru 2026 este o valoare fictivă de laborator. Rezultatul include câmpurile numerice și textele afișabile, dar nu tipărire, depunere, ecran ZK sau înregistrare contabilă. Un refuz injectat la lookup verifică propagarea absenței parametrului, nu comportamentul DB native.'}})
 print([(r['id'],r['output_percent']) for r in ex])
if __name__=='__main__':examples()

