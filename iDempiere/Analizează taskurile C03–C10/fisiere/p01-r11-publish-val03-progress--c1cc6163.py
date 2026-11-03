from pathlib import Path
import datetime
import hashlib
import json
import re

root = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
folder = root/'executie/R11_fisiere'
hash_file = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
ref = lambda p:{'path':p.relative_to(root).as_posix(),'sha256':hash_file(p)}
verdict = folder/'A11/Verdict_A11_R11_val03_v1.json'
assert hash_file(verdict) == '95593bbc0888f0963ae25c7cb93077565749be3ee75c5320702f7ef910219d57'
received = read(verdict)
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
checkpoint = '''<section id="r11-val03"><h2>Recepția valului 03 — progres confirmat independent</h2>
<p><strong>A11 a recepționat valul 03.</strong> Registrul păstrează 6.709 fișiere, 652 de taskuri și 2.619 criterii. Sunt acum 95 de fișiere cu exerciții parțiale și 20 de criterii cu observații directe în șase taskuri. Creșterea față de valul 02 este de trei fișiere și opt legături parțiale pentru T58. Niciun fișier, task sau flux complet nu primește recepție integrală prin acest val.</p>
<p>Verificarea independentă a refăcut 809 hashuri și 7.114 trimiteri la dovezi. Toate cele 17 contracte de flux rămân deschise. Nota 10/10 aparține planului aprobat. <a href="executie/R11_fisiere/A11/Verdict_A11_R11_val03_v1.json">Verdict A11</a> · <a href="executie/R11_fisiere/A12/Val_03/index.html">Registrul și checklistul valului 03</a></p>
<p>A11 a corectat interpretarea testelor: un program cu 20 de teste omise nu demonstrează funcționarea; numărătorile istorice includ evenimente de subtest; izolarea Node V10 are o limită UDP și o selecție pe markeri. Limitele sunt consemnate, iar probele istorice sunt păstrate. Loturile frontend/backend noi folosesc un adaptor care refuză orice subproces.</p></section>'''
progress = '''<section id="r11-triaj-fixture"><h2>Verificări suplimentare frontend, UX și backend</h2>
<p>Am separat erorile de mediu ale testelor de problemele aplicației. Au fost folosite sursele originale, manifeste de teme din Git, utilizatori și cataloage sintetice. Rapoartele noi se recepționează separat și nu măresc automat acoperirea nominală de mai sus.</p>
<table><thead><tr><th>Zona verificată</th><th>Rezultat și implicație</th></tr></thead><tbody>
<tr><td>Administrare teme</td><td>Cele cinci erori de pregătire sunt explicate de registrul local lipsă. Cu o configurație sintetică explicită, cele cinci teste părinte și 20 de subteste trec; tema necunoscută este refuzată.</td></tr>
<tr><td>Import SAGA și proxy de procese</td><td>Contextul valid de utilizator și firma selectată explică zece eșecuri SAGA și testul de proxy. Fără token sau cu utilizator invalid se refuză accesul înainte de proxy. Un test SAGA cere încă /webui/, deși cardul actual deschide /app/remote; navigarea nativă completă rămâne de verificat.</td></tr>
<tr><td>Pagini de magazin</td><td>Trei programe originale trec pe configurație sintetică. Temele de eveniment și sezon verifică 144 de răspunsuri de pagină. Galeria cere minimum două imagini; testul nu dovedește traducerile reale, execuția JavaScript a magazinului sau comanda ERP.</td></tr>
<tr><td>Ajutor contextual</td><td><strong>16 din 70 de rute statice randate nu au articol dedicat.</strong> Browserul confirmă că apare ajutorul general existent. Sunt afectate inclusiv pagini de import, fiscalitate și salarizare. Recomandarea este completarea dicționarului actual și a legăturilor spre funcțiile native iDempiere.</td></tr>
<tr><td>Opt suite backend suplimentare</td><td>105 teste originale trec: trasabilitate contabilă, active și valută, bancă, sold partener, planificator bancar, jurnal/documente, ajutor și rute de cabinet. Sunt teste de componentă cu limite explicite pentru SQLite și dublurile ERP. Include cele 29 de teste ale suitei T32 L6j care lipsea din recepția T58.</td></tr>
</tbody></table>
<p><a href="executie/R11_fisiere/Triaj_fixture_UI_Val03/Raport_triaj_UI_config.json">Probe și limite UI</a> · <a href="executie/R11_fisiere/Triaj_fixture_UI_Val03/Proba_help_browser_v2.json">Cele 16 rute și martorii în browser</a> · <a href="executie/R11_fisiere/Backend_extindere_Val04/Raport_8_suite_backend.json">Cele opt suite backend</a> · <a href="executie/R11_fisiere/Triaj_fixture_UI_Val03/Erata_metoda_V12_V13.json">Corecția descrierii mediului de test</a></p>
<p>Continuă separat verificarea HR pe PostgreSQL sintetic și aprofundarea traseului nativ al rețetelor WMS. Stația fizică nu condiționează auditul codului. Sistemele operaționale sunt accesate numai pentru citire.</p></section>'''
for name in ['Raport_audit.html','Audit_C03.html','Audit_C10.html']:
    p = root/name
    text = p.read_text(encoding='utf8')
    text = re.sub(r'<!--r11-checkpoint-->.*?<!--end-r11-checkpoint-->','',text,flags=re.S)
    text = re.sub(r'<!--r11-val03-progress-->.*?<!--end-r11-val03-progress-->','',text,flags=re.S)
    marker = '<!--end-r11-lot-curent-->' if name == 'Raport_audit.html' else '<!--end-actualizare-r11-capitol-->'
    assert text.count(marker) == 1
    text = text.replace(marker,marker+'<!--r11-val03-progress-->'+checkpoint+progress+'<!--end-r11-val03-progress-->')
    text = text.replace('1.062 cazuri trecute','1.062 evenimente pytest trecute')
    p.write_text(text,encoding='utf8')

handoff = folder/'A12/Val_03/Handoff_val_03.json'
checklist = folder/'A12/Val_03/Checklist_val03.json'
supplements = [folder/'Triaj_fixture_UI_Val03/Raport_triaj_UI_config.json',folder/'Backend_extindere_Val04/Raport_8_suite_backend.json']
for name in ['Stare_continuare_audit.json','Runda_11_stare.json']:
    p = root/name
    state = read(p)
    state['utc'] = utc
    state['last_independent_checkpoint'] = {'utc':received['utc'],'verdict':verdict.relative_to(root).as_posix(),'verdict_sha256':hash_file(verdict),'checklist':checklist.relative_to(root).as_posix(),'checklist_sha256':hash_file(checklist),'state':'RECEPȚIE VAL_03 PARȚIALĂ; AUDIT INTEGRAL ÎN CURS','counts':received['counts'],'whole_execution_grade':None,'product_grade':None}
    state['current_nominal_handoff'] = ref(handoff)
    state['latest_population_delta'] = ref(root/'executie/delta/2026-11-02T22-21-42-843Z/Comparatie_ultimul_checkpoint.json')
    state['supplements_pending_independent_or_nominal_reception'] = [ref(p) for p in supplements]
    if 'next_round' in state:
        state['next_round']['stage'] = 'Val_03 recepționat parțial; UI V12, backend V13 și HR/WMS se primesc în suplimente distincte.'
        state['next_round']['A12_current'] = handoff.relative_to(root).as_posix()
        state['next_round']['harness_note'] = 'A11 N02: evenimentele de subtest se numără separat; 20 skipped nu au credit; Node V10 are limite UDP și markeri. V12/V13 refuză orice subprocess; erata de metodă este separată.'
    p.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8')
print('Publicarea curentă reflectă Val_03; suplimentele sunt delimitate.')
