from a03_r8_archive import *
from decimal import Decimal as N
def main():
 sections=['dovezi-04-executant/auto-verificare','dovezi-66-aud-cod-r1/auto-verificare-rulata-de-auditor']; files=[path('T156',fold+'/C-'+n+'.txt') for n in ['2','3','4','5','6','7','8','16','22'] for fold in sections if path('T156',fold+'/C-'+n+'.txt') in paths];b=bulk(files);res=[]
 for f,(bl,data) in b.items():
  c=f.split('/C-')[-1][:-4];lines=data.decode('utf8',errors='replace').splitlines();q={}
  for line in lines:
   tokens=line.strip().split('|')
   if len(tokens)>1 and tokens[0].startswith('Q-') and all(re.fullmatch(r'-?[0-9]+(?:\.[0-9]+)?',t.strip()) for t in tokens[1:]):q.setdefault(tokens[0],[]).append([N(t) for t in tokens[1:]])
  ok=None;ev=None
  if c=='2' and len(q.get('Q-TOT',[]))==2:
   ev=[r[1:] for r in q['Q-TOT']];ok=ev[0]==ev[1]
  elif c=='3' and len(q.get('Q-A-IN',[]))>=2:ev=q['Q-A-IN'];ok=ev[-1]==[0,0,0] and ev[0]!=ev[-1]
  elif c=='4' and q.get('Q-A-IN') and len(q.get('Q-B-IN',[]))==2:
   a=q['Q-A-IN'][0];b0,b1=q['Q-B-IN'];ev={'A_before':a,'B_before':b0,'B_after':b1,'expected_B_after':[x+y for x,y in zip(a,b0)]};ok=b1==ev['expected_B_after']
  elif c=='5' and q.get('Q-A-IN') and q.get('Q-B-IN'):ev={'A':q['Q-A-IN'],'B':q['Q-B-IN']};ok=None
  elif c=='6' and len(q.get('Q-A-OUT',[]))==2:ev=q['Q-A-OUT'];ok=ev[0]==ev[-1]
  elif c=='16' and len(q.get('Q-PINST',[]))>=2:ev=q['Q-PINST'];ok=ev[0]==[0,0] and ev[-1]==[1,1]
  elif c=='22':
   vals=[dict((k,int(v)) for k,v in re.findall(r'(ad_[a-z]+|para|index|trigger|treenode)=(\d+)',s)) for s in lines];vals=[a for a in vals if len(a)>=8]
   if len(vals)>=2:ev=vals[:2];ok=ev[0]==ev[1]
  if ev is not None:res.append({'historical_criterion':'C-'+c,'file':f,'blob':bl,'sha256':H(data),'values':ev,'recomputed':ok})
 J(out/'T156_recalcul_balanta_istoric.json',{'utc':UTC(),'sha':sha,'scope':'Recalcul contabil pe valorile numerice din probele celor doi autori istorici atunci când fișierele lor conțin seriile complete. Acțiunea de mutare, UI și clona istorică nu sunt lansate de acest proces. Nicio înregistrare productivă nu a fost citită.','items':res})
 print([(r['historical_criterion'],r['recomputed']) for r in res])
if __name__=='__main__':main()

