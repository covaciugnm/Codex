from a12_r9_orig import *
import subprocess
dd='Documentatie/echipa-2026-10-09/T35-cadru-platforme-vanzari/'
rr='Documentatie/echipa-2026-10-09/COORDONARE_SESIUNI.md';spec=dd+'08-L3_arhitect_spec.md';rp=dd+'11-L3b_implementator_raport.md';lg=dd+'LOG_MODIFICARI.md'
def check():
 rego,regb=getp(rr);regl=regb.decode().splitlines();sigo=block(rr,rego,[211,212,217,218]);revref='435250f930';sobj=git('rev-parse '+shlex.quote(revref+':'+spec)).decode().strip();b=fetch_oid(sobj).splitlines(keepends=True);s=b[28:379];md5=hashlib.md5(b''.join(s)).hexdigest();want='c7416bf0992ce048c614f4d94bb64e1a';ms=[{'registry_row':idx,'author_field':regl[idx-1].split('|')[2].strip(),'same_digest':want in regl[idx-1],'proof':sigo['lines'][k]}for k,idx in [(2,217),(3,218)]];assert md5==want,(md5,want)
 # Mutation controls applied only to normalized contract bytes and signatures.
 mut=b''.join(s).replace(b'TabelaFisaCanal',b'TabelaFisaCanalX',1);m=hashlib.md5(mut).hexdigest()
 out={'utc':now(),'criterion':'T35.08-R3-001','authority_and_plan':r7map['T35.08-R3-001']['source_row'],'required':'Ambele sesiuni semnează aceeași revizie din §C; montația este independentă.','registry':sigo,'signed_contract':{'source':spec,'supplied_revision':revref,'blob':sobj,'line_first':29,'line_last':379,'line_count':len(s),'recomputed_md5':md5,'recomputed_sha256':hashlib.sha256(b''.join(s)).hexdigest()},'observed_bilateral':ms,'negative':{'one_contract_byte_sequence_changed':m,'does_not_match_either_signature':all(m not in v['proof']['text']for v in ms),'one_signature_removed_leaves_one_party':len(ms[:1])},'scope':'Atestă acordul documentar între doi autori din registru și identitatea textului, nu semnături criptografice ale persoanelor și nu instalarea.'};f=P9/'T35_08_acord_bilateral.json';wr(f,out)
 logoid,logb=getp(lg);lo=logb.decode().splitlines();roid,rb=getp(rp);rl=rb.decode().splitlines()
 poss=[]
 for i,l in enumerate(rl,1):
  if re.match(r'\| Comituri(?: r[3-7][a-z]?)? \|',l):poss.append((i,l))
 pat=re.compile(r'(?<![0-9a-f])([0-9a-f]{10})(?![0-9a-f])');refs={}
 for i,l in poss:
  for hn in pat.findall(l):refs.setdefault(hn,[]).append(i)
 assert len(refs)>20
 q=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab cat-file --batch-check'],input=('\n'.join(refs)+'\n').encode(),capture_output=True,timeout=35);q.check_returncode();resolved=q.stdout.decode().splitlines()
 def batchmeta():
  words=shlex.join(refs);cp=git('show --no-patch --format=%H%x09%ct%x09%s '+words).decode().splitlines();return {a[0][:10]:a for a in (x.split('\t',2)for x in cp)if len(a)==3}
 meta=batchmeta();rs=[]
 for (k,linesci),actual in zip(refs.items(),resolved):
  hh=actual.split()[0];hit=[i for i,l in enumerate(lo,1)if re.search(r'(?<![a-f0-9])'+k+r'(?![a-f0-9])',l)];tail=[{'line':i,'field3_commit_cell':lo[i-1].split('|')[3].strip()[:145]if lo[i-1].startswith('|')and len(lo[i-1].split('|'))>3 else None,'line_hash':hashlib.sha256(lo[i-1].encode()).hexdigest(),'mentions_L3b':bool(re.search('L3b',lo[i-1],re.I))}for i in hit]
  rs.append({'commit_short':k,'oid':hh if 'commit'in actual else None,'object_reply':actual,'meta':meta.get(k),'report_rows':linesci,'log_matches':tail,'exact_T10_commit_cell_containing_hash':any(k in (r['field3_commit_cell']or'')for r in tail)})
 out={'utc':now(),'criterion':'T35.09-R3-001','original_scope':r7map['T35.09-R3-001']['source_row'],'report_source':block(rp,roid,[200]+[i for i,l in poss]),'T10_log_source':{'path':lg,'oid':logoid},'nominal_reports':rs,'results':{'explicit_commits_in_report_table_rows':len(refs),'git_verified_commit':sum(bool(z['oid'])for z in rs),'at_least_one_literal_any_logrow':sum(bool(z['log_matches'])for z in rs),'exact_commit_cell_contains_hash':sum(z['exact_T10_commit_cell_containing_hash']for z in rs),'missing_literal_original_log': [z['commit_short']for z in rs if not z['log_matches']]},'limit':'Raportul codului poate lega hashul comitului precedent pe rândul următor; o mențiune în proză nu substituie intrarea T10 directă. Nu se concluzionează lipsa T10 pentru commituri disponibile în alte jurnale sau sub o formă prescurtată; instalarea clasei rămâne separată.'}
 p=P9/'T35_09_predare_commituri.json';wr(p,out);print(sha(f),sha(p),out['results'])
if __name__=='__main__':check()

