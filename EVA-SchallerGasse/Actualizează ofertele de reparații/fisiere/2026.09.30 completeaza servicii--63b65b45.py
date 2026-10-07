from pathlib import Path
import json
P=Path(__file__).parent/'2026.09.30 statusuri verificate.json';s=json.loads(P.read_text(encoding='utf-8'))
def add(n,t,a,ids):s[n]={'status':t,'urmatorul_pas':a,'surse':ids}
s['Attensam']['status']='2026.09.03: confirma trecerea contractelor de deratizare si deszapezire pe A&C. Factura de iarna 34642: 653,12 EUR brut; debit bancar verificat 640,06 EUR la 2026.09.28, referinta R.34642/1088117, cu scont 2%. Separat, la 2026.09.16 Attensam cere dovada platii facturii 34648. Plata 34642 nu stinge automat factura 34648.'
s['Attensam']['urmatorul_pas']='Confirmarea alocarii platii de 640,06 EUR la factura 34642 si clarificarea facturii distincte 34648. Scontul de iarna avea termen 2026.09.30, plata integrala 2026.10.15 potrivit scrisorii primite.'
s['Attensam']['surse']+=['390ca184-c598-408e-b40f-45a9b928c7fb','a1e505fd-1be0-439b-9c4c-081764a0107a','10. Banci + Extrase de cont/Facturi achitate/03 - 2026-09-28 ATTENSAM Rechnung 34642 - BEZAHLT 640,06 EUR (mit Skonto) - A&C AT22 - Buchung 1471264511.pdf']
s['Weigl']['status']+=' 2026.09.23: beneficiarul a trimis planul parterului P2041 si un detaliu marit, cu cerinte tehnice; solicita oferta pana la 2026.10.20.'
s['Weigl']['urmatorul_pas']='Urmarirea ofertei pana la termenul cerut 2026.10.20; confirmarea primirii planurilor si completarea sectiunilor/cotelor daca sunt cerute.'
s['Weigl']['surse']+=['4ec85789-b4b3-4339-9be3-5a4ffeed0670']
for n,id in [('Pech','7dd1b621-7f4c-4438-997c-787b92f3f002'),('Paknehad','5e0b3425-12fe-4135-b022-cae619c3bca5')]:
 s[n]['status']+=' 2026.09.29: cerere separata Bauwerksbuch trimisa, cu raspuns solicitat pana la 2026.10.12; raspuns nou neidentificat.'
 s[n]['urmatorul_pas']+=' Urmarirea cererii Bauwerksbuch la 2026.10.12.'
 s[n]['surse'].append(id)
add('Donau Versicherung','2026.07.20: retrimite raspunsul din 2026.07.10; asiguratorul afirma lipsa acoperirii din cauza restantelor si anunta solutionarea separata a ajustarii politei 2044001194. 2026.07.14: posibila excludere a riscurilor apa/chirie, conditionata de autorizatie, descrierea lucrarilor si confirmarea instalatorului. Nu este identificata confirmarea reinstaurarii acoperirii.','Prioritar: confirmare scrisa a acoperirii actuale, solutionarea ajustarii si reconcilierea somatiei de 3.734,34 EUR cu dosarul Commerz-Inkasso/Maritczak; evitarea dublei plati a aceleiasi prime.',['1bc16469-dcb3-4cf3-819a-9a75f081bbc1','d10bdd3f-8439-45f0-a061-e222c9290266','b487e95f-8a9f-4865-9836-ae95481ce360'])
add('Maritczak - Commerz Inkasso','2026.09.15: beneficiar trimite cerere documente si prelungire termen pentru dosarul 2616052 / Donau 2044001194, suma solicitata 3.734,34 EUR. Termenul din somatie era 2026.09.21; prelungirea nu este confirmata.','Urmarirea raspunsului si a dosarului justificativ, corelat cu asiguratorul si consultantul juridic.',['b487e95f-8a9f-4865-9836-ae95481ce360'])
add('KSV1870','2026.07.05: confirma luarea in evidenta a contestatiei integrale pentru dosarul 20260504299, oprirea urmaririi extrajudiciare si nepublicarea cazului in informatiile KSV; asteapta pozitia creditorului. Nu este confirmare de anulare a creantei.','Pastrarea contestatiei si urmarirea raspunsului creditorului; dosar distinct de somatia Donau/Commerz-Inkasso.',['82948df8-e296-41c4-b04e-b70ed9f4006e'])
add('MA29 - Geologie','2026.07.09: explica accesul la profilele geologice prin webshop, 7,20 EUR/profil; confirmare comanda 712819 pentru trei profile, total 21,60 EUR.','Pastrarea profilelor si transmiterea lor proiectantului structurii; datele disponibile nu inlocuiesc investigatiile specifice cerute de proiectant.',['56293993-e651-4183-8a80-03682cd16329','542c3e30-b7bb-4c96-afff-10dc33f371b7'])
P.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8');print(len(s))
