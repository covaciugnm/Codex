# SDK experimental iFLYTEK Glasses 0.1.0

SDK de cercetare, reconstruit din comportamentul observabil al aplicației oficiale Android. Nu este SDK-ul oficial și nu este încă o soluție autonomă de captură audio de pe ochelari. Biblioteca Java se compilează și funcționează pentru construirea/validarea pachetelor fără aplicația producătorului. Conectarea Bluetooth, negocierea sesiunii și decodarea fluxului audio pe dispozitiv real rămân de integrat și verificat.

## Ce este livrat

- `dist/ifly-glasses-experimental-0.1.0.jar`: bibliotecă Java 8, fără dependențe externe pentru codec/comenzi. Poate fi inclusă într-un proiect Android Java/Kotlin ca JAR; nu este un APK instalabil.
- `src/`: implementarea nouă a codec-ului de cadre, CRC-8, profilului GATT, comenzilor JSON și adaptorului recorderului.
- `evidence/decompiled/`: 86 clase principale/nested de nivel superior exportate din pachetul headset, cu JADX 1.5.6. Nu sunt sursele originale Kotlin și nu sunt tratate drept proiect compilabil.
- `evidence/dependencies/`, `evidence/protocol/`: clase suplimentare urmărite pentru callback, Opus, profil și protocol. Pachetul obfuscat cu numele Alipay nu dovedește că aceste clase aparțin efectiv SDK-ului Alipay.
- `evidence/extracted/`: cele șase DEX și bibliotecile native Opus/Speex/libc++ selectate. Binarele originale sunt păstrate ca dovezi, separat de JAR-ul nou.
- `tests/`, `test-results.txt`: teste de codec, fragmentare, corupere, limite și adaptor prin simularea ABI-ului. Fixture-urile nu intră în JAR.
- `examples/BatteryQuery.java`: produce un cadru de interogare a bateriei, fără a-l transmite.

## Limbajele din APK

| Strat | Dovezi | Concluzie |
|---|---|---|
| Bluetooth | `CoreBluetoothDevice.kt`, `BtGlassPlayer.kt`, `BaseBtRecorder.kt`, `IRecorder.kt` în metadate SMAP/DebugMetadata | Kotlin, compilat în DEX; JADX îl afișează ca Java |
| Unele clase și Opus JNI | `BluePackValueInfo`, `OpusDecoder`, metode native JNI | Java/JVM și punte către cod nativ; fișierul Java decompilat nu dovedește singur limbajul original al fiecărei clase |
| Interfața aplicației | `assets/flutter_assets`, `libflutter.so`, `libapp.so` | Flutter/Dart compilat AOT |
| Audio nativ | `libopus-android.so`, exporturi JNI, simboluri `__cxa_*` și `_ZNSt*` | Cod nativ cu suport C++; nu s-au recuperat sursele originale C/C++ |

SDK-ul nou este Java pentru a fi apelabil din Android/Kotlin, fără dependențe Android la compilarea nucleului. Un port C++ al codec-ului este posibil; nu este inclus în versiunea 0.1.0.

## Utilizare

Includeți JAR-ul în modulul Android, de exemplu `implementation(files("libs/ifly-glasses-experimental-0.1.0.jar"))` în Gradle Kotlin DSL. Biblioteca nu gestionează permisiunile Android sau scanarea BLE.

```java
String json = Commands.query(Commands.BATTERY, 1, 0);
byte[] packet = FrameCodec.json(0, json);
// Transportul aplicației gazdă scrie packet în GlassesProfile.COMMAND_WRITE.
// Activați întâi notificările pentru GlassesProfile.NOTIFY.
FrameCodec.Assembler incoming = new FrameCodec.Assembler();
// În callback-ul transportului:
// for (FrameCodec.Frame f : incoming.accept(bytes)) { ... }
```

`FrameCodec.decode` verifică cadrul complet; `Assembler` gestionează fragmentarea și concatenarea. La un cadru corupt aruncă excepție și golește starea. Nu face resincronizare automată și nu decodează payload-ul audio Opus. Tipurile/subtipurile necunoscute rămân date brute. Lungimea maximă acceptată rezultă din câmpul de 16 biți; nu reprezintă MTU-ul Bluetooth.

Transportul trebuie să respecte MTU-ul negociat și proprietățile caracteristicilor de pe dispozitiv. Valoarea 480 observată în configurația producătorului nu trebuie presupusă drept MTU universal. Alegerea `biz_num`, secvențelor, handshake-ului și ordinea comenzilor trebuie validate față de sesiunea reală; exemplul cu zero este numai generare offline.

### Adaptorul recorderului existent

`RecorderBridge` cere un obiect recorder al producătorului, deja inițializat și conectat, în același proces/classloader. Nu permite unei aplicații externe să acceseze automat obiectele din aplicația iFLYTEK. Nu descarcă/încarcă automat APK-ul și nu înlocuiește bootstrap-ul producătorului.

```java
try (RecorderBridge bridge = new RecorderBridge(existingRecorder,
    (session, type, pcm16le, opus) -> {
        // PCM semnat, little-endian. Tipurile 5 și 6 identifică self/other.
        // Procesați rapid sau transferați către propria coadă audio.
    })) {
    bridge.start("session-from-host", 2, 0, 0);
    // Păstrați bridge-ul deschis pe toată durata capturii.
    bridge.stop("session-from-host");
}
```

Codul de mai sus ilustrează API-ul, nu o aplicație completă. `start` invocă metoda producătorului; succesul se stabilește din callback, nu din revenirea apelului. `close` apelează `release` și eliberează recorderul împrumutat, deci nu îl partajați cu alte funcții ale gazdei. Adaptorul înlocuiește callback-ul existent. Callback-ul utilizatorului trebuie să fie rapid și să nu arunce excepții. ABI-ul este specific APK-ului analizat, putând varia la o actualizare.

## Reconstruire și testare

Rulați `build.ps1` cu JDK 21 (`-Jdk` permite altă locație). Sunt necesare `javac`, `java` și `jar`; nu trebuie Gradle sau Android SDK pentru acest nucleu. Codul este compilat cu `--release 8`.

Validare executată: 40 verificări codec/comenzi, simulare adaptor recorder și exemplu baterie. Nu au fost executate teste pe Android, conectare cu ochelari, captură/decodare Opus live, TTS, rutare către căști ori măsurători de latență.

## Proveniență și limitele extragerii

APK: `https://m.iflytranslate.com/download/android/FY10010010`

SHA-256: `73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2`.

JADX: `https://github.com/skylot/jadx/releases/tag/v1.5.6`.

O parte din nume este obfuscată; unele metode au avertismente și două apar ca nedecompilate în setul headset. Aceste fișiere sunt dovezi de analiză, nu o reconstruire fidelă integrală a proiectului original. Bibliotecile `.so` extrase sunt ARM64 Android, nu DLL-uri Windows. Drepturile componentelor extrase rămân ale titularilor lor; nu sunt incluse sau relicențiate în JAR-ul nou.

Următorul prag tehnic: conectare GATT pe ochelarii reali, captură trafic pentru handshake și verificarea interogării bateriei, apoi start/stop, demultiplexarea audio și Opus. Nu declarăm implementată acea parte pe baza testelor offline.
