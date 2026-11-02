const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),C=require('./core.js');
async function run(reverse){
 let listener,clock=10000,loaded=false,top=0,captures=[];
 const message=t=>({innerText:t,getAttribute:()=>null,querySelectorAll:()=>[],contains:()=>false});
 const recent=message('Alice 2026-10-23 12:00 recent'),older=message('Alice 2025-01-01 12:00 older');
 const sc={scrollHeight:500,clientHeight:50,matches:()=>true,get scrollTop(){return top},set scrollTop(v){top=reverse?Math.min(0,v):Math.max(0,v)},dispatchEvent(){if(reverse?top<0:top>0)loaded=true}};
 const root={get innerText(){return recent.innerText+(loaded?older.innerText:'')},previousElementSibling:{innerText:'Alice 5:00 PM Local Time',previousElementSibling:null},parentElement:{querySelector:()=>null},querySelectorAll:q=>q==='*'?[sc]:q.includes('data-message-id')?(loaded?[recent,older]:[recent]):[]};
 const row={getAttribute:n=>n==='aria-label'?'Chat avatar Alice 2026-10-23':null,innerText:'Alice 2026-10-23',closest:()=>null,scrollIntoView(){},click(){}};
 const list={querySelectorAll:q=>q==='button,[role=button]'?[row]:[]};
 const chrome={storage:{local:{get:async()=>({autoSave:false}),set:async()=>{}},onChanged:{addListener(){}}},runtime:{onMessage:{addListener:f=>listener=f},sendMessage:async req=>{captures.push(structuredClone(req.data));return{ok:true,data:{messages:req.data.messages.length}}}}};
 const ctx={ArchiveCore:C,chrome,document:{querySelector:q=>q==='#im-chat'?root:q==='#im-list'?list:null},location:{href:'https://message.alibaba.com/message/messenger.htm?activeAccountId=1'},URL,Event,Date:class extends Date{static now(){return clock}},setInterval(){},setTimeout:(f,ms)=>{clock+=ms;f()},getComputedStyle:()=>({overflowY:'auto',flexDirection:'column'})};ctx.globalThis=ctx;
 vm.runInNewContext(fs.readFileSync(__dirname+'/content.js','utf8'),ctx);
 const call=type=>new Promise(resolve=>listener({type},{},resolve));
 await call('startAll');
 for(let i=0;i<100;i++){await new Promise(setImmediate);if(!(await call('state')).data.running)break}
 assert(!(await call('state')).data.runStatus.startsWith('Eroare'),(await call('state')).data.runStatus);
 assert(captures.some(s=>s.messages.some(m=>m.text.includes('older'))),'must save history loaded from either scroll direction in a 50px panel');
 assert(!(await call('state')).data.running,'must finish a stable list');
}
(async()=>{await run(false);await run(true);console.log('PASS: older history loads with both positive and negative scroll offsets in short panels')})().catch(e=>{console.error(e);process.exitCode=1});
