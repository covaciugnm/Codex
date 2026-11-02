# Modele de reproducere, construite separat de sursele primare și de verdictele curente.
families={
'DOCUMENTAR':('revizor independent și autorul documentului','registrul istoric și fișierul de verdict al etapei, pe commitul de închidere','compară subiectul, commitul, constatările, scorul și reparațiile din raport; verifică o ediție ulterioară','exclude verdictul altui subtask sau al altei etape; o simplă mențiune 10/10 nu închide obligația','dosar și istoric Git'),
'RECEPȚIE_STOC':('gestionar autorizat; control contabil separat','două produse P și Q, două gestiuni, doi locatori și ASI; numără 20 și 18 în clonă','compară M_InventoryLine/M_InOutLine, M_Transaction, M_StorageOnHand și Fact_Acct după operație/reversare','refuz rol fără drept, lot lipsă și retry al aceleiași linii; Q trebuie să rămână neschimbat','ERP + bază'),
'CANAL':('responsabil pe canalul A și martor pe canalul B','P și setul S pe două canale și două G1, stoc inițial 20 și rezervă de 7','compară valorile ERP și răspunsul adaptorului de test pe fiecare canal; urmărește preț, cantitate și istoricul','canal B nu se modifică la editarea pe A; repetarea aceleiași chei nu creează efect suplimentar','ERP + API + date canal'),
'CONTABIL':('contabil și rol cu acces restrâns','același cont pe două scheme cu 100 USD și 20 EUR; document și inversare pe firmă/organizație de probă','compară ID, debit/credit și sold pe schemă înainte, după și la storno','nu amesteca schemele; perioadă închisă sau drept refuzat nu trebuie să lase postări','Fact_Acct + C_AcctSchema + document'),
'FISCAL':('contabil al firmei de probă','perioada istorică din criteriu, formularul și varianta exactă; caz cu valoare și caz zero','compară XML/rubrica/totalul cu referința oficială din aceeași perioadă; păstrează identificator, hash și rezultatul validatorului','perioadă vecină, versiune greșită sau postare inversă; nu trimite declarația la partener','ERP + formular + validator'),
'IMPORT':('operator import cu drept asupra firmei A','arhivă sintetică formatată pentru sursa nominală, un rând bun, unul invalid și a doua firmă martor','compară staging și documentul final; repetă după eroare și cu aceeași sursă','zero dubluri la retry, zero mutații în firma B; succesul sumarului nu ține locul citirii efectului','staging + proces + model'),
'UX':('utilizator al ecranului pe rol autorizat și un rol de comparație','aceeași limbă, stare și versiune UI; o valoare completă, una lipsă, rezoluția din criteriu','deschide din meniul nominal; capturează DOM/accesibilitate înainte și după click și citește efectul persistent','apăsare duplicată, anulare și rol fără permisiune; controlul trebuie să păstreze datele și feedbackul stabil','frontend + meniul real + bază'),
'SECURITATE':('operator din organizația A, operator pe B, administrator fixture','două identități, roluri explicite, două organizații și un obiect existent în fiecare','compară statusul HTTP, corpul și obiectul/numărul de rânduri înainte și după','token lipsă/expirat sau ID al firmei B; așteaptă refuz lizibil și zero mutații străine','autentificare + API + DB'),
'INFRA':('operator de laborator cu izolarea impusă de registru','imagine cu digest pin, slot autorizat, două rulări concurente și o eroare injectată','măsoară sănătatea, build-ul sau reluarea specifică; conservă identitatea resur­sei proprii','repornirea/curățenia nu poate șterge resursa altei sesiuni; testează efectul după eșec','build + operare + date'),
'COD':('verificator tehnic al componentei numite și utilizatorul fluxului','exportul Git fixat și JAR-ul instalat, intrare validă și perechea invalidă pentru clasa/metoda din sursă','execută oracolul individual din dosar și testează operația prin punctul normal de intrare; arhivează fișier+linii','compară cu o valoare vecină și cu o versiune anterioară; prezența unei clase nu confirmă funcția','sursă + componentă + test') }
pf=[('DOCUMENTAR','^DIRECTIVĂ_DE_METODĂ|planul taskului auditat|verdictul auditorului|scorul auditorului|audit.+criter|audit independent|aprobare consultant|atestarea|proiectele per funcție'),('SECURITATE','token|portofoli|autoriz|permisi|doi pași|2FA|izolarea pe firm|altă firm|fără drept'),('FISCAL','D(?:100|101|107|112|205|207|300|301|390|394|398|406|700|710)|TVA|SAF.T|ANAF|Intrastat|OSS|impozit|declar[aț]'),('IMPORT','arhiv|import|staging|SAGA-FIDEL|repost'),('RECEPȚIE_STOC','stoc|gestiun|inventar|WMS|locator|recepți|ASI|M_InOut|M_Transaction|pick'),('CANAL','canal|marketplace|comision|eMAG|checkout|site-ul|magazin|platform|AWB|curier'),('CONTABIL','balanț|contabil|Fact_Acct|GL_Journal|plată|încas|moned|sold|schem|storno|revers'),('UX','ecran|buton|tabul|meniul|click|interfaț|aplicaț|traduc|etiche|dialog'),('INFRA','build|jar|versiune|tag|restaur|dump|script|montare|graf|deploy|container')]
def fam(c):
 s=c['kind']+' '+c['normative_content']+' '+c['expected_oracle'];return next((k for k,rx in pf if re.search(rx,s,re.I)),'COD')
def textshort(v,maxn=280):return str(v or '')[:maxn]
def pointers(c,k):
 pat=r'(?<![/:])\b(?:[\w-]+/)*[A-Za-z][\w.:-]*\.(?:java|py|sql|tsx?|html|sh|xml|md|json|tsv)\b';return list(dict.fromkeys(re.findall(pat,c['normative_content']+' '+c['expected_oracle'])))[:4]
roots=[
('Reverificare_PO_receptie_match_storno.json',['T27.06','T27.07','T325','T156'],'PO12→recepție 7→factură7, retur/storno cu match; nu dovedește transportul/vama, putaway sau mutarea conturilor.'),
('Reverificare_balanta_si_receptie_nativa.json',['T156','T157','T58'],'Sold comun pe două scheme confirmat în SQL; nu extinde experiența de închidere în orice cabinet.'),
('Reverificare_inchidere_GL_doua_scheme.json',['T157','T58','T03.02'],'Închidere INCH-1 CO/Y, 120 în EUR din 100 USD + 20 EUR. Date de intrare seed introduse în SQL; scrierea reală prin ERP.'),
('Reverificare_devalidare_GL.json',['T157','T58','T03.02'],'Stornarea nativă RE/Y după închiderea contabilă; nu retroatribui acest caz închiderea istorică.'),
('Reverificare_retur_concurent_colete.json',['T337','T216','T220'],'Autorizare RMA nativă și colete. Nu implică recepția fizică, nota de credit, plata sau contact curier.'),
('Reverificare_crash_PG_ERP.json',['T216','T220','T36.47'],'Cădere injectată între ERP și persistența locală. Rămâne distinctă de un incident de producție sau de scriptul vechi.'),
('Reverificare_restaurare_integrala.json',['T231.03','T42.04'],'Restore complet de cabinet; verifică distinct dosarul de audit, nu doar anexa și rolul.'),
('Reverificare_restaurare_un_canal.json',['T353','T231.03'],'Un canal restaurat fără pierderea datelor altuia; nu certifică întreg dosarul de audit sau editorul traducerilor.'),
('Reverificare_import_catalog_prin_proxy.json',['T353','T352'],'Rute de import catalog prin proxy și efect asupra controller/handler; distinct de scrierea ofertei din iDempiere.'),
('Reverificare_WMS_dimensiuni_native.json',['T324','T366'],'Comparație între dimensiune omisă și nulă. Nu certifică automat importul numeric sau validările T366.'),
('Reverificare_import_furnizori_SAGA.json',['T98','T227','T257'],'Import furnizori cu eroare/retry/0 dubluri; nu este document financiar.'),
('Reverificare_import_factura_SAGA.json',['T257','T227','T154.03'],'Import financiar nativ L8→L12 pe factură sintetică; nu este un eșantion comercial sau un audit al tuturor rapoartelor.'),
('Reverificare_T257_import_fidel_si_protectie.json',['T257','T154.03','T156'],'Refuz protecție SAGA-FIDEL pe documentul importat; distinge protecția de alte procese contabile.'),
('Reverificare_T257_martor_SAGA_FIDEL.json',['T257','T156'],'Martor sintetic pentru reset/refuz, separat de importul L8→L12.'),
('Reverificare_T257_repostare_si_storno.json',['T257','T154.03'],'Document ordinar cu patru note de postare; rol și acțiune distincte de importul fidel.'),
('Reverificare_alocare_incasari_stari.json',['T05','T169','T216','T220'],'Alocare ERP pe stări diferite, nu corelare bancă/AWB întreg.'),
('Reverificare_rol_DocAction.json',['T36.27','T239.02','T333'],'DocAction refuzat pe organizație; nu este sinonim cu canale sau identitatea mobilă.'),
('Reverificare_ASGI_Org0_DocAction.json',['T36.27','T239.02'],'ASGI, org0 și starea facturii după acțiune refuzată.'),
('Reverificare_G3_rezervare_canal.json',['T354','T352'],'13 când există doar 7 rezervate; PO de 4 scade la 9, nu 13; un singur defect de politică.') ]
# Only these finance criteria explicitly relate to the observed posting operation and scheme gate.
def gl_update(c,k):
 if k not in ('T157','T58') or not (IN/'Reverificare_inchidere_GL_doua_scheme.json').exists():return
 if not re.search('schem|contabil|sold|închider.+venit|închider.+TVA',c['normative_content'],re.I):return
 if not re.search('schem|GL_Journal|venitur|cheltuiel|soldurile',c['normative_content'],re.I):return
 obs=[]
 for fp in ['Reverificare_inchidere_GL_doua_scheme.json','Reverificare_devalidare_GL.json']:
  if (IN/fp).is_file():obs.append(ent(fp,'/',rd(IN/fp),'Cazul de închidere prin proces nativ pe soldurile introduse ca fixture; nu acoperă un task întreg.'))
 if obs:
  c['cross_financial_observation']={'evidence_ids':obs,'reason':'Închidere GL_Journal INCH-1 CO/Y pentru 120 în schema euro testată; în sursă 100 USD +20 EUR, apoi reversare RE/Y. Nu se atribuie automat criteriilor altor procese.'}
  if k=='T157' and re.search('schem',c['normative_content'],re.I):attach(c,'CONTRAEXEMPLU_NATIV_SCHEME','Inchidere nativă a amestecat 100 USD și 20 EUR și a postat 120 EUR; cazul se aplică schemelor și procesului testate, fără a certifica restul cerinței.',obs)
def domain_handoff(k):
 out=[]
 for f,ks,msg in roots:
  if k not in ks or not (IN/f).exists():continue
  z=rd(IN/f);e=ent(f,'/',{'id':z.get('id'),'source':z.get('scope')or z.get('boundary')or z.get('limit'),'level':z.get('level')},msg);out.append({'source':f,'evidence_id':e,'boundary':msg})
 return out
def actions(c,k,initially_unexec):
 f=fam(c);actor,fixture,steps,negative,surface=families[f];refs=pointers(c,k);source=c['source_evidence_id'];sr=ev[source];location=str(sr['source'])+' @ '+str(sr['pointer']);own=owner.get(k,'A12'); 
 return {'task':k,'criterion':c['id'],'zone_owner':own,'actual_specialist_if_needed':f,'reviewer':'A11','source_location':location,'scope_from_task':c['normative_content'],'condition_from_source':c.get('preconditions'),'expected_verbatim':c['expected_oracle'],'fixture_independent_of_observation':fixture,'test_actor_not_original_attribution':actor,'designated_entry_and_evidence':((', '.join(refs)+'; ') if refs else '')+surface,'steps':steps,'negative_or_counterexample':negative,'residual_to_check':'Verifică starea rămasă din '+surface+' după «'+c['normative_content'][:105]+'».','alternate_route':'În lipsa UI, verifică prin procesul/DAO sau analiza documentară din '+surface+' pe aceeași versiune și arată explicit care pas E2E nu a fost exercitat.','current_disposition':c['current']['status'],'current_observed':c['current'].get('observed'),'current_evidence_ids':c['current'].get('evidence_ids',[]),'candidate_unit_evidence_ids':c.get('component_assertion_crosscheck',{}).get('ids',[]),'candidate_financial_evidence_ids':c.get('cross_financial_observation',{}).get('evidence_ids',[]),'original_NEEXECUTAT_R3':initially_unexec,'requires_external_or_hardware':bool(re.search('terminal fizic|telefon fizic|scanner fizic|cont partener real|aprobare.+proprietar|consultantul confirmă',c['normative_content'],re.I)),'individual_dependency':'Compară efectul concret pe '+str((refs or [surface])[0])+' și oracolul «'+textshort(c['expected_oracle'],185)+'». Dacă lipsește baseline-ul istoric, indică commitul/documentul care îl poate reconstitui.'}
css='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font:16px/1.5 system-ui;color:#173444;max-width:1150px;margin:2em auto;padding:0 1em}details{margin:.55em 0;padding:.8em;background:#f3f7f8}summary{cursor:pointer;font-weight:650}input{font:inherit;padding:.6em;width:65%}table{border-collapse:collapse;width:100%}td,th{text-align:left;vertical-align:top;padding:.45em;border-bottom:1px solid #cfe0e3}a{color:#176574}code{overflow-wrap:anywhere}</style>'
(recordsdir:=R/'taskuri').mkdir(exist_ok=True); (htmls:=R/'fise_html').mkdir(exist_ok=True);rows=[];plans=[];recoverledger=[];links=set();association=set();initially_1868=set()
histids={}
for k,d in hist.items():
 for c in d['criteria']:histids[c]=d
def markup(w,n,allc):
 k=w['task'];body='<h1>'+esc(k)+' · '+esc(w['title'])+'</h1><p>'+esc(w['canonical'])+' · '+esc(w['state_at_new_capture'])+' · <a href="../taskuri/Fisa_'+esc(k)+'.json">Fișa completă</a> · <a href="../Audit_individual_P01_R4.html">Index R4</a> · <a href="../../R3/fise_html/Fisa_'+esc(k)+'.html">Runda R3</a></p>'
 for c in allc:
  body+='<details><summary>'+esc(c['id'])+' · '+esc(c['current']['status'])+'</summary><p>'+esc(c['normative_content'])+'</p><p><b>Așteptat.</b> '+esc(c['expected_oracle'])+'</p><p><b>Observat.</b> '+esc(c['current'].get('observed') or c['current'].get('blocking_reason') or 'Cerința nu a fost executată integral.')+'</p><p><b>La închidere.</b> '+esc(c['closure'].get('observed')or c['closure'].get('blocking_reason')or 'Înregistrare insuficientă.')+'</p><p><b>Următoarea probă.</b> '+esc(c['next_action'])+'</p><code>'+esc(c['source_evidence_id'])+' '+esc(', '.join(c['current']['evidence_ids']))+'</code></details>'
 return '<!doctype html><html lang="ro"><title>'+esc(k)+' · Audit P01 R4</title>'+css+'<body>'+body+'</body></html>'
def runone(n):
 k=n['task'];orig=R3/n['file'];assert sha(orig)==n['sha256'];w=rd(orig);b=[];nativecase=domain_handoff(k);newcase=k in dec;was=[]
 if newcase:recover(k,b)
 allc=w['operative_criteria_and_audit_criteria']+w['R3_new_criteria']+b
 for c in allc:
  isold=c['current']['status']=='NEEXECUTAT' and c not in b
  if isold:was.append(c['id'])
  native(c,k);gl_update(c,k)
  if c['id']in patchmap:
   data=patchmap[c['id']];es=[];notes=[]
   for j,v in data:
    b0=v['files'];es.append(efile('probe/grep_criterii.json','/'+str(j),v,'COMANDĂ_PLAN_EXECUTATĂ','grep real din plan pe fișiere rezolvate unic; rezultatul actual diferă de comparația historică la o ramură veche.'));notes.append(', '.join(Path(p['path']).name+'='+str(p['matching_line_count']) for p in b0))
   attach(c,'COMANDĂ_STATICĂ_OBSERVATĂ','Am executat comanda din plan pe exportul fixat: '+' / '.join(notes)+'. Numărul de linii este static și nu certifică operația de business.',es+c['current']['evidence_ids'])
  if c['id'] in histids:
   h=histids[c['id']];reports=[d for d in h['docs'] if d['verdict_utterances']]
   c['own_archival_documents']={'count':len(h['docs']),'with_concrete_verdict_statements':len(reports)}
   if reports and (c['kind']=='DIRECTIVĂ_DE_METODĂ' or re.search('planul taskului auditat',c['normative_content'],re.I)):
    ids=[efile('probe/historical_audit_artifacts.json','/'+k,{'docs':[dict(path=v['path'],blob=v['blob'],head=v['heading'],claim=v['verdict_utterances'][:1])for v in reports]},'RAPOARTE_DOSAR_CITITE','Rapoartele sunt istorice și proprii taskului; existența lor nu este certificarea integrală a tuturor fazelor sau a independenței de către A12.')]
    c['closure']={'status':'TRASĂ_DOCUMENTARĂ_PROPRIE_VERIFICATĂ','observed':str(len(reports))+' rapoarte ale etapei din dosarul exact conțin verdict citibil. Tipul, autorul și data fiecărei etape trebuie stabilite distinct.','evidence_ids':ids}
    if c['current']['status']=='NEEXECUTAT':attach(c,'DOCUMENTAR_PARȚIAL_DOSAR_ACTUAL','Citite '+str(len(reports))+' rapoarte cu trimiteri și verdict în fișier direct al acestui task. Nu se acordă independent 10 ori o judecată funcțională din raportul vechi.',ids)
  unit(c,k,c['current']['status']!='NEEXECUTAT')
 localplans=[actions(c,k,c['id']in was)for c in allc if c['id']in was or c['current']['status']=='NEEXECUTAT']
 if k=='T259':
  w['automated_UI_provenance']='Noul test de audit R4 deschide în Chromium din meniul ZK; TestT259Contracte din repo inspectează SQL/JAR. Dacă se cere un test UI versionat în produs, sursa acestuia nu este demonstrată.'
 forensic=[]
 for c in allc:
  req=c['id']; wanted=[(c['source_evidence_id'],'source')]+[(x,'authority')for x in c.get('authority_evidence_ids',[])]
  for ph in ('current','closure'):
   for x in c[ph]['evidence_ids']:wanted.append((x,ph))
  for x in c.get('component_assertion_crosscheck',{}).get('ids',[]):wanted.append((x,'component_candidate'))
  for x in c.get('cross_financial_observation',{}).get('evidence_ids',[]):wanted.append((x,'financial_context'))
  for eid,rel in wanted:assert eid in ev,(k,req,eid);forensic.append((eid,k,req,rel))
 w['schema']='P01.audit.case.r4';w['R4_new_criteria']=b;w['R4_first_1868_action_ids']=[v['criterion']for v in localplans if v['original_NEEXECUTAT_R3']];w['R4_r3_immutable']={'json_sha256':n['sha256'],'html_sha256':n['html_sha256'],'A11_R3_individual_score':ledger[k]['R3_quality_score'],'R4_quality_score_independent':None};w['R4_technical_scope_and_routes']=nativecase;w['R4_reviewed_after_R3']=now();w['R4_source_identity']={'registry_url':registry_urls,'primary_row':snap[k][0],'supplement_row':su[k][0],'primary_sha':sha(B/'capturi/00_STATUS_TASKURI.json'),'supplement_sha':sha(S/'00_STATUS_TASKURI.json'),'original_id':k,'canonical':w['canonical'],'recorded_final_date_primary':snap[k][1].get('finalizat_la'),'recorded_final_date_supplement':su[k][1].get('finalizat_la'),'updated_supplement':su[k][1].get('ultima_actualizare'),'limit':'Data înregistrării în stare nu este automat data execuției.'};w['functional_criteria_unidentified']=False if newcase else w.get('functional_criteria_unidentified');w['A11_score_R4']=None
 out=recordsdir/('Fisa_'+k+'.json');wr(out,w);hp=htmls/('Fisa_'+k+'.html');hp.write_text(markup(w,n,allc),encoding='utf8');return ({'task':k,'canonical':w['canonical'],'title':w['title'],'state':w['state_at_new_capture'],'file':'taskuri/'+out.name,'html':'fise_html/'+hp.name,'sha256':sha(out),'html_sha256':sha(hp),'R3_sha':n['sha256'],'checks':len(allc),'R4_new_scope':newcase,'unexecuted_current':sum(c['current']['status']=='NEEXECUTAT'for c in allc),'coverage_not_complete':True,'R4_score':None},localplans,forensic,was)
def aggregate():
 for row,ps,lis,was in values:
  rows.append(row);plans.extend(ps);links.update(lis);initially_1868.update(was)
 for eid,k,c,role in sorted(links):back[eid].append({'task':k,'criterion':c,'relation':role})
 assert len(rows)==652 and len(initially_1868)==1868
 grouped=defaultdict(lambda:defaultdict(list))
 for v in plans:
  if v['original_NEEXECUTAT_R3']:grouped[v['zone_owner']][v['actual_specialist_if_needed']].append(v['criterion'])
 wr(R/'Registru_1868.json',{'schema':'P01.original_R3_1868','purpose':'Câte o fișă de reexecuție cu actor, precondiție, oracol, intrare, contraexemplu, persistare, sursă și alternative; activitățile propuse nu sunt trecute drept executate.','groups':grouped,'original_count':len(initially_1868),'records':[v for v in plans if v['original_NEEXECUTAT_R3']]});wr(R/'Dovezi_criterii.json',{'schema':'R4','evidence':ev,'inverse_task_requirement_links':back,'R3_catalog_hash':sha(R3/'Dovezi_criterii.json')})
 idx='<h1>A12 · Audit individual P01 · R4</h1><p>652 fișe; 25 aliasuri reexaminate cu sursă nominală. Vezi <a href="Registru_1868.json">traseul celor 1.868 cerințe neexecutate în R3</a>, <a href="Dovezi_criterii.json">catalogul probelor</a> și <a href="A12_raport.json">raportul tehnic</a>. R3 a primit 4,4/10; nota pentru R4 aparține A11.</p><input id="q" placeholder="Filtrează după cod, denumire, stare"><table><thead><tr><th>Task</th><th>Cod</th><th>Denumire</th><th>Stare</th><th>Neexecutate</th></tr></thead><tbody>'
 for row in rows:idx+='<tr><td><a href="'+row['html']+'">'+esc(row['task'])+'</a></td><td>'+esc(row['canonical'])+'</td><td>'+esc(row['title'])+'</td><td>'+esc(row['state'])+'</td><td>'+str(row['unexecuted_current'])+'</td></tr>'
 idx+='</tbody></table><script>q.oninput=()=>{for(let tr of document.querySelectorAll("tbody tr"))tr.hidden=!tr.textContent.toLocaleLowerCase("ro").includes(q.value.toLocaleLowerCase("ro"))}</script>';hp=R/'Audit_individual_P01_R4.html';hp.write_text('<!doctype html><html lang="ro"><title>652 fișe P01 · R4</title>'+css+'<body>'+idx+'</body></html>',encoding='utf8')
 counts={'population':652,'source_checks_R3':2594,'recovered_from_25':len(dec),'checks_current':sum(x['checks']for x in rows),'numeric_status_NEEXECUTAT_now':sum(x['unexecuted_current']for x in rows),'formal_1868_covered_in_rework':len(initially_1868),'original_1868_current_statuses':dict(Counter(p['current_disposition'] for p in plans if p['original_NEEXECUTAT_R3'])),'unit_fixtures':len(set(x['suite']for x in tr)),'unit_attempts':len(tr),'units_executed_first_pass':sum(x['run_exit']is not None for x in tr),'unit_exit0_first_pass':sum(x['run_exit']==0 for x in tr),'unit_calibrations':len(retry),'static_commands':len(patch),'historical_artifacts_opened':sum(h['review_documents_found']for h in hist.values()),'edge_count':len(links)}
 wr(R/'A12_raport.json',{'schema':'P01.task.r4','created':now(),'scope':'652 și 2 capturi, R1/R2/R3 păstrate. Toate cele 1.868 cu statut NEEXECUTAT în R3 au traseu propriu. Nu se acordă automat credit pentru un candidat de suită, o probă transversală sau o propunere de execuție.','score':None,'R3_score_by_A11':4.4,'R3_sha':sha(R3/'A12_raport.json'),'counts':counts,'proof_catalog_sha':sha(R/'Dovezi_criterii.json'),'action_ledger_sha':sha(R/'Registru_1868.json'),'html_sha':sha(hp),'current_input_hashes':{p.name:sha(p)for p in sorted(IN.glob('*.json'))},'scope_limits':['Pentru T352, clasele din Git sunt nemontate în cele cinci cabinete; testul de două canale confirmă propunere și verificarea selecției pe componentă, nu un click și commit ERP cu acel JAR.','Pentru T366, A05 a exercitat serviciul nativ în bundle și contarea, fără automatizare a fiecărui dialog ZK.','Dovezile T257 separă tranzacția ordinară, martorul sintetic, furnizorii, importul financiar L8/L12 și protecțiile pe factura importată; echivalența între scheme rămâne limitată.','Înregistrarea unei probe fără sursă la închidere, hardware fizic sau sesiune reală nu dobândește retroactiv acea probă; fiecare rând restant are acțiune desemnată.'],'records':rows});print(counts,sha(R/'A12_raport.json'),flush=True)
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=7) as px:values=list(px.map(runone,rr['records']))
 aggregate()

