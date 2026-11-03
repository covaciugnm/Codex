from pathlib import Path
import sys,json,hashlib
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');D=Path('D:/CodexWork')
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
ref=lambda p:{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
spec=rd(Path(sys.argv[1]))
inputs={k:ref(R/p) for k,p in spec['paths'].items()}
hd=rd(R/spec['paths']['handoff']);metrics=rd(R/spec['paths']['metrics'])
assert hd['counts']==metrics['counts']
head=hd.get('head',hd.get('candidate'));assert head=='df85d33c1648ce2b2df130a60a05ef696e2e5480'
assert spec['lots_and_register_independently_received'] is True
counts=hd['counts'];n=counts['current_bounded_source_identities']
axes={k:v['count'] for k,v in metrics['current_exclusive_primary_levels'].items()}
assert sum(axes.values())==n
coverage=f'Registrul păstrează 6.728 de identități tehnice. Sunt acum {n} de surse cu dovezi parțiale, față de 44 în Val04. '+spec['coverage_breakdown']+' Inventarierea, lectura, compilarea, încărcarea, apelarea metodelor și persistența sunt evidențiate separat. Niciun fișier, task sau contract nu este recepționat integral.'
next_action=spec['next']
cfg={
 'independent_lots_received':True,'independent_register_received':True,'inputs':inputs,'counts':counts,'axes':axes,
 'state':f'R12 VAL05 RECEPȚIONAT PARȚIAL; {n} SURSE CU DOVEZI DIFERENȚIATE; 17 CONTRACTE DESCHISE',
 'open_contracts':17,'coverage_meaning':coverage,'resources':spec['resources'],'retained_scratch_count':spec['retained_scratch_count'],'next':next_action,
 'population':{'all':997,'P01':694,'historic_completed_tasks':652,'historic_criteria':2619,'new_members_since_0143':0,'removed_members_since_0143':0,'state_changes_since_0143':0,'T343_document_pointer_changed':True},
 'revision_boundary':{'github_frozen_candidate':head,'server_worktree_head_observed':'c594a93a1d4e606f8c2e432108a29e97244d692e','capture':'2026-11-03T02:45Z','no_transfer_to_server_worktree':True},
 'native_order':spec['native_order'],
 'backend_catalog_pagination':{'manifest':inputs['pagination_manifest'],'receipt':inputs['pagination_verdict'],'executor_cases':16,'limited_conformant':10,'nonconformant':6,'independent_calls_separate':6,'finding':'R12-CATALOG-JSON-PAGINATION-01','mechanisms':1,'affected_method_sites':2,'HTTP_DB_UI_executed':False},
 'reading_qa':spec['reading_qa'],'visual_inspection_completed':False,'visual_inspection_note':None,
}
section=(D/'p01-r12-val05-section.template.html').read_text(encoding='utf-8')
replacements={
 'REPLACE_STATUS':'Dovezi noi pe componente originale, recepționate independent. Auditul integral rămâne deschis.',
 'REPLACE_COVERAGE':coverage,
 'REPLACE_PAGINATION_RECEIPT':'A11 a recalculat cele 16 ieșiri și a reprodus separat problema prin șase apeluri proprii (doi martori conformi și patru contraexemple). Aceste apeluri sunt evidențiate separat de cazurile executorului.',
 'REPLACE_PAGINATION_READING':spec['paths']['pagination_reading'],
 'REPLACE_PAGINATION_VERDICT':spec['paths']['pagination_verdict'],
 'REPLACE_NATIVE':Path(spec['native_fragment']).read_text(encoding='utf-8'),
 'REPLACE_NEXT':next_action+' Nu au fost efectuate modificări ale aplicației sau scrieri în sistemele operaționale.',
 'REPLACE_RESOURCES':spec['resources'],
 'REPLACE_A12_INDEX':spec['paths']['reading_index'],
 'REPLACE_A11_REGISTER':spec['paths']['verdict'],
 'REPLACE_CHECKLIST':spec['paths']['checklist'],
}
for old,new in replacements.items():assert old in section,old;section=section.replace(old,new)
assert 'REPLACE_' not in section
sp=D/'p01-r12-val05-section.html';sp.write_text(section,encoding='utf-8');cfg['html_block']=str(sp)
out=D/'p01-publish-r12-val05-config.json';out.write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
