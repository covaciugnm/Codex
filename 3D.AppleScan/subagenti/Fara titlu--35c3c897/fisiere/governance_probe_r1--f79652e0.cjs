const fs=require('fs'),path=require('path'),cp=require('child_process');
const auditRoot=__dirname,dossier=path.resolve(__dirname,'../..');
const results=[];
function setup(name){const r=path.join(auditRoot,name);fs.mkdirSync(path.join(r,'tools'),{recursive:true});for(const d of ['02_echipa','03_plan','05_validare','07_audit','09_jurnale'])fs.mkdirSync(path.join(r,d),{recursive:true});fs.copyFileSync(path.join(dossier,'tools/manage.cjs'),path.join(r,'tools/manage.cjs'));return r;}
function save(r,p,v){fs.writeFileSync(path.join(r,p),JSON.stringify(v,null,2));}
function run(r,args){const p=cp.spawnSync(process.execPath,[path.join(r,'tools/manage.cjs'),...args],{encoding:'utf8'});return {exit_code:p.status,stdout:p.stdout.trim(),stderr:p.stderr.trim()};}
let r=setup('gov_r1_invalid_task');
save(r,'02_echipa/roles.json',{roles:[{id:'MGR'},{id:'AUD-GOV'}]});
save(r,'03_plan/tasks.json',{tasks:[{id:'W-X',owner:'NONEXISTENT',auditor:'FAKE',status:'accepted',dependencies:[],outputs:[],experiments:['EX-MISSING'],acceptance:'some condition',next_action:'finished',attempt:0}]});
results.push({id:'GOV-T01',purpose:'Invalid owner/auditor and accepted task without outputs/evidence, unknown experiment',actual:run(r,['validate'])});
r=setup('gov_r1_unreciprocal_links');
save(r,'03_plan/requirements.json',{requirements:[{id:'R1',tests:['E1']}]});
save(r,'05_validare/experiments.json',{experiments:[{id:'E1',requirements:[],metric:'m',target:'t',protocol:'p',sample:'s',owner:'A',auditor:'A'}]});
results.push({id:'GOV-T02',purpose:'Unreciprocal requirement/test link, same experimental author/auditor, missing requirement owner/acceptance',actual:run(r,['validate'])});
r=setup('gov_r1_audit_coverage');
save(r,'07_audit/REGISTRU.json',{status:'accepted',required_domains:['AUD-GOV','AUD-SEC'],findings:[]});
results.push({id:'GOV-T03',purpose:'Accepted audit without domain reports or review evidence',actual:run(r,['validate'])});
r=setup('gov_r1_event_schema');
results.push({id:'GOV-T04',purpose:'Missing task, event type, result accepted by event command',actual:run(r,['event','test_actor'])});
results.push({id:'GOV-T05',purpose:'Malformed event semantically but valid JSON accepted by validate',actual:run(r,['validate'])});
r=setup('gov_r1_manifest_tmp');
fs.writeFileSync(path.join(r,'interrupted.tmp'),'uncommitted write');
results.push({id:'GOV-T06',purpose:'Create manifest with existing tmp',actual:run(r,['manifest'])});
results.push({id:'GOV-T07',purpose:'Verify same untouched tree with tmp',actual:run(r,['verify'])});
r=setup('gov_r1_init_existing');
fs.copyFileSync(path.join(dossier,'tools/create-registers.cjs'),path.join(r,'tools/create-registers.cjs'));
save(r,'02_echipa/roles.json',{sentinel:'must remain'});
const before=fs.readFileSync(path.join(r,'02_echipa/roles.json'),'utf8');
const init=cp.spawnSync(process.execPath,[path.join(r,'tools/create-registers.cjs')],{encoding:'utf8'});
results.push({id:'GOV-T08',purpose:'Initializer refuses existing roles and preserves bytes',actual:{exit_code:init.status,preserved:before===fs.readFileSync(path.join(r,'02_echipa/roles.json'),'utf8'),stderr:init.stderr.split('\n').slice(0,4).join('\n')}});
fs.writeFileSync(path.join(auditRoot,'governance_r1_results.json'),JSON.stringify({at:new Date().toISOString(),dossier_mutations:false,scope:'fixture execution of copied tooling',results},null,2));
console.log(JSON.stringify(results));

