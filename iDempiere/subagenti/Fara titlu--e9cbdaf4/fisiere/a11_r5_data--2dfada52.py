import pathlib,json,collections
E=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie');F=E/'R5'
def r(p):return json.loads(p.read_text(encoding='utf-8-sig'))
d=r(F/'Dovezi_criterii.json'); print(d.keys());ev=d['evidence'];rows=[(k,v)for k,v in ev.items() if k.startswith('EV5-')];print('new',len(rows),collections.Counter(v['level']for k,v in rows))
for k,v in rows[:2]:print(k,str(v)[:1000])
reg=r(F/'Registru_reexecutare_R5.json')['records'];print('reg keys',list(reg[0]));print('fields',list(reg[0]['entry_and_oracle_specific_to_case']));r4=r(F/'../R4/Dovezi_criterii.json')['evidence'];one=next(x for x in ev if x.startswith('EV4'));print('EV4 resolved',ev[one].keys());print(str(ev[one])[:550])
rep=r(F/'A12_raport.json');print(rep['counts']['by_status']);print(rep['retained_limitations']);print('new states',rep['artifact_hashes']);print('src',list(rep['sources'])[:4])

