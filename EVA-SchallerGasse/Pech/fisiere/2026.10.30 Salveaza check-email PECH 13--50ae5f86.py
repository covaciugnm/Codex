from pathlib import Path
source=Path('folder map/2026.10.30 Salveaza check-email PECH 10.py').read_text(encoding='utf-8')
replacements={
    '2026.10.30 Dovezi check-email PECH 10.json':'2026.10.30 Dovezi check-email PECH 13.json',
    'Nicio noutate PECH fata de verificarea generala de astazi la 08:15:47.':'Nicio noutate PECH fata de verificarea punctuala de astazi la 10:00:01.',
    'zero relevante PECH: 26 Gmail':'zero relevante PECH: 37 mesaje returnate de controlul Gmail',
    '25 cautari, 42 metadate;':'25 cautari, 53 metadate;'
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new)
exec(compile(source,__file__,'exec'))
