from a03_r4_slot import *
import time
wd=pidfile.read_text();assert dest=='158' and re.fullmatch(pattern,wd)
for nm,outf in [('race.json','T58_race_native.json'),('asset_account_fix.json','T58_asset_account_fix.json'),('august-extra-seed.json','T58_2schema_setup.json')]:
 x=sh(f'cat {wd}/{nm}');assert x.returncode==0;dump1(outf,json.loads(x.stdout))
rr=j(probe/'T58_race_native.json');assert len(rr['attempts'])==10 and not any(y['VC_without_AMORT'] for y in rr['attempts'])
resource={'utc':now(),'legacy_owner_task':'P01.T58','actual_official_task':'P01.T158','actual_canonical_task':'P01.C02.T0002','research_criteria':['T58-R2-005','T58-R2-006','T58-R2-009','T58-R2-010','T58-R2-013','T58-R2-014'],'registry_sha':h(d/'Inventar_P01.json'),'relationships':[{k:r.get(k) for k in ('technical','code','raw_state','merged_into','alias_legacy','registry_json_pointer')} for r in j(d/'Inventar_P01.json')['rows'] if r['technical'] in ('T58','T158')],'original_refusal':j(probe/'T58_refuz_istoric.json'),'case_limit':'Aliasul istoric este confirmat prin registru. ID-ul criteriului T58-R2-xxx rămâne cel al fișei A12 T58, distinct de ocuparea fizică a destinației P01.T158. Nicio sarcină de implementare nu a fost redeschisă în portal.'}
sh(f'touch {wd}/finish')
for k in range(24):
 t=sh(f'cd {wd} && tail -14 lifecycle.log');lines=clean_summary(t.stdout)
 if 'CLEANED' in '\n'.join(lines):break
 time.sleep(1)
resource.update(teardown_log=lines,containers_after=sh("docker ps -a --filter label=eva.sesiune=eva-contab-codex-a03r4 --format '{{.Names}}'").stdout.splitlines(),released_task=sh(f'cd {wd} && cat release-task 2>/dev/null || true').stdout[:400],released_slot=sh(f'cd {wd} && cat release-slot 2>/dev/null || true').stdout[:400],teardown_checked_utc=now(),cleanup_complete=any('CLEANED' in line for line in lines));dump1('T58_restitution.json',resource);print(resource['cleanup_complete'],resource['containers_after'],resource['released_task'],resource['released_slot'])
