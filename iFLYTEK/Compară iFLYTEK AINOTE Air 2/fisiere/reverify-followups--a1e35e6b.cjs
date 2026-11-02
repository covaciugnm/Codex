// Read-only triage of the remaining queues. It does not promote candidates to API methods.
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),out=path.join(root,'reverificare-detaliata');
const read=f=>JSON.parse(fs.readFileSync(path.join(root,f),'utf8').replace(/^\uFEFF/,''));
const prefix=fs.readFileSync(path.join(__dirname,'catalog-extract.cjs'),'utf8').split('function resolve(')[0];
const ctx={require,__dirname,console};vm.runInNewContext(prefix+'\nglobalThis.reader={get,src,mask,cache};',ctx);const {get,src,cache}=ctx.reader;
const functions=read('catalog-parametri-functii/functii.json'),params=read('catalog-parametri-functii/parametri.json'),old=read('reverificare-detaliata/baseline-indicatori.json');
const channelAudit=read('catalog-parametri-functii/audit-flutter.json');
const candidates=[];
for(const a of channelAudit)for(const [n,name] of (a.unresolvedCandidates||[]).entries()){
 const d=get(a.file),occurrences=[];let from=0,needle=JSON.stringify(name),at;
 while((at=d.s.indexOf(needle,from))>=0){
  from=at+needle.length;const m=d.methods.filter(x=>x.start<at&&x.end>at).sort((a,b)=>(a.end-a.start)-(b.end-b.start))[0];
  const line=d.s.slice(0,at).split('\n').length,text=d.s.split('\n')[line-1].trim();
  const context=m?m.body.slice(0,at-m.bodyStart):'';
  const methodVars=[...context.matchAll(/(?:String\s+)?(\w+)\s*=\s*\w+\.method\s*;/g)].map(x=>x[1]);
  const isMethodCompare=(m?.args.some(x=>/MethodCall$/.test(x.type))||/\bMethodCall\s/.test(m?.signature||''))&&(/\.method\.equals\(/.test(text)||methodVars.some(v=>new RegExp('\\b'+v+'\\.equals\\(').test(text)||new RegExp('\\.equals\\('+v+'\\)').test(text)));
  occurrences.push({line,excerpt:text,owner:m?.owner,method:m?.name,methodCallComparison:!!isMethodCompare,decompilationIssue:!!m?.body.includes('Method not decompiled')});
 }
 const classification=occurrences.some(x=>x.methodCallComparison)?'comparatie_cu_MethodCall_method_observata':occurrences.every(x=>x.decompilationIssue)?'corp_nedecompilat_sau_indiciu_in_comentariu':'alta_comparatie_sau_constanta';
 candidates.push({id:'candidate:'+a.file+':'+n,name,file:a.file,classification,occurrences,next:classification==='comparatie_cu_MethodCall_method_observata'?'Reconstituirea ramurii, argumentelor, rezultatelor și condițiilor de înregistrare; nu este adăugată automat în catalog.':'Urmărirea semantică a variabilei comparate / verificare în Smali dacă Java este incomplet.',limit:'Triage lexical pe sursa Java, nu confirmare a unei funcții invocabile sau a unui contract complet.'});
}
const remaining=functions.filter(f=>(f.kind==='Flutter MethodChannel'&&(!f.outputParameterIds.length||!f.resultObservations?.length))||(f.kind==='recepție BLE'&&!f.schemaPaths?.length)).map(f=>{
 const evidence=f.evidence||[],text=evidence.map(e=>e.excerpt||'').join('\n');
 return {id:f.id,name:f.name,kind:f.kind,source:f.source,line:f.line,hasOutputs:!!f.outputParameterIds.length,hasResultObservations:!!f.resultObservations?.length,hasSchemaPaths:!!f.schemaPaths?.length,
  checked:'Ramura și helperii deja atribuiți au fost rescanați pentru producători expliciți, delegări, chei JSON și limite de decompilare. Nu este analiză manuală integrală a fiecărei ramuri.',
  indicators:{errorOrNotImplemented:/\.(?:error|notImplemented)\(/.test(text),resultForwardHelper:/\b(?:V2|U2|gg3\.[a-z])\(/.test(text),delegates:f.delegateExpressions||[],helpers:f.helperMethods||[],javaDecompilationWarning:/Method not decompiled|JADX (?:ERROR|WARN)/.test(text)},
  status:f.listenerTrace?.status||(f.resultObservations?.length?'observatii_existente_schema_completa_neconfirmata':f.outputParameterIds.length?'campuri_existente_fara_cai_explicite':'delegari_sau_rezultate_neatribuite_complet'),
  next:f.listenerTrace?.detail||'Urmărește proprietarul callbackului și condițiile; confirmă numai câmpurile citite sau produse, păstrând separat wire, model local și rezultat Flutter.',evidence:evidence.map(e=>({file:e.file,line:e.line,role:e.role}))};
});
const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const protocol=read('protocol-comunicare/source-provenance.json').map(e=>({...e,currentSha256:hash(path.join(src,e.file)),matches:hash(path.join(src,e.file))===e.sha256}));
const proofSpecs=[
 ['com/iflytek/fanyi/blc/service/impl/TranslateServiceImpl.java',/buildDescriptor|create\w+Stream|X-sign/, 'Nouă fabrici gRPC; numele rutei vine din argument, nu dintr-un nume fix de model.'],
 ['translate_sdk/ClientHost.java',/public (String|int)/,'Host/port/certificate sunt configurabile.'],
 ['translate_sdk/BaseClientParams.java',/llmtransparam|translator|hostId|public String path/,'llmtransparam este Map; nu identifică versiunea unui model server.'],
 ['com/alipay/verifyiotidentity/obfuscated/nh1.java',/llmtransparam/,'Map transmis de apelant; modelul activ nu rezultă din simpla prezență a cheii.'],
 ['com/example/recorde_translate_plugin/glass/GlassOTAManager.java',/otaFilePath = .*getFilesDir/,'Calea implicită a descărcării este în spațiul privat al aplicației; existența codului nu înseamnă că fișierul este prezent.']
];
const technical=proofSpecs.map(([file,pattern,conclusion])=>{const d=get(file);if(!d)throw Error('Missing technical source '+file);return {file,conclusion,sha256:hash(path.join(src,file)),observations:d.s.split('\n').flatMap((s,i)=>pattern.test(s)?[{line:i+1,excerpt:s.trim()}]:[])};});
const countBy=(xs,k)=>xs.reduce((o,x)=>(o[x[k]]=(o[x[k]]||0)+1,o),{});
const summary={date:new Date().toISOString(),method:'Triage automat delimitat și verificări punctuale în sursă. Categoriile nu sunt un scor de rezolvare semantică.',candidateOccurrences:candidates.length,candidateStates:countBy(candidates,'classification'),remainingFunctionRecords:remaining.length,remainingStates:countBy(remaining,'status'),protocolSourceHashes:protocol.length,protocolSourcesUnchanged:protocol.every(x=>x.matches),hardwareTested:false,cloudTested:false,firmwareImageAvailable:false};
fs.writeFileSync(path.join(out,'cozi-reverificate.json'),JSON.stringify({summary,candidates,remaining,protocol,technical,sourceHashes:[...cache.keys()].map(file=>({file,sha256:hash(path.join(src,file))}))},null,2));
console.log(JSON.stringify(summary));
