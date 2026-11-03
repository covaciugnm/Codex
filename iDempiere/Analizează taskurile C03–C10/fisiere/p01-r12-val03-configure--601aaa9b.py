from pathlib import Path
import sys,json,hashlib
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');D=Path('D:/CodexWork')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
items={
'verdict':(sys.argv[1],sys.argv[2]),
'manifest':('executie/R12_fisiere/A12/Val_03/MANIFEST_R12_Val03.json','5f80d3973e34be94ce12aafdea307eec43aca359b42f2a0042c740e6c9db9a23'),
'handoff':('executie/R12_fisiere/A12/Val_03/Handoff_R12_Val03_v2.json','58c7de3c525c69af3dd41799eed8e485f682e577233ea47f9acef3d7bda15dbb'),
'manifest_reading_corrected':('executie/R12_fisiere/A12/Val_03/MANIFEST_lectura_finala_Val03_v1.json','1b40caa6b7587badc3e304467ad0a4386c5a3f725f4c4b9c3f0efd107b530dfe'),
'state_addendum':('executie/R12_fisiere/A12/Val_03/SIGILIU_supliment_stari_Val03_v1.json','2a0c42fd6bc8ea2e11458a49792259c7f92c82a77e6217e997c343064a7dd38c'),
'checklist':('executie/R12_fisiere/A11/Val03_loturi/Checklist_A11_dupa_R12_Val03_v1.json','3e6aff18819a2d88cd6de04b7ee71dbdd159b80ea7df5652524896306a9dd3ba'),
'native_verdict':('executie/R12_fisiere/A11/Val03_loturi/Verdict_A11_N05_lot03_v1.json','bfe30d3d390f20cff2bf159eb4ecd2b9fdd81da2cc30abdd6424d40b2adf144b'),
'a10_verdict':('executie/R12_fisiere/A11/Val03_loturi/Verdict_A11_A10_lot03_v1.json','bb2024524f65b9a5f56d0fb418f0fb8f7f46b4a512ac3331e04c3eea51a4b064'),
'a06_verdict':('executie/R12_fisiere/A11/Val03_loturi/Verdict_A11_A06_lot03_v1.json','0d75650460ef5d40f03882ee3761fda6b74e3caa4f5f9ff1782ec832f1504842'),
'g3_verdict':('executie/R12_fisiere/A11/Val03_loturi/Verdict_A11_G3_SQL_lot04_v1.json','033ff6bfb76269eb37a29ad888e249d3e009c37aa2d6f6333928fd46a9fa3e73'),
'population_supplement':('executie/R12_fisiere/A12/Val_03/Supliment_populatie_0039.json','cac08725a0ba8790ccccf8c8e373039006ecb1aed3bb82a9828110da81f241e9'),
'population_delta':('executie/delta/2026-11-03T00-39-34-490Z/Comparatie_ultimul_checkpoint.json','2b2d872957e17ad860d0db219f2e19f8b6f5c4bc7ee5bd07d0a94b0c54918303'),
'peer_accounting':('executie/R12_fisiere/A03/A03_peer_N05_v1.json','a9e499e4db9c74d43add7f0401daafbf0e5a03ff6fd5ca7d30015088ca34464d'),
'native_manifest':('executie/R12_fisiere/A05_N05_lot03/MANIFEST_A05_N05_lot03_v1.json','1a194d28361afe9184e017f8efee7659618edb18f5ff1a671f9134f9adbc623f'),
'a06_manifest':('executie/R12_fisiere/A06_T343_instrumente_lot03/MANIFEST_A06_lot03.json','5743839e4a93c1cb2d7e61b010081668693ea1ae4f4fcae388876b96d1a319fe'),
'a10_manifest':('executie/R12_fisiere/A10_Instrumente_ramase_lot03/Manifest_lot03.json','7b3289641e6321eeccbac23e3fb9d03ebc570f9906928e9902b3aea5ff41724d'),
'g3_manifest':('executie/R12_fisiere/A06_Rezervari_nativ_lot04/MANIFEST_A06_rezervari_lot04.json','bf5dee20c4e539bc10610ec17ba23433d907a71e483f53fb31c0dd36293e4232'),
'native_reader_manifest':('executie/R12_fisiere/A05_N05_lot03/MANIFEST_lectura_v3.json','b552489faa6ed8a272b6c42e901f763822547636140814fe0ba6535893550220')}
inputs={}
for k,(p,s) in items.items():
 assert sha(R/p)==s,(k,sha(R/p),s)
 inputs[k]=ref(R/p)
hd=json.loads((R/items['handoff'][0]).read_text(encoding='utf-8-sig'));cnt=hd['counts']
assert cnt['current_bounded_execution_or_comparator_sources']==39 and cnt['business_contracts_open']==17 and cnt['full_tasks_closed']==0
coverage='Registrul păstrează 6.728 de identități tehnice. Față de cele 13 surse din Val02, sunt acum 39 cu dovezi limitate și diferențiate: 26 cu componente sau trasee de metode originale, 7 cu comparatoare sintetice, 2 cu utilizări de tip/record și 4 numai cu fixture, legături de rulare ori metadate. Cele 31 lecturi statice suplimentare nu sunt execuții. Niciun fișier, task sau contract de business nu primește recepție integrală.'
resources='Laboratorul nativ N05 a fost oprit și șters; portul56455 este liber, fără JVM aferent. Cache-ul și harnessul pasiv rămân pentru reproducere. Șase directoare ale celorlalte probe sunt păstrate: verificarea automată a respins ștergerea cu „blocked by policy”. Refuzurile nu au fost ocolite; nu se declară restituirea integrală a tuturor fișierelor temporare.'
next_text='Continuarea urmărește cele 17 contracte complete: recepția remedierii N05, rezervări SO/PO prin cititori și documente native, DocAction/Fact_Acct, identități CPP/CPA, gestiuni multiple și fluxuri frontend cu rol. Se verifică și fișierele neschimbate; cele 19 instrumente noi au doar probe parțiale. Niciun criteriu istoric nu este închis automat.'
block=(D/'p01-r12-val03-section.template.html').read_text(encoding='utf-8')
replacements={'REPLACE_COVERAGE':coverage,'REPLACE_NATIVE':(D/'p01-r12-val03-native.fragment.html').read_text(encoding='utf-8'),'REPLACE_A10_VERDICT':items['a10_verdict'][0],'REPLACE_NEXT':next_text,'REPLACE_RESOURCES':resources,'REPLACE_REGISTER_VERDICT':items['verdict'][0],'REPLACE_CHECKLIST':items['checklist'][0]}
for a,b in replacements.items():block=block.replace(a,b)
block=block.replace('A12/Val_03/index.html','A12/Val_03/index_final.html').replace('trecut de la50 la54','trecut de la 50 la 54').replace('fizic50, SO4, PO9','stoc fizic 50, rezervări de vânzare 4, comandă furnizor 9').replace('portul56455','portul 56455')
a=block.index('<h3>Disponibilul');b=block.index('<h3>WMS:');c=block.index('<h3>Șapte instrumente')
block=block[:a]+block[b:c]+block[a:b]+block[c:]
assert 'REPLACE_' not in block
bp=D/'p01-r12-val03-section.html';assert not bp.exists();bp.write_text(block,encoding='utf-8')
cfg={'independent_lots_received':True,'independent_register_received':True,'inputs':inputs,'counts':cnt,'axes':{'original_components_or_method_paths':26,'synthetic_comparators':7,'type_record_uses':2,'fixture_binding_metadata':4,'static_only_added':31},'state':'R12 VAL03 RECEPȚIONAT PARȚIAL; 39 SURSE CU DOVEZI DIFERENȚIATE; 17 CONTRACTE DESCHISE','open_contracts':17,'coverage_meaning':coverage,'resources':resources,'next':next_text+' Reia din handoff v2 și checklistul A11, verificând execuțiile active și delta de cod/populație înainte de probe. Nu modifica sistemele operaționale. Nu reîncerca ștergerile respinse automat.','revision_boundary':{'github_frozen_candidate':hd['head'],'server_worktree_head_observed':'1687cc8376902e7aa7163a883e07c7271bcae511','capture':'2026-11-03T00:39Z','no_transfer_to_server_worktree':True},'native_N05':{'manifest':inputs['native_manifest'],'independent_receipt':inputs['native_verdict'],'same_existing_finding':True,'quantitative_WMS':11,'initial_quantity':10,'not_physical_count':True,'not_Fact_Acct_balance_acceptance':True,'normal_serial_managedTrx':True,'concurrency_and_rollback_managedTrx':False,'external_commit_coordination':True,'full_UI':False,'scenarios':7,'recovery_only_for_recoverable_components':True},'html_block':str(bp),'reading_qa':['executie/Publicare_R12_Val03/QA_2026-11-03T01-26-13Z/QA.json','executie/Publicare_R12_Val02/QA_2026-11-03T01-11-12Z/QA.json','executie/Publicare_R12_Val02/QA_2026-11-03T01-13-13Z/QA.json','executie/Publicare_R12_Val03/QA_2026-11-03T01-32-10Z/QA.json']}
p=D/'p01-publish-r12-val03-config.json';assert not p.exists();p.write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8');print(p)
