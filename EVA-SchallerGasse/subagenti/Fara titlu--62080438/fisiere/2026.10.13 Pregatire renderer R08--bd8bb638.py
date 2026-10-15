from pathlib import Path
import hashlib

vis = Path(__file__).resolve().parent
source = vis / '2026.10.13 Renderer contracte elegante R07.py'
target = vis / '2026.10.13 Renderer contracte elegante R08.py'
assert not target.exists(), 'New renderer path required.'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
text = source.read_text(encoding='utf-8')
text = text.replace('VERTRAGSVORSCHLAG', 'WERKVERTRAG')
text = text.replace("subject='Vertragsvorschlag'", "subject='WERKVERTRAG'")
text = text.replace("{'renderer':'2026.10.13 R07','contracts':results}", "{'renderer':'2026.10.13 R08','contracts':results}")
start = text.index('def inferred_cover(data):')
end = text.index('def rule_table_style():',start)
text = text[:start] + text[end:]
start = text.index('def cover_story(data, sty):')
end = text.index('def build_story(data, sty):',start)
text = text[:start] + text[end:]
start = text.index('    story = cover_story(data,sty)',text.index('def build_story'))
end = text.index("    for category in ['sections','annexes']:",start)
text = text[:start] + """    story = [
        p('WERKVERTRAG',sty['contract_title']),
        Spacer(1,3*mm),
        p('Wohnhaus Schallergasse 35, 1120 Wien',sty['cover']),
        Spacer(1,6*mm),
    ]
""" + text[end:]
style_marker = "        'cover_title': ParagraphStyle('cover_title', fontName='ContractUI-Bold',"
assert style_marker in text
text = text.replace(style_marker, "        'contract_title': ParagraphStyle('contract_title', fontName='ContractUI-Bold',\n            fontSize=22, leading=26, textColor=NAVY),\n" + style_marker)
old_inventory = "    content.extend((f'preamble.{i}',x) for i,x in enumerate(data['preamble'],1))\n"
assert old_inventory in text
text = text.replace(old_inventory,'')
old_process = "    validate_source(data)\n    sty=styles()\n    facts=inferred_cover(data)\n"
assert old_process in text
text = text.replace(old_process,"    validate_source(data)\n    if args.render and data['preamble']:\n        raise ValueError('R08 requires preamble=[]; provide audited R08 JSON before rendering.')\n    sty=styles()\n")
text = text.replace("'version':data['version'],'cover':facts,'fonts':font_records,", "'version':data['version'],'opening':'WERKVERTRAG; project; directly section 1','fonts':font_records,")
assert 'Vorbemerk' not in text
assert 'Vertragsvorschlag' not in text
assert 'VERTRAGSVORSCHLAG' not in text
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8')
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
print('R08 renderer SHA-256:',hashlib.sha256(target.read_bytes()).hexdigest())
print('R07 renderer unchanged SHA-256:',source_hash)
