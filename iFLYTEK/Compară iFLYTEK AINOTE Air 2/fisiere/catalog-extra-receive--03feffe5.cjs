// Resolve same-class JSON parser delegates from the previously opaque BLE branches.
module.exports=function({allFunctions,allParams,paramMap,get,evidence,addParam,link,typeClass,corefile}){
 const core=get(corefile),audit=[];
 for(const f of allFunctions.filter(f=>f.kind==='recepție BLE'&&!f.outputParameterIds.length)){
  const body=f.evidence[0].excerpt,delegates=[];
  for(const call of body.matchAll(/\b([\w$]+)\((strD\d*)\)/g)){
   if(body[call.index-1]==='.')continue;
   const found=core.methods.filter(m=>m.name===call[1]&&m.owner===f.owner&&m.args.length===1&&m.args[0].type==='String');
   if(found.length===1&&!delegates.includes(found[0]))delegates.push(found[0]);
  }
  const record={id:f.id,opt:f.opt,source:corefile,delegates:delegates.map(m=>({name:m.name,line:m.line})),fields:[],status:'payload_delegat_sau_eveniment_fara_campuri_citite'};
  for(const m of delegates){
   const input=m.args[0].name;
   const roots=[...m.body.matchAll(new RegExp('JSONObject\\s+(\\w+)\\s*=\\s*new JSONObject\\('+input+'\\)','g'))].map(x=>x[1]);
   const receiver='(?:new JSONObject\\('+input+'\\)'+(roots.length?'|'+roots.join('|'):'')+')';
   const re=new RegExp(receiver+'\\.(getInt|optInt|getLong|optLong|getString|optString|getBoolean|optBoolean|getJSONObject|optJSONObject|getJSONArray|optJSONArray)\\("([^"\\r\\n]+)"(?:,\\s*([^)]*))?\\)','g');
   for(const z of m.body.matchAll(re)){
    const t=/Int/.test(z[1])?'int':/Long/.test(z[1])?'long':/String/.test(z[1])?'String':/Boolean/.test(z[1])?'boolean':/Array/.test(z[1])?'JSONArray':'JSONObject';
    const line=core.s.slice(0,m.bodyStart+z.index).split('\n').length,ev=evidence(corefile,line,z[0],'citire la rădăcina JSON în parserul delegat '+m.name);
    const fallbackExpression=z[3]?.trim();let fallback;
    if(fallbackExpression!==undefined){
      if(/^-?\d+[Ll]?$/.test(fallbackExpression)&&Number.isSafeInteger(Number(fallbackExpression.replace(/[Ll]$/,''))))fallback=Number(fallbackExpression.replace(/[Ll]$/,''));
      else {try{fallback=JSON.parse(fallbackExpression);}catch{fallback={expression:fallbackExpression};}}
    }
    const p=addParam({scope:f.id+':response',name:z[2],javaType:t,valueClass:typeClass(t),direction:'răspuns BLE',format:'cheie la rădăcina JSON în cadrul BLE',description:'Citire '+z[1]+' în parserul delegat '+m.name+'. Câmpul aparține mesajului primit, nu modelului local.',confidence:'citire verificată static în parser delegat',evidence:[ev],...(fallback!==undefined?{parserFallback:fallback,parserFallbackExpression:fallbackExpression}:{})});
    if(!p.evidence.some(e=>e.file===ev.file&&e.line===ev.line))p.evidence.push(ev);link(f,p,'output');
    (f.schemaPaths||=[]).push({path:z[2],parameterId:p.id,direction:'output',representation:'JSON pe fir; rădăcina parserului delegat '+m.name});
    record.fields.push({name:z[2],type:t,parser:z[1],fallback,helper:m.name,evidence:ev});
   }
   f.evidence.push(evidence(corefile,m.line,m.body,'parser de răspuns delegat '+m.name));
  }
  if(record.fields.length){record.status='campuri_extrase_din_parser_delegat';f.notes.push('Reverificare: câmpurile din helperii JSON au fost adăugate explicit; callbackurile și erorile locale rămân distincte de payload.');for(const relatedId of f.relatedFunctionIds){const command=allFunctions.find(c=>c.id===relatedId&&c.kind==='comandă BLE');if(command)for(const id of f.outputParameterIds)link(command,paramMap.get(id),'output');}}
  else if(/\.r3\(\)/.test(body))record.status='notificare_fara_payload_citit_in_aceasta_ramura';
  f.additionalReceiveReview={status:record.status,delegates:record.delegates,limit:'Analiză a codului client; nu validare a firmware-ului.'};audit.push(record);
 }
 return audit;
};
