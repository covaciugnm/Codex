const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1280,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8765');
  await page.setInputFiles('#merge-one','.runtime/merge-browser/clip2.mp4');
  await page.setInputFiles('#merge-many',['.runtime/merge-browser/clip10.mp4']);
  if(await page.locator('#merge-list tr').count()!==2)throw Error('Additive selection');
  await page.locator('#merge-list tr').nth(1).getByRole('button',{name:'Mută mai sus: clip10.mp4',exact:true}).click();
  if(!(await page.locator('#merge-list tr').first().innerText()).includes('clip10.mp4'))throw Error('Reorder');
  await page.click('#merge-clear');
  await page.setInputFiles('#merge-folder','.runtime/merge-browser');
  if(await page.locator('#merge-list tr').count()!==2)throw Error('Folder video filtering');
  if(!(await page.locator('#merge-list tr').first().innerText()).includes('clip2.mp4'))throw Error('Natural order');
  await page.fill('#merge-name','Test-browser-unire');
  await page.click('#merge-start');
  await page.locator('#merge-result').waitFor({state:'visible',timeout:60000});
  const href=await page.locator('#merge-result').getAttribute('href');
  const result=await page.request.get('http://127.0.0.1:8765'+href);if(!result.ok()||(await result.body()).length<1000)throw Error('Missing result');
  await page.locator('[aria-labelledby="merge-heading"]').screenshot({path:'.runtime/merge-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile overflow');
  if(errors.length)throw Error(errors.join('\n'));
  console.log('Merge browser OK: single, multiple, folder, order, actual upload/merge/download, mobile');
  console.log(decodeURIComponent(href));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
