import pathlib,json,hashlib,shutil
from email.message import EmailMessage
from email.policy import SMTP
r=pathlib.Path.cwd()
data=json.loads("{\"draft\":{\"id\":\"1d170c83-0a92-4af5-bcc2-b4ee68aeca23\",\"kind\":\"reply\",\"source\":\"chatgpt\",\"status\":\"pending\",\"account_id\":\"476c2aa5-b01c-48d1-9647-4e8b4be4ad61\",\"account_email\":\"office@ac-wohnart.at\",\"to\":[\"office@bmberger.at\"],\"cc\":[],\"bcc\":[],\"subject\":\"Re: AW: Schallergasse 35 – Erinnerung: Rückmeldung zu unserem Vertragsvorschlag\",\"body\":\"Sehr geehrter Herr Berger,\\n\\nvielen Dank für Ihre Rückmeldung. Selbstverständlich können Sie sich über das Wochenende Zeit nehmen, um die Unterlagen in Ruhe zu prüfen.\\n\\nWir freuen uns darauf, Sie möglichst bald danach persönlich zu treffen und unser Projekt sowie die offenen Punkte gemeinsam zu besprechen. Bitte lassen Sie uns wissen, welcher Termin Ihnen dafür gut passen würde.\\n\\nMit freundlichen Grüßen\\n\\nCosmin Adrian Covaciu\",\"attachments\":[],\"reply_to_email_id\":\"da60edd5-98cd-4455-a66f-efbd8a61967f\",\"created_at\":\"2026-10-22T09:34:23.062746Z\",\"updated_at\":\"2026-10-22T09:34:23.062746Z\",\"note\":\"Salvată în EVA → Drafts; trimiterea se face din EVA.\"},\"received\":{\"id\":\"da60edd5-98cd-4455-a66f-efbd8a61967f\",\"account_email\":\"office@ac-wohnart.at\",\"subject\":\"AW: Schallergasse 35 – Erinnerung: Rückmeldung zu unserem Vertragsvorschlag\",\"from_name\":\"Markus Berger\",\"from_address\":\"office@bmberger.at\",\"to\":[\"office@ac-wohnart.at\"],\"cc\":[],\"received_at\":\"2026-10-21T15:00:31Z\",\"text\":\"Sehr geehrter Herr Covaciu,\\r\\nGerne bestätige ich den Erhalt der E-Mails von letzter Woche. Leider war ich bis dato mit anderen Projekten stark ausgelastet, jetzt kann ich mich Ihrem wieder gerne widmen.\\r\\nBitte geben Sie mir noch das Wochenende, um die Unterlagen zu sichten. Dann können wir gerne einen Termin vereinbaren.\\r\\n\\r\\n\\r\\nBei Rückfragen stehe ich Ihnen gerne zur Verfügung.\\r\\n\\r\\nMit freundlichen Grüßen\\r\\nMarkus Berger\\r\\n\\r\\n-------------------------------------------------------------------\\r\\nBmstr. Dipl.-Ing. (FH) Markus Berger GmbH\\r\\nIngenieurkonsulent für Bauingenieurwesen rB.\\r\\nSchönbrunner Straße 123 / 2\\r\\n\\r\\nA - 1050 Wien\\r\\n\\r\\nTel.: +43-1-78 64 614\\r\\n\\r\\nMobil: +43-664-283 0 933\\r\\n\\r\\nE-Mail: office@bmberger.at<mailto:office@bmberger.at>\\r\\n\\r\\n\\r\\n\\r\\n________________________________\\r\\nVon: office@ac-wohnart.at <office@ac-wohnart.at>\\r\\nGesendet: Dienstag, 20. Oktober 2026 15:39\\r\\nAn: Markus Berger <office@bmberger.at>\\r\\nBetreff: Schallergasse 35 – Erinnerung: Rückmeldung zu unserem Vertragsvorschlag\\r\\n\\r\\n\\r\\nSehr geehrter Herr Berger,\\r\\n\\r\\nwir möchten höflich an unsere E-Mail vom 13. Oktober 2026 und den übermittelten Vertragsvorschlag für das Projekt Schallergasse 35, 1120 Wien, erinnern.\\r\\n\\r\\nBitte bestätigen Sie uns kurz, ob unsere E-Mail und sämtliche PDF-Anlagen vollständig bei Ihnen eingegangen sind.\\r\\n\\r\\nWir möchten die offenen Punkte gerne mit Ihnen abstimmen und anschließend die Unterzeichnung des Vertrags vorbereiten.\\r\\n\\r\\nDürfen wir Sie daher um Ihre schriftliche Stellungnahme zu unserem Vertragsvorschlag bitten?\\r\\n\\r\\nFalls Sie Anmerkungen, Einwände oder Änderungswünsche haben, teilen Sie uns diese bitte möglichst unter Angabe der betreffenden Vertragsstelle und Ihres konkreten Formulierungsvorschlags mit.\\r\\n\\r\\nSollten Sie keine Einwände haben, freuen wir uns über eine entsprechende schriftliche Rückmeldung.\\r\\n\\r\\nBitte berücksichtigen Sie auch den erbetenen Leistungs- und Rechnungsplan mit den wesentlichen Etappen, Terminen und zugehörigen Beträgen, den wir gemeinsam abstimmen und als Vertragsanlage beifügen möchten.\\r\\n\\r\\nBitte teilen Sie uns außerdem mit, bis wann wir mit Ihrer inhaltlichen Rückmeldung rechnen dürfen.\\r\\n\\r\\nZur leichteren Zuordnung fügen wir den Vertragsvorschlag und Ihr ursprüngliches Angebot nochmals unverändert als PDF bei.\\r\\n\\r\\nVielen Dank für Ihre Zeit und die Prüfung unserer Unterlagen.\\r\\n\\r\\nMit freundlichen Grüßen\\r\\n\\r\\nCosmin Adrian Covaciu\\r\\n\",\"truncated\":false,\"labels\":[\"1: To respond\",\"99: Important\"],\"category\":\"fyi\",\"folder\":\"Markus Berger\",\"thread_id\":\"<VI1P193MB06551AB31DFC88D259D71D5BCB662@VI1P193MB0655.EURP193.PROD.OUTLOOK.COM>\",\"is_read\":false,\"is_sent\":false,\"attachments\":[],\"note\":\"\"},\"source\":{\"id\":\"01a0f6eb-c105-7760-973e-241d6f6be8c1\",\"title\":\"Berger&Pech\"}}")
out=r/"08. Corespondenta/2026.10.22 Berger - preluare separata si draft intalnire"
out.mkdir(exist_ok=True)
d=data["draft"]; e=data["received"]
(out/"2026.10.22 Dovezi EVA si sursa conversatie.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
header=f"Data: 2026.10.22\nStatut: DRAFT NETRIMIS\nExpeditor: {d['account_email']}\nDestinatari: {', '.join(d['to'])}\nCC: {', '.join(d['cc'])}\nID Eva-Mail: {d['id']}\nSubiect: {d['subject']}\nAtasamente: niciunul\n\n"
(out/"2026.10.22 DRAFT Berger intalnire.txt").write_text(header+d["body"],encoding="utf-8")
m=EmailMessage(policy=SMTP);m["From"]=d["account_email"];m["To"]=", ".join(d["to"]);m["Subject"]=d["subject"];m["X-Unsent"]="1";m["X-Eva-Draft-ID"]=d["id"];m.set_content(d["body"])
(out/"2026.10.22 DRAFT Berger intalnire NETRIMIS.eml").write_bytes(m.as_bytes())
src=r/"08. Corespondenta/2026.10.22 Verificare zilnica/2026.10.21 18-00-31 PRIMIT Markus Berger da60edd5.txt"
shutil.copy2(src,out/src.name)
inv=json.loads((r/"folder map/inventar.json").read_text(encoding="utf-8-sig"))
base=r/"00.Proiect/09. Vertraege/bmberger.at/2026.10.13 Werkvertrag R09"
refs=[]
for name in ["2026.10.13 Anlage 5 Originalangebot BERGER 2026.08.17.pdf","2026.10.13 Werkvertrag BERGER R09.pdf"]:
 p=base/name;h=hashlib.sha256(p.read_bytes()).hexdigest()
 rows=[x for x in inv if x["cale"]==p.relative_to(r).as_posix()]
 match=bool(rows and rows[0]["sha256"]==h)
 shutil.copy2(p,out/("2026.10.22 "+name[11:]))
 refs.append({"sursa":str(p.relative_to(r)),"sha256":h,"identic_index":match})
(out/"2026.10.22 Surse oferta Berger.json").write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding="utf-8")
note=f"""2026.10.22 — BERGER, preluare separata din conversatia Berger&Pech
Conversatie sursa: 01a0f6eb-c105-7760-973e-241d6f6be8c1; conversatie curenta: Berger, 01a162f3-09dc-7422-872d-06cdd90ad5e7.
Status scurt: oferta originala 2026.08.17 si propunerea contractuala R09 preluate separat ca copii nemodificate. Oferta/propunerea nu sunt contract acceptat. Draft cordial de raspuns salvat in EVA, NETRIMIS, ID {d['id']}.
Ultimul raspuns: PRIMIT 2026.10.21, Markus Berger confirma primirea emailurilor si solicita timp peste weekend pentru analiza; ID da60edd5-98cd-4455-a66f-efbd8a61967f.
Urmatorul pas: revizuirea/trimiterea draftului din EVA, apoi stabilirea intalnirii cat mai curand dupa analiza; data intalnirii ramane nefixata.
Sursa: {out.relative_to(r).as_posix()}/2026.10.22 Dovezi EVA si sursa conversatie.json
Acoperire: recitire punctuala a mesajului indicat si a contextului din Berger&Pech; nu este o verificare noua exhaustiva a inboxului.
"""
(out/"2026.10.22 Preluare Berger si jurnal.txt").write_text(note,encoding="utf-8")
for rel in ["2026.10.22 Log progres proiect.txt","08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.22 Log discutii - Markus Berger.txt","2026.09.30 Status proiect.txt","folder map/README.md"]:
 p=r/rel
 backup=out/("2026.10.22 Istoric "+p.name)
 shutil.copy2(p,backup)
 p.write_text(note+"\nISTORIC PASTRAT\n\n"+p.read_text(encoding="utf-8-sig"),encoding="utf-8")
print(json.dumps({"saved":str(out),"sources":refs},ensure_ascii=False))

