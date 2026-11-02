const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/viewer.html','utf8'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const nodes=new Map(),node=id=>{if(!nodes.has(id))nodes.set(id,{textContent:'',className:'',disabled:false,replaceChildren(){},value:''});return nodes.get(id)};
let running=false,starts=0,requests=[];
const context={document:{getElementById:node},location:{port:'8766'},setInterval(){},AbortSignal,console,fetch:async(url,opts)=>{
 requests.push(url);
 if(url==='/control/status')return {ok:true,json:async()=>({running})};
 if(url==='/control/start'){assert.equal(opts.method,'POST');starts++;running=true;return{ok:true,json:async()=>({running:true})}}
 if(url==='/api/status')return{ok:true,json:async()=>({root:'fixture',conversations:[]})};
 throw Error('Unexpected request: '+url);
}};
vm.runInNewContext(script,context);
(async()=>{
 await new Promise(setImmediate);
 assert.equal(node('connection').className,'offline');assert.equal(node('start-server').disabled,false);
 assert(!requests.includes('/api/status'),'do not query dead worker when status is offline');
 await node('start-server').onclick();
 assert.equal(starts,1);assert.equal(node('connection').className,'online');assert.equal(node('start-server').disabled,true);
 console.log('PASS: offline red state, start button, online green state, viewer JavaScript syntax');
})().catch(e=>{console.error(e);process.exitCode=1});
