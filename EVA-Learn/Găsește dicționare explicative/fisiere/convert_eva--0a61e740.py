import os,sys,json,time,re,csv,hashlib,sqlite3,zipfile,tarfile,gzip,bz2,lzma,struct,io,shutil,html,unicodedata,traceback
from pathlib import Path
from xml.etree import ElementTree as ET
import xlsxwriter
from pypdf import PdfReader
ROOT=Path(r"\\192.168.100.169\Comun\00.Roboti\EVA.Pro\Learn\EVA_LEARN_DB_35")
WORK=Path(__file__).parent/"eva_conversion_staging"
WORK.mkdir(exist_ok=True)
GROUPS=json.loads((ROOT/"00_Administrare/limbi.json").read_text("utf-8"))
BYCODE={c:g for g in GROUPS for c in g["codes"]}
STATE=ROOT/"00_Administrare/conversion_status.json"
DONE=json.loads(STATE.read_text("utf-8")) if STATE.exists() else {}
COLS=["entry_id","language_code","dialect","script","word","part_of_speech","sense_number","definition_language","definition","translation_language","translation","pronunciation","example","tags","source_id","source_record","quality_status"]
SOURCECOLS=["source_id","source_name","edition","source_url","source_page","license","usage_class","original_file"]
TRANS=["entry_id","target_language","translation","romanization","tags"]
SOUND=["entry_id","ipa","audio_url","ogg_url","mp3_url","tags"]
EXAMPLE=["entry_id","text","translation","reference"]
REPORT=[];ACTIVE={};ALIASES={}
MAXROWS=200000
def clean(s):
    s=str(s or "")
    s=re.sub(r"<br\s*/?>","\n",s,flags=re.I)
    s=re.sub(r"<[^>]+>","",s)
    return html.unescape(s).strip()
def script(s):
    ranges=[("Arab",0x600,0x6ff),("Deva",0x900,0x97f),("Beng",0x980,0x9ff),("Guru",0xa00,0xa7f),("Gujr",0xa80,0xaff),("Orya",0xb00,0xb7f),("Taml",0xb80,0xbff),("Telu",0xc00,0xc7f),("Knda",0xc80,0xcff),("Mlym",0xd00,0xd7f),("Sinh",0xd80,0xdff),("Thai",0xe00,0xe7f),("Mymr",0x1000,0x109f),("Ethi",0x1200,0x137f),("Khmr",0x1780,0x17ff),("Tfng",0x2d30,0x2d7f),("Cyrl",0x400,0x52f),("Han",0x3400,0x9fff)]
    found=[name for name,a,b in ranges if any(a<=ord(c)<=b for c in s)]
    if found:return "+".join(found)
    return "Latn" if any("LATIN" in unicodedata.name(c,"") for c in s) else ""
def safe(s):return re.sub(r"[^A-Za-z0-9_.-]+","_",str(s))[:95]
def txt(node):return "".join(node.itertext()).strip() if node is not None else ""
def localname(n):return n.tag.rsplit("}",1)[-1]
def usage(row):return row[20] if len(row)>20 and row[20] else row[11]
def source_key(row):
    name=row[5];edition=str(row[13]).split(";")[0]
    if name.startswith("FreeDict"):name="FreeDict "+row[2]+"-"+row[4]
    if "WikDict" in name:name="WikDict "+row[2]+"-"+row[4]
    return hashlib.sha256((name+"|"+row[2]+"|"+row[4]+"|"+edition).encode()).hexdigest()[:20]
def jsonstr(v):return json.dumps(v,ensure_ascii=False,separators=(",",":"))
def log(s):print(time.strftime("%H:%M:%S")+" "+s,flush=True)
class Dataset:
    def __init__(self,row,original):
        self.row=row;self.sid=source_key(row);self.group=BYCODE[row[2]]
        self.base=WORK/self.group["folder"]/("src_"+self.sid);self.base.mkdir(parents=True,exist_ok=True)
        self.original=original;self.count=0;self.part=0;self.workbooks=[];self.tables={};self.wb=None
        self.csvfiles={}
        for table,cols in [("entries",COLS),("translations",TRANS),("sounds",SOUND),("examples",EXAMPLE)]:
            f=open(self.base/(table+".csv"),"w",encoding="utf-8-sig",newline="")
            w=csv.writer(f);w.writerow(cols);self.csvfiles[table]=(f,w)
        self.raw=open(self.base/"records.jsonl","w",encoding="utf-8")
        self.db=sqlite3.connect(self.base/"dictionary.sqlite")
        self.db.execute("PRAGMA journal_mode=OFF");self.db.execute("PRAGMA synchronous=OFF")
        for table,cols in [("entries",COLS),("translations",TRANS),("sounds",SOUND),("examples",EXAMPLE),("sources",SOURCECOLS)]:
            self.db.execute("CREATE TABLE "+table+" ("+",".join(c+" TEXT" for c in cols)+")")
        source=[self.sid,row[5],row[13],row[8],row[9],row[11],usage(row),original]
        self.db.execute("INSERT INTO sources VALUES ("+",".join("?" for _ in source)+")",source)
        self.source=source;self.newpart()
    def newpart(self):
        if self.wb:self.wb.close()
        self.part+=1;file=self.base/("DB_"+self.row[2]+"_"+self.row[4]+"_"+self.sid+"_"+str(self.part).zfill(3)+".xlsx")
        self.workbooks.append(file)
        self.wb=xlsxwriter.Workbook(file,{"constant_memory":True,"strings_to_formulas":False,"strings_to_urls":False,"tmpdir":str(WORK)})
        self.header=self.wb.add_format({"bold":True,"bg_color":"#17365D","font_color":"white"})
        self.tables={}
        for table,cols in [("entries",COLS),("translations",TRANS),("sounds",SOUND),("examples",EXAMPLE),("sources",SOURCECOLS),("long_text",["table","row_id","column","part","text"])]:
            sh=self.wb.add_worksheet(table);sh.freeze_panes(1,0);sh.set_row(0,28);sh.write_row(0,0,cols,self.header)
            sh.set_column(0,len(cols)-1,20);self.tables[table]=[sh,1,len(cols)]
        self.tables["entries"][0].set_column(4,4,30);self.tables["entries"][0].set_column(8,8,70)
        self.write_excel("sources",self.source)
    def write_excel(self,table,row):
        sh,n,colcount=self.tables[table]
        if n>=1048575:
            # Auxiliary tables use a new sheet before the Excel limit; never discard rows.
            sh.autofilter(0,0,n-1,colcount-1)
            index=2
            while any(x.name==table[:25]+"_"+str(index) for x in self.wb.worksheets()):index+=1
            sh=self.wb.add_worksheet(table[:25]+"_"+str(index));sh.write_row(0,0,{"translations":TRANS,"sounds":SOUND,"examples":EXAMPLE,"long_text":["table","row_id","column","part","text"]}[table],self.header);n=1
            self.tables[table]=[sh,n,colcount]
        for j,v in enumerate(row):
            value=str(v or "")
            if len(value)>32767 and table!="long_text":
                for k in range(0,len(value),32000):self.write_excel("long_text",[table,row[0],j,k//32000+1,value[k:k+32000]])
                value="[Text integral în long_text / SQLite / CSV]"
            sh.write_string(n,j,value)
        self.tables[table][1]+=1
    def aux(self,table,row):
        self.csvfiles[table][1].writerow(row)
        self.db.execute("INSERT INTO "+table+" VALUES ("+",".join("?" for _ in row)+")",[str(x or "") for x in row])
        self.write_excel(table,row)
    def entry(self,word,definition="",translation="",pos="",sense=1,pron="",example="",tags="",quality="structured_unreviewed",raw=None,translations=None,sounds=None,examples=None,record=""):
        word=str(word).strip()
        if not word:return
        if self.count and self.count%MAXROWS==0:self.newpart()
        eid=hashlib.sha256((self.sid+"|"+str(self.count+1)+"|"+word+"|"+str(sense)).encode()).hexdigest()[:32]
        row=[eid,self.row[2],self.row[1] if self.row[2] in {"arz","ary","apd","pnb","nan","wuu","yue","tzm","rif","shi","kab","azb","azj"} else "",script(word),word,pos,sense,self.row[4] if definition else "",definition,self.row[4] if translation else "",translation,pron,example,tags,self.sid,record,quality]
        self.aux("entries",row);self.count+=1
        if raw is not None:self.raw.write(jsonstr({"entry_id":eid,"source_record":record,"data":raw})+"\n")
        for t in translations or []:
            target=t.get("lang_code") or t.get("code") or ""
            if target in BYCODE:self.aux("translations",[eid,target,t.get("word",""),t.get("roman",""),jsonstr(t.get("tags",[]))])
        for s in sounds or []:self.aux("sounds",[eid,s.get("ipa",""),s.get("audio",""),s.get("ogg_url",""),s.get("mp3_url",""),jsonstr(s.get("tags",[]))])
        for e in examples or []:self.aux("examples",[eid,e.get("text",""),e.get("english",e.get("translation","")),e.get("ref","")])
        if self.count%10000==0:self.db.commit()
    def close(self):
        self.db.commit();self.db.execute("CREATE INDEX entries_word ON entries(word)");self.db.execute("CREATE INDEX entries_language ON entries(language_code)");self.db.execute("CREATE INDEX translations_target ON translations(target_language)");self.db.commit()
        result=self.db.execute("PRAGMA quick_check").fetchone()[0];self.db.close()
        if result!="ok":raise ValueError("SQLite integrity "+result)
        for f,w in self.csvfiles.values():f.close()
        self.raw.close()
        for sh,n,colcount in self.tables.values():sh.autofilter(0,0,max(1,n-1),colcount-1)
        self.wb.close()
        with open(self.base/"sources.csv","w",encoding="utf-8-sig",newline="") as f:w=csv.writer(f);w.writerow(SOURCECOLS);w.writerow(self.source)
        metadata={"source_id":self.sid,"source":self.source,"rows":self.count,"excel_parts":len(self.workbooks),"columns":COLS,"validation":"SQLite quick_check=ok; XLSX ZIP CRC verified; originals retained"}
        (self.base/"METADATA.json").write_text(jsonstr(metadata),"utf-8")
        for file in self.workbooks:
            with zipfile.ZipFile(file) as z:
                if z.testzip():raise ValueError("Invalid XLSX ZIP "+str(file))
        dest=ROOT/self.group["folder"]/"02_Excel_DB"/self.base.name
        shutil.copytree(self.base,dest,dirs_exist_ok=True)
        return {"source_id":self.sid,"group":self.group["folder"],"entries":self.count,"excel_files":len(self.workbooks),"path":str(dest),"sqlite":str(dest/"dictionary.sqlite"),"status":"converted"}
def parse_lines(stream,row,dataset,format,recordprefix=""):
    text=io.TextIOWrapper(stream,encoding="utf-8-sig",errors="replace")
    if format=="jsonl":
        for line_number,line in enumerate(text,1):
            if not line.strip():continue
            try:o=json.loads(line)
            except Exception as e:raise ValueError("Invalid JSONL line "+str(line_number)+": "+str(e))
            code=o.get("lang_code",row[2])
            if code not in BYCODE or code!=row[2]:continue
            senses=o.get("senses") or [{}]
            for si,s in enumerate(senses,1):
                gloss=s.get("glosses",s.get("raw_glosses",[]));gloss=[gloss] if isinstance(gloss,str) else gloss
                dataset.entry(o.get("word",""),definition="\n".join(str(x) for x in gloss),pos=o.get("pos",""),sense=si,pron="; ".join(x.get("ipa","") for x in o.get("sounds",[]) if x.get("ipa")),example="\n".join(e.get("text","") for e in s.get("examples",[])),tags=jsonstr(s.get("tags",[])),raw={"word_record":o,"sense_index":si},translations=s.get("translations",o.get("translations",[])),sounds=o.get("sounds",[]),examples=s.get("examples",[]),record=recordprefix+":"+str(line_number))
    else:
        delimiter="\t" if format in {"tsv","muse"} else ","
        reader=csv.reader(text,delimiter=delimiter)
        for n,parts in enumerate(reader,1):
            if not parts:continue
            if format=="muse" and len(parts)==1:parts=parts[0].split()
            if len(parts)<2:continue
            if n==1 and parts[0].lower() in {"word","source","source_word","src","term","source_term","headword"}:continue
            dataset.entry(parts[0],translation=parts[1],tags=jsonstr(parts[2:]),quality="equivalent_unreviewed",raw=parts,record=recordprefix+":"+str(n))
def parse_tei(stream,row,dataset,prefix=""):
    n=0
    for event,node in ET.iterparse(stream,events=("end",)):
        tag=localname(node)
        if tag not in {"entry","entryFree"}:continue
        n+=1;orths=[txt(x) for x in node.iter() if localname(x)=="orth"]
        if not orths:node.clear();continue
        definitions=[txt(x) for x in node.iter() if localname(x)=="def"]
        quotes=[txt(x) for x in node.iter() if localname(x)=="quote"]
        pos=";".join(txt(x) for x in node.iter() if localname(x)=="pos")
        dataset.entry(orths[0],definition="\n".join(definitions),translation="\n".join(quotes),pos=pos,tags=jsonstr({"alternative_forms":orths[1:]}),raw={"xml":ET.tostring(node,encoding="unicode")},record=prefix+":"+str(n))
        node.clear()
def dict_value(body,seq):
    if not seq:return body.decode("utf-8","replace").rstrip("\0")
    values=[];offset=0
    for i,t in enumerate(seq):
        if i==len(seq)-1:
            segment=body[offset:];offset=len(body)
        elif t.isupper():
            if offset+4>len(body):break
            length=struct.unpack(">I",body[offset:offset+4])[0];offset+=4;segment=body[offset:offset+length];offset+=length
        else:
            end=body.find(b"\0",offset);end=len(body) if end<0 else end;segment=body[offset:end];offset=end+1
        if t.islower():values.append(segment.decode("utf-8","replace").rstrip("\0"))
        else:values.append("[Binary data type "+t+", "+str(len(segment))+" bytes; see original]")
    return "\n".join(values)
def parse_stardict(files,row,dataset):
    ifos=[name for name in files if name.endswith(".ifo")]
    for ifo in ifos:
        meta=files[ifo].decode("utf-8","replace");seq=re.search(r"^sametypesequence=(.*)$",meta,re.M);seq=seq.group(1).strip() if seq else ""
        off64="idxoffsetbits=64" in meta;stem=ifo[:-4]
        idxname=next((x for x in (stem+".idx",stem+".idx.gz") if x in files),None)
        dictname=next((x for x in (stem+".dict",stem+".dict.dz",stem+".dict.gz") if x in files),None)
        if not idxname or not dictname:continue
        idx=files[idxname];idx=gzip.decompress(idx) if idxname.endswith(".gz") else idx
        body=files[dictname];body=gzip.decompress(body) if dictname.endswith((".dz",".gz")) else body
        cursor=0;n=0
        while cursor<len(idx):
            end=idx.find(b"\0",cursor)
            if end<0:raise ValueError("Truncated StarDict index")
            word=idx[cursor:end].decode("utf-8","replace");cursor=end+1
            olen=8 if off64 else 4
            if cursor+olen+4>len(idx):raise ValueError("Truncated StarDict offset")
            offset=int.from_bytes(idx[cursor:cursor+olen],"big");size=int.from_bytes(idx[cursor+olen:cursor+olen+4],"big");cursor+=olen+4;n+=1
            if offset+size>len(body):raise ValueError("StarDict index outside dictionary")
            raw=dict_value(body[offset:offset+size],seq);value=clean(raw)
            if row[2]==row[4]:dataset.entry(word,definition=value,raw={"definition_original":raw,"sametypesequence":seq},record=ifo+":"+str(n))
            else:dataset.entry(word,translation=value,quality="dictionary_gloss_unreviewed",raw={"definition_original":raw,"sametypesequence":seq},record=ifo+":"+str(n))
def b64num(value):
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    n=0
    for c in value:n=n*64+alphabet.index(c)
    return n
def parse_dictd(files,row,dataset):
    for name in [x for x in files if x.endswith(".index")]:
        stem=name[:-6];dn=next((x for x in (stem+".dict",stem+".dict.dz") if x in files),None)
        if not dn:continue
        body=files[dn];body=gzip.decompress(body) if dn.endswith(".dz") else body
        for n,line in enumerate(files[name].decode("utf-8","replace").splitlines(),1):
            parts=line.split("\t")
            if len(parts)<3:continue
            offset,size=b64num(parts[-2]),b64num(parts[-1])
            if offset+size>len(body):raise ValueError("Dictd index outside dictionary")
            value=body[offset:offset+size].decode("utf-8","replace")
            dataset.entry(parts[0],definition=value if row[2]==row[4] else "",translation=value if row[2]!=row[4] else "",quality="dictionary_gloss_unreviewed",raw={"text":value},record=name+":"+str(n))
def book_excel(file,row,job):
    sid=job["id"];g=BYCODE[row[2]];base=WORK/g["folder"]/("document_"+sid);base.mkdir(parents=True,exist_ok=True)
    book=xlsxwriter.Workbook(base/("DOCUMENT_"+sid+".xlsx"),{"constant_memory":True,"strings_to_formulas":False})
    sh=book.add_worksheet("pages");sh.write_row(0,0,["document_id","language_code","page","chunk","text","quality_status","source_url","license"]);sh.freeze_panes(1,0);sh.set_column(4,4,100)
    number=0
    try:
        reader=PdfReader(file,strict=False);texts=((i+1,page.extract_text() or "") for i,page in enumerate(reader.pages))
        for page,text in texts:
            for k in range(0,max(1,len(text)),32000):
                number+=1;values=[sid,row[2],page,k//32000+1,text[k:k+32000],"scan_needs_ocr" if not text.strip() else "page_text_unreviewed",row[8],row[11]]
                for c,v in enumerate(values):sh.write_string(number,c,str(v))
    finally:book.close()
    dest=ROOT/g["folder"]/"02_Excel_DB"/base.name;shutil.copytree(base,dest,dirs_exist_ok=True)
    return {"status":"document_text_only","pages_or_chunks":number,"excel_files":1,"group":g["folder"],"path":str(dest),"note":"Text pe pagini. Nu este segmentat automat în cuvinte/sensuri; scanurile fără text necesită OCR."}
def convert(job):
    src=ROOT/job["path"];cache=WORK/("cache_"+job["id"]+"_"+src.name)
    shutil.copyfile(src,cache)
    outputs=[]
    try:
        rows=job["rows"];first=rows[0];suffix=src.name.lower()
        if suffix.endswith(".pdf"):return [book_excel(cache,first,job)]
        if suffix.endswith((".djvu",".7z",".slob")):return [{"status":"original_retained","reason":"Format special; există originalul. Conversie lexicală automată neconfirmată.","path":str(src)}]
        if suffix.endswith(".xlsx"):return [{"status":"original_excel","path":str(src),"reason":"Excel original păstrat; schema lui trebuie mapată separat."}]
        if suffix.endswith(".zip"):
            archive=zipfile.ZipFile(cache)
            names=archive.namelist()
            exact={r[21]:r for r in rows if len(r)>21 and r[21]}
            tsvnames=[n for n in names if n.lower().endswith((".tsv",".csv")) and (not exact or n in exact)]
            if tsvnames:
                for name in tsvnames:
                    row=exact.get(name,first)
                    if row[2] not in BYCODE:continue
                    key=source_key(row)
                    if key in ALIASES:outputs.append({"status":"converted_alias","source_id":key,"target":ALIASES[key]});continue
                    ds=Dataset(row,job["path"]+"|"+name)
                    with archive.open(name) as stream:parse_lines(stream,row,ds,"tsv" if name.endswith(".tsv") else "csv",name)
                    result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            else:
                xmlnames=[n for n in names if n.lower().endswith((".tei",".xml")) and not "META-INF" in n]
                if xmlnames:
                    for name in xmlnames:
                        key=source_key(first)
                        if key in ALIASES:outputs.append({"status":"converted_alias","source_id":key,"target":ALIASES[key]});break
                        ds=Dataset(first,job["path"]+"|"+name)
                        with archive.open(name) as stream:parse_tei(stream,first,ds,name)
                        result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
                elif any(n.endswith((".ifo",".index")) for n in names):
                    key=source_key(first)
                    if key in ALIASES:outputs.append({"status":"converted_alias","source_id":key,"target":ALIASES[key]})
                    else:
                        files={n:archive.read(n) for n in names if n.endswith((".ifo",".idx",".idx.gz",".dict",".dict.dz",".dict.gz",".index"))}
                        ds=Dataset(first,job["path"]);parse_stardict(files,first,ds) if any(n.endswith(".ifo") for n in files) else parse_dictd(files,first,ds)
                        result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            archive.close()
        elif suffix.endswith((".tar.xz",".tar.bz2",".tar.gz",".tar")):
            archive=tarfile.open(cache,"r:*");members=archive.getmembers()
            xmls=[m for m in members if m.isfile() and m.name.lower().endswith((".tei",".xml"))]
            key=source_key(first)
            if key in ALIASES:outputs.append({"status":"converted_alias","source_id":key,"target":ALIASES[key]})
            elif xmls:
                ds=Dataset(first,job["path"])
                for member in xmls:
                    stream=archive.extractfile(member);parse_tei(stream,first,ds,member.name);stream.close()
                result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            elif any(m.name.endswith((".ifo",".index")) for m in members):
                files={m.name:archive.extractfile(m).read() for m in members if m.isfile() and m.name.endswith((".ifo",".idx",".idx.gz",".dict",".dict.dz",".dict.gz",".index"))}
                ds=Dataset(first,job["path"]);parse_stardict(files,first,ds) if any(n.endswith(".ifo") for n in files) else parse_dictd(files,first,ds)
                result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            archive.close()
        elif suffix.endswith((".jsonl",".jsonl.gz",".tsv",".csv",".txt",".xml",".tei")):
            key=source_key(first)
            if key in ALIASES:outputs.append({"status":"converted_alias","source_id":key,"target":ALIASES[key]})
            elif suffix.endswith((".jsonl",".jsonl.gz",".tsv",".csv")) or "MUSE" in first[5]:
                ds=Dataset(first,job["path"])
                stream=gzip.open(cache,"rb") if suffix.endswith(".gz") else open(cache,"rb")
                format="jsonl" if ".jsonl" in suffix else "tsv" if suffix.endswith(".tsv") else "muse" if "MUSE" in first[5] else "csv"
                with stream:parse_lines(stream,first,ds,format,job["path"])
                result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            elif suffix.endswith((".xml",".tei")):
                ds=Dataset(first,job["path"])
                with open(cache,"rb") as stream:parse_tei(stream,first,ds)
                result=ds.close();ALIASES[key]=result["path"];outputs.append(result)
            else:outputs.append({"status":"original_text","path":str(src),"reason":"Text/OCR integral; segmentarea în intrări nu a fost confirmată."})
        if not outputs:outputs=[{"status":"original_retained","path":str(src),"reason":"Structura nu corespunde formatelor lexicale recunoscute; original păstrat."}]
        return outputs
    finally:
        if cache.exists():cache.unlink()
def save():
    temp=STATE.with_suffix(".tmp")
    temp.write_text(json.dumps(DONE,ensure_ascii=False,indent=2),"utf-8");os.replace(temp,STATE)
def main():
    for result in DONE.values():
        for output in result.get("outputs",[]):
            if output.get("status")=="converted":ALIASES[output["source_id"]]=output["path"]
    count=0
    while True:
        try:jobs=json.loads((ROOT/"00_Administrare/downloads_dictionary.json").read_text("utf-8"))
        except (json.JSONDecodeError,OSError):time.sleep(2);continue
        available=[j for j in jobs if j["status"]=="downloaded" and j["id"] not in DONE]
        available.sort(key=lambda j:(j["path"].lower().endswith((".pdf",".txt",".slob",".djvu")),j.get("bytes",0)))
        for job in available:
            log("Converting "+job["id"]+" "+Path(job["path"]).name)
            try:
                outputs=convert(job);DONE[job["id"]]={"status":"processed","outputs":outputs}
                log("Converted "+job["id"]+" entries="+str(sum(o.get("entries",0) for o in outputs)))
            except Exception as e:
                DONE[job["id"]]={"status":"conversion_failed","error":str(e),"trace":traceback.format_exc()}
                log("Conversion failed "+job["id"]+" "+str(e))
            save();count+=1
        if not any(j["status"] in {"pending","downloading"} for j in jobs) and not available:break
        time.sleep(10)
    log("FINISHED sources="+str(len(DONE))+" entries="+str(sum(o.get("entries",0) for r in DONE.values() for o in r.get("outputs",[]))))
if __name__=="__main__":main()
