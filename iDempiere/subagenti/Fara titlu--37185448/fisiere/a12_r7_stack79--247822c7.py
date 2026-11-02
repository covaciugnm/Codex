from a12_r7_stack import *
reg=rd(E/'R6/Registru_reexecutare_R6.json')['records'];t0=[w for w in reg if w['R6_state']=='NEEXECUTAT'and w['entry_and_oracle_specific_to_case']['named_test_fixtures_in_source']]
names=sorted({y for z in t0 for y in z['entry_and_oracle_specific_to_case']['named_test_fixtures_in_source']});orig=rd(RP/'stack_exec.json');old={z['suite']for z in orig};suite_candidates={nm:(plug/'test'/(nm+'.java'))for nm in names};todo=[(t,k)for k,p in suite_candidates.items()if k not in old and p.exists()and 'public static void main(' in p.read_text(encoding='utf8') for t in ['git','instalat']]
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5)as pool:out=list(pool.map(case,todo))
 wr(RP/'stack_exec_neexec.json',{'names_available':names,'already_run':sorted(old&set(names)),'new':out,'without_main_in_root':[k for k,p in suite_candidates.items()if not p.exists()or'public static void main('not in p.read_text(encoding='utf8')]});print(len(out),sum(v['traced']for v in out),sum(v['exit']==0 for v in out))

