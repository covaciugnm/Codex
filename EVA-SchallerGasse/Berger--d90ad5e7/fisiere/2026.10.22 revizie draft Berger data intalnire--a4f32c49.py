import pathlib,json,hashlib,datetime,sqlite3
from email.message import EmailMessage
from email.policy import SMTP
r=pathlib.Path.cwd(); base=r/"folder map"
d=json.loads("{\"id\":\"1d170c83-0a92-4af5-bcc2-b4ee68aeca23\",\"kind\":\"reply\",\"source\":\"chatgpt\",\"status\":\"pending\",\"account_id\":\"476c2aa5-b01c-48d1-9647-4e8b4be4ad61\",\"account_email\":\"office@ac-wohnart.at\",\"to\":[\"office@bmberger.at\"],\"cc\":[],\"bcc\":[],\"subject\":\"Re: AW: Schallergasse 35 – Erinnerung: Rückmeldung zu unserem Vertragsvorschlag\",\"body\":\"Sehr geehrter Herr Berger,\\n\\nvielen Dank für Ihre Rückmeldung. Selbstverständlich können Sie sich über das Wochenende Zeit nehmen, um die Unterlagen in Ruhe zu prüfen.\\n\\nWir freuen uns darauf, Sie persönlich zu treffen und unser Projekt sowie die offenen Punkte gemeinsam zu besprechen.\\n\\nGerne schlagen wir dafür Freitag, den 2026.10.30, für ein Treffen in Wien vor. Würde Ihnen dieser Tag passen? Bitte teilen Sie uns mit, welche Uhrzeit für Sie günstig wäre.\\n\\nMit freundlichen Grüßen\\n\\nCosmin Adrian Covaciu\",\"attachments\":[],\"reply_to_email_id\":\"da60edd5-98cd-4455-a66f-efbd8a61967f\",\"created_at\":\"2026-10-22T09:34:23.062746Z\",\"updated_at\":\"2026-10-22T10:28:52.096518Z\",\"note\":\"Salvată în EVA → Drafts; trimiterea se face din EVA.\"}")
assert "2026.10.30" in d["body"]
out=r/"08. Corespondenta/2026.10.22 Berger - preluare separata si draft intalnire"
changed=[]
def save(p,t):
 p.write_text(t,encoding="utf-8");changed.append(p)
save(out/"2026.10.22 DRAFT Berger intalnire v2.json",json.dumps(d,ensure_ascii=False,indent=2))
head=f"Data: 2026.10.22\nStatut: DRAFT NETRIMIS\nExpeditor: {d['account_email']}\nDestinatari: {', '.join(d['to'])}\nCC: {', '.join(d['cc'])}\nID Eva-Mail: {d['id']}\nSubiect: {d['subject']}\nAtasamente: niciunul\n\n"
save(out/"2026.10.22 DRAFT Berger intalnire v2.txt",head+d["body"])
m=EmailMessage(policy=SMTP);m["From"]=d["account_email"];m["To"]=", ".join(d["to"]);m["Subject"]=d["subject"];m["X-Unsent"]="1";m["X-Eva-Draft-ID"]=d["id"];m.set_content(d["body"])
p=out/"2026.10.22 DRAFT Berger intalnire v2 NETRIMIS.eml";p.write_bytes(m.as_bytes());changed.append(p)
note=f"""2026.10.22 — BERGER, revizie draft v2
Status scurt: acelasi draft EVA {d['id']} actualizat si recitit: propunere intalnire la Viena vineri 2026.10.30; cere ora potrivita. DRAFT NETRIMIS; data neconfirmata.
Ultimul raspuns: PRIMIT 2026.10.21, ID da60edd5-98cd-4455-a66f-efbd8a61967f, solicita analiza peste weekend. Fara raspuns nou verificat.
Urmatorul pas: trimiterea draftului si obtinerea confirmarii datei/orei de la Berger.
Sursa: {out.relative_to(r).as_posix()}/2026.10.22 DRAFT Berger intalnire v2.json; instructiunea utilizatorului.
Versiunea v2 inlocuieste textul draftului anterior; fisierele v1 raman istoric.
"""
for rel in ["2026.10.22 Log progres proiect.txt","08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri/2026.10.22 Log discutii - Markus Berger.txt","2026.09.30 Status proiect.txt","folder map/README.md"]:
 p=r/rel;save(p,note+"\nISTORIC PASTRAT\n\n"+p.read_text(encoding="utf-8-sig"))
rows=json.loads((base/"inventar.json").read_text(encoding="utf-8-sig"));by={x["cale"]:x for x in rows}
db=sqlite3.connect(base/"cautare.sqlite")
for p in changed:
 if p.parent==base:continue
 rel=p.relative_to(r).as_posix();b=p.read_bytes();h=hashlib.sha256(b).hexdigest();tx=p.read_text(encoding="utf-8");cache=base/"texte"/(h+".txt");cache.write_text(tx,encoding="utf-8")
 row=by.get(rel,{});st=p.stat()
 row.update(cale=rel,folder=p.parent.relative_to(r).as_posix(),extensie=p.suffix,octeti=len(b),modificat=datetime.datetime.fromtimestamp(st.st_mtime).isoformat(),modificat_ns=st.st_mtime_ns,sha256=h,duplicat_al="",ce_reprezinta="BERGER — draft si jurnal actualizat",baza_descrierii="actualizare punctuala verificata",extras_continut=tx[:1800],stare_citire="text citit",text_cache=cache.relative_to(r).as_posix(),detalii={},rezumat_verificat="2026.10.22: draft NETRIMIS; intalnire propusa 2026.10.30 la Viena, neconfirmata.",ocr_cache="")
 if rel not in by:rows.append(row);by[rel]=row
 db.execute("DELETE FROM documente WHERE cale=?",(rel,));db.execute("INSERT INTO documente VALUES (?,?,?,?)",(rel,row["ce_reprezinta"],tx,h))
db.commit();db.close()
(base/"inventar.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
print("Draft v2 arhivat; jurnale, inventar.json si cautare.sqlite actualizate.")

