from pathlib import Path
import json, hashlib, shutil

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
DATE='2026.10.13'
registry=OUT/f'{DATE} Registru transfer preambul R08.json'
data=json.loads(registry.read_text(encoding='utf-8'))
history=OUT/f'{DATE} Istoric emailuri inainte de formularea politicoasa'
history.mkdir(exist_ok=False)
shutil.copy2(registry,history/registry.name)
for rec in data['operatiuni']:
    path=ROOT/rec['R08_email_source']
    draft=json.loads(path.read_text(encoding='utf-8'))
    shutil.copy2(path,history/path.name)
    greeting='Sehr geehrter Herr Berger,' if rec['provider']=='BERGER' else 'Sehr geehrte Damen und Herren,'
    parts=[greeting,
      'Vielen Dank für Ihre Geduld. Bitte entschuldigen Sie die längere Bearbeitungszeit. Die Fertigstellung hat sich verzögert, da wir auf die abschließende Ausarbeitung und Rückmeldung unserer Rechtsanwälte sowie unseres technischen Teams gewartet haben.',
      'Wir möchten den Vertrag mit Ihnen unterzeichnen und die Zusammenarbeit für unser Projekt Schallergasse 35 gerne aufnehmen. Anbei übermitteln wir Ihnen den von unseren Rechtsanwälten und unserem technischen Team ausgearbeiteten Vertragsvorschlag einschließlich der Anlagen als PDF.',
      *rec['preamble_moved_verbatim'],
      'Wir wären Ihnen sehr dankbar, wenn Sie die Unterlagen in Ruhe prüfen und uns Ihre Anmerkungen schriftlich mitteilen könnten. Für Ihre Hinweise und konstruktiven Vorschläge sind wir selbstverständlich offen.',
      'Sollten Sie einzelne Formulierungen oder Regelungen in der übermittelten Fassung nicht annehmen können, bitten wir Sie freundlich um einen konkreten Gegenvorschlag mit den von Ihnen gewünschten Formulierungen.',
      'Wenn Sie keine Anmerkungen haben, freuen wir uns über Ihre schriftliche Bestätigung. Anschließend möchten wir die beiderseitige Unterzeichnung des Vertrags mit Ihnen abstimmen.',
      'Vielen Dank für Ihre Mühe und die Prüfung unserer Unterlagen. Wir freuen uns auf Ihre Rückmeldung und die weitere Zusammenarbeit.',
      'Mit freundlichen Grüßen']
    draft['body_de']='\n\n'.join(parts)+'\n'
    draft['signature_instruction']='EVA adaugă automat semnătura titularului; corpul se oprește după formula de încheiere.'
    draft['attribution_source']='Instrucțiunea expresă a utilizatorului: propunere primită de la avocații proprii și echipa tehnică; nu este o certificare independentă a autoriei.'
    for p in rec['preamble_moved_verbatim']:assert draft['body_de'].count(p)==1
    other='PECH' if rec['provider']=='BERGER' else 'BERGER'
    assert other.lower() not in draft['body_de'].lower()
    assert 'verhand' not in draft['body_de'].lower()
    path.write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rec['R08_email_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
data['email_latest_instruction']='2026.10.13: Germană foarte politicoasă, intenție de semnare, întârziere datorată finalizării de către avocați și echipa tehnică, deschidere la observații; PDF-uri proprii atașate, drafturi EVA netrimise.'
registry.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','emailuri_actualizate':2,'preambul_integral':True,'contracte_modificate':False},ensure_ascii=False))
