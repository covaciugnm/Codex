from pathlib import Path
import re
root=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
p1=root/'2026.10.14 01 Incetarea politei Donau.txt'
p2=root/'2026.10.14 02 Neplata si acoperirea Donau.txt'
t=p1.read_text(encoding='utf8')
t=t.replace('Forma juridică nu înlocuiește analiza scopului tranzacției, dar nu există acum probe pentru tratarea acestei asigurări ca act de consum.', 'A&C este o GmbH, iar polița privește activitatea sa imobiliară; pe aceste date, dreptul consumatorului din §8 alin.3 nu se aplică.')
t=t.replace('Poziția DONAU rămâne incompletă: nu a justificat integral contractul-cadru, acordul pentru 2036, aplicarea tuturor clauzelor și statutul acoperirii pe ramuri.', 'În actele primite și analizate, poziția DONAU rămâne incompletă: nu este justificat integral contractul-cadru, acordul pentru 2036, aplicarea tuturor clauzelor și statutul acoperirii pe ramuri.')
t=t.replace('Există trei direcții concrete:', 'Piața austriacă permite în principiu contracte comerciale de asigurare pe zece ani. Întrebarea decisivă pentru noi este cine a convenit data 2036, când, cu ce mandat și cu ce drepturi de ieșire. OGH a validat o durată individual negociată; această soluție nu validează automat orice durată impusă prin condiții standard. [J1]\n\nExistă trei direcții concrete:')
t=t.replace('34–43 ABS', '34–42 ABS')
t=t.replace('[L1 §68; P2 AHVB art.12]', '[L1 §68; P2 p.71, AHVB art.12.4]')
p1.write_text(t,encoding='utf8')
t=p2.read_text(encoding='utf8')
t=t.replace('Eine Fristbestimmung, ohne Beachtung dieser Vorschriften ist unwirksam.', 'Eine Fristbestimmung, ohne Beachtung dieser Vorschriften, ist unwirksam.')
t=t.replace('„... sofern der Versicherungsnehmer zur Zeit des Eintrittes mit der Zahlung der Prämie im Verzug ist, es sei denn, daß er an der rechtzeitigen Zahlung ohne sein Verschulden verhindert war.”', '„Tritt der Versicherungsfall nach dem Ablauf der Frist ein und ist der Versicherungsnehmer zur Zeit des Eintrittes mit der Zahlung der Folgeprämie im Verzug, so ist der Versicherer von der Verpflichtung zur Leistung frei, es sei denn, daß der Versicherungsnehmer an der rechtzeitigen Zahlung ohne sein Verschulden verhindert war.”')
t=t.replace('„Die Nichtzahlung der Zinsen oder Kosten hat die in den Abs. 1 bis 3 bezeichneten Rechtsfolgen nicht zur Folge.”', '„Die Nichtzahlung von Zinsen oder Kosten löst die Rechtsfolgen der Abs. 1 bis 3 nicht aus.”')
t=t.replace('§39a exclude efectele prevăzute de §§38/39', '§39a exclude exonerarea asigurătorului prevăzută de §§38/39')
t=t.replace(' ca în unele texte istorice', '')
t=t.replace('§108 în forma actuală nu conține vechea interdicție generală de derogare de la §91.', '§108 în forma actuală nu enumeră §91 între dispozițiile de la care nu se poate deroga în defavoarea asiguratului.')
t=t.replace('OGH 7 Ob 69/01z, 2001.03.30', 'OGH 7 Ob 69/01z, 2001.04.27')
t=t.replace('OGH7Ob69/01z,2001.03.30', 'OGH 7 Ob 69/01z, 2001.04.27')
t=t.replace('https://www.ris.bka.gv.at/JustizEntscheidung.wxe?Abfrage=Justiz&Dokumentnummer=JJT_20010330_OGH0002_0070OB00069_01Z0000_000&IncludeSelf=True', 'https://www.ris.bka.gv.at/Dokumente/Justiz/JJT_20010427_OGH0002_0070OB00069_01Z0000_000/JJT_20010427_OGH0002_0070OB00069_01Z0000_000.pdf')
t=t.replace('Scenariul D: numai costuri/dobânzi restante sau rest de primă în limita§39a. Acestea nu justifică singure sancțiunile prevăzute de lege.', 'Scenariul D: numai costuri/dobânzi restante. Acestea nu declanșează efectele §39 alin.1–3. Dacă rămâne o primă mică în limita §39a, nu intervine exonerarea; această regulă nu șterge restanța și nu trebuie extinsă automat la orice alt efect juridic.')
t=t.replace('§1333alin.2ABGB permite costuri', '§41b VersVG permite taxele asigurătorului numai pentru cheltuieli suplimentare cauzate de conduita asiguratului; aceasta trebuie verificată și pentru cei 30 EUR. Plafoanele tarifare de recuperare nu dovedesc singure necesitatea fiecărei poziții. §1333 alin.2 ABGB permite costuri')
t=t.replace('Simplul text din ordin „numai prime” nu garantează lipsa oricărei dispute.', 'AHVB art.11.2.4 prevede și „Alle eingehenden Zahlungen werden auf die älteste Schuld angerechnet.” Regula contractuală de alocare pe datoria cea mai veche trebuie inclusă în analiză pentru ramura sa. Simplul text din ordin „numai prime” nu garantează lipsa oricărei dispute. [P2 p.69]')
p2.write_text(t,encoding='utf8')
repls={'optzile':'opt zile','pânăla':'până la','pânăîn':'până în','de89pagini':'de 89 pagini','cuTVA':'cu TVA','EURTVA':'EUR TVA','de6.367':'de 6.367','în10%':'în 10%','și19,14':'și 19,14','asupra§':'asupra §','condițiile§':'condițiile §','conform§':'conform §','efectele§':'efectele §','alin.3.':'alin.3.','legea§':'legea §','§39poate':'§39 poate','§40sau':'§40 sau','pentru60':'pentru 60','maxim60':'maxim 60','maximum60':'maximum 60','plafonul practic este60':'plafonul practic este 60','nu636':'nu 636','limita§':'limita §','costuri550':'costuri 550','accesorii550':'accesorii 550','pretins5':'pretins 5','anualăde':'anuală de','înși':'în și','versus':'versus','DONAUmenține':'DONAU menține','externăDONAU':'externă DONAU','Jurisprudență':'Jurisprudență','prescripție':'prescripție','p.4somație':'p.4 somație','dobândăîntreprofesioniști':'dobândă între profesioniști','înainteasinistrului':'înaintea sinistrului','dreptistoric':'drept istoric','costuricon':'costuri con','condițiilesomației':'condițiile somației','art.4laPDFp.35':'art.4 la PDF p.35','condițiipe':'condiții pe','înacelași':'în același','clauza1000K':'clauza 1000K','clauza1242K':'clauza 1242K','clauza3031K':'clauza 3031K','controlB2B':'control B2B','clauzaX18':'clauza X18','stabilitepentru':'stabilite pentru','inițialăde':'inițială de','29din':'29 din','aplicatDONAU':'aplicat DONAU','documenteși':'documente și','relevante.4.775':'relevante. 4.775'}
for path in [p1,p2]:
    t=path.read_text(encoding='utf8')
    for a,b in repls.items():t=t.replace(a,b)
    lines=[]
    for line in t.splitlines():
        # Original excerpts and URLs stay intact; normalize authored prose only.
        chunks=re.split(r'(„[^”]*”|https?://\S+|[a-f0-9]{64})',line)
        for i,ch in enumerate(chunks):
            if ch.startswith(('„','http')) or re.fullmatch('[a-f0-9]{64}',ch):continue
            ch=re.sub(r'(?<=[A-Za-zăâîșțĂÂÎȘȚ])(20\d\d\.\d\d\.\d\d)',r' \1',ch)
            ch=re.sub(r'(20\d\d\.\d\d\.\d\d)(?=[A-Za-zăâîșțĂÂÎȘȚ])',r'\1 ',ch)
            ch=re.sub(r'(?<=[0-9])EUR\b', ' EUR',ch)
            ch=re.sub(r'EUR(?=[A-Za-zăâîșțĂÂÎȘȚ0-9])','EUR ',ch)
            ch=re.sub(r'(?<=[,;:])(?=[A-Za-zăâîșțĂÂÎȘȚ0-9§])',' ',ch)
            ch=re.sub(r'(?<=[A-Za-zăâîșțĂÂÎȘȚ])(?=§)', ' ', ch)
            ch=re.sub(r'§(?=\d)', '§ ', ch)
            ch=re.sub(r'OGH(?=\d)', 'OGH ',ch)
            ch=re.sub(r'(\d)Ob(?=\d)',r'\1 Ob ',ch)
            ch=re.sub(r'(?<=Ob )(?=\d)','',ch)
            ch=re.sub(r'\bID(?=[a-z0-9])','ID ',ch)
            ch=re.sub(r'SHA-256(?=[a-f0-9])','SHA-256 ',ch)
            ch=re.sub(r'(?<=[0-9])pagini\b',' pagini',ch)
            ch=re.sub(r'(?<=[0-9])comunicări\b',' comunicări',ch)
            ch=re.sub(r'(?<=[0-9])pagină\b',' pagină',ch)
            ch=re.sub(r'(?<=[0-9])net\b',' net',ch)
            ch=ch.replace('șiKostenaufstellung','și Kostenaufstellung').replace('înSituație','în Situație').replace('ABSart.','ABS art.').replace('PDFp.','PDF p.').replace('VersVG distinge','VersVG distinge').replace('§§1','§§ 1').replace('§§38','§§ 38').replace('§§99','§§ 99').replace('alin.2ABGB','alin.2 ABGB').replace('regimulUGB','regimul UGB').replace('§36VersVG','§ 36 VersVG').replace('§39VersVG','§ 39 VersVG')
            ch=re.sub(r'\bp\.(?=\d)','p. ',ch)
            ch=re.sub(r'\balin\.(?=\d)','alin. ',ch)
            ch=re.sub(r'\bart\.(?=\d)','art. ',ch)
            ch=re.sub(r'\bpct\.(?=\d)','pct. ',ch)
            chunks[i]=ch
        lines.append(''.join(chunks))
    path.write_text('\n'.join(lines)+'\n',encoding='utf8')
    print(path.name, len(lines),len(t.split()))
