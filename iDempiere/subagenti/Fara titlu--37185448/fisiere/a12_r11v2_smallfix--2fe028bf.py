from pathlib import Path
p=Path(__file__).with_name('a12_r11v2_tasklinks.py');s=p.read_text(encoding='utf8');s=s.replace("contab/wms/EvaNotaSetBomEvents.java","contab/component/EvaNotaSetBomEvents.java");p.write_text(s,encoding='utf8')

