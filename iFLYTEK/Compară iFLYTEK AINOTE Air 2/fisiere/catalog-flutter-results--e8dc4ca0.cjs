// Extract only explicit Result/EventSink producers in an already assigned dispatch block.
// Dynamic maps and delegated bodies remain marked as incomplete, never invented schemas.
module.exports=function({f,block,get,mask,close,split,resolve,evidence,addParam,link,typeClass}){
  const d=get(block.file), masked=mask(block.body);
  const resultNames=new Set([...d.s.matchAll(/\b(?:MethodChannel\.)?Result\s+(\w+)/g)].map(x=>x[1]));
  // q98 is verified to implement MethodChannel.Result and forward success/error once.
  const safeResultFile='com/alipay/verifyiotidentity/obfuscated/q98.java',safeResult=get(safeResultFile);
  const safeResultNames=new Set();
  if(safeResult?.s.includes('class q98 implements MethodChannel.Result'))for(const a of d.s.matchAll(/\bq98\s+(\w+)\s*=\s*q98\.b\(/g)){resultNames.add(a[1]);safeResultNames.add(a[1]);}
  const envelopeFile='com/alipay/verifyiotidentity/obfuscated/w18.java',envelope=get(envelopeFile);
  const envelopeMethod=envelope?.methods.find(m=>m.name==='a'&&m.args.length===0&&m.body.includes('map.put("code", this.a)'));
  const h0=d.methods.find(m=>m.owner==='com.alipay.verifyiotidentity.obfuscated.nh1'&&m.name==='h0'&&m.body.includes('return new w18(PluginDefineResponseCode.SUCCESS.getCode(), str, true, null)'));
  const envelopeExpr=expr=>envelopeMethod&&(/^new w18\([\s\S]*\)\.a\(\)$/.test(expr)||(h0&&/^h0\("(?:\\.|[^"\\])*"\)\.a\(\)$/.test(expr)));
  const eventNames=new Set([...d.s.matchAll(/\b(?:EventChannel\.)?EventSink\s+(\w+)/g)].map(x=>x[1]));
  function valueType(expr){
    if(/^new (?:HashMap|LinkedHashMap|Map)\b/.test(expr))return 'Map';
    if(envelopeExpr(expr))return 'Map<String, Object>';
    if(/^new (?:ArrayList|List)\b/.test(expr))return 'List';
    if(/^Boolean\.(?:TRUE|FALSE)|^(?:true|false)$|^Boolean\.valueOf\(/.test(expr))return 'boolean';
    if(/^Integer\.valueOf\(|^-?\d+$/.test(expr))return 'int';
    if(/^Long\.valueOf\(|^-?\d+L$/.test(expr))return 'long';
    if(/^"(?:\\.|[^"\\])*"$/.test(expr))return 'String';
    if(expr==='null')return 'null';
    return 'necunoscut';
  }
  function addValue(scope,name,expr,ev,kind){
    const type=valueType(expr),p=addParam({scope:f.id+':'+scope,name,javaType:type,valueClass:typeClass(type),
      format:'Flutter StandardMessageCodec / '+kind,direction:'ieșire Flutter / '+kind,
      description:'Valoare transmisă explicit de producătorul '+kind+'. Expresiile și sursele sunt păstrate; structura delegată poate fi incompletă.',
      confidence:'producător observat static',evidence:[]});
    p.evidence.push(ev);p.observedExpressions=[...new Set([...(p.observedExpressions||[]),expr])];
    if(envelopeExpr(expr)){
      const proof=evidence(envelopeFile,envelopeMethod.line,envelopeMethod.body,'w18.a(): câmpuri ale rezultatului Flutter');
      p.evidence.push(proof);f.evidence.push(proof);
      p.envelope={owner:'w18',fields:{code:'String',message:'String',data:'Map<String, Object> | null',success:'boolean'},limit:'Structura data este dinamică; acest rezultat local nu confirmă operația pe dispozitiv sau în cloud.'};
      if(/^h0\(/.test(expr)){const hp=evidence(block.file,h0.line,h0.body,'h0(): înveliș w18 cu success=true și data=null');p.evidence.push(hp);f.evidence.push(hp);}
    }
    const types=new Set([...(p.observedJavaTypes||[]),type]);p.observedJavaTypes=[...types];
    p.javaType=[...types].join(' | ');p.valueClass=types.size>1?'uniune de reprezentări':typeClass(type);
    link(f,p,'output');return p;
  }
  for(const m of masked.matchAll(/\b([\w$.]+)\.(success|error|notImplemented)\s*\(/g)){
    const receiver=m[1].split('.').pop(),kind=eventNames.has(receiver)?'EventChannel.EventSink':resultNames.has(receiver)?'MethodChannel.Result':null;
    if(!kind)continue;
    if(safeResultNames.has(receiver)){
      const proof=evidence(safeResultFile,10,safeResult.s.split('\n').slice(9,67).join('\n'),'q98 implementează Result; transmite cel mult un success/error/notImplemented');
      if(!f.evidence.some(e=>e.file===safeResultFile&&e.role===proof.role))f.evidence.push(proof);
      f.resultForwarding='q98 folosește AtomicBoolean: după primul rezultat, apelurile ulterioare sunt ignorate.';
    }
    const open=m.index+m[0].lastIndexOf('('),end=close(masked,open,'(',')'),args=split(block.body.slice(open+1,end));
    const expression=block.body.slice(m.index,end+1),ev=evidence(block.file,d.s.slice(0,block.start+m.index).split('\n').length,expression,block.role+' / '+kind);
    (f.resultObservations||=[]).push({kind,method:m[2],receiver:m[1],arguments:args,evidence:ev});
    if(f.name==='startGlassOTA')continue; // separately verified callback variants in catalog-response-contracts.
    if(m[2]==='success'){
      const expr=args[0]||'null';
      if(kind==='MethodChannel.Result')addValue('result','result',expr,ev,kind);
      if(kind==='EventChannel.EventSink'){
        const variant={kind,method:'success',valueExpression:expr,fields:[],evidence:ev,coverage:'doar câmpurile put() ale producătorului local identificat; condițiile sunt în sursă'};
        const before=block.body.slice(0,m.index),escaped=expr.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
        if(/^\w+$/.test(expr)){
          const declarations=[...before.matchAll(new RegExp('\\b(?:HashMap|LinkedHashMap|Map)(?:<[^;=]+>)?\\s+'+escaped+'\\s*=\\s*new\\s+(?:HashMap|LinkedHashMap)\\b[^;]*;', 'g'))];
          const decl=declarations.at(-1);
          if(decl){const tail=before.slice(decl.index+decl[0].length),tailMask=mask(tail);
            for(const put of tailMask.matchAll(new RegExp('\\b'+escaped+'\\.put\\s*\\(', 'g'))){
              const po=put.index+put[0].lastIndexOf('('),pe=close(tailMask,po,'(',')'),pa=split(tail.slice(po+1,pe));
              if(pa.length!==2)continue;
              const key=resolve(pa[0],block.file);if(typeof key!=='string')continue;
              const at=block.start+decl.index+decl[0].length+put.index,putEv=evidence(block.file,d.s.slice(0,at).split('\n').length,tail.slice(put.index,pe+1),'producător Map pentru EventSink');
              const p=addValue('event',key,pa[1],putEv,kind);
              variant.fields.push({name:key,parameterId:p.id,valueExpression:pa[1]});
            }
          }
        }
        if(!variant.fields.length)variant.unknown='Conținut dinamic / delegat; nu s-a atribuit automat o schemă.';
        (f.eventProducerObservations||=[]).push(variant);
      }
    }
    if(m[2]==='error'){
      (f.resultErrorContracts||=[]).push({kind,code:args[0],message:args[1],details:args[2],evidence:ev});
    }
  }
};
