import pathlib,hashlib,json,shutil,difflib,datetime
root=pathlib.Path(r"D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924")
p=root/"01_CANON/00_CANON_NUCLEU.md"
folder=root/"00_STUDIO/audit/G0-CANON-v4/R2_corecturi"
folder.mkdir(exist_ok=False)
raw=p.read_bytes()
old=raw.decode("utf-8")
assert hashlib.sha256(raw).hexdigest()=="243630e9071df7c7ee15cbf9f079fdac69f1d292950daab42cf927f36aa9ab26"
(folder/"00_CANON_inainte.md").write_bytes(raw)
bad="**Proza ?i traducerile (OBS-10):** ingredientele obligatorii sunt ale BD; proza le adapteaz? formei ?i h?r?ii D1. Tran?ele anticipate nu repovestesc deschiderea ?i ac?iunea de zi. Traducerile apar dup? BD-ul propriu ?i deznod?m?ntul rom?nesc."
good="**Proza și traducerile (OBS-10):** ingredientele obligatorii sunt ale BD; proza le adaptează formei și hărții D1. Tranșele anticipate nu repovestesc deschiderea și acțiunea de zi. Traducerile apar după BD-ul propriu și deznodământul românesc."
badrow="| V4-87 | OBS-10, jurnal ?5.6 | proz? ?i traduceri | acceptat: adaptare de form? ?i protejarea surprizei | ?12 | Studio, D1, D3?D6 | G1 |"
goodrow="| V4-87 | OBS-10, jurnal §5.6 | proză și traduceri | acceptat: adaptare de formă și protejarea surprizei | §12 | Studio, D1, D3–D6 | G1 |"
assert old.count(bad)==old.count(badrow)==1
assert bad.count("?")+badrow.count("?")==20
new=old.replace(bad,good).replace(badrow,goodrow)
new=new.replace("# DRACULA · NUCLEUL CANONIC (v4.2, 24.09.2026)","# DRACULA · NUCLEUL CANONIC (v4.3, 24.09.2026)",1)
prefix="> **Versiunea:** v4.2 · 24.09.2026 ·"
assert new.count(prefix)==1
new=new.replace(prefix,"> **Versiunea:** v4.3 · 24.09.2026 · corectura R2 a celor 20 de caractere deteriorate din OBS-10/V4-87, fără schimbare de sens; dovezi în `00_STUDIO/audit/G0-CANON-v4/R2_corecturi/`. Auditul R2 al v4.2: 8,50/8,50/8,50, FAIL; urmează R3. Istoricul v4.2:",1)
p.write_bytes(new.encode("utf-8"))
after=hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copy2(p,folder/"00_CANON_predat.md")
diff="".join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile="v4.2",tofile="v4.3"))
(folder/"diferente.patch").write_text(diff,encoding="utf-8")
check={'data':datetime.datetime.now().astimezone().isoformat(),'inainte':hashlib.sha256(raw).hexdigest(),'dupa':after,'caractere_reparate':20,'pasaje_reparate':2,'utf8_valid':True,'sens_schimbat':False,'marcaje_inlocuite':old.count(bad)+old.count(badrow),'rest_continut_neschimbat':new.replace(good,bad).replace(goodrow,badrow).splitlines()[5:]==old.splitlines()[5:]}
assert check['rest_continut_neschimbat']
(folder/"rezultat.json").write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding="utf-8")
plan=root/"00_STUDIO/audit/G0-CANON-v4/R2_plan_masuri.md"
with plan.open("a",encoding="utf-8") as f:
    f.write("\n### Rezultatul corecturii\n\nM2.1: copie exactă înainte în R2_corecturi/00_CANON_inainte.md. M2.2: 20 de caractere reparate în cele două pasaje; UTF-8 valid; comparația inversă confirmă restul conținutului neschimbat, exceptând antetul versiunii. M2.3: v4.3 predată, SHA-256 `"+after+"`; autorul Studio primește referința pentru aliniere. M2.4: în așteptarea noului complet. Dovezi: R2_corecturi/rezultat.json și diferente.patch. Nicio notă nouă nu este acordată de autor.\n")
print(json.dumps(check,ensure_ascii=False))

