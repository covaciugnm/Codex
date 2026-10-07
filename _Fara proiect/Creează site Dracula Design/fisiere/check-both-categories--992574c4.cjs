const {chromium}=require('./browser/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch();
 try {
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  for(const port of [4181,4183]) for(const lang of ['ro','en','de']) {
   await page.goto(`http://127.0.0.1:${port}/${lang}/collection`);
   await page.locator('.filters').waitFor();
   const cases=port===4181 ? [['accesorii',5],['haine',0],['business',2],['all',5]] : [['stafide-naturale',0],['stafide-aromatizate',0],['all',2]];
   for(const [code,count] of cases) {
    await page.locator(`[data-filter=${code}]`).click();
    await page.waitForFunction(n=>document.querySelectorAll('.product-grid .product').length===n,count);
   }
   await page.setViewportSize({width:390,height:844});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForFunction(()=>document.documentElement.scrollWidth===innerWidth);
   console.log(port,lang,'category counts and mobile layout OK');
   if(lang==='ro') {
    const cookie=page.locator('[data-action=cookies]');
    if(await cookie.count()) await cookie.click();
    await page.locator('.product-image img').evaluateAll(imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode();})));
    await page.screenshot({path:`outputs/${port===4181?'dracula-design-office':'dracula-food'}/preview-categorii-mobil.png`,fullPage:true});
   }
   await page.setViewportSize({width:1440,height:1000});
  }
  if(errors.length) throw Error(errors.join('\n'));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
