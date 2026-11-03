exec(open('D:/CodexWork/A11A10Inspect.py',encoding='utf-8').read().split("print('MANIFEST'")[0])
with zipfile.ZipFile(B/'Dovezi_complete_lot03.zip') as z:
 for n in ['shell_v2/I01_normal/source.diff','shell/I04_normal/source.diff','shell_v2/I10_normal/source.diff','shell/Preparation_manifest.json','shell_v2/I01_duplicate_last_base/Case_preflight.json','dom/Boundaries.json','pure/Boundaries.json','shell/I04_normal/stdout.txt']:
  t=z.read(n).decode('utf8');print('\nFILE',n,'\n',t[:7000])
