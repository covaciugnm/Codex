from pathlib import Path
import a12_r8_jvm as j
from concurrent.futures import ThreadPoolExecutor
import json
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');stage=B/'executie/R10_pregatire/A12/R10_documentar_supliment';stage.mkdir(exist_ok=True);j.J=stage/'jvm';j.J.mkdir(exist_ok=True);j.T8=Path('D:/CodexWork/a12-r10-doc-jvm');j.T8.mkdir(exist_ok=True)
with ThreadPoolExecutor(max_workers=2)as ex: rows=list(ex.map(j.go,[(t,'TestT35Cadru') for t in ['git','instalat']]))
(stage/'JVM_T35Cadru.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');print([(z['target'],z['exit'],z['traced'])for z in rows])
