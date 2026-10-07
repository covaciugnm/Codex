# Rezultate — Fișă proiect Ghidul-solicitantului

Răspunsuri și rezultate disponibile în istoricul local; fără limită de lungime aplicată de export.

## Asistent

[external_agent_tool_call: PowerShell]
description: Search for guide PDF and 1.5.1 folders
command: $paths = @("\\192.168.100.169\Comun","D:\00. Downloads","Z:\","$env:USERPROFILE\Downloads"); foreach($p in $paths){ if(Test-Path $p){ Get-ChildItem $p -Recurse -Depth 4 -Filter "*1.5.1*" -ErrorAction SilentlyContinue | Select-Object -First 20 FullName,LastWriteTime } }
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
FullName                                                                                                LastWriteTime  
--------                                                                                                -------------  
\\192.168.100.169\Comun\#recycle\00. Proiecte 2026\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf 05.10.2026 1...
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri          01.08.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Do... 01.08.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Do... 01.08.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Do... 01.08.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Do... 01.08.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe ... 10.12.2025 0...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe-... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Corrig... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Decizi... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Decizi... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\ERATA-... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Ghidul... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Inform... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Intreb... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Sintez... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe ... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe ... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe ... 03.12.2025 1...
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe ... 03.12.2025 1...
Z:\#recycle\00. Proiecte 2026\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf                      05.10.2026 1...
Z:\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri                               01.08.2025 1...
Z:\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Ane... 01.08.2025 1...
Z:\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Dec... 01.08.2025 1...
Z:\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Fis... 01.08.2025 1...
Z:\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Ghi... 01.08.2025 1...
Z:\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe Ghidul solicitantului... 10.12.2025 0...
Z:\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Anexe-Ghidul-solicitantului... 03.12.2025 1...
Z:\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Corrigendum-–-Interventia-1... 03.12.2025 1...
Z:\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Decizia-de-aprobare-a-Corri... 03.12.2025 1...
Z:\00. Proiecte\2025.12.10 Incubatoare de afaceri\1. Documente originale\Decizia-de-aprobare-a-Ghidu... 03.12.2025 1...
Z:\0...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: List project folders and recycle contents
command: $b="\\192.168.100.169\Comun"; Get-ChildItem "$b\00. Proiecte" | Select Name,LastWriteTime | ft -AutoSize | Out-String -Width 300; Test-Path "$b\00. Proiecte 2026"; Get-ChildItem "$b\#recycle\00. Proiecte 2026" | Select Name,Length,LastWriteTime | ft -AutoSize | Out-String -Width 300; foreach($f in "2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri","2025.12.10 Incubatoare de afaceri"){ "== $f"; Get-ChildItem "$b\00. Proiecte\$f" -Recurse | Select @{n='P';e={$_.FullName.Replace("$b\00. Proiecte\$f\","")}},Length,LastWriteTime | ft -AutoSize | Out-String -Width 400 }
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<persisted-output>
Output too large (150.1KB). Full output saved to: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\bkls1l9b1.txt

Preview (first 2KB):
Name                                                                                                                                               LastWriteTime      
----                                                                                                                                               -------------      
0. 2025.12 - FISE PROIECTE                                                                                                                         03.12.2025 10:24:00
0. Arhiva                                                                                                                                          05.12.2025 12:56:38
0. Licente ROSE                                                                                                                                    06.11.2025 17:23:49
0. Obtinere Licente ROSE                                                                                                                           05.12.2025 13:04:00
00 Centralizator Proiecte                                                                                                                          27.08.2025 16:23:02
00. Consultare - Acțiunii 2.1 – Dezvoltarea de noi serviciiaplicații                                                                               17.11.2025 10:39:32
00. Continua 2026.02.15 Interreg VI-A NEXT Ungaria-Slovacia-România-Ucraina                                                                        19.02.2026 12:36:17
00. Continua 2026.12.31 Granturi pentru industria prelucratoare                                                                                    05.08.2025 17:42:01
02.03.2026 Sprijin pentru înființarea întreprinderilor sociale în microregiunea Valea Jiului                                                       18.12.2025 17:35:56
...
</persisted-output>
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: List project folder names
command: $b="\\192.168.100.169\Comun"; Get-ChildItem "$b\00. Proiecte" -Directory | % Name; "---2026:"; Test-Path "$b\00. Proiecte 2026"; Get-ChildItem "$b\00. Proiecte 2026" -ErrorAction SilentlyContinue | % Name; "---recycle:"; Get-ChildItem "$b\#recycle\00. Proiecte 2026" | % {"$($_.Name) | $($_.Length) | $($_.LastWriteTime)"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
0. 2025.12 - FISE PROIECTE
0. Arhiva
0. Licente ROSE
0. Obtinere Licente ROSE
00 Centralizator Proiecte
00. Consultare - Acțiunii 2.1 – Dezvoltarea de noi serviciiaplicații
00. Continua 2026.02.15 Interreg VI-A NEXT Ungaria-Slovacia-România-Ucraina
00. Continua 2026.12.31 Granturi pentru industria prelucratoare
02.03.2026 Sprijin pentru înființarea întreprinderilor sociale în microregiunea Valea Jiului
1. DOTARI SCOLI
10.06.2025 DOC SELECTIE PARTENERI CIUGUD
2024.05.15 2.2 Întreprinderi digitale pentru o economie avansată – sectoarele de specializare inteligentă
2024.08.30 Parc Fotovoltaic - Depuse - Clarificari
2024.09.30 PoCIDIF Ghidul Solicitantului „Sprijin pentru întreprinderi nou înființate inovatoare”
2024.10.21 PIDS - CENTRE MULTIFUNCȚIONALE, CENTRE CU DOTĂRI SPORTIVE ȘI CULTURALE PENTRU COPII
2025 .07.14. ITI MOTII TARA DE PIATRA
2025. 08. 22 . Surse regenerabile de energie si stocarea energiei
2025.02.10  PEO Erasmus + Studenti
2025.02.27 AFM Arii Naturale Protejate
2025.02.27 Permacultură în orașe
2025.02.28 EENergy - Project
2025.02.28 NU Urban Mobility
2025.03.15 IMM Burse 1000 E Studenti (HORIZON-CL4-2021-HUMAN-01)
2025.04.01.16.00 PEO - PIDS  ROMI 2025
2025.04.21 EIT Manufacturing - Accelerate RED-Robot
2025.04.25 Promovarea energiei din surse regenerabile și reducerea emisiilor de gaze cu efect de seră
2025.04.29 Finantare Privind Drepturile Copilului si Participarea Copiilor Anexa 2
2025.04.31 PoIDS Programe formare îngrijitorilor informali
2025.05.07 Prevenire si Combaterea violentei Impotriva Copiilor
2025.05.13 Apel pentru proiecte care vizează conținutul TV și online - Apelul 2
2025.05.13 Apel pentru proiecte care vizează sprijinirea cooperării transnaționale și schimburilor între organizațiile active în domeniul cultural
2025.05.30     1.1.2.Dezvoltarea capacităților private de CDI
2025.06.17 DOC SELECTIE PARTENERI UAT STREMT
2025.06.20 DOC SELECTIE PARTENERI DAS ALBA
2025.06.23 ANUNT SELECTIE PARTENERI PRIVATI COMUNA BERGHIN
2025.06.24 DOC SEELCTIE PARTENERI PRIVATI TEIUS
2025.06.30 Centre respiro
2025.06.30 DOCUMENT SELECTIE PRIMARIA ABRUD
2025.06.30 Elvetia Cooperare
2025.07.24. EIC Pathfinder Challenges
2025.07.24. OMV PETROM
2025.07.31 Sprijinirea copiilor si tinerilor in procesul de dezinstitutionalizare
2025.08.01 BRD Proiect
2025.08.01 WE CARE TOGHETER EDITIA 2025
2025.08.04 WOMEN TechEU
2025.08.22 Energie Verde pt Autoconsum
2025.08.29 CDI Sanatate STEP_scheme_de_ajutor_consultare
2025.09.02 Alex Petrutiu SES
2025.09.02 European Innovation Council
2025.09.05 Serv ingrijire la domiciliu pers varstnice
2025.09.11. Puscau Bogdan Sebastian SES
2025.09.30  O șansă în plus prin învățământul profesional și tehnic
2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri
2025.10.23. Promovarea egalitatii si combaterea rasismului, xenofobiei si a tuturor celorlate forme de discriminare
2025.10.30 Apel pentru solutii inovatoare privind imbunatatirea intergarii pers cu dizab pe piata muncii
2025.11.01 DR16 AFIR Sere Rosii
2025.11.13 Apel pentru misiuni de colaborare in vederea reducerii dauenlor asupra mediului legate de sistemul alimentar
2025.11.14 ONG 15k Euro
2025.11.15 ONG
2025.11.25 Servicii Ingrijire Batrani ITI
2025.11.27 Programul Rabla 2025
2025.11.30 Tranzitie Justa 300.000
2025.12.05 Stimularea cererii întreprinderilor pentru inovare
2025.12.10 EIC STEP
2025.12.10 Incubatoare de afaceri
2025.12.10 Start ONG
2025.12.17 Apelul 2 - Granturi pentru proiecte cu accent pe implicare civică
2026.02.17 Innovative robotic automated onstruction
2026.02.28 TJ IMM Mures
2026.05.30 CONȘTIENT ȘI LIBER
2026.06.30 2.2 Digitalizare
2026.07.17 1.3.3 Platforma pilot de inovare deschisa
2026.12.31 Schema de ajutor de stat dedicata industriei prelucratoare
2028.06.30. Sprijin pt operatiunile selectate de GAL pt mediul rrual
2028.12.29 1.3.1 CDI
AFIR arhiva
AFIR DR-16 - INVESTIȚII ÎN SECTORUL LEGUME ȘISAU CARTOFI
AFIR Fotovoltaic 2
AFM IM...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Inspect sibling project folder structures
command: $b="\\192.168.100.169\Comun\00. Proiecte 2026"; foreach($f in "2026.10.20 - Administrator parc UAT IMM INDIRECT 1.5.2 Parcuri industriale în domenii RIS","2026.11.06 - clustere inm membre - P1-1.2.2 - CLUSTERE INOVATIVE","2026.10.01 Actualizare finantari Romania"){ "== $f"; Get-ChildItem "$b\$f" -Recurse | % { $_.FullName.Replace("$b\$f\","") + " | " + $_.Length + " | " + $_.LastWriteTime } }; Get-ChildItem "$b" -Recurse -Include *1.5.1*,*incubat*,*acceler* | % FullName; Get-Item "$b\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf" | % {"$($_.Length) $($_.LastWriteTime)"}
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
== 2026.10.20 - Administrator parc UAT IMM INDIRECT 1.5.2 Parcuri industriale în domenii RIS
0.ARHIVA | 1 | 06/25/2026 14:33:56
1. DOCUMENTE OFICIALE | 1 | 06/25/2026 14:34:20
CONDIȚII DE ELIGIBILITATE.docx | 24443 | 06/26/2026 14:02:47
1. DOCUMENTE OFICIALE\ANEXE | 1 | 06/25/2026 14:35:11
1. DOCUMENTE OFICIALE\Ghidul-solicitantului-Interventia-1.5.2-.pdf | 1877650 | 06/25/2026 14:33:38
1. DOCUMENTE OFICIALE\ANEXE\Anexa 1- Instrucțiuni de completare CF-1.5.2.docx | 7076007 | 06/25/2026 14:35:09
1. DOCUMENTE OFICIALE\ANEXE\Anexa 10- Notă privind fundamentarea costurilor.docx | 900733 | 06/25/2026 14:35:04
1. DOCUMENTE OFICIALE\ANEXE\Anexa 11- Lista de echipamente dotări lucrări servicii.docx | 902014 | 06/25/2026 14:35:05
1. DOCUMENTE OFICIALE\ANEXE\Anexa 12- Tabel centralizator numere cadastrale.docx | 902222 | 06/25/2026 14:35:05
1. DOCUMENTE OFICIALE\ANEXE\Anexa 13- Planul de dezvoltare parcuri industriale-.docx | 937091 | 06/25/2026 14:35:05
1. DOCUMENTE OFICIALE\ANEXE\Anexa 14- Macheta  financiară_152_Parcuri_Industriale.xlsx | 145249 | 06/25/2026 14:35:06
1. DOCUMENTE OFICIALE\ANEXE\Anexa 14.1 - Checklist verificare a analizei financiare.docx | 923227 | 06/25/2026 14:35:06
1. DOCUMENTE OFICIALE\ANEXE\Anexa 15- Planul de monitorizare.docx | 842459 | 06/25/2026 14:35:07
1. DOCUMENTE OFICIALE\ANEXE\Anexa 16-  Contract de finanțare - condiții generale și specifice.docx | 983801 | 06/25/2026 14:35:07
1. DOCUMENTE OFICIALE\ANEXE\Anexa 2- Declarația unică.docx | 920217 | 06/25/2026 14:35:09
1. DOCUMENTE OFICIALE\ANEXE\Anexa 3- Grila evaluare tehnică și financiară.docx | 858748 | 06/25/2026 14:35:09
1. DOCUMENTE OFICIALE\ANEXE\Anexa 4- Grila de verificare eligibilitate și contractare.docx | 865404 | 06/25/2026 14:35:10
1. DOCUMENTE OFICIALE\ANEXE\Anexa 5- Model orientativ Hotărâre de aprobare a proiectului.docx | 902684 | 06/25/2026 14:35:10
1. DOCUMENTE OFICIALE\ANEXE\Anexa 6- Acord de parteneriat (model orientativ).docx | 913931 | 06/25/2026 14:35:11
1. DOCUMENTE OFICIALE\ANEXE\Anexa 7- Declarație privind eligibilitatea TVA.docx | 912995 | 06/25/2026 14:35:11
1. DOCUMENTE OFICIALE\ANEXE\Anexa 8- Declarație privind conformitatea documentelor din MySMIS.docx | 900040 | 06/25/2026 14:35:03
1. DOCUMENTE OFICIALE\ANEXE\Anexa 9- Declarație privind ajutoarele de stat și minimis primite.docx | 914699 | 06/25/2026 14:35:04
== 2026.11.06 - clustere inm membre - P1-1.2.2 - CLUSTERE INOVATIVE
0.ARHIVA | 1 | 06/25/2026 14:17:55
1.DOCUMENTE OFICIALE | 1 | 06/25/2026 14:19:24
CONDIȚII DE ELIGIBILITATE.docx | 24455 | 06/26/2026 14:39:12
1.DOCUMENTE OFICIALE\ANEXE | 1 | 06/25/2026 14:19:34
1.DOCUMENTE OFICIALE\Decizie-nr.-148.pdf | 1664438 | 06/25/2026 14:10:13
1.DOCUMENTE OFICIALE\Ghidul-solicitantului-Corrigendum-1-Interventia-1.2.1.pdf | 2095096 | 06/25/2026 14:09:39
1.DOCUMENTE OFICIALE\ANEXE\Anexa 1 - Instructiuni de completare  CF 121.docx | 6808140 | 06/25/2026 14:19:27
1.DOCUMENTE OFICIALE\ANEXE\Anexa 10 - Declarație privind ajutoarele de stat și minimis primite- 121.docx | 915093 | 06/25/2026 14:19:32
1.DOCUMENTE OFICIALE\ANEXE\Anexa 11 - Model hotărâre AGA.docx | 909766 | 06/25/2026 14:19:33
1.DOCUMENTE OFICIALE\ANEXE\Anexa 12 - Planul de monitorizare.docx | 838748 | 06/25/2026 14:19:33
1.DOCUMENTE OFICIALE\ANEXE\Anexa 13- Contract de finantare_conditii generale si specifice-121.docx | 970400 | 06/25/2026 14:19:33
1.DOCUMENTE OFICIALE\ANEXE\Anexa 14-Calendarul implementării proiectului.docx | 905527 | 06/25/2026 14:19:34
1.DOCUMENTE OFICIALE\ANEXE\Anexa 2 - Declaratie Unica.docx | 918798 | 06/25/2026 14:19:28
1.DOCUMENTE OFICIALE\ANEXE\Anexa 3 - Grila ETF-121_v1.docx | 850027 | 06/25/2026 14:19:28
1.DOCUMENTE OFICIALE\ANEXE\Anexa 4- Grila verificare eligibilitate contractare.docx | 708555 | 06/25/2026 14:19:29
1.DOCUMENTE OFICIALE\ANEXE\Anexa 5- Plan de implementare.docx | 916681 | 06/25/2026 14:19:29
1.DOCUMENTE OFICIALE\ANEXE\Anexa 6- Macheta financiară1.2.1.xlsx | 136978 | 06/25/2026 14:19...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Copy files to scratchpad and list old folders
command: $b="\\192.168.100.169\Comun\00. Proiecte 2026"; $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; Copy-Item "$b\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf" "$s\ghid151.pdf"; Copy-Item "$b\2026.10.20 - Administrator parc UAT IMM INDIRECT 1.5.2 Parcuri industriale în domenii RIS\CONDIȚII DE ELIGIBILITATE.docx" "$s\cond152.docx"; Get-ChildItem "\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri" -Recurse | % FullName; Get-ChildItem "\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri" -Recurse | ? {$_.FullName -notmatch 'Documente originale'} | % FullName; Get-ChildItem "\\192.168.100.169\Comun\00. Proiecte\0. 2025.12 - FISE PROIECTE" | % Name
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<persisted-output>
Output too large (72.4KB). Full output saved to: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\brln9ai3g.txt

Preview (first 2KB):
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Anexe-Ghidul-solicitantului-Interventia-1.5.1.zip
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Centralizator-intrebari-si-raspunsuri-1.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Centralizator-intrebari-si-raspunsuri.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Codul MySMIS al apelului.docx
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Decizia-de-aprobare-a-Ghidului-solicitantului-Interventia-1.5.1.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Fisa-de-prezentare-ghid-consultare-publica-RO_1.5.1.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Ghidul-solicitantului-Interventia-1.5.1.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale\Intrebari-frecvente.pdf
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Arhiva
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P2
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Bo Pintea Resume 2025 Alba Vision.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Descriere Deviz General CF HG907-2016.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Deviz General Conform HG907.docx
...
</persisted-output>
[/external_agent_tool_result]

## Asistent

Am găsit ghidul în `00. Proiecte 2026` (fără folder dedicat) și două foldere vechi pentru Apelul 1 în `00. Proiecte`. Acum citesc ghidul și fișele existente.

## Asistent

[external_agent_tool_call: PowerShell]
description: Extract guide text and read template fisa
command: $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; Get-Content "C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\brln9ai3g.txt" | Select-String -NotMatch "Documente originale\\|\\Arhiva\\" | Select -First 80; cd $s; pdftotext -layout ghid151.pdf ghid151.txt; (Get-Content ghid151.txt).Count; python -c "import docx;d=docx.Document('cond152.docx');[print(p.text) for p in d.paragraphs];[print(' | '.join(c.text for c in r.cells)) for t in d.tables for r in t.rows]"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri\1. Documente Originale
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Arhiva
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P2
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Bo Pintea Resume 2025 Alba Vision.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Descriere Deviz General CF HG907-2016.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Deviz General Conform HG907.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Incubator Afaceri IT â€“ Tabel de Ofertare Valor
icÄƒ (conform HG 907-2016).docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Lista de materiale È™i echipamente pentru modern
izarea halei IT.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Lista echipamente È™i materiale pentru moderniza
rea halei C4 Ã®n incubator IT â€“ conformitate 100% cu normele.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Normativele legislative RO Ã®ntocmirea PT+DTE+De
viz.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\Raport de Conformitate pentru Modernizarea Halei
 C4 Ã®n Incubator IT.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.2 Documente Obligatorii de Incarcat in MySm
is
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\3. Clarificare nr.1
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\4. Clarificare nr.2
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis.zip
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.2 Documente Obligatorii de Incarcat in MySm
is.zip
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\3. Clarificare nr.1.zip
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\4. Clarificare nr.2.zip
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\BVC Incubator.xlsx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\Deviz-general-model-excel-conform-HG-907.xlsx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\DocumentaÈ›ie Proiect Incubator de Afaceri IT
.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\Plan Tehnic È™i Financiar C4 V2.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\0.Cerere fi
nantare V1 MODEL DE URMAT!!!.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\1. Capacita
te Solicitant.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\1.1 CV-mana
ger de proiect.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\1.1 Documen
te Incarcare in MySmis.zip
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\10. Metodol
ogie de implementare proiect.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\10.1 Maturi
tate Proiect.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\10.2 Descri
erea Investitiei.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri\P1\1.1 Documente Incarcare in MySmis\11. Calenda
r Proiect.docx
\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de aface...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\ghid151.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
1	                 Programul Regiunea Centru
2	
3	       PRIORITATEA 1:
4	
5	 O REGIUNE COMPETITIV PRIN INOVARE I �NTREPRINDERI
6	         DINAMICE PENTRU O ECONOMIE INTELIGENT
7	
8	OS 1.3. Intensificarea creterii durabile i a competitivitii IMM-urilor i crearea de locuri de
9	                                                    munc �n
10	
11	                         cadrul IMM-urilor, inclusiv prin investiii productive
12	           OS 1.4 Dezvoltarea competenelor pentru specializare inteligent, tranziie
13	
14	                                        industrial i antreprenoriat
15	                        Aciunea 2: Structuri de sprijin pentru dezvoltare IMM
16	                 Intervenia 1.5.1: Incubatoare si acceleratoare de afaceri- APEL 2
17	
18	                                                       Agenia pentru Dezvoltare Regional Centru
19	                                                       Autoritate de Management Programul Regiunea Centru
20	                                                       www.adrcentru.ro I E-mail: office@adrcentru.ro
21	                                                              Tel.: 0258-818616, Fax: 0258 � 818613, Str. Decebal, 11, 510093, Alba Iulia
22	        Cuprins
23	
24	1. PREAMBUL, ABREVIERI I GLOSAR ..................................................................................... 5
25	  1.1. Preambul................................. ............................................................................................ 5
26	  1.2. Abrevieri............... ............................................................................................................... 5
27	  1.3. Glosar.................. ................................................................................................................ 6
28	
29	2. ELEMENTE DE CONTEXT................................................................................................... 15
30	  2.1. Informaii generale Program ............................................................................................. 15
31	  2.2. Prioritatea/Fond/Obiectiv de politic/Obiectiv specific ................................................... 15
32	  2.3. Reglementri europene i naionale, cadrul strategic, documente programatice
33	  aplicabile.................................................................................................................................. 18
34	
35	3. ASPECTE SPECIFICE APELULUI DE PROIECTE...................................................................... 18
36	  3.1. Tipul de apel ...................................................................................................................... 18
37	  3.2. Forma de sprijin (granturi; instrumentele financiare; premii) .......................................... 18
38	  3.3. Bugetul alocat apelului de proiecte .................................................................................. 18
39	  3.4. Rata de cofinanare ........................................................................................................... 19
40	  3.5. Zona/zonele geografic(e) vizat(e) de apelul de proiecte............................................... 21 2
41	  3.6. Aciuni sprijinite �n cadrul apelului.................................................................................... 21
42	  3.7. Grup int vizat de apelul de proiecte............................................................................... 22
43	  3.8. Indicatori............... ............................................................................................................ 22
44	  3.9. Rezultatele ateptate ........................................................................................................ 27
45	  3.10.Operaiune de importan strategic ............................................................................... 27
46	  3.11.Investiii teritoriale integrate ....................................................................................
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Re-extract guide text in UTF-8
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && pdftotext -enc UTF-8 ghid151.pdf g.txt && grep -v "ADR Centru - Autoritate de Management" g.txt | grep -v '^\s*$' > g2.txt && wc -l g2.txt && grep -n "3.1. Tipul de apel\|4.1. Data\|5.1. Eligibilitatea\|5.4. Valoarea\|7.4. Anexe\|8.4. Evaluarea\|14.ANEXE\|14. ANEXE" g2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
1724 g2.txt
11:3. ASPECTE SPECIFICE APELULUI DE PROIECTE...................................................................... 18 3.1. Tipul de apel ...................................................................................................................... 18 3.2. Forma de sprijin (granturi; instrumentele financiare; premii) .......................................... 18 3.3. Bugetul alocat apelului de proiecte .................................................................................. 18 3.4. Rata de cofinanțare ........................................................................................................... 19 3.5. Zona/zonele geografică(e) vizată(e) de apelul de proiecte............................................... 21 2 3.6. Acțiuni sprijinite în cadrul apelului.................................................................................... 21 3.7. Grup țintă vizat de apelul de proiecte............................................................................... 22 3.8. Indicatori............... ............................................................................................................ 22 3.9. Rezultatele așteptate ........................................................................................................ 27 3.10.Operațiune de importanță strategică ............................................................................... 27 3.11.Investiții teritoriale integrate ............................................................................................ 27 3.12.Dezvoltare locală plasată sub responsabilitatea comunității ........................................... 27 3.13.Reguli privind ajutorul de stat........................................................................................... 27 3.14.Reguli privind instrumentele financiare............................................................................ 38 3.15.Acțiuni interregionale, transfrontaliere și transnaționale ................................................ 38 3.16.Principii orizontale............................................................................................................. 38 3.17.Aspecte de mediu (inclusiv aplicarea Directivei 2011/92/UE a Parlamentului European și a Consiliului). Aplicarea principiului DNSH. Imunizarea la schimbările climatice ..................... 38 3.18.Caracterul durabil al proiectului ....................................................................................... 39 3.19.Acțiuni menite să garanteze egalitatea de șanse, de gen, incluziunea și nediscriminare..........................................................................................................................39 3.20.Teme secundare ............................................................................................................... 40
14:4.1. Data deschiderii apelului de proiecte....................................................................42
19:5.1. Eligibilitatea solicitanților și partenerilor .......................................................................... 43
22:5.4. Valoarea minimă și maximă eligibilă/nerambursabilă a unui proiect .............................. 71
32:7.4. Anexe și documente obligatorii la depunerea cererii ....................................................... 82
40:8.4. Evaluarea tehnică și financiară. Criterii de evaluare tehnică și financiară........................ 93
52:14.ANEXE........................................................................................................................... 111
231:3.1. Tipul de apel
776:4.1. Data deschiderii apelului de proiecte
794:5.1. Eligibilitatea solicitanților și partenerilor
1298:5.4. Valoarea minimă și maximă eligibilă/nerambursabilă a unui proiect
1458:7.4. Anexe și documente obligatorii la depunerea cererii
1574:8.4. Evaluarea tehnică și financiară. Criterii de evaluare tehnică și financiară
1721:14. ANEXE
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\g2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
File content (35187 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\g2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
File content (78747 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\g2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
231	3.1. Tipul de apel
232	18
233	Apelul de proiecte este de tip competitiv, cu termen limită de depunere a cererilor de finanțare.
234	Astfel, proiectele pot fi depuse doar în perioada menționată în cadrul subsecțiunii 4.3 a prezentului document, în limita fondurilor disponibile acestui apel de proiecte.
235	Pot intra în etapa de contractare proiectele care se încadrează în alocarea financiară, care în urma evaluării tehnice și financiare au obținut un punctaj de minim 70 de puncte și care nu au fost notate cu 0 la criteriile menționate în grila ETF (conform instrucțiunilor de completare).
236	3.2. Forma de sprijin (granturi; instrumentele financiare; premii)
237	Prin prezentul apel de proiecte, sprijinul se va acorda sub formă de grant.
238	3.3. Bugetul alocat apelului de proiecte
239	Alocarea financiară corespunzătoare acestui apel este de 9.201.232 euro, din care sprijin FEDR 7.821.047 euro și 1.380.185 euro finanțare de la bugetul de stat.
240	Cursul valutar la care se va calcula încadrarea în alocarea financiara a apelului de proiecte este cursul inforeuro valabil în luna publicării apelului de proiecte luna august 2026 respectiv 1 euro= 5.2434lei.
241	In cadrul prezentului apel de proiecte, există posibilitatea supracontractării conform OUG nr. 133/2021 – art. 15, alin. 1, lit. b) si art. 5, alin 2 al HG nr. 829/2022, în funcție de disponibilitatea fondurilor, pe baza instrucțiunilor emise de AM PR Centru.
242	3.4. Rata de cofinanțare
243	În cadrul prezentului apel activitățile eligibile și cheltuielile aferente acestora pot fi finanțate prin ajutor de stat regional și ajutor de minimis, conform prevederilor schemei de ajutor de stat aplicabilă.
244	Detalii privind rata de cofinanțare, în funcție de tipul de ajutor aplicabil:
245	Pentru proiectele depuse în cadrul prezentului apel, cuantumul cofinanțării acordate solicitantului în limita intensității ajutorului de stat regional, stabilite în funcție de locul de implementare a proiectului (județul în care se implementează proiectul), precum și de tipul solicitantului (încadrarea în categoria microîntreprinderilor, întreprinderilor mici sau mijlocii, întreprinderi mari), este conform tabelului de mai jos:
246	a) Ajutorul de stat regional
247	Contribuția maximă a programului la cheltuielile eligibile finanțabile prin ajutor regional
248	19 Tip
249	Intensitatea maximă a ajutorului de stat (%)
250	Alba Brașov
251	Covasna
252	Harghita
253	Mureș
254	Sibiu
255	Întreprindere
256	Micro / Mică 70
257	60
258	60
259	60
260	70
261	60
262	Mijlocie
263	60
264	50
265	50
266	50
267	60
268	50
269	Întreprinderi 50
270	40
271	40
272	40
273	50
274	40
275	mari
276	În cazul în care proiectul conține atât investiții inițiale finanțabile prin ajutor de stat regional, cât și investiții finanțabile prin ajutor de minimis, procentele de mai sus se aplică numai la valoarea cheltuielilor eligibile finanțabile prin ajutor de stat regional.
277	În cazul proiectelor depuse în parteneriat, rata de co-finanțare mai sus-menționată se aplică solicitantului individual /liderului de parteneriat. Ajutorul de stat regional se acordă doar solicitantului individual/liderului de parteneriat care face dovada deținerii dreptului real solicitat asupra imobilului ce face obiectul investiției, conform prevederilor prezentului ghid.
278	Pentru toate tipurile de solicitanți eligibili în cadrul acestui apel, încadrarea in categoria de întreprindere se va realiza având în vedere prevederile Legii nr. 346/2004 privind stimularea înființării și dezvoltării IMM-urilor, Recomandarea CE nr. 361/2003 privind definiția IMM-urilor, Manualului utilizatorului pentru definiția IMM-urilor (Comisia Europeană, 2015), Jurisprudența Curții Europene de Justiție în ceea ce privește definiția IMM-urilor, conform Recomandării CE nr. 361/2003. În cadrul acestui apel, la stabilirea încadrării în categoria întreprinderilor se va avea în vedere orice entitate care desfășoară o activitate economică, indiferent de forma sa juridică, de
279	mod...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\g2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
740	Respectarea principiilor orizontale menționate la nivelul Acordului de Parteneriat și Programului Regiunea Centru se va realiza pe toată perioada de elaborare, implementare și durabilitate a proiectelor. Proiectele care includ măsuri suplimentare cadrului legal in vigoare, vor fi punctate în grila de evaluare tehnică și financiară.
741	Pentru stabilirea abordării optime a respectării acestor principii, se vor avea în vedere, fără a se limita la, actele normative naționale și comunitare prevăzute în Lista cuprinzând legislația orientativă aplicabilă, disponibilă pe site-ul https://www.regiocentru.ro/documente-utile/
742	3.17. Aspecte de mediu (inclusiv aplicarea Directivei 2011/92/UE a Parlamentului European și a Consiliului). Aplicarea principiului DNSH. Imunizarea la schimbările climatice
743	Proiectele finanțate vor avea în vedere, pe toată perioada de implementare a proiectului, 38 respectarea obligațiilor prevăzute în PR Centru pentru implementarea principiului „Do No Significant Harm” (DNSH) așa cum acesta este definit prin Regulamentul (UE) 852/2020 privind instituirea unui cadru care să faciliteze investițiile durabile. In acest sens, solicitantul va descrie la secțiunea relevantă din cererea de finanțare si anexele sale, modul în care sunt respectate obligațiile minime prevăzute de legislația specifică aplicabilă, acțiunile suplimentare propuse (dacă este cazul), precum și modul de respectare a principiilor DNSH in implementarea proiectelor. Pentru analiza modului în care principiul DNSH este respectat, solicitantul de finanțare va avea în vedere metodologia disponibilă la adresa https://www.regiocentru.ro/documente-utile/ privind abordarea principiului DNSH în Programul Regiunea Centru. Solicitantul va avea în vedere respectarea principiului DNSH inclusiv la întocmirea documentațiilor de atribuire a contractelor de achiziție. Totodată, în faza de evaluare se va verifica dacă proiectele propuse respecta principiul DNSH prin parcurgerea și completarea unei liste de verificare DNSH (conform modelului prezentat în Metodologie). Imunizarea infrastructurii finanțate la schimbări climatice, respectiv adaptarea la schimbările climatice și atenuarea efectelor nocive asupra mediului și rezistența în fața dezastrelor, va fi avută în vedere atât în etapa de elaborare, cât și pe durata implementării proiectelor, precum și în etapa de exploatare și întreținere a investițiilor, asigurându-se astfel durabilitatea infrastructurii și standardul serviciilor cu abordarea adecvată a riscurilor climatice. Pe durata exploatării, infrastructura creată va fi eficient monitorizată si din perspectiva evenimentelor
744	climatice. In acest sens, proiectul integrează măsuri de atenuare și de adaptare la schimbările
745	climatice respectând Orientările Comisiei Europene privind imunizarea la schimbările climatice.
746	De asemenea, solicitantul va avea în vedere, în mod special: Raportul de mediu pentru PR Centru 2021-2027 si Analiza privind evaluarea principiului DNSH în PR CENTRU 20212027: https://www.regiocentru.ro/programul-regiunea-centru-2021-2027/.
747	3.18. Caracterul durabil al proiectului
748	Obiectivele de mediu și climă reprezintă obiective transversale care definesc strategia și intervențiile PR Centru, urmărind sustenabilitatea ecologică, respectiv considerentele legate de mediu definite la nivel european. Se vor încuraja proiecte care susțin dezvoltarea durabila si care aleg opțiunile de implementare care contribuie la îmbunătățirea performanței de mediu, la dezvoltarea unei economii moderne durabile, competitive și eficientă din punct de vedere al utilizării resurselor
749	3.19. Acțiuni menite să garanteze egalitatea de șanse, de gen, incluziunea și nediscriminarea
750	În implementarea PR Centru, precum si in etapele de elaborare si implementare a proiectelor, se va asigura respectarea drepturilor fundamentale și conformitatea cu Carta Drepturilor Fundamentale a UE, a Convenției Națiunilor Unite privind Drepturile Persoanelor...
[/external_agent_tool_result]

## Asistent

Citesc ghidul (Apel 2: depunere 21.10–21.12.2026). Continui cu activități, valori, anexe și grila de evaluare.

## Asistent

[external_agent_tool_call: Bash]
description: Read partnerships and activities section
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '940,1060p' g2.txt | cut -c1-1500
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
2. Parteneriate între maxim 2 entitățile menționate la litera A și administratorului incubatorului de afaceri .
Indiferent de forma de organizare a solicitantului (entitate individuală sau parteneriat), acesta este considerat întreprindere și, în conformitate cu prevederile Legii 346/2004, se încadrează într-una din categoriile microîntreprindere, întreprindere mică, mijlocie sau mare.
Categoria microîntreprinderilor și a întreprinderilor mici și mijlocii („IMM-uri”) este formată din întreprinderi care au mai puțin de 250 de angajați și a căror cifră de afaceri anuală nu depășește 50 de milioane EUR și/sau ale căror active totale nu depășesc 43 de milioane EUR, echivalent în lei
✓ în cadrul categoriei IMM-urilor, o întreprindere mijlocie are între 50 și 250 de salariați şi realizează o cifră de afaceri anuală netă de până la 50 milioane euro, echivalent în lei sau dețin active totale care nu depășesc echivalentul în lei a 43 milioane euro, echivalent în lei ✓ în cadrul categoriei IMM-urilor, o întreprindere mică are între 10 și 49 de salariați şi realizează o cifră de afaceri anuală netă sau dețin active totale de până la 10 milioane euro, echivalent în lei ✓ în cadrul categoriei IMM-urilor, o microîntreprindere are până la 9 salariaţi şi realizează o cifră de afaceri anuală netă sau deţin active totale de până la 2 milioane euro, echivalent,
echivalent în lei;.
Se recomandă o atenţie sporită în aplicarea corectă a prevederilor Legii 346/2004, cu modificările și completările ulterioare, în special în ceea ce priveşte identificarea întreprinderilor partenere și/sau legate cu întreprinderea solicitantă. Încadrarea datelor solicitantului (a numărului mediu anual de salariaţi şi a cifrei de afaceri anuale nete/ activelor totale) în pragurile prevăzute pentru categoria IMM-urilor se verifică abia după luarea în calcul a datelor aferente tuturor întreprinderilor partenere şi ale celor legate cu întreprinderea solicitantă, identificate conform legii.
Solicitantul IMM va completa şi Anexa 8 - Declarație privind încadrarea întreprinderii în categoria IMM (din care să reiasă încadrarea în categoria microîntreprinderilor/ întreprinderilor mici/ întreprinderilor mijlocii). Datele utilizate pentru calculul numărului mediu anual de salariați, cifra de afaceri netă anuală şi activele totale sunt cele raportate în situațiile financiare aferente exercițiului financiar precedent depunerii cererii de finanțare, aprobate de adunarea generală a acționarilor sau asociaților (conform Art. 6 alin (1) din Legea 346/2004). Această prevedere se aplică inclusiv în cazul cererilor de finanțare depuse în primele luni ale anului4, chiar dacă situațiile financiare aprobate de adunarea generală a acționarilor sau asociaților nu au fost încă depuse la unitățile teritoriale ale Ministerului Finanțelor Publice.
ATENTIE! Valoarea finanțării nerambursabile solicitate la data depunerii cererii de finanțare nu poate fi modificată în sensul creșterii acesteia în cazul în care intervin modificări pe parcursul procesului de evaluare, selecție și contractare raportat la încadrarea în diferitele categorii de întreprinderi. Cu toate acestea, valoarea finanțării nerambursabile va fi redusă în conformitate cu modificarea încadrării în categoria de întreprinderi pe parcursul procesului de evaluare, selecție și contractare în sensul respectării încadrării în limitele maxime acceptabile conform 53 prevederilor legate de ajutorul de stat. A se vedea cap. 3.4 din prezentul ghid. În sensul acestui apel, ”întreprinderea din mediul urban/rural” se referă la întreprinderea care propune o investiție (crearea/extinderea unui incubator de afaceri) în mediul urban/rural, indiferent de localizarea sediului social al acesteia. Sucursalele, agențiile, reprezentanțele sau alte unităţi fără personalitate juridică nu sunt eligibile.
5.1.3. Categorii de parteneri eligibili
În cazul în care solicitantul este un parteneriat, parteneriatul este format astfel: 1. Parteneriatele dintre fondator...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Read values, duration, keyword hits
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '1061,1080p;1290,1340p' g2.txt | cut -c1-1500; echo ======; grep -n -i "sectoare de excelen\|RIS3 Centru\|domenii de specializare\|CAEN.*neeligib\|30.06.2028\|31.12.2029\|minimum 70\|100 de puncte\|criteriu.*eliminator" g2.txt | cut -c1-300 | head -40
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
comerciale sau de alimentatie publica, bazelor sportive, bazelor de agrement, spațiilor
spa&wellness .
e) Nu sunt eligibile proiectele care includ exclusiv incubatoare virtuale (portal sau incubator
fără pereți – „without walls”).
f) Nu sunt eligibile proiectele care includ investiții demarate.
De asemenea, nu fac obiectul finanțării acestui apel domeniile enumerate la art. 7 din Regulamentul 2021/1058 al Parlamentului European și al Consiliului din 24 iunie 2021 privind Fondul european de dezvoltare regională și Fondul de coeziune.
5.3. Eligibilitatea cheltuielilor
5.3.1. Baza legală pentru stabilirea eligibilității cheltuielilor • Regulamentul (UE, EURATOM) nr. 2020/2093 al Consiliului din 17 decembrie 2020 de stabilire a cadrului financiar multianual pentru perioada 2021 – 2027
• Regulamentul al Parlamentului European și al Consiliului nr. 1060/2021 de
stabilire a dispozițiilor comune privind Fondul european de dezvoltare regională,
Fondul social european Plus, Fondul de coeziune, Fondul pentru o tranziție justă
și Fondul european pentru afaceri maritime, pescuit și acvacultură și de stabilire
a normelor financiare aplicabile acestor fonduri, precum și Fondului pentru azil,
migrațiune și integrare, Fondului pentru securitate internă și Instrumentului de sprijin
financiar pentru managementul frontierelor și politica de vize, cu modificările și
completările ulterioare
• Regulamentul UE 1058/2021 al Parlamentului European și al Consiliului din 24 iunie 2021
privind Fondul european de dezvoltare regională și Fondul de coeziune, cu modificările și
completările ulterioare
• Regulamentul (UE) 2021/1237 al Comisiei din 23 iulie 2021 de modificare a
• cheltuieli efectuate peste plafoanele stabilite prin prezentul ghid
• cheltuieli cu achiziționarea de bunuri care, conform legii, intră în categoria obiectelor de
inventar. Reprezintă active corporale de natura obiectelor de inventar activele corporale a
căror valoare fiscala, la data intrării in patrimoniul beneficiarului, este mai mica decât plafonul
valoric prevăzut de Codul fiscal, actualizat prin Hotărâre a Guvernului)
5.3.4. Opțiuni de costuri simplificate. Costuri directe și costuri indirecte Nu este cazul.
5.3.5. Opțiuni de costuri simplificate. Costuri unitare/sume forfetare și rate forfetare Nu este cazul
5.3.6. Finanțare nelegată de costuri Nu este cazul.
5.4. Valoarea minimă și maximă eligibilă/nerambursabilă a unui proiect
• Valoarea minimă eligibilă a finanțării nerambursabile solicitate: 100.000 euro • Valoarea maximă eligibilă a finanțării nerambursabile solicitate: 2.000.000 euro
Aceste valori cuprind atât finanțarea acordată sub formă de ajutor de stat regional, cât și finanțarea acordată sub formă de ajutor de minimis.
Finanțarea nerambursabilă maximă acordată sub formă de ajutor de minimis în cadrul prezentei scheme nu poate depăși echivalentul în lei a sumei de 300.000 euro/proiect, calculat la cursul InforEuro valabil la data acordării ajutorului, cu respectarea condițiilor de cumul aplicabile ajutorului de minimis
ATENȚIE! Criteriul cu privire la valoarea minimă a finanțării nerambursabile se va menține până la data semnării contractului de finanțare, inclusiv.
71 5.5. Cuantumul cofinanțării acordate
a) Ajutor de stat regional
Tip
Alba
Intreprindere
Micro / Mică 70
Mijlocie
60
Întreprinderi 50
mari
Contribuția programului (acoperită din FEDR și co-finanţarea
naţională acordată din bugetul de stat)
Brașov
Covasna
Harghita
Mureș
Sibiu
60
60
60
70
60
50
50
50
60
50
40
40
40
50
40
În cazul proiectelor depuse în parteneriat, rata de co-finanțare mai sus-menționată se aplică solicitantului individual/liderului de parteneriat. Ajutorul de stat regional se acordă doar solicitantului/liderului de parteneriat care face dovada deținerii dreptului real solicitat asupra imobilului ce face obiectul investiției, conform prevederilor prezentului ghid.
Cofinanțarea din contribuție proprie aferentă ajutorului regional trebuie asigurată de beneficiarul ajutorului (solicitantul...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Read section 5.7 other eligibility requirements
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '1340,1460p' g2.txt | cut -c1-1200
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
Perioada de implementare a activităților proiectului este rezonabilă și nu depășește 30 iunie 2028. Perioada de implementare a activităților proiectului se referă la activitățile ce urmează a fi realizate după momentul contractării proiectului. Solicitantul trebuie să prevadă în mod realist perioada de implementare pentru fiecare activitate în parte, luând în considerare specificul fiecărei activități.
5.7. Alte cerințe de eligibilitate a proiectului
5.7.1. Activitățile propuse se încadrează în acțiunile sprijinite în cadrul Priorității 1, Acțiunea 2. Structuri de sprijin pentru dezvoltare IMM, Intervenția 1.5.1 Incubatoare si acceleratoare de afaceri
Activitățile propuse prin proiect trebuie să se încadreze în acțiunile sprijinite în cadrul Priorității 1.O regiune competitivă prin inovare si întreprinderi dinamice pentru o economie inteligentă, 72 respectiv în acțiunile sprijinite de obiectivele specifice vizate de Intervenția 1.5.1 Incubatoare si acceleratoare de afaceri: OS 1.3. Intensificarea creșterii durabile și a competitivității IMM-urilor și crearea de locuri de muncă în cadrul IMM-urilor, inclusiv prin investiții productive și după caz, OS 1.4 Dezvoltarea competențelor pentru specializare inteligentă, tranziție industrială și antreprenoriat, conform prevederilor din secțiunile 2.2, 3.6, 5.2.1 și 5.2.2 de mai sus.
5.7.2. Proiectul se refera la dezvoltarea unui incubator de afaceri sectorial/ incubator de afaceri cu portofoliu mixt (toate firmele incubate activează în maxim 3 din cele 9 sectoare de excelență din RIS3 Centru), cu respectarea principiilor de funcționare a unui incubator de afaceri
Se are în vedere alinierea cu obiectivele asumate prin PR Centru și cu sectoarele de excelență identificate în RIS3 Centru15, respectiv:
• Automotive și Mecatronică • Industria Aeronautică • Sectorul Agricultură și Industrie Alimentară • Sectorul Silvicultură, Prelucrarea Lemnului și Mobilier • Sectorul Industrie Ușoară • Sectorul IT și Industrii Creative • Sectorul Sănătate • Sectorul Mediu Construit Sustenabil
15 Strategia de Specializare inteligentă a Regiunii Centru 2021-2027 disponibilă pentru consultare accesând https://www.adrcentru.ro/wp-content/uploads/2021/01/RIS3Centru_2021-2027.pdf
• Sectorul Turism Incubatorul de afaceri sectorial - incubatorul de afaceri în cadrul căruia toate firmele incubate activează într-unul din sectoarele de excelență din RIS3, oferă toată gama de servicii necesare celor care au o idee fezabilă, aplicabilă într-un anumit sector, expresie a potențialului endogen existent în acel teritoriu. Incubatorul de afaceri cu portofoliu mixt - incubatorul de afaceri în cadrul căruia toate firmele incubate activează în maxim 3 din sectoarele de excelență din RIS3, oferă toată gama de servicii necesare celor care au o idee fezabilă, aplicabilă într-un anumit sector, expresie a potențialului endogen existent în acel teritoriu. În funcție de sectorul vizat acestea pot necesita infrastructură specifică. Solicitantul trebuie sa se asigure că sectoarele selectate sunt complementare, iar infrastructura finanțată poate fi utilizată de mai mulți rezidenți.
La momentul lansării de evenimente de informare (de tip lansare ciclu/program, organizare sesiuni de lucru tematice, demo day, întâlniri cu investitorii), respectiv activităților de preincubare, administratorul incubatorului se va asigura că potențialii rezidenți cunosc care sunt activitățile economice acceptate (codurile CAEN în conformitate cu Anexa 3).
De asemenea, se va asigura de următoarele :
✓ La momentul semnării contractului de incubare, rezidentul are domeniul de activitate
eligibil (clasa CAEN) vizat de investiție, înscris în obiectul de activitate (conform
certificatului constatator ORC), indiferent dacă acesta reprezintă activitatea principală
sau secundară a întreprinderii.
✓ La momentul demarării activității economice, rezidentul are deja domeniul de activitate
73
eligibil (clasa CAEN) vizat de investiție, autorizat la sediul (principal sau s...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Read annexes list and ETF criteria
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '1460,1520p;1574,1724p' g2.txt | cut -c1-700
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<persisted-output>
Output too large (56.8KB). Full output saved to: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\b5s3tt5ly.txt

Preview (first 2KB):
2. Situațiile financiare ale solicitantului depuse și înregistrate la unitățile teritoriale ale
Ministerului Finanțelor aferente exercițiului financiar anterior depunerii cererii de
finanțare (pentru solicitant și parteneri, dacă este cazul)
82
a. Bilanțul; b. Contul de profit şi pierdere/Contul rezultatului exercițiului/ Contul de rezultate
patrimonial; c. Contul de execuție bugetară (Anexa Contul de execuție a bugetului: venituri şi
cheltuieli); d. Indicatori Execuție bugetara anuali (conform Anexa nr. 2 la O.M.A.I-O.M.F.P nr.
244/2651/2010 “pentru aprobarea metodologiilor de aplicare a prevederilor art. 14 alin. (7, ale art. 57 alin. (2^1) si ale art. 76^1 alin. (1 lit. e) din Legea nr. 273/2006 privind finanțele publice locale”); e. Anexa nr. 1.3 la norme şi proceduri, Calculul gradului de îndatorare- ultimul exercițiu financiar încheiat; ATENTIE! Acolo unde metodologia impune calcularea de indicatori trimestriali, se vor atașa indicatorii execuției bugetare pe bilanțurile trimestriale (31.03, 30.06, 30.09, 31.12).
Se vor atașa, dacă este cazul, inclusiv dovada depunerii acestora la unitățile teritoriale ale Ministerului Finanțelor Publice.
3. (Daca este cazul) Situațiile financiare anuale ale entităților identificate ca întreprinderi partenere și/sau legate cu solicitantul depuse / înregistrate la unitățile teritoriale ale Ministerului de Finanțe, conform Declarației privind încadrarea în categoria IMM, aferente exercițiului financiar anterior depunerii cererii de finanțare: Bilanțul prescurtat (Formular 10) , Contul de profit şi pierdere (Formular 20);
4. Declarație privind eligibilitatea TVA pentru solicitant și parteneri, dacă este cazul
Se va utiliza modelul de declarație anexat la Ghidului solicitantului (Anexa 9 Declarație privind eligibilitatea TVA) Se va anexa de către toți partenerii care au cheltuieli alocate, după caz
...
</persisted-output>
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Read annexes and ETF truncated
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '1468,1520p' g2.txt | cut -c1-450; echo =====ETF; sed -n '1574,1640p' g2.txt | cut -c1-400; echo ====ANEXE; sed -n '1715,1724p' g2.txt | cut -c1-3000
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
<persisted-output>
Output too large (32.7KB). Full output saved to: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\bjc22rsf2.txt

Preview (first 2KB):
Se vor atașa, dacă este cazul, inclusiv dovada depunerii acestora la unitățile teritoriale ale Ministerului Finanțelor Publice.
3. (Daca este cazul) Situațiile financiare anuale ale entităților identificate ca întreprinderi partenere și/sau legate cu solicitantul depuse / înregistrate la unitățile teritoriale ale Ministerului de Finanțe, conform Declarației privind încadrarea în categoria IMM, aferente exercițiului financiar anterior depunerii cererii de finanțare: Bilanțul prescurtat (Formular 10) , Contul de profit şi pierdere (Formular 20);
4. Declarație privind eligibilitatea TVA pentru solicitant și parteneri, dacă este cazul
Se va utiliza modelul de declarație anexat la Ghidului solicitantului (Anexa 9 Declarație privind eligibilitatea TVA) Se va anexa de către toți partenerii care au cheltuieli alocate, după caz
5. Declarația pe proprie răspundere a reprezentantului legal al solicitantului/liderul de parteneriat cu privire la conformitatea cu originalul a documentelor încărcate sau care vor fi încărcate în MySMIS2021/SMIS2021+ pe parcursul procesului de evaluare, selecție și contractare Se va utiliza modelul de declarație anexat la Ghidului solicitantului (Anexa 10- Declarație conformitate documente încărcate în MYSMIS)
6. Declarația privind încadrarea în categoria IMM și, dacă este cazul, Calculul pentru întreprinderi partenere sau legate (Anexa 8- Declarația privind încadrarea în categoria IMM). În cazul parteneriatelor, fiecare entitate membră a parteneriatului va completa câte o declarație. În cazul solicitanților APL sau parteneriat între APL, nu este obligatorie prezentarea acestei declarații (acești solicitanți se încadrează în categ
7. Declarație pe propria răspundere a solicitantului/partenerilor privind ajutoarele de stat și de minimis primite de întreprinderea unică în ultimii 3 ani – (Anexa 11 Declarație privind ajutoarele de stat și de minimis primite).
83 În cazul parteneriatelor, toți membrii parteneriatului vor prezenta acest document.
...
</persisted-output>
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Read]
file: C:\Users\User\.claude\projects\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\tool-results\bjc22rsf2.txt
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
1	Se vor atașa, dacă este cazul, inclusiv dovada depunerii acestora la unitățile teritoriale ale Ministerului Finanțelor Publice.
2	3. (Daca este cazul) Situațiile financiare anuale ale entităților identificate ca întreprinderi partenere și/sau legate cu solicitantul depuse / înregistrate la unitățile teritoriale ale Ministerului de Finanțe, conform Declarației privind încadrarea în categoria IMM, aferente exercițiului financiar anterior depunerii cererii de finanțare: Bilanțul prescurtat (Formular 10) , Contul de profit şi pierdere (Formular 20);
3	4. Declarație privind eligibilitatea TVA pentru solicitant și parteneri, dacă este cazul
4	Se va utiliza modelul de declarație anexat la Ghidului solicitantului (Anexa 9 Declarație privind eligibilitatea TVA) Se va anexa de către toți partenerii care au cheltuieli alocate, după caz
5	5. Declarația pe proprie răspundere a reprezentantului legal al solicitantului/liderul de parteneriat cu privire la conformitatea cu originalul a documentelor încărcate sau care vor fi încărcate în MySMIS2021/SMIS2021+ pe parcursul procesului de evaluare, selecție și contractare Se va utiliza modelul de declarație anexat la Ghidului solicitantului (Anexa 10- Declarație conformitate documente încărcate în MYSMIS)
6	6. Declarația privind încadrarea în categoria IMM și, dacă este cazul, Calculul pentru întreprinderi partenere sau legate (Anexa 8- Declarația privind încadrarea în categoria IMM). În cazul parteneriatelor, fiecare entitate membră a parteneriatului va completa câte o declarație. În cazul solicitanților APL sau parteneriat între APL, nu este obligatorie prezentarea acestei declarații (acești solicitanți se încadrează în categ
7	7. Declarație pe propria răspundere a solicitantului/partenerilor privind ajutoarele de stat și de minimis primite de întreprinderea unică în ultimii 3 ani – (Anexa 11 Declarație privind ajutoarele de stat și de minimis primite).
8	83 În cazul parteneriatelor, toți membrii parteneriatului vor prezenta acest document.
9	8. (pentru proiectele ce includ lucrări pentru care este necesară emiterea autorizării de construire) Certificatul de urbanism sau Autorizația de construire
10	Este obligatorie anexarea la cererea de finanțare a certificatului de urbanism. Certificatul de urbanism anexat la cererea de finanțare trebuie să fie cel eliberat în vederea obținerii autorizației de construire pentru proiectul aferent cererii de finanțare depuse și trebuie să fie valabil la data depunerii cererii de finanțare. Singura excepție cu privire la termenul de valabilitate a certificatului de urbanism la data depunerii cerer
11	Pentru proiectele de investiții pentru care, la data depunerii cererii de finanțare a fost emisă Autorizația de construire se va depune autorizația de construire, obținută în baza legislației în vigoare. În acest caz, la proiect nu se vor mai atașa avizele/acordurile solicitate prin certificatul de urbanism.
12	9. (pentru proiectele ce includ lucrări pentru care este necesară emiterea autorizării de construire- doar pentru proiectele care la data depunerii cererii de finanțare nu au emisă
13	Autorizația de construire) Decizia etapei de încadrare a proiectului în procedura de evaluare a impactului asupra mediului sau Clasarea notificării emisă de la autoritatea pentru protecția mediului, în conformitate cu Legea 292/2018 privind evaluarea impactului anumitor proiecte publice și private asupra mediului, cu modificările și completările ulterioare. Transmiterea Deciziei etapei de evaluare inițială nu este acceptabilă.
14	10. (pentru proiectele ce includ lucrări pentru care este necesară emiterea autorizării de construire) Devizul General în conformitate cu HG 907/2016 privind aprobarea conținutului-cadru al documentației tehnico-economice aferente investițiilor publice, precum și a structurii și metodologiei de elaborare a devizului general pentru obiective de investiții și lucrări de intervenții
15	Devizul general trebuie să fi fost realizat/actualizat cu cel mu...
[/external_agent_tool_result]

## Asistent

Am tot ce trebuie din ghid. Creez acum folderul și fișa.

## Asistent

[external_agent_tool_call: Bash]
description: Read ETF criteria descriptions fully
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '1633,1636p;1647p' g2.txt | cut -c1-2500
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
In cazul acestui apel de proiecte, vizita la fața locului se va realiza în etapa de contractare, pentru un eșantion de cel puțin 10% din proiectele pentru care se demarează etapa de contractare. La această vizită va participa un expert din partea AM PR, vizita având drept scop verificarea măsurii în care spațiul destinat implementării proiectului este adecvat realizării investiției propuse în cererea de finanțare. Din partea solicitantului, la vizita la fața locului va participa reprezentantul legal al solicitantului/împuternicit al acestuia.
Vizita în teren se va realiza în termenul de 15 zile lucrătoare aferent solicitărilor de clarificări, în caz contrar proiectul fiind exclus din procesul de contractare.
Nu se va prelua niciun document la etapa de vizită la fața locului, iar cu ocazia acesteia nu trebuie să se aducă clarificări suplimentare ori informații care nu se regăsesc în cererea de finanțare depusă.
8.9.2. Decizia de acordare/respingere a finanțării
9. ASPECTE PRIVIND CONFLICTUL DE INTERESE Pe parcursul derulării procesului de evaluare, selecție, contractare, implementare si pe perioada de durabilitate a proiectului, solicitanții de finanțare au obligația de a respecta toate prevederile legale naționale si europene în vigoare cu privire la conflictul de interese. Reprezentatul legal al solicitantului are obligația de a lua toate măsurile necesare pentru a evita apariția sau pentru a înlătura orice situație de natură să determine un conflict de interese, pe toată perioada menționată mai sus, începând cu data depunerii cereri de finanțare. Totodată, reprezentantul legal al solicitantului are obligația de a informa AM PR Centru despre orice situație are cunoștința si care este de natură să dea naștere unui conflict de interese. Pe parcursul derulării procesului de evaluare, selecție, contractare, implementare si pe perioada de durabilitate a proiectului, AM PR Centru va lua toate măsurile necesare pentru a evita apariția sau pentru a înlătura orice situație de natură să determine un conflict de interese, în conformitate cu prevederile naționale și europene în vigoare aplicabile. Persoanele implicate în elaborarea și implementarea proiectelor sunt obligate să evite crearea unei situații de conflict de interese. Acestea trebuie să-și exercite imparțial și obiectiv atribuțiile, funcțiile deținute/încredințate și să se abțină de la orice acte sau fapte care implică familia, viața afectivă, afinitățile politice/naționale, interesul economic sau orice alt interes personal sau direct. Astfel, persoanele implicate vor lua decizii numai pe criterii obiective de natură juridică/tehnică/economică și altele asemenea, întemeindu-se pe dovezi suficiente și adecvate.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Read full ETF criteria lines
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && grep -n "^I. Contribuția proiectului\|^II. Capacitatea\|^III. Calitatea\|Departajarea proiectelor" g2.txt | cut -d: -f1 | while read n; do sed -n "${n}p" g2.txt | cut -c1-1800; echo; done
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
I. Contribuția proiectului la realizarea obiectivului priorității de investiție Prioritizarea proiectelor se face în baza obiectivelor și rezultatelor asumate de solicitant prin investiția propusă, cu referire la capacitatea de incubare, locurile de muncă create de firmele rezidente, gradul de ocupare a incubatorului, rata de supraviețuire a firmelor incubate, includerea de programe de instruire pentru angajați.

II. Capacitatea solicitantului de implementare a proiectului In cadrul acestui criteriu, se analizează performanța instituțională a solicitantului în activitatea de incubare și derularea de proiecte/programe de accelerare a afacerilor, sprijin pentru antreprenoriat, competența și calificările pe care le are administratorul incubatorului și personalul acestuia și nu în ultimul rând serviciile oferite firmelor incubate

III. Calitatea, maturitatea si sustenabilitatea proiectului Prioritizarea se face pe baza calității planului de dezvoltare a incubatorului, calitatea şi justificarea bugetului, precum și maturitatea proiectului; se analizează sustenabilitatea solicitantului si a 94 proiectului (sustenabilitatea operațională (planul de mentenanță cu lucrările specifice) şi financiară (sustenabilitatea financiara a societății).

Departajarea proiectelor care au obținut același punctaj, în vederea încadrării în alocarea apelului de proiecte și demarării etapei de contractare, se va face în funcție de punctajele obținute la următoarele criterii, în ordinea enumerată, până la departajarea solicitanților: 1.1.Numărul de întreprinderi care utilizează capacitatea de incubare 1.2. Raportul cost eficienta a investiției 2.1. Performanța instituțională a administratorului incubatorului de afaceri 1.3. Gradul de ocupare a incubatorului de afaceri 2.2. Competențele și calificările existente la nivelul incubatorului 2.3. Contractul de incubare 1.4. Angajați din IMM-uri care finalizează programe de formare a competențelor pentru specializare inteligentă, pentru tranziție industrială și antreprenoriat (pe tip de competente:
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Inspect template styles
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && python -c "
import docx;d=docx.Document('cond152.docx')
for p in d.paragraphs[:40]: print(repr(p.style.name), [ (r.bold,r.font.size) for r in p.runs][:2], p.text[:50])
print(d.sections[0].left_margin, len(d.tables))"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
Traceback (most recent call last):
  File "<string>", line 3, in <module>
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u021a' in position 5: character maps to <undefined>
'Normal' [(True, None)]
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Inspect template styles
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && PYTHONIOENCODING=utf-8 python -c "
import docx;d=docx.Document('cond152.docx')
for p in d.paragraphs[:25]: print(repr(p.style.name), p.paragraph_format.left_indent, [ (r.bold,r.font.size,r.font.name) for r in p.runs][:2], p.text[:50])
print(d.sections[0].left_margin, len(d.tables))"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
'Normal' None [(True, None, None)] CONDIȚII DE ELIGIBILITATE – Intervenția 1.5.2 Parc
'Normal' None [(True, None, None)] 1. Tipul apelului
'Normal' None [(None, None, None), (True, None, None)] Apelul este competitiv, cu termen limită de depune
'Normal' None [(None, None, None)] Cod apel:
'Normal' None [(True, None, None)] PRC/1058/PRC_P1/OP1/RSO1.3/PRC_A37
'Normal' None [(None, None, None)] Perioada apelului:
'Normal' None [(True, None, None), (None, None, None)] Data deschidere apel: 18 iunie 2026
Depunere proie
'Normal' None [(None, None, None), (True, None, None)] Cererile de finanțare se depun exclusiv prin MySMI
'Normal' None [(None, None, None)] 
'Normal' None [(True, None, None)] 2. Bugetul apelului
'Normal' None [(None, None, None)] Alocarea totală a apelului este:
'Normal' None [(True, None, None)] 10.855.626 euro
'Normal' None [(None, None, None)] din care:
'Normal' None [(True, None, None), (None, None, None)] 9.227.282 euro FEDR;
'Normal' None [(True, None, None), (None, None, None)] 1.628.344 euro buget de stat.
'Normal' None [(None, None, None)] Bugetul este împărțit astfel:
'Normal' None [(True, None, None), (None, None, None)] 9.443.862 euro pentru componenta de ajutor de stat
'Normal' None [(True, None, None), (None, None, None)] 1.411.764 euro pentru componenta de ajutor de mini
'Normal' None [(None, None, None)] Cursul InforEuro utilizat este cel din luna iunie 
'Normal' None [(True, None, None), (None, None, None)] 1 euro = 5,2481 lei. 
'Normal' None [(None, None, None)] 
'Normal' None [(True, None, None)] 3. Scopul apelului
'Normal' None [(None, None, None), (True, None, None)] Apelul finanțează crearea, extinderea și moderniza
'Normal' None [(None, None, None)] Sunt sprijinite:
'Normal' None [(None, None, None), (True, None, None)] proiecte greenfield – parcuri industriale dezvolta
914400 0
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa.py (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Create project folder, copy guide, generate fisa
command: $b="\\192.168.100.169\Comun\00. Proiecte 2026"; $f="$b\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2"; New-Item -ItemType Directory -Force "$f\0.ARHIVA","$f\1. DOCUMENTE OFICIALE\ANEXE" | Out-Null; Copy-Item "$b\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf" "$f\1. DOCUMENTE OFICIALE\"; $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; python "$s\make_fisa.py" "$f\CONDIȚII DE ELIGIBILITATE.docx"; Get-ChildItem $f -Recurse | % { $_.FullName + " | " + $_.Length }
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
ok
\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\0.ARHIVA | 1
\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\1. DOCUMENTE OFICIALE | 1
\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\CONDIȚII DE ELIGIBILITATE.docx | 45120
\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\1. DOCUMENTE OFICIALE\ANEXE | 1
\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\1. DOCUMENTE OFICIALE\Ghidul-solicitantului-Interventia-1.5.1-–-Apel-2.pdf | 2086249
[/external_agent_tool_result]

## Asistent

Nu aveai folder pentru Apelul 2 la 1.5.1, așa că l-am creat și am pus în el fișa de proiect, făcută după modelul celorlalte fișe din `00. Proiecte 2026`.

**Ce am verificat**
- În `\\192.168.100.169\Comun\00. Proiecte 2026\` ghidul era doar în rădăcina folderului, fără folder de proiect. Folderul pentru 1.5.2 Parcuri industriale există, dar e altă intervenție.
- Pentru Apelul 1 ai două foldere în `00. Proiecte`, pe care le poți refolosi:
  - `\\192.168.100.169\Comun\00. Proiecte\2025.10.10 - 1.5.1 Incubatoare si aceleratoare de afaceri`: documentele oficiale ale Apelului 1.
  - `\\192.168.100.169\Comun\00. Proiecte\2025.12.10 Incubatoare de afaceri`: dosarul lucrat (P1, incubator IT în hala C4, RED INTERNET SALES), cu secțiunile cererii de finanțare, deviz și clarificările 1 și 2.

**Ce am creat**
- Folder: `\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\`
  - `0.ARHIVA\`
  - `1. DOCUMENTE OFICIALE\` cu o copie a ghidului; subfolderul `ANEXE\` e gol deocamdată.
  - Fișa: `\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\CONDIȚII DE ELIGIBILITATE.docx`. Are 22 de secțiuni, checklist de eligibilitate și trimiteri la dosarul din Apelul 1.

**Ce reține fișa din ghid**
- **Cod apel:** PRC/1218/PRC_P1/OP1. Depunerea e între **21.10.2026, ora 12:00** și **21.12.2026, ora 12:00**, prin MySMIS.
- **Buget apel:** 9.201.232 €. Pe proiect se pot cere între **100.000 și 2.000.000 €**, din care maximum 300.000 € ajutor de minimis.
- **Partea de investiție (ajutor de stat regional):** se finanțează 70% în Alba și Mureș și 60% în celelalte județe, pentru micro- și întreprinderi mici. UAT-urile se încadrează ca întreprinderi mari, deci primesc 50% sau 40%.
- **Partea de servicii (ajutor de minimis):** se finanțează 100%.
- **Implementarea** trebuie terminată până la **30.06.2028**.
- **Selecția:** în prima lună de depunere (până la 30.11.2026) intră la contractare doar proiectele cu minimum **85 de puncte**; după aceea pragul e de 70. Merită să țintești prima lună.
- **Motive sigure de respingere:**
  - lipsește Planul de dezvoltare (Anexa 15) sau Macheta financiară (Anexa 16);
  - pachetul de incubare nu include obligatoriu consultanță în afaceri și management;
  - lucrările de construcție și dotările sunt sub 50% din bugetul eligibil;
  - proiectul e un incubator doar virtual sau un centru de afaceri.
- **Țintă:** minimum 16 firme incubate (10 dacă incubatorul e pe un singur sector de producție), în maximum 3 dintre sectoarele de specializare ale Regiunii Centru.

**Ce rămâne de făcut**
- **Anexele ghidului (1–18)** trebuie descărcate de pe regiocentru.ro în `ANEXE\`. Spune-mi dacă vrei să le descarc eu.
- **Ghidul din rădăcina** `00. Proiecte 2026` e tot acolo, eu doar l-am copiat. Dacă vrei, îl șterg din rădăcină.
- **Coșul de reciclare:** o copie a ghidului apare și în `#recycle\00. Proiecte 2026`, deci probabil l-ai mai mutat sau șters o dată de acolo.

## Asistent

[external_agent_tool_call: Bash]
description: Locate section boundaries and read state aid exclusions
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && grep -n "^3.14\|^7.6\|^7.7\|^5.2. Eligibilitatea\|^5.1. Eligib\|^3.13\|^8.1\|^2. Documente privind identificarea" g2.txt; sed -n '530,740p' g2.txt | cut -c1-220
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
19:5.1. Eligibilitatea solicitanților și partenerilor .......................................................................... 43
20:5.2. Eligibilitatea activităților.................................................................................................... 54
34:7.6. Anexele și documente obligatorii la momentul contractării ............................................ 86
35:7.7. Renunțarea la cererea de finanțare .................................................................................. 91
37:8.1. Principalele etape ale procesului de evaluare, selecție și contractare ............................. 91
510:3.13. Reguli privind ajutorul de stat
737:3.14. Reguli privind instrumentele financiare Nu este cazul.
794:5.1. Eligibilitatea solicitanților și partenerilor
959:5.2. Eligibilitatea activităților
1504:7.6. Anexele și documente obligatorii la momentul contractării
1519:2. Documente privind identificarea reprezentantului legal al solicitantului/ liderului de
1556:7.7. Renunțarea la cererea de finanțare
1559:8.1. Principalele etape ale procesului de evaluare, selecție și contractare
ajutoarelor este stabilit pe baza prețului sau a cantității de produse achiziționate sau
introduse pe piață;
c) ajutoarelor acordate întreprinderilor care își desfășoară activitatea în domeniul
producției primare de produse agricole;
d) ajutoarelor acordate întreprinderilor care desfășoară activități de prelucrare și
comercializare a produselor agricole, în unul din următoarele cazuri:
i. atunci când valoarea ajutoarelor este stabilită pe baza prețului sau a cantității de produse
de acest tip achiziționate de la producători primari sau introduse pe piață de
întreprinderile respective;
ii. atunci când ajutoarele sunt condiționate de transferarea lor parțială sau integrală către
producătorii primari;
e) ajutoarelor destinate activităților legate de export către țări terțe sau către alte state
membre, respectiv ajutoarelor direct legate de cantitățile exportate, ajutoarelor
destinate înființării și funcționării unei rețele de distribuție sau destinate altor cheltuieli
curente legate de activitatea de export;
f) ajutoarelor condiționate de utilizarea preferențială a bunurilor și serviciilor naționale față
de bunurile și serviciile importate.
g) ajutoarelor acordate întreprinderilor care își desfășoară activitatea în domeniul
producției primare de produse pescărești și de acvacultură;
h) ajutoarelor acordate întreprinderilor care desfășoară activități de prelucrare și
comercializare a produselor pescărești și de acvacultură, în cazul în care cuantumul
ajutoarelor este stabilit pe baza prețului sau a cantității de produse achiziționate sau
introduse pe piață;
i) ajutoarelor acordate întreprinderilor care își desfășoară activitatea în domeniul
producției primare de produse agricole;
j) ajutoarelor acordate întreprinderilor care desfășoară activități de prelucrare și
comercializare a produselor agricole, în unul din următoarele cazuri:
iii. atunci când valoarea ajutoarelor este stabilită pe baza prețului sau a cantității de produse
de acest tip achiziționate de la producători primari sau introduse pe piață de
întreprinderile respective;
iv. atunci când ajutoarele sunt condiționate de transferarea lor parțială sau integrală către
producătorii primari;
k) ajutoarelor destinate activităților legate de export către țări terțe sau către alte state
membre, respectiv ajutoarelor direct legate de cantitățile exportate, ajutoarelor
destinate înființării și funcționării unei rețele de distribuție sau destinate altor cheltuieli
curente legate de activitatea de export;
l) ajutoarelor condiționate de utilizarea preferențială a bunurilor și serviciilor naționale față
de bunurile și serviciile importate.
m) ajutoarelor pentru facilitarea închiderii minelor de cărbune necompetitive, astfel cum
sunt reglementate de Decizia 2010/787/UE a Consiliului;
n) ajutoarelor pentru sectorul siderurgic, sectorul lignitului și sectorul cărbunelui;
o) ajutoarelor pen...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Find markers and read contracting docs
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && grep -n "^Un solicitant care își desfășoară\|^Ajutorul de stat regional$\|^Ajutorul de minimis$\|^Pentru cheltuielile finanțate prin ajutorul de minimis\|^Calcularea echivalentului" g2.txt; sed -n '1504,1556p' g2.txt | cut -c1-160 | head -80
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
606:Un solicitant care își desfășoară activitatea atât în sectoare/domenii eligibile, cât și în sectoare/domenii neeligibile, așa cum sunt menționate anterior, poate beneficia de finanțare pentru domeniile de activitate eligibile, cu condiția să se asigure, prin mijloace corespunzătoare, precum separarea activităților sau o distincție între costuri, că activitățile desfășurate în sectoarele excluse nu beneficiază de ajutoarele de stat acordate în baza prezentului ghid și respectă prevederile schemei de ajutor de stat și de minimis aplicabile acestuia. Acest aspect este inclus în Declarația unică, depusă odată cu cererea de finanțare.
607:Ajutorul de stat regional
646:Ajutorul de minimis
724:Pentru cheltuielile finanțate prin ajutorul de minimis, valoarea ajutorului de minimis acordată este de 300.000 euro, cu respectarea plafonului de minimis acordat unei întreprinderi unice în ultimii 3 ani. Perioada de 3 ani care trebuie luată în considerare în sensul prezentului regulament ar trebui evaluată în mod continuu. Pentru fiecare nou ajutor de minimis acordat, trebuie luată în considerare valoarea totală a ajutoarelor de minimis acordate în ultimii 3 ani.
725:Calcularea echivalentului subvenție brută Regulament de minimis se aplică numai ajutoarelor pentru care este posibilă calcularea ex ante cu exactitate a echivalentului subvenție brută pentru ajutoare, fără a fi necesară efectuarea unei
7.6. Anexele și documente obligatorii la momentul contractării
1. Documentele statutare ale solicitantului și ale partenerilor (dacă este cazul)
Pentru unități administrativ teritoriale comună, oraș municipiu, municipiu reședință de județ ✓ Hotărâre judecătorească de validare primar și Hot
Pentru unități administrativ teritoriale județ ✓ Hotărârea judecătorească de validare a Președintelui Consiliului judeţean și Hotărârea Consiliulu
sau Hotărâre de validare a Consiliului Județean/ Hotărârea Consiliului județean de alegere a Președintelui Consiliului Județean Vor fi prezentate după
Pentru instituție sau consorțiu de instituții de învățământ superior acreditate (universități, institute, academii de studii) înființate potrivit Le
✓ Documentul legal privind înființarea, funcționarea, acreditarea instituției (după caz) de învățământ superior, inclusiv documentul din care să re
✓ Ordinul de numire al reprezentantului legal al instituției de învățământ superior (ex. , Ordinul de numire in funcție a rectorului)
✓ Alte documente statutare în funcție de specificul partenerului
Pentru institute, centre și stațiuni de cercetare dezvoltare: conform legii de înființare, organizare 87 și funcționare a acestora. (ex. Hotărâre privin
de Cercetare Dezvoltare; Hotărârea pentru aprobarea Regulamentului-cadru de organizare şi funcționare
Pentru camere de comerț: documente statutare conform legii de înființare, organizare și funcționare a acestora.
Pentru persoanele juridice de drept privat ✓ În cazul persoanelor juridice de drept privat se vor anexa documentele statutare, după caz: act constitutiv, co
În conformitatea cu Ordonanța 26/2000 cu privire la asociații și fundații, ONG devine persoana juridică din momentul înscrierii ei în Registrul asocia�
În cazul solicitanților din alte state membre ale Uniunii Europene, entități înregistrate în conformitate cu legislația specifică din statul membru a c�
2. Documente privind identificarea reprezentantului legal al solicitantului/ liderului de
parteneriat și, dacă este cazul a partenerilor
Pentru reprezentantul legal al solicitantului individual/ liderului de parteneriat și, dacă este cazul,
al partenerului se va anexa o copie a documentului de identificare.
88
Datele din documentul de identificare trebuie să corespundă cu cele menționate în cadrul cererii de finanțare la secțiunea privind identificarea reprezent
3. [unde e cazul] Mandatul special/ împuternicirea specială pentru semnarea anumitor secțiuni din cererea de finanțare
În cazul în care reprezentantul legal al solicitantului este un cetăţean străin nerez...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Write]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
File created successfully at: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py (file state is current in your context — no need to Read it back)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Generate full eligibility docx and preview
command: $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; $f="\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2"; cd $s; $env:PYTHONIOENCODING="utf-8"; python make_fisa2.py "$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx"; python -c "import docx;d=docx.Document(r'$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx');t=[p.text for p in d.paragraphs];print(len(t));[print(x[:150]) for x in t[15:60]]"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
nu gasesc: 5. CONDIȚII DE ELIGIBILITATE
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\api.py", line 27, in Document
    document_part = cast("DocumentPart", Package.open(docx).main_document_part)
                                         ^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\package.py", line 126, in open
    pkg_reader = PackageReader.from_file(pkg_file)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\pkgreader.py", line 22, in from_file
    phys_reader = PhysPkgReader(pkg_file)
                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\phys_pkg.py", line 21, in __new__
    raise PackageNotFoundError("Package not found at '%s'" % pkg_file)
docx.opc.exceptions.PackageNotFoundError: Package not found at '\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx'
[/external_agent_tool_result]

## Asistent

Line 789 is "5. CONDIȚII DE ELIGIBILITATE" — probably a different character; I'll use the line after the heading.

## Asistent

[external_agent_tool_call: PowerShell]
description: Fix marker and regenerate docx
command: $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; cd $s; (Get-Content make_fisa2.py -Encoding utf8) -replace "find\('5\. CONDIȚII DE ELIGIBILITATE', 700\)","find('Cererea de finanțare (inclusiv anexele', 700)" | Set-Content make_fisa2.py -Encoding utf8; $f="\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2"; $env:PYTHONIOENCODING="utf-8"; python make_fisa2.py "$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx"; python -c "import docx;d=docx.Document(r'$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx');t=[p.text for p in d.paragraphs];print(len(t));[print(x[:140]) for x in t[17:75]]"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
nu gasesc: 3.5. Zona/zonele
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\api.py", line 27, in Document
    document_part = cast("DocumentPart", Package.open(docx).main_document_part)
                                         ^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\package.py", line 126, in open
    pkg_reader = PackageReader.from_file(pkg_file)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\pkgreader.py", line 22, in from_file
    phys_reader = PhysPkgReader(pkg_file)
                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\docx\opc\phys_pkg.py", line 21, in __new__
    raise PackageNotFoundError("Package not found at '%s'" % pkg_file)
docx.opc.exceptions.PackageNotFoundError: Package not found at '\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx'
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Verify all section markers exist
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -i "s#find('3.5. Zona/zonele', 200)#find('3.5. Zona', 200)#" make_fisa2.py && grep -o "find('[^']*'" make_fisa2.py | sed "s/find('//;s/'$//" | while read p; do printf "%s -> " "$p"; grep -n -F -m1 -- "$p" g2.txt | cut -c1-8 | grep -v "^1[0-9]:\|^[0-9]:\|^[2-5][0-9]:" || echo; done
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
5.1.2. Categorii de solicitanți eligibili -> 926:5.1.
5.2. Eligibilitatea activităților -> 
Cererea de finanțare (inclusiv anexele -> 790:Cere
5.1.2. Categorii de solicitanți eligibili -> 926:5.1.
3.4. Rata de cofinanțare -> 
3.5. Zona -> 
Ajutorul nu poate fi acordat unui beneficiar care a efectuat o relocare -> 522:Aju
Ajutorul de stat regional -> 246:a) A
Ajutorul de minimis -> 280:b) A
3.14. Reguli privind -> 737:3.14
7.4. Anexe și documente obligatorii la depunerea cererii -> 
7.5. Aspecte administrative -> 
7.6. Anexele și documente obligatorii la momentul contractării -> 
7.7. Renunțarea ->
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: PowerShell]
description: Regenerate docx and preview
command: $s="C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad"; cd $s; $f="\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2"; $env:PYTHONIOENCODING="utf-8"; python make_fisa2.py "$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx"; if ($?) { python -c "import docx;d=docx.Document(r'$f\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx');t=[p.text for p in d.paragraphs];print(len(t));[print(x[:140]) for x in t[17:70]]" }
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
nu gasesc: 3.5. Zona
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Inspect raw line bytes and script
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -n '284,287p' g2.txt | cut -c1-60 | od -c | head -20; grep -n "find(" make_fisa2.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
0000000   i   n   c   u   b   a   t   o   r   u   l   u   i       p   e
0000020   n   t   r   u       a   c   t   i   v   i   t 304 203 310 233
0000040   i       d   e       t   i   p       s   o   f   t       a   f
0000060   e   r   e   n   t   e       d   e   z   v   o  \n   M   o   d
0000100   a   l   i   t   a   t   e   a       d   e       p   a   r   t
0000120   i   c   i   p   a   r   e       a       p   a   r   t   e   n
0000140   e   r   i   l   o   r       l   a       a   s   i   g   u   r
0000160   a   r   e   a       c   h   e   l  \n  \f   3   .   5   .    
0000200   Z   o   n   a   /   z   o   n   e   l   e       g   e   o   g
0000220   r   a   f   i   c 304 203   (   e   )       v   i   z   a   t
0000240 304 203   (   e   )       d   e       a   p   e   l   u   l    
0000260   d   e       p   r   o  \n   Z   o   n   a       v   i   z   a
0000300   t 304 203       d   e       p   r   e   z   e   n   t   u   l
0000320       a   p   e   l       d   e       p   r   o   i   e   c   t
0000340   e       t   r   e   b   u   i   e       s 304 203       f   i
0000360   e       s  \n
0000364
7:def find(prefix, start=0):
69:     find('5.1.2. Categorii de solicitanți eligibili'), find('5.2. Eligibilitatea activităților', 900)),
71:     find('Cererea de finanțare (inclusiv anexele', 700), find('5.1.2. Categorii de solicitanți eligibili')),
73:     find('3.4. Rata de cofinanțare', 200), find('3.5. Zona', 200)),
75:     find('Ajutorul nu poate fi acordat unui beneficiar care a efectuat o relocare'), find('Ajutorul de stat regional', 600)),
77:     find('Ajutorul de minimis', 640), find('3.14. Reguli privind', 700)),
79:     find('7.4. Anexe și documente obligatorii la depunerea cererii', 1000), find('7.5. Aspecte administrative', 1000)),
81:     find('7.6. Anexele și documente obligatorii la momentul contractării', 1000), find('7.7. Renunțarea', 1000)),
[/external_agent_tool_result]

## Asistent

Form feeds (`\f`) at page starts — I'll strip them when reading.

## Asistent

[external_agent_tool_call: Bash]
description: Strip form feeds and regenerate
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && sed -i "s#read().split('\\\\n')#read().replace('\\\\f','').split('\\\\n')#" make_fisa2.py && grep -n "read()" make_fisa2.py && F="//192.168.100.169/Comun/00. Proiecte 2026/2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2/FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx" && PYTHONIOENCODING=utf-8 python make_fisa2.py "$F" && PYTHONIOENCODING=utf-8 python -c "
import docx,sys;d=docx.Document(sys.argv[1]);t=[p.text for p in d.paragraphs];print(len(t))
for x in t[17:60]: print(x[:130])" "$F"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
5:L = open('g2.txt', encoding='utf-8').read().split('\n')
nu gasesc: 3.5. Zona
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Edit]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Regenerate docx and preview
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && F="//192.168.100.169/Comun/00. Proiecte 2026/2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2/FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx" && PYTHONIOENCODING=utf-8 python make_fisa2.py "$F" && PYTHONIOENCODING=utf-8 python -c "
import docx,sys;d=docx.Document(sys.argv[1]);t=[p.text for p in d.paragraphs];print(len(t))
for x in t[17:70]: print(x[:130])" "$F"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
ok [('A.', 33), ('B.', 136), ('C.', 44), ('D.', 85), ('E.', 91), ('F.', 42), ('G.', 52)]
318

A. CATEGORII DE SOLICITANȚI ȘI PARTENERI ELIGIBILI (cap. 5.1.2 – 5.1.4)
5.1.2. Categorii de solicitanți eligibili
A. Entitățile individuale care au calitatea de fondator al incubatorului de afaceri Conform Legii 102/2016 cu modificările si comp
1. Autoritate a administrației publice locale - unități administrativ-teritoriale din mediul urban sau rural: județele, municipiil
2. Instituții de învățământ superior acreditate (universități, institute, academii de studii) înființate și acreditate în conformi
3. Institute, centre și stațiuni de cercetare-dezvoltare (înființate în baza Ordonanței Guvernului nr. 57/2002 privind cercetarea 
4. Camere de comerț (înființate în baza Legii camerelor de comerț din România nr. 335/2007, cu modificările și completările ulteri
5. Societate (înființată în baza Legii societăților nr. 31/1990, republicată, cu modificările și completările ulterioare) ;
6. Societate cooperativă (înființată în baza Legii nr. 1/2005 privind organizarea şi funcționarea cooperației);
7. Asociații și fundații constituite în baza Ordonanței Guvernului nr. 26/2000 aprobată cu modificări şi completări prin Legea nr.
8. Organizație patronală sau organizație sindicală înregistrate conform Legii dialogului social nr. 62/2011, cu modificările și co
În cazul solicitanților din alte state membre ale Uniunii Europene, aceștia trebuie să fie înregistrați în conformitate cu legisla
ATENTIE! Pentru derularea activităților de tip soft (obligatorii), entitatea solicitantă (individual) trebuie să aibă și calitatea
B. Parteneriatele:
1. Parteneriatele dintre fondatorii incubatorului de afaceri menționați la litera A (maxim 3) – cu condiția ca unul dintre fondato
2. Parteneriate între maxim 2 entitățile menționate la litera A și administratorului incubatorului de afaceri .
Indiferent de forma de organizare a solicitantului (entitate individuală sau parteneriat), acesta este considerat întreprindere și
Categoria microîntreprinderilor și a întreprinderilor mici și mijlocii („IMM-uri”) este formată din întreprinderi care au mai puți
✓ în cadrul categoriei IMM-urilor, o întreprindere mijlocie are între 50 și 250 de salariați şi realizează o cifră de afaceri anua
Se recomandă o atenţie sporită în aplicarea corectă a prevederilor Legii 346/2004, cu modificările și completările ulterioare, în 
Solicitantul IMM va completa şi Anexa 8 - Declarație privind încadrarea întreprinderii în categoria IMM (din care să reiasă încadr
ATENTIE! Valoarea finanțării nerambursabile solicitate la data depunerii cererii de finanțare nu poate fi modificată în sensul cre
5.1.3. Categorii de parteneri eligibili
În cazul în care solicitantul este un parteneriat, parteneriatul este format astfel: 1. Parteneriatele dintre fondatorii incubator
ATENTIE! Pentru implementarea activităților de tip soft, oricare din membrii parteneriatului poate să aibă calitatea de administra
2. Parteneriate între maxim 2 entitățile menționate la secțiunea 5.1.2, litera A și administratorului incubatorului de afaceri .
5.1.4. Reguli și cerințe privind parteneriatul
Criteriile de eligibilitate ale solicitantului se aplică fiecărui partener din cadrul acordului de parteneriat, după cum este indi
Liderul de parteneriat trebuie să fie reprezentat în mod obligatoriu de solicitantul care deține un drept real asupra infrastructu
Entitatea solicitantă (individual) sau oricare din membrii parteneriatului pot avea și calitatea de administrator al incubatorului
Pentru activități de tip soft (promovarea incubatorului de afaceri și a bunelor practici, activități de sprijinire a firmelor incu
În scopul constituirii parteneriatelor se încheie acorduri de tipul celor descrise în prezentul ghid (a se vedea Anexa 7- Acord de
Orice modificare pe parcursul perioadei de evaluare, selecție și contractare asupra situațiilor prevăzute în cadrul declarațiilor 

B. CERINȚE GENERALE PRIV...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Edit]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py has been updated successfully.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Regenerate and check list items present
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && F="//192.168.100.169/Comun/00. Proiecte 2026/2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2/FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx" && PYTHONIOENCODING=utf-8 python make_fisa2.py "$F" && PYTHONIOENCODING=utf-8 python -c "
import docx,sys;d=docx.Document(sys.argv[1]);t=[p.text for p in d.paragraphs];print(len(t))
for x in t: 
  if x[:3] in ('a. ','b. ','c. ','d. ','e. ','f. ','g. ','a) ','b) ','c) ','d) ','e) ','f) ','g) ','h) ','i) ','j) ','k) ','l) ','m) ','n) ','o) ','p) ','q) ','r) ','s) ','t) ','u) ','v) ','w) ','x) ') or x[:2] in ('2.','3.','4.','5.','6.'): print(x[:90])" "$F"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
ok [('A.', 33), ('B.', 136), ('C.', 44), ('D.', 85), ('E.', 91), ('F.', 42), ('G.', 52)]
327
5.1.2. Categorii de solicitanți eligibili
2. Instituții de învățământ superior acreditate (universități, institute, academii de stud
3. Institute, centre și stațiuni de cercetare-dezvoltare (înființate în baza Ordonanței Gu
4. Camere de comerț (înființate în baza Legii camerelor de comerț din România nr. 335/2007
5. Societate (înființată în baza Legii societăților nr. 31/1990, republicată, cu modificăr
6. Societate cooperativă (înființată în baza Legii nr. 1/2005 privind organizarea şi funcț
2. Parteneriate între maxim 2 entitățile menționate la litera A și administratorului incub
5.1.3. Categorii de parteneri eligibili
2. Parteneriate între maxim 2 entitățile menționate la secțiunea 5.1.2, litera A și admini
5.1.4. Reguli și cerințe privind parteneriatul
5.1. Eligibilitatea solicitanților și partenerilor
5.1.1. Cerințe generale privind eligibilitatea solicitanților și partenerilor
a. Se află în stare de faliment/ insolvență sau face obiectul unei proceduri de lichidare 
b. Face obiectul unei proceduri legale pentru declararea sa într-una din situațiile de la 
c. Este subiectul unui ordin de recuperare în urma unei decizii anterioare a organelor com
d. Este în dificultate, în conformitate cu Regulamentul (UE) nr. 651/2014 al Comisiei din 
e. A fost găsit vinovat, printr-o hotărâre judecătorească definitivă, pentru comiterea une
f. Are obligații de plată scadente către instituțiile publice, nu şi-a îndeplinit la timp 
g. Solicitantul, inclusiv toate entitățile cu care formează un grup de firme (dacă este ca
a) în cazul solicitantului pentru care au fost stabilite debite în sarcina sa ca urmare a 
b) deține dreptul legal de a desfășura activitățile prevăzute în cadrul proiectului.
2. Solicitantul (Solicitantul individual/Membrii parteneriatului) are capacitatea financia
3. Solicitantul (Solicitantul individual/parteneriatul) a selectat administratorul incubat
a) este înregistrată ca operator economic, persoană juridică conform Legii societăţilor nr
b) nu este în stare de faliment ori lichidare, conform prevederilor Legii nr. 85/2014 priv
c) deţine personal calificat, cu experienţă profesionala de minim 3 ani în domeniul juridi
d) prezintă planul de dezvoltare a incubatorului de afaceri, cuprinzând modul de autofinan
e) prezintă strategia de monitorizare a rezidenţilor incubatorului pe parcursul a 2 ani po
f) prezintă un plan de promovare pentru perioada de preincubare şi un plan de afaceri pe d
g) este numit de către fondator, dacă acesta este o persoană juridică de drept privat, pân
h) este selectat conform regulamentului de selectare şi numire a administratorului incubat
4. Solicitantul individual/liderul de parteneriat deține drepturi asupra imobilului (clădi
5. Solicitantul individual/ membrii parteneriatului demonstrează că poate/pot să asigure c
a) să nu înceteze sau delocalizeze activitatea productivă în afara regiunii de dezvoltare 
b) să nu realizeze o modificare asupra calității și dreptului său asupra imobilului, decât
c) să nu realizeze o modificare substanțială care afectează natura, obiectivele sau condiț
6. (pentru proiectele care prevăd lucrări de construcții care se supun autorizării) Imobil
a) să fie liber de orice sarcini sau interdicții incompatibile cu realizarea activităților
b) să nu facă obiectul unor garanții, cesionări și nici a unei alte forme de sarcini care 
3.4. Rata de cofinanțare
a) Ajutorul de stat regional
b) Ajutorul de minimis Pentru proiectele depuse în cadrul prezentului apel rata de cofinan
a) ajutoarelor acordate întreprinderilor care își desfășoară activitatea în domeniul produ
b) ajutoarelor acordate întreprinderilor care desfășoară activități de prelucrare și comer
c) ajutoarelor acordate întreprinderilor care își desfășoară activitatea în domeniul produ
d) ajutoarelor acordate întreprinderilor care desfășoară activități de prelucrare și comer
e...
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Inspect section C paragraphs
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && PYTHONIOENCODING=utf-8 python -c "
exec(open('make_fisa2.py',encoding='utf-8').read().split('d = docx.Document()')[0].replace('out = sys.argv[1]',''))
a=find('3.4. Rata de cofinanțare',200);b=find('3.5. Zona',200)
for i,p in enumerate(clean(a,b)): print(i,p[:80])"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
Exit code 1
Traceback (most recent call last):
  File "<string>", line 2, in <module>
  File "<string>", line 1
    ﻿import docx, re, sys
    ^
SyntaxError: invalid non-printable character U+FEFF
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Inspect section C paragraphs
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && PYTHONIOENCODING=utf-8 python -c "
exec(open('make_fisa2.py',encoding='utf-8-sig').read().split('d = docx.Document()')[0].replace('out = sys.argv[1]',''))
a=find('3.4. Rata de cofinanțare',200);b=find('3.5. Zona',200)
for i,p in enumerate(clean(a,b)): print(i,p[:80])"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
0 3.4. Rata de cofinanțare
1 În cadrul prezentului apel activitățile eligibile și cheltuielile aferente acest
2 Detalii privind rata de cofinanțare, în funcție de tipul de ajutor aplicabil:
3 Pentru proiectele depuse în cadrul prezentului apel, cuantumul cofinanțării acor
4 a) Ajutorul de stat regional
5 Contribuția maximă a programului la cheltuielile eligibile finanțabile prin ajut
6 Tip
7 Intensitatea maximă a ajutorului de stat (%)
8 Alba Brașov
9 Covasna
10 Harghita
11 Mureș
12 Sibiu
13 Întreprindere
14 Micro / Mică 70
15 Mijlocie
16 Întreprinderi 50 mari
17 În cazul în care proiectul conține atât investiții inițiale finanțabile prin aju
18 În cazul proiectelor depuse în parteneriat, rata de co-finanțare mai sus-mențion
19 Pentru toate tipurile de solicitanți eligibili în cadrul acestui apel, încadrare
20 b) Ajutorul de minimis Pentru proiectele depuse în cadrul prezentului apel rata 
21 În conformitate cu prevederile Regulamentului (UE) 2023/2831 al Comisiei din 13 
22 Ajutorul de minimis se acordă: • Solicitant individual/liderul de parteneriat pe
23 Modalitatea de participare a partenerilor la asigurarea cheltuielilor eligibile
[/external_agent_tool_result]

## Asistent

Replace paragraphs 6–16 of section C with a proper table.

## Asistent

[external_agent_tool_call: Edit]
file: C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
The file C:\Users\User\AppData\Local\Temp\claude\--192-168-100-169-Comun-\d0bcea29-fde3-4489-9881-b56f99a0b6ce\scratchpad\make_fisa2.py has been updated successfully.
[/external_agent_tool_result]

## Asistent

[external_agent_tool_call: Bash]
description: Regenerate and verify section C and ending
command: cd "C:/Users/User/AppData/Local/Temp/claude/--192-168-100-169-Comun-/d0bcea29-fde3-4489-9881-b56f99a0b6ce/scratchpad" && F="//192.168.100.169/Comun/00. Proiecte 2026/2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2/FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx" && PYTHONIOENCODING=utf-8 python make_fisa2.py "$F" && PYTHONIOENCODING=utf-8 python -c "
import docx,sys;d=docx.Document(sys.argv[1]);print(len(d.paragraphs),len(d.tables))
t=[p.text for p in d.paragraphs]
i=[k for k,x in enumerate(t) if x.startswith('C. ')][0]
for x in t[i:i+12]: print(x[:100])
for x in t[-15:]: print(x[:100])" "$F"; ls -la "//192.168.100.169/Comun/00. Proiecte 2026/2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2/"
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result]
ok [('A.', 33), ('B.', 136), ('C.', 44), ('D.', 85), ('E.', 91), ('F.', 42), ('G.', 52)]
316 1
C. Reprezentantul legal al Solicitantului individual / al fiecărui membru al parteneriatului care îș
Orice modificare pe parcursul perioadei de evaluare, selecție și contractare asupra situațiilor prev
2. Solicitantul (Solicitantul individual/Membrii parteneriatului) are capacitatea financiară de a im
Solicitantul individual/membrii parteneriatului demonstrează că are/au capacitate financiară de a as
• contribuția proprie declarata în secțiunea aferenta din Cererea de Finanțare; • toate costurile, i
• resursele financiare necesare implementării optime a proiectului în condițiile rambursării ulterio
• cheltuielile de funcționare și întreținere aferente proiectului care includ investiții în infrastr
Solicitantul (Solicitantul individual/Membrii parteneriatului), asigură o contribuție financiară din
La depunerea cererii de finanțare, solicitantul va completa Anexa 2 - Declarație Unică prin care își
În etapa contractuală, solicitantul va prezenta Hotărârea/Decizia de aprobare a proiectului și a sum
Contribuția proprie a solicitantului la valoarea eligibilă a proiectului este în conformitate cu reg
Pentru componentele finanțabile prin ajutor de stat regional, contribuția proprie a solicitantului l
6. Hotărârea/ Decizia de aprobare a proiectului și cheltuielilor legate de proiect în conformitate c
Se va utiliza modelul anexat la Ghidului solicitantului (Anexa 6- Model orientativ Hotărâre de aprob
Contribuția proprie a solicitantului la valoarea eligibilă a proiectului este în conformitate cu reg
7. Certificatele de atestare fiscală ale solicitantului/ partenerilor, dacă este cazul, referitor la
In situația realizării și funcționării interoperabilității cu bazele de date, se va solicita depuner
8. Certificatul de cazier fiscal al solicitantului/partenerilor, daca este cazul
Certificatul de cazier fiscal trebuie să fie în termen de valabilitate.
În situația realizării și funcționarii interoperabilității cu bazele de date, se va solicita depuner
9. Formularul bugetar "Fișa proiectului finanțat/ propus la finanțare în cadrul programelor aferente
10. Formularul 1 – Fișa de fundamentare. Proiect propus la finanțare/ finanțat din fonduri europene 
11. Plan de monitorizare întocmit în corelare cu prevederile din ghidul solicitantului, fiind incluș
Se va utiliza modelul anexat la Ghidului solicitantului (Anexa 17- Planul de monitorizare)
12. Orice alt document din lista celor anexate la formularul cererii de finanțare, actualizat, dacă 
Netransmiterea, în etapa de contractare, a oricărui document obligatoriu, în termenul de 15 zile luc
În situația asigurării interoperabilității cu bazele de date administrate de alte instituții publice
total 112
drwxr-xr-x 1 User 197121     0 Oct  5  2026 .
drwxr-xr-x 1 User 197121     0 Oct  5 15:45 ..
drwxr-xr-x 1 User 197121     0 Oct  5 15:45 0.ARHIVA
drwxr-xr-x 1 User 197121     0 Oct  5 15:45 1. DOCUMENTE OFICIALE
-rw-r--r-- 1 User 197121 45120 Oct  5 15:45 CONDIȚII DE ELIGIBILITATE.docx
-rw-r--r-- 1 User 197121 64639 Oct  5  2026 FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx
[/external_agent_tool_result]

## Asistent

Am făcut fișa completă cu condițiile de eligibilitate pentru firmă, cu textul preluat integral din ghid, nu rezumat:

`\\192.168.100.169\Comun\00. Proiecte 2026\2026.12.21 - SRL ONG UAT - P1 - 1.5.1 Incubatoare si acceleratoare de afaceri - Apel 2\FIȘĂ ELIGIBILITATE SOLICITANT - text complet ghid.docx`

Fișa începe cu un checklist de 13 puncte pentru verificare rapidă. Urmează textul integral din ghid, în ordinea asta:
- **A. Cine poate depune (cap. 5.1.2–5.1.4):** cele 8 tipuri de fondatori și cele 2 forme de parteneriat, plus regulile de parteneriat și încadrarea IMM.
- **B. Condițiile generale ale firmei (cap. 5.1.1):** situațiile de excludere (a–i), inclusiv definiția completă a întreprinderii în dificultate, condițiile pentru reprezentantul legal, capacitatea financiară, cele 8 condiții pentru administratorul incubatorului, dreptul asupra imobilului, durabilitatea și imobilul fără sarcini.
- **C. Intensitatea ajutorului (cap. 3.4):** tabelul pe județe și tipuri de întreprindere (70/60/50% în Alba și Mureș, 60/50/40% în celelalte) și regulile pentru minimis.
- **D. Sectoare și activități excluse (cap. 3.13, a–x):** agricultură primară, pescuit, export, cărbune, oțel, transport, energie, tutun, combustibili fosili, plus regula despre relocare.
- **E. Minimis (cap. 3.13):** definiția întreprinderii unice, plafonul de 300.000 € pe 3 ani și cum se cumulează ajutoarele.
- **F. Documentele firmei la depunere (cap. 7.4)**.
- **G. Documentele firmei la contractare (cap. 7.6):** acte statutare, actul de identitate al reprezentantului legal, dreptul asupra imobilului, hotărârea de aprobare, certificatele de atestare fiscală, cazierul fiscal și planul de monitorizare.

**Ce trebuie să îndeplinească firma:**
1. Să fie fondator eligibil, de exemplu SRL sau SA. Dacă depune singură, trebuie să fie și administratorul incubatorului.
2. Administratorul trebuie numit până la depunere și să aibă personal cu cel puțin 3 ani experiență în juridic, contabilitate, financiar și management.
3. Să dețină dreptul asupra imobilului pentru toată durata proiectului, inclusiv perioada de durabilitate, fără ipotecă, litigii sau revendicări.
4. Să nu fie în insolvență, lichidare sau dificultate și să nu aibă datorii la bugetul de stat sau local.
5. Să nu fi făcut o relocare către locul investiției în ultimii 2 ani.
6. Să poată acoperi contribuția proprie, cheltuielile neeligibile și cheltuielile de funcționare.
7. Ajutoarele de minimis primite de întreprinderea unică în ultimii 3 ani, adunate cu cele din proiect, să nu depășească 300.000 €.
8. Încadrarea ca IMM se calculează împreună cu firmele partenere și legate. O firmă controlată în proporție de 25% sau mai mult de un organism public se consideră întreprindere mare și primește o intensitate a ajutorului mai mică.

Prima fișă, `CONDIȚII DE ELIGIBILITATE.docx` (rezumatul întregului apel), e tot în folder, alături de cea nouă.

## Asistent

[external_agent_tool_call: Bash]
description: Test key-based SSH to 192.168.100.160
command: ls ~/.ssh/ 2>/dev/null; ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new user@192.168.100.160 'hostname; whoami; uname -a' 2>&1 | tail -5
[/external_agent_tool_call]

## Asistent

[external_agent_tool_result: error]
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.
[/external_agent_tool_result]

## Asistent

<EXTERNAL SESSION IMPORTED>
