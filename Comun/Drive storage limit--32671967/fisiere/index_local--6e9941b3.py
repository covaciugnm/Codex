import os,csv,sys,time
sp=sys.argv[1]; root=sys.argv[2]; tag=sys.argv[3]
sizes=set()
with open(os.path.join(sp,'cloud_files.csv'),encoding='utf-8') as f:
    for r in csv.DictReader(f): sizes.add(int(r['size']))
EXCL=[x.lower() for x in [r'C:\Users\User\My Drive (covaciu.gnm@gmail.com)',r'C:\Windows',r'C:\$Recycle.Bin',r'C:\System Volume Information',r'C:\Users\User\AppData\Local\Google\DriveFS']]
out=open(os.path.join(sp,f'local_{tag}.tsv'),'a',encoding='utf-8')
stack=[root]; n=m=0; t=time.time()
while stack:
    d=stack.pop()
    if d.lower().rstrip(chr(92)) in EXCL or os.path.basename(d) in ('$RECYCLE.BIN','System Volume Information'): continue
    try: it=os.scandir(d)
    except Exception: continue
    with it:
      try:
        for e in it:
            try:
                if e.is_dir(follow_symlinks=False): stack.append(e.path)
                elif e.is_file(follow_symlinks=False):
                    n+=1; s=e.stat(follow_symlinks=False).st_size
                    if s in sizes: out.write(f"{e.name.lower()}\t{s}\t{e.path}\n"); m+=1
            except Exception: pass
      except OSError:
        time.sleep(5); stack.append(d)
    if n and n%200000<50: 
        with open(os.path.join(sp,f'progress_{tag}.txt'),'w') as p: p.write(f"{n} scanate {m} candidate {int(time.time()-t)}s\n")
out.close()
with open(os.path.join(sp,f'progress_{tag}.txt'),'w') as p: p.write(f"GATA {n} scanate {m} candidate {int(time.time()-t)}s\n")
