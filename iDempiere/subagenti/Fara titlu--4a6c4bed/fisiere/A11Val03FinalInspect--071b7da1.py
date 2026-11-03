import pathlib,json
V=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A12/Val_03')
def j(n):return json.loads((V/n).read_text(encoding='utf8'))
for a,b in [('Matrice_taskuri_criterii_R12_Val03.json','Matrice_taskuri_criterii_R12_Val03_corectata_v1.json'),('Handoff_R12_Val03.json','Handoff_R12_Val03_v2.json')]:
 x,y=j(a),j(b);print(a,'newkeys',y.keys()-x.keys(),'modified',[(k,repr(y[k])[:150]) for k in x if x[k]!=y.get(k)])
c=j('Conservare_652_fise_2619_criterii.json');print('historic',[(k,v) for k,v in c.items() if k!='all_dossiers_rehashed'])
for n in ['Ipoteza_G3_dubla_scadere_NEEXECUTATA.json','Ipoteza_G3_promo_NEEXECUTATA.json']:
 print(n,j(n))
