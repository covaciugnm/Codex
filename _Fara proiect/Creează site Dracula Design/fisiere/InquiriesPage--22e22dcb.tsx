import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { get, patch } from '../../api/client';
type Inquiry={id:string;kind:string;name:string;email:string;body:string;locale:string;status:string;created_at:string};
export default function InquiriesPage(){
 const {t}=useTranslation();const qc=useQueryClient();
 const query=useQuery({queryKey:['inquiries'],queryFn:()=>get<{items:Inquiry[]}>('/dracula/inquiries')});
 const update=useMutation({mutationFn:({id,status}:{id:string;status:string})=>patch('/dracula/inquiries/'+id,{status}),onSuccess:()=>qc.invalidateQueries({queryKey:['inquiries']})});
 return <section className="page"><h1>{t('nav.inquiries')}</h1>{query.isPending?<p>{t('table.loading')}</p>:null}{query.isError||update.isError?<p role="alert">{t('inquiries.error')}</p>:null}{query.data?.items.length===0?<p>{t('inquiries.empty')}</p>:null}{query.data?.items.map(item=><article className="card" key={item.id} style={{marginBottom:16,padding:24}}><h2>{item.name}</h2><p>{item.email} · {item.locale.toUpperCase()} · {new Date(item.created_at).toLocaleString()}</p><p>{t('inquiries.'+item.kind)}</p><p style={{whiteSpace:'pre-wrap'}}>{item.body}</p><label>{t('inquiries.status')} <select value={item.status} disabled={update.isPending} onChange={e=>update.mutate({id:item.id,status:e.target.value})}>{['new','in_progress','closed'].map(s=><option value={s} key={s}>{t('inquiries.'+s)}</option>)}</select></label></article>)}</section>;
}
