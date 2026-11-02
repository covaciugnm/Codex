from pathlib import Path
import argparse, json, re, hashlib
from pypdf import PdfReader
import pdfplumber

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(s): return re.sub(r'\s+', '', str(s)).replace('\u00ad','').replace('\u200b','')
def inventory(data):
    rows=[]
    rows += [(f'preamble.{i}', v) for i,v in enumerate(data['preamble'],1)]
    for kind in ('sections','annexes'):
        for block in data[kind]:
            n=block['number']; rows.append((f'{kind}.{n}.title', block['title']))
            rows += [(f'{kind}.{n}.paragraph.{i}',v) for i,v in enumerate(block.get('paragraphs',[]),1)]
            for ti,t in enumerate(block.get('tables',[]),1):
                rows += [(f'{kind}.{n}.table.{ti}.header.{i}',v) for i,v in enumerate(t['headers'],1)]
                for ri,r in enumerate(t['rows'],1):
                    rows += [(f'{kind}.{n}.table.{ti}.row.{ri}.cell.{i}',v) for i,v in enumerate(r,1)]
    rows += [(f'signature.{i}',v) for i,v in enumerate(data['signatures'],1)]
    return rows

def main():
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--pdf',required=True); p.add_argument('--report',required=True)
    a=p.parse_args(); src=Path(a.source); target=Path(a.pdf); report=Path(a.report)
    assert not report.exists(),report
    data=json.loads(src.read_text(encoding='utf-8-sig')); r=PdfReader(target)
    texts=[page.extract_text() or '' for page in r.pages]
    # Strip repeated page headers/footer and paragraph continuation labels only.
    clean=[]
    for text in texts:
        lines=text.splitlines()
        lines=[line for line in lines if not re.match(r'^(SCHALLERGASSE 35 \| WERKVERTRAG|(?:BERGER|PECH) \| VERHANDLUNGSENTWURF|2026\.10\.13 \| VERHANDLUNGSENTWURF|Seite \d+ von \d+|(?:§ \d+\(\d+\)|Anlage \d+\(\d+\)) - Fortsetzung)',line)]
        clean.append('\n'.join(lines))
    all_text=norm('\n'.join(clean)); fields=inventory(data)
    missing=[{'id':ref,'text':value} for ref,value in fields if norm(value) not in all_text]
    boundaries=[]
    with pdfplumber.open(target) as doc:
        for i,page in enumerate(doc.pages,1):
            bad=[{'text':c.get('text'),'x0':round(c['x0'],2),'x1':round(c['x1'],2),'top':round(c['top'],2),'bottom':round(c['bottom'],2)} for c in page.chars if c['x0']<0 or c['x1']>page.width+0.5 or c['top']<0 or c['bottom']>page.height+0.5]
            if bad: boundaries.append({'page':i,'characters':bad})
    result={'date':'2026.10.13','provider':data['provider'],'source_sha256':sha(src),'pdf_sha256':sha(target),'pages':len(r.pages),'source_fragments':len(fields),'missing_fragments':missing,'characters_outside_page':boundaries,'visual_review':'separate per-page PNG inspection required','text_status':'PASS' if not missing and not boundaries else 'REVIEW'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['missing_fragments','characters_outside_page']},ensure_ascii=False))
    if missing: print('Missing IDs:',[x['id'] for x in missing])
    assert not missing and not boundaries,'Content/layout extraction concern; inspect report.'

if __name__=='__main__': main()
