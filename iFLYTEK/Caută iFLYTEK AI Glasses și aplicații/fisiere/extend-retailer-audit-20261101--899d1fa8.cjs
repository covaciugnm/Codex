'use strict';
const {page,pool}=require('./audit-retailers-20261101.cjs');
(async()=>{await pool([
 ['https://sahaha.vn/en/san-pham/iflytek-ai-glasses/','exact-model'],
 ['https://www.xunfei.cn/goods?goodsId=2448','official-product'],
 ['https://loomy.xunfei.cn/skills','official-skills'],
 ['https://loomy.xunfei.cn/changelog','official-changelog'],
 ['https://loomy.xunfei.cn/docs/user-guide/toolbox','official-help'],
 ['https://loomy.xunfei.cn/docs/user-guide/skills','official-help'],
 ['https://github.com/iflytek/astronclaw-tutorial','official-related-tutorial'],
 ['https://github.com/iflytek/astronclaw-tutorial/blob/main/README_EN.md','official-related-tutorial'],
 ['https://tech.ifeng.com/c/8vIAcseEnxb','exact-model-review'],
 ['https://www.goodwaytechs.com/es/goodway-g100-smart-ai-camera-glasses.html','different-hardware-G100'],
 ['https://aventaglasses.com/','different-hardware-G100'],
 ['https://aventaglasses.com/pages/support','different-hardware-G100'],
 ['https://iflytek.co.jp/pages/download','regional-download'],
 ['https://fr.iflytek.com/pages/ainote-app-download','regional-download'],
 ['https://uk.iflytek.com/pages/ainote-app-download','regional-download'],
 ['https://store.iflytek.com/pages/ainote-app-download','regional-download'],
 ['https://www.openchinacart.com/products/2010225999563791','accessory-listing']
 ].map(([u,s])=>()=>page(u,s)));
})().catch(e=>{console.error(e);process.exitCode=1;});
