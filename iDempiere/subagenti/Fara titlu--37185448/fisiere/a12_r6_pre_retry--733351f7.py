from a12_r6_exec import *
from pathlib import Path
src=Path(__file__).parent/'a12_r6_mutations.py';s=src.read_text(encoding='utf8')
s=s.replace("[sys.executable,'-I',str(h(2))","[sys.executable,'-X','utf8','-I',str(h(2))").replace("cp,'TestT204Ecrane'","cp,'com.eva.ro.contab.form.TestT204Ecrane'").replace("_T204.log'","_T204_valid.log'").replace("'Mutanti_T204.json'","'Mutanti_T204_valid.json'").replace("'Probe_istorice.json'","'Probe_istorice_recalibrate.json'").replace("('t191_'+tag+'.log')","('t191_'+tag+'_utf8.log')").replace("+' -- Documentatie/'","+' -- Documentatie/echipa-2026-10-09/COORDONARE_SESIUNI.md'").replace("'t330_contract_git.log'","'t330_contract_git_exact.log'")
(Path(__file__).parent/'a12_r6_mutations_cal.py').write_text(s,encoding='utf8')

