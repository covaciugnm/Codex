from pathlib import Path
import re
O=Path(__file__).parent
p=O/'build_v3.py';s=p.read_text(encoding='utf-8')
def para(prefix,text):
    global s
    pat=r"p\('"+re.escape(prefix)+r"[^\n]*\n"
    s,n=re.subn(pat,lambda m:'p('+repr(text)+')\n',s)
    assert n==1,(prefix,n)
para('PGX/Qwen rămâne','PGX/Qwen rămâne candidat: modelul, licența, capacitatea și costul per 1.000 produse se măsoară în PoC. Modulul ai_assistant nu dovedește disponibilitatea inferenței necesare. Conținutul de produs și încărcările utilizatorilor sunt date nefiabile, niciodată instrucțiuni pentru agent.')
para('Anul 1957','Istoria fabricii, capacitatea, originea și sustenabilitatea cer dovezi. Promisiunea publică privind spargerile se păstrează conform §8.4. Fișa de proveniență nu este numită pașaport digital obligatoriu pentru toată ceramica. [L1, L2, L7]')
para('Baza comercială nu','D02 se completează până în săptămâna 2: 12 luni de vânzări agregate, minimum 8 săptămâni de trafic eligibil, segmente, marjă și retururi. Baseline-ul nu este disponibil în fișierele inspectate; validarea sa precede angajamentul comercial și bugetul final.')
para('Recepția livrabilelor','Recepția verifică livrabilele controlabile. Țintele comerciale sunt ipoteze de testat; sezonalitatea și schimbările de preț/media se controlează separat.')
s=s.replace('Ținte la 90 zile: +10% conversie pentru disponibilitatea asistentului și +10% AOV pentru disponibilitatea configuratorului, măsurate A/B pe utilizatori eligibili. Comparația utilizatorilor care aleg singuri asistentul cu ceilalți este doar descriptivă, afectată de selecție.','La 90 zile: +10% conversie asistent și +10% AOV configurator, A/B pe disponibilitatea funcției. Comparația celor care aleg singuri asistentul cu ceilalți este descriptivă, afectată de selecție.')
s=s.replace('Bifa atestă informarea, nu creează o renunțare la drepturi. [L10]','Bifa atestă informarea, nu creează o renunțare la drepturi. [L10b]')
s=s.replace('90 zile după valul 3; utilizarea','90 zile după valul 3b; utilizarea')
s=s.replace('Pragurile din capitolul 8,','Pragurile din §8.1–8.4,')
p.write_text(s,encoding='utf-8')
p=O/'build_trace_v3.py';s=p.read_text(encoding='utf-8')
for a,b in {'publicitate/fjernsalg':'publicitate/vânzare la distanță','efort360':'efort 360','Configurator2D':'Configurator 2D','configurator2D':'configurator 2D','Cele179':'Cele 179','cele179':'cele 179','și20':'și 20','de50':'de 50','domeniu360':'domeniu 360','WBS360':'WBS 360','calendar26':'calendar 26','de18':'de 18','automat:118':'automat: 118','auditul tehnic:6':'auditul tehnic: 6','tehnic:6':'tehnic: 6','și2 clarificări':'și 2 clarificări','până la500':'până la 500','și10 oportunități':'și 10 oportunități','extindere180':'extindere 180','răspuns1h':'răspuns 1 h','restabilire8h':'restabilire 8 h','RTO60':'RTO 60','RPO15':'RPO 15','peste100%':'peste 100%','zile=29,4%':'zile = 29,4%','fereastra90':'fereastra 90','de26':'de 26','10 produse,20':'10 produse, 20','Reg.1935':'Reg. 1935','regiuni.':'regiuni.','MDE10%':'MDE 10%','putere80%':'putere 80%','alfa5%':'alfa 5%','S4. Etaloane':'S4. Etaloane','val2':'val 2'}.items():s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
p=O/'visuals_v3.py';s=p.read_text(encoding='utf-8').replace("'4 LOCURI'","'ACASĂ'");p.write_text(s,encoding='utf-8')
print('Revizie editorială finală')
