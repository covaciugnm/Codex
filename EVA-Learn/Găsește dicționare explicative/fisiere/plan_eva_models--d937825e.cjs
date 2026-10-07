const fs=require('fs'),p=require('path'),crypto=require('crypto');
const root='\\\\192.168.100.169\\Comun\\00.Roboti\\EVA.Pro\\Learn\\EVA_LEARN_DB_35';
const groups=JSON.parse(fs.readFileSync(p.join(root,'00_Administrare','limbi.json'),'utf8'));
const cat=JSON.parse(fs.readFileSync(p.join(__dirname,'catalogue_source.json'),'utf8'));
const jobs=new Map(),refs=[],issues=[];
const byName=new Map(groups.slice(5).map((g,i)=>[i+1,g]));
function add(url,relative,kind,meta={}){if(!jobs.has(url))jobs.set(url,{id:crypto.createHash('sha256').update(url).digest('hex').slice(0,12),url,path:relative,kind,status:'pending',...meta});}
async function hf(repo,relative,filter,meta){try{const r=await fetch('https://huggingface.co/api/models/'+repo,{signal:AbortSignal.timeout(45000)});if(!r.ok)throw Error('HTTP '+r.status);const d=await r.json();fs.mkdirSync(p.join(root,relative),{recursive:true});fs.writeFileSync(p.join(root,relative,'HF_METADATA.json'),JSON.stringify({id:d.id,sha:d.sha,gated:d.gated,license:d.cardData?.license},null,2));const names=d.siblings.map(s=>s.rfilename);for(const file of names.filter(filter)){if(file.includes('..'))continue;add('https://huggingface.co/'+repo+'/resolve/'+d.sha+'/'+file,p.join(relative,...file.split('/')),meta.kind,meta);}return {names,sha:d.sha,gated:d.gated,license:d.cardData?.license};}catch(e){issues.push({repo,error:e.message});return null;}}
(async()=>{
 const offline=cat.find(s=>s.name==='TTS_30').rows.filter(r=>r[5].includes('Desc'));
 const distinct=[...new Map(offline.map(r=>[r[3],r])).values()];
 for(const row of distinct){
  const g=byName.get(row[0]),repo=row[3];const relative=repo.includes('IndicF5')?p.join('00_Modele_comune','TTS','IndicF5'):p.join(g.folder,'03_TTS',repo.replace('/','__'));
  const m=await hf(repo,relative,f=>/README|LICENSE|config.*json|vocab.*json|tokenizer.*json|special_tokens.*json/i.test(f)||f.endsWith('.safetensors'),{kind:'TTS',repo,languageGroup:g.folder,license:row[6]});
  if(m&&!m.names.some(f=>f.endsWith('.safetensors'))){for(const file of m.names.filter(f=>f.endsWith('pytorch_model.bin')))add('https://huggingface.co/'+repo+'/resolve/'+m.sha+'/'+file,p.join(relative,file),'TTS',{repo,languageGroup:g.folder,license:row[6]});}
  for(const sharedRow of offline.filter(r=>r[3]===repo)){const gg=byName.get(sharedRow[0]);refs.push({group:gg.folder,type:'TTS',repo,path:relative,license:row[6],availability:m?'Metadate publice; vezi raportul descărcării':'Metadate neconfirmate',variant:row[8]});}
 }
 const vp=await fetch('https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json');const voices=await vp.json();
 fs.writeFileSync(p.join(root,'00_Administrare','piper_voices.json'),JSON.stringify(voices));
 for(const g of groups){
  const candidates=Object.entries(voices).filter(([k,v])=>g.codes.includes(v.language?.code?.split('_')[0])||g.codes.includes(v.language?.family));
  candidates.sort((a,b)=>(a[1].quality==='medium'?0:1)-(b[1].quality==='medium'?0:1)||Object.values(a[1].files).reduce((s,f)=>s+(f.size_bytes||0),0)-Object.values(b[1].files).reduce((s,f)=>s+(f.size_bytes||0),0));
  if(!candidates.length)continue;const [key,v]=candidates[0],relative=p.join(g.folder,'03_TTS','Piper',key);
  for(const [file,meta] of Object.entries(v.files)){if(file.includes('..'))continue;add('https://huggingface.co/rhasspy/piper-voices/resolve/main/'+file,p.join(relative,...file.split('/')),'TTS',{repo:'rhasspy/piper-voices',languageGroup:g.folder,license:'Consultă MODEL_CARD; licența fiecărei voci diferă',expectedMd5:meta.md5_digest});}
  const modelFile=Object.keys(v.files).find(f=>f.endsWith('.onnx'));if(modelFile)add('https://huggingface.co/rhasspy/piper-voices/resolve/main/'+modelFile.slice(0,modelFile.lastIndexOf('/')+1)+'MODEL_CARD',p.join(relative,'MODEL_CARD'),'TTS',{repo:'rhasspy/piper-voices',languageGroup:g.folder});
  refs.push({group:g.folder,type:'TTS',repo:'Piper '+key,path:relative,license:'Vezi MODEL_CARD local',availability:'Fișiere și metadate listate; vezi raportul descărcării',variant:v.language?.name_native||key});
 }
 const whisperRelative=p.join('00_Modele_comune','STT','faster-whisper-base');
 await hf('Systran/faster-whisper-base',whisperRelative,f=>f!==' .gitattributes'&&/README|LICENSE|config.json|tokenizer.json|vocabulary.*|model.bin/.test(f),{kind:'STT',repo:'Systran/faster-whisper-base',license:'MIT'});
 const rawWhisper=await (await fetch('https://raw.githubusercontent.com/openai/whisper/main/whisper/tokenizer.py')).text();
 const supported=new Set([...rawWhisper.matchAll(/^    "([a-z]+)": "[^"]+",$/gm)].map(m=>m[1]));fs.writeFileSync(p.join(root,'00_Administrare','whisper_tokenizer.py'),rawWhisper);
 const mmsRelative=p.join('00_Modele_comune','STT','MMS_1b_all');
 const iso={ro:['ron'],en:['eng'],de:['deu'],fr:['fra'],es:['spa'],bn:['ben'],ur:['urd-script_arabic'],yue:['yue'],ha:['hau'],mr:['mar'],te:['tel'],wuu:['wuu'],ta:['tam'],fa:['fas'],arab_dialect:['arz','ary'],vi:['vie'],kn:['kan'],gu:['guj'],am:['amh'],my:['mya'],berber:['tzm','rif-script_arabic','rif-script_latin','shi','kab'],ml:['mal'],or:['ory'],apd:['apd'],pnb:['pnb'],uz:['uzb-script_latin','uzb-script_cyrillic'],ig:['ibo'],yo:['yor'],th:['tha'],ne:['npi'],nan:['nan'],kk:['kaz'],si:['sin'],km:['khm'],az:['azj-script_latin','azj-script_cyrillic','azb']};
 const target=new Set(Object.values(iso).flat());
 const mms=await hf('facebook/mms-1b-all',mmsRelative,f=>/^(README|LICENSE|config.json|preprocessor_config.json|tokenizer_config.json|special_tokens_map.json|vocab.json|model.safetensors)$/.test(f)||(/^adapter\..*\.safetensors$/.test(f)&&target.has(f.slice(8,-12))),{kind:'STT',repo:'facebook/mms-1b-all',license:'CC BY-NC 4.0 — uz necomercial'});
 const listedAdapters=mms?new Set(mms.names.filter(f=>/^adapter\..*\.safetensors$/.test(f)).map(f=>f.slice(8,-12))):new Set();
 if(mms&&!mms.names.includes('model.safetensors'))for(const f of mms.names.filter(f=>f==='pytorch_model.bin'))add('https://huggingface.co/facebook/mms-1b-all/resolve/'+mms.sha+'/'+f,p.join(mmsRelative,f),'STT',{repo:'facebook/mms-1b-all',license:'CC BY-NC 4.0'});
 for(const g of groups){
  const whisperCodes=g.codes.filter(c=>supported.has(c));if(whisperCodes.length)refs.push({group:g.folder,type:'STT',repo:'faster-whisper-base',path:whisperRelative,license:'MIT',availability:'Coduri listate oficial: '+whisperCodes.join(', '),variant:'Limbă generală; nu garantează fiecare dialect / alfabet'});
  const adapters=(iso[g.code]||[]).filter(c=>listedAdapters.has(c));if(adapters.length)refs.push({group:g.folder,type:'STT',repo:'Meta MMS-1b-all',path:mmsRelative,license:'CC BY-NC 4.0 — necomercial',availability:'Adaptoare listate: '+adapters.join(', '),variant:'Verifică vocabularul și alfabetul fiecărui adaptor',adapters});
  if(!whisperCodes.length&&!adapters.length)issues.push({group:g.folder,type:'STT',error:'Nu este listată o variantă exactă în modelele descărcate; nu se promite acoperire.'});
 }
 const release=await (await fetch('https://api.github.com/repos/espeak-ng/espeak-ng/releases/latest',{headers:{'User-Agent':'EVA-Learn'}})).json();
 for(const a of (release.assets||[]).filter(a=>/x64.*msi|win.*zip/i.test(a.name)))add(a.browser_download_url,p.join('00_Modele_comune','TTS','eSpeak_NG',a.name),'TTS',{repo:'espeak-ng',license:'GPL-3.0',purpose:'Motor TTS offline; instalator păstrat, nu instalat'});
 add('https://raw.githubusercontent.com/espeak-ng/espeak-ng/master/docs/languages.md',p.join('00_Modele_comune','TTS','eSpeak_NG','languages.md'),'TTS',{repo:'espeak-ng',license:'GPL-3.0'});
 add('https://raw.githubusercontent.com/espeak-ng/espeak-ng/master/COPYING',p.join('00_Modele_comune','TTS','eSpeak_NG','COPYING'),'TTS',{repo:'espeak-ng',license:'GPL-3.0'});
 const vf=await (await fetch('https://alphacephei.com/vosk/models')).text();fs.writeFileSync(p.join(root,'00_Administrare','vosk_models.html'),vf);
 const vosks=[['en','vosk-model-small-en-us-0.15.zip'],['de','vosk-model-small-de-0.15.zip'],['fr','vosk-model-small-fr-0.22.zip'],['es','vosk-model-small-es-0.42.zip'],['fa','vosk-model-small-fa-0.42.zip'],['vi','vosk-model-small-vn-0.4.zip'],['gu','vosk-model-small-gu-0.42.zip'],['te','vosk-model-small-te-0.42.zip']];
 for(const [code,file] of vosks){if(!vf.includes(file))continue;const g=groups.find(g=>g.code===code),relative=p.join(g.folder,'04_STT','Vosk');add('https://alphacephei.com/vosk/models/'+file,p.join(relative,file),'STT',{repo:'Vosk',languageGroup:g.folder,license:'Vezi tabelul oficial vosk_models.html'});refs.push({group:g.folder,type:'STT',repo:'Vosk '+file,path:relative,license:'Vezi tabelul oficial local',availability:'Arhivă listată oficial; vezi raportul descărcării',variant:'Model mic; acuratețea nu a fost testată'});}
 for(const g of groups){const local=refs.filter(r=>r.group===g.folder);for(const type of ['TTS','STT'])fs.writeFileSync(p.join(root,g.folder,type==='TTS'?'03_TTS':'04_STT','MODELE.json'),JSON.stringify(local.filter(r=>r.type===type),null,2),'utf8');}
 fs.writeFileSync(p.join(root,'00_Administrare','modele_referinte.json'),JSON.stringify(refs,null,2),'utf8');
 fs.writeFileSync(p.join(root,'00_Administrare','modele_neconfirmate.json'),JSON.stringify(issues,null,2),'utf8');
 fs.writeFileSync(p.join(root,'00_Administrare','downloads_models.json'),JSON.stringify([...jobs.values()],null,2),'utf8');
 console.log(JSON.stringify({modelFiles:jobs.size,references:refs.length,issues:issues.length,mmsAdapters:[...listedAdapters].filter(c=>target.has(c)),piperGroups:refs.filter(r=>r.repo.startsWith('Piper')).map(r=>r.group)},null,2));
})();
