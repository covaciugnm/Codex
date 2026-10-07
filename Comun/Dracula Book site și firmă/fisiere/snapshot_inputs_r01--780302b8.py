from pathlib import Path
import hashlib,json,datetime,sys,shutil
sys.stdout.reconfigure(encoding='utf-8')
root=Path(r'D:\00. Downloads\Dracula Book\02. ATELIER EDITORIAL - ROMANE 50000')
base=Path(r'D:\00. Downloads\Dracula Book')
sources=[
('SITE_APP',Path(r'S:\dracula-book\public\app.js')),
('H',base/'AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Hotelul_din_Rue_des_Ames_FINAL_v2.docx'),
('HB',base/'AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/Story_Bible_FINAL.docx'),
('HC',base/'AMORIS SERIES/Hotelul din Rue des Âmes/Versiunea 2/ChangeLog_v2.txt'),
('AC',base/'AMORIS SERIES/Dracula Amoris - concept Alex & Isabella.docx'),
('B',base/'AMORIS SERIES/BENEATH THE SKIN OF THE SEA/Versiunea 1/BENEATH_THE_SKIN_OF_THE_SEA_Complete_Novel.docx'),
('SH',base/'AMORIS SERIES/Shadows in the Port/Versiunea 1/Shadows in the Port V1.docx'),
('N',base/'MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/Versiunea 3/Book-1-The-Northern-Crown-EDITED-FINAL.docx'),
('NP',base/'MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/Versiunea 3/DRAMATIS_PERSONAE.md'),
('Z',base/'MYTHICA SERIES/Saga Celor Zece Coroane/Cartea 1 The_Northern_Crown/saga-of-the-ten-crowns-complete-with-book1-world.zip'),
('CAT',base/'00. CATALOG SI REZUMAT.md')]
dest=root/'08_ARHIVA/INTRARI_CANON/20260924-r01'
dest.mkdir(parents=True,exist_ok=False)
index=[]
for id,src in sources:
    data=src.read_bytes();target=dest/(id+src.suffix)
    with target.open('xb') as stream:stream.write(data)
    index.append({'source_id':id,'source_path':str(src),'archive_path':target.relative_to(root).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
(dest/'index.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Copii ale intrărilor-cheie pentru trasabilitate; sursele nu sunt modificate; nu certifică lectura integrală.','files':index},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'copies':len(index),'bytes':sum(x['bytes'] for x in index),'destination':str(dest)},ensure_ascii=False))

