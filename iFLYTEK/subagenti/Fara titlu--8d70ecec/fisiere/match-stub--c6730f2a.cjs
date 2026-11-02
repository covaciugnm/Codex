'use strict';
function parseSignature(text){
 if(typeof text!=='string')return null;const open=text.indexOf('('),close=text.lastIndexOf('):');if(open<1||close<open)return null;const prefix=text.slice(0,open),dot=prefix.lastIndexOf('.');if(dot<1)return null;
 const body=text.slice(open+1,close),parameters=[];let start=0,depth=0;for(let i=0;i<body.length;i++){if(body[i]==='<')depth++;else if(body[i]==='>')depth--;else if(body[i]===','&&depth===0){parameters.push(body.slice(start,i).trim());start=i+1;}if(depth<0)return null;}if(depth!==0)return null;if(body)parameters.push(body.slice(start).trim());if(parameters.some(x=>!x))return null;
 return{owner:prefix.slice(0,dot),name:prefix.slice(dot+1),parameters,returnType:text.slice(close+2)};
}
function extractStubSignature(javaText,offset){const tail=javaText.slice(offset),m=/^throw new (?:java\.lang\.)?UnsupportedOperationException\("((?:\\.|[^"\\])*)"\)/.exec(tail);if(!m)return null;try{const literal=JSON.parse('"'+m[1]+'"');return literal.startsWith('Method not decompiled: ')?literal.slice(23):null;}catch{return null;}}
function matchStub(signature,classes){const parsed=parseSignature(signature);if(!parsed)return{status:'UNRESOLVED',reason:'Unsupported source signature syntax',candidates:[]};const candidates=new Map();
 for(const c of classes)for(const m of c.methods||[]){if(!m.independentDexMatch||!Array.isArray(m.ownerJavaNames)||!m.ownerJavaNames.includes(parsed.owner)||!m.methodJavaNames.includes(parsed.name)||m.parameterJavaNames.length!==parsed.parameters.length||!m.returnJavaNames.includes(parsed.returnType))continue;
 const params=parsed.parameters.map(p=>p.endsWith('...')&&(m.accessFlags&128)?p.slice(0,-3)+'[]':p);if(!params.every((p,i)=>m.parameterJavaNames[i].includes(p)))continue;
 const id=m.dexSha256+':'+m.rawDescriptor+':'+m.methodIndex;candidates.set(id,m);
 }
 const list=[...candidates.values()];return{status:list.length===1?'UNIQUE_VERIFIED_IDENTITY':list.length?'AMBIGUOUS':'UNRESOLVED',parsed,candidates:list,semanticRepairApproved:false,scope:'Stub-to-raw-method identity only; no semantic body correctness is implied'};
}
module.exports={parseSignature,extractStubSignature,matchStub};
