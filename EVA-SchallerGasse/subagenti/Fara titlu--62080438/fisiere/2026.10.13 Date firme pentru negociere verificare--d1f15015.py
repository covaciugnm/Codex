from pathlib import Path
import json,hashlib,pypdfium2 as pdfium
root=Path.cwd()
work=root/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
out=work/'2026.10.13 Date firme pentru negociere surse vizuale'
out.mkdir(exist_ok=True)
sources={
 'BERGER':('00.Proiect/09. Vertraege/bmberger.at/2026.08.17/2026_08_17_Anbot_Statik_Detail.pdf',[0,3]),
 'PECH':('00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Juristischer Werkvertrag/2026.10.13 Anlage 5 Originalangebot PECH 2026.09.17.pdf',[0]),
 'AC FBA':('01. Proprietate + Acte/Acte Firma A&C Wohnart/FBA A&C Wohnart, FN 668224h.pdf',[0,1]),
 'AC UID':('06. Utilitati/UTILITATI APA - Wiener Wasser/Mitteilung Steuernummer, UID_A&C Wohnart.pdf',[0]),
}
inventory=json.loads((root/'folder map/inventar.json').read_text(encoding='utf-8'))
records=[]
for name,(rel,pages) in sources.items():
 p=root/rel
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 idx=next(x for x in inventory if x['cale']==rel)
 records.append({'id':name,'path':rel,'sha256':digest,'unchanged_vs_index':digest==idx['sha256'],'pages_inspected':[n+1 for n in pages]})
 doc=pdfium.PdfDocument(str(p))
 for n in pages:
  image=doc[n].render(scale=2).to_pil()
  image.save(out/f'2026.10.13 {name} p{n+1}.png')
for provider in ['BERGER','PECH']:
 p=root/f'00.Proiect/09. Vertraege/{"bmberger.at" if provider=="BERGER" else "zt-pech.at"}/2026.10.13 Juristischer Werkvertrag/2026.10.13 Werkvertrag {provider} R05.pdf'
 records.append({'id':provider+' R05','path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'unsigned_draft_no_independent_identity_proof'})
(work/'2026.10.13 Date firme pentru negociere surse locale.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
