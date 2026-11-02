from a12_r6_exec import *
import importlib.util
current=Path(__file__).parent/'a12_r6_instrument_final.py'
mod=current.parent/'a12_r6_instrument_pdf_only.py'
mod.write_text(current.read_text(encoding='utf8').replace("'final_'+tag","'pdfdeps_'+tag"),encoding='utf8')
spec=importlib.util.spec_from_file_location('a12_r6_instrument_pdf_only',mod); cal=importlib.util.module_from_spec(spec);spec.loader.exec_module(cal)
alln=sp.check_output(['ssh','-o','BatchMode=yes',server,'docker exec eva-idempiere-cesiro ls -1 /opt/idempiere/plugins']).decode().splitlines();rx=r'commons\.commons-(?:compress|io|codec|collections4|math3)|log4j\.api_|slf4j\.api_|wrapped.*(?:SparseBitSet|xmlbeans|curvesapi)|(?:fontbox|pdfbox|openpdf|flying.saucer|openhtmltopdf|xhtmlrenderer)'
def x(name):
 p=fetch('dep-'+name,'docker exec eva-idempiere-cesiro cat /opt/idempiere/plugins/'+name)
 with zipfile.ZipFile(p)as zz:
  for s in zz.namelist():
   if s.endswith('.jar'):
    dst=deps/('inner-'+Path(s).name)
    if not dst.exists():dst.write_bytes(zz.read(s))
 return (name,sha(p))
fl=[n for n in alln if n.endswith('.jar')and re.search(rx,n,re.I)]
with ThreadPoolExecutor(max_workers=5)as pool:man=dict(pool.map(x,fl))
# Maintains original outputs; call test routine against a new immutable destination for this dependency calibration.
re=[]
for tag in ['git','instalat']:
 q=cal.test((tag,'TestT29Tiparire',None));re.append(q)
wr(E6/'T29_martor_font_POI.json',{'jars_native_copied_readonly':man,'runs':re});print([(v['run'],v['witness'][-4:])for v in re])

