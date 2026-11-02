from a12_r8_measurements import *
xdir=Path('D:/CodexWork/a12-r8-spec-extra/index.json')
if xdir.exists():a+=rd(xdir)
rg8.extend(rd(P/'JVM/Executii_supliment.json'))
def full():
 run()
 for cid in ['T04.01-R3-001','T04.03-R3-001','T04.10-R3-001']:
  comp(cid,'TestT211Adaptoare',r'/order/save|/order/acknowledge|/order/read|contul|comanda eMAG|paginare','Citirile de comenzi rămân read-only chiar când protocolul de interogare e HTTP POST; căile de mutație sunt refuzate înaintea rețelei.','Transport fals și cont sintetic; import complet în compania reală, deconturi și ecran nu sunt deduse.',12)
 comp('T211.03-R2-002','TestT35Canale',r'COL_CANAL_VANZARE|stoc.{1,40}(canal|prag)|stocul virtual','Regulă de stoc pe canal și 0 diferență în M_StorageOnHand la publicare.','Măsoară parametrii și modelul de canal; nu probează invariantul de stoc înainte/după trimiterea la patru origini.',10)
 comp('T314-R2-021','TestT211Garda',r'4|Blocat din cod|citirile pe fiecare|COMANDA_ANULARE','Patru tipuri cu gardă, citirile admise distinct și scrierile blocate; mesajul are cheie în RO/EN.','Mecanismul gărzii și transportul nu sunt fiecare buton din meniul Vânzări.',8)
 hist('T213.01-R2-003','dovezi-22/clona-dev/ux3/jurnal_ux_l2.txt',r'PB-4.*Campania|C_Campaign|marketing|campaniile','Campania marketing primește și rândul EVA_CampanieMarketing; separat de C_Campaign canal.','Traseu din UI istoric. Relația existenței ambelor tipuri trebuie observată pe rol/companie.',8)
 hist('T17-R2-001','01_fable_cercetare_smart_fintech_si_flux_cesiro1.md',r'Open Banking|AIS|Smart Fintech|PSD2|API','Cercetarea furnizorului pentru conectarea extraselor și corelarea comenzii cu stoc, factură, bancă, AWB și ramburs.','Documentul istoric nu confirmă integrare reală sau accesul la contul furnizorului; fapte contractuale trebuie reverificate la furnizor.',7)
 hist('T204-R2-014','01_plan.md',r'\| O-1 .{0,110}RETRAS','Decizia autorizată retrage A5/D1215 și transferă livrarea la T203.','Se verifică dispoziția; funcția transferată și starea reală a lui T203 sunt separate.')
 z=next(x for x in a if '/T203-'in x['file']and x['file'].endswith('02b_raport_implementare_L-D_L-C.md'));m=[{'line':i,'text':l[:330]}for i,l in enumerate(txt(z).splitlines(),1) if 'D1215'in l and re.search('L-D|livrare|doc:',l,re.I)][:6]
 ev('T204-R2-014','TRANSFER_DOCUMENTAT_CĂTRE_DOSARUL_NOMINAL','historical','Confruntare între task și dosarul succesorului.','Succesorul acceptă livrarea/D1215 în planul și raportul său.',m,[{'git_blob':z['oid'],'git_commit_tree':BASE,'repository_file':z['file'],'lines':[v['line'] for v in m]}],'Dovadă de transfer explicit; nu verifică funcționarea PDF sau a documentului la T203.')
 z=next(x for x in a if '/T224-'in x['file']and x['file'].endswith('10_audit_lot_A_r1.md'));ls=txt(z).splitlines();tab=[]
 for i,l in enumerate(ls,1):
  if not re.match(r'\| \d+ \| \x60?[a-f0-9]{7,40}\x60? \|',l):continue
  cells=[v.strip()for v in l.strip().strip('|').split('|')];tab.append({'line':i,'commit':cells[1].strip(chr(96)),'fields':[v[:1]for v in cells[2:]],'linehash':sha256(l.encode()).hexdigest()})
 assert len(tab)==21
 ev('T224-R2-016','AUDIT_DOCUMENTAR_RECALCULAT','historical','Parcurgere integrală a tabelului, toate rândurile și celulele; verifică antetul care definește cele cinci dimensiuni.', '21 commituri ×5 celule fără gol și o singură identitate Git pe rând.',{'rows':len(tab),'unique_commit_codes':len(set(z['commit']for z in tab)),'field_counts':Counter(len(z['fields'])for z in tab),'empty_cells':sum(not v for z in tab for v in z['fields']),'header':ls[tab[0]['line']-3],'rows_checksums':tab},[{'git_commit_tree':BASE,'git_blob':z['oid'],'repository_file':z['file'],'range':[tab[0]['line'],tab[-1]['line']]}],'Tabelul din audit este verificat; nu validează obiectul programatic al fiecărui commit.')
 # inspect the latest T224 suite output and exact legitimate disposition (including aborted runs)
 cands=[]
 for z in a:
  if '/T224-' not in z['file']or z['size']>150000 or not re.search(r'(suita|rezumat.*test|baza.*rezumat|audit_lot_B)',z['file'].split('/')[-1],re.I):continue
  sr=txt(z);mt=[(i,l)for i,l in enumerate(sr.splitlines(),1)if re.search(r'REZULTAT.*0 FAIL|rulator.*exit.?0|rezumat.*FAIL|0 roșii',l,re.I)]
  if mt:cands.append((z,mt))
 for z,mt in cands[-2:]:hist('T224-R2-011',z['file'],r'REZULTAT.*0 FAIL|rulator.*exit.?0|rezumat.*FAIL|0 roșii','Rezultatul lotului B și re-proba rândului marcat anterior «NU».','Reexecuția ulterioară a scripturilor T224 nu exercită singură lotul B al produsului.',3)
 sk='T314-R2-012';zs=[z for z in a if '/T314-'in z['file']and 'proba' in z['file']and '/M_'not in z['file']and z['file'].endswith('.txt')and z['size']<90000 and re.search(r'VALIDATA.{0,60}RESPINSA|RESPINSA.{0,45}VALIDATA',txt(z),re.I)];zs.sort(key=lambda z:(not re.search('/dovezi-17/',z['file']),len(z['file'])))
 if zs:hist(sk,zs[0]['file'],r'VALIDATA.{0,60}RESPINSA|RESPINSA.{0,45}VALIDATA','Fișă VALIDATA acceptată, RESPINSA exclusă în lista de comenzi.','Consemnare la cabinetul istoric; verifică filtrul în refolosirile curente.',4)
 # Historical Q3: exact customer-account site test only archived app revision. Do not mix origins.
 for cid in ['T216-R2-002','T216-R2-006','T216-R2-005']:
  hist(cid,'dovezi-10/auto-verificare/PB-1_A_B_A.txt',r'eva_tipdocument|invoice\s*\||POST.*201|Confirm|GET.*200|^[ ]*invoice|primul|DocumentNo','Factura emisă și transmisă, série/număr în documentele corelate; afișarea și încasarea sunt operații suplimentare.','Proba inițială aparține originii A/B din dublura site; la Q precondiția de validare nu a existat.',8)
 q=rd(P/'JVM/Executii_supliment.json')
 return cases
if __name__=='__main__':
 cs=full();res=P/'Rezultate_A12_93_si_supliment.json';wr(res,{'utc':now(),'cases':cs,'allocation':{z['criterion']:{'task':z['task'],'owner':z['owner'],'has_observation':z['criterion']in cs,'required_next_if_not_fully_covered':z['case_method']}for z in rows},'sources_checked':{'archive_text_inputs_distinct_by_path':len(set(v['file']for v in a)),'fixed_source':BASE,'JVM_attempts':len(rg8),'JVM_marker_occurrences_traced':sum(x['traced']for x in rg8),'SQL_read_only_prod_or_sandboxes_only':True,'independent_product_score':None}});print(sha(res),len(cs),sum(map(len,cs.values())),[z['criterion']for z in rows if z['criterion']not in cs])

