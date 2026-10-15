from pathlib import Path
import json,hashlib,shutil
from pypdf import PdfReader
ROOT=Path(r'D:\00. Downloads\Apartamente Viena\00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)')
WORK=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def readj(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def writej(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def copy(source,dest):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert sha(dest)==sha(source),'Fișier existent diferit; nu se suprascrie'
 else:shutil.copy2(source,dest)
 assert sha(source)==sha(dest)
 return dict(cale=rel(dest),sursa=rel(source),sha256=sha(dest),octeti=dest.stat().st_size)
expected={
 'BERGER':dict(json='238764889a777d38ca35b9f42a60880c713af1f17518d4e1f16f7c78e669d26e',docx='170caa79d7f00392a66cfead8f236864b6d34109d5214f8acff490789ca74a81',pdf='853fbd6a2d37015a7e88d9e49148e20745ee7b1cf120f321534480308d0afdf6'),
 'PECH':dict(json='13080c5284c24daae9f3980497b94d69fa3ae115208eb9cd5263416606849464',docx='d798cd082e593d81814677edcff79a0492579912cd8f474999c3bbede38da25e',pdf='da5320ad2ff9c9ed0cf4f9870e5bceb28f90733c8e778425e50040e1e6eabbb8')}
report=WORK/'2026.10.13 Audit juridic final R02.txt'
txt=report.read_text(encoding='utf-8-sig')
for e in expected.values():
 for value in e.values():assert value in txt
assert 'BERGER 10/10 și PECH 10/10' in txt
records=[]
for name,domain in [('BERGER','bmberger.at'),('PECH','zt-pech.at')]:
 dest=ROOT/'00.Proiect/09. Vertraege'/domain/'2026.10.13 Juristischer Werkvertrag'
 sourcejson=WORK/f'2026.10.13 Werkvertrag {name} R02.json';j=readj(sourcejson)
 stem=f'2026.10.13 Werkvertrag {name} juristisch R02'+(' final' if name=='BERGER' else '')
 sourceword=WORK/(stem+'.docx');sourcepdf=WORK/(stem+'.pdf')
 assert sha(sourcejson)==expected[name]['json'] and sha(sourceword)==expected[name]['docx'] and sha(sourcepdf)==expected[name]['pdf']
 assert len(PdfReader(sourcepdf).pages)==21
 files=[]
 files.append(copy(sourceword,dest/f'2026.10.13 Werkvertrag {name}.docx'))
 files.append(copy(sourcepdf,dest/f'2026.10.13 Werkvertrag {name}.pdf'))
 files.append(copy(sourcejson,dest/f'2026.10.13 Vertragsinhalt {name}.json'))
 sourceoffer=WORK/j['sources']['original_offer']['annex_file']
 assert sha(sourceoffer)==j['sources']['original_offer']['sha256']
 files.append(copy(sourceoffer,dest/sourceoffer.name))
 files.append(copy(report,dest/report.name))
 sources=WORK/'2026.10.13 Surse audit juridic final.json'
 files.append(copy(sources,dest/sources.name))
 rec=dict(data='2026.10.13',prestator=name,parti=['A&C Wohnart Immobilien GmbH',name],versiune='R02 finală',limba='Germană, fără introducere română',capitole=16,anexe=6,pagini_contract_PDF=21,pagini_oferta_anexa_separata=4,net_EUR=45000 if name=='BERGER' else 69300,TVA_EUR=9000 if name=='BERGER' else 13860,brut_EUR=54000 if name=='BERGER' else 83160,audit_scor=10,audit_obiect='Calitatea redactării unui proiect de negociere; nu validare judiciară, abilitare actuală, poliță ori acceptare comercială',statut='NETRIMIS și NESEMNAT; acceptare neconfirmată',completari_inainte_semnare='Reprezentare/date actuale, persoane și abilitări, independență, asigurare, calendar și acceptarea întregului pachet',fisiere=files)
 writej(dest/f'2026.10.13 Registru contract {name}.json',rec)
 records.append(rec)
manifest=WORK/'2026.10.13 Registru contracte juridice finale.json'
writej(manifest,dict(data='2026.10.13',documente=records,operatiune='Reorganizare și revizii critice pe surse austriece; documente finale copiate identic în dosarele prestatorilor',mesaje_noi=0,originale_Eva_noi=0,trimiteri=0,semnaturi=0,plati=0))
qa=WORK/'2026.10.13 Verificare vizuala finala.txt'
qa.write_text(
'2026.10.13 | Verificare vizuală finală a contractelor juridice\n\n'
'BERGER: R02 avea o pagină goală la19. Eliminat exclusiv paragraful gol dintre ultimul tabel al Anexei4 și titlul Anexei5; textul și toate celulele rămân identice. '
'Toate cele21 de pagini finale au fost reverificate individual la rezoluție originală de redactor_juridic; PASS. Anexa4 completă pe18;Anexa5 pe19; semnături pe12; numerotare1–21 și antete repetate corect.\n'
'PECH: toate cele21 de pagini R02 verificate individual la rezoluție originală de contract_pech; PASS. Fără pagini goale, clipping, text suprapus sau caractere lipsă; tabele, semnături și footer corecte.\n'
'Exporturile sunt din DOCXurile efective în Microsoft Word, read-only, macrocomenzi dezactivate; rendererul skill Documents a rasterizat PDFurile native cu Poppler la135dpi. '
'Controlul semantic și financiar independent a fost efectuat de auditor_juridic, pe hashurile finale. Criterii/redactare10/10 sunt distincte de această verificare a aspectului.\n'
f'Registru: {rel(manifest)}\n',encoding='utf-8')
H=WORK/'2026.10.13 Istoric inainte actualizare jurnale'
H.mkdir(exist_ok=True)
def backup(p):
 out=H/p.name
 if out.exists():assert out.read_bytes()==p.read_bytes()
 else:shutil.copy2(p,out)
def prepend(p,t):
 backup(p);p.write_text(t+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
summary=(
'2026.10.13 | Contracte comerciale austriece BERGER și PECH reorganizate și auditate\n'
'Status scurt: două proiecte Werkvertrag B2B, numai în germană, cu16capitole numerotate și6anexe. Fiecare are21pagini PDF, plus oferta originală de4pagini anexată separat. '
'Sumele păstrate: BERGER45.000EURnet/54.000EURbrut; PECH69.300EURnet/83.160EURbrut. Rolurile PI,ZT128 și Bauwerksbuch pentru întreaga clădire sunt reglementate distinct; fără BauKG și management general REALIG.\n'
'Audit critic independent cu rubrică fixată: inițial8,75/8,40;R01 9,8/9,9;R02 final10/10 pentru calitatea redactării proiectelor de negociere. '
'Corecții: exigibilitate obiectivă, retenție/garanție/eliberare și folosirea documentelor, întârzieri și încetare1168, protecție1170b, tranzițieBO2026, insolvență, calendar și alocare a ratelorBERGER pe cele4poziții. '
'Verificare semantică integrală și verificare vizuală a tuturor42pagini finale PASS.\n'
'Ultimul răspuns: operațiune locală, fără comunicare nouă de la prestatori; ultimii respondenți externi și sursele lor sunt păstrați mai jos. '
'Contractele rămân NETRIMISE/NESEMNATE, cu acceptare neconfirmată.\n'
'Următorul pas: lectura proiectelor și confirmarea înainte de semnare a datelor, reprezentării, persoanelor, abilitărilor, independenței, asigurării și calendarului. '
'Nota10 nu reprezintă aceste confirmări și nu se transferă asupra modificărilor ulterioare.\n'
f'Surse: {rel(manifest)}; {rel(report)}; {rel(qa)}\n'
'Dosare finale: 00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Juristischer Werkvertrag și 00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Juristischer Werkvertrag. '
'Istoricul și ofertele originale sunt păstrate. Fără emailuri trimise, semnături sau plăți; numărătorileEva802mesaje/826originale/783documentare neschimbate.')
for name in ['2026.10.13 Status proiect.txt','2026.10.13 Log progres proiect.txt']:prepend(ROOT/name,summary)
BASE=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail'
reg=BASE/'2026.10.13 Registru comunicatii.json';backup(reg);r=readj(reg)
r['actualizari_punctuale'].append(dict(data='2026.10.13',tip='reorganizare_contracte_B2B_si_audit_R02',sursa=rel(manifest),audit=rel(report),mesaje_noi=0,originale_noi=0,trimiteri=0,semnaturi=0,plati=0,scor_redactare={'BERGER':10,'PECH':10},statut='NETRIMISE/NESEMNATE; proiecte de negociere',destinatii={x['prestator']:x['fisiere'][0]['cale'] for x in records}))
writej(reg,r)
for rec,pname,last in [(records[0],'Markus Berger','2026.08.17'),(records[1],'Pech','2026.09.17')]:
 path=BASE/'Parteneri'/f'2026.10.13 Log discutii - {pname}.txt'
 block=(
 f'2026.10.13 | {rec["prestator"]} contract juridic R02 reorganizat\n'
 f'Status scurt:21pagini PDF șiWord,16§ și6anexe, numai germană; sumele originale păstrate. Audit de redactare10/10, verificare integralătext/tabele și aspectPASS. '
 'NETRIMIS și NESEMNAT; acceptare neconfirmată. FărăBauKG/managementgeneralREALIG;BWB întregexistent+nou șiPIpânăfinalizare incluse ca obligații propuse.\n'
 f'Ultimul răspuns extern: {last}; reorganizarea nu este un răspuns nou și nu prelungește oferta existentă.\n'
 'Următorul pas: lectura, negocierea și completarea probelor/persoanelor/datei reale înainte de semnare și preluarea funcțiilor. '
 'BERGER: prelungirea/reconfirmarea comercială nu este documentată; PECH: calendarul detaliat și acceptarea extinderilor sunt de confirmat.\n'
 f'Surse: {rec["fisiere"][0]["cale"]}; {rec["fisiere"][1]["cale"]}; {rel(report)}; {rel(manifest)}')
 prepend(path,block)
README=ROOT/'folder map/README.md';backup(README)
readme=(
'# 2026.10.13 — Contracte juridice BERGER și PECH cu audit critic final R02\n\n'
'Versiuni curente: ../00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Juristischer Werkvertrag/2026.10.13 Werkvertrag BERGER.docx și PDF; '
'../00.Proiect/09. Vertraege/zt-pech.at/2026.10.13 Juristischer Werkvertrag/2026.10.13 Werkvertrag PECH.docx și PDF. '
'Fiecare21pagini,16capitole și6anexe, numai germană, plus oferta originală separatăAnlage5. Totaluri net45.000/69.300EUR păstrate. '
'Rapoarte, rubrică, jurisprudență și istoric: ../00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit/. '
'Audit final10/10 pentru redactarea proiectelor de negociere, nu pentru acceptare sau confirmarea datelor/abilitărilor/polițelor; NETRIMISE/NESEMNATE. '
'Registru final: ../00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit/2026.10.13 Registru contracte juridice finale.json. '
'Toate42pagini finale verificate vizual; jurnalele și registrul comunicărilor actualizate, istoricul păstrat. Nicio comunicareEva nouă, semnare sau plată.\n')
README.write_text(readme+'\nISTORIC PĂSTRAT\n\n'+README.read_text(encoding='utf-8-sig'),encoding='utf-8')
(WORK/'2026.10.13 Jurnal actualizare finala.txt').write_text(summary,encoding='utf-8')
assert r['acoperire']['mesaje_salvate']==802 and r['acoperire']['atasamente_salvate']==826
print(json.dumps(dict(status='Finale salvate și hashurile verificate',documente=[dict(prestator=x['prestator'],word=x['fisiere'][0]['cale'],pdf=x['fisiere'][1]['cale'],audit=x['audit_scor'],pagini=21) for x in records]),ensure_ascii=False,indent=2))

