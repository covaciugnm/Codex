import os,sys,json,hashlib,zipfile,io,struct,zlib,re,sqlite3,time,gzip,traceback,html
from pathlib import Path
ROOT=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository')
OUT=Path(r'D:\Codex\iFLYTEK-audit\results'); OUT.mkdir(exist_ok=True)
DB=sqlite3.connect(OUT/'catalog.sqlite'); DB.execute('pragma journal_mode=wal')
DB.executescript('''
create table if not exists artifacts(hash text primary key,kind text,bytes integer,stats text);
create table if not exists versions(id text primary key,path text,sha256 text,metadata text);
create table if not exists entries(version text,component text,path text,sha256 text,bytes integer);
create table if not exists classes(artifact text,idx integer,name text,flags integer,superclass text,source text);
create table if not exists methods(artifact text,idx integer,signature text,defined integer,flags integer,code_offset integer,code_hash text,registers integer,inputs integer,debug_offset integer);
create table if not exists fields(artifact text,idx integer,signature text,defined integer,flags integer);
create table if not exists variables(artifact text,method_idx integer,kind text,address integer,register integer,name text,type text,signature text);
create table if not exists evidence(artifact text,method_idx integer,offset integer,category text,kind text,value text);
create table if not exists native_symbols(artifact text,table_name text,name text,type text,binding text,defined integer,address text,size integer);
create table if not exists native_dependencies(artifact text,kind text,value text);
create table if not exists errors(artifact text,stage text,error text);
''')
sha=lambda b:hashlib.sha256(b).hexdigest()
cats={
 'Bluetooth/BLE':r'bluetooth|Bluetooth|Gatt|GATT|RFCOMM|[Bb][Ll][Ee](?:Manager|Device|Service)|0000[0-9a-fA-F]{4}-0000-1000-8000-00805f9b34fb',
 'WiFi/retea':r'Wifi|WiFi|wifi|P2p|P2P|Socket|WebSocket|Datagram|Multicast|MQTT|mqtt|tcp://|udp://|wss?://',
 'USB/drivere':r'UsbDevice|UsbManager|usb/|ttyUSB|ttyS[0-9]|SerialPort|HidDevice|/dev/|libusb|ioctl|firmware|Firmware|[Oo][Tt][Aa]',
 'Imagine/video':r'Camera|MediaCodec|MediaMuxer|Video|video|ImageReader|ImageCapture|jpeg|h264|H264|hevc|HEVC|ffmpeg|FFmpeg|RTSP|rtsp|webrtc|WebRTC',
 'Audio':r'AudioRecord|AudioTrack|AudioManager|Microphone|microphone|MediaRecorder|opus|Opus|pcm|PCM|aac|AAC|Tts|TTS|SpeechRecognizer|speech|Speech',
 'Multilingvism/AI':r'Translat|translat|language|Language|locale|Locale|recogniz|Recogniz|OCR|ocr|ASR|[Ss]ynthesi|[Ss]park|[Xx]fyun|[Ii]flytek',
 'Autentificare/chei':r'api[_-]?[Kk]ey|[Aa]pp[Ss]ecret|[Aa]ccess[Tt]oken|[Rr]efresh[Tt]oken|Authorization|[Ss]ecret[Kk]ey|[Ss]endMsgCode|[Cc]heckCode|[Ll]ogin|[Ee]ncrypt|[Dd]ecrypt|[Ss]ignature|CertificatePinner|TrustManager|HostnameVerifier',
 'Transfer/API':r'https?://|upload|Upload|download|Download|multipart|Multipart|retrofit|Retrofit|okhttp|OkHttp|grpc|[Ff]ile[Tt]ransfer'
}
RX={k:re.compile(v) for k,v in cats.items()}
URL=re.compile(r'(?:https?|wss?|tcp|udp|rtsp)://[^\s\x00<>"\x27]{3,500}')
SENSITIVE=re.compile(r'(?i)(api[_-]?key|secret|password|token|authorization|credential|private[_-]?key)')
def clean(s):
 s=str(s)
 s=re.sub(r'(?i)([?&](?:key|api_key|token|access_token|secret|password|sign|signature)=)[^&#\s]*',r'\1[REDACTAT]',s)
 s=re.sub(r'(?i)(https?://)[^/@\s]+:[^/@\s]+@',r'\1[REDACTAT]@',s)
 s=re.sub(r'(?i)((?:api[_-]?key|appsecret|access_token|password|authorization)\s*[=:]\s*)[^\s,;"\x27}]+',r'\1[REDACTAT]',s)
 if '-----BEGIN ' in s or re.search(r'\beyJ[A-Za-z0-9_-]{20,}\.',s): return '[valoare sensibila omisa; sha256='+sha(s.encode())+']'
 return s[:1500]
def evidence(h,m,off,kind,s):
 cs=[k for k,r in RX.items() if r.search(s)]
 for c in cs: DB.execute('insert into evidence values(?,?,?,?,?,?)',(h,m,off,c,kind,clean(s)))
 return bool(cs)
def uleb(b,p,signed=False):
 n=shift=0
 for _ in range(5):
  x=b[p];p+=1;n|=(x&127)<<shift;shift+=7
  if not x&128:
   if signed and x&64:n-=1<<shift
   return n,p
 raise ValueError('invalid LEB128')
def dex(b,h):
 u2=lambda p:struct.unpack_from('<H',b,p)[0]
 u4=lambda p:struct.unpack_from('<I',b,p)[0]
 if b[:4]!=b'dex\n' or b[4:7] not in (b'035',b'037',b'038',b'039',b'040'):raise ValueError('unsupported DEX header '+repr(b[:8]))
 assert u4(32)==len(b) and u4(40)==0x12345678
 assert u4(8)==zlib.adler32(b[12:])&0xffffffff
 assert b[12:32]==hashlib.sha1(b[32:]).digest()
 strings=[]
 for i in range(u4(56)):
  p=u4(u4(60)+4*i);_,p=uleb(b,p);q=b.index(b'\0',p)
  s=b[p:q].replace(b'\xc0\x80',b'\0').decode('utf-8','surrogatepass'); strings.append(s.encode('utf-16','surrogatepass').decode('utf-16','replace'))
 types=[strings[u4(u4(68)+4*i)] for i in range(u4(64))]
 protos=[]
 for i in range(u4(72)):
  p=u4(76)+12*i; po=u4(p+8); pars=[] if not po else [types[u2(po+4+j*2)] for j in range(u4(po))]
  protos.append('('+''.join(pars)+')'+types[u4(p+4)])
 fields=[];methods=[]
 for i in range(u4(80)):
  p=u4(84)+8*i;fields.append(types[u2(p)]+'->'+strings[u4(p+4)]+':'+types[u2(p+2)])
 for i in range(u4(88)):
  p=u4(92)+8*i;methods.append(types[u2(p)]+'->'+strings[u4(p+4)]+protos[u2(p+2)])
 fd={};md={}; local_count=0;decoded=0;code_count=0
 def debug(mi,p):
  nonlocal local_count
  if not p:return
  _,p=uleb(b,p);n,p=uleb(b,p)
  for i in range(n):
   v,p=uleb(b,p)
   if v:DB.execute('insert into variables values(?,?,?,?,?,?,?,?)',(h,mi,'parameter',0,i,strings[v-1],None,None));local_count+=1
  addr=0
  while True:
   op=b[p];p+=1
   if op==0:break
   if op==1:v,p=uleb(b,p);addr+=v
   elif op==2:_,p=uleb(b,p,True)
   elif op in (3,4):
    reg,p=uleb(b,p);name,p=uleb(b,p);typ,p=uleb(b,p);sig=0
    if op==4:sig,p=uleb(b,p)
    DB.execute('insert into variables values(?,?,?,?,?,?,?,?)',(h,mi,'local',addr,reg,strings[name-1] if name else None,types[typ-1] if typ else None,strings[sig-1] if sig else None));local_count+=1
   elif op in (5,6):_,p=uleb(b,p)
   elif op==9:_,p=uleb(b,p)
   elif op>=10:addr+=(op-10)//15
 widths=[1]*256
 for x in [2,5,8,0x13,0x15,0x16,0x19,0x1a,0x1c,0x1f,0x20,0x22,0x23,0x29,*range(0x2d,0x3e),*range(0x44,0x6e),*range(0x90,0xb0),*range(0xd0,0xe3),0xfe,0xff]:widths[x]=2
 for x in [3,6,9,0x14,0x17,0x1b,0x24,0x25,0x26,0x2a,0x2b,0x2c,*range(0x6e,0x73),*range(0x74,0x79),0xfc,0xfd]:widths[x]=3
 widths[0x18]=5;widths[0xfa]=widths[0xfb]=4
 def code(mi,p):
  nonlocal decoded,code_count
  code_count+=1
  regs,ins,outs,tries,dbg,n=struct.unpack_from('<HHHHII',b,p);start=p+16;end=start+2*n;pc=0
  while pc<n:
   pos=start+2*pc;unit=u2(pos);op=unit&255;w=widths[op]
   if op==0 and unit:
    if unit==0x100:w=4+2*u2(pos+2)
    elif unit==0x200:w=2+4*u2(pos+2)
    elif unit==0x300:w=4+(u2(pos+2)*u4(pos+4)+1)//2
    else:raise ValueError('bad payload')
   if pc+w>n:raise ValueError('instruction bounds')
   if op in (0x1a,0x1b):
    idx=u2(pos+2) if op==0x1a else u4(pos+2);s=strings[idx]
    evidence(h,mi,pc,'const-string',s)
    for url in URL.findall(s):DB.execute('insert into evidence values(?,?,?,?,?,?)',(h,mi,pc,'Endpoint','const-string',clean(url)))
   elif op in (*range(0x6e,0x73),*range(0x74,0x79),0xfa,0xfb):evidence(h,mi,pc,'invoke',methods[u2(pos+2)])
   elif 0x52<=op<=0x6d:evidence(h,mi,pc,'field-use',fields[u2(pos+2)])
   pc+=w;decoded+=1
  assert pc==n
  debug(mi,dbg)
  return regs,ins,dbg,sha(b[start:end])
 for i in range(u4(96)):
  p=u4(100)+32*i;ci,flags,sup,interfaces,source,ann,data,stat=struct.unpack_from('<8I',b,p)
  DB.execute('insert into classes values(?,?,?,?,?,?)',(h,ci,types[ci],flags,types[sup] if sup!=0xffffffff else None,strings[source] if source!=0xffffffff else None))
  if data:
   counts=[]
   for _ in range(4):v,data=uleb(b,data);counts.append(v)
   for count in counts[:2]:
    idx=0
    for _ in range(count):delta,data=uleb(b,data);idx+=delta;fl,data=uleb(b,data);assert idx not in fd;fd[idx]=fl
   for count in counts[2:]:
    idx=0
    for _ in range(count):
     delta,data=uleb(b,data);idx+=delta;fl,data=uleb(b,data);co,data=uleb(b,data);assert idx not in md
     regs=ins=dbg=0;ch=None
     if co:
      try:regs,ins,dbg,ch=code(idx,co)
      except Exception as ex:DB.execute('insert into errors values(?,?,?)',(h,'method-code:'+str(idx),str(ex)))
     md[idx]=(fl,co,ch,regs,ins,dbg)
 DB.executemany('insert into methods values(?,?,?,?,?,?,?,?,?,?)',[(h,i,s,1,*md[i]) if i in md else (h,i,s,0,None,None,None,None,None,None) for i,s in enumerate(methods)])
 DB.executemany('insert into fields values(?,?,?,?,?)',[(h,i,s,int(i in fd),fd.get(i)) for i,s in enumerate(fields)])
 for i,s in enumerate(strings):
  for url in URL.findall(s):DB.execute('insert into evidence values(?,?,?,?,?,?)',(h,None,i,'Endpoint','string-pool',clean(url)))
 return dict(version=b[4:7].decode(),strings=len(strings),classes=u4(96),method_ids=len(methods),defined_methods=len(md),field_ids=len(fields),defined_fields=len(fd),debug_variables=local_count,code_methods=code_count,instructions=decoded,checksum=True,[CREDENTIAL_REDACTED]
def elf(b,h):
 from elftools.elf.elffile import ELFFile
 ef=ELFFile(io.BytesIO(b));count=0
 for name in ('.dynsym','.symtab'):
  sec=ef.get_section_by_name(name)
  if sec:
   for s in sec.iter_symbols():
    if not s.name:continue
    DB.execute('insert into native_symbols values(?,?,?,?,?,?,?,?)',(h,name,clean(s.name),s['st_info']['type'],s['st_info']['bind'],int(s['st_shndx']!='SHN_UNDEF'),str(s['st_value']),s['st_size']));count+=1
 dyn=ef.get_section_by_name('.dynamic')
 if dyn:
  for t in dyn.iter_tags():
   if t.entry.d_tag=='DT_NEEDED':DB.execute('insert into native_dependencies values(?,?,?)',(h,'NEEDED',t.needed))
 for match in re.finditer(rb'[\x20-\x7e]{6,1500}',b):
  s=match.group().decode()
  if URL.search(s) or re.search(r'(?i)bluetooth|gatt|uuid|wss?://|api[_-]?key|appsecret|sendMsgCode|checkCode|/dev/|rtsp://',s):evidence(h,None,match.start(),'native-string',s)
 return dict(machine=ef['e_machine'],bits=ef.elfclass,symbols=count,has_symtab=ef.get_section_by_name('.symtab') is not None,has_dwarf=ef.has_dwarf_info(),flutter_aot=bool(ef.get_section_by_name('.dynsym') and b'_kDart' in b))
def analyze(b,kind):
 h=sha(b)
 if DB.execute('select 1 from artifacts where hash=?',(h,)).fetchone():return h
 before=DB.execute('select count(*) from errors').fetchone()[0]
 try:stats=dex(b,h) if kind=='dex' else elf(b,h)
 except Exception as ex:stats={'failed':str(ex)};DB.execute('insert into errors values(?,?,?)',(h,kind,traceback.format_exc()))
 stats['errors']=DB.execute('select count(*) from errors').fetchone()[0]-before
 DB.execute('insert into artifacts values(?,?,?,?)',(h,kind,len(b),json.dumps(stats)))
 DB.commit();print('ARTIFACT',kind,h[:12],json.dumps(stats),flush=True);return h
def component(z,vid,name):
 for e in z.infolist():
  if e.is_dir():continue
  if e.filename.endswith(('.dex','.so')):
   b=z.read(e);h=analyze(b,'dex' if e.filename.endswith('.dex') else 'elf')
   DB.execute('insert into entries values(?,?,?,?,?)',(vid,name,e.filename,h,len(b)))
  elif e.filename=='AndroidManifest.xml':
   try:
    from androguard.core.axml import AXMLPrinter
    from lxml import etree
    b=z.read(e);xml=AXMLPrinter(b).get_xml_obj();text=etree.tostring(xml).decode();(OUT/'manifests').mkdir(exist_ok=True)
    safe=re.sub('[^a-zA-Z0-9_.-]','_',vid+'_'+name);(OUT/'manifests'/(safe+'.xml')).write_text(text,encoding='utf-8')
    for el in xml.iter():
     for k,v in el.attrib.items():
      if el.tag in ('uses-permission','uses-feature','activity','service','provider','receiver','uses-library','meta-data'):
       DB.execute('insert into evidence values(?,?,?,?,?,?)',(vid,None,None,'Manifest',el.tag+':'+k,clean(v)))
   except Exception as ex:DB.execute('insert into errors values(?,?,?)',(vid,'manifest:'+name,str(ex)))
  elif re.search(r'assets/.*\.(?:json|xml|txt|js|html|properties|yaml|yml)$',e.filename,re.I) and e.file_size<8_000_000:
   b=z.read(e);s=b.decode('utf-8','replace');h=sha(b)
   for url in sorted(set(URL.findall(s))):DB.execute('insert into evidence values(?,?,?,?,?,?)',(vid,None,None,'Endpoint','asset:'+e.filename,clean(url)))
   if re.search(r'locale|l10n|i18n|language|translation',e.filename,re.I):DB.execute('insert into evidence values(?,?,?,?,?,?)',(vid,None,None,'Multilingvism/AI','asset',e.filename+' sha256='+h))
 DB.commit()
def main():
 from loguru import logger
 logger.disable('androguard')
 inputs=list((ROOT/'collection-2026-11-01/applications').glob('*.apk'))+list((ROOT/'collection-2026-11-01/applications').glob('*.xapk'))+[p for p in (ROOT/'apk-analysis-2026-11-01/.work/inputs').glob('*.apk') if not p.name.startswith('iflytek-')]+list(Path(r'D:\Codex\iFLYTEK-audit\stable-inputs').glob('*.apk'))
 expected={v['sourceSha256'] for v in json.loads((ROOT/'apk-analysis-2026-11-01/catalog.json').read_text())['versions']}
 for vid,h in DB.execute('select id,sha256 from versions').fetchall():
  if h not in expected:
   DB.execute('delete from versions where id=?',(vid,));DB.execute('delete from entries where version=?',(vid,))
 DB.commit()
 seen={r[0] for r in DB.execute('select sha256 from versions')}
 for path in inputs:
  print('INPUT',str(path),flush=True);b=path.read_bytes();h=sha(b)
  if h in seen:continue
  if h not in expected:raise ValueError('input SHA256 not in verified baseline inventory: '+str(path))
  vid=path.stem;meta={'input_bytes':len(b),'type':path.suffix,'derived':('rebuilt' in vid or 'romania40' in vid)}
  DB.execute('insert into versions values(?,?,?,?)',(vid,str(path),h,json.dumps(meta)));DB.commit()
  z=zipfile.ZipFile(io.BytesIO(b))
  if path.suffix=='.xapk':
   meta.update(json.loads(z.read('manifest.json')));DB.execute('update versions set metadata=? where id=?',(json.dumps(meta),vid))
   for e in z.infolist():
    if e.filename.endswith('.apk'):component(zipfile.ZipFile(io.BytesIO(z.read(e))),vid,e.filename)
  else:component(z,vid,path.name)
  seen.add(h);DB.commit()
 DB.executescript('create index if not exists mi on methods(artifact,idx); create index if not exists ev on evidence(artifact,method_idx); create index if not exists ent on entries(version,sha256);')
 DB.execute('pragma wal_checkpoint(truncate)');DB.close()
if __name__=='__main__':main()
