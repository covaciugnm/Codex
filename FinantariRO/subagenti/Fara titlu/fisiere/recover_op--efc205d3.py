exec(open('recover_eu_alternatives.py',encoding='utf-8').read().split('\nwith ThreadPoolExecutor')[0])
def op(id,fmt='pdf'):return 'https://op.europa.eu/o/opportal-service/download-handler?identifier='+id+'&format='+fmt+'&language=ro&productionSystem=cellar&part='
urls=[('Regulament2023_1676',op('636fb984-4894-11ee-aeff-01aa75ed71a1')),('Regulament2024_2509',op('fb2caf66-7ba3-11ef-bbbe-01aa75ed71a1','pdfa2a')),('Carta_drepturi_2016',op('15dd93b6-09d5-406e-8d2d-74afe719f94d')),('Regulament2021_1057','https://www.adrbi.ro/media/2321/regulamentul-ue-2021-1057-fse-p.pdf'),('Recomandare2022_C476_01',op('4e1055e8-7c4e-11ed-9887-01aa75ed71a1')),('Plan_educatie_digitala_COM2020_624_RO',op('c8eef67f-0346-11eb-a511-01aa75ed71a1'))]
with ThreadPoolExecutor(max_workers=5) as pool:r=list(pool.map(attempt,urls))
(out/'Registru_op_Runda3.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
for x in r:print(x['nume'],x['status'],x.get('octeti'),x.get('pagini'),x.get('eroare'))
