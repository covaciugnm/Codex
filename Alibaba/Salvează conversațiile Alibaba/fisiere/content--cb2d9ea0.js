(() => {
 if(globalThis.__alibabaArchiveV2)return;globalThis.__alibabaArchiveV2=true;
 const C=ArchiveCore,clean=s=>String(s||'').replace(/\s+/g,' ').trim(),wait=ms=>new Promise(r=>setTimeout(r,ms));
 const nodesSelector='[data-message-id],[class*=message-item],[class*=messageItem],[class*=message-bubble],[class*=messageBubble],[class*=msg-item],[class*=msgItem],[class*=im-message]';
 let enabled=false,running=false,stop=false,busy=false,lastIdentity='',identityAt=Date.now(),previousBody='',lastFingerprint='',runStatus='Oprit';
 let completeId='',transitionBody='';
 function root(){return document.querySelector('#im-chat')}
 function identity(){const u=new URL(location.href);return u.searchParams.get('activeAccountId')||''}
 function nodes(r){const all=[...r.querySelectorAll(nodesSelector)];return all.filter(e=>!all.some(o=>o!==e&&e.contains(o)))}
 function contact(r){
  const parent=r.parentElement;
  for(const q of ['[class*=chat-header] [class*=name]','[class*=chatHeader] [class*=name]','[class*=conversation-header] [class*=name]']){const e=parent?.querySelector(q);if(e&&clean(e.textContent))return clean(e.textContent)}
  // The header immediately before #im-chat contains the current interlocutor.
  let p=r.previousElementSibling;
  for(let i=0;p&&i<7;i++,p=p.previousElementSibling){const t=clean(p.innerText);const match=t.match(/^(.{1,100}?)\s+\d{1,2}:\d{2}\s*(?:AM|PM)?\s*Local Time/i);if(match)return match[1]}
  const list=document.querySelector('#im-list');
  for(const e of list?.querySelectorAll('[aria-selected=true],[class*=selected],[class*=active]')||[]){const t=(e.innerText||'').split('\n').map(clean).filter(Boolean)[0];if(t&&!/^(All|Unread|Search)$/i.test(t)&&t.length<100)return t}
  // A stable ID is safer than assigning messages to the wrong person's name.
  return 'Contact '+identity();
 }
 function profile(r){
  const name=contact(r),list=document.querySelector('#im-list');
  const candidates=[...(list?.querySelectorAll('[aria-selected=true],[class*=selected],[class*=active]')||[])];
  const row=candidates.find(e=>clean(e.innerText).includes(name));
  if(!row)return{};
  const get=q=>clean(row.querySelector?.(q)?.textContent);
  const company=get('[class*=company],[data-company-name]');
  // Only explicit Alibaba fields from the selected contact; never the AI summary.
  const alibabaCategory=get('[data-category-name],[class*=category-name],[class*=categoryName]');
  const country=get('[data-country-name],[class*=country-name]');
  return{company,alibabaCategory,country,source:'Alibaba Messenger — rândul contactului selectat'};
 }
 function extract(){
  const r=root(),id=identity();if(!r||!id)throw Error('Structura Alibaba nu este recunoscută: #im-chat sau ID absent.');
  const messages=[],attachments=[],unresolved=[];
  for(const e of nodes(r)){
   const text=clean(e.innerText),media=[];
   for(const x of e.querySelectorAll('a[href],img[src],video,video source,[data-download-url],[data-file-url]')){
    const kind=x.matches('video,source')?'video':x.tagName==='IMG'?'image':'file';
    const url=x.getAttribute('data-download-url')||x.getAttribute('data-file-url')||x.currentSrc||x.src||x.href||'';
    const hint=(String(x.className)+' '+url).toLowerCase();
    if(/avatar|emoji|icon|logo|flag|badge|sprite|\.svg(?:\?|$)/.test(hint))continue;
    if(kind==='image'&&x.naturalWidth<150&&x.naturalHeight<150&&!/file|media|photo|image-message/.test(hint))continue;
    if(kind==='file'&&!x.hasAttribute('download')&&!/download|attachment|clouddisk|\.(pdf|docx?|xlsx?|zip|rar|step|stp|mp4)(?:\?|$)/i.test(url))continue;
    let name=clean(x.getAttribute('download')||x.getAttribute('data-filename')||x.getAttribute('alt')||x.textContent);
    if(!name){try{name=decodeURIComponent(new URL(url).pathname.split('/').pop())}catch{}}
    media.push({url,name:name||kind,kind});
   }
   if(!text&&!media.length)continue;
   const explicit=e.getAttribute('data-message-id')||e.getAttribute('data-msg-id');
   const fallback=text+'|'+media.map(m=>C.mediaKey(m.url)).join('|');
   const messageKey=explicit?'id:'+explicit:'content:'+fallback;
   const wrapper=e.closest?.('.message-item-wrapper')||e,classes=String(wrapper.className||'');
   const sender=/item-right|outgoing|\bself\b/.test(classes)?'self':/item-left|incoming/.test(classes)?'partner':'unknown';
   messages.push({key:messageKey,text,sender,time:(text.match(/\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}/)||[])[0]||''});
   for(const m of media){if(C.allowedURL(m.url)){attachments.push({...m,key:C.mediaKey(m.url),messageKey})}else if(m.kind==='video'){unresolved.push({key:messageKey+':video',messageKey,kind:'video',name:'Video fără adresă directă'})}}
   const fileNames=text.match(/[^\n]{0,100}?\.(?:pdf|docx?|xlsx?|zip|rar|7z|step|stp|dwg|mp4)\b/gi)||[];
   for(const name of fileNames)if(!media.some(m=>m.kind==='file'))unresolved.push({key:messageKey+':'+name,messageKey,kind:'file',name});
  }
  return{id,contact:contact(r),profile:profile(r),pageUrl:'https://message.alibaba.com/message/messenger.htm?activeAccountId='+encodeURIComponent(id),messages,attachments,unresolved,historyComplete:completeId===id};
 }
 async function save(force=false){
  if(busy){if(!force)return;while(busy)await wait(150)}const id=identity(),body=clean(root()?.innerText);
  if(id!==lastIdentity){transitionBody=previousBody;lastIdentity=id;identityAt=Date.now();lastFingerprint='';return}
  if(Date.now()-identityAt<2500)return;
  if(transitionBody&&body===transitionBody){if(force)throw Error('Noua conversație nu s-a încărcat încă.');return}transitionBody='';
  if(!force&&body===previousBody&&lastFingerprint)return;
  const d=extract();if(!d.messages.length)return;
  const fp=JSON.stringify(d);if(!force&&fp===lastFingerprint)return;
  busy=true;try{const r=await chrome.runtime.sendMessage({type:'capture',data:d});if(!r?.ok)throw Error(r?.error||'Salvarea a eșuat');lastFingerprint=fp;previousBody=body;runStatus='Salvat: '+d.contact+' — '+r.data.messages+' mesaje';return r.data}finally{busy=false}
 }
 function scrollPane(container){
  if(!container)return null;
  const candidates=[container,...container.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+30&&e.clientHeight>30&&(/(auto|scroll)/.test(getComputedStyle(e).overflowY)||e.matches('.scroll-box')));
  return candidates.sort((a,b)=>(b.scrollHeight-b.clientHeight)-(a.scrollHeight-a.clientHeight))[0]||null;
 }
 async function history(){
  const id=identity();let stable=0,old='',steps=0;
  while(!stop&&id===identity()&&steps++<300){
   const r=root();if(!r)throw Error('Panoul conversației a dispărut.');
   await save(true);
   const sc=scrollPane(r);if(!sc){runStatus='Istoric fără panou de derulare; verificare manuală necesară.';break}
   // Alibaba uses both normal and reversed scrolling layouts. Visit both ends
   // and save each loaded page, including when the visible panel is very short.
   for(const edge of [-1,0,1]){
    if(stop||id!==identity())break;
    sc.scrollTop=edge*sc.scrollHeight;sc.dispatchEvent(new Event('scroll',{bubbles:true}));await wait(1400);
    await save(true);
   }
   const sig=nodes(r).map(e=>clean(e.innerText)).join('|');stable=sig===old?stable+1:0;old=sig;
   if(stable>=3){
    const first=nodes(r)[0],last=nodes(r).at(-1);
    // Only claim a beginning when Alibaba's initial system notice is present at the top.
    if([first,last].some(e=>/Keep chats and transactions on Alibaba\.com/.test(e?.innerText||'')))completeId=id;
    await save(true);break;
   }
  }
  if(steps>=300)throw Error('Limita de încărcare a istoricului a fost atinsă; continuă manual.');
 }
 function rows(){
  const list=document.querySelector('#im-list');if(!list)return[];
  return [...list.querySelectorAll('button,[role=button]')].filter(e=>{
   const label=e.getAttribute('aria-label')||e.innerText||'';
   return /Chat avatar|\d{4}-\d|\d{2}:\d{2}/.test(label)&&!e.closest('[role=menu]');
  });
 }
 function rowKey(e){return e.getAttribute('data-id')||e.getAttribute('data-account-id')||clean(e.getAttribute('aria-label')||e.innerText).replace(/\b\d{1,2}:\d{2}\b/g,'')}
 async function all(){
  if(running)return;running=true;stop=false;const visited=new Set();let exhausted=0;
  try{
   const list=document.querySelector('#im-list'),sc=scrollPane(list);if(!list||!rows().length)throw Error('Lista de conversații nu este recunoscută. Folosește salvarea la deschidere.');
   if(sc){sc.scrollTop=0;await wait(800)}
   while(!stop){
    const candidates=rows(),next=candidates.find(e=>!visited.has(rowKey(e)));
    if(next){
     exhausted=0;visited.add(rowKey(next));const oldId=identity(),oldBody=clean(root()?.innerText);next.scrollIntoView({block:'nearest'});next.click();await wait(1200);
     if(stop)break;
     // Capture only after route and content have had time to settle.
     if(identity()!==lastIdentity){transitionBody=identity()!==oldId?oldBody:'';lastIdentity=identity();identityAt=Date.now();lastFingerprint=''}
     await wait(2700);if(stop)break;
     if(identity()===oldId&&visited.size>1){runStatus='Conversație neschimbată; verificare necesară.';continue}
     runStatus='Parcurg '+visited.size+' conversații…';await history();
    }else{
     if(!sc)break;const before=sc.scrollTop;sc.scrollTop+=Math.max(sc.clientHeight*0.8,250);sc.dispatchEvent(new Event('scroll',{bubbles:true}));await wait(1300);
     if(sc.scrollTop===before&&!rows().some(e=>!visited.has(rowKey(e))))exhausted++;else exhausted=0;
     if(exhausted>=3)break;
    }
   }
   runStatus=stop?'Parcurgere oprită. Datele salvate sunt păstrate.':'Lista curentă a fost parcursă. Verifică raportul; conversațiile arhivate necesită o rulare separată.';
  }catch(e){runStatus='Eroare: '+e.message;await chrome.storage.local.set({lastError:{message:runStatus,at:new Date().toISOString()}})}finally{running=false;await chrome.storage.local.set({runStatus})}
 }
 chrome.runtime.onMessage.addListener((req,sender,send)=>{
  if(req.type==='stop'){stop=true;send({ok:true});return}
  if(req.type==='startAll'){all();send({ok:true});return}
  if(req.type==='state'){send({ok:true,data:{enabled,running,runStatus,contact:root()?contact(root()):'',id:identity()}});return}
  if(req.type==='saveNow'){
   (async()=>{const id=identity();if(id!==lastIdentity){transitionBody=previousBody;lastIdentity=id;identityAt=Date.now();lastFingerprint=''}await wait(Math.max(0,2600-(Date.now()-identityAt)));return save(true)})().then(data=>send({ok:true,data})).catch(e=>send({ok:false,error:String(e)}));return true;
  }
 });
 chrome.storage.local.get('autoSave').then(s=>enabled=s.autoSave!==false);
 chrome.storage.onChanged.addListener((changes,area)=>{if(area==='local'&&changes.autoSave)enabled=!!changes.autoSave.newValue});
 setInterval(()=>{if(enabled&&!running)save().catch(e=>{runStatus='Eroare: '+e.message;chrome.storage.local.set({lastError:{message:runStatus,at:new Date().toISOString()}})})},4000);
})();

