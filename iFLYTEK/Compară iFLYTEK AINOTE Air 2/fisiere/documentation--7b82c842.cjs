const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=process.argv[2],out=process.argv[3],local=process.argv[4];
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.join(d,e.name)]);
const save=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof v==='string'?v:JSON.stringify(v,null,2));};
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
function text(s){let m=s.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)||s.match(/<article\b[^>]*>([\s\S]*?)<\/article>/i);if(m)s=m[1];return s.replace(/<(script|style|svg|noscript)\b[^>]*>[\s\S]*?<\/\1>/gi,'').replace(/<(?:br|\/p|\/div|\/h\d|\/li|\/tr)\s*[^>]*>/gi,'\n').replace(/<[^>]+>/g,' ').replace(/&#x([a-f0-9]+);/gi,(_,x)=>String.fromCodePoint(parseInt(x,16))).replace(/&#(\d+);/g,(_,x)=>String.fromCodePoint(+x)).replaceAll('&nbsp;',' ').replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&quot;','"').replace(/[ \t]+/g,' ').replace(/\n\s*\n/g,'\n\n').trim();}
const inputs=[...walk(path.join(root,'original')).filter(f=>/\.html$/.test(f)),...walk(path.join(root,'Software/Biblioteca_Glasses/Documentatie')).filter(f=>/\.html$/.test(f)),...walk(path.join(root,'Software/Cercetare_SDK_2026-10-30')).filter(f=>/\.(md|txt)$/.test(f)),...walk(path.join(root,'Ochelari')).filter(f=>/\.(html|txt|md)$/.test(f))];
let rows=[],seen=new Map(),corpus=[];
for(const f of inputs){const raw=fs.readFileSync(f,'utf8'),plain=/\.html$/.test(f)?text(raw):raw,key=hash(plain),dup=seen.get(key),id=String(rows.length+1).padStart(3,'0');const headings=Array.from(raw.matchAll(/<h[1-6]\b[^>]*>([\s\S]*?)<\/h[1-6]>/gi),m=>text(m[1]));
 const row={id,source:path.relative(root,f).replaceAll('\\','/'),sha256:key,characters:plain.length,duplicateOf:dup??null,title:headings[0]??path.basename(f),headings,file:'corpus/'+id+'.txt'};
 if(dup)row.file=rows.find(r=>r.id===dup).file;else {seen.set(key,id);save(path.join(out,'documentatie',row.file),plain);corpus.push({id,plain});}rows.push(row);
}
save(path.join(out,'documentatie','index.json'),rows);
save(path.join(out,'documentatie','lectura-index.txt'),rows.map(r=>`${r.id} | ${r.source} | ${r.characters} chars | duplicate=${r.duplicateOf??'-'}\n${r.headings.join(' / ')}`).join('\n\n'));
const terms={hardware:/Bluetooth|蓝牙|眼镜|Wi-Fi|teleprompter|提词器|GlassClaw/ig,audio:/PCM|Opus|音频|采样率|sample rate|录音/ig,ai:/ASR|TTS|AIKIT|AIUI|识别|合成/ig,integration:/MCP|AINOTE|Loomy|API|SDK/ig};
let hits={};for(const [key,re]of Object.entries(terms)){hits[key]=[];for(const doc of corpus){let match;re.lastIndex=0;let n=0;while((match=re.exec(doc.plain))&&n++<15)hits[key].push({document:doc.id,offset:match.index,excerpt:doc.plain.slice(Math.max(0,match.index-100),match.index+400)});}}
save(path.join(out,'documentatie','correlations.json'),hits);
const src=path.join(local,'jadx/app/src/main/java'),files=walk(src).filter(f=>f.endsWith('.java'));let channelRows=[],plugins=[],allDomains=new Set(),abi=[];
const reg=fs.readFileSync(path.join(src,'io/flutter/plugins/GeneratedPluginRegistrant.java'),'utf8');
for(const m of reg.matchAll(/getPlugins\(\)\.add\(new ([\w.$]+)\(\)\);[\s\S]*?Error registering plugin ([^,]+), ([^"\n]+)/g))plugins.push({alias:m[1],plugin:m[2],originalClass:m[3]});
for(const f of files){const s=fs.readFileSync(f,'utf8');const rel=path.relative(path.join(local,'jadx'),f).replaceAll('\\','/');
 if(/MethodChannel|EventChannel/.test(s)&&/new (?:MethodChannel|EventChannel)/.test(s)){
  const channels=Array.from(s.matchAll(/new (MethodChannel|EventChannel)\([^;\n]{0,300}/g),m=>({kind:m[1],expression:m[0]}));
  const methods=[...new Set(Array.from(s.matchAll(/(?:\.equals\(|case\s+)\s*"([\w.\/-]{1,100})"/g),m=>m[1]))];
  const keys=[...new Set(Array.from(s.matchAll(/\.argument\("([\w.\/-]{1,100})"\)/g),m=>m[1]))];
  const cls=path.basename(f,'.java');channelRows.push({class:cls,file:rel,channels,methodCandidates:methods,argumentKeys:keys});
 }
 if(/com[\\/]example|easytrans|translateapp/.test(f))for(const m of s.matchAll(/https?:\/\/([a-zA-Z0-9.-]+)(?=[:/"\s])/g))allDomains.add(m[1]);
}
save(path.join(out,'inventar','flutter-plugins.json'),plugins);save(path.join(out,'inventar','flutter-channel-contracts.json'),channelRows);save(path.join(out,'inventar','network-host-references.json'),[...allDomains].sort());
save(path.join(out,'documentatie','flutter-contracts.txt'),channelRows.map(r=>`${r.class}\n${r.file}\nCHANNELS\n${r.channels.map(c=>c.expression).join('\n')}\nMETHOD NAME CANDIDATES (must inspect dispatch)\n${r.methodCandidates.join(', ')}\nARGUMENT KEY CANDIDATES\n${r.argumentKeys.join(', ')}\n`).join('\n'));
const summary={documents:rows.length,uniqueDocuments:seen.size,uniqueCharacters:corpus.reduce((n,c)=>n+c.plain.length,0),flutterPlugins:plugins.length,channelClasses:channelRows.length,channelExpressions:channelRows.reduce((n,r)=>n+r.channels.length,0)};
save(path.join(out,'documentatie','summary.json'),summary);console.log(JSON.stringify(summary));
