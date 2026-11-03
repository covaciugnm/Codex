import pathlib,json,gzip,collections
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');V=R/'executie/R12_fisiere/A12/Val_03'
def j(n):return json.loads((V/n).read_text(encoding='utf8'))
matrix=j('Matrice_taskuri_criterii_R12_Val03.json')
for x in matrix['current_rows']:
 p=R/x['original_row']['path'];r=json.loads(p.read_text(encoding='utf8'))[int(x['original_row']['pointer'][1:])];print(x['alias'],[(k,v) for k,v in r.items() if k not in ['observatii','descriere','istoric'] and not isinstance(v,(list,dict))][:20])
reg=[json.loads(x) for x in gzip.decompress((V/'Registru_6728_R12_Val03.jsonl.gz').read_bytes()).decode().splitlines()]
for x in reg:
 if x['path'].endswith(('MiscareWms.java','EvaWmsGardaEvents.java','ProceseEcran.java','garzi.sh')): print('REG',json.dumps(x,ensure_ascii=False)[:11000])
for n in ['Evenimente_9_surse_si_2_lecturi.json','Evenimente_N05_17_si_29_lecturi.json','N05_Matrice_4_criterii_istorice.json','Delta_integrala_Val03.json','Index_invers_surse_Val03.json','Cazuri_nominale_121.json']:
 d=j(n);print(n,list(d),json.dumps(d,ensure_ascii=False)[:2200])
