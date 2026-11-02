"""German contract PDF renderer. Source JSONs are read-only.

No PDF is produced without --render. Run the PDF skill's artifact marker once
before the first authoring invocation. Supply a fresh path for every new edition.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from copy import copy
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, LongTable,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

NAVY = colors.HexColor('#243746')
LINE = colors.HexColor('#CDD4DA')
INK = colors.HexColor('#202B34')
MUTED = colors.HexColor('#596976')
PAPER = colors.white
TINT = colors.HexColor('#F4F6F8')
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
BODY_W = PAGE_W - 2 * MARGIN
BODY_H = PAGE_H - 2 * MARGIN
PAD = 9.0


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def register_fonts(font_dir):
    folder = Path(font_dir)
    choices = {
        'ContractBody': ('cambria.ttc', 0),
        'ContractBody-Bold': ('cambriab.ttf', 0),
        'ContractBody-Italic': ('cambriai.ttf', 0),
        'ContractBody-BoldItalic': ('cambriaz.ttf', 0),
        'ContractUI': ('calibri.ttf', 0),
        'ContractUI-Bold': ('calibrib.ttf', 0),
        'ContractUI-Italic': ('calibrii.ttf', 0),
        'ContractUI-BoldItalic': ('calibriz.ttf', 0),
    }
    used = {}
    for name, (filename, index) in choices.items():
        path = folder / filename
        if not path.is_file():
            raise FileNotFoundError(f'Required Windows font: {path}')
        pdfmetrics.registerFont(TTFont(name, str(path), subfontIndex=index))
        used[name] = {'path': str(path.resolve()), 'sha256': sha(path)}
    for base in ['ContractBody', 'ContractUI']:
        pdfmetrics.registerFontFamily(base, normal=base, bold=base+'-Bold',
            italic=base+'-Italic', boldItalic=base+'-BoldItalic')
    return used


def styles():
    return {
        'body': ParagraphStyle('body', fontName='ContractBody', fontSize=11,
            leading=14, textColor=INK, alignment=TA_LEFT, splitLongWords=True,
            allowWidows=0, allowOrphans=0),
        'label': ParagraphStyle('label', fontName='ContractUI-Bold', fontSize=9,
            leading=11, textColor=NAVY),
        'heading': ParagraphStyle('heading', fontName='ContractUI-Bold', fontSize=15,
            leading=19, textColor=NAVY, spaceAfter=8),
        'contract_title': ParagraphStyle('contract_title', fontName='ContractUI-Bold',
            fontSize=22, leading=26, textColor=NAVY),
        'cover_title': ParagraphStyle('cover_title', fontName='ContractUI-Bold',
            fontSize=26, leading=31, textColor=NAVY),
        'cover': ParagraphStyle('cover', fontName='ContractUI', fontSize=11,
            leading=14, textColor=INK),
        'small': ParagraphStyle('small', fontName='ContractUI', fontSize=9,
            leading=12, textColor=MUTED),
        'table_header': ParagraphStyle('table_header', fontName='ContractUI-Bold',
            fontSize=10, leading=12.5, textColor=NAVY),
        'table_body': ParagraphStyle('table_body', fontName='ContractBody',
            fontSize=11, leading=14, textColor=INK, splitLongWords=True),
        'table_dense': ParagraphStyle('table_dense', fontName='ContractUI',
            fontSize=10, leading=13, textColor=INK, splitLongWords=True),
        'overview': ParagraphStyle('overview', fontName='ContractUI', fontSize=10,
            leading=14, textColor=NAVY),
    }


BOLD_FRAGMENTS = []

def p(text, style):
    # Escaping protects source content from being interpreted as formatting.
    # Unicode, money strings, filenames, dates and source wording stay intact.
    raw = escape(str(text)).replace('\n', '<br/>')
    if BOLD_FRAGMENTS:
        import re
        alternatives = sorted(set(escape(x) for x in BOLD_FRAGMENTS), key=len, reverse=True)
        raw = re.sub('|'.join(re.escape(x) for x in alternatives), lambda m: '<b>'+m.group(0)+'</b>', raw)
    return Paragraph(raw, style)


class RequirementCard(Flowable):
    """A bordered paragraph whose body splits, with its reference repeated.

    The section heading is part of the first card's layout. It cannot be stranded
    above a page break, and does not force an entire long paragraph onto a new page.
    """
    def __init__(self, label, text=None, style_set=None, body=None,
                 heading=None, continuation=False, source_id=None):
        super().__init__()
        self.label = label
        self.styles = style_set
        self.body = body if body is not None else p(text or '', style_set['body'])
        self.heading_text = heading
        self.heading = p(heading, style_set['heading']) if heading else None
        self.continuation = continuation
        self.source_id = source_id or label
        self.spaceBefore = 0
        self.spaceAfter = 6
        self.hAlign = 'LEFT'

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        inner = max(20, availWidth - 2 * PAD)
        suffix = ' - Fortsetzung' if self.continuation else ''
        self.label_para = p(self.label + suffix, self.styles['label'])
        self.label_h = self.label_para.wrap(inner, availHeight)[1]
        self.body_h = self.body.wrap(inner, availHeight)[1]
        self.heading_h = self.heading.wrap(availWidth, availHeight)[1] + 8 if self.heading else 0
        self.card_h = 2 * PAD + self.label_h + 6 + self.body_h
        self.height = self.heading_h + self.card_h
        return self.width, self.height

    def split(self, availWidth, availHeight):
        self.wrap(availWidth, availHeight)
        overhead = self.heading_h + 2 * PAD + self.label_h + 6
        room = availHeight - overhead
        # At least two body lines travel with the reference and heading.
        if room < self.styles['body'].leading * 2:
            return []
        parts = self.body.split(availWidth - 2 * PAD, room)
        if len(parts) < 2:
            return []
        result = []
        for i, part in enumerate(parts):
            result.append(RequirementCard(self.label, style_set=self.styles, body=part,
                heading=self.heading_text if i == 0 else None,
                continuation=self.continuation or i > 0, source_id=self.source_id))
        return result

    def draw(self):
        c = self.canv
        if self.heading:
            height = self.heading_h - 8
            self.heading.drawOn(c, 0, self.height - height)
        c.saveState()
        c.setStrokeColor(LINE)
        c.setFillColor(PAPER)
        c.setLineWidth(.35)
        c.roundRect(0, 0, self.width, self.card_h, 2.5, stroke=1, fill=1)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.1)
        c.line(0, PAD, 0, self.card_h - PAD)
        c.restoreState()
        label_y = self.card_h - PAD - self.label_h
        self.label_para.drawOn(c, PAD, label_y)
        self.body.drawOn(c, PAD, PAD)


class ContractCanvas(Canvas):
    """Numbered footer without a separate PDF regeneration pass."""
    def __init__(self, *args, contract_meta=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_contract_pages = []
        self._contract_outlines = []
        self.contract_meta = contract_meta or {}

    def record_contract_outline(self, label, anchor):
        self._contract_outlines.append((self._pageNumber, label, anchor))

    def showPage(self):
        self._saved_contract_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        pages = len(self._saved_contract_pages)
        for state in self._saved_contract_pages:
            self.__dict__.update(state)
            for page, label, anchor in self._contract_outlines:
                if page == self._pageNumber:
                    self.bookmarkPage(anchor)
                    self.addOutlineEntry(label, anchor, level=0, closed=False)
            self.draw_contract_footer(pages)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_contract_footer(self, total):
        self.saveState()
        self.setStrokeColor(LINE)
        self.setLineWidth(.35)
        self.line(MARGIN, 13.5 * mm, PAGE_W - MARGIN, 13.5 * mm)
        self.setFont('ContractUI', 8.5)
        self.setFillColor(MUTED)
        date = self.contract_meta.get('date', '')
        provider = self.contract_meta.get('provider', '')
        self.drawString(MARGIN, 9 * mm, f'{date} | WERKVERTRAG | {provider}')
        self.drawRightString(PAGE_W - MARGIN, 9 * mm, f'Seite {self._pageNumber} von {total}')
        self.restoreState()


class ContractDoc(BaseDocTemplate):
    def __init__(self, filename, data, **kwargs):
        self.contract_data = data
        self._outline_seen = set()
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN,
            rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
            title=data['title'], author='A&C Wohnart Immobilien GmbH', subject='WERKVERTRAG', **kwargs)
        frame = Frame(MARGIN, MARGIN, BODY_W, BODY_H,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='contract', frames=frame, onPage=self.header))

    def header(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('ContractUI-Bold', 8.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_H - 10.5*mm, 'SCHALLERGASSE 35 | WERKVERTRAG')
        canvas.drawRightString(PAGE_W-MARGIN, PAGE_H-10.5*mm,
            str(self.contract_data['provider'])+' | WERKVERTRAG')
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(.35)
        canvas.line(MARGIN, PAGE_H - 13*mm, PAGE_W-MARGIN, PAGE_H-13*mm)
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, RequirementCard) and flowable.heading_text:
            label = flowable.heading_text
            anchor = 'outline-' + hashlib.sha256(label.encode('utf-8')).hexdigest()[:16]
            if anchor not in self._outline_seen:
                self.canv.record_contract_outline(label, anchor)
                self._outline_seen.add(anchor)


def validate_source(data):
    for key in ['provider', 'title', 'version', 'date', 'preamble', 'sections', 'annexes', 'signatures']:
        if key not in data:
            raise ValueError(f'Missing source field: {key}')
    if len(data['sections']) != 16 or len(data['annexes']) != 6:
        raise ValueError('Expected exactly 16 sections and 6 annexes; confirm the renderer schema if changed.')
    for collection, count in [('sections',16), ('annexes',6)]:
        numbers = [x['number'] for x in data[collection]]
        if numbers != list(range(1,count+1)):
            raise ValueError(f'Nonconsecutive numbering: {collection}')
        for block in data[collection]:
            if not isinstance(block.get('paragraphs', []), list):
                raise ValueError('paragraphs must be a list of unnumbered source strings')
            for table in block.get('tables', []):
                cols = len(table['headers'])
                if not cols or any(len(row) != cols for row in table['rows']):
                    raise ValueError(f'Invalid table in {collection} {block["number"]}')


def rule_table_style():
    return TableStyle([
        ('BOX',(0,0),(-1,-1),.35,LINE),
        ('INNERGRID',(0,0),(-1,-1),.35,LINE),
        ('BACKGROUND',(0,0),(-1,0),TINT),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
    ])


def source_table(table, sty, label):
    cols = len(table['headers'])
    widths = table.get('widths_cm')
    # Presentation-only override: the full German milestone labels fit without
    # a stranded final letter. The source text and operative data stay intact.
    if label == 'Anlage 3 - Tabelle 1' and cols == 3:
        widths = [4.25, 8.25, 4]
    if not widths or len(widths) != cols or any(x <= 0 for x in widths):
        widths = [1] * cols
    total = sum(widths)
    widths = [BODY_W * value / total for value in widths]
    cell_style = sty['table_dense'] if cols >= 5 else sty['table_body']
    # Keep the caption in the repeating table header. A separate caption with
    # keepWithNext can move a whole LongTable onto a fresh page in ReportLab.
    rows = [[p(label, sty['label'])] + [''] * (cols - 1),
            [p(x, sty['table_header']) for x in table['headers']]]
    rows += [[p(x,cell_style) for x in row] for row in table['rows']]
    result = LongTable(rows, colWidths=widths, repeatRows=2,
        splitByRow=1, splitInRow=1, hAlign='LEFT', spaceBefore=0, spaceAfter=8)
    result.setStyle(rule_table_style())
    result.setStyle(TableStyle([
        ('SPAN',(0,0),(-1,0)),
        ('BACKGROUND',(0,0),(-1,0),PAPER),
        ('BACKGROUND',(0,1),(-1,1),TINT),
    ]))
    return [result]


def build_story(data, sty):
    story = [
        p('WERKVERTRAG',sty['contract_title']),
        Spacer(1,3*mm),
        p('Wohnhaus Schallergasse 35, 1120 Wien',sty['cover']),
        Spacer(1,6*mm),
    ]
    for category in ['sections','annexes']:
        for block in data[category]:
            no=block['number']
            head=(f'§ {no}' if category=='sections' else f'Anlage {no}')+' - '+block['title']
            paragraphs=block.get('paragraphs',[])
            for i,body in enumerate(paragraphs,1):
                label=f'§ {no}({i})' if category=='sections' else f'Anlage {no}({i})'
                story.append(RequirementCard(label,body,sty,heading=head if i==1 else None,
                    source_id=f'{category}.{no}.paragraph.{i}'))
            if not paragraphs:
                h=p(head,sty['heading']);h.keepWithNext=True;story.append(h)
            for i,table in enumerate(block.get('tables',[]),1):
                label=(f'§ {no}' if category=='sections' else f'Anlage {no}')+f' - Tabelle {i}'
                story.extend(source_table(table,sty,label))
    if data['signatures']:
        # All existing fields are preserved; no signature or named authority is supplied.
        sig=[p('Unterschriften',sty['heading'])]
        for line in data['signatures']:
            item=p(line,sty['body']);item.spaceAfter=11;sig.append(item)
        story.extend([Spacer(1,5*mm),KeepTogether(sig)])
    return story


def source_inventory(data):
    content=[]
    for category in ['sections','annexes']:
        for block in data[category]:
            no=block['number']
            content.append((f'{category}.{no}.title',block['title']))
            content.extend((f'{category}.{no}.paragraph.{i}',x) for i,x in enumerate(block.get('paragraphs',[]),1))
            for ti,t in enumerate(block.get('tables',[]),1):
                content.extend((f'{category}.{no}.table.{ti}.header.{j}',x) for j,x in enumerate(t['headers'],1))
                for ri,row in enumerate(t['rows'],1):
                    content.extend((f'{category}.{no}.table.{ti}.row.{ri}.cell.{j}',x) for j,x in enumerate(row,1))
    content.extend((f'signature.{i}',x) for i,x in enumerate(data['signatures'],1))
    return [{'id':i,'text':str(t),'sha256_utf8':hashlib.sha256(str(t).encode('utf-8')).hexdigest()} for i,t in content]


def process(source,output,args,font_records):
    source=Path(source).resolve()
    before=sha(source)
    data=json.loads(source.read_text(encoding='utf-8-sig'))
    validate_source(data)
    global BOLD_FRAGMENTS
    BOLD_FRAGMENTS = data.get('bold_fragments', [])
    if args.render and data['preamble']:
        raise ValueError('R08 requires preamble=[]; provide audited R08 JSON before rendering.')
    sty=styles()
    inventory=source_inventory(data)
    result={'source':str(source),'source_sha256':before,'provider':data['provider'],
        'version':data['version'],'opening':'WERKVERTRAG; project; directly section 1','fonts':font_records,
        'layout':{'page':'A4 portrait','margin_mm':18,'body_pt':11,'leading_pt':14,
            'border_pt':.35,'border':'#CDD4DA','accent':'#243746','paragraph_padding_pt':9},
        'sections':16,'annexes':6,'source_text_inventory':inventory,'rendered':False}
    if not args.render:
        # Exercise real font metrics and paragraph splitting, without a Canvas/PDF.
        longest=max((x for s in data['sections'] for x in s['paragraphs']),key=len)
        card=RequirementCard('§ 1(1)',longest,sty,heading='§ 1 - Layoutprüfung')
        result['paragraph_layout_check']={'wrapped_height_pt':card.wrap(BODY_W,BODY_H)[1],
            'split_fragments_at_220pt':len(card.split(BODY_W,220))}
    else:
        if not output:raise ValueError('--output is required with --render')
        output=Path(output).resolve()
        if output.exists():raise FileExistsError(f'Refusing overwrite: {output}')
        output.parent.mkdir(parents=True,exist_ok=True)
        doc=ContractDoc(str(output),data)
        doc.build(build_story(data,sty),canvasmaker=lambda *a,**k:ContractCanvas(*a,
            contract_meta={'provider':data['provider'],'date':data['date']},**k))
        from pypdf import PdfReader
        result.update(rendered=True,output=str(output),output_sha256=sha(output),
            pages=len(PdfReader(output).pages))
    if sha(source)!=before:raise RuntimeError('Source changed during rendering; stop review.')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',action='append',required=True,help='Contract JSON; repeat for both providers')
    parser.add_argument('--output',action='append',help='Fresh PDF path, paired with --source')
    parser.add_argument('--font-dir',default='C:/Windows/Fonts')
    parser.add_argument('--manifest',help='Fresh JSON path for source hashes, fonts and content inventory')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--render',action='store_true',help='Explicit PDF authoring gate; marker must already have run')
    mode.add_argument('--validate-only',action='store_true',help='No PDF; this is also the default')
    args=parser.parse_args()
    if args.render and (not args.output or len(args.output)!=len(args.source)):
        parser.error('Supply one fresh --output per --source')
    if args.manifest and Path(args.manifest).exists():
        raise FileExistsError('Manifest path already exists; use a fresh dated edition')
    fonts=register_fonts(args.font_dir)
    outputs=args.output or [None]*len(args.source)
    results=[process(src,out,args,fonts) for src,out in zip(args.source,outputs)]
    if args.manifest:
        target=Path(args.manifest);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps({'renderer':'2026.10.13 R08','contracts':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k not in ['fonts','source_text_inventory']} for r in results],ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
