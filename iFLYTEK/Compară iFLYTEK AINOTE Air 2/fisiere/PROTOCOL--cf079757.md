# Protocol observat în APK

Constatările se aplică configurației `DeviceType.GLASSES` din APK-ul cu SHA-256 din README. Nu există încă validare pe XF-AIGlasses-01 fizic.

## GATT

| Rol | UUID |
|---|---|
| Serviciu | `434f544f-5250-5050-414b-4554594c4669` |
| Scriere comenzi | `00006001-0000-1000-8000-00805f9b34fb` |
| Notificări | `00006002-0000-1000-8000-00805f9b34fb` |
| Scriere audio în configurație | aceeași caracteristică `6002` |

Sursa: `evidence/protocol/.../l04.java`, interfața `bm7` și apelul `zb0.K1`, respectiv `CoreBluetoothDevice` la înregistrarea notificărilor. Proprietățile reale ale caracteristicilor trebuie citite din dispozitiv.

## Cadru de comandă JSON

| Offset | Octeți | Sens |
|---|---|---|
| 0 | 4 | `AA FF 55 00` |
| 4 | 4 | zero în builderul observat |
| 8 | 1 | versiune: `01` pentru configurația ochelarilor |
| 9 | 1 | opCode: `01` request; `02` response, `03` indication, `04` notification |
| 10 | 2 | secvență uint16 little-endian |
| 12 | 2 | lungime payload + 3, uint16 little-endian |
| 14 | 1 | moduleID: `01` pentru comenzi JSON |
| 15 | 1 | msgID: `01` la comenzile JSON observate |
| 16 | N | JSON UTF-8 |
| 16+N | 1 | CRC-8, polinom `0x07`, init 0, fără reflexie/xor final |

CRC acoperă toate datele dinaintea ultimului octet. Total: N+17. Sursa: `zb0.b`, `zb0.w1`, `zb0.s1`, `hm7.a`, `ml0.e`, constante `aa4.X3/Y3`. Schema detaliată de mai sus este pentru comenzi JSON; payload-ul binar audio are câmpuri suplimentare.

## Comenzi implementate

Fiecare JSON conține `opt`, `optNum`, `biz_num`. Aceste ID-uri trebuie corelate de aplicația gazdă; nu sunt o autentificare.

| opt | Funcție | Parametri suplimentari |
|---|---|---|
| 62001 | Informații sistem | — |
| 62002 | Versiune | — |
| 62003 | Baterie | — |
| 62201 | Start captură/traducere | `translationScene`, `multiModeSwitch`, `compressionRatio` |
| 62202 | Stop | `translationScene` opțional pentru ochelari |

Surse: `zb0.o0`, `zb0.r0`, switch-ul `ff0.B`, `zb0.f1`, `zb0.j1` și `CoreBluetoothDevice.k2`. Setările original/traducere sunt expuse prin `RecorderBridge`; nu au builder independent în această versiune.

## Audio și adaptor

- `BtGlassRecorder.i` livrează PCM și Opus opțional prin `kh4.onData(session, AudioType, yw)`.
- `yw.e()` returnează PCM; `yw.f()` returnează Opus opțional.
- `CoreBluetoothDevice.P4` creează decodor Opus 16000 Hz mono; `R4` are și o cale stereo, 16000 Hz. Nu presupunem că orice callback are mereu două canale sau mereu unul.
- `OpusDecoder.j` convertește `short[]` în PCM little-endian: 16 biți semnați.
- Tipuri: 0 default, 1 left ear, 2 right ear, 3 near end, 4 far end, 5 glass self, 6 glass other. Sunt tipuri semantice, nu neapărat canale fizice separate ale microfoanelor.
- `BtGlassRecorder.m` = start; `.j` = înregistrare callback moștenită; `stop`, `release`, `setOriginalEnable`, `setTranslateEnable` au nume păstrate.

Nu este reconstruită încă integral secvența de conectare, handshake și starea transcrierii. Prezența constructorilor pentru Opus nu dovedește latența, calitatea sau disponibilitatea offline a întregului flux.


## Clarificare după analiza integrală

Denumirile channel/payloadType/subtype din API-ul experimental corespund câmpurilor opCode/moduleID/msgID din protocol. Configurația declară caracteristica audio 6002, însă traseul zb0.L1 analizat trimite audio pe caracteristica de comandă 6001. Valorile sequenceId și optNum au contoare separate. biz_num este inițial -1 în constructorul vendor și poate fi înlocuit de coada de comenzi; valoarea 0 din exemple este aleasă pentru test. Raportul extins este în APK_Reconstituit_2026-10-30/protocol-comunicare/INDEX.html.

