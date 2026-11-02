from a12_r6_exec import *
from collections import defaultdict,Counter
r=E/'R6_supliment';r.mkdir(exist_ok=True)
p=E/'R6_pregatire/ERP/UX/UX_15_forme_roluri.json';d=rd(p);assert sha(p)=='8e6bdfe4a723a57c57b29fadd4f226cee4e34e6e62b6927cf7f9c422e47dd83d';ng=E/'R3_zone/A04/Addendum_moneda_NIR.json';n=rd(ng);assert sha(ng)=='39598d287747a4751303653db4b79803888764f070b2900c0c1cc34d1fdde4a8'
cross=defaultdict(list)
for i,row in enumerate(d['matrix']):
 assert row['state']=='DESCHIDERE_CONFIRMATA'and row['role']in (102,103)
 for o in row['criteria']:
  pp=E/('R6/taskuri/Fisa_'+o['task']+'.json');case=rd(pp);cs=sum([case[k]for k in ['operative_criteria_and_audit_criteria','R3_new_criteria','R4_new_criteria']],[]);c=next(z for z in cs if z['id']==o['criterion'])
  cross[o['criterion']].append({'task':o['task'],'criterion':o['criterion'],'persisted_task_sha':sha(pp),'role':row['role'],'AD_Session_ID':row['role_session'],'form_class':row['class'],'source_file':p.relative_to(B).as_posix(),'pointer':'/matrix/'+str(i),'expected_in_this_test':'Cu rolul și dreptul nominal, click pe meniul asociat formei → tab sau panou activ nou și două controale din sursă.','observed':row['state'],'grant':row['ad_form_grant'],'original_requirement_not_decided_by_navigation':c['normative_content'],'business_status_after_navigation':c['current']['status'],'start_context_verified_only':True})
assert len(cross)==23 and sum(map(len,cross.values()))==48
out=r/'A12_UX_NIR_provenienta.json';wr(out,{'utc':datetime.now(UTC).isoformat(),'previous_R6_report_sha':sha(E/'R6/A12_raport.json'),'kind':'Rezultate primite după generarea R6, fără modificarea fișelor deja sigilate.','users':d['summary'],'ux_source_sha':sha(p),'ux_unique_form_criterion_relations':24,'unique_criteria':23,'by_criterion':dict(cross),'control_negative':{'source_pointer':'/native_grant_control','condition':'Archive Viewer absent din meniul GardenUser; nu este o verificare HTTP 403.','source_file':p.relative_to(B).as_posix()},'NIR':{'source_file':ng.relative_to(B).as_posix(),'sha':sha(ng),'pointer':'/invoice','invoice':n['invoice'],'currency_label':n['observed_currency_label'],'recovery':n['recovery'],'scope':n['monetary_scope'],'finding':n['finding'],'task_credit':'Nu s-a găsit un criteriu nominal despre moneda prețului cu amănuntul pe NIR în cele 2.619 de criterii. Totalul afișat nu este atribuit drept valoare RON și nu schimbă un verdict T227.'},'score':None});print(sha(out))

