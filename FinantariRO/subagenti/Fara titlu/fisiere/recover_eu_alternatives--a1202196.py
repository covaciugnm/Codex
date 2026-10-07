exec(open('recover_eu_round3.py',encoding='utf-8').read().split('with ThreadPoolExecutor')[0])
urls=[('Regulament2021_1057','https://publications.europa.eu/resource/celex/32021R1057.RO.PDF'),('Regulament2024_2509','https://publications.europa.eu/resource/celex/32024R2509.RO.PDF'),('Regulament2023_1676','https://publications.europa.eu/resource/celex/32023R1676.RO.PDF'),('Recomandare2022_C476_01','https://publications.europa.eu/resource/celex/32022H1215(01).RO.PDF'),('Carta_drepturi_2016','https://publications.europa.eu/resource/celex/12016P/TXT.RO.PDF'),('Agenda_competente_COM2020_274','https://www.parlament.gv.at/dokument/XXVII/EU/25777/imfname_10990599.pdf'),('Plan_educatie_digitala_COM2020_624','https://education.ec.europa.eu/sites/default/files/document-library-docs/deap-communication-sept2020_en.pdf'),('Pact_verde_COM2019_640','https://data.consilium.europa.eu/doc/document/ST-15051-2019-INIT/ro/pdf')]
def attempt(pair):
 name,url=pair; rec={'nume':name,'url_sursa':url,'data':'2026-10-07','status':'NERECUPERAT'}
 try:
  r=requests.get(url,timeout=20,headers={'User-Agent':'Mozilla/5.0'});raw=r.content;rec.update(http=r.status_code,octeti=len(raw),url_final=r.url)
  if r.status_code!=200 or not raw.startswith(b'%PDF'):raise ValueError('Raspunsul nu este PDF valid')
  p=PdfReader(io.BytesIO(raw));t='\n\n'.join(f'=== PAGINA {i+1} ===\n'+(x.extract_text() or '') for i,x in enumerate(p.pages))
  if len(t)<2500:raise ValueError('Text insuficient pentru verificare')
  file=out/(name+'.pdf');file.write_bytes(raw);file.with_suffix('.pdf.txt').write_text(t,encoding='utf-8');rec.update(status='DESCARCAT_DE_VALIDAT',fisier=file.name,sha256=hashlib.sha256(raw).hexdigest(),pagini=len(p.pages),caractere_text=len(t))
 except Exception as e:rec['eroare']=str(e)[:200]
 return rec
with ThreadPoolExecutor(max_workers=8) as pool:r=list(pool.map(attempt,urls))
(out/'Registru_alternative_Runda3.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
for x in r:print(x['nume'],x['status'],x.get('octeti'),x.get('pagini'),x.get('eroare'))
