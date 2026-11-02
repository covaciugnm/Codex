from a12_r10_base import *
for f in [E/'A11_control_supliment_G3_C20_postR9.json',P10/'T210_auth_original_et_mutant.json',P10/'T210_auth_trace_routes.json',P10/'Invarianta_T211_03.json',P10/'JVM_original.json',P10/'Plan_R10_164_et_dix_zones.json',P10/'Cai_nominale_873_fara_dublare.json']:
 d=rd(f);print(f.name,sha(f),list(d)); 
 if f.name.startswith('A11_'): 
  for k in ['prior_staging_experiment','manual_disassemblable_kit','native_primary_product_reconciliation','thresholds']:print(k,str(d[k])[:1150])
for z in r9reg:
 if z['task']in ['T210','T211.03','T211.01','T201','T220','T224','T227','T06']and(z in f164 or z in nw873):print(z['criterion'],z['text'][:225])
p=P10/'JVM/git_TestT227VerificareImport.log';print([z for z in (P10/'JVM').iterdir()]);print('MUTS',[(z['id'],[(str(f))[:100]for f in z['observed_failures'][:3]])for z in rd(P10/'T227_mutanti_nominali.json')['controls']]);
