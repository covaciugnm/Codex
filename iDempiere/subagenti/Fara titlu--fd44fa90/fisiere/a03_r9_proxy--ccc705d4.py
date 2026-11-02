from a03_r9_trace import *
import ast,importlib.util,socket,tempfile
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
def runproxy():
 d=wrk/'frontend';d.mkdir(exist_ok=True); fs=['frontend/app.py','frontend/bnr.py','frontend/i18n.py'];bb=batch([sha+':'+f for f in fs]);sources={}
 for f in fs:
  x,b=bb[sha+':'+f];(d/P(f).name).write_bytes(b);sources[f]={'git_blob':x,'sha256':H(b)}
 # Unchanged route, actual registered Flask decorator; exchange HTTP with a controlled fake backend only.
 (d/'themes').mkdir(exist_ok=True);sys.path.insert(0,str(d)); sys.dont_write_bytecode=True
 os.environ['EVA_API_BASE']='http://example.invalid';os.environ['EVA_DEFAULT_TENANT']='';os.environ['EVA_OP_PROCESS_TIMEOUT']='600'
 connect=socket.socket.connect
 def no_ip(self,addr):
  if self.family in (socket.AF_INET,socket.AF_INET6):raise RuntimeError('IP disabled for R9')
  return connect(self,addr)
 socket.socket.connect=no_ip
 spec=importlib.util.spec_from_file_location('a03_r9_eva_frontend',d/'app.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 calls=[];stubmsg='5. AMORT; pasul anterior nu este efectuat'; m._me_role_user=lambda:('manager','auditor-sintetic')
 def transport(method,path,payload,tenant,timeout):
  calls.append({'method':method,'path':path,'payload':payload,'tenant':tenant,'timeout':timeout})
  from flask import jsonify
  if payload.get('params',{}).get('Operatie')=='timeout':raise TimeoutError('fixture timeout')
  return jsonify({'isError':True,'summary':stubmsg}),200
 m._eva_req=transport
 src=path('T58','dovezi-95-proba-p3/varf-1358b7329a/C-06b_R-A_portal.txt');his=get(src);line=next(z for z in his.decode().splitlines() if z.startswith('$ POST /app/api/operare/'));addr,raw=line[len('$ POST '):].split(' ',1); body=json.loads(raw);c=m.app.test_client(); ev=[]
 def invoke(tag,body):
  before=len(calls);r=c.post(addr,json=body);data=r.get_json(silent=True);ev.append({'id':tag,'status':r.status_code,'redirect_to_login':r.headers.get('Location')=='/app/login','calls':calls[before:],'body_unchanged':bool(calls[before:]) and calls[-1]['payload']==body,'response_is_error':isinstance(data,dict) and data.get('isError') is True,'response_refusal_marker':isinstance(data,dict) and data.get('summary')==stubmsg})
 invoke('no_session',body);c.set_cookie('eva_token','R9-synthetic-token');c.set_cookie('eva_cui','99999958');invoke('negative_gate_payload',body);c.set_cookie('eva_cui','99999959');body2={'params':{**body['params'],'DateFrom':'2026-09-01','DateTo':'2026-09-30'}};invoke('other_tenant_and_period',body2)
 c.set_cookie('eva_cui','99999958');invoke('transport_timeout',{'params':{'Operatie':'timeout'}})
 assert ev[0]['status']==302 and not ev[0]['calls'] and ev[1]['status']==200 and ev[1]['body_unchanged'] and ev[1]['response_refusal_marker'] and ev[2]['calls'][0]['tenant']=='99999959' and ev[3]['status']==504
 src2=get('frontend/app.py').decode().splitlines();ln=[i+1 for i,s in enumerate(src2) if 'return _eva_req("POST", f"/operare/{sub}"' in s];assert len(ln)==1
 J(out/'T58_proxy_intrare.json',{'utc':UTC(),'sha':sha,'criteria':['T58-R2-007','T58-R2-008'],'input_sources':sources,'historical':{'file':src,'sha256':H(his),'body_used':body,'old_note_zero':sum('INCHIDERE-VC' in s and ('→ 0' in s or ' 0' in s) for s in his.decode().splitlines()),'historic_id_verdict':'1358b7329a; rândurile HTTP și SELECT sunt istorice din aceeași anexă, nu au fost copiate în răspunsul din ERPul curent.'},'actual_handler':{'line':ln[0],'role':'Rol manager de laborator injectat la limita serviciului de autentificare. Cookie fără autentificare refuzat de decoratorul original.','real':'Flask original și ruta decorată, JSON decodare/serializare, selectarea firmei, timeout și transmiterea către _eva_req.','mock':'_eva_req primește corpul real și întoarce un refuz sintetic sau timeout; fără autentificare iDempiere și fără acces IP.','trials':ev},'scope':'Compararea intrării fixe prin portal este închisă pe proxy. Conformitatea răspunsului real la poarta AMORT și absența unei note GL la SHA curent nu au fost testate în această rundă.'})
 print('proxy',[(x['id'],x['status']) for x in ev])
if __name__=='__main__':runproxy()

