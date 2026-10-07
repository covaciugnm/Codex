---
name: kstar-baterie-theodor-palady
description: proiect baterii KSTAR pt Theodor Pallady 5 - structura foldere D:\00. Downloads\2026.09.22 - KStar Baterie Theodor Palady 5, oferta PI 19.150 EUR, contact Sebastian Babu
metadata:
  type: project
---

Proiect BESS KSTAR pentru amplasamentul str. Theodor Pallady nr. 5, ALBA IULIA (nu Bucuresti). Adresa de facturare difera: Neets Fotoshooting SRL, str. Stefan Luchian 3B, Alba Iulia. Acces limitat: livrarea trebuie facuta cu camioneta de max. 3,5 t, NU cu TIR/semiremorca. Dosar: `D:\00. Downloads\2026.09.22 - KStar Baterie Theodor Palady 5\`

Structura folderelor (stabilita de user la 22.09.2026):
- `1. Oferta` - oferte / proforme
- `5. Contract` - contracte
- `10. Documentatie Tehnica` - manuale, fise tehnice, ghiduri instalare
- `99. Inbox` - corespondenta NOUA, neintegrata inca; se goleste prin mutare in folderul potrivit

Contacte:
- Sebastian Babu - National Sales Manager KSTAR New Energy, Bucuresti, WhatsApp +40 765 078 172 (invitatie LinkedIn 21.05.2026 pe link_covaciu@yahoo.com)
- Andy Luo / "Andy Chen" - andy.luo@kstar.com, KSTAR Poland Sp. z o.o., Krakow (emite proformele)

Oferta curenta: PI KSTAR-PI-A20260915-01 din 15.09.2026, 19.150 EUR, DAP Alba Iulia, cumparator Neets Fotoshooting SRL (CUI 47362309). Sistem 50kW/102,4kWh All-in-One C&I BESS: KAC50DP2 Gen2 4x2MPPT + baterie 100,48 kWh LFP EVE 314Ah, racire AC, 2 dispozitive antiincendiu. Plata 100% T/T inainte de livrare, ridicare 14 zile dupa plata, garantie 5 ani produs / 10 ani performanta. Valabila pana la 30.09.2026.

De clarificat: PI-ul e emis DAP Alba Iulia pe Neets Fotoshooting (nu pe adresa Theodor Pallady), iar bateria din PI e BC100DE2A in timp ce manualele primite sunt pentru BC107DE2.

Date tehnice verificate din manualul BC107DE2 rev. B (01.07.2025), folder 10. Documentatie Tehnica:
- dulap 107,52 kWh, 384 Vcc (342-432 V), 120S1P, 140 A (0,5C), DoD recomandat 90%
- celula LFP 280 Ah / 3,2 V / 896 Wh; modul 17,92 kWh 20S1P, 64 V, 137 kg
- 1062 x 1371 x 2083 mm, ~1430 kg, IP54, 70 dB, -30…+50 C, umiditate 5-95%, altitudine 3000 m, A/C racire+incalzire
- comunicatie CAN/Ethernet/RS485/4G; spatiu 1200 mm fata, 1200 mm lateral PCS, 400 mm sus; transport la 40% SOC
- mentenanta: verificare lunara, curatare condensator A/C la 6 luni, calibrare SOC la 30 zile
- in cutia de accesorii: certificat de conformitate, raport de testare din fabrica, certificat de garantie

TREI neconcordante intre PI si documentatie (de lamurit inainte de comanda):
1. PI titlu 102,4 kWh vs PI articol 100,48 kWh
2. PI model BC100DE2A vs manuale BC107DE2 (107,52 kWh)
3. PI celule EVE 314 Ah vs manual celule 280 Ah
Manualul nu contine durata de viata (cicluri), randament round-trip si nicio fisa tehnica pentru PCS KAC50DP2 (primit doar quick install guide).

Ciorna trimisa in EVA Drafts catre Sebastian.b@kstar.com (22.09.2026) acopera aceste puncte + contract de furnizare, plata (propunere 30/70 in loc de 100% avans), DAP Bucuresti cu facturare Alba Iulia, certificate si SLA.

Alimentare si autonomie (din manual): dulapul NU e autonom - schimba energie cu exteriorul doar prin PCS (cap. 4.5) si are nevoie de alimentare auxiliara 220 V c.a. monofazat (L/N/PE, OVC II) pentru climatizare (3000 W racire / 2000 W incalzire) si modulul c.a./c.c. al HVB (cap. 3.5.1). Exista black start in c.c. prin butonul DC START tinut 3-6 s (cap. 4.3.2). Restrictii: incarcare interzisa sub 0 C; temp. optima celule 20-30 C; peste 45 C derating 10%/grad; fundatie beton ridicata ~300 mm, sol compactat 98%, 6 prezoane M14x50; PIF impune calibrare capacitate la 100% DoD (descarcare la 0% SOC, repaus 2 h, incarcare completa).
Cerinta proprie: tehnician KSTAR prezent pe santier la montaj SI la PIF.

Legat de [[firme-organizare]].
