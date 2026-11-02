import json,pathlib
E=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie');F=E/'R3'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
q=rd(F/'Dovezi_criterii.json')['evidence']; rec=rd(F/'Reexaminare_368.json')
for u in rec:
 if u['reconstructed']:continue
 t=u['task'];j=rd(F/'taskuri'/('Fisa_'+t+'.json')); r=j['R3_semantic_review'];txt=[]
 for i in r['nominal_origin_sources']:
  o=q[i]['content_or_observation'];lit=o['literal'];a=o['alias'];txt.append((a,str(lit)[:150]))
 print(t, j['source_literal']['raw_cerere'].split('codul «')[-1].split('»')[0][:30], txt[:2] if txt else j['title'][:80])

