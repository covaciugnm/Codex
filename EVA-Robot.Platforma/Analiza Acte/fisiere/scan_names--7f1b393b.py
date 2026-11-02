import os,re,json,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
root=Path('Z:/')
out=Path(r'C:\Users\User\.codex\visualizations\2026\10\22\01a16433-6d2f-7bf2-93f1-ca88c3efba44')
pat=re.compile(r'aowei|jining|261001|(^|[^a-z])agv([^a-z]|$)|30786697085|5066591032|5071728143|rubber.track|crawler.chassis',re.I)
def scan(top):
 todo=[(str(top),0)]; hits=[]; errors=[]; count=0; dirs=0; deep=0
 while todo:
  loc,depth=todo.pop()
  try:
   with os.scandir(loc) as it:
    for ent in it:
     count+=1
     if pat.search(ent.name):hits.append(ent.path)
     if ent.is_dir(follow_symlinks=False):
      dirs+=1
      if depth<4:todo.append((ent.path,depth+1))
      else:deep+=1
  except OSError as e:errors.append(str(e))
 return dict(root=str(top),entries=count,dirs=dirs,deeper_omitted=deep,hits=hits,errors=errors)
tops=[x for x in root.iterdir() if x.is_dir()]
with ThreadPoolExecutor(max_workers=24) as pool, (out/'scan_shallow.jsonl').open('w',encoding='utf-8') as log:
 for fut in as_completed([pool.submit(scan,x) for x in tops]):
  r=fut.result();log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
  print(r['root'],r['entries'],len(r['hits']),flush=True)
