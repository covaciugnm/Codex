import os,sys,json,time,subprocess,datetime,collections,html,shutil,ctypes
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import persoane_scan_20261031 as s
import persoane_copy_20261031 as cp
L=s.LOCAL;A=s.AUDIT;D=s.DEST
k=ctypes.windll.kernel32
k.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];k.OpenProcess.restype=wintypes.HANDLE
k.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)];k.CloseHandle.argtypes=[wintypes.HANDLE]
def alive(pid):
    if not pid:return False
    handle=k.OpenProcess(0x1000,False,int(pid))
    if not handle:return False
    code=wintypes.DWORD();ok=k.GetExitCodeProcess(handle,ctypes.byref(code));k.CloseHandle(handle)
    return bool(ok and code.value==259)
def launch(script,label):
    log=open(L/(label+'.log'),'ab',buffering=0)
    p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).parent/script)],stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
    log.close();return p.pid
def report(state):
    scans=cp.records(L/'scan.jsonl');copies=cp.records(L/'copies.jsonl');ocr=cp.records(L/'ocr.jsonl');archives=cp.records(L/'archives.jsonl')
    counts=collections.Counter(r.get('status','') for r in copies)
    unique={r['sha256'] for r in scans if r.get('sha256')}
    needocr={r['sha256'] for r in scans if r.get('sha256') and not r.get('error') and (r.get('blank_pages') or r.get('ext') in s.IMGEXT)}
    ocrdone={r.get('sha256') for r in ocr}
    errors=sum(bool(r.get('error')) for r in scans)
    selection=json.loads((L/'selection.json').read_text('utf-8')) if (L/'selection.json').exists() else {}
    now=datetime.datetime.now().isoformat(timespec='seconds')
    stats={'stare':state,'actualizat':now,'inventar_fisiere':selection.get('inventory',0),'documente_selectate':selection.get('selected',0),'surse_analizate':len(scans),'continuturi_unice_analizate':len(unique),'copii_noi_verificate':counts['COPIAT_VERIFICAT_SHA256'],'surse_deja_reprezentate':counts['DEJA_EXISTENT_SHA256']+counts['DUBLURA_SURSA']+counts['DEJA_EXISTENT'],'ocr_unice_verificate':sum(bool(r.get('ocr_complete')) for r in ocr),'ocr_ramase':len(needocr-ocrdone),'erori_citire':errors,'erori_copiere':counts['EROARE_COPIERE'],'erori_ocr':sum(bool(r.get('ocr_error')) for r in ocr)}
    stats['arhive_inventariate']=len(archives);stats['arhive_cu_continut_necitit']=len(archives)
    invstate=L/'inventory_complete.json'
    if invstate.exists():stats['inventariere_unitate']=json.loads(invstate.read_text('utf-8'))
    (L/'progress.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),'utf-8')
    A.mkdir(parents=True,exist_ok=True)
    (A/'Stadiu.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),'utf-8')
    txt='COMPLETARE DOSARE PERSOANE - 31.10.2026\n\n'+'\n'.join(f'{a}: {b}' for a,b in stats.items())+'\n\nOriginalele nu sunt sterse sau mutate. Documentele anterioare din destinatie nu sunt suprascrise.\nCopiile noi sunt verificate SHA-256. Copiile identice sunt legate in jurnal de fisierul deja pastrat.\nNumele din cale sau continut identifica persoane asociate, nu neaparat titulari exclusivi.\nDatele din numele sursei sunt pastrate; modificat AAAA.LL.ZZ este data modificarii sursei, nu data emiterii.\nDocumentele fara titular confirmat sunt in 99. De verificat. Dosarele comune raman integrale.\nRegistrul Excel din 01.10.2026 ramane istoric; completarea curenta este evidentiata separat in raportul HTML si jurnal.\n\nInventarierea nu inseamna verificare integrala a continutului. Scanarile OCR, arhivele, formatele vechi/protejate si erorile sunt evidentiate separat. Imaginile de produse, fisierele tehnice si temporarele Office nu sunt documente personale si nu sunt copiate automat.\n\nRaport: '+str(A/'Raport completare.html')+'\n'
    (D/'00. Stadiu completare 2026-10-31.txt').write_text(txt,'utf-8-sig')
    (A/'Stadiu.txt').write_text(txt,'utf-8-sig')
    latest={}
    for r in copies:latest[r['source']]=r
    rows=[]
    for r in sorted(latest.values(),key=lambda r:('; '.join(r.get('persons',[])),r.get('target',''))):
        vals=[r.get('status',''),'; '.join(r.get('persons',[])) or 'Titular de verificat',r.get('target',''),r.get('source',''),r.get('date_basis',''),r.get('copy_error','')]
        rows.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in vals)+'</tr>')
    doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>Completare dosare persoane - 31.10.2026</title><style>body{font:14px Arial;margin:25px;color:#182b3b}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd5de;padding:8px;text-align:left;overflow-wrap:anywhere}th{background:#e7eef5;position:sticky;top:0}pre{white-space:pre-wrap}input{padding:10px;width:60%;margin:15px 0}</style><h1>Completare dosare persoane</h1><pre>'+html.escape(txt)+'</pre><input id="q" placeholder="Cauta persoana, sursa sau document" oninput="filterRows()"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['Stare','Persoane asociate','Copie pastrata','Sursa originala','Datare','Observatii'])+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table><script>function filterRows(){let q=document.getElementById("q").value.toLowerCase();document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))}</script></html>'
    (A/'Raport completare.html').write_text(doc,'utf-8')
    # Snapshot logs remain append-only locally; exported copies are generated reports of this run.
    for name in ['copies.jsonl','ocr.jsonl','selection.json','extra_people.json','people.json']:
        if (L/name).exists():shutil.copyfile(L/name,A/name)
    return stats
def main():
    scanpid=int(sys.argv[1]);invpid=int(sys.argv[2]);copypid=int(sys.argv[3]);ocrpid=int(sys.argv[4]) if len(sys.argv)>4 else 0;archivepid=0;archives_started=False
    invhandle=k.OpenProcess(0x1000,False,invpid)
    finalscan=False;lastreport=0;lastcopy=0;scansize=-1;ocrsize=-1;failures=0
    (L/'supervisor_pid.txt').write_text(str(os.getpid()),'ascii')
    while True:
        try:
            invrunning=alive(invpid);scanrunning=alive(scanpid);copyrunning=alive(copypid)
            if invhandle and not invrunning:
                code=wintypes.DWORD();k.GetExitCodeProcess(invhandle,ctypes.byref(code));k.CloseHandle(invhandle);invhandle=None
                (L/'inventory_complete.json').write_text(json.dumps({'exit_code':code.value,'incheiata_fara_erori':code.value==0,'fisiere':len(s.INV.read_text('utf-8-sig').splitlines())}),'utf-8')
            (L/'process_state.json').write_text(json.dumps({'supervisor':os.getpid(),'scan':scanpid,'inventory':invpid,'copy':copypid,'ocr':ocrpid,'archives':archivepid}),'utf-8')
            if not scanrunning and not invrunning and not finalscan:
                scanpid=launch('persoane_scan_20261031.py','scan-final');finalscan=True;scanrunning=True
            if not invrunning and not archives_started:
                archivepid=launch('persoane_archives_20261031.py','archives');archives_started=True
            nsize=(L/'scan.jsonl').stat().st_size if (L/'scan.jsonl').exists() else 0
            osize=(L/'ocr.jsonl').stat().st_size if (L/'ocr.jsonl').exists() else 0
            if not copyrunning and (nsize!=scansize or osize!=ocrsize) and time.time()-lastcopy>60:
                copypid=launch('persoane_copy_20261031.py','copy-batches');lastcopy=time.time();scansize=nsize;ocrsize=osize
            if not alive(ocrpid):
                ocrrows=cp.records(L/'ocr.jsonl');done={r.get('sha256') for r in ocrrows}
                pending=[r for r in cp.records(L/'scan.jsonl') if r.get('sha256') not in done and not r.get('error') and (r.get('blank_pages') or r.get('ext') in s.IMGEXT)]
                if pending:ocrpid=launch('persoane_ocr_20261031.py','ocr-batches')
            if time.time()-lastreport>90:
                stats=report('IN CURS - inventariere / analiza / OCR / copiere')
                print(json.dumps(stats,ensure_ascii=False),flush=True);lastreport=time.time()
            if finalscan and not alive(scanpid) and not alive(copypid) and not alive(ocrpid) and archives_started and not alive(archivepid):
                marker=L/'last_scan_complete.json'
                if not marker.exists() or json.loads(marker.read_text('utf-8')).get('inventory_lines')!=len(s.INV.read_text('utf-8-sig').splitlines()):
                    report('INTRERUPT - analiza nu s-a incheiat; reluare necesara');return
                stats=report('ETAPE AUTOMATE INCHEIATE - consultati erorile si documentele de verificat')
                if not stats['ocr_ramase']:
                    for name in ['scan.jsonl','baseline.json']:
                        if (L/name).exists():shutil.copyfile(L/name,A/name)
                    shutil.copyfile(s.INV,A/'Inventar surse.txt')
                    (L/'supervisor_complete.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),'utf-8')
                    return
            failures=0
        except Exception as e:
            failures+=1;print('SUPERVISOR_ERROR '+repr(e),flush=True)
            if failures>=10:
                (L/'supervisor_error.txt').write_text(repr(e),'utf-8');return
        time.sleep(15)
if __name__=='__main__':main()
