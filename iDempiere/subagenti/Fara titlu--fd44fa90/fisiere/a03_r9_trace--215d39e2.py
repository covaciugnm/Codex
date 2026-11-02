from a03_r8_base import H,UTC,J,repo,sha,ssh,get,path,P
import collections,sys,subprocess as sp,datetime,os,re,json,shlex,difflib,concurrent.futures as cf
base=P('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');out=base/'executie/R9_pregatire/A03';out.mkdir(parents=True,exist_ok=True);wrk=P('D:/CodexWork/a03-r9');wrk.mkdir(exist_ok=True)
def git(cmd,stdin=None):r=ssh('cd '+repo+' && git '+cmd,stdin);assert r.returncode==0,(cmd,r.stderr[:100]);return r.stdout
def batch(objects):
 orders=list(dict.fromkeys(objects));b=git('cat-file --batch',(''.join(x+'\n' for x in orders)).encode());i=0;res={}
 for o in orders:
  end=b.index(b'\n',i);hdr=b[i:end].decode();hd=hdr.split(' ');i=end+1
  if hd[-1]=='missing':res[o]=None;continue
  assert len(hd)==3 and hd[1]=='blob',hdr;z=int(hd[2]);body=b[i:i+z];i+=z+1;assert __import__('hashlib').sha1(b'blob '+str(z).encode()+b'\0'+body).hexdigest()==hd[0]
  res[o]=(hd[0],body)
 assert i==len(b);return res
def rows(b,strict=True):
 data={}
 for line in b.decode('utf8').splitlines():
  if not line or line.startswith('#'):continue
  c=line.split('\t')
  if len(c)!=10 or not c[-1].isdigit():
   if strict:raise ValueError('invalid inventory format')
   continue
  if strict:assert (c[0],c[1]) not in data
  data[c[0],c[1]]=c
 return data
def original(k):return k[0] if k[0].startswith(('backend/','frontend/','idempiere/','tools/','bootstrap/','provisioner/','proxy/','import-bridge/','mail/','mirror/','scripts/','Spree/')) else 'idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+k[0]
tr=path('T159','dovezi-10/triaj.tsv');old='b7e563428c';bridge='263f6e2fd5a'
def run():
 hist=git('log --full-history --reverse --format=%H '+sha+' -- '+tr).decode().splitlines()
 # Record only commits whose actual first-parent tree changes this file, plus the original parent for each merge.
 stamps=git('show -s --format="%H%x09%P%x09%s" '+' '.join(hist)).decode().splitlines();g={line.split('\t')[0]:(line.split('\t')[1].split(),line.split('\t')[2]) for line in stamps}
 revisions=list(dict.fromkeys([old,bridge,sha]+hist+[p for ps,_ in g.values() for p in ps])); files=batch([v+':'+tr for v in revisions]);fd={v:(rows(files[v+':'+tr][1],v in (old,bridge,sha)) if files[v+':'+tr] else {}) for v in revisions};oldrows=fd[old];current=fd[sha];protected={k:v for k,v in oldrows.items() if v[2] in ('MUTA','TEXT')};assert len(protected)==302 and not set(protected)&set(current)
 ev=[];cut={}
 for c in hist:
  parents,msg=g[c];b=files[c+':'+tr];fp=parents[0] if parents else None
  if not b or not fp or files[fp+':'+tr]==b:continue
  if not set(fd[fp])&set(protected):continue
  lost=set(protected)&(set(fd[fp])-set(fd[c]));gain=set(protected)&(set(fd[c])-set(fd[fp])); 
  if not lost and not gain:continue
  ev.append({'commit':c,'first_parent':fp,'subject':msg,'before':len(set(protected)&set(fd[fp])),'after':len(set(protected)&set(fd[c])),'lost':len(lost),'gain':len(gain)})
  for k in lost:cut.setdefault(k,[]).append((fp,c))
 # Exact occurrences and assigned key tokens in each source, on both snapshots. Do not use them as semantic proof.
 src=sorted(set(original(k) for k in protected)); objects=batch([v+':'+p for v in (old,sha) for p in src]);d=[]; counts=collections.Counter()
 for k,c in sorted(protected.items()):
  p=original(k);p0=objects[old+':'+p];p1=objects[sha+':'+p]
  keys=[x.strip() for x in re.split(';',c[4]) if re.fullmatch(r'[A-Z][A-Z0-9_]*',x.strip())];body0=p0[1].decode('utf8',errors='replace').splitlines() if p0 else [];body1=p1[1].decode('utf8',errors='replace').splitlines() if p1 else []
  pos0=[i+1 for i,x in enumerate(body0) if x.strip()==k[1]];pos1=[i+1 for i,x in enumerate(body1) if x.strip()==k[1]];keypos={key:[i+1 for i,x in enumerate(body1) if re.search(r'(?<!\w)'+re.escape(key)+r'(?!\w)',x)] for key in keys}; otherfile=sum(1 for kk in current if kk[0]!=k[0] and kk[1]==k[1]);stat='FIȘIER_ORIGINAL_LIPSĂ' if not p0 else 'FIȘIER_ABSENT_ACUM' if not p1 else 'TEXT_IDENTIC_RĂMAS_ÎN_ACELAȘI_FIȘIER' if pos1 else 'TEXT_SCHIMBAT_CHEIE_ȚINTĂ_IDENTIFICATĂ_ÎN_FIȘIER' if any(keypos.values()) else 'TEXT_SCHIMBAT_FĂRĂ_CHEIE_ȚINTĂ_ÎN_ACELAȘI_FIȘIER';counts[stat]+=1
  d.append({'pair_hash':H(('\t'.join(k)).encode()),'file':k[0],'verdict':c[2],'lot':c[5],'source_resolved':p,'old_source_blob':p0[0] if p0 else None,'current_source_blob':p1[0] if p1 else None,'old_source_exact_lines':pos0,'current_source_exact_lines':pos1,'current_source_target_key_lines':keypos,'same_inventory_text_different_path_now':otherfile,'inventory_removal_edges_first_parent':cut.get(k,[]),'classification_file_level':stat})
 # Audit comparator on controlled inputs only. No edits to source.
 gen=path('T159','dovezi-10/generator_hardcodari.py');gb=get(gen);(wrk/'guard.py').write_bytes(gb);baseline=files[old+':'+tr][1];cur=files[sha+':'+tr][1];(wrk/'old.tsv').write_bytes(baseline)
 key=next(k for k,v in protected.items() if v[2]=='MUTA');line=protected[key][:];orig_line='\t'.join(line)+'\n';rcases={}
 def test(n,new):
  f=wrk/(n+'.tsv');f.write_bytes(new);r=sp.run([sys.executable,'-X','utf8','-I',wrk/'guard.py','reclasificate',wrk/'old.tsv',f],cwd=wrk,capture_output=True);snew=rows(new);pp=set(protected); present=pp&set(snew);missing=pp-set(snew);bad={k for k in present if snew[k][2] not in ('MUTA','TEXT')};changes={k for k in present if snew[k][2]!=protected[k][2]};rcases[n]={'original_guard_rc':r.returncode,'original_guard_summary':r.stdout.decode('utf8',errors='replace').splitlines()[-1],'independent_present':len(present),'independent_missing':len(missing),'present_verdict_outside_protected':len(bad),'any_distinct_verdict_including_swap_MUTA_TEXT':len(changes),'exact_copy_witness_exit':int(bool(missing or changes)),'candidate_sha256':H(new)}
 test('real_actual',cur);test('full_copy',baseline);test('copy_minus_one',baseline.replace(orig_line.encode(),b'',1));test('one_reintroduced_same',cur+orig_line.encode());z=line[:];z[2]='TEHNIC';test('one_reintroduced_changed',cur+('\t'.join(z)+'\n').encode()); z[2]='TEXT';test('one_reintroduced_other_protected_value',cur+('\t'.join(z)+'\n').encode());z=line[:];z[0]='renamed/'+z[0];test('copied_but_file_renamed',baseline.replace(orig_line.encode(),('\t'.join(z)+'\n').encode(),1))
 assert rcases['copy_minus_one']['exact_copy_witness_exit']==1 and rcases['copy_minus_one']['original_guard_rc']==0 and rcases['one_reintroduced_changed']['original_guard_rc']==1
 J(out/'T159_R2_050_traseu.json',{'utc':UTC(),'criterion':'T159-R2-050','sha':sha,'frozen':old,'ancestor_rebind':{'frozen_blob':files[old+':'+tr][0],'reachable_bridge':bridge,'bridge_blob':files[bridge+':'+tr][0],'freeze_sha256':H(baseline),'target_blob':files[sha+':'+tr][0],'target_sha256':H(cur),'why':'Comitul înghețat din spec nu este strămoș al arborelui final. Comitul accesibil 263f6e2fd5a are exact același blob al inventarului (reidentificare de conținut; nu echivalează commiturile).'},'input_count':len(oldrows),'target_count':len(current),'protected':len(protected),'old_verdict_distribution':dict(collections.Counter(v[2] for v in protected.values())),'protected_renamed_file_text_hypotheses':sum(x['same_inventory_text_different_path_now']>0 for x in d),'common_protected_by_exact_key':len(set(protected)&set(current)),'source_level_counts':dict(counts),'known_edge_locations':sum(bool(x['inventory_removal_edges_first_parent']) for x in d),'changes':ev,'comparator':{'path':gen,'SHA256':H(gb),'controls':rcases,'scope':'Un rând de inventar este cheia (fișier,text), nu o cheie fiscală unică. O potrivire a numelui parametrului în întreg fișierul nu dovedește înlocuirea corectă la acel apel. Testul strict este o probă suplimentară pentru afirmația de păstrare prin copiere, nu o obligație istorică de a menține în inventarul de hardcodări expresiile deja migrate.'},'rows':d})
 print('results',len(revisions),list(counts.items()),len(ev),sum(bool(x['inventory_removal_edges_first_parent']) for x in d));print([(x['commit'][:10],x['before'],x['after'],x['lost'],x['gain']) for x in ev if x['lost']>=10])
if __name__=='__main__':run()

