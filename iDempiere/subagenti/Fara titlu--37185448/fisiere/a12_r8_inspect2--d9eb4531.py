from a12_r8_cases import *
for task,ends in [('T224-',['trei_rulari/rulare_3/G-00/rezultat.txt','trei_rulari/rulare_3/G-01/rezultat.txt','trei_rulari/rulare_3/cabinet/smoke.txt','trei_rulari/rulare_3/cabinet/retea_inspect.txt','/dovezi-29/08_garzi_comit.txt']),('T216-',['PB-95_tipar_factura_site.txt','PB-93_auto_confirma_trimis.txt']),('T310-',['/montare_cesiro.txt','fum_post/q31_fum_r49.json']),('T214-',['/dovezi-16/02_proba/par_total.txt']),('T06-',['/C-01_C-02_dictionar.txt']),('T201-',['/K-24.txt']),('T204-',['/C-24.txt'])]:
 for end in ends:
  r=next((x for x in a if '/'+task in x['file']and x['file'].endswith(end)),None)
  if r:print(r['file'].split('/',3)[-1],txt(r)[:1300])
for su in ['TestT204Ecrane','TestT29Acoperire','TestT28Meniu','TestT201Ecrane','TestT22Preluare','TestT22Stripe','TestT22Trimitere','TestT22FisaCanal']:
 print('SUITE',su)
 f=P/'JVM'/('git_'+su+'.log');ls=f.read_text(encoding='utf8').splitlines();print('\n'.join(l for l in ls if not l.startswith('ANCHOR')and re.search(r'K-15|[0-9]+ site|C0-15|T28-44|^.*garda|confirm|resping|Contul.*valid|eMAG|Preia|SKU|[0-9]+ câmpuri',l,re.I))[:600])

