import pathlib,re,json,hashlib,shutil,datetime,difflib
from datetime import date,timedelta
root=pathlib.Path(r"D:\00. Downloads\Dracula Book\DRACULA-COMICS-CODEX-G0-20260924");e=root/"00_STUDIO/audit/G0-STUDIO-v4/R4_corecturi"
manifest=json.loads((e/"manifest.json").read_text(encoding="utf-8"))
# Small typographical cleanup only in newly written strings, no change to meaning.
fixes={"cele8categorii":"cele 8 categorii","regulii11":"regulii 11","regulii4":"regulii 4","regula4":"regula 4","regula11":"regula 11","secțiunea14":"secțiunea 14","regula13":"regula 13","minimum8,20":"minimum 8,20","secțiunile1–16 și20":"secțiunile 1–16 și 20","harta1–20":"harta 1–20","Volumul1":"Volumul 1","Ep.1–5":"Ep. 1–5","120pagini":"120 pagini","PASS Ep.5":"PASS Ep. 5","tehnoredactarea03.02":"tehnoredactarea 03.02","CIP17.02":"CIP 17.02","la19.02":"la 19.02","GT22.02":"GT 22.02","tipar23.02":"tipar 23.02","livrare08.03":"livrare 08.03","Sunt păstrate nouă zile":"Sunt prevăzute nouă zile","cu15decizii":"cu 15 decizii","numărătoarea12:16":"numărătoarea 12:16","și05_TITULARI":"și 05_TITULARI","B22.02":"B 22.02","Ep.5":"Ep. 5","rămâne19.02":"rămâne 19.02","StudioR5":"Studio R5","CanonR2":"Canon R2","StudioR4":"Studio R4","CanonR3":"Canon R3","Cele15decizii":"Cele 15 decizii","Paris1794":"Paris 1794","variantaB":"varianta B","M4.7:":"M4.7:","25briefuri":"25 briefuri","în00_STUDIO":"în 00_STUDIO","Canon:01_CANON":"Canon: 01_CANON","jurnal:00_STUDIO":"jurnal: 00_STUDIO","și03_JURNAL":"și 03_JURNAL","stare(AP-16)":"stare (AP-16)","ținta medie de2runde":"ținta medie de 2 runde","SprintI":"Sprint I","decizia15":"decizia 15","procedurăv5":"procedură v5","anticipăm9,50":"anticipăm 9,50","publicat19.02":"publicat 19.02","focalizate cu limite":"focalizate cu limite"}
for rel in list(manifest["files"])[:3]:
 p=root/rel;t=p.read_text(encoding="utf-8")
 if rel.endswith("S_showrunner.md"):
  a,b=t.split("## Istoric integral până la auditul R4",1)
  for x,y in fixes.items():a=a.replace(x,y)
  t=a+"## Istoric integral până la auditul R4"+b
 else:
  for x,y in fixes.items():t=t.replace(x,y)
 p.write_text(t,encoding="utf-8",newline="")
s=(root/"00_STUDIO/01_ECHIPA_SI_ROADMAP.md").read_text(encoding="utf-8")
j=(root/"00_STUDIO/03_JURNAL_PROGRES.md").read_text(encoding="utf-8")
r=(root/"00_STUDIO/rapoarte/S_showrunner.md").read_text(encoding="utf-8").split("## Istoric integral până la auditul R4")[0]
rows={k:next(l for l in s.splitlines() if l.startswith("| "+k+" |")) for k in ["RS19","RS27","RS28","RS33","GT"]}
checks={}
checks["tren_exclus_locuri"]="Trenurile sunt vehicule" in rows["RS28"] and "Orient Express" not in rows["RS28"] and "Producător după H1" in rows["RS28"]
checks["monument_interior_verificat"]="inclusiv reprezentările din interiorul BD" in rows["RS27"] and "nu dă automat" in rows["RS27"]
checks["hotel_loc_distinct"]="hotelurile sunt locuri" in rows["RS19"]
checks["8_categorii_normative"]=all("hoteluri" not in line for line in s.splitlines() if line.strip().startswith(("- K5: 0 mărci reale","- K4: planșa vehiculelor")))
checks["splash_explicita"]="excepție explicită: p. 4 și alte splash-uri motivate au un panou" in s and "panourile numărate o singură dată" in s
checks["GT_dupa_publicare"]=date(2027,2,19)<date(2027,2,22)<date(2027,2,23)<date(2027,3,8) and "22.02.2027" in rows["GT"]
bd=sum((date(2027,2,23)+timedelta(days=i)).weekday()<5 for i in range(1,(date(2027,3,8)-date(2027,2,23)).days+1))
checks["livrare_9_zile_planificate"]=bd==9 and "08.03.2027" in s
checks["status_referinta_concordant"]=all("b51981121c39953258b32989d85a4239120f85aa8746229736ca605c25f57357" in t for t in [s,j,r]) and "canonul v4.3 este predat" in rows["RS33"]
checks["fara_stare_nepredat_curenta"]="rămâne de sincronizat" not in r and "pregătire R4" not in r
checks["istoric_S_intact"]=(root/"00_STUDIO/rapoarte/S_showrunner.md").read_text(encoding="utf-8").endswith((e/"inainte/00_STUDIO/rapoarte/S_showrunner.md").read_text(encoding="utf-8-sig"))
# All KPI bullets must occur in the same brief after normalizing bullet endings.
def norm(x):return re.sub(r"\s+"," ",x.strip().rstrip(";").rstrip(".").lstrip("- ").strip())
source=set(norm(l) for l in s.splitlines() if re.match(r"\s*-\s*K\d+:",l))
mismatches=[];n=0
for p in (root/"00_STUDIO/02_BRIEFURI").glob("*.md"):
 active=False
 for l in p.read_text(encoding="utf-8").splitlines():
  if l.startswith('## '): active=l.startswith('## KPI')
  if not active: continue
  if re.match(r"\s*-\s*K\d+:",l):
   n+=1
   if norm(l) not in source:mismatches.append({"file":p.name,"KPI":l})
checks["KPI_briefuri_identice"]=not mismatches
tasks=set(norm(l) for l in s.splitlines() if l.startswith('  - ') and not re.match(r'\s*-\s*K\d+:',l))
task_errors=[];task_count=0
for p in (root/'00_STUDIO/02_BRIEFURI').glob('*.md'):
 active=False;in_tasks=False
 for l in p.read_text(encoding='utf-8').splitlines():
  if l.startswith('## '):active=l.startswith('## Sarcini actuale');in_tasks=False
  if active and l.startswith('- **'):in_tasks=l.startswith('- **Sarcini:**')
  if active and in_tasks and l.startswith('  - '):
   task_count+=1
   if norm(l) not in tasks:task_errors.append({'file':p.name,'task':l})
checks['sarcini_briefuri_identice']=not task_errors
result={"date":datetime.datetime.now().astimezone().isoformat(),"checks":checks,"brief_KPI_checked":n,"mismatches":mismatches,"calendar_workdays":bd,"all_pass":all(checks.values()),"scope":"Verificări focalizate R4, nu rerulare integrală V1–V51; evaluarea semantică independentă urmează."}
result['brief_tasks_checked']=task_count
result['task_mismatches']=task_errors
(e/"rezultat.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
for rel,info in manifest["files"].items():
 p=root/rel;info["sha256"]=hashlib.sha256(p.read_bytes()).hexdigest();info["bytes"]=p.stat().st_size;shutil.copy2(p,e/"predat"/rel)
 a=(e/"inainte"/rel).read_text(encoding="utf-8-sig");b=p.read_text(encoding="utf-8")
 (e/"diferente"/(pathlib.Path(rel).name+".patch")).write_text("".join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=rel+"-inainte",tofile=rel+"-dupa")),encoding="utf-8")
manifest["created"]=result["date"]
(e/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=True))
