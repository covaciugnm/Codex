from pathlib import Path
import json
P=Path(__file__).parent/'2026.09.30 statusuri verificate.json';s=json.loads(P.read_text(encoding='utf-8'))
def add(n,t,a,ids):s[n]={'status':t,'urmatorul_pas':a,'surse':ids}
add('Sedlak','2026.09.21: Michael Hollinger cere documentatia de licitatie pentru a evalua serviciile solicitate; fara pret ofertat.','Pregatirea/transmiterea documentatiei actuale si urmarirea raspunsului; nu este identificata o transmitere ulterioara in istoricul analizat.',['db83c626-bfe9-413a-9556-3b9ca3eaf0a7'])
add('KPPK','2026.08.11: refuz de ofertare pentru verificator, din lipsa de capacitate.','Inchidere ca refuz in runda curenta.',['b16e0900-8cb6-4b28-9c77-87cdddd56558'])
add('LVR','2026.06.01: solicita actualizare dupa discutia prin SMS si dupa oferta anterioara, pentru a-si planifica resursele.','Consemnarea deciziei privind continuarea colaborarii; oferta veche necesita reconfirmare.',['5a0a4649-9e01-40ea-88e9-3f171fd7ca02'])
add('Mattes Projektmanagement','2026.04.20: transmite documentatia vizitei din 2026.04.14 prin link valabil trei zile. La 2026.04.17 a trimis oferta de proiectare, licitatie si ÖBA.','Verificarea setului local al documentatiei si a eventualelor lipsuri; linkul temporar din aprilie nu este considerat descarcat prin simpla arhivare a emailului.',['35815f69-fd80-4e3c-b7d2-f90738a67702','b340c190-0ced-4288-b4b1-63195d1b2a9a'])
add('SMT Immobilien','2026.05.07: revine asupra ofertei de administrare trimise la 2026.03.03 si solicita feedback.','Pastrarea pentru comparatie; nicio acceptare identificata.',['edca7f98-ada7-4af7-8bb1-3d3e33f2dda2'])
add('Hofhans','2026.06.24: cere ca decontul final de apa si eventualul credit sa fie trimise fostei administratii, urmand decontarea cu noua administratie. Corespondenta juridica din septembrie include solicitarea beneficiarului de predare completa a dosarului.','Obtinerea situatiei de inchidere si a eventualelor credite transferate, precum si inventarul contractelor, facturilor si acceselor.',['539732dc-4010-42ad-a011-71f395b6f052','bbadf4d3-585d-4821-b316-4a958a293af3'])
s['OBENAUF']['status']+=' Exista lista de preturi orientative din 2026.09.16; adaosul de 20% este indicat pentru subcontractari. Aceasta nu reprezinta oferta globala ferma.'
P.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8');print(len(s))
