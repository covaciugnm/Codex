const {request,chromium}=require('./browser/node_modules/playwright');
const fs=require('fs');
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
(async()=>{
 const results=[], qa=[];const browser=await chromium.launch();
 for(const [port,mailport,domain,slug] of [[4181,4182,'dracula-design.com','dracula-design'],[4183,4184,'dracula-food.com','dracula-food']]){
  const base='http://127.0.0.1:'+port, inbox='http://127.0.0.1:'+mailport;
  const r=await request.newContext();const mark=(name,value)=>{results.push({site:domain,name,value});console.log(domain,name,JSON.stringify(value));};
  const api=async(path,data)=>{
   const st=await r.storageState();const c=st.cookies.find(c=>c.name.endsWith('csrf'));
   const resp=await r.fetch(base+path,{method:data===undefined?'GET':'POST',data,headers:{'X-CSRF-Token':c?.value||''}});const body=await resp.json();
   if(resp.status()>=400)throw Error(path+' '+resp.status()+' '+JSON.stringify(body));return body;
  };
  const getMail=async(email,subjectContains)=>{
   for(let i=0;i<15;i++){
    const list=await r.get(inbox+'/api/v1/messages').then(x=>x.json());
    const m=list.messages.find(x=>x.To.some(t=>t.Address===email)&&x.Subject.toLowerCase().includes(subjectContains.toLowerCase()));
    if(m)return await r.get(inbox+'/api/v1/message/'+m.ID).then(x=>x.json());await delay(1000);
   }throw Error('Missing captured email '+subjectContains);
  };
  const email='qa-mail-'+Date.now()+'@'+domain;
  await api('/api/dracula/bootstrap');
  const registration=await api('/api/account/register?lang=de',{email,password:'EmailTest121.',full_name:'QA Mail Capture',accept_terms:true});
  qa.push({site:slug,email,user_id:registration.account_id});fs.writeFileSync('work/email-qa-accounts.json',JSON.stringify(qa,null,2));mark('registration',{created:!!registration.account_id});
  const verification=await getMail(email,'bestätigen');
  const verifyurl=verification.Text.match(/http[^\s]+\/de\/account\?verify=[^\s]+/)[0];
  const verified=await api('/api/account/verify-email',{token:new URL(verifyurl).searchParams.get('verify')});
  mark('verification_email',{status:verified.status,from:verification.From.Address,inlineImages:verification.Inline?.length||0,company:verification.HTML.includes('Dracula-Company'),correctAddress:verification.HTML.includes(slug==='dracula-food'?'Dracula-Farm':'Dracula-Castel')});
  await api('/api/account/forgot-password?lang=en',{email});
  const reset=await getMail(email,'password');
  const url=reset.Text.match(/http[^\s]+\/en\/reset-password\?token=[^\s]+/)[0];
  const p=await browser.newPage();await p.goto(url);await p.locator('[data-form=reset]').waitFor();
  await p.locator('[name=password]').fill('EmailReset121.');await p.locator('[name=password_confirm]').fill('EmailReset121.');await p.locator('[data-form=reset] button').click();await p.waitForURL('**/en/account');
  const fresh=await request.newContext();const login=await fresh.post(base+'/api/account/login',{data:{email,password:'EmailReset121.'}});if(!login.ok())throw Error('Reset login failed');
  mark('password_reset',{emailCaptured:true,browserFlow:true,newPasswordLogin:login.status(),linkLocale:'en',wrongBrand:/cesiro/i.test(reset.Text+reset.HTML)});
  const forbidden=await r.post(base+'/api/account/reset-password',{headers:{'X-CSRF-Token':(await r.storageState()).cookies.find(c=>c.name.endsWith('csrf'))?.value||''},data:{token:new URL(url).searchParams.get('token'),password:'NoReuse121.'}});mark('reset_token_single_use',forbidden.status());
  const other=await r.get('http://127.0.0.1:'+(mailport===4182?4184:4182)+'/api/v1/messages').then(x=>x.json());mark('mailbox_isolation',!other.messages.some(x=>x.To.some(t=>t.Address===email)));
  await p.close();await fresh.dispose();await r.dispose();
 }
 await browser.close();fs.writeFileSync('work/email-qa-accounts.json',JSON.stringify(qa,null,2));fs.writeFileSync('work/email-capture-results.json',JSON.stringify(results,null,2));
})().catch(e=>{console.error(e.message);process.exit(1)});
