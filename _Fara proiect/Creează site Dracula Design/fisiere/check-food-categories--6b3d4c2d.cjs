const {chromium}=require('./browser/node_modules/playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage();
  try {
    for (const lang of ['ro','en','de']) {
      await p.goto('http://127.0.0.1:4183/'+lang+'/collection');
      await p.locator('[data-filter=stafide-naturale]').waitFor();
      console.log(lang,await p.locator('.filters').innerText());
      await p.locator('[data-filter=stafide-aromatizate]').click();
      if(await p.locator('.product-grid .product').count()) throw Error('Incorrect category filtering');
    }
    await p.setViewportSize({width:390,height:844});
    const sizes=await p.evaluate(()=>[innerWidth,document.documentElement.scrollWidth]);
    if(sizes[0]!==sizes[1]) throw Error('Mobile overflow');
    console.log('Filters and mobile layout OK');
  } finally { await b.close(); }
})().catch(e=>{console.error(e);process.exit(1)});
