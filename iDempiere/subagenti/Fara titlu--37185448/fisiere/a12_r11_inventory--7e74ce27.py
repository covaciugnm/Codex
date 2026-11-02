from a12_r10_publish import *
from collections import defaultdict,Counter
import subprocess,re
P=E/'R11_plan_delta';SRC=P/'A12_tracker_snapshot_v2';target='2fe90ed3f128c33dff7cf9f8674e664a70679390';SSET={'montat','închis','anulat','agregat'}
def asarr(v):return v if isinstance(v,list)else[v]if v else[]
def bare(s):return re.sub(r'^P\d+\.', '',re.sub(r'\s+\(alias [^)]*\)$','',str(s))).strip()
def footprint(v):return hashlib.sha256(enc(v).encode()).hexdigest()
def build():
 snap=rd(SRC/'manifest.json');assert all(sha(SRC/k)==v for k,v in snap['sha_before'].items());assert snap['github_remote_head'].split()[0]==target
 allrows=rd(SRC/'00_STATUS_TASKURI.json');idmap={r['id']:r for r in allrows};assert len(idmap)==len(allrows);p01={i:r for i,r in idmap.items() if r['proiect']=='P01'};m=rd(SRC/'00_CORESPONDENTA_COD_CAPITOL.json');cm={r['id_tehnic']:r for r in m['coduri']};old=rd(B/'Inventar_P01.json');a0={z['technical']:z for z in old['rows']};rr={r['task']:r for r in rd(R10/'A12_raport.json')['records']};hist=rd(E/'A12_istoric_git_stari.json');hmap={z.get('task',z.get('id')):i for i,z in enumerate(hist['rows'])};basep=E/'delta/2026-11-02T20-46-47-993Z/00_STATUS_TASKURI.json';br={z['id']:z for z in rd(basep)if z.get('proiect')=='P01'}
 refidx=defaultdict(set);aux=defaultdict(list);unmapped=[]
 for r in allrows:
  for a in asarr(r.get('id_vechi'))+asarr(cm.get(r['id'],{}).get('id_vechi')):
   x=a.get('id')if isinstance(a,dict)else a
   if x:refidx[bare(x)].add(r['id'])
 def resolve(v):
  k=bare(v);return k if k in idmap else next(iter(refidx[k]))if len(refidx.get(k,()))==1 else None
 def walk(node,f,p,ancestor=None):
  ref=node.get('task')or (node['id']if resolve(node.get('id'))else None); inherit=not bool(ref);tokens=str(ref or ancestor or '').split('/');matched=set(filter(None,(resolve(k)for k in tokens)))
  for k in matched:
   if k in p01:aux[k].append({'source':f,'pointer':p,'inherited':inherit,'explicit_reference':ref,'node':node.get('id'),'state':node.get('stare')})
  if not matched:unmapped.append({'file':f,'pointer':p,'record_id':node.get('id'),'reference':ref,'inherited_from':ancestor,'no_independent_unit':True})
  for i,child in enumerate(node.get('copii',[])):walk(child,f,p+'/copii/'+str(i),ref or ancestor)
 for file,key in [('00_STATUS_RAMASE.json','ramase'),('00_STATUS_FINALIZATE.json','finalizate')]:
  for i,n in enumerate(rd(SRC/file)[key]):walk(n,file,'/'+key+'/'+str(i))
 cand=SRC/'registru_din_Git_candidat.json'
 if not cand.exists():
  pp=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab show '+target+':Documentatie/echipa-2026-10-09/00_STATUS_TASKURI.json'],capture_output=True,timeout=32);pp.check_returncode();cand.write_bytes(pp.stdout)
 cg={z['id']:z for z in rd(cand)if z.get('proiect')=='P01'};rows=[];changed=[];reopened=[];newfinal=[]
 for pos,r in enumerate(allrows):
  if r['proiect']!='P01':continue
  tid=r['id'];m0=cm.get(tid,{});old0=br.get(tid);fi=rr.get(tid);s=r['stare_generala'];dates=r.get('finalizat_la');code=r.get('cod_capitol')or m0.get('cod');ch=r.get('capitol')or m0.get('capitol')or m['capitol_randuri_vechi'].get(tid);ali=sorted(set(bare(t.get('id')if isinstance(t,dict)else t)for t in asarr(r.get('id_vechi'))+asarr(m0.get('id_vechi'))if t));where=[o for o in aux[tid]if o['source']=='00_STATUS_FINALIZATE.json'and not o['inherited']];eligible=s in SSET or bool(where);diff=[k for k in sorted(set(old0 or {})|set(r))if (old0 or {}).get(k)!=r.get(k)];moved=old0 and s!=old0['stare_generala'];explicitly_active_reopen=tid in rr and old0 and old0['stare_generala']in SSET and s not in SSET
  if diff:changed.append({'technical':tid,'canonical':code,'former':old0['stare_generala']if old0 else None,'now':s,'fields':diff,'frozen':bool(fi)})
  if explicitly_active_reopen:reopened.append(tid)
  if eligible and not fi:newfinal.append(tid)
  rows.append({'project':'P01','technical':tid,'canonical':code,'chapter':ch,'title':r.get('nume_sugestiv',r.get('denumire')),'alias_declared':ali,'canonical_in_row':r.get('cod_capitol'),'canonical_in_mapping':m0.get('cod'),'canonical_conflict':bool(r.get('cod_capitol')and m0.get('cod')and m0['cod']!=r['cod_capitol']),'live_pointer':'/'+str(pos),'live_row_sha256':footprint(r),'current_state':s,'last_edit_as_declared':r.get('ultima_actualizare'),'exact_finish_date_if_declared':dates,'parent':r.get('parinte'),'aggregation_target':r.get('agregat_in'),'split_targets':m['inchise_prin_impartire'].get(tid),'eligible_now':eligible,'in_R10':bool(fi),'R10_file_sha256':fi['sha256']if fi else None,'R10_file':('executie/R10/'+fi['file'])if fi else None,'R10_criterion_count':fi['criteria']if fi else 0,'declared_artifacts_count':len(r.get('documente_produse',[])),'historic_comparator_pointer':('/rows/'+str(hmap[tid]))if tid in hmap else None,'final_list_explicit_pointers':[v['pointer']for v in where],'also_in_auxiliary':aux[tid],'git_registry_state':cg.get(tid,{}).get('stare_generala'),'live_equals_git_registry_row':r==cg.get(tid),'change_from_R10':diff,'disposition':'REAUDIT_ON_CHANGED_CODE_OR_TRANSITIVE_DEPENDENCY'if eligible else'OUTSIDE_FINAL_COHORT_KEEP_MONITORED'})
 assert len(rows)==693 and {z['technical']for z in rows if z['eligible_now']}==set(rr)and len(rr)==652;assert len(rd(R10/'Registru_reexecutare_R10.json')['rows'])==2619
 out=P/'A12_registru_693_stari_alias_v2.json';wr(out,{'captured':snap,'canonic_source':S(SRC/'00_CORESPONDENTA_COD_CAPITOL.json'),'stable_live_before_after':True,'oracle_for_project_assignment':'row.project as recorded; never infer P01 by numeric prefix/historical title. Resolve direct aliases before inherited annotations.','canonical_syntax':'P01.Cnn.Tnnnn; null means lacking a canonical ID and never invent one. Alias legacy is presented separately.','capture_7_files':{f:S(SRC/f)for f in snap['sha_before']},'candidate_registry_git':S(cand),'historical':S(E/'A12_istoric_git_stari.json'),'R10':S(R10/'MANIFEST_R10.json'),'intake':{'all':len(allrows),'P01':len(rows),'by_status':Counter(v['current_state']for v in rows),'canonical_mapped':sum(bool(v['canonical'])for v in rows),'without_canonical':sum(not v['canonical']for v in rows),'official_final':sum(v['current_state']in SSET for v in rows),'extra_final_list_direct':['T229'],'new_final_cohort':newfinal,'reopenings_between_two_snapshots_observed':reopened,'cohort_intersection':len(rr),'from_R10_snapshot':S(basep),'only_changed_live':changed,'new_live_P01_rows':sorted(set(p01)-set(br)),'deleted_live_P01_rows':sorted(set(br)-set(p01)),'delta_vs_candidate_git_count':sum(not z['live_equals_git_registry_row'] for z in rows),'unmapped_auxiliary_not_per_se_final_task_count':len(unmapped),'limit_no_transition_tape':'Două fotografii nu dovedesc inexistența unei redeschideri și reînchideri între ele. Păstrează logurile nominale din istoric, notifică A11 pentru orice tranzit observabil. Un task activ păstrează starea actuală și nu intră printr-o notă de pe alt task.'},'rows':rows,'unmapped_auxiliary':unmapped});print(sha(out),len(rows),len(hmap),sum(z['historic_comparator_pointer'] is not None for z in rows),[(z['technical'],z['fields'])for z in changed]);return out
if __name__=='__main__':build()

