from a12_r10_base import *
from collections import Counter
rr=rd(P9/'Relectura_882_pointeri.json');src_idx={v['criterion']:v for v in rr['rows']};old_index={z['criterion']:z for z in rd(E/'R8_pregatire/Index_883_relectura_surse.json')['records']}
def build():
 vals=[];before=Counter()
 for r in nw873:
  id=r['criterion'];raw=r7map[id];p=src_idx[id];u=raw['individual_reasoning'];au=raw.get('original_inputs_and_accepted_oracle')or{};ss=r7reg.get(id,{}).get('entry_and_oracle_specific_to_case')or {};ln=old_index[id];ops=u.get('case_specific_entrypoints')or{};missing_fields=u.get('missing_parameters_for_complete_path')or[]
  if id.startswith('T210-'):route='DESFĂȘURARE_CONTRACT_HTTP_T210'
  elif id.startswith('T227-'):route='CONTRACT_IMPORT_SAGA_NUMAI_LA_NIVELUL_OBSERVABIL'
  elif id in ('T211.01-R2-003','T211.03-R2-003'):route='MOTORUL_REGULII_VERSUS_PUBLICAREA_ERP'
  elif p['primary_source_type']=='manual_json':route='MANUAL_CPP_CPA_REȚEA_DE_DEPENDENȚE'; 
  elif p['primary_source_type']=='git_text'and au.get('kind')=='independent_table_fields':route='TABEL_EXPLICIT_ÎN_DOSAR_DAR_ORACOLUL_COMPLET_RĂMÂNE_NEEXECUTAT'
  elif p['primary_source_type']=='git_text':route='SPECIFICAȚIE_GIT_DE_LOCALIZAT_REGULA_ATOMICĂ'
  elif p['primary_source_type']=='git_json':route='REGISTRU_ISTORIC_URMEAZĂ_ID_ȘI_SUCCESORUL'
  elif p['primary_source_type']=='captured_json' and p['object_type']=='dict':route='FIȘĂ_PORTAL_CU_AUTOR_ȘI_ȚINTĂ_DE_REGĂSIT'
  else:route='CÂMP_INDIVIDUAL_JSON_RECONSTITUIE_CEREREA_ȘI_ETALONUL'
  before[route]+=1
  v={'criterion':id,'task':r['task'],'canonical':r['canonical'],'owner':r['owner'],'norm':r['text'],'route_to_next_control':route,'source_locator':{'file':p['location'],'pointer':p['original_pointer'],'blob_or_file_sha':p['file_SHA_or_Git_oid'],'value_hash':p['value_sha256_canonical_JSON'],'type':p['primary_source_type']},'field_of_approved_source_to_retest':{'known_condition':au.get('condition'),'expected_if_recorded':au.get('expected'),'primary_original_recipe':ss.get('recipe_from_own_row')or ops.get('author_recipe'),'existing_named_tests':ss.get('named_test_fixtures_in_source')or[],'existing_named_native_entities':ss.get('native_entities_explicit')or[],'observed_candidate_lines_from_before':p['preexisting_search_candidates']},'missing_for_full_reception':missing_fields,'qualification':'Se urmărește versiunea și identitatea actorului, apoi dovada pe aceeași cheie dacă există un oracol. O linie din sursă singură nu creează verdict.','product_credit_from_triage':0}
  if route.startswith('TABEL')or route=='SPECIFICAȚIE_GIT_DE_LOCALIZAT_REGULA_ATOMICĂ':v['specific_next']='Extrage columna de așteptat și domeniul alăturat la '+p['location']+' @'+str(p['original_pointer'])+'; execută pe datele named dacǎ sunt recuperabile. Martorul trebuie să schimbe o condiție individuală, nu întreaga versiune.'
  elif route.startswith('MANUAL'):v['specific_next']='Recitește corpul cerinței '+id+' în JSON, stabilește dependența canonică din manual, actorul și tabelul native; compară versiunea activă înainte/după.'
  elif route.startswith('REGISTRU')or route.startswith('FIȘĂ')or route.startswith('CÂMP'):v['specific_next']='Confruntă '+str(r['task'])+' cu id_vechi, ultima stare și ținta nominală; caută un înscris datat separat de câmpul registrului. Nu se inventează data exactă sau o normă nouă.'
  else:v['specific_next']='Execută numai subcondiția nominală pe traseul '+route+'; fixează transportul/fixture şi a doua cale ca martor.'
  vals.append(v)
 hist={z['criterion']:z for z in his167};pan=rd(P10/'Plan_R10_164_et_dix_zones.json')
 f=P10/'Cai_nominale_873_fara_dublare.json';wr(f,{'utc':now(),'source_prior':source(P9/'Relectura_882_pointeri.json'),'count':len(vals),'separate_unavailable_preexisting_history':len(hist),'candidate_distribution':before,'probative_outcomes_belong_to_named_receipts':True,'records':vals});print(sha(f),before)
if __name__=='__main__':build()

