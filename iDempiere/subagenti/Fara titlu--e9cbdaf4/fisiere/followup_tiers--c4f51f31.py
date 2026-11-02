import pathlib,json,collections,re
O=pathlib.Path(__file__).parent;E=O.parent;F=E/'R4'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
a=rd(F/'Registru_1868.json')['records'];out={}
for name in ['fixture_independent_of_observation','designated_entry_and_evidence','steps','negative_or_counterexample','residual_to_check','individual_dependency']:
 count=collections.Counter(str(x[name])for x in a);out[name]={'unique_strings':len(count),'records_with_nonunique_string':sum(v for v in count.values() if v>1),'most_common_count':count.most_common(1)[0][1],'most_common_example':count.most_common(1)[0][0][:210]}
ex=collections.Counter((v['current_disposition'],v['requires_external_or_hardware'])for v in a);owners=collections.Counter(v['zone_owner'] for v in a if v['current_disposition']=='NEEXECUTAT');top={}
for zone in owners:
 rows=[v for v in a if v['zone_owner']==zone and v['current_disposition']=='NEEXECUTAT' and not v['requires_external_or_hardware']]
 if rows:top[zone]=[{'criterion':v['criterion'],'scope':v['scope_from_task'][:100],'entry':v['designated_entry_and_evidence'],'condition':v['condition_from_source'][:100]}for v in rows[:2]]
f=E/'A11_ledger_652_R4.json';d=rd(f);olds=collections.Counter((y['status'],y['was_new_R4'])for x in d['cases']for y in x['all_criteria'])
out.update({'pending_by_owner_from_original1868':dict(owners),'nonexclusive_external_by_state':[[st,ext,n]for(st,ext),n in ex.items()],'local_still_actionable_examples':top,'new_alias_dispositions':{k:v for(k,n),v in olds.items() if n},'note':'Doublons textuels ne prouvent pas à eux seuls un critère invalide. Ils mesurent le niveau de spécificité des champs pris individuellement.'});out['note']='Repetiția unui câmp nu dovedește singură o eroare. Identitatea de task și oracolul pot fi specifice chiar dacă pașii de probă sunt comuni.'
(O/'remaining_tiers.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print({k:(out[k]['unique_strings'],out[k]['most_common_count'])for k in ['fixture_independent_of_observation','designated_entry_and_evidence','steps','negative_or_counterexample','individual_dependency']},owners)

