import fs from 'node:fs';
import crypto from 'node:crypto';
import vm from 'node:vm';
const base='Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/';
const sourcePath=base+'A08_Storefront_catalog_lot04/Sources/idempiere/plugins/com.eva.ro.webshop/resources/static/themes/storefront.js';
const outPath=base+'A11/Val04_loturi/Contraoracol_A11_catalog_componenta_v1.json';
const bytes=fs.readFileSync(sourcePath),source=bytes.toString('utf8'),hash=x=>crypto.createHash('sha256').update(x).digest('hex');
if(hash(bytes)!=='5c7af41dff422695aa0970e28ab00fa978c47bd974dc47071197b71b42e50e9f')throw Error('source hash');
const fetchPart=source.slice(source.indexOf('  async function fetchProducts('),source.indexOf('\n  function applyFilter('));
const searchPart=source.slice(source.indexOf('  function applySearchQuery('),source.indexOf('\n  function displayCurrencyForCountry('));
if(!fetchPart.endsWith('  }\n')||!searchPart.endsWith('  }\n'))throw Error('extraction boundary');
const fragments=[{function:'fetchProducts',start:265,end:285,sha256:hash(fetchPart)},{function:'applySearchQuery',start:215,end:222,sha256:hash(searchPart)}];
function fixture(respond){
 const requests=[],view={html:'SEED',title:'All',empty:null,more:null,total:null};
 const state={page:2,perPage:48,categoryId:'',query:'',loading:false,hasMore:true};
 const productGrid={get innerHTML(){return view.html},set innerHTML(x){view.html=x},insertAdjacentHTML:(_,x)=>{view.html+=x}};
 const productTitle={get textContent(){return view.title},set textContent(x){view.title=x}};
 const c=vm.createContext({URLSearchParams,productGrid,productTitle,state,tenant:'A11-synthetic',lang:'ro',categoryLinks:[],featured:{hidden:false},labels:{allProducts:'All',searchEmpty:'Empty search',noCategoryProducts:'Empty category'},appendCatalogFilters:()=>{},productCard:p=>'['+p.id+']',setLoadMore:v=>{view.more=v},updateResultsSummary:v=>{view.total=v},setEmpty:(v,t)=>{view.empty={visible:v,text:t}},refreshDisplayedPrices:()=>{},fetch:url=>{requests.push(String(url));return respond(requests.length,String(url));}},{codeGeneration:{strings:false,wasm:false}});
 new vm.Script(fetchPart+'\n'+searchPart,{filename:'original-extracted-functions.js'}).runInContext(c,{timeout:1000});
 return {c,state,requests,view,call:code=>new vm.Script(code).runInContext(c,{timeout:1000}),snap:()=>JSON.parse(JSON.stringify({state,requests,view}))};
}
const ok=items=>Promise.resolve({ok:true,status:200,json:async()=>({items:items.map(id=>({id})),total:items.length,has_more:false})});
const cases=[];
function record(id,description,f,extra,assertion){const x={id,description,...f.snap(),...extra,independent_predicate:assertion};if(!assertion)throw Error('oracle '+id);cases.push(x)}
{
 const f=fixture(n=>ok([n===1?'A11-positive-A':'A11-positive-B']));
 f.state.query='A';await f.call('fetchProducts({reset:true})');f.state.query='B';await f.call('fetchProducts({reset:true})');
 record('A11-CAT-S01','Sequential positive; original fetch permits next request',f,{},f.requests.length===2&&!f.state.loading&&f.view.html==='[A11-positive-B]');
}
for(const kind of ['network','invalid_json']){
 const f=fixture(n=>n===1?(kind==='network'?Promise.reject(new Error('A11 network sentinel')):Promise.resolve({ok:true,status:200,json:async()=>{throw new SyntaxError('A11 JSON sentinel')}})):ok(['SHOULD-RECOVER']));
 let err;try{await f.call('fetchProducts({reset:true})')}catch(e){err={name:e.name,message:e.message}}
 const afterError=f.snap();f.state.query='retry';await f.call('fetchProducts({reset:true})');
 record('A11-CAT-'+kind,'Original loading remains locked after exception; independent retry does not call fetch',f,{error:err,after_error:afterError},!!err&&f.requests.length===1&&f.state.loading&&f.view.html==='SEED');
}
{
 const f=fixture(n=>n===1?Promise.resolve({ok:false,status:500,json:async()=>({error:'A11 synthetic HTTP failure'})}):ok(['A11-RECOVER']));
 await f.call('fetchProducts({reset:true})');const failed=f.snap();await f.call('fetchProducts({reset:true})');
 record('A11-CAT-HTTP500','Original ignores HTTP status, displays empty; later success is permitted',f,{after_http500:failed},failed.view.html===''&&failed.view.empty.visible&&failed.view.empty.text==='Empty category'&&!failed.state.loading&&f.requests.length===2&&f.view.html==='[A11-RECOVER]');
}
{
 let release;const first=new Promise(r=>{release=r});const f=fixture(n=>n===1?first:ok(['A11-GAMMA']));
 f.state.query='Alpha';f.view.title='Alpha';const pending=f.call('fetchProducts({reset:true})');
 f.call('applySearchQuery("Beta")');const held=f.snap();
 release({ok:true,status:200,json:async()=>({items:[{id:'A11-ALPHA'}],total:1,has_more:false})});await pending;
 const stale=f.snap();f.call('applySearchQuery("Gamma")');await new Promise(resolve=>setImmediate(resolve));
 record('A11-CAT-RACE','Original search sets Beta but suppresses its fetch; Alpha result remains under Beta; Gamma succeeds after settle',f,{held_after_beta:held,after_alpha_reply:stale},held.requests.length===1&&held.state.query==='Beta'&&held.view.title==='Beta'&&stale.view.html==='[A11-ALPHA]'&&stale.view.title==='Beta'&&f.requests.length===2&&f.view.html==='[A11-GAMMA]'&&f.view.title==='Gamma');
}
const result={utc:new Date().toISOString(),reviewer:'A11 independent',candidate:'df85d33c1648ce2b2df130a60a05ef696e2e5480',source:{path:sourcePath,sha256:hash(bytes)},fragments,method:'Independent Node vm evaluation of two exact original function substrings; independent state/view/fetch oracles. No browser, complete script, servlet/API, network, database or ERP invoked. productCard and DOM side effects are declared minimal adapters, not originals. vm is not an OS sandbox; trusted fixed source only, no process/require exposed inside context.',cases,unique_case_identities:cases.length,all_independent_predicates:true,calibration:'Initial evaluator v1 used three host Promise microtask ticks before observing the second async cross-context request and failed its final race oracle. No verdict/result artifact was written. v1 preserved. v2 waits one host event-loop turn with setImmediate for the same deterministic response; no product function or assertion changed. The initial harness timing failure is not a product defect or credited case.',relation_to_A08:'Separate five component witnesses; not additional executor cases, browser scenarios or whole-file acceptance.',persistent_effect:'Only ephemeral in-memory state. Original source unchanged; evaluator exited, no services or scratch directories.',product_score:null};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({path:outPath,sha256:hash(fs.readFileSync(outPath)),cases:cases.length}));
