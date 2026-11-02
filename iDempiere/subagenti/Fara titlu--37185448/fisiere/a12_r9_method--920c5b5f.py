from a12_r9_publish import *
import shutil
r=R9;mdir=r/'metoda';mdir.mkdir(exist_ok=True)
my=['a12_r9_read.py','a12_r9_plan.py','a12_r9_orig.py','a12_r9_xlsx.py','a12_r9_t0409_jvm.py','a12_r9_t35_doc_check.py','a12_r9_cesiro_dict.py','a12_r9_git_controls.py','a12_r9_t204_retry.py','a12_r9_t314_final.py','a12_r9_checks.py','a12_r9_det.py','a12_r9_source882.py','a12_r9_alias.py','a12_r9_receipts.py','a12_r9_publish.py','a12_r9_qa.py','a12_r9_ui.py']
for f in my:shutil.copyfile(Path(os.environ['TEMP'])/f,mdir/f)
wr(mdir/'Manifest.json',{f:H(mdir/f)for f in my})
(r/'Metoda_reproducere.md').write_text('''# Audit P01 R9

Indexul permite căutarea după task, alias canonic, titlu sau stare. Toate cele 652 de fișe au câte un fișier JSON și o variantă HTML. Versiunea R8 este păstrată prin SHA în fiecare fișă. Criteriile fără probă suplimentară își păstrează starea de la ediția anterioară.

## Citirea rezultatelor

Registrul pornește cu 1.226 de criterii fără execuție. Cele 177 cărora li s-a atribuit o fixtură și cele 882 pentru care era necesară relectura au id-urile individuale păstrate. 218 subcazuri parțiale sunt o populație separată. Din cele 38 de dependențe parțial externe, două coincid cu poziții ale celor 177. Poziția JSON, documentul contabil, proba JVM și observația de interfață pot avea același criteriu și niveluri de dovadă diferite.

Pentru relectura completă a celor 882 folosiți fișierul de pregătire Relectura_882_pointeri.json și addendumul de aliasuri referit de raport. Sunt 858 poziții fizice și 68 înregistrări Git în care obiectul istoric diferă de obiectul căii la cutoff. Cele 4 subcondiții A06 au fost testate independent anterior de A11. Testele noi A12 urmăresc 5 alte criterii și își păstrează separat domeniul verificat. Detectorii Git au perechi de revizii explicite. Citirile AD sunt agregate și read-only. Rulările parserului și SQL-ului folosesc fixturi generate și nu efectuează operații în contabilitatea unei firme.

Fișierele originale de execuție au amprente în sursele R9. Registrul și catalogul se pot parcurge în ambele sensuri. Pentru reexecuție scripturile curente depind de funcțiile comune de citire și izolarea JVM din metoda păstrată în R8. Reexecutarea nu trebuie îndreptată către ediții deja sigilate. Previzualizarea tehnică folosește o destinație temporară distinctă. Un nou MANIFEST exterior leagă fără autoreferință raportul, QA, verificarea UX și dosarele, după ultima scriere. Nota de audit aparține A11.
''',encoding='utf8')
print(H(r/'Metoda_reproducere.md'),H(mdir/'Manifest.json'))

