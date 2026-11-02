from a12_r7_pg_cui import *
orig=E/'R7/A12_raport.json';assert sha(orig)=='04c62ea2a020515ca6c20210eb450be343a56fd1dada2be253bb3b41297626ec';dest=E/'R7_supliment';dest.mkdir(exist_ok=True);p=E/'R7_pregatire/G3';a,b=p/'Dictionar_si_writers_CESIRO.json',p/'Dictionar_UI_antet_linii_CESIRO.json'
assert sha(a)=='5a31897734404175906c140420eaf32a7d0077b2cbba8bd829f7532caa289e20'and sha(b)=='1f6e11f98141fda251cfe5a08bf7578ce43df1ff895630f30a7d66f7efe91e8f'
info=[]
for ff in [a,b]:
 z=rd(ff)
 for i,v in enumerate(z['inputs']):
  info.append({'source':ff.relative_to(E).as_posix(),'sha':sha(ff),'pointer':'/inputs/'+str(i),'control':v.get('name')or v.get('id'),'value_exact':v['rows'],'limit':'Read-only din dicționarul și metadatele instalației măsurate; nu a rulat acțiunea de pe meniurile candidate.'})
scope=['T216-R2-001','T216-R2-002','T216-R2-005','T216-R2-006','T216-R2-007']
sw=rd(E/'R7/taskuri/Fisa_T216.json')
inh={c['id']:c['current']['status']for c in sw['operative_criteria_and_audit_criteria']if c['id']in scope}
target=dest/'A12_A06_metadate_Q.json';wr(target,{'utc':datetime.now(UTC).isoformat(),'R7_unmodified':sha(orig),'criterion_links':inh,'matching_scopes':info,'binary_metadata_scope':{'source':a.relative_to(E).as_posix(),'source_sha':sha(a),'pointer':'/installed_eva','observation':'Dintre cinci bundle-uri EVA verificate, numai șase clase din bundle-ul contabil conțin șirul literal EVA_Proprie. Filtrarea prin nume nu inventariază toți scriitorii generici.'},'interpretation':'Coloana și dicționarul au implicitul N. Câmpul este actualizabil, fără callout/proces atașat coloanei, nu s-au identificat triggere comerciale din sfera interogării și cele trei tabele nu au taburi AD standard în această instalație. Există trei intrări custom candidate. Acest material delimitează investigația de după recepția Q și V01, fără dovadă despre operatorul care ar fi completat în producție sau despre rezultatul altei comenzi.','implementation_score':None});print(sha(target))

