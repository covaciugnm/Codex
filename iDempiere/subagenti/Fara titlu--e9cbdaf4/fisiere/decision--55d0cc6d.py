from pathlib import Path
import json,hashlib,collections
O=Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_bytes())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ptr(x,key):
 for a in key.lstrip('#/').split('/'):
  if not a:continue
  a=a.replace('~1','/').replace('~0','~');x=x[int(a)]if isinstance(x,list)else x[a]
 return x
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
S=E/'R6_supliment';U=rd(S/'A12_UX_NIR_provenienta.json');T=rd(S/'A12_T36_T36_31.json')
assert h(S/'A12_UX_NIR_provenienta.json')=='ca3c3d2c975ae2d11774d6d11e5ca4c560682816e22f7ebb084dee57e82e5882' and h(S/'A12_T36_T36_31.json')=='df544b14b484290f1b1f15f9c51f5340c6efb4c5e525f34268e3ed934eca4bd3'
raw=rd(R/T['rows'][0]['source_file'])
groups=collections.defaultdict(list)
for x in T['rows']:
 assert h(R/x['source_file'])==x['sha256']==T['origin'];value=ptr(raw,x['pointer']);assert value==x['observed']
 groups[x['target']].append(value)
assert len(groups['git'])==len(groups['instalat'])==12 and groups['git']==groups['instalat']
ux=rd(R/U['control_negative']['source_file']);assert h(R/U['control_negative']['source_file'])==U['ux_source_sha']
seen=set();pairs=set();focus=set()
for i,rows in U['by_criterion'].items():
 for x in rows:
  z=ptr(ux,x['pointer']);assert z['role_session']==x['AD_Session_ID'] and z['role']==x['role']and z['class']==x['form_class'] and z['state']==x['observed']and z['ad_form_grant'];assert any(q['criterion']==i for q in z['criteria'])
  assert h(E/'R6/taskuri'/('Fisa_'+x['task']+'.json'))==x['persisted_task_sha']
  seen.add((z['class'],i,z['role']));pairs.add((z['class'],i));focus.add(i)
assert len(seen)==48 and len(pairs)==24 and len(focus)==23 and len(ux['matrix'])==30
for row in ux['matrix']:
 assert row['state']=='DESCHIDERE_CONFIRMATA'
 events=[ob for ob in row['observations'] if ob['result']=='DESCHIDERE_CONFIRMATA']
 assert any(all(k for k in v['checks'].values()) for ob in events for v in ob['observed'])
N=U['NIR'];p=R/N['source_file'];assert h(p)==N['sha'];n=rd(p);assert n['invoice']==N['invoice']
money=[]
for c in n['cases']:
 for s in c['source_links']: assert h(E/s['path'])==s['sha256']
 money.append([c['id'],c['input'],c['total_cells_exact']])
assert float(n['invoice']['GrandTotal'])==7*10+5*100
supp={'revision':'R6 POST-SIGILARE','reviewer':'A11','inputs_sha256':{p.name:h(p)for p in (S/'A12_T36_T36_31.json',S/'A12_UX_NIR_provenienta.json')},'T36_and_36_31':{'verdict':'ACCEPTAT_PROBA_SQL_ÎN_ARIA_CONFIRMĂRII_RESTULUI','source':T['origin'],'distinct_scenarios':12,'two_builds':24,'examples':groups['git'],'scope':'Signed rest/tenant/credit/allocare prin fixture SQL, nu admitere globală a ferestrei Scadențar ori a tuturor operațiunilor părinte.'},'UX':{'verdict':'ACCEPTAT_DESCHIDERE; FĂRĂ_VERDICT_DE_BUSINESS','unique_forms':len({x['class']for x in ux['matrix']}),'role_form_openings':30,'unique_form_criterion':24,'multiple_role_claims':48,'unique_business_criteria':23,'all_original_requirements_preserved':True,'negative':'Archive Viewer absent GardenUser în navigare; nu este HTTP 403.'},'NIR':{'verdict':'ACCEPTAT_F01_PREVIEW; NICIO_DUBLARE_DE_DEFECT; RECUPERARE_MANUALĂ','primary':h(p),'invoice':n['invoice'],'totals_from_captures':money,'limit':'Linia afișează lei la diferențe de pe factură USD, totalul nu are monedă tipărită; nicio emitere/postare/pierdere cuantificată. T227 nu devine acceptat.'},'score_on_R6':None}
w(E/'A11_control_suplimente_A12_postR6.json',supp)
L=rd(E/'A11_ledger_652_R6.json');r5=rd(E/'A11_control_A12_R5.json');strict=rd(O/'strict_R6.json')
ratings=r5['criteria']
for c in ratings:
 c['previous_QC_R5']=c['earned']
 for s in c['subchecks']:
  s['previous_R5']=s.pop('earned');s.pop('previous',None);s['earned']=s['previous_R5']
  if s['id']=='QC04-R4':s.update(result='VERIFICAT',earned=0.2)
 c['earned']=round(sum(s['earned']for s in c['subchecks']),1)
rnotes=['652/652 JSON și HTML, factori de versiune și istoric distincte, plus 64 hashuri de intrare și cinci ale artefactelor.','2.619 criterii în aceeași ordine și 8.246 muchii controlate în ambele sensuri. 1.587 neexecutate și surse normativ incomplete fără transfer din probe generale.','T259 și T338 în aria probată. Deschiderea celor 15 forme pe două roluri este livrată după sigilarea R6 și notată separat. Nu închide cele 23 criterii de business.','T03: două fire, două tranzacții, rollback, retry, mutant. Concurența este afirmată numai în JVM testată. Cross-JVM A11 și 3<5 statice delimitate. QC04-R4 câștigat. Contractul comercial complet rămâne deschis.','Efectele DB proprii sunt identificate; la T06 diferență zero pe subcazurile executate, nu probă pe populația istorică 168. Există în continuare căi de ocolire și efecte globale nerezolvate.','T338 păstrează lanțul nativ de comandă și aviz în aria lor și lipsurile de corelare G2. Nu este acreditat un transfer de custozi, un AWB ori un retur dintr-o simplă confirmare de document.','Izolarea necunoscută marcată, iar controlul concret la T06 cu CUI diferit s-a oprit la guard anterior. Lipsa rolurilor și drepturilor tuturor căilor rămâne explicită.','T190 criteriul C4 verificat în ambele JAR-uri, T18.01/02 și T40.14 tratează AD_Table și suportul nativ fără promovare la efectul comercial.','108 comparații, 487 oracole ori lipsuri individuale, 258 predicate verificate direct, 236 locatori EV6. Alte 148 rezultate nu au predicatul nominal cuvenit și nu sunt acreditate. Cazurile-limită și performanța nu au acoperire integrală.','R5-Q1 și R5-Q4 corectate și reverificate. Toate cele 81 acțiuni au un răspuns; 148 oracole fără predicat, 1.587 neexecutate și referințele documentare incomplete mențin limita asupra închiderii integrale.']
for c,n in zip(ratings,rnotes):c['justification']=n
score=round(sum(c['earned'] for c in ratings),1);assert score==5.8
report=dict(schema='eva.A11.A12.R6',reviewer='A11',target_sha256=L['source'],gate='RELUARE_NECESARĂ',quality_score=score,verified_subchecks=29,out_of=50,product_score=None,score_scope='Calitatea demonstrațiilor auditului. Eșecul reproductibil la un produs este o dovadă pozitivă de calitate a auditului; un pas imposibil din cauza defectului se marchează ca dependență, cu martori și limită. Scorul nu estimează sănătatea software.',criteria=ratings,ledger={'path':'A11_ledger_652_R6.json','hash':h(E/'A11_ledger_652_R6.json'),'tasks':652,'requirements':2619,'edges':8246,'asymmetric':0,'tasks_fully_quality10':0},integrity={'source_sha256':strict['sources_sha256'],'input_files':64,'artifact_hashes':5,'new_distinct_evidence':236,'observations':240,'new_claimed_criteria':32,'controls_found_by_historical_attachment':99,'attachment_locator_instances_reopened':201,'distinct_source_blobs':100,'original_487_evaluated':487,'old_cases_reviewed':108,'source_predicate_reread':258,'source_predicate_discrepancies':len(strict['source_predicate_locator_discrepancies']),'strict_EV6':strict['EV6_strict']},
positive_and_limits={'T03-R2-039':'Prag static 3<5, prima condiție 0. Garda produsului pe două fire și rollback cu martorul fără unicitate sunt demonstrate în laborator. A11 a obținut simultan aceeași cheie în două JVM pe Git și pe JAR-ul instalat. Nu se susține dublare contabilă ori existență a două noduri în cabinet.','T06-R2-008_020_021':'Refuz nativ archiva ilizibilă cu SQLiteException și 0 rânduri, PInstance măsurat. Cazul cu alt CUI s-a oprit la precondiție; nu a exercitat mesajul specific cui_diferit. Din cauza acestei precondiții nu se creditează o ramură ulterioară.','T190-R2-007':'Opt valori distincte × două JAR-uri, și A11 le-a refăcut cu aceeași funcție nativă com.eva.ro.contab.setup.EvaMetadata.coloaneDeLargit. Accept C4 unitar, independent de tabel fizic/migrare.','T159_T204_T314_T323':'Mutații/teste exercitate pe straturile declarate: 19 situri de tipărire în cod, rol injectat SQL/Java; 7 rute de locator sunt probe de propagare, nu 7 documente persistate.','T110_T111':'T110 are 524 rânduri documentare. T111 nu dovedește toate explicațiile de beneficiu: G254/G301/G376 descriu inactivitatea.','observation':'24 au ieșit din NEEXECUTAT: 17 subcazuri, 1 precondiție, 3 contexte native, 2 documentare și 1 diferență de versiune. Cele 30 contexte/observații fără verdict dispozitiv sunt separate de cele 1.587. 309 stări PASS_DOVEDIT preponderent administrative, așa cum sunt delimitate în R5.'},
remaining={'noexecution':1587,'no_declared_external_part':1542,'has_partial_external':45,'new_13_remaining':9,'unclassified_external_for_added':0,'unknown_predicate_EV5':148,'original_R5_Q2_blank_resolved':81,'owner_all':{'A12':27,'A10':41,'A03':599,'A07':84,'A04':104,'A09':161,'A06':214,'A05':254,'A01':103},'open_qualifications':'Cele 45 au dependență externă/hardware/autoritate în parte; nu sunt 45 dosare blocate complet. Absența unui etalon istoric nu devine automat defect sau acceptare.'},
mandatory_reaudit=[{'id':'R6-Q1','scope':'Descompune cele 1.542 locale fără parte externă și cele 45 cu dependență parțială. Pentru fiecare distinge cerință cu fixture realizabil, cerință fără oracol recuperabil, document istoric și pas blocat de defect. Execută componentele realizabile și vorbește cu titularul numai pentru ce lipsește efectiv.'},{'id':'R6-Q2','scope':'La T06-R2-020 reia cu CUI valid, existent la cabinet și alt CUI valid în arhiva sintetică, verifică exact refuzul specific și delta 0 înainte/după. La T03 consemnează că garda locală permite doi deținători în două JVM; stabilește cu surse dacă distribuția aplicației și alte gărzi sunt relevante înaintea unui verdict contabil.'},{'id':'R6-Q3','scope':'La cele 148 EV5 fără predicat recuperează definiția ori fixează explicit demonstrația permisă. După observarea unui eșec de produs păstrează traseul până la blocaj și execută contraprobă pentru cauza sa, fără a condiționa calitatea auditului de remedierea produsului.'}],
hard_blockers={'HB04':'Criterii obligatorii fără probă completă în 1.587 poziții.','HB09':'Pentru subcazurile cu oracol și fixtură lipsă nicio instrucțiune de review nu substituie probele nominale.','HB11':'Nota 10 nu este eligibilă. Nicio autopunctare detectată.','HB13_R5_T03':'Dispoziția numerelor a fost corectată.'},separate_after_freeze={'path':'A11_control_suplimente_A12_postR6.json','hash':h(E/'A11_control_suplimente_A12_postR6.json'),'not_in_score':True},independent={p.name:h(p)for p in [O/'ledger.py',O/'strict_R6.json',O/'jvm.py',O/'A11Job.java',O/'independent_jvm.json']})
w(E/'A11_control_A12_R6.json',report);print(h(E/'A11_control_A12_R6.json'),h(E/'A11_control_suplimente_A12_postR6.json'))

