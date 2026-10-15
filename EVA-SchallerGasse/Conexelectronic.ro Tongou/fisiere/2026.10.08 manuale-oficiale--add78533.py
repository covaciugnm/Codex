from pathlib import Path
import requests,json,hashlib
from pypdf import PdfReader
import logging
logging.getLogger('pypdf').setLevel(logging.ERROR)
DEST=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ')
urls=[
('TOQCB2 manual tehnic','https://elcb.net/wp-content/uploads/2023/03/TOQCB2-IOT-Smart-Circuit-Breaker-Manual-Tongou.pdf','Aceeași denumire ca linkul Conex defect; conținutul identic nu poate fi verificat fără originalul Conex.'),
('TOQCB2 manual Tuya','https://www.tongou.com/wp-content/uploads/2024/08/TOQCB2-Smart-Circuit-Breaker-Tuya-Version-User-Manual.pdf','Aceeași denumire ca linkul Conex etichetat 4G/LTE; manual de familie, nu dovadă că orice variantă include toate protocoalele.'),
('SY1 SY2 manual operare','https://www.tongou.com/wp-content/uploads/2024/07/SY1-SY2-Din-Rail-Smart-Switch-Operating-Manual.pdf','Manual de familie alternativ; nu este confirmat identic cu Manual TO-Q-SY2-JWT.pdf sau ZIGBEE 2-3-4P.pdf de la Conex.'),
('SY1 SY2 fisa tehnica','https://www.tongou.com/wp-content/uploads/2024/04/Din-Rail-Smart-Switch-TO-Q-SY1-TO-Q-SY2-Series.pdf','Fișă oficială de familie suplimentară; varianta comercializată și versiunea hardware necesită corelare.'),
('TOSMR1 fisa tehnica','https://www.chayo.tech/wp-content/uploads/2024/04/Smart-Circuit-Breaker-TOSMR1-Series.pdf','Fișă oficială TOSMR1; alternativă de familie pentru SMR1.pdf indisponibil la Conex. SKU 43073 are model neconcordant în descriere.'),
('TOSMR1 manual operare','https://www.chayo.tech/wp-content/uploads/2024/08/SMR1-SMART-METERING-CIRCUIT-BREAKER-Manual.pdf','Manual oficial de familie TOSMR1; asociere sigură la seria din titlul SKU 43082, asociere de confirmat pentru 43073.'),
('TOQCB2L fisa tehnica','https://www.tongou.com/wp-content/uploads/2024/04/Smart-Circuit-Breaker-TOQCB2L-Series.pdf','Fișă oficială de familie RCBO; curbele, tipul diferențial și protocoalele sunt variante, nu funcții simultane garantate ale tuturor SKU.'),
('TORD4 declaratie conformitate','https://www.chayo.tech/wp-content/uploads/2025/04/TORD4-63-CE-DOC.pdf','Familia TORD4 este declarată RCCB de fabricant, în contradicție cu încadrarea RCBO/curba C a SKU 43092 la Conex.'),
('TORD4 catalog coduri','https://www.tongou.com/es/wp-content/uploads/2018/01/1.Miniature-Circuit-Breaker-1-2-4.pdf','Catalog fabricant: codul exact TORD4-63/2/63/003 apare la RCCB tip AC, 63 A, 30 mA; document istoric, identificarea produsului livrat trebuie confirmată.'),
('TOSP DC manual operare','https://www.chayo.tech/wp-content/uploads/2026/06/TOSP-DC-User-Manual.pdf','Manual oficial de familie SPD DC; modelul, tensiunea și configurația exactă se verifică separat.'),
('TOSP DC declaratie conformitate','https://www.chayo.tech/wp-content/uploads/2025/03/TOSP-DC-CE-DOC.pdf','Declarație de familie pentru SPD DC.'),
('TOSP DC certificat CE','https://www.chayo.tech/wp-content/uploads/2024/08/TOSP-DC-DC-PV-SPD-CE-Certificate.pdf','Certificat de familie, nu înlocuiește verificarea modelului livrat.'),
('TOSPO AC certificat CE','https://www.chayo.tech/wp-content/uploads/2024/05/TOSPO-AC-SPD-CE.pdf','Certificat de familie SPD AC; denumirile Conex TOSPOC40 și TOSPO trebuie corelate.')]
rows=[]
for title,url,note in urls:
    name='2026.10.08 '+title+'.pdf';p=DEST/'Datasheet si manuale'/name
    row={'titlu':title,'url':url,'observatii':note,'path':str(p.relative_to(DEST))}
    try:
        if not p.exists():
            r=requests.get(url,timeout=45);r.raise_for_status();assert r.content.startswith(b'%PDF');p.write_bytes(r.content)
        pdf=PdfReader(p);row.update(status='DESCARCAT',pages=len(pdf.pages),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        (DEST/'Date structurate'/(p.stem+'.txt')).write_text('\n'.join(f'PAGINA {i+1}\n{pg.extract_text()}' for i,pg in enumerate(pdf.pages)),encoding='utf-8')
    except Exception as e:row.update(status='EROARE',error=str(e))
    rows.append(row);print(title,row['status'],row.get('pages'),flush=True)
(DEST/'Date structurate'/'2026.10.08 registru manuale oficiale.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
