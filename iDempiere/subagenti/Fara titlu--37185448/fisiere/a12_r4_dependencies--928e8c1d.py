# Décisions de périmètre: les ressources sont affectées à la proposition précise, pas au nom du chapitre seul.
import re
def dep(k,c):
 id=c['id'];txt=c['normative_content']+' '+c['expected_oracle'];roles=[];types=[];local='Reproducere pe sursa, JAR-ul sau cabinetul de probă desemnat; separat de închiderea istorică.';provenance=[]
 def need(tp,who,condition):types.append(tp);roles.append({'responsabil_sursă':who,'condiție_precisă':condition})
 # Distinguish specifically reported physical routes; a request to list a task or to run a unit suite does not require hardware.
 if k=='T328':
  local='În cele 15 ecrane, emulează tastatura/Enter, cod valid repetat, inexistent, ambiguu și ostil. Folosește separat TestScanareCod și TestScanareEcrane cu JAR-ul precis.'
  if id.endswith(('003','004')):need('ÎNCHIDERE_MIXTĂ_HARDWARE','gestionar WMS / laborator','Confirmați cu scaner de tip tastatură conectat: focus/Enter, citire repetată și reacția la cod invalid în ecranele cerute. Simulatorul și bytecode-ul nu confirmă dispozitivul fizic.')
  elif id.endswith('002'):provenance.append('Numărul de câmpuri este verificabil local în DOM/bytecode; testul scanerului fizic este criteriu separat.')
 elif k in ('T40.10','T160.03') and re.search('scan|etichet|tip[aă]ri',txt,re.I):
  local='Testează citirea simulată a codului și redarea șablonului din rolul de gestiune.'
  need('ÎNCHIDERE_MIXTĂ_HARDWARE','laborator WMS','Dacă livrabilul include scaner/imprimantă conectată, reproduce pe dispozitivul configurat și confirmă decodarea etichetei fizice.')
 elif k in ('T335','T336','T338'):
  local='Emulatorul Android, tastatura virtuală, geometriile și API-ul de test sunt verificabile fără telefon real.'
  if re.search('scan|camer|cititor|telefon|accesibil|TalkBack|instala|APK',txt,re.I):need('DISPOZITIV_CONDIȚIONAL','operator WMS / dispozitiv de probă','Pentru porțiunea dispozitiv real/cameră/TalkBack sau distribuție pe telefon, păstrează separat AVD, JVM și hardware. O cerință strict despre semnătură sau manifest nu solicită hardware.')
 if k=='T351':
  local='Adaptorul și allowlist-ul /terminal/locations și /terminal/readers se pot testa cu stub, inclusiv refuz de alt host sau alt verb.'
  need('DECIZIE_DE_ACTIVARE','proprietar','Taskul POS pornește doar la cuvântul proprietarului. Declarația «nu deocamdată» nu este ordin de integrare în producție.')
  if id.endswith('002'):need('CONTRACT_PARTENER_SANDBOX','responsabil POS / furnizor plăți','Pentru autorizarea și reconcilierea terminalului, folosește cont sandbox și terminal simulator Stripe; pentru operarea la casă, un terminal/card de probă. Dovada de la adaptor nu confirmă acceptarea de către furnizor.')
 elif k in ('T22.14','T212.05','T216') and re.search('stripe|card|payout',txt,re.I):
  local='Simulator pentru payment_intent, payout și asociere; nu necesită sume reale.'
  if not re.search('^K-\\d+.*(testul de clas|baza de teste)',txt,re.I):need('CONTRACT_PARTENER_SANDBOX','responsabil integrare plăți','Confirmarea contractului Stripe din sandbox și evenimentul partenerului sunt separate de simulator; nu cere încasare în producție.')
 if k in ('T04.01','T04.02','T04.03','T04.06','T04.10','T31','T219')and re.search('eMAG|curier|platform|partener|contul firmei|datele firmei',txt,re.I):
  local='Contract și fixture partener izolată; testează parse/duplicate/0 scrieri externe.'
  if not re.search('simulator|stub|fără (apel|internet)|allowlist|rute permise',txt,re.I):need('PARTENER_PENTRU_CONFIRMĂRI_REALE','responsabil canal','Recepția efectivă eMAG/curier/platformă necesită contract sandbox/read-only autorizat; importul fișierului și interfața rulează local.')
 if k in ('T01.09','T10','T17','T17.02','T18.04','T136','T224.01','T225.04','T11')and re.search('ANAF|SPV|e-Factura|REGES|OAuth|banc[aă]|consim',txt,re.I):
  local='Testează callback/stări/fișiere cu endpoint simulat; dovezile publice și SDK-ul local sunt distincte de acceptarea serviciului.'
  # Explicitly declared simulated or offline scope remains local even if ANAF is mentioned many times.
  if not re.search('numai pe simulator|doar pe simulator|fără.*apel|mock|simule|simulator.{0,40}fără|stub',txt,re.I) and re.search('conectarea|conecte|transmi|se aduce|desc[aă]rc|autoriz|token|consim|prime[șs]te',txt,re.I):need('IDENTITATE_PARTENER_AUTORIZATĂ','responsabil fiscal/bancar','Acceptarea reală de către SPV/ANAF/REGES/bancă necesită mediu de test/identitate autorizate; replay cu fixtură este deja realizabil.')
 if k in ('T08.03','T08.04','T08.06','T89','T122')and re.search('consultant|proprietar|aviz|confirm|validat',txt,re.I):
  local='Se pot confrunta markerul, textul și trimiterea oficială cu versiunea sursei.'
  need('APROBARE_ISTORICĂ_NOMINALĂ','consultant/proprietar','Dovada datată de aviz nu este substituită de numărarea markerilor sau de o opinie a auditorului.')
 if (k.startswith('T38.')or k in ('T32.08','T32.09','T261','T296','T303','T310','T358','T361','T362','T363','T364','T365','T367','T372','T378','T10.06')) and re.search('mont|instal|deploy|cabinete|dump|tag|imagin',txt,re.I):
  local='Verifică raportul și imaginea/artefactele înregistrate; dacă mai există, inspectează numai citire.'
  need('PROVENIENȚĂ_DEPLOY_ISTORICĂ','proprietar/release manager','Pentru momentul inițial sunt necesare ediția, cabinetul, digestul și actul de montare; o instalare nouă nu dovedește trecutul.')
 if re.search('cont|declara|TVA|impozit|rubric|legal|normativ|model',txt,re.I)and re.search('surse oficiale|verificarea legală online|norm[ăa] legal[ăa] la data|validatorul oficial|DUK.{0,35}(confirm|oficial)|act normativ',txt,re.I):
  local='Validarea XSD/DUK în laborator este posibilă cu versiunea datată a pachetului.'
  if re.search('aviz|depun|recipis|online real|acces real',txt,re.I):need('REFERINȚĂ_FISCALĂ_DATATĂ','responsabil fiscal','Pentru aviz/recepție oficială concretă documentează versiunea, perioada și sursa emitentului; nu atribui XML local o recipisă.')
 if c['kind'] in ('DIRECTIVĂ_DE_METODĂ','OBLIGAȚIE_RECONSTITUITĂ_DIN_ALIAS_NOMINAL') or 'planul taskului auditat' in txt.lower():
  provenance.append('Scorul ori aprobarea inițială necesită actul exact, data și versiunea. Raportul în Git poate fi citit local; dacă lipsește, sursa istorică poate necesita titularul dosarului.')
 return {'classification':'LOCAL_PLUS_'+('+'.join(dict.fromkeys(types))) if types else ('LOCAL_CU_PROVENIENȚĂ_ISTORICĂ'if provenance else 'LOCAL_CORPUS_SAU_LABORATOR'),'local_feasible':local,'external_or_physical_part_only':roles,'historical_provenance_separate':provenance,'requires_external_or_hardware':bool(roles),'do_not_block_local_steps':True,'logic':'Identitate nominală de task, obiectivul criteriului și sursa de prag/acceptare; menționarea unei platforme nu face întreaga fișă externă.'}

