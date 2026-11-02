from a12_r8_ui import *
p=Path('D:/CodexWork/a12-r8-preview');f=p/'Audit_individual_P01_R8.html';s=f.read_text(encoding='utf8')
if 'table-scroll'not in s:
 s=s.replace('</style>','*{box-sizing:border-box}body{overflow-wrap:anywhere}.table-scroll{max-width:100%;overflow-x:auto;overscroll-behavior-x:contain}.table-scroll table{width:100%;min-width:740px}@media(max-width:575px){body{padding:0 12px;margin:16px auto}.table-scroll td,.table-scroll th{padding:5px 7px}input{width:100%}}</style>').replace('<table><thead>','<div class="table-scroll" role="region" tabindex="0"><table><thead>').replace('</tbody></table>','</tbody></table></div>');f.write_text(s,encoding='utf8')
verify(p)

