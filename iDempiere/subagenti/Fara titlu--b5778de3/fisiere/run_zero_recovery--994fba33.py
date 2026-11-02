from pathlib import Path
from lab import *
import sys,subprocess
assert W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh'
folder=W/'a04-nir-r3';assert not folder.exists(), 'immutable target already exists'
txt=(W/'a04-post3.py').read_text().replace("d=W/'a04-nir-post/run3'","d=W/'a04-nir-r3'")
start=txt.index("  m=pg.get_by_role(");end=txt.index("  row=pg.get_by_text(docno",start)
txt=txt[:start]+'''  rec["runtime_roles"]=rows("SELECT ur.ad_user_id,ur.ad_role_id,r.name FROM adempiere.ad_user_roles ur JOIN adempiere.ad_role r using(ad_role_id) WHERE ur.ad_user_id=(SELECT ad_user_id FROM adempiere.ad_user WHERE name='GardenAdmin' and ad_client_id=11 order by 1 limit 1) AND ur.isactive='Y' order by 2")
  rec["ui_session_visible_titles"]=[x for x in pg.locator("[title]:visible").evaluate_all("es=>es.map(e=>e.getAttribute('title'))") if x and ('Garden' in x or '11'==x)]
  rec["input_fixture"]="same 1000002 CO/USD, postconfiguration; no need to repeat the migration callback tested in R6"
'''+txt[end:]
txt=txt.replace("[('control','7\\n3'),('blank','\\n3'),('invalid','invalida\\n3')]","[('zero-first','0\\n3'),('invalid-first','invalida\\n3'),('manual-recovery','7\\n3')]")
txt=txt.replace("('370.00' if label!='invalid' else 'validare sau corecție fără deplasarea valorii la alt articol')","('300.00' if label=='zero-first' else '370.00' if label=='manual-recovery' else 'blocaj explicit cu posibilitatea corectării')")
script=W/'a04-r3-ui.py';script.write_text(txt);subprocess.run([sys.executable,str(script)],check=True)
