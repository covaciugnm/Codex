from pathlib import Path
import sys,json,importlib.machinery
sys.argv.append('unused');m=importlib.machinery.SourceFileLoader('r8g','D:/CodexWork/a05r8-git.py').load_module()
tasks=m.tasks; hist=json.loads((m.w/'history-corpus.json').read_text(encoding='utf8'))
spec=[(z['task'],z['source']['source_file'],z['source']['sha_or_git_blob']) for z in m.my if z['source']['source_file'].startswith('Documentatie/')]
program=m.header+'paths='+repr(sorted(set(spec)))+'\nhist='+repr({t:h['dated_master_snapshot'] for t,h in hist['tasks'].items()})+"""
ans={}
for task,path,expected in paths:
 oid=g('rev-parse',cut+':'+path);dat=blob(oid)
 try:old=g('rev-parse',hist[task]+':'+path);oldtxt=blob(old).decode('utf8','replace') if old else None
 except (sp.CalledProcessError,KeyError):old,oldtxt=None,None
 ans[task]={'file':path,'current_oid':oid,'registry_oid':expected,'snapshot':hist[task],'historic_oid':old,'lines_current':dat.decode('utf8','replace').splitlines(),'lines_old':oldtxt.splitlines() if oldtxt else []}
path='Documentatie/echipa-2026-10-09/T40-gestiuni-fifo-lifo-cmp-paritate-saga/01a_matrice_paritate_saga_eva.md'
tables={}
for task,rev in [('T329_closure',hist['T329']),('T330_closure',hist['T330']),('cut',cut)]:
 oid=g('rev-parse',rev+':'+path);data=blob(oid).decode('utf8','replace').splitlines()
 tables[task]={'commit':rev,'git_blob':oid,'file':path,'lines':{str(n):data[n-1] for n in [57,92]},'by_indicator':[(i+1,s[:500]) for i,s in enumerate(data) if s.startswith('|') and ('3.09' in s or '4.19' in s)][:5]}
print(json.dumps({'plans':ans,'matrix':tables},ensure_ascii=False))
"""
o=json.loads(m.remote(program));m.dump(m.w/'oracles.json',o);m.dump(m.out/'Matrice_T40.json',o['matrix'])
