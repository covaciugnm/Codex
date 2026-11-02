from pathlib import Path
import json, hashlib
O=Path(__file__).parent
p=O/'build_v4.py'
s=p.read_text(encoding='utf-8')
replacements={
"('Cadou personal','Ambalaj cadou":"('Cadou gata de dăruit','Ambalaj cadou",
'21 implementate în tema de bază':'21 de implementat în tema de bază',
'21 tipuri implementate în tema de bază':'21 tipuri de implementat în tema de bază',
'9.2 Cache și consistență fără API nou':'9.2 Cache și consistență în motorul existent',
'TVA, transport, discount, card cadou și monedă explicite':'TVA, transport, discount și monedă explicite',
'Reconciliere, outbox/idempotentă, tampon și alarme; intervenție umană pentru excepții.':'Reconcilierea existentă, idempotentă, tampon și alarme; fără outbox comercial nou în temă.',
'personalization_submit, registry_purchase, pro_quote_submit.':'personalization_submit, pro_quote_submit; evenimentele E4–E7 se activează odată cu extensia. registry_purchase rămâne rezervat conceptului ulterior.',
'Minimum 15 ipoteze ordonate prin impact, încredere și efort; țintă de două experimente pe lună dacă traficul permite.':'Minimum 15 ipoteze ordonate prin impact, încredere și efort; se selectează 3–4 experimente principale în șase luni, după puterea statistică.',
'Homepage și produs\',\'≤170 KB transferat':'Homepage și produs\',\'≤170 KB total; React pe produs ≤120 KB',
'Home, categorie, produs și serie rămân lizibile și navigabile cu JavaScript oprit; insulele adaugă interactivitate.':'Conținutul esențial al celor 21 tipuri rămâne lizibil fără JavaScript; paginile publice sunt navigabile. Funcțiile interactive au alternativă sau mesaj clar, fără pagini goale.',
'praguri de cantitate, preț contractual și cerere repetată':'praguri existente de cantitate, preț public și cerere repetată; prețul contractual pe client rămâne ulterior',
'Lista de ID-uri/SKU-uri este în documentul de trasabilitate.':'Lista de ID-uri/SKU-uri este păstrată în Matrice_Raspuns_Audituri_CESIRO_V2.docx, anexa eșantionului.',
'Nu sunt incluse în costurile de mai sus: buget media plătită, comisioane PSP/marketplace, transport și spargeri, materiale și capacitate de fabricație, personal CESIRO sau achiziție hardware AI.':'Nu sunt incluse în bugetul software de bază: publicitate plătită, comisioane PSP/marketplace, transport și spargeri, materiale și capacitate de fabricație sau hardware AI. Timpul editorilor și al PO CESIRO este cuantificat separat și inclus numai în anvelopa extinsă din §17.1.',
}
for old,new in replacements.items():
    assert old in s,old
    s=s.replace(old,new)
s=s.replace("('S2 CESIRO sitemap','https://cesiro.com/sitemap.xml'),", "('S2 CESIRO sitemap','https://cesiro.com/sitemap.xml'),('S3 Ceașcă 220 ml','https://cesiro.com/p/ceasca-cu-farfurioara-220-ml-maro-decorat-cu-flori-si-spic-de-grau'),('S4 Set 9 piese','https://cesiro.com/p/set-masa-4-pers-9-piese-cana-roz-200-ml-bol-tava-termorezistenta-portelan-cu-trandafiri-roz'),")
s=s.replace("    p(idea)\n", "    p(idea)\n")
s=s.replace("    c=t.cell(0,0);c.paragraphs", "    pr=t._tbl.tblPr;bd=OxmlElement('w:tblBorders')\n    for edge in ['top','left','bottom','right','insideV']:\n        el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');bd.append(el)\n    pr.append(bd)\n    for cell in t.rows[0].cells:\n        m=OxmlElement('w:tcMar')\n        for edge in ['top','bottom','left','right']:\n            el=OxmlElement('w:'+edge);el.set(qn('w:w'),'100');el.set(qn('w:type'),'dxa');m.append(el)\n        cell._tc.get_or_add_tcPr().append(m)\n    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))\n    c=t.cell(0,0);c.paragraphs")
p.write_text(s,encoding='utf-8')
root=Path('Z:/images/Bucatarie & Masa')
paths=['Cani & Cesti/cana-striatii-bej-model-cesiro-casa-masa-familie-locuin-01.jpg','Seturi de masa (Vesela)/010l-set-16-01.jpg','Seturi de masa (Vesela)/set-mic-dejun-verde-aranjat-01.jpg','Seturi de masa (Vesela)/set-vesela-ceramica-24-piese-negru-cu-tacamuri-aurii-01.jpg']
data=[{'path':(root/q).as_posix(),'sha256':hashlib.sha256((root/q).read_bytes()).hexdigest(),'usage':'Referință vizuală în proiect V4; fotografie din arhiva existentă, fără editare. Asocierea exactă SKU, drepturile și afirmațiile tehnice cer validare înainte de publicare.'} for q in paths]
(O/'evidence-v4/visual-sources.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('V4 rafinat și surse vizuale salvate')
