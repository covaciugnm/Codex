from a12_r9_read import *
from a12_r8_arch import git,BASE
from pathlib import PurePosixPath
import gzip,hashlib,subprocess,shlex
R9L=Path('D:/CodexWork/a12-r9-isolated');R9L.mkdir(exist_ok=True)
def fetch_oid(oid):
 p=R9L/(oid+'.gz')
 if p.exists():d=gzip.decompress(p.read_bytes())
 else:
  gd=next((z for z in [D/'blobs'/(oid+'.gz'),Path('D:/CodexWork/p01-r6-annex')/(oid+'.gz'),Path('D:/CodexWork/a12-r8-archives')/(oid+'.gz'),Path('D:/CodexWork/a12-r8-morearchive')/(oid+'.gz'),Path('D:/CodexWork/a12-r8-spec-extra')/(oid+'.gz')]if z.exists()),None)
  d=gzip.decompress(gd.read_bytes())if gd else git('cat-file blob '+shlex.quote(oid));p.write_bytes(gzip.compress(d))
 assert hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==oid;return d
def getp(p):
 oo=git('rev-parse '+shlex.quote(BASE+':'+p)).decode().strip();return oo,fetch_oid(oo)
def block(p,oid,jj):
 ls=fetch_oid(oid).decode('utf8').splitlines();return {'path':p,'blob_oid':oid,'commit_tree':BASE,'lines':[{'line':j,'text':ls[j-1],'sha256':hashlib.sha256(ls[j-1].encode()).hexdigest()}for j in jj if 1<=j<=len(ls)]}
if __name__=='__main__':
 for key in ('T04.07-R3-001','T04.08-R3-001','T04.09-R3-001','T35.08-R3-001','T35.09-R3-001'):
  v=r7map[key]['source_row'];p=v['source_file'];o=v['sha_or_git_blob'];i=v['source_position'];ls=fetch_oid(o).decode('utf8').splitlines()
  print('\n',key,len(ls));print('\n'.join(str(j+1)+' '+ls[j][:430] for j in range(max(0,i-4),min(i+3,len(ls)))))

