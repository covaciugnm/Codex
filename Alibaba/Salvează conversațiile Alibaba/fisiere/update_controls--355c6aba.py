from pathlib import Path
p=Path(__file__).with_name('viewer.html')
s=p.read_text('utf-8-sig')
if 'id="start-server"' not in s:
    s=s.replace('<span id="connection">Conectare…</span>', '<span id="connection" role="status" aria-live="polite">Verificare server…</span><button id="start-server" disabled>Pornește serverul</button>')
    s=s.replace('</style>', '''
#connection.online{color:#26743a;background:#e6f6e9}#connection.offline{color:#a62727;background:#ffe7e7}#connection.checking{color:#756327;background:#fff4d7}
#start-server{border:1px solid #dce2e8;border-radius:8px;background:#fff;padding:9px 12px;color:#26313c}#start-server:disabled{opacity:.5;cursor:default}@media(max-width:590px){header{gap:8px}#start-server{font-size:11px;padding:7px}header strong{font-size:15px}header small{max-width:100px}}
</style>''',1)
    s=s.replace("const token='__TOKEN__'", "if(location.port==='8765')location.replace('http://127.0.0.1:8766/');\nconst token='__TOKEN__'",1)
    s=s.replace("headers:{'X-Archive-Key':token}});", "headers:{'X-Archive-Key':token},signal:AbortSignal.timeout(15000)});",1)
    start=s.index('async function load(){')
    end=s.index("$('search').oninput",start)
    s=s[:start]+'''
let loading=false,starting=false;
function serverState(running,label){
 $('connection').className=running?'online':'offline';
 $('connection').textContent=(running?'● ':'● ')+(label||(running?'Server de comunicare pornit':'Server de comunicare oprit'));
 $('start-server').disabled=running||starting;
 $('start-server').textContent=starting?'Se pornește…':running?'Server pornit':'Pornește serverul';
}
async function control(path,method='GET'){
 const r=await fetch('/control/'+path,{method,headers:{'X-Archive-Key':token},signal:AbortSignal.timeout(method==='POST'?20000:5000)});
 const data=await r.json();if(!r.ok)throw Error(data.error||'Lansatorul local nu răspunde.');return data;
}
async function load(){
 if(loading)return;loading=true;
 try{
  let health;
  try{health=await control('status')}catch(e){serverState(false,'Lansator local indisponibil');$('notice').textContent='Deschide software/server/Deschide-arhiva.cmd pentru a reactiva lansatorul local.';return}
  serverState(health.running);
  if(!health.running){$('notice').textContent='Serverul de comunicare este oprit sau nu răspunde. Apasă Pornește serverul. Datele deja salvate sunt păstrate.';return}
  try{const s=await api('status');summaries=s.conversations.sort((a,b)=>a.contact.localeCompare(b.contact));$('path').textContent=s.root;$('count').textContent=summaries.length;drawList();if(selected)await select(selected,true);else if(summaries.length)await select(summaries[0].id)}catch(e){showError(e)}
 }finally{loading=false}
}
$('start-server').onclick=async()=>{
 if(starting)return;starting=true;serverState(false,'Se pornește serverul…');$('connection').className='checking';
 try{const r=await control('start','POST');if(!r.running)throw Error('Pornirea nu a fost confirmată.');serverState(true);$('notice').textContent='Server pornit. Se actualizează arhiva.'}
 catch(e){serverState(false);$('notice').textContent=e.message+' Dacă lansatorul nu răspunde, deschide Deschide-arhiva.cmd.'}
 finally{starting=false;await load()}
};
''' +s[end:]
    p.write_text(s,encoding='utf-8')
