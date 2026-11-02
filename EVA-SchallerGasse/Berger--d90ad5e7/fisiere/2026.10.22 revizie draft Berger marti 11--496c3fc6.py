import pathlib,json
r=pathlib.Path.cwd()
p=r/"folder map/2026.10.22 revizie draft Berger data intalnire.py"
s=p.read_text(encoding="utf-8")
lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith("d=json.loads("): lines[i]="d=json.loads("+repr("{\"id\":\"1d170c83-0a92-4af5-bcc2-b4ee68aeca23\",\"kind\":\"reply\",\"source\":\"chatgpt\",\"status\":\"pending\",\"account_id\":\"476c2aa5-b01c-48d1-9647-4e8b4be4ad61\",\"account_email\":\"office@ac-wohnart.at\",\"to\":[\"office@bmberger.at\"],\"cc\":[],\"bcc\":[],\"subject\":\"Re: AW: Schallergasse 35 – Erinnerung: Rückmeldung zu unserem Vertragsvorschlag\",\"body\":\"Sehr geehrter Herr Berger,\\n\\nvielen Dank für Ihre Rückmeldung. Selbstverständlich können Sie sich über das Wochenende Zeit nehmen, um die Unterlagen in Ruhe zu prüfen.\\n\\nWir freuen uns darauf, Sie persönlich zu treffen und unser Projekt sowie die offenen Punkte gemeinsam zu besprechen.\\n\\nGerne schlagen wir dafür Dienstag, den 2026.10.27, um 11:00 Uhr (Wiener Ortszeit) für ein Treffen in Wien vor. Würde Ihnen dieser Termin passen?\\n\\nMit freundlichen Grüßen\\n\\nCosmin Adrian Covaciu\",\"attachments\":[],\"reply_to_email_id\":\"da60edd5-98cd-4455-a66f-efbd8a61967f\",\"created_at\":\"2026-10-22T09:34:23.062746Z\",\"updated_at\":\"2026-10-22T10:35:57.072927Z\",\"note\":\"Salvată în EVA → Drafts; trimiterea se face din EVA.\"}")+")"
s="\n".join(lines)
s=s.replace("v2","v3").replace("fisierele v1 raman istoric","fisierele v1 si v2 raman istoric").replace("2026.10.30","2026.10.27").replace("vineri 2026.10.27; cere ora potrivita","marti 2026.10.27, ora 11:00 Viena").replace("2026.10.27 la Viena, neconfirmata","2026.10.27 la ora 11:00 Viena, neconfirmata")
assert "2026.10.27" in s
exec(compile(s,"arhivare_v3","exec"))

