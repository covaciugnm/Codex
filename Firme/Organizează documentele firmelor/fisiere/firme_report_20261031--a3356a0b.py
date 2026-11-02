import json, collections, shutil, time, ctypes, subprocess
from pathlib import Path
ROOT=Path('Z:/00. Firme/00. RAPORT ARHIVA/Colectare 2026-10-31')
LOCAL=Path('C:/Users/User/AppData/Local/Temp/firme-jurnal-20261031.jsonl')
INV=Path('C:/Users/User/AppData/Local/Temp/inventar-firme-20261031.txt')
PY=r'C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe'
SCRIPT=r'C:\Users\User\AppData\Local\Temp\collect_firme_20261031.py'
def alive(pid):
    h=ctypes.windll.kernel32.OpenProcess(0x1000,False,pid)
    if not h:return False
    code=ctypes.c_ulong();ctypes.windll.kernel32.GetExitCodeProcess(h,ctypes.byref(code));ctypes.windll.kernel32.CloseHandle(h)
    return code.value==259
def report(final=False):
    rows=[]
    if LOCAL.exists():
        for line in LOCAL.read_text(encoding='utf-8').splitlines():
            try:rows.append(json.loads(line))
            except Exception:pass
    last={r['source']:r for r in rows}
    copies={r['destination']:r for r in rows if r['status'] in ('copiat_verificat','copie_recuperata_verificata')}
    counts=collections.Counter(r['status'] for r in last.values())
    counts['copii_noi_distincte_verificate']=len(copies)
    byfirm=collections.Counter(f for r in copies.values() for f in r['firms'])
    unclear=[r for r in last.values() if r.get('scan_without_text') or r.get('content_unread') or r.get('error') or r.get('copy_error') or r.get('partial_prior_copy')]
    summary={'stare':'trecere_automata_incheiata' if final else 'in_curs','fisiere_analizate':len(last),'rezultate':dict(counts),'copii_pe_firme':dict(byfirm),'necesita_verificare_continut':len(unclear),'limite':['Scanarile sunt recitite prin OCR in etapa a doua; cele ramase fara text lizibil sunt semnalate.','Formatele binare vechi sunt identificate dupa cale cand nu exista extractor.','ZIP-urile sunt selectate si dupa inventarul intern; arhivele relevante sunt copiate integral, fara extragerea si clasificarea fiecarui membru.','Data actului este folosita numai daca apare explicit in denumire sau intr-un camp Data neechivoc; altfel DATA NECONFIRMATA.','Registrul de firme existent este baza identificarii; actele cu firma neidentificata sigur sunt pastrate la DE VERIFICAT.']}
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'SITUATIE_CURENTA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'NECESITA_VERIFICARE.jsonl').write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in unclear),encoding='utf-8')
    lines=['COLECTARE DOCUMENTE FIRME - 2026-10-31', 'Stare: '+summary['stare'], 'Sursa: intreaga unitate Z:\\', 'Destinatie: Z:\\00. Firme', '', 'Nu se sterg si nu se suprascriu documentele sursa sau cele existente.','Copiile noi sunt verificate prin SHA-256. Dublurile exacte sunt consemnate cu calea exemplarului existent.', '', 'Fisiere analizate: '+str(len(rows))]+[f'{k}: {v}' for k,v in counts.items()]+['','Limite si verificari ramase:']+summary['limite']+['','Copii noi pe firme:']+[f'{k}: {v}' for k,v in sorted(byfirm.items())]
    (ROOT/'CITESTE-MA.txt').write_text('\n'.join(lines),encoding='utf-8-sig')
    return len(rows)
def main():
    import sys
    pid=int(sys.argv[1]);inventory_pid=int(sys.argv[2]);report()
    while alive(pid):time.sleep(30);report()
    while alive(inventory_pid):time.sleep(30);report()
    # Run again after inventory completion to include files discovered after the first snapshot.
    with (ROOT/'CONTINUARE.log').open('a',encoding='utf-8') as out:
        proc=subprocess.Popen([PY,'-u',SCRIPT],stdout=out,stderr=subprocess.STDOUT,creationflags=0x08000000)
        while proc.poll() is None:time.sleep(30);report()
        if proc.returncode!=0:
            report();(ROOT/'EROARE_EXECUTIE.txt').write_text('Continuarea s-a oprit. Vezi CONTINUARE.log. Cod: '+str(proc.returncode));return
    shutil.copyfile(INV,ROOT/'INVENTAR_CAI_SURSA.txt')
    shutil.copyfile(SCRIPT,ROOT/'colectare.py')
    report(True)
if __name__=='__main__':main()
