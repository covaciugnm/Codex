const fs=require('fs'),path=require('path'),crypto=require('crypto');
const local=process.argv[2],out=process.argv[3],workspace=process.argv[4];
const inv=path.join(out,'inventar');fs.mkdirSync(inv,{recursive:true});
const save=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof v==='string'?v:JSON.stringify(v,null,2));};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.join(d,e.name)]);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty=t=>t&&t.startsWith('L')?t.slice(1,-1).replaceAll('/','.'):t;
function dex(file){
 const b=fs.readFileSync(file),u=o=>b.readUInt32LE(o),u16=o=>b.readUInt16LE(o);
 if(b.toString('ascii',0,4)!=='dex\n')throw Error('Not DEX '+file);
 function leb(p){let v=0,s=0,x;do{x=b[p.i++];v|=(x&127)<<s;s+=7;if(s>35)throw Error('ULEB overflow');}while(x&128);return v>>>0;}
 const strings=Array.from({length:u(56)},(_,i)=>{let p={i:u(u(60)+4*i)};leb(p);let end=b.indexOf(0,p.i);return b.toString('utf8',p.i,end);});
 const types=Array.from({length:u(64)},(_,i)=>strings[u(u(68)+4*i)]);
 const protos=Array.from({length:u(72)},(_,i)=>{const o=u(76)+12*i,a=u(o+8);return {returnType:types[u(o+4)],args:a?Array.from({length:u(a)},(_,j)=>types[u16(a+4+2*j)]):[]};});
 const fieldIds=Array.from({length:u(80)},(_,i)=>{const o=u(84)+8*i;return {owner:pretty(types[u16(o)]),type:types[u16(o+2)],name:strings[u(o+4)]};});
 const methodIds=Array.from({length:u(88)},(_,i)=>{const o=u(92)+8*i;return {owner:pretty(types[u16(o)]),...protos[u16(o+2)],name:strings[u(o+4)]};});
 let classes=[];
 for(let i=0;i<u(96);i++){
  const o=u(100)+32*i,name=pretty(types[u(o)]),iface=u(o+12),src=u(o+16),data=u(o+24),superId=u(o+8);
  const c={name,dex:path.basename(file),access:u(o+4),super:superId===0xffffffff?null:pretty(types[superId]),interfaces:iface?Array.from({length:u(iface)},(_,j)=>pretty(types[u16(iface+4+2*j)])):[],sourceFile:src===0xffffffff?null:strings[src],fields:[],methods:[]};
  if(data){const p={i:data},counts=[leb(p),leb(p),leb(p),leb(p)];
   for(let group=0;group<4;group++){let id=0;for(let j=0;j<counts[group];j++){id+=leb(p);const access=leb(p);if(group<2)c.fields.push({...fieldIds[id],access,storage:group===0?'static':'instance'});else c.methods.push({...methodIds[id],access,codeOffset:leb(p),kind:group===2?'direct':'virtual'});}}
  }
  classes.push(c);
 }
 return {classes,summary:{file:path.basename(file),version:b.toString('ascii',4,7),sha256:hash(b),classDefs:u(96),methodReferences:u(88),fieldReferences:u(80),declaredMethods:classes.reduce((n,c)=>n+c.methods.length,0),declaredFields:classes.reduce((n,c)=>n+c.fields.length,0)}};
}
let classes=[],dexSummary=[];
for(const f of fs.readdirSync(path.join(local,'raw')).filter(n=>/^classes\d*\.dex$/.test(n))){const d=dex(path.join(local,'raw',f));classes.push(...d.classes);dexSummary.push(d.summary);}
save(path.join(inv,'dex-summary.json'),dexSummary);
save(path.join(inv,'api-complete.json'),classes);
function moduleFor(c){const n=c.name;
 if(/easytrans\.headset/.test(n))return 'Bluetooth-ochelari-casti';
 if(/easytrans\.core\.opus/.test(n))return 'Audio-Opus';
 if(/^com\.example\./.test(n))return 'Pluginuri-Flutter';
 if(/^com\.iflytek\.(aikit|aiui|speech|cloud)/.test(n))return 'Motoare-AI-iFLYTEK';
 if(/^com\.iflytek\./.test(n))return 'iFLYTEK-alte-module';
 if(/^com\.antgroup\.glasses|^com\.alipay\.android\.glass/.test(n))return 'Servicii-Ant-Glasses';
 if(/^com\.alipay\.verifyiotidentity\.obfuscated\./.test(n))return 'Obfuscat-origine-mixta';
 if(/^com\.alipay/.test(n))return 'Alipay';
 if(/^(io\.flutter|kotlin|kotlinx|android|androidx)\./.test(n))return 'Framework-runtime';
 if(/^(okhttp|okio|retrofit|com\.google\.gson)/.test(n))return 'Retea-serializare';
 return 'Alte-dependente';
}
let packages={},modules={},nativeMethods=[];
const apiDir=path.join(out,'api');fs.mkdirSync(apiDir,{recursive:true});let apiTexts={};
for(const c of classes){const pkg=c.name.slice(0,c.name.lastIndexOf('.')),mod=moduleFor(c);c.module=mod;
 const entry=packages[pkg]??={package:pkg,classes:0,methods:0,fields:0};entry.classes++;entry.methods+=c.methods.length;entry.fields+=c.fields.length;
 const m=modules[mod]??={name:mod,classes:0,methods:0,fields:0};m.classes++;m.methods+=c.methods.length;m.fields+=c.fields.length;
 (apiTexts[mod]??=[]).push(`\nCLASS ${c.name}\nDEX ${c.dex}; source ${c.sourceFile??'unknown'}; flags 0x${c.access.toString(16)}\nEXTENDS ${c.super}\nIMPLEMENTS ${c.interfaces.join(', ')}\n`+c.fields.map(f=>` FIELD 0x${f.access.toString(16)} ${f.type} ${f.name}`).join('\n')+'\n'+c.methods.map(m=>` METHOD 0x${m.access.toString(16)} ${m.returnType} ${m.name}(${m.args.join(', ')}) @${m.codeOffset}`).join('\n'));
 for(const m of c.methods)if(m.access&0x100)nativeMethods.push(m);
}
for(const [mod,lines] of Object.entries(apiTexts))save(path.join(apiDir,mod+'.txt'),lines.join('\n'));
save(path.join(inv,'packages.json'),Object.values(packages).sort((a,b)=>b.classes-a.classes));save(path.join(inv,'modules.json'),Object.values(modules));save(path.join(inv,'jni-methods.json'),nativeMethods);
save(path.join(inv,'classes.tsv'),'class\tdex\tsourceFile\tmethods\tfields\tmodule\n'+classes.map(c=>[c.name,c.dex,c.sourceFile??'',c.methods.length,c.fields.length,c.module].join('\t')).join('\n'));
const sourceDir=path.join(local,'jadx/app/src/main/java'),sourceFiles=walk(sourceDir).filter(f=>f.endsWith('.java'));
let failures=[],channels=[],methods=[],imports={},functional=[];
for(const f of sourceFiles){const s=fs.readFileSync(f,'utf8'),rel=path.relative(path.join(local,'jadx'),f).replaceAll('\\','/');
 const fail=(s.match(/Method not decompiled/g)||[]).length,warn=(s.match(/JADX (?:WARN|ERROR)/g)||[]).length;if(fail||warn)failures.push({file:rel,notDecompiled:fail,warnings:warn});
 if(/com[\\/]example|easytrans|translateapp/.test(f)){
  for(const m of s.matchAll(/new (?:MethodChannel|EventChannel)\([^;\n]{0,300}/g))channels.push({file:rel,expression:m[0]});
  for(const m of s.matchAll(/(?:case|equals\()\s*"([^"\n]{1,100})"/g))methods.push({file:rel,name:m[1]});
  const deps=Array.from(s.matchAll(/^import ([\w.$]+);/gm),m=>m[1]);imports[rel]=deps;
 }
 if(/easytrans|com[\\/]example|translateapp/.test(f)){
  const keys=['Bluetooth','Recorder','Player','Camera','Wifi','WiFi','Teleprompter','Translation','Translate','Audio','Video','Photo','Meeting','Subtitle','Record','Opus','GlassClaw','Document','Mcp','Offline'];
  const hit=keys.filter(k=>s.includes(k));if(hit.length)functional.push({file:rel,keywords:hit});
 }
}
save(path.join(inv,'decompilation-issues.json'),failures);save(path.join(inv,'flutter-channels.json'),channels);save(path.join(inv,'plugin-method-candidates.json'),methods);save(path.join(inv,'plugin-dependencies.json'),imports);save(path.join(inv,'functional-source-map.json'),functional);
const rawFiles=walk(path.join(local,'raw'));let files=rawFiles.map(f=>{let b=fs.readFileSync(f);return {file:path.relative(path.join(local,'raw'),f).replaceAll('\\','/'),bytes:b.length,sha256:hash(b)};});save(path.join(inv,'apk-files.json'),files);
const manifest=fs.readFileSync(path.join(local,'jadx/app/src/main/AndroidManifest.xml'),'utf8');
const permissions=[...new Set(Array.from(manifest.matchAll(/<uses-permission\b[^>]*android:name="([^"]+)"/gs),m=>m[1]))];
const components=Array.from(manifest.matchAll(/<(activity|service|receiver|provider|activity-alias)\b([^>]+)>?/g),m=>({kind:m[1],attributes:m[2].trim()}));
save(path.join(inv,'android-components.json'),{package:manifest.match(/\bpackage="([^"]+)"/)?.[1],version:manifest.match(/android:versionName="([^"]+)"/)?.[1],permissions,components});
// ELF64 section/symbol metadata. No machine code is executed.
let natives=[];
for(const f of rawFiles.filter(f=>f.endsWith('.so'))){const b=fs.readFileSync(f);if(b.toString('hex',0,4)!=='7f454c46'||b[4]!==2||b[5]!==1){natives.push({file:path.basename(f),unsupported:true});continue;}
 const shoff=Number(b.readBigUInt64LE(40)),size=b.readUInt16LE(58),count=b.readUInt16LE(60),stridx=b.readUInt16LE(62);
 const raw=Array.from({length:count},(_,i)=>{const o=shoff+i*size;return {nameId:b.readUInt32LE(o),type:b.readUInt32LE(o+4),offset:Number(b.readBigUInt64LE(o+24)),size:Number(b.readBigUInt64LE(o+32)),link:b.readUInt32LE(o+40),entrySize:Number(b.readBigUInt64LE(o+56))};});
 const str=raw[stridx];const cstr=(offset)=>{const end=b.indexOf(0,offset);return b.toString('utf8',offset,end<0?b.length:end);};
 const sections=raw.map(s=>({...s,name:cstr(str.offset+s.nameId)}));let symbols=[],needed=[];
 for(const s of sections.filter(s=>s.type===11||s.type===2)){const strings=sections[s.link];for(let o=s.offset;o<s.offset+s.size;o+=s.entrySize||24){const id=b.readUInt32LE(o);if(!id)continue;const name=cstr(strings.offset+id);symbols.push({name,binding:b[o+4]>>>4,type:b[o+4]&15,section:b.readUInt16LE(o+6),value:b.readBigUInt64LE(o+8).toString(),size:b.readBigUInt64LE(o+16).toString()});}}
 for(const s of sections.filter(s=>s.type===6)){const strings=sections[s.link];for(let o=s.offset;o<s.offset+s.size;o+=16)if(b.readBigInt64LE(o)===1n)needed.push(cstr(strings.offset+Number(b.readBigUInt64LE(o+8))));}
 const info={file:path.relative(path.join(local,'raw'),f).replaceAll('\\','/'),machine:b.readUInt16LE(18),bytes:b.length,sha256:hash(b),needed,sections,symbols};
 const name=path.basename(f);save(path.join(out,'nativ',name+'.json'),info);
 natives.push({file:info.file,bytes:b.length,symbols:symbols.length,jni:symbols.filter(s=>s.name.startsWith('Java_')).length,needed});
 if(name==='libapp.so'){const strings=(b.toString('latin1').match(/[\x20-\x7e]{8,}/g)||[]).filter(s=>s.length<300&&/(?:package:[\w/.-]+\.dart|\.dart$|MethodChannel|EventChannel|flutter\/|recorde_translate|glassclaw|teleprompter)/i.test(s));save(path.join(out,'nativ','dart-aot-identifiers.txt'),[...new Set(strings)].sort().join('\n'));}
}
save(path.join(inv,'native-libraries.json'),natives);
const compact=classes.map(c=>({n:c.name,d:c.dex,s:c.sourceFile,m:c.methods.length,f:c.fields.length,g:c.module}));save(path.join(inv,'classes.js'),'window.APK_CLASSES='+JSON.stringify(compact)+';');
const summary={apkFiles:files.length,apkUncompressedBytes:files.reduce((n,f)=>n+f.bytes,0),dexFiles:dexSummary.length,classes:classes.length,declaredMethods:classes.reduce((n,c)=>n+c.methods.length,0),declaredFields:classes.reduce((n,c)=>n+c.fields.length,0),javaFiles:sourceFiles.length,javaFilesWithIssues:failures.length,methodsNotDecompiled:failures.reduce((n,f)=>n+f.notDecompiled,0),nativeLibraries:natives.length,nativeJavaMethods:nativeMethods.length,flutterChannelExpressions:channels.length,pluginMethodCandidates:methods.length,permissions:permissions.length,components:components.length};save(path.join(inv,'summary.json'),summary);console.log(JSON.stringify(summary));
