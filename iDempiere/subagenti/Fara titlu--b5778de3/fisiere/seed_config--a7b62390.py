from lab import *
from pathlib import Path
import json,datetime,hashlib
assert W.name=='eva-contab-codex-p01uizk-r5.vUjauFBh'
assert cmd(['docker','inspect','--format','{{index .Config.Labels "eva.sesiune"}}',AP])=='eva-contab-codex-p01uizkr5'
assert str(PG).startswith('eva-test-') and rows("select ad_client_id,name from adempiere.ad_client order by 1;")==[['0','System'],['11','GardenWorld']]
assert sql("select count(*) from adempiere.ad_scheduler where isactive='Y'")=='0'
d=W/'a04-nir-post';d.mkdir(exist_ok=True)
q="select ad_sysconfig_id,ad_client_id,ad_org_id,name,value,description from adempiere.ad_sysconfig where ad_client_id=11 and name='EVA_SETARI_FIRMA_MIGRAT'"
old=rows(q);assert not old,old
assert sql("select count(*) from adempiere.ad_sysconfig where ad_sysconfig_id=2000095005")=='0'
meta={"utc":now(),"phase":"Explicit synthetic witness in isolated GardenWorld. These are not the output nor the validation of the migration process.","before":old,"guard":str(PG),"image":cmd(['docker','inspect','--format','{{.Image}}',AP]),"source_sha":"6df998aee0e514d30856c461962afe99ebd0d113","jar_provenance_sha_expected":None}
sql("begin; INSERT INTO adempiere.ad_sysconfig (ad_sysconfig_id,ad_sysconfig_uu,ad_client_id,ad_org_id,name,value,description,configurationlevel,createdby,updatedby) VALUES(2000095005,gen_random_uuid(),11,0,'EVA_SETARI_FIRMA_MIGRAT','Y','A04 synthetic NIR postconfiguration test only','C',100,100); commit;")
meta['after']=rows(q);meta['fixture_periods_before_NIR']=rows("select cheie,validfrom,valoaretext,valoarenumar from adempiere.eva_setarefirmaperioada where ad_client_id=11 order by 1;");(d/'config.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print(meta['after'])
