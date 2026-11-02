from lab import *
import os,re,sys,subprocess
assert W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh'
text=(W/'probe_ui.py').read_text()
line=next(s for s in text.splitlines() if s.startswith('candidates=query('))
word="in ('WEvaComparatieBancaForm'"; assert word in line
replacement=line[:line.index(word)]+"in ('WSagaFurnizoriForm','WSagaImportExtrasForm','WSagaSituatieFurnizoriForm') ORDER BY f.classname,m.ad_menu_id) q\")"
text=text.replace(line,replacement)
fixture=W/'a04-r3-roluri-zk';assert not fixture.exists()
py=W/'a04-r3-zk-probe.py';py.write_text(text);os.environ['A09_FIX']=str(W);os.environ['A09_ARTIFACT']=str(fixture)
subprocess.run([sys.executable,str(py)],check=True)
