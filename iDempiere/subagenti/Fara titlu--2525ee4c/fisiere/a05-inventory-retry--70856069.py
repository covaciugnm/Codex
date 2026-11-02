import pathlib,concurrent.futures,threading
w=pathlib.Path('/tmp/codex-a05.ObWQES');exec((w/'fixture.py').read_text().split('if __name__')[0])
barrier=threading.Barrier(2)
def again(i):
    t=auth('GardenAdmin','GardenAdmin',11,102,11);barrier.wait(timeout=6);s,b=request('PUT','models/M_Inventory/1000000',{'doc-action':'CO'},t); print('retry',i,s,b.get('DocStatus'),str(b.get('detail',''))[:220],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(again,[1,2]))

