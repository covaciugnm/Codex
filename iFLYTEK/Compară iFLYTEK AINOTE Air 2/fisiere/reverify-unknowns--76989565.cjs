/* Conservative evidence pass over every previously unknown parameter. No device/cloud calls. */
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),out=path.join(root,'reverificare-detaliata');fs.mkdirSync(out,{recursive:true});
const parserText=fs.readFileSync(path.join(__dirname,'catalog-extract.cjs'),'utf8').split('function resolve(')[0];
const sandbox={require,__dirname,api:null};vm.runInNewContext(parserText+';api={get,src,cache,split,mask};',sandbox);const {get,src,cache,split,mask}=sandbox.api;
const params=JSON.parse(fs.readFileSync(path.join(out,'baseline-parametri.json'),'utf8')),functions=JSON.parse(fs.readFileSync(path.join(out,'baseline-functii.json'),'utf8'));
const clean=s=>s.replace(/\/\*[\s\S]*?\*\//g,'').replace(/@[\w.]+(?:\([^)]*\))?\s*/g,'').replace(/\b(public|private|protected|static|final|synchronized|native)\b/g,'').replace(/\s+/g,' ').trim();
const norm=t=>t==='HashMap'||/^HashMap</.test(t)?t.replace('HashMap','Map'):t;
const proof=(file,line,excerpt,role)=>({file,line,excerpt:String(excerpt).trim(),role});
const lineAt=(d,pos)=>d.s.slice(0,pos).split('\n').length;
const methodAt=(d,line)=>d.methods.filter(m=>m.line<=line&&lineAt(d,m.end)>=line).sort((a,b)=>b.start-a.start)[0];
const returnType=m=>clean(m.signature.slice(0,m.signature.indexOf(m.name+'(')));
function typeTarget(type,d,owner){type=type.replace(/<.*>/,'').replace(/\[\]$/,'');const nested=d.classes.find(c=>c.name===type&&(c.parent===owner||c.full===owner+'$'+type));if(nested)return {d,owner:nested.full};if(d.classes.some(c=>c.name===type))return {d,owner:d.classes.find(c=>c.name===type).full};const file=d.imports[type]||path.posix.join(path.posix.dirname(d.file),type+'.java');const target=get(file);return target?{d:target,owner:target.pkg+'.'+type}:null;}
function variableType(name,d,m,absolute){name=name.replace(/^this\./,'');const a=m?.args.find(a=>a.name===name);if(a)return {type:clean(a.type),evidence:[proof(d.file,m.line,m.signature,'tip argument declarat')]};
  const before=m?d.s.slice(m.bodyStart,absolute):'';const re=new RegExp('\\b([\\w.$]+(?:<[^;=\\r\\n]+>)?(?:\\[\\])?)\\s+'+name+'\\s*(?:=|;)','g');let found=[...before.matchAll(re)].filter(x=>!['return','throw','new'].includes(x[1])).at(-1);
  if(found)return {type:norm(found[1]),evidence:[proof(d.file,lineAt(d,m.bodyStart+found.index),found[0],'declarație locală')]};
  const fields=[...d.s.matchAll(new RegExp('^[ \\t]*(?:public|private|protected)\\s+(?:(?:static|final|volatile)\\s+)*([\\w.$]+(?:<[^;=\\r\\n]+>)?(?:\\[\\])?)\\s+'+name+'\\s*(?:=|;)','gm'))].filter(x=>!d.methods.some(k=>k.start<x.index&&k.end>x.index));
  const same=fields.filter(x=>d.classes.filter(c=>c.start<x.index&&c.end>x.index).at(-1)?.full===m?.owner);found=(same.length?same:fields).length===1?(same.length?same:fields)[0]:null;
  return found?{type:norm(found[1]),evidence:[proof(d.file,lineAt(d,found.index),found[0],'tip câmp declarat')]}:null;
}
function infer(expr,d,m,absolute,depth=0){if(!expr||depth>5)return null;expr=expr.trim();const ev=proof(d.file,lineAt(d,absolute),expr,'expresie inspectată');
  const simple=/^(String|Boolean|Integer|Long|Double|Float|Byte|Short)\.valueOf\(/.exec(expr);if(simple)return {type:simple[1],evidence:[ev]};
  if(/^"(?:\\.|[^"\\])*"(?:\s*\+|$)/.test(expr))return {type:'String',evidence:[ev]};if(expr==='null')return {type:'null',evidence:[ev]};if(/^(true|false|Boolean.TRUE|Boolean.FALSE)$/.test(expr))return {type:'Boolean',evidence:[ev]};if(/^-?\d+[Ll]$/.test(expr))return {type:'Long',evidence:[ev]};if(/^-?\d+$/.test(expr))return {type:'Integer',evidence:[ev]};
  if(/\?\s*Integer\.valueOf\(.+\)\s*:\s*null$/.test(expr))return {type:'Integer | null',evidence:[ev]};
  const ctor=expr.match(/^new ([\w.]+(?:<[^>]*>)?)(?:\(|\[)/);if(ctor)return {type:norm(ctor[1]),evidence:[ev]};
  if(/^(?:this\.)?[\w$]+$/.test(expr))return variableType(expr,d,m,absolute);
  const call=expr.match(/^([\w.$]+)\(([\s\S]*)\)$/);if(!call)return null;
  const name=call[1].split('.').at(-1),receiver=call[1].slice(0,-name.length).replace(/\.$/,'');let target={d,owner:m?.owner},receiverProof=[];
  if(receiver&&receiver!=='this'){
    const v=variableType(receiver,d,m,absolute);if(v){target=typeTarget(v.type,d,m?.owner);receiverProof=v.evidence;}else target=typeTarget(receiver,d,m?.owner);
  }
  if(!target)return null;const candidates=target.d.methods.filter(k=>k.name===name&&(!target.owner||k.owner===target.owner)&&k.args.length===split(call[2]).length);if(candidates.length!==1)return null;
  const k=candidates[0],type=returnType(k),evidence=[ev,...receiverProof,proof(target.d.file,k.line,k.signature,'semnătura producătorului')];if(!type||type==='void')return null;
  if(type!=='Object')return {type:norm(type),evidence};
  const returns=[...mask(k.body).matchAll(/\breturn\b/g)].map(z=>({at:k.bodyStart+z.index,expr:k.body.slice(z.index+6).split(';')[0].trim()})).filter(z=>!target.d.methods.some(n=>n.start>k.start&&n.end<k.end&&n.start<z.at&&n.end>z.at));
  const inferred=returns.map(z=>infer(z.expr,target.d,k,z.at,depth+1));if(!returns.length||inferred.some(z=>!z||z.type==='Object'))return {type:'Object',evidence};const types=[...new Set(inferred.map(x=>x.type))];return {type:types.join(' | '),evidence:[...evidence,...inferred.flatMap(x=>x.evidence)],note:'Tip derivat din toate expresiile return inspectabile ale producătorului; excepțiile sunt separate.'};
}
const resolutions=[];
for(const p of params.filter(p=>p.javaType==='necunoscut')){
  const record={id:p.id,name:p.name,direction:p.direction,functionIds:p.functionIds,before:p.javaType,status:'inca_necunoscut',evidence:[],attempts:[],remaining:'Domeniul semantic, unitățile și compatibilitatea cu firmware-ul nu sunt stabilite numai din tip.'};
  const found=[];
  for(const e of p.evidence){const d=get(e.file);if(!d)continue;const lines=d.s.split('\n'),line=lines[e.line-1]||'',absolute=lines.slice(0,e.line-1).join('\n').length+1,m=methodAt(d,e.line);if(!m)continue;record.attempts.push({file:e.file,line:e.line,method:m.name});
    if(p.direction==='intrare Flutter'){
      let type=null;const expr=p.expression,idx=line.indexOf(expr),before=idx>=0?line.slice(0,idx):line;const cast=before.match(/\((String|Integer|Long|Boolean|Double|Float|Number|Map(?:<[^>]+>)?|List(?:<[^>]+>)?|byte\[\])\)\s*[\w.]*$/);
      if(cast)found.push({type:cast[1],evidence:[proof(e.file,e.line,line,'cast explicit al argumentului')]});
      else if(/\.equals\(.*\.argument\(/.test(line)){
        const receiver=line.match(/(\w+)\.equals\(/)?.[1];const declared=receiver&&new RegExp('Boolean\\s+'+receiver+'\\s*=\\s*Boolean\\.TRUE').test(m.body);
        if(declared){record.coercion='Boolean.TRUE.equals(argument): numai Boolean true produce true; null și celelalte obiecte produc false.';record.status='conversie_documentata';record.evidence.push(proof(e.file,e.line,line,'conversie Boolean.TRUE.equals; nu cast de intrare'));}
      }else{
        const varName=before.match(/\bObject\s+(\w+)\s*=\s*(?:\(\(Map\) arguments\)\.get\()?$/)?.[1]||line.match(/\bObject\s+(\w+)\s*=/)?.[1];
        if(varName){const tail=d.s.slice(absolute+line.length,Math.min(m.end,absolute+1800));const types=[...tail.matchAll(new RegExp('\\(\\((String|Integer|Long|Boolean|Double|Float|Number|Map|List|byte\\[\\])\\)\\s*'+varName+'\\)','g'))].map(z=>z[1]);const unique=[...new Set(types)];
          if(unique.length===1&&!tail.includes(varName+' instanceof')){found.push({type:unique[0],evidence:[proof(e.file,e.line,line,'argument stocat local'),proof(e.file,e.line+1,tail.slice(0,900),'cast al consumatorului local; nullable neconfirmat')]});}
          else if(unique.length){record.status='conversie_documentata';record.coercion='Ramuri de conversie pentru '+unique.join(' / ')+'. Tipurile alternative, omisiunea și fallbackul se citesc în corpul atașat; nu se declară domeniu închis.';record.evidence.push(proof(e.file,e.line,d.s.slice(absolute,Math.min(m.end,absolute+1500)),'conversii condiționate / fallback'));}
        }
      }
      if(!found.length&&record.status==='inca_necunoscut'){record.evidence.push(proof(e.file,e.line,line,'citire generică; tipul necesită urmărirea consumatorului'));}
    }else{
      const expressions=p.expression?[p.expression]:(p.observedExpressions||[]);
      for(const expr of expressions){
        // Each observed expression belongs to its own producer evidence, not to
        // every source line attached to the union parameter.
        if(!String(e.excerpt||'').includes(expr))continue;
        const positions=[];let at=m.body.indexOf(expr);while(at>=0){positions.push(m.bodyStart+at);at=m.body.indexOf(expr,at+expr.length);}
        if(!positions.length){record.attempts.push({file:e.file,line:e.line,method:m.name,unlocatedExpression:expr});continue;}
        const expressionAt=positions.reduce((a,b)=>Math.abs(a-absolute)<=Math.abs(b-absolute)?a:b);
        const z=infer(expr,d,m,expressionAt);if(z)found.push(z);else record.evidence.push(proof(e.file,lineAt(d,expressionAt),expr,'producător încă nerezolvat'));
      }
    }
  }
  if(found.length){const types=[...new Set(found.map(x=>x.type))];const dynamic=types.some(t=>t==='Object'||/^Object\b/.test(t));if(!dynamic){record.status='tip_rezolvat_static';record.javaType=types.join(' | ');record.evidence.push(...found.flatMap(x=>x.evidence));}else{record.status=record.coercion?'conversie_documentata':'container_dinamic';record.declaredType=types.join(' | ');record.evidence.push(...found.flatMap(x=>x.evidence));}}
  record.evidence=[...new Map(record.evidence.map(x=>[JSON.stringify(x),x])).values()];record.attempts=[...new Map(record.attempts.map(x=>[JSON.stringify(x),x])).values()];
  if(record.status==='inca_necunoscut')record.next='Urmărire interprocedurală sau Smali pentru consumator/callback; o valoare dinamică poate necesita observație runtime.';
  else if(record.status==='tip_rezolvat_static')record.next='Tip verificat static; validarea domeniului și a comportamentului efectiv rămâne distinctă.';
  else record.next='Se cunoaște conversia sau containerul Java, dar schema acceptată / payloadul concret necesită un pas separat.';
  resolutions.push(record);
}
const reviewedFile=path.join(out,'rezolvari-revizuite.json');
if(fs.existsSync(reviewedFile))for(const review of JSON.parse(fs.readFileSync(reviewedFile,'utf8'))){const r=resolutions.find(x=>x.id===review.id);if(!r)throw Error('Unknown reviewed ID '+review.id);Object.assign(r,review,{evidence:[...r.evidence,...review.evidence]});for(const ev of review.evidence)get(ev.file);}
const dexFile=path.join(out,'tipuri-dex-reverificate.json'),checkedDex=new Set();
if(fs.existsSync(dexFile))for(const v of JSON.parse(fs.readFileSync(dexFile,'utf8')).resolutions){
 for(const e of v.dexEvidence)if(!checkedDex.has(e.file)){const hash=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,e.file))).digest('hex');if(hash!==e.sha256)throw Error('DEX evidence changed '+e.file);checkedDex.add(e.file);}
 const r=resolutions.find(x=>x.id===v.id);if(!r)throw Error('Unknown DEX resolution '+v.id);
 const file=v.wrapper.file.replace('reconstituit/jadx/app/src/main/java/',''),d=get(file),first=v.wrapper.lines[0],last=v.wrapper.lines.at(-1);
 Object.assign(r,{status:'tip_rezolvat_static',javaType:v.javaType,nullable:v.nullable,nullableStatus:v.nullableStatus,dexEvidence:v.dexEvidence,officialSource:v.officialSource,resolutionNote:'Semnătură Android citită independent din DEX și corelată la wrapperul Java.',next:v.limit});
 r.evidence.push(proof(file,first,d.s.split('\n').slice(first-1,last).join('\n'),'wrapper Java; tipul apelului este confirmat separat în DEX'));
}
const fingerprints=[...cache.keys()].sort().map(file=>({file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(src,file))).digest('hex')}));
const summary={date:new Date().toISOString(),apk:'1.0.3899',baselineUnknown:resolutions.length,states:resolutions.reduce((o,x)=>(o[x.status]=(o[x.status]||0)+1,o),{}),method:'Inspecție statică conservatoare: cast, semnătura producătorului, return și conversia locală. Toate cele 199 intrări au un rezultat al încercării; nu sunt 199 semantici complete.',hardwareTested:false,sourceFiles:fingerprints.length};
fs.writeFileSync(path.join(out,'parametri-reverificati.json'),JSON.stringify({summary,resolutions,sourceHashes:fingerprints},null,2));
fs.writeFileSync(path.join(out,'parametri-reverificati.txt'),resolutions.map(r=>[r.id+' · '+r.name+' · '+r.status+(r.javaType?' → '+r.javaType:''),r.coercion||'',r.evidence.map(e=>e.file+':'+e.line+' '+e.excerpt).join('\n'),r.next].join('\n')).join('\n\n'));
console.log(JSON.stringify(summary));
