from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
future=' Im Bauwerksbuch sind außerdem die Voraussetzungen und die erforderliche fachliche Qualifikation der für künftige Überprüfungen zuständigen Personen nach § 128a Abs. 4 Z 4 BO für Wien festzuhalten.'
energy='(2a) Der AN übernimmt in das Bauwerksbuch die nach § 128a Abs. 4 Z 7 erforderliche Dokumentation der einschlägigen Maßnahmen und Änderungen gemäß § 118c Abs. 2 und 7. Die AG und zuständigen Energie- beziehungsweise Haustechnikfachplaner liefern die fachfremden Nachweise; der AN fordert sie konkret an, ordnet sie zu und dokumentiert fehlende Grundlagen. Energetische Systemplanung oder Ausführung solcher Maßnahmen werden dadurch nicht beauftragt; tragwerksbezogene Schnittstellen bleiben geschuldet.'
for name,section in [('BERGER','§ 6'),('PECH','§ 8')]:
    p=root/f'2026.10.12 Contract {name} continut.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    s=next(s for s in d['sections'] if s['title'].startswith(section))
    for i,para in enumerate(s['paragraphs']):
        if para.startswith('(2)') and 'für künftige Überprüfungen' not in para:s['paragraphs'][i]+=future
    if name=='BERGER' and not any('§ 128a Abs. 4 Z 7' in x for x in s['paragraphs']):
        ix=next(i for i,x in enumerate(s['paragraphs']) if x.startswith('(2)'))
        s['paragraphs'].insert(ix+1,energy)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(name,hashlib.sha256(p.read_bytes()).hexdigest())
