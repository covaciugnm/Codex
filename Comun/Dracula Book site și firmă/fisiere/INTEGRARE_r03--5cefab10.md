# Integrare r03 — raport al producătorului, nu verdict de audit
24.09.2026. P-MANAGER. Domeniu G00; 0 cuvinte de roman nou. Originalele și site-ul au rămas numai în citire.

## Modificări și proveniență
P-SYSTEMS a livrat corecțiile F05/F06 în 06_REGISTRU/r03_staging; P-RESEARCH a livrat patru aplicații exploratorii în 02_DOCUMENTARE/r03_staging. Predările exacte sunt în ISTORIC/*-predare-r03.json.
Exportul și testul live diferă de staging numai prin eliminarea unui LF final suplimentar la integrarea textului. Nu sunt byte-identice: SHA live export 1f55842d4ea83ca52083b47f63fd9fa8d7733ebfee7d0b690a574270cc32851c; test 55695a838c123af22922c1ef68cb6cb87ed2f61b1664455f08af65ac972a22d3. Codul executabil este neschimbat; testele au fost rerulate pe fișierele live. Versiunile r02 originale sunt păstrate în CONTEXT_R03/previous-r02-* și în arhive.
APLICATII_WORKID_REALE.md este integrat cu antet DEPUS și notă de integrare; cele patru WorkID-uri reale și sursele nu sunt rescrise. Banca și raportul CANON_EXISTENT nu sunt modificate. RES primește dependență explicită SEL și copii de referință în propriul spațiu de probe.
TRASABILITATE, README-uri, protocolul și modelele 02/06/07 includ revizia r03 și interdicția de a declara 08_ARHIVA drept intrare ingerată. Sunt folosite copii plate cu proveniență pentru indexurile vechi. Nu se relaxează pragul, independența sau calibrarea.

## Verificări efective
Nucleu: 233 teste trecute în 25,499s; TESTE_NUCLEU_INTEGRAT_r03.txt. Nucleul de patru fișiere rămâne v2, neschimbat din r02.
Export: 65 teste trecute, zero skip; log inițial TESTE_EXPORT_INTEGRAT_r03.txt, retest final TESTE_EXPORT_FINAL_r03.txt (1,524s). Total două suite: 298 teste; nu reprezintă 298 de criterii literare sau validare umană.
Export real: history-r03-preaudit are 9 surse /1766 înregistrări /281 mesaje. VERIFICARE_PREFIXE_REALE_r03.json confirmă byte cu byte cele 9 prefixe. Filtrarea datelor interne este păstrată; nu se pretinde arhivarea raționamentelor interne ori recuperarea ieșirilor istorice trunchiate.

## Documente Word/PDF
Regenerare din cele șapte surse ale manualului. 28 pagini. Exporterul primește allowWidows=0/allowOrphans=0 după observarea unui singur cuvânt izolat pe pagina finală; varianta finală a paginii 28 a fost inspectată vizual. Controlul tuturor paginilor nu găsește text în afara paginii; randări punctuale 1/6/7/28 sunt păstrate în VIZUAL_R03_v02. Nu este pretinsă inspecția vizuală manuală integrală.
Compararea inițială COMPARATIE_DOCUMENTE_r03.json a semnalat un paragraf traversând paginile 27/28: subsolul PDF întrerupea căutarea textului. Conținutul nu lipsea. La afișare, consola cp1252 a generat suplimentar UnicodeEncodeError după salvarea rezultatului. Verificatorul v02 exclude doar cele 28 subsoluri recunoscute; o primă execuție v02 a oprit pe o escapare de newline corectată înaintea rezultatului final. Ambele verificatoare și rezultatul inițial rămân păstrate.
COMPARATIE_DOCUMENTE_r03_v02.json: 1146 unități de sursă, ordine exactă în Word după 5 unități de copertă, zero unități lipsă în PDF după eliminarea subsolurilor. Aceasta este verificare structurală, nu evaluare de stil.

## Conservarea r02 și măsuri r03
r02-after-audit-v02: 1077 intrări verificate în trei arhive și recuperare la rece fără erori hash/cale/contract. Respingerile reale sunt păstrate. OBS-MANAGER-002 și rezultatele sale explică incidentul de ambalare, inclusiv prima citire prematură a unei comenzi încă în execuție; nu s-a suprascris arhiva.
F05/F06, F-RES-SOURCES-001 și META-RES-001-r02-F01 sunt propuse pentru retest, NU închise de producători. Auditorul GOV trebuie să prezinte propria corecție și matrice T01–T04; metaauditorul decide validitatea corecției. Canonul H-C9 rămâne de reconciliat la G01, chiar dacă omisiunea din raportul preliminar a fost remediată.
Următorul control: r03 înghețat, audituri independente, metaaudit, porți, arhive și recuperare efectivă. Toate constatările și încercările eșuate rămân vizibile.
