const fs=require('fs'),p=require('path'),b=process.argv[2],rd=n=>JSON.parse(fs.readFileSync(p.join(b,n),'utf8')),a=rd('A12_index_taskuri.json'),q=rd('A12_plan_taskuri.json');
const src=new Map();const lookup=(fn,ptr)=>{if(!src.has(fn))src.set(fn,rd('capturi/'+fn));let val=src.get(fn);return ptr.split('/').slice(1).reduce((v,k)=>v?.[k.replace(/~1/g,'/').replace(/~0/g,'~')],val)};
let errs=[],n=0,exact=0;for(const row of a.rows){for(const ref of [...(row.source_registry||[]),...(row.source_lists||[])]){n++;if(lookup(ref.file,ref.pointer)===undefined)errs.push([row.source_id,ref.file,ref.pointer]);}
for(const ob of row.obligations||[]){let [fn,ptr]=ob.pointer.split('#');if(!ptr)continue;n++;const val=lookup(fn.replace(/^capturi\//,''),ptr);if(val===undefined)errs.push([row.source_id,'obligation',ob.pointer]);else if(ob.kind==='cerere_proprietar'||ob.kind==='descriere'){if(val!==ob.text)errs.push([row.source_id,'obligation text',ob.pointer]);else exact++;}}
}
console.log('Source pointers',n,'exact requirement/description',exact,'errors',errs.length,errs.slice(0,10));console.log('status',q.scoring_policy.authority,q.task_report_template.audit_quality.status);const rr=rd('A11_rubrica_control.json');console.log('gate expected: '+rr.criteria.flatMap(c=>c.plan_subchecks).length+' checks');

