module.exports=function({data,src,root}){
 const fs=require('fs'),path=require('path'),crypto=require('crypto');const file=path.join(root,'reverificare-detaliata/parametri-reverificati.json');if(!fs.existsSync(file))return;
 const r=JSON.parse(fs.readFileSync(file,'utf8'));
 for(const e of r.sourceHashes){const hash=crypto.createHash('sha256').update(fs.readFileSync(path.join(src,e.file))).digest('hex');if(hash!==e.sha256)throw Error('Reverification source changed: '+e.file);}
 const category=t=>/\|/.test(t)?'uniune de reprezentări':/List|\[\]/.test(t)?'listă':/Map/.test(t)?'obiect / hartă':/^(boolean|Boolean)$/.test(t)?'boolean':/^(int|Integer|long|Long|byte|Byte|short|Short)$/.test(t)?'întreg':/^(float|Float|double|Double)$/.test(t)?'număr real':t==='Number'?'număr Java abstract':t==='String'?'text':t==='null'?'valoare null':'obiect / referință';
 for(const v of r.resolutions){const p=data.parameters.find(p=>p.id===v.id);if(!p)continue;
  if(v.status==='tip_rezolvat_static'&&p.javaType==='necunoscut'){p.javaType=v.javaType;p.valueClass=category(v.javaType);if(p.observedJavaTypes)p.observedJavaTypes=[v.javaType];}
  if(v.coercion)p.coercion=v.coercion;
  if(v.coercionVariants)p.coercionVariants=v.coercionVariants;
  if(v.dexEvidence){p.dexEvidence=v.dexEvidence;p.officialSource=v.officialSource;p.nullable=v.nullable;p.nullableStatus=v.nullableStatus;}
  if(v.observedKeys){p.observedKeys=v.observedKeys;p.keyStatus='cheie parametrizată; numele {str} nu este o cheie literală pe fir';}
  p.staticReverification={status:v.status,previousType:v.before||'necunoscut',note:v.resolutionNote||v.remaining,next:v.next,report:'../reverificare-detaliata/INDEX.html#'+v.id};
  for(const ev of v.evidence)if(!p.evidence.some(e=>e.file===ev.file&&e.line===ev.line&&e.role===ev.role))p.evidence.push(ev);
 }
};
