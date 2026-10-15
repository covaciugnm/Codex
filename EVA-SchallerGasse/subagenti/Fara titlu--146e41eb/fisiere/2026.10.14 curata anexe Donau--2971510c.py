from pathlib import Path
import re
d=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
for file in ['2026.10.14 Cerere documente Donau NETRIMIS.txt','2026.10.14 Registru documente necesare.txt']:
 p=d/file;t=p.read_text(encoding='utf8')
 for a,b in {'ciorna2026':'ciorna 2026','ab2026':'ab 2026','Ablauf2036':'Ablauf 2036','vom2026':'vom 2026','Rahmenvereinbarung290':'Rahmenvereinbarung 290','ABS1000A':'ABS 1000A','Fassung2018':'Fassung 2018','Art.4.5':'Art. 4.5','§91':'§ 91','§§39,39a und91VersVG':'§§ 39, 39a und 91 VersVG','§39Abs.4VersVG':'§ 39 Abs. 4 VersVG','Zahlungsfrist2026':'Zahlungsfrist 2026','am2026':'am 2026','genannten5.326':'genannten 5.326','Quartalsprämie1.591':'Quartalsprämie 1.591','die30EURGläubigerkosten':'die 30 EUR Gläubigerkosten','Zusatzdeckungen1242K und3031K':'Zusatzdeckungen 1242K und 3031K','nach1000K':'nach 1000K','Ablaufs2036':'Ablaufs 2036','§ 91VersVG':'§ 91 VersVG','5.326,15EUR':'5.326,15 EUR','1.591,81EUR':'1.591,81 EUR','portal2026':'portal 2026','la2026':'la 2026','Temeiul1000K':'Temeiul 1000K','§70':'§ 70','§106':'§ 106','dela2026':'de la 2026','de la2026':'de la 2026','explicația§91':'explicația § 91','Imediat:5–9 și14':'Imediat: 5–9 și 14','paralel1–4 și11–12':'paralel 1–4 și 11–12',';13':' ; 13','și10':'și 10','Commerz2026':'Commerz 2026','riscului§':'riscului §','§5c':'§ 5c','Notificări§':'Notificări §','Temeiul1000K':'Temeiul 1000K'}.items():t=t.replace(a,b)
 t=re.sub(r'(?<=\d)VersVG',' VersVG',t)
 p.write_text(t,encoding='utf8')
 print(file)
