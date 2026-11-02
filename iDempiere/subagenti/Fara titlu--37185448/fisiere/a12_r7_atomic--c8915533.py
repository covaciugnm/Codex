from a12_r7_pg_cui import *
import base64,collections
records=rd(E/'R6/Registru_reexecutare_R6.json')['records'];rg={x['criterion']:x for x in records if x['R6_state']=='NEEXECUTAT'}
man=rd(RP/'stack_exec.json')+rd(RP/'stack_exec_neexec.json')['new'];suite_by={ (a['suite'],a['target']):a for a in man}
dev={
'T06-R2-004':('TestComparatieSaga',r'(?:N[0-7](?:\b|:)|CUI|lips.*SOCIET|cititor)'),
'T11-R2-013':('TestRegesPoarta',r'(?:poarta|poartă|caz|cod|refuz|URL)'),
'T156-R2-023':('TestT156MutareCont',r'(?:C-17\b|B7|t156.*RO|%s.*argument)'),
'T156-R2-028':('TestT156MutareCont',r'(?:INV4|ensureT156.*(?:idempot|a doua))'),
'T159-R2-006':('TestT159LotA',r'paritate H(?:0[1-9]|1[0-9]|2[0-9])\b'),
'T159-R2-009':('TestT159LotA',r'(?:UK.*2020|2020.*UK|UK.*UE_TARA_GB)'),
'T159-R2-010':('TestT159LotA',r'amprenta.*(?:D300|D390|D394|D406)|(?:D300|D390|D394|D406).*amprent'),
'T159-R2-011':('TestT159LotA',r'(?:rd\.?33|D300_ACH9_RD33)'),
'T159-R2-018':('TestT159LotB',r'paritate.*(?:vârst|trept|norm|CM|sărbător|sarbator)'),
'T159-R2-019':('TestT159LotB',r'(?:grupa D112|D112.*C2|C2.*D112)'),
'T163-R2-015':('TestT163ArticoleDiverse',r'(?:^.{0,9}C-[0-9]+\b|set.*atribut|inventar|storn)'),
'T186-R2-009':('TestT186Utilitar',r'U-[12].*(?:1 WARNING|încă 1 WARNING)'),
'T186-R2-010':('TestT186Utilitar',r'U-[456].*(?:CANAR|SQLException|clasei)'),
'T186-R2-011':('TestT186Utilitar',r'(?:t186\.|%s).*(?:EN|RO|format|chei)|U-7.*chei'),
'T186-R2-015':('TestT186Propagare',r'(?:P-[1-7]|UX-[3-7])'),
'T186-R2-020':('TestT186PropagareLB',r'(?:ConfigSocietati|c-catch|1341)'),
'T186-R2-023':('TestT186CatchGoale',r'K-7[ac].*0 blocuri'),
'T186-R2-024':('TestT186CatchGoale',r'K-7.*(?:Python|Java = Python|echival)'),
'T186-R2-025':('TestT186CatchGoale',r'(?:intenționat|intenţionat|20 caractere)'),
'T190-R2-005':('TestReges',r'T190.*(?:inventar|coloane.*prea scurte|lungim.*clasei)'),
'T190-R2-006':('TestReges',r'T190.*(?:16/16|13/13)'),
'T190-R2-035':('TestStudiiSalariat',r'C-32\b'),
'T190-R2-036':('TestStudiiSalariat',r'C-33\b'),
'T204-R2-003':('TestT29Acoperire',r'(?:T204|acoperire)'),
'T204-R2-007':('TestT204Ecrane',r'(?:ferestre.tsv|fixture.*ferestre|fereastra.*lot)'),
'T204-R2-009':('TestT204Procese',r'(?:PDF|XLSX)'),
'T204-R2-011':('TestT29Acoperire',r'(?:excepți|excepti|fixture)'),
'T204-R2-015':('TestT29Catalog',r'(?:registr|Tipărit|P01.T204)'),
'T216-R2-004':('TestT22Factura',r'(?:C_Order\.POReference|C_Invoice\.POReference|DOCUMENTE_COMANDA per factura)'),
'T216.02-R2-003':('TestT22Api',r'(?:id.empoten|refuz|403|autoriza|cheie)'),
'T227-R2-018':('TestT227VerificareImport',r'(?:K-17\b|K-19\b|K-20\b)'),
'T227-R2-036':('TestT28Meniu',r'(?:Meniu|Import|Situații|naviga)'),
'T256-R2-017':('TestT256D394',r'(?:C-[1-6].|caz.*[1-6]|D394.*(?:refuz|ident))'),
'T314-R2-007':('TestT28Meniu',r'(?:Administra|Valuta|Vânzări|Operatii)'),
'T314-R2-011':('TestT314Meniu',r'T314-(?:sql|firma|izolare|nentenant|tenant|canal|rezerva)'),
'T314-R2-031':('TestT314Rol',r'(?:administrarePentru|valutaPentru|constructor|câmp)'),
'T325-R2-005':('TestPutaway',r'(?:10 linii|10 propuse|10/10.*propu|K-04)'),
'T325-R2-026':('TestPutaway',r'(?:propus|propunere).*R[1-4]|R1.*(?:propus|propunere)'),
'T326-R2-040':('TestListaPicking',r'(?:Σ|suma|cantitățile|total.*val).*?(?:val|list)|3 comenzi de probă'),
'T329-R2-015':('TestLoturi',r'(?:K[1-5]\b|ecran.*(?:ASI|lot)|cinci ecrane)'),
'T329-R2-016':('TestLoturi',r'(?:K1[0-7]|K[1-9][.: ]).*(?:lot|ASI|refuz)'),
'T329-R2-021':('TestLoturi',r'(?:t329\.refuz\.tenant|două firme|client 0)'),
'T329-R2-029':('TestLoturi',r'(?:CMP.*lot|lot.*CMP|cost.*lot)'),
'T330-R2-022':('TestFefo',r'(?:cuLot|MovementDate|DateInvoiced|lipiciul|din dialog)'),
'T330-R2-031':('TestFefo',r'(?:propus.*(?:LA|LB|lot)|FEFO.*(?:ieșir|lot))'),
'T331-R2-004':('TestGestiuneNecontabila',r'(?:SQL_FARA_NC|NC.*(?:stoc nominal|stocuri|scade|aproviz|canal)|eNecontabila:)'),
'T340-R2-002':('TestBonConsumLot',r'(?:ASI.*0|0.*ASI|lot.*refuz)')}
def trials():
 out=[]
 for cid,(suite,match)in dev.items():
  if cid not in rg:continue
  for tag in ['git','instalat']:
   if (suite,tag)not in suite_by:continue
   row=suite_by[suite,tag];raw=RP/row['log'];ls=raw.read_text(encoding='utf8').splitlines();hits=[]
   for i,l in enumerate(ls,1):
    if not l.startswith('ANCHOR:'):continue
    head,*frames=l.split('|');actual=base64.b64decode(head[7:]).decode().strip()
    if re.search(match,actual,re.I):
     meaningful=[f for f in frames if f.startswith(suite+'.java:')]; 
     if meaningful:hits.append({'log_line':i,'observed':actual,'assertion_frames':meaningful})
   if not hits:continue
   # Keep up to 8 distinct assertions per URI; listing total is not a test result multiplying the number of builds.
   cf=rg[cid]['entry_and_oracle_specific_to_case'];out.append({'criterion':cid,'target':tag,'suite':suite,'explicit_test_name_in_criterion':suite in cf['named_test_fixtures_in_source'],'branch_selector':match,'expected_from_criterion_source':cf['expected_structured']or cf['constraint_from_own_row'],'original':cf['source_file'],'source_line':cf['source_pointer_original'],'entry':row['test_source'],'source_sha':row['sha_source'],'jar_sha':row['jar_sha'],'log':row['log'],'log_sha':row['sha'],'component_oracle':'Fiecare message/StackTrace leagă predicatul efectiv la testul cu SHA precizat. Numai rezultatul explicit are credit parțial.', 'hits_count_in_scope':len(hits),'bound_results':hits[:8],'exit':row['exit'],'limit':'O aserțiune sau o familie din fixtura aplicației nu dovedește automat tranzacția ERP, manipularea din rol, istoricul sau mutanții ceruți în afara ei.'})
 return out
if __name__=='__main__':
 out=trials();wr(RP/'Cazuri_locale_nominale_79.json',{'original_tasks_with_named_fixtures':79,'scopes_with_confirmed_specific_assertions':len({v['criterion']for v in out}),'records':out,'distinct_business_scenarios_are_not_repetitions_on_two_jars':True});print('matched',len({v['criterion']for v in out}),len(out))

