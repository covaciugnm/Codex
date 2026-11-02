const fs=require('fs'),path=require('path'),crypto=require('crypto');
module.exports=function(root){
 const folder=path.join(root,'audit-calitate'),rounds=fs.readdirSync(folder).filter(n=>/^runda-\d+$/.test(n)&&fs.existsSync(path.join(folder,n,'audit.json'))).map(n=>({folder:n,...JSON.parse(fs.readFileSync(path.join(folder,n,'audit.json'),'utf8'))})).sort((a,b)=>a.round-b.round);
 const current=rounds.at(-1);if(!current)throw Error('No independent audit');
 const checks=(current.checks?.artifactHashes||[]).map(e=>{const f=path.join(root,e.file),actual=fs.existsSync(f)?crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'):null;return {...e,actual,matches:actual===e.sha256};});
 return {rounds,current,checks,matchesCurrentData:checks.length>0&&checks.every(e=>e.matches),changedFiles:checks.filter(e=>!e.matches).map(e=>e.file)};
};
