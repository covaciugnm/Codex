import pathlib, json, re, hashlib, math, collections, zipfile, subprocess

root=pathlib.Path(__file__).resolve().parent.parent
out=root/'firmware-analiza'
out.mkdir(exist_ok=True)
work=pathlib.Path((root/'inventar/work-directory.txt').read_text(encoding='utf-8').strip())
raw=work/'raw'
if not raw.is_dir(): raw=root/'extras/apk'
src=work/'jadx/app/src/main/java'
if not src.is_dir(): src=root/'reconstituit/jadx/app/src/main/java'

def save(name,value):
    (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def binary_info(f):
    b=f.read_bytes(); sample=b[:1024*1024];freq=collections.Counter(sample)
    entropy=-sum((v/len(sample))*math.log2(v/len(sample)) for v in freq.values()) if sample else 0
    magic='unidentified'
    for sig,label in [(b'\x7fELF','ELF'),(b'\xca\xfe\xba\xbe','Java class / CAFEBABE'),(b'PK\x03\x04','ZIP'),(b'\x1f\x8b','gzip'),(b'\xfd7zXZ\x00','XZ'),(b'hsqs','SquashFS LE'),(b'ANDROID!','Android boot image'),(b'\x3a\xff\x26\xed','Android sparse image'),(b'\x27\x05\x19\x56','U-Boot uImage')]:
        if b.startswith(sig): magic=label;break
    return dict(file=f.relative_to(raw).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),head32=b[:32].hex(),magic=magic,entropyFirstMiB=round(entropy,5),note='Entropy and filename do not prove encryption or executable firmware.')

bins=[binary_info(f) for f in raw.rglob('*') if f.is_file() and f.suffix.lower() in ['.bin','.fw','.img','.dfu','.elf','.rom','.upd','.pac']]
models=[]
for entry in bins:
    if 'ant_iflytekair2' in entry['file'] or 'ant_rayneov4' in entry['file']:
        entry['classification']='Audio model loaded by AgseEncoder on Android; not established as glasses firmware.'
        entry['source']='com/alipay/glass/audio/AgseEncoder.java'
    elif 'AssetManifest' in entry['file']: entry['classification']='Flutter asset manifest.'
    elif 'DebugProbesKt' in entry['file']: entry['classification']='Kotlin debug resource.'
    elif 'FYJ2mic' in entry['file']:
        data=(raw/entry['file']).read_bytes()
        text=data[4:12000].decode('utf-8','replace').lstrip()
        model,consumed=json.JSONDecoder().raw_decode(text)
        model_file=pathlib.Path(entry['file']).stem+'.json'
        save(model_file,model)
        entry['classification']='Embedded neural-network graph (FC, Relu, FSMN, etc.); not a CPU firmware image.'
        entry['modelJson']=model_file
        models.append({'file':entry['file'],'json':model_file,'nodes':len(model.get('nodes',[])),'operators':dict(collections.Counter(n.get('op') for n in model.get('nodes',[])))})
    elif 'EVAD_ESR' in entry['file']:
        entry['classification']='Audio/VAD resource candidate; executable glasses firmware not established.'
save('fisiere-binare.json',bins)
save('modele-audio.json',models)

app=raw/'lib/arm64-v8a/libapp.so'
b=app.read_bytes();selected=[];download_urls=[];allurls=[]
pat=re.compile(r'firmware|Firmware|ota_|_ota|/ota|ota[A-Z]|Ota|OTA|download_url|downloadUrl|upgradeUrl|/hardware/upgrade/')
for m in re.finditer(rb'[\x20-\x7e]{5,}',b):
    text=m.group().decode('ascii')
    if pat.search(text): selected.append({'offset':m.start(),'offsetHex':hex(m.start()),'text':text[:3000]})
    for url in re.findall(r'https?://[^\s<>"\x00]+',text):
        allurls.append(url)
        if re.search(r'firmware|/ota|\.bin(?:[?#]|$)|\.fw(?:[?#]|$)|upgrade',url,re.I):
            download_urls.append({'offset':m.start(),'url':url})
save('indicii-dart-ota.json',selected)
save('urluri-candidate-ota.json',download_urls)

# Inventory archive member names only; third-party SDK examples are not attributed to this model.
software=root.parent
listed=subprocess.run(['rg','--files',str(software)],capture_output=True,text=True,encoding='utf-8',check=True).stdout.splitlines()
archive_findings=[];archives_scanned=0;errors=[]
for name in listed:
    f=pathlib.Path(name)
    if f.suffix.lower() not in ['.zip','.aar']: continue
    if root in f.parents: continue
    try:
        with zipfile.ZipFile(f) as z:
            archives_scanned+=1
            matches=[]
            for i in z.infolist():
                if re.search(r'(?:firmware|(?:^|/)ota(?:/|_)|\.(?:bin|fw|img|dfu|elf|rom|upd)$)',i.filename,re.I):
                    item={'entry':i.filename,'bytes':i.file_size}
                    if 0<i.file_size<250 and not i.is_dir():
                        small=z.read(i)
                        if small.startswith(b'version https://git-lfs.github.com/spec/v1'):
                            item['classification']='Git LFS pointer, not the binary payload'
                            item['pointer']=small.decode('ascii').strip()
                    matches.append(item)
            if matches: archive_findings.append({'archive':str(f.relative_to(software)).replace('\\','/'),'matches':matches,'modelCompatibility':'unverified'})
    except (OSError,zipfile.BadZipFile) as e: errors.append({'file':str(f),'error':str(e)})
save('arhive-candidati.json',archive_findings)

refs=[]
for file,needles in {
'com/example/recorde_translate_plugin/glass/GlassOTAManager.java':['public void startOTA','/ota_package.bin','private void enterOTA()','MD5Utils.getMd5','private File getCurrentTransferFile'],
'com/alipay/glass/audio/AgseEncoder.java':['private boolean loadModelFromAssets','ant_iflytekair2_model_v1.5.bin'],
'com/example/recorde_translate_plugin/glass/wifip2p/WifiManagerPlugin.java':['startGlassOTA','filePath','otaVersion'],
}.items():
    text=(src/file).read_text(encoding='utf-8')
    for needle in needles:
        pos=text.find(needle)
        if pos>=0: refs.append({'file':file,'line':text[:pos].count('\n')+1,'needle':needle,'excerpt':text[max(0,pos-120):pos+1100]})
save('dovezi-sursa.json',refs)
summary={'apk':'com.iflytek.translateapp 1.0.3899','apkSha256':'73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2','binaryAssets':len(bins),'otaRelatedAotStrings':len(selected),'candidateOtaUrls':len(download_urls),'archivesScanned':archives_scanned,'archivesWithCandidates':len(archive_findings),'archiveErrors':errors,'confirmedGlassesFirmwareImages':0,'note':'0 means none identified as this model firmware in this audit; candidates still require format and provenance analysis.'}
summary['extractedNeuralGraphs']=len(models)
summary['userContext']={'ownsGlasses':True,'phonePlatform':'Android','firmwareUpdateDownloaded':False}
save('audit.json',summary)
print(json.dumps(summary,ensure_ascii=False))
