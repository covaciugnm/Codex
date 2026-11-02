from a12_r5_core import *
from html import escape
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import os
rt=rd(R4/'A12_raport.json');profiles=rd(R/'probe/parametri_individuali_din_sursa.json')['records'];pre={x['criterion']:x for x in profiles}
codes={'COD':('JVM/Git','Fixează bytecode-ul și SURSA testului. Ia separat linia executată, markerul, oracolul sursă, intrările/branch-ul și contradicțiile. Markerul de căutare este numai locator.'),
'RECEPȚIE_STOC':('Document nativ sau calculator WMS','Distingi mișcările, locator/ASI, cantitățile, efectele Fact_Acct, actorul, refuzul, reluarea și stornarea. Evaluezi numai pașii pretenției.'),
'UX':('Ecran sau client','Măsori rolul și starea inițială prin sesiune separată, acțiunea, DOM/captură și persistența cerută. O clasă sau un meniu constituie alt strat.'),
'FISCAL':('Regulă și document fiscal','Separi validarea de schemă/format, înregistrările pe cabinet, sandbox-ul instituției și urmele istorice asumate.'),
'DOCUMENTAR':('Documente și lineage','Stabilești starea sursei, autorul identificabil, decizia și ținta, citatul datat și dovada execuției funcției transferate când există.'),
'INFRA':('Izolare/infrastructură','Precizezi cheia de resursă, topologia, replica, refuzul, presiunea aplicată, contorul efectelor, recuperarea și pragul cerut.'),
'CANAL':('Site/staging/ERP','Separi canal și rol, stoc, comandă, staging, validare, rezervă și efect extern. Definești limite care nu sunt traversate.'),
'CONTABIL':('Document și contabilizare','Precizezi organizația, schema, moneda și perioada, cheile de document, starea și valorile conturilor, storno și reluare.'),
'IMPORT':('Sursă import și proces nativ','Păstrezi fișierul-sursă sintetic identificat, procesul și configurația, perechile înainte/după, erorile și reluarea.'),
'SECURITATE':('Identitate și autorizare','Separi rol, tenant și organizație, cheie nouă/replay, efect persistent, răspunsul și informația dezvăluită.'),
'SURSĂ':('Fișa prima afirmație','Extragi numai intrările, efectele și valorile afirmate. Lipsurile rămân nominale.')}
wr(R/'Protocol_exec.json',{k:{'method':v[0],'common_protocol':v[1]}for k,v in codes.items()})
unknown='NEEXECUTAT'
def buildreg(x,c):
 f=x['component_source']; actual=obs.get(c['id'],[]);need=f['required_scenario_gaps'][:]
 if f['recipe_from_own_row']and re.search(r'<(?:vârf|jar|cl|pg|doc|director|dosar)[^>]*>',f['recipe_from_own_row'],re.I):need.append('Rezolvă substituenții nominali din comanda sursă.')
 miss=bool(f['business_oracle_missing']);entry=f['verified_symbol_entrypoints']or f['versioned_paths_uniquely_resolved']or f.get('recipe_from_own_row');target=f.get('expected_structured')
 mat=('PROBĂ_DIRECTĂ_LIMITATĂ' if actual else 'ORACOL_INDEPENDENT_NESPECIFICAT' if miss else 'RUTA_EXECUTABILĂ_NESPECIFICATĂ' if not entry else 'PARAMETRI_DE_PROBĂ_INCOMPLEȚI' if need else 'SCENARIU_SURSĂ_IDENTIFICAT_NEEXECUTAT' if c['current']['status']==unknown else 'SURSĂ_CORELATĂ_CU_REZULTAT_ANTERIOR')
 remedies={}
 if not entry:remedies['intrare']='Identifică în dosarul nominal '+str(f['source_file'])+' operația concretă care ar exercita acest criteriu.'
 if miss:remedies['oracol']='Nu există un prag/efect independent în rândul recuperat. Pentru '+c['id']+' trebuie precizate condiția și starea de acceptare dintr-o sursă de autoritate.'
 if not f['fixture_literals_verbatim'] and not f.get('environment_or_legacy_baseline')and not actual:remedies['fixture']='Furnizește sau reconstituie datele de pornire din proba originală pentru '+c['id']+' înainte de o cerere funcțională.'
 if not f['negative_inputs_verbatim'] and not actual:remedies['control_negativ']='Pragul de eșec/refuz nu este precizat în rândul sursă pentru '+c['id']+'.'
 if actual:remedies['de_acoperit']=[{'layer':y['layer'],'remaining':y['scope_limit']}for y in actual[:1]]
 resource=x['external_split'] or {'classification':'PERIMETRU_NEDOCUMENTAT_PENTRU_CRITERIUL_RECUPERAT','requires_external_or_hardware':None,'local_feasible':'Document nominal la '+str(f['source_file'])+' cu limite distincte ale reproducerii.','historical_provenance_separate':['Autoritatea și exemplarul de la închidere pentru '+c['id']+' trebuie dovedite separat de reproducerea curentă.']}
 return {'task':x['task'],'criterion':c['id'],'original_1868':x['originally_in_1868'],'owner':x['technical_owner'],'protocol_ref':x['protocol_group']or'SURSĂ','entry_and_oracle_specific_to_case':f,'machine_exercised':[{k:v for k,v in y.items()if k in ['evidence','entry','explicit_expected','case_input','layer','result']}for y in actual],'missing_or_conditional':need,'maturity':mat,'individual_next_step':remedies,'resource_boundaries':resource,'R4_state':x['R4_status'],'R5_state':c['current']['status'],'accepted_implementation':None}
def allc(w):return sum([w[g]for g in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[])
def getlinks(c):
 l=[(c['source_evidence_id'],'source')]+[(z,'authority')for z in c.get('authority_evidence_ids',[])]
 for name in ('closure','current'):l += [(z,name)for z in c[name]['evidence_ids']]
 for f,key,rel in [('component_assertion_crosscheck','ids','component_candidate'),('cross_financial_observation','evidence_ids','financial_context'),('installed_schema_probe','ids','metadata_context'),('archive_criterion_output','ids','historic_artifact_context')]:l+=[(z,rel)for z in c.get(f,{}).get(key,[])]
 for z in c.get('strict_related_sources_R5',[]):l.append((z,'case_context'))
 return list(dict.fromkeys(l))
def strv(v):return v if isinstance(v,str)else json.dumps(v,ensure_ascii=False)
def e(v):return escape(strv(v) if v is not None else '—')
def htmlout(w,rows,reg,pos):
 li=[]
 for c in rows:
  cid=c['id'];a=reg.get(cid,{});src=a.get('entry_and_oracle_specific_to_case',{});state=c['current'];items=c.get('R5_measured_scenarios',[])
  dlist=''.join('<li><strong>'+e(v['entry'])+'</strong> · '+e(v['result'])+'<br><small>'+e(v['scope_limit'])+' · '+e(v['evidence'])+'</small></li>'for v in items)
  li.append('<section id="'+e(cid)+'"><h2>'+e(cid)+'</h2><p>'+e(c['normative_content'])+'</p><dl><dt>Statut observat</dt><dd>'+e(state['status'])+'</dd><dt>Sursa și oracolul</dt><dd>'+e(src.get('source_file') or ev[c['source_evidence_id']]['source'])+' · '+e(src.get('source_pointer_original') if src else ev[c['source_evidence_id']]['pointer'])+'<br>'+e(src.get('expected_structured') or c['expected_oracle'])+'</dd><dt>Rută și parametri proprii</dt><dd>'+e(src.get('recipe_from_own_row')or src.get('verified_symbol_entrypoints'))+' · '+e(src.get('fixture_literals_verbatim'))+'</dd><dt>Observat acum</dt><dd>'+e(state.get('observed'))+'</dd><dt>La închidere</dt><dd>'+e(c['closure']['status'])+'</dd><dt>Ce mai trebuie probat</dt><dd>'+e(a.get('individual_next_step')or state.get('blocking_reason')or c.get('constraint'))+'</dd></dl>'+('<ul>'+dlist+'</ul>'if dlist else '')+'</section>')
 return '<!doctype html><html lang="ro"><meta charset="utf-8"><title>'+e(w['task'])+' · audit P01</title><style>body{font:16px/1.55 system-ui;color:#152d43;max-width:980px;margin:32px auto;padding:0 18px}section{border-top:1px solid #b8c6ce;margin:25px 0}dt{font-weight:650}dd{margin:0 0 9px;overflow-wrap:anywhere}small{color:#536878}</style><body><nav><a href="../Audit_individual_P01_R5.html">Indexul celor 652 de fișe</a> · <a href="../taskuri/Fisa_'+quote(w['task'])+'.json">Fișă JSON și toate dovezile</a></nav><h1>'+e(w['task'])+' · '+e(w.get('title'))+'</h1><p>'+e(w.get('canonical'))+' · '+e(pos['state'])+' · '+str(len(rows))+' criterii. '+str(len(w['R5_summary']['added_observations_by_criterion']))+' au o observație nouă identificată. Nota independentă R5 este în așteptare.</p>'+(''.join(li) if li else '<p>Vezi în fișa JSON autoritatea și starea administrativă.</p>')+'</body></html>'
def run():
 for name in ['taskuri','fise_html']: (R/name).mkdir(exist_ok=True)
 pindices={x['criterion']:i for i,x in enumerate(profiles)}; data=[];reg_rows={};index=[];rels=[];totalcounts=Counter()
 for rr in rt['records']:
  f=R4/rr['file'];assert digest(f)==rr['sha256'];w=rd(f);key=w['task']; criteria=allc(w);w['schema']='A12.R5.652';w['previous_R4']={'file':f.relative_to(B).as_posix(),'sha256':rr['sha256'],'quality_score_by_A11':5.4};w['R5_measured_contrast_CW']=related.get(key);assert len(criteria)==rr['checks']
  for c in criteria:
   cid=c['id'];prev=c['current'].copy();extra=obs.get(cid,[]);c['R5_measured_scenarios']=extra
   if extra:
    c['R4_current_prior_to_R5']=prev;delta=' · '.join(dict.fromkeys(t['layer']for t in extra));existing=prev['status'];status='PROBĂ_PARȚIALĂ_R5_COMPONENTĂ' if existing==unknown else existing
    ids=list(dict.fromkeys([*prev['evidence_ids'],*(t['evidence']for t in extra)])); text=' | '.join(t['result'] for t in extra[:3])
    current={'status':status,'observed':((prev['observed']+' | ')if prev.get('observed')else '')+'R5. '+text+(' · Alte observații în R5_measured_scenarios.' if len(extra)>3 else ''),'evidence_ids':ids,'blocking_reason':prev.get('blocking_reason') if existing!=unknown else 'Acoperire măsurată pe '+delta+'. '+extra[0]['scope_limit']};c['current']=current
    if cid=='T219-R2-003':
     c['R4_closure_before_R5']=c['closure'].copy();c['closure']={'status':'APARTENENȚĂ_8_OBIECTE_LA_COMMIT_VERIFICATĂ','observed':text,'evidence_ids':[t['evidence']for t in extra if t['layer']=='istoric Git'],'blocking_reason':'Arborele Git dovedește obiectele cerute la revizia istorică, nu montarea sau data exactă a închiderii.'}
     c['current']['status']='ARBORE_ISTORIC_NOMINAL_VERIFICAT_ÎN_R5'
   if cid in pre:
    a=buildreg(pre[cid],c);reg_rows[cid]=a;c['R5_case_protocol_and_specifics']={'registry_ref':'Registru_reexecutare_R5.json#/records/'+str(pindices[cid]),'maturity':a['maturity'],'protocol_ref':a['protocol_ref'],'next':a['individual_next_step']}
    c['R4_plan_preserved_at']=f.relative_to(B).as_posix()
    # Current-only preconditions explicitly separate general protocol and identifiable case source.
    sc=a['entry_and_oracle_specific_to_case']; c['preconditions']='Protocol '+a['protocol_ref']+'. '+str(sc.get('environment_or_legacy_baseline') or ('Intrări nominale: '+str(sc['fixture_literals_verbatim']) if sc['fixture_literals_verbatim']else 'Date de pornire istorice nedeterminate în această sursă.'))
    if not extra and c['current']['status']==unknown:c['current']['blocking_reason']='; '.join(str(v)for v in a['individual_next_step'].values())or 'Scenariul din sursă nu are o execuție R5 nominală.'
   for eid,rel in getlinks(c):
    assert eid in ev,(cid,eid); rev[eid].append({'task':key,'criterion':cid,'relation':rel})
   totalcounts[c['current']['status']]+=1
  added=[c['id']for c in criteria if c['R5_measured_scenarios']]
  w['R5_summary']={'score_independent':None,'scope':'Cerințe individuale și constatări la versiunea Git fixată; execuție suplimentară, fără credit funcțional la închidere din rezultate ulterioare.','added_observations_by_criterion':added,'unevaluated_current':[c['id']for c in criteria if c['current']['status']==unknown],'task_verdict':'ACTIVITATE_AUDITATĂ_REZULTAT_LIMITAT_LA_CERINȚELE_DOCUMENTATE','semantic_compare_CW':bool(w['R5_measured_contrast_CW'])}
  out=R/rr['file'];page=R/rr['html']; data.append((out,w,page,htmlout(w,criteria,reg_rows,rr)));index.append(dict(task=key,canonical=w['canonical'],title=w['title'],state=rr['state'],file=rr['file'],html=rr['html'],R4_sha=rr['sha256'],criteria=len(criteria),new_observed=len(added),unknown=len(w['R5_summary']['unevaluated_current'])))
 def save(v):
  out,w,page,ss=v;wr(out,w);page.write_text(ss,encoding='utf8');return sha(out),sha(page)
 with ThreadPoolExecutor(max_workers=10)as pool:
  for r,(h,g)in zip(index,pool.map(save,data)):r.update(sha256=h,html_sha256=g)
 assert not(set(obs)-{c['id']for _,w,_,_ in data for c in allc(w)})
 assert set(pre)==set(reg_rows)and sum(totalcounts.values())==2619
 ordered=[reg_rows[x['criterion']]for x in profiles];wr(R/'Registru_reexecutare_R5.json',{'archive_1868':1868,'additional_criteria':13,'records':ordered,'maturity_counts':Counter(x['maturity']for x in ordered),'require_external_or_hardware_for_part_only':sum(bool(x['resource_boundaries']['requires_external_or_hardware'])for x in ordered)})
 wr(R/'Dovezi_criterii.json',{'schema':'A12/R5','R4_catalog_sha256':digest(R4/'Dovezi_criterii.json'),'evidence':ev,'inverse_task_requirement_links':dict(rev)})
 rows=''.join('<tr><td><a href="'+e(z['html'])+'">'+e(z['task'])+'</a></td><td>'+e(z['canonical'])+'</td><td>'+e(z['title'])+'</td><td>'+e(z['state'])+'</td><td>'+e(z['criteria'])+'</td><td>'+e(z['new_observed'])+'</td><td>'+e(z['unknown'])+'</td></tr>'for z in index)
 html='<!doctype html><html lang="ro"><meta charset="utf-8"><title>Audit P01 · R5</title><style>body{font:16px/1.45 system-ui;color:#183449;max-width:1450px;margin:24px auto;padding:0 20px}th,td{text-align:left;padding:6px;border-bottom:1px solid #ccc}th{position:sticky;top:0;background:#f1f5f7}</style><h1>Audit individual P01 · runda 5</h1><p>'+str(len(index))+' fișe, '+str(sum(totalcounts.values()))+' criterii. Observații noi nominale pe '+str(len(obs))+' criterii. Rămân '+str(totalcounts[unknown])+' criterii fără execuție individuală. O constatare de componentă se limitează la observația și la JAR-ul documentate. Fiecare fișă delimitează probele la închidere de verificarea curentă.</p><p><a href="A12_raport.json">Raport și hashuri</a> · <a href="Registru_reexecutare_R5.json">Registrul cazurilor</a> · <a href="Dovezi_criterii.json">Catalog și legături</a></p><table><tr><th>Fișă</th><th>Identificator</th><th>Obiectiv</th><th>Stare</th><th>Criterii</th><th>Observație R5</th><th>Neexecutate</th></tr>'+rows+'</table></html>'
 (R/'Audit_individual_P01_R5.html').write_text(html,encoding='utf8')
 sources=[R4/'A12_raport.json',E/'A11_control_A12_R4.json',E/'R3_zone/A03/A03_raport.json',E/'A09_raport_R2.json',E/'A09/F07_referinta_AND04.json',*P.glob('*.json'),*(P/'JVM').glob('*R5*.json'),*(P/'Simulatoare').glob('*.json'),*(R/'probe').glob('*.json'),R/'sql_batch/executii.json',R/'sql_batch/recalibrare/executii.json',R/'vectors/oracole.json',R/'vectors/rezultate.json',R/'calibrare/executii.json',plan,*sorted((sup/'probe').glob('EX??.json')),*sorted((sup/'probe').glob('EX??_peer_*.json')),*(E/('R2_zone/'+zone+'/'+zone+'_raport.json')for zone in ['A06','A07','A08','A10']),E/'R2_zone/A05_raport.json']
 hashes={v.relative_to(B).as_posix():digest(v)for v in sources if v.is_file()}
 sql=rd(R/'sql_batch/executii.json')+rd(R/'sql_batch/recalibrare/executii.json')
 pg=[v for v in sql if v['psql_exit']is not None]; marks=Counter(q['state'] for v in pg for q in v['actual_assertions'])
 report={'schema':'A12_R5_P01','publication_utc':date(),'git_sha':'6df998aee0e514d30856c461962afe99ebd0d113','staging':'PROPUS_SPRE_A11','quality_score_independent':None,'score_product':None,'changes_made':'1.220 locatori de R4 au fost recitiți și ancorați. Protocolul comun a fost separat de parametrii documentați nominal. A03 nu conferă dovezi funcționale prin matricea de proprietari. Probele de componentă se atribuie exclusiv la nivelul afirmațiilor executate.','counts':{'tasks':len(index),'criteria':sum(totalcounts.values()),'bidirectional_edges':sum(map(len,rev.values())),'EV4_resolved':len(fields),'EV5_new':sum(k.startswith('EV5-')for k in ev),'distinct_criteria_measured_this_round':len(obs),'new_observations':sum(map(len,obs.values())),'current_unexecuted':totalcounts[unknown],'original_1868_current_unexecuted':sum(r['original_1868']and r['R5_state']==unknown for r in ordered),'additional13_current_unexecuted':sum(not r['original_1868']and r['R5_state']==unknown for r in ordered),'maturity_counts':Counter(x['maturity']for x in ordered),'by_status':totalcounts,'sql_attempts_including_retries':len(sql),'sql_reached_pg':len(pg),'sql_exit_zero':sum(q['psql_exit']==0 for q in pg),'sql_markers':marks,'sql_fixtures_closed':sum(q['fixture_closed']for q in pg),'independent_vectors_exercised':56},'retained_limitations':['O fișă pe fiecare task identificat nu implică execuție de produs integrală pentru acel task.','A03 R3 folosit ca relație de responsabilitate, zero credite primite prin el.','Aserțiunile JVM proiect pot folosi propriile așteptări ale proiectului; vectorii A12 cu rezultate calculate separat au strat distinct.','Cele două execuții PostgreSQL TestT36Rest au ieșit cu eroare pentru coloana c_invoice.poreference absentă în schema sintetică, fără atribuirea unui defect în produs.','Stare comercială la închidere, hardware, contract sau partener extern rămân evaluate separat.','Asocierile ZK ale A09 desemnează 23 criterii distincte pe 15 forme. Fără rezultat DOM specific în acest instantaneu nu primesc credit.'],'sources':hashes,'artifact_hashes':{n:digest(R/n)for n in ['Dovezi_criterii.json','Registru_reexecutare_R5.json','Protocol_exec.json','Audit_individual_P01_R5.html']},'records':index}
 wr(R/'A12_raport.json',report);print(report['counts']);print('report',sha(R/'A12_raport.json'))
if __name__=='__main__':run()

