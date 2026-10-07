const fs=require('fs');const p='outputs/dracula-design-office/backend/public/shop.js';let s=fs.readFileSync(p,'utf8');
const helper=`
async function paymentReturn(path){
 if(!state.profile)return auth();
 const number=decodeURIComponent(path.split('/').pop());
 const result=await api('/api/account/orders/'+encodeURIComponent(number));const o=result.order||result;
 const pending=o.status==='pending_payment';
 return '<section class="page confirmation">'+icon('favorite')+'<h1>'+t(pending?'checkout.pending':'checkout.received')+'</h1><p>'+esc(number)+'</p><p>'+t('status.'+o.status)+'</p><p>'+money(o.total_ron||o.total)+'</p>'+(pending?'<button class="button-primary" data-action="pay" data-number="'+esc(number)+'">'+t('payment.card')+'</button>':'')+'<p>'+link('/account',t('account.orders'),'button-outline')+'</p></section>';
}
`;
s=s.replace('async function render()',helper+'\nasync function render()');
s=s.replace("else if(path==='/confirmation')body=confirmation();", "else if(path==='/confirmation')body=confirmation();else if(path.startsWith('/checkout/confirmare/')||path.startsWith('/checkout/plata/'))body=await paymentReturn(path);");
s=s.replace("if(action==='filter')", "if(action==='pay'){b.disabled=true;const payment=await api('/api/payments/stripe/session','POST',{order_number:b.dataset.number});location.assign(payment.url);}else if(action==='filter')");
fs.writeFileSync(p,s);
