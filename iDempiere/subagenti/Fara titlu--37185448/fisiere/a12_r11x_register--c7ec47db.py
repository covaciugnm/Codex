from a12_r11x_base import *
from pathlib import PurePosixPath
m=read(P/'Manifest_Dispatch_tehnic_integral.json');by=collections.Counter(r['owner']for r in rows)
wave={'A01':('1','A01','Frontend/proxy – contrôle construction et sessions/tenancy; A01 fournit les preuves.'),
      'A06':('1','A06','Import/canal G3 – origine JSON vers staging; A06 fournit les preuves.'),
      'A03':('1b','A12','Bancă/comparație SAGA T171 și martorul Fact_Acct/T257; titular A03 pentru domeniu și restul fișierelor.'),
      'A10':('1b','A12','T201 registru cu concurență pe PostgreSQL izolat și mecanismul de numere; A10 pentru suite, volum și infrastructura rămasă.'),
      'A02':('2','A02','Dicţionar AD și schema; verifică actor, client/organizație și scrierea/rollback prin intrarea implementată.'),
      'A04':('2','A04','Import/NIR, legături factură-recepție și cost; include diferența între totaluri și monedă.'),
      'A05':('2','A05','G1/G2, locatori, ASI, costuri și stornare. T329/T330 se urmăresc separat.'),
      'A07':('2','A07','Comanda validată, aviz, AWB, încasări/retururi; urmărește cheile prin documente.'),
      'A08':('3','A08','Storefront și specificul canalului, permisiuni pe canal, probe de agenți/vânzări.'),
      'A09':('3','A09','ZK/mobile, roluri, interacțiune reală și device vs emulator.')}
base_rows=[]
for r in rows:
 assert catalog[r['path']]['git_object']==r['git_object']
 base_rows.append({'id':r['id'],'path':r['path'],'git_oid':r['git_object'],'git_mode':r['mode'],'candidate':head,'owner':r['owner'],'peer':r['peer'],'class':r['class'],'profile':r['profile'],'priority':r['priority'],'delta':r['delta'],'task_relation':r['association_mode'],'task_hypotheses':r['task_candidates'],'control':r['control'],'peer_control':r['peer_control'],'pipeline_candidates':r['pipeline_candidates'],'wave':wave[r['owner']][0],'qualifying_executor':None,'axis':dict.fromkeys(axes,'UNVERIFIED'),'file_verdict':None,'evidence':[],'reason':'Înregistrare de lucru; proba se adaugă numai în lotul de rezultate semnat, pe ID și blob, după rulare/lectură.'})
rp=A/'Registru_6709_initial.jsonl.gz'
assert not rp.exists()
with rp.open('wb')as f:
 with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0)as g:
  for row in base_rows:g.write((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode())
check=lines(rp);assert len(check)==6709 and all(x['axis']==dict.fromkeys(axes,'UNVERIFIED')for x in check)
def status(o):
 return {'assigned_basis':m['teams'].get(o)if isinstance(m['teams'],dict)else o,'owner':o,'wave':wave[o][0],'named_responsibility':wave[o][1],'mandate':wave[o][2],'files':by[o],'execution_state':'Activitate anunțată; cere raport nominal pentru proba efectivă.'if o in ['A01','A06','A03','A10']else'În următorul val; responsabil de domeniu alocat, disponibilitate de execuție încă neconfirmată.'}
h=A/'Contract_handoff_valuri_A12.json'; save(h,{'utc':now(),'head':head,'gate':ref(gate),'plan':ref(plan),'source_template':ref(P/'A06_sablon_fisa_fisier.json'),'register':ref(rp),'population':len(check),'owners':[status(o)for o in sorted(by)],'allocation':{'coordinator':'Analiză sintactică Python/JS/JSON/XML/YAML; nu dublați aceste execuții în lotul A12.','source_binding':'solicitare regiștri CDC; când există rezultat real, scrieți separat părinți/probe și ID/date git direct, nu doar numele fișierului.','A12':'Măsurări proprii pentru bancă, numerotare/DB și Java. Pentru rest, A12 verifică dovezile executorului și agregă.'},'per_file_event':['ID/cale/blob la head și ediția registrului','owner/peer și executor real','axa observată + scop/ancoră/intrare folosită, explicit independente de celelalte axe','actor, condiție, așteptare și valori efective, contraexemplu, retry, efect DB și curățare unde se aplică','proba externă cu hash și locator, limite și următoarea acțiune','reviewer independent, decizie și SHA separat'],'merge':'append-only by immutable batch; key = (candidate, file-id, event-id). Summaries count distinct file and axis, never commands. Empty axes do not become inspected, blocked or exercised by default. Installing a bundle is separate from executing a contained method.','qa':'În populația și literele ID toate 6.709 corespund bloburilor catalogului original. La deschidere 0 fișiere revendicate ca exercitate.'});print(ref(rp),ref(h),len(check),sorted(by.items()))

