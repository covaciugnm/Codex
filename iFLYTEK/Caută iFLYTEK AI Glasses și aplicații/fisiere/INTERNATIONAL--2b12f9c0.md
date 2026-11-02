# SUA / UE: traseul internațional identificat și limitele confirmării

Verificare publică și statică la 1 noiembrie 2026. Obiectivul este identificarea aplicației, contului și serviciilor pentru utilizatori internaționali, păstrând distinctă compatibilitatea cu ochelarii XF-AIGlasses-01.

## Există un cont internațional cu e-mail

În APK-ul Bavvo 1.0.1222 deja arhivat au fost confirmate, prin citirea bibliotecii originale verificate după SHA-256:

| Componentă | Adresă / indiciu |
|---|---|
| Cont internațional | `https://account-ap1.iflyoversea.com` |
| Interfață web a contului | `https://account-h5-ap1.iflyoversea.com` |
| Servicii de traducere internaționale | `https://transsaas-api-ap1.iflyoversea.com` |
| Interfață web Bavvo | `https://transsaas-h5-ap1.iflyoversea.com` |
| Servicii hardware | `https://hardware-ap1.iflyoversea.com` |
| Cod de interfață / flux e-mail | `BVEmailInputView`, `sendEmailRegisterCode`, `submitEmailRegister`, `_emailPasswordLogin`, `loginByEmailPassword` |

Codul JavaScript public al [paginii internaționale de cont](https://account-h5-ap1.iflyoversea.com/pass/mobile/?lang=en) include înregistrare prin e-mail, verificarea codului e-mail și autentificarea prin e-mail/parolă: `/register/email/sendCode`, `/register/email/checkCode`, `/register/email/submitPwd`, `/login/email/submitPwd`.

[Dovezile exacte și hashurile surselor](international-login-evidence.json) · [JavaScript oficial arhivat](sources/international-account-app.js). Nu s-au apelat aceste operații și nu s-a efectuat o autentificare. Prezența codului și adreselor confirmă existența componentelor internaționale; funcționarea pentru un anumit cont și asocierea cu un anumit model necesită o confirmare suplimentară.

[Pagina oficială Bavvo](https://www.iflytek.com/en/products/translator/bavvo.html) identifică produsul internațional. APK/XAPK-urile Bavvo sunt deja în [colecția precedentă](../collection-2026-11-01/README.md); nu au fost încărcate din nou.

Pachetul Android global deja păstrat este [Bavvo 1.0.1222 — XAPK](https://github.com/covaciugnm/iFLYTEK/releases/download/iflytek-software-2026-11-01/bavvo-1.0.1222.xapk), `com.iflytek.bavvo`, SHA-256 `2b314f265da6a916cbfcc930d18183b36272d0e1180b93ca53c89c787eeb9bfd`. Este un candidat concret pentru traseul internațional de cont; compatibilitatea sa cu XF-AIGlasses-01 rămâne neconfirmată.

## Ce arată verificarea magazinelor iOS

API-ul public Apple a fost interogat pentru același identificator Bavvo `6757071464` în toate cele **27 de țări UE**, plus UK și SUA:

- SUA: aplicația `Bavvo - AI Translator`, `com.iflytek.bavvo`, versiunea iOS 1.0.1191, a fost returnată.
- Cele 27 de țări UE și UK: `resultCount: 0` la momentul verificării. Italia a avut inițial HTTP 500, apoi răspuns 200 cu zero rezultate la reîncercare.
- Căutările Apple separate după numele Bavvo în România, Germania și UK nu au identificat o altă listare Bavvo.

[Toate interogările și rezultatele pe țări](eu-app-availability.json) · [Căutările după nume](regional-apple-search.json) · [Răspuns SUA](sources/bavvo-ios-us.json).

Acestea sunt observații ale API-ului iOS, nu o dovadă privind disponibilitatea APK-ului Android, eligibilitatea unui anumit dispozitiv sau o interdicție permanentă de utilizare. Nu permit afirmarea că există deja un APK distinct pentru UE sau că un cont internațional va fi acceptat de aplicația chinezească.

Pentru Android, [pagina Google Play Bavvo cu parametrul de țară România](https://play.google.com/store/apps/details?id=com.iflytek.bavvo&hl=en&gl=RO) a răspuns HTTP 200 și a returnat date structurate pentru `Bavvo - AI Translator`, platforma Android. [Observația exactă](google-play-ro-observation.json) confirmă listarea publică; nu este un test de instalare autentificat, eligibilitate a telefonului sau asociere cu ochelarii. APK/XAPK-urile globale deja descărcate pot fi consultate în colecția precedentă.

Pentru aplicația chinezească `讯飞翻译`, ID `6739250870`, răspunsul CN returnează `com.iflytek.translateapp`, iOS 1.0.3741; interogările SUA și România au returnat zero rezultate. Formularul web chinezesc analizat anterior prezintă +86/+852/+853, conform [raportului SMS precedent](../retailer-audit-2026-11-01/SMS-LOGIN-SERVICES.md).

## Distribuția hardware nu este încă demonstrată până la activare

Producătorul a prezentat ochelarii pentru utilizare internațională la [MWC 2026](https://www.iflytek.com/en/news-events/mwc2026.html) și [IFA 2026](https://www.iflytek.com/en/news-events/news/343.html). Comunicatul IFA descrie și extinderea viitoare a vânzărilor și serviciilor locale în Europa. Sursele colectate nu oferă o procedură verificabilă de activare XF-AIGlasses-01 cu număr românesc sau o confirmare explicită că acesta se asociază cu Bavvo.

O ofertă cu preț în GBP/EUR sau livrare internațională trebuie corelată cu modelul/SKU, aplicația indicată și contul acceptat. [Auditul comercianților](../retailer-audit-2026-11-01/README.md) păstrează ofertele și instrucțiunile găsite. Până la identificarea unei oferte cu instrucțiuni concrete, conexiunea dintre traseul internațional Bavvo și exemplarul utilizatorului rămâne neconfirmată. Nu a fost testată asocierea Bluetooth, cloudul sau funcționarea pe ochelari.

## CLI-ul și HeyCyan sunt piste distincte

Skillul oficial confirmă autorizarea CLI prin browser (`transaas login --web`) și SMS. Autorizarea prin browser folosește un cont acceptat de platformă; nu elimină cerințele contului. Binarele descărcate includ adresele platformei chinezești. Nu este demonstrat că acceptă automat sesiunea internațională Bavvo sau că activează ochelarii.

Pentru alte familii de ochelari, [ghidul vânzătorului POV One](https://povoneglasses.com/pages/support) indică HeyCyan și descrie folosirea fără creare de cont. Listările Apple HeyCyan au fost returnate atât pentru SUA, cât și pentru România; [răspuns RO](sources/heycyan-ios-ro.json). Acest lucru nu confirmă compatibilitatea HeyCyan cu XF-AIGlasses-01. Pachetul și manualele au fost arhivate separat pentru a păstra această distincție.

Concluzia susținută de dovezi: **există infrastructură internațională și un flux de cont prin e-mail; nu este încă verificată soluția completă de activare pentru modelul de ochelari al utilizatorului în UE.**
