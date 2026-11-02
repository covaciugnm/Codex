from a12_r8_arch_survs import *
for t,pi in [('T224-',r'rezumat|registru|struct|simul|masca|retea|smoke|21.*comit|garz|eliber|intent|G00|scenarii|matrix|matrice|rezultat'),('T06-',r'T-04|test.*compar|suita|bloc_t171|blocuri_t171|109ok|tinte_sql'),('T220-',r'k12|pas0|autoaudit|clasific|rulator|zgar|resp|valid|mot|instan|rulat|scen|gard|eliberare|stare_final|mock_cereri'),('T314-',r'K09|K_09|menu|online_comenzi|canale|K18|K19|r-a2|K11|arbore|txt$'),('T227-',r'proba.*_[ab]|date_|qty|stoc|K-12c|K12c|mutanti_res|r7_.*json|rezultate'),('T04-',r'|x')]:
 m=search(t,pi);print(t,len(m));print('\n'.join(x['file'].split('/',3)[-1] for x in m if re.search(r'03|09|08|14|16|25|40|12|proba',x['file'].split('/',3)[-1]))[-2700:])

