'use strict';
function normalizeDefaults(text) {
  // DEX omitted static initial values are type-appropriate zero/null.
  return text.replace(/^(\.field[^\r\n]*\bstatic\b[^\r\n]*:)([^\s=]+) = ([^\r\n]+)$/gm,(all,prefix,type,value)=>{
    const zero=(type==='Z'&&value==='false') || (/^(?:L[^;]+;|\[.+)$/.test(type)&&value==='null') ||
      (type==='I'&&value==='0x0') || (type==='J'&&value==='0x0L');
    return zero?prefix+type:all;
  });
}
function normalizeMethod(method) {
  const lines=method.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
  const labels=new Map(), catches=[], body=[];
  let instruction=0;
  for(const line of lines) {
    if(line.startsWith(':')) labels.set(line,instruction);
    const handler=line.match(/^\.catch\s+(\S+)\s+\{(:\S+)\s+\.\.\s+(:\S+)\}\s+(:\S+)$/);
    const catchall=line.match(/^\.catchall\s+\{(:\S+)\s+\.\.\s+(:\S+)\}\s+(:\S+)$/);
    if(handler) { catches.push({type:handler[1],start:handler[2],end:handler[3],target:handler[4]}); continue; }
    if(catchall) { catches.push({type:'*',start:catchall[1],end:catchall[2],target:catchall[3]}); continue; }
    if(/^:try_(?:start|end)_\w+$/.test(line)) continue;
    // Decline normalization if a try-boundary label is also a branch target.
    if(/:try_(?:start|end)_/.test(line)) return method;
    body.push(line);
    if(/^[a-z][a-z0-9/-]*(?:\s|$)/.test(line)) instruction++;
  }
  const coverage=new Map();
  for(const h of catches) {
    const start=labels.get(h.start),end=labels.get(h.end),target=labels.get(h.target);
    if(start===undefined||end===undefined||target===undefined||end<start) return method;
    for(let i=start;i<end;i++) {
      if(!coverage.has(i)) coverage.set(i,[]);
      coverage.get(i).push([h.type,target]);
    }
  }
  return body.join('\n')+'\nEXCEPTION_COVERAGE='+JSON.stringify([...coverage].sort((a,b)=>a[0]-b[0]));
}
function normalizeSmali(text) {
  return normalizeDefaults(text).replace(/^\.method\b[\s\S]*?^\.end method$/gm,normalizeMethod);
}
function normalizeAttrs(text) {
  return text.replace(/(<attr\b[^>]*?(?<!\/)>)(([\s\S]*?))(<\/attr>)/g,(all,start,body,_inner,end)=>{
    const children=body.match(/<(?:enum|flag)\b[^>]*\/>/g)||[];
    if(!children.length||body.replace(/<(?:enum|flag)\b[^>]*\/>/g,'').trim()) return all;
    return start+'\n'+children.map(s=>s.trim()).sort().join('\n')+'\n'+end;
  });
}
module.exports={normalizeSmali,normalizeAttrs};
