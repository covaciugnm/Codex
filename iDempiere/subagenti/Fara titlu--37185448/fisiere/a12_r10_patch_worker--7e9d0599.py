from pathlib import Path
p=Path(__file__).parent/'a12_r10_native_worker.py';ss=p.read_text(encoding='utf8');ss=ss.replace("j=rf('select log_msg from ad_pinstance_log where ad_pinstance_id='", "msgcol=next(k for k in ['p_msg','log_msg','msgtext']if k in fields('ad_pinstance_log')); j=rf('select '+msgcol+' from ad_pinstance_log where ad_pinstance_id='" );p.write_text(ss,encoding='utf8')
p=Path(__file__).parent/'a12_r10_pg201.py';ss=p.read_text(encoding='utf8');old="v=call(cmd,t,en);out=v.stdout+v.stderr;path=dest/(tag+'.log');";new="""if tag in ['start','stop']:
  of=tmp/(tag+'-capture');ef=tmp/(tag+'-errors')
  with of.open('wb')as fo,ef.open('wb')as fe:
   pp=sp.run(list(map(str,cmd)),stdout=fo,stderr=fe,timeout=t,env=en,creationflags=getattr(sp,'CREATE_NO_WINDOW',0))
  v=sp.CompletedProcess(cmd,pp.returncode,of.read_text(encoding='utf8',errors='replace'),ef.read_text(encoding='utf8',errors='replace'))
 else:v=call(cmd,t,en)
 out=v.stdout+v.stderr;path=dest/(tag+'.log');""";assert old in ss;p=p.with_name('a12_r10_pg201_fixed.py');p.write_text(ss.replace(old,new),encoding='utf8')
