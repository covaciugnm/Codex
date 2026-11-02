import pathlib,collections,json
D=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R5')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
ev=rd(D/'Dovezi_criterii.json')['evidence'];rows=[(k,v)for k,v in ev.items() if k.startswith(('EV4-','EV5-'))];cnt=collections.Counter();samples={}
for k,v in rows:
 for l in v['strict_primary_locators']:
  t=l.get('kind');cnt[(k[:3],t)]+=1;samples.setdefault(t,[v['source'],repr(l)[:440]])
print(cnt);print(samples)
a=rd(D/'Registru_reexecutare_R5.json');s=a['records'][0];print('regr',list(s),list(s['entry_and_oracle_specific_to_case']));r=rd(D/'A12_raport.json');print('fields first',r['counts'].get('maturity_counts')); print('states R5',r['counts']['by_status']); print('qa',list(rd(D/'Verificare_R5.json')))

