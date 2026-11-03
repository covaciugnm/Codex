from a12_r11x_base import *
import re,copy
V=A/'Val_02';V.mkdir(exist_ok=True)
init=A/'Registru_6709_val_01.jsonl.gz';assert sha(init)=='0bcab91235e392d9b6017e3567a27ad2593f2f70ad955e6e448ec118ab6f2571'
R={r['path']:r for r in lines(init)};inputs={};manifest_receipts=[];NEW=[];events=[];input_data={}
def source(p,h=None):
 if rel(p) in input_data:
  if h:assert inputs[rel(p)]['sha256']==h
  return input_data[rel(p)]
 hs=sha(p)
 if h:assert hs==h,(str(p),hs,h)
 inputs[rel(p)]={'path':rel(p),'sha256':hs,'bytes':p.stat().st_size}
 input_data[rel(p)]=read(p)
 return input_data[rel(p)]
def ptr(j,p):
 for t in p.lstrip('/').split('/'):
  if p=='':break
  t=t.replace('~1','/').replace('~0','~');j=j[int(t)]if isinstance(j,list)else j[t]
 return j
def entry(path,sourcefile,pointer,executor,ax,scope,observed=None,limits=None):
 assert path in R
 j=source(sourcefile);value=ptr(j,pointer);assert value is not None
 r=R[path];event={'executor':executor,'source_file':rel(sourcefile),'source_sha256':sha(sourcefile),'pointer':pointer,'scope':scope,'result':observed,'axes':ax,'limits_and_own_axis_values':limits,'candidate':head}
 eid=sha_bytes(json.dumps(event,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())[:24];event['event_id']='R11V2-'+eid
 assert all(e.get('event_id')!=event['event_id']for e in r['evidence'])
 for a in ax:assert a in axes;r['axis'][a]='OBSERVED_ONLY_AT_LINKED_SCOPE'
 r['evidence'].append(event);r['qualifying_executor']=sorted({e['executor']for e in r['evidence']});events.append({**event,'path':path,'file_id':r['id'],'git_oid':r['git_oid']});return event['event_id']
def manifest(p,expected):
 j=source(p,expected);fs=j.get('files',j.get('artifacts'));fs=([{'file':k,'sha256':v if isinstance(v,str)else v['sha256']}for k,v in fs.items()]if isinstance(fs,dict)else fs);assert isinstance(fs,list)
 for r in fs:
  nm=r.get('file',r.get('path'));target=B/nm if nm.startswith('executie/')else p.parent/nm
  assert target.is_file()and sha(target)==r['sha256'],(str(target),r['sha256'])
 manifest_receipts.append({'manifest':ref(p),'verified_members':len(fs),'valid':True});return j

