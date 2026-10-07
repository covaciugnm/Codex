const fs=require('fs'),path=require('path'),zlib=require('zlib');
const base=__dirname;
const data=JSON.parse(fs.readFileSync(path.join(base,'dictionary_data.json'),'utf8').replace(/^\uFEFF/,''));
const output=path.join(base,'Dictionare_RO_EN_DE_FR_ES_2026-10-01.xlsx');
const xmlEscape=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&apos;').replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g,'');
function col(i){let r='';for(i++;i;i=Math.floor((i-1)/26))r=String.fromCharCode(65+(i-1)%26)+r;return r;}
const order=[2,4,7,6,10,8,9,12,14,11,15,16,17,18,19,1,3,5,13,0];
const dictHeaders=order.map(i=>data.headers[i]);
const dictRows=rows=>rows.map(r=>order.map(i=>r[i]));
const dictWidths=[19,24,38,26,70,37,32,70,64,55,65,18,70,60,18,25,16,16,16,12];
const sheets=[
{name:'Ghid si note',headers:['Subiect','Explicație completă'],rows:data.guide,widths:[34,145],subtitle:'Conținutul complet al răspunsului, limitele verificării și instrucțiunile de utilizare.'},
{name:'Catalog complet',headers:dictHeaders,rows:dictRows(data.all),widths:dictWidths,subtitle:'90 de înregistrări. Limbile, adresele complete, formatele, costurile și evaluările sunt păstrate pentru fiecare sursă.'},
{name:'Traduceri',headers:dictHeaders,rows:dictRows(data.all.filter(r=>r[1]==='Traduceri')),widths:dictWidths,subtitle:'58 de înregistrări; toate cele 20 de direcții dintre RO, EN, DE, FR și ES. Fișiere, aplicații și resurse lexicale.'},
{name:'Explicative',headers:dictHeaders,rows:dictRows(data.all.filter(r=>r[1]==='Explicative')),widths:dictWidths,subtitle:'6 variante pentru definiții în aceeași limbă: RO, EN, DE, FR, ES; reader.dict și DEX Android.'},
{name:'Definitii multilingve',headers:dictHeaders,rows:dictRows(data.all.filter(r=>r[1]==='Definiții multilingve')),widths:dictWidths,subtitle:'20 combinații Kaikki. A doua limbă este limba definițiilor; conținutul diferă între ediții.'},
{name:'Carti PDF si EPUB',headers:dictHeaders,rows:dictRows(data.all.filter(r=>r[1]==='Cărți')),widths:dictWidths,subtitle:'6 cărți istorice gratuite. Sunt marcate explicit volumele sau intervalele de litere parțiale.'},
{name:'Recenzii',headers:['Cod','Sursa','Scor / 5','Număr aproximativ recenzii','Aprecieri / evaluare','Critici / limite','Adresă recenzii / sursă','La ce se aplică evaluarea','Precizări'],rows:data.reviewRows,widths:[12,28,16,25,65,65,70,60,65],subtitle:'Scorurile aplicațiilor nu sunt scoruri pentru fiecare pereche. Mărturiile reader.dict sunt publicate de furnizor.'},
{name:'Licente',headers:['Sursa','Condiții de utilizare','Adresă pentru licență / informații','Note / adresă suplimentară'],rows:data.licenseRows,widths:[27,120,85,120],subtitle:'Gratuit la descărcare nu presupune automat dreptul de redistribuire sau integrare într-un program.'}
];
const files=new Map();
function add(name,body){files.set(name,Buffer.from(body,'utf8'));}
const declaration='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
const ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';
const relNs='http://schemas.openxmlformats.org/officeDocument/2006/relationships';
const packageRel='http://schemas.openxmlformats.org/package/2006/relationships';
const styleXML=declaration+'<styleSheet xmlns="'+ns+'">'+
'<numFmts count="1"><numFmt numFmtId="164" formatCode="0.0&quot;/5&quot;"/></numFmts>'+
'<fonts count="4"><font><sz val="11"/><name val="Calibri"/><color rgb="FF203048"/></font><font><b/><sz val="11"/><name val="Calibri"/><color rgb="FFFFFFFF"/></font><font><b/><sz val="18"/><name val="Calibri"/><color rgb="FFFFFFFF"/></font><font><u/><sz val="11"/><name val="Calibri"/><color rgb="FF0563C1"/></font></fonts>'+
'<fills count="5"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF17365D"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFEAF1F8"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFF2F6FB"/><bgColor indexed="64"/></patternFill></fill></fills>'+
'<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left/><right/><top/><bottom style="thin"><color rgb="FFD8E2EE"/></bottom><diagonal/></border></borders>'+
'<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'+
'<cellXfs count="9">'+
'<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'+
'<xf numFmtId="0" fontId="2" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center"/></xf>'+
'<xf numFmtId="0" fontId="0" fillId="3" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>'+
'<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>'+
'<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'+
'<xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'+
'<xf numFmtId="0" fontId="3" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'+
'<xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'+
'<xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'+
'</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>';
add('xl/styles.xml',styleXML);
let hyperlinkCount=0;
sheets.forEach((sheet,i)=>{
const rels=[],hyperlinks=[];
function cell(value,r,c,style){
const ref=col(c)+r;
if(typeof value==='number'&&Number.isFinite(value))return '<c r="'+ref+'" s="'+style+'"><v>'+value+'</v></c>';
return '<c r="'+ref+'" s="'+style+'" t="inlineStr"><is><t xml:space="preserve">'+xmlEscape(value)+'</t></is></c>';
}
const maxCol=col(sheet.headers.length-1),lastRow=sheet.rows.length+4;
let xml=declaration+'<worksheet xmlns="'+ns+'" xmlns:r="'+relNs+'"><dimension ref="A1:'+maxCol+lastRow+'"/><sheetViews><sheetView workbookViewId="0"><pane xSplit="'+(sheet.headers.length>9?2:0)+'" ySplit="4" topLeftCell="'+(sheet.headers.length>9?'C5':'A5')+'" activePane="'+(sheet.headers.length>9?'bottomRight':'bottomLeft')+'" state="frozen"/><selection pane="'+(sheet.headers.length>9?'bottomRight':'bottomLeft')+'" activeCell="'+(sheet.headers.length>9?'C5':'A5')+'" sqref="'+(sheet.headers.length>9?'C5':'A5')+'"/></sheetView></sheetViews><sheetFormatPr defaultRowHeight="18"/><cols>';
sheet.widths.forEach((w,j)=>{const hidden=sheet.headers.length===20&&j>=15?' hidden="1"':'';xml+='<col min="'+(j+1)+'" max="'+(j+1)+'" width="'+w+'" customWidth="1"'+hidden+'/>';});
xml+='</cols><sheetData><row r="1" ht="32" customHeight="1">'+cell('Dicționare — '+sheet.name,1,0,1)+'</row><row r="2" ht="40" customHeight="1">'+cell(sheet.subtitle,2,0,2)+'</row><row r="3" ht="10" customHeight="1"/><row r="4" ht="40" customHeight="1">';
sheet.headers.forEach((v,j)=>xml+=cell(v,4,j,3));xml+='</row>';
sheet.rows.forEach((row,k)=>{
const r=k+5;const isDict=sheet.headers.length===20;
let lines=2;
row.forEach((v,j)=>{if(j>=15&&isDict)return;const capacity=Math.max(10,Math.floor((sheet.widths[j]||30)*0.86));lines=Math.max(lines,Math.ceil(String(v??'').length/capacity)+1);});
const height=Math.min(195,Math.max(sheet.name==='Ghid si note'?35:58,lines*15+8));
xml+='<row r="'+r+'" ht="'+height+'" customHeight="1">';
row.forEach((v,j)=>{
let style=k%2?5:4;
if(typeof v==='string'&&/^https?:\/\/\S+$/.test(v)){
style=k%2?7:6;
const id='rId'+(rels.length+1);
rels.push('<Relationship Id="'+id+'" Type="'+relNs+'/hyperlink" Target="'+xmlEscape(v)+'" TargetMode="External"/>');
hyperlinks.push('<hyperlink ref="'+col(j)+r+'" r:id="'+id+'"/>');hyperlinkCount++;
}
if(sheet.name==='Recenzii'&&j===2&&typeof v==='number')style=8;
xml+=cell(v,r,j,style);
});
xml+='</row>';
});
xml+='</sheetData><autoFilter ref="A4:'+maxCol+lastRow+'"/><mergeCells count="2"><mergeCell ref="A1:'+maxCol+'1"/><mergeCell ref="A2:'+maxCol+'2"/></mergeCells>';
if(hyperlinks.length)xml+='<hyperlinks>'+hyperlinks.join('')+'</hyperlinks>';
xml+='<printOptions horizontalCentered="1"/><pageMargins left="0.3" right="0.3" top="0.4" bottom="0.4" header="0.2" footer="0.2"/><pageSetup orientation="landscape" paperSize="9" fitToWidth="1" fitToHeight="0"/></worksheet>';
add('xl/worksheets/sheet'+(i+1)+'.xml',xml);
if(rels.length)add('xl/worksheets/_rels/sheet'+(i+1)+'.xml.rels',declaration+'<Relationships xmlns="'+packageRel+'">'+rels.join('')+'</Relationships>');
});
add('xl/workbook.xml',declaration+'<workbook xmlns="'+ns+'" xmlns:r="'+relNs+'"><bookViews><workbookView activeTab="0"/></bookViews><sheets>'+sheets.map((s,i)=>'<sheet name="'+xmlEscape(s.name)+'" sheetId="'+(i+1)+'" r:id="rId'+(i+1)+'"/>').join('')+'</sheets><calcPr calcId="191029"/></workbook>');
add('xl/_rels/workbook.xml.rels',declaration+'<Relationships xmlns="'+packageRel+'">'+sheets.map((s,i)=>'<Relationship Id="rId'+(i+1)+'" Type="'+relNs+'/worksheet" Target="worksheets/sheet'+(i+1)+'.xml"/>').join('')+'<Relationship Id="rId'+(sheets.length+1)+'" Type="'+relNs+'/styles" Target="styles.xml"/></Relationships>');
add('_rels/.rels',declaration+'<Relationships xmlns="'+packageRel+'"><Relationship Id="rId1" Type="'+relNs+'/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="'+relNs+'/extended-properties" Target="docProps/app.xml"/></Relationships>');
add('[Content_Types].xml',declaration+'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'+sheets.map((s,i)=>'<Override PartName="/xl/worksheets/sheet'+(i+1)+'.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>').join('')+'<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>');
add('docProps/core.xml',declaration+'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Dicționare RO EN DE FR ES — catalog complet</dc:title><dc:subject>Descărcări, explicații, traduceri, recenzii și licențe</dc:subject><dc:creator>Codex</dc:creator><dc:description>Răspunsul complet organizat în Excel: 90 înregistrări, 20 direcții de traducere și 8 foi.</dc:description><dcterms:created xsi:type="dcterms:W3CDTF">2026-10-01T00:00:00Z</dcterms:created></cp:coreProperties>');
add('docProps/app.xml',declaration+'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><TitlesOfParts><vt:vector size="'+sheets.length+'" baseType="lpstr">'+sheets.map(s=>'<vt:lpstr>'+xmlEscape(s.name)+'</vt:lpstr>').join('')+'</vt:vector></TitlesOfParts></Properties>');
const crcTable=Array.from({length:256},(_,n)=>{let c=n;for(let j=0;j<8;j++)c=(c&1)?0xEDB88320^(c>>>1):c>>>1;return c>>>0;});
function crc32(b){let c=0xFFFFFFFF;for(const byte of b)c=crcTable[(c^byte)&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
const locals=[],centrals=[];let offset=0;
for(const[name,body]of files){
const filename=Buffer.from(name);const compressed=zlib.deflateRawSync(body,{level:9});const crc=crc32(body);
const header=Buffer.alloc(30);header.writeUInt32LE(0x04034b50,0);header.writeUInt16LE(20,4);header.writeUInt16LE(0x800,6);header.writeUInt16LE(8,8);header.writeUInt16LE(((2026-1980)<<9)|(10<<5)|1,12);header.writeUInt32LE(crc,14);header.writeUInt32LE(compressed.length,18);header.writeUInt32LE(body.length,22);header.writeUInt16LE(filename.length,26);
locals.push(header,filename,compressed);
const central=Buffer.alloc(46);central.writeUInt32LE(0x02014b50,0);central.writeUInt16LE(20,4);central.writeUInt16LE(20,6);central.writeUInt16LE(0x800,8);central.writeUInt16LE(8,10);central.writeUInt16LE(((2026-1980)<<9)|(10<<5)|1,14);central.writeUInt32LE(crc,16);central.writeUInt32LE(compressed.length,20);central.writeUInt32LE(body.length,24);central.writeUInt16LE(filename.length,28);central.writeUInt32LE(offset,42);
centrals.push(central,filename);offset+=header.length+filename.length+compressed.length;
}
const cd=Buffer.concat(centrals);const end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(files.size,8);end.writeUInt16LE(files.size,10);end.writeUInt32LE(cd.length,12);end.writeUInt32LE(offset,16);
const result=Buffer.concat([...locals,cd,end]);fs.writeFileSync(output,result);
let cursor=0,verified=0;
while(result.readUInt32LE(cursor)===0x04034b50){
const crc=result.readUInt32LE(cursor+14),compressedLength=result.readUInt32LE(cursor+18),uncompressedLength=result.readUInt32LE(cursor+22),nameLength=result.readUInt16LE(cursor+26),extraLength=result.readUInt16LE(cursor+28);
const name=result.subarray(cursor+30,cursor+30+nameLength).toString();
const start=cursor+30+nameLength+extraLength;const body=zlib.inflateRawSync(result.subarray(start,start+compressedLength));
if(body.length!==uncompressedLength||crc32(body)!==crc||!files.get(name).equals(body))throw Error('ZIP integrity failed: '+name);
cursor=start+compressedLength;verified++;
}
const directions=new Set(data.all.filter(r=>r[1]==='Traduceri').map(r=>r[3]+'-'+r[5]));
if(data.all.length!==90||directions.size!==20||verified!==files.size)throw Error('Completeness check failed');
console.log(JSON.stringify({file:output,bytes:result.length,entries:data.all.length,directions:directions.size,sheets:sheets.map(s=>({name:s.name,rows:s.rows.length})),hyperlinks:hyperlinkCount,zipEntriesVerified:verified},null,2));

