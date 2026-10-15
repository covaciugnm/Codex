from pathlib import Path
import json,re,csv
D=Path('D:/00. Downloads/Apartamente Viena/00. Cladire 1 Schallergasse 35, 1120 Wien (Meidling)/04. Firme + Executie/08. Ofertanti electrice/Tongou - Conex Electronic/2026.10.08 Catalog comparativ')
raw=json.loads((D/'Date structurate/2026.10.08 produse-sursa.json').read_text(encoding='utf-8'))
UNKNOWN='? Neprecizat';YES='✓ Da';NO='Nu';NA='— Nu se aplică'
issues={
'43067':['Poli: titlul indică 2P, descrierea 1P+N. Încadrat la 2 poli după titlul comercial, fără echivalare tehnică.','Frecvență Wi-Fi scrisă 2.4Hz în sursă; unitate eronată probabil. De confirmat 2,4 GHz.'],
'43068':['Descrierea enumeră Wi-Fi implicit, Zigbee și 4G personalizare. Numai Wi-Fi este confirmat de titlul acestui SKU; nu sunt trei protocoale simultane.','Frecvență Wi-Fi scrisă 2.4Hz în sursă; unitate eronată probabil.'],
'43073':['Curent: titlul 1–20 A, descrierea 1–40 A. Valoarea corectă necesită confirmare.','Model: descrierea TOQCB2L, fișierul asociat SMR1.pdf. Familia exactă este neconfirmată.'],
'43076':['Fișierul asociat Manual TO-Q-SY2-JWT are altă familie în nume față de TOQCB2 Zigbee. Asocierea necesită confirmare.'],
'43077':['Descriere scurtă 400 V, interval detaliat AC 90–295 V. Poate fi diferența între faze și alimentarea electronicii, dar pagina nu o explică.','Manual asociat numit TO-Q-SY2-JWT pentru un produs TOQCB2 Zigbee; asociere neconfirmată.'],
'43078':['Descriere scurtă 400 V, interval detaliat AC 90–295 V. Referința tensiunilor nu este explicată.','Manual asociat numit TO-Q-SY2-JWT pentru un produs TOQCB2 Zigbee; asociere neconfirmată.'],
'43083':['Titlul TO-Q-SY2-JLT-E, descrierea TO-Q-SY2-JLT fără sufix. Manualul legat de Conex poartă numele TOQCB2; nu confirmă varianta SY2.'],
'43084':['Titlul: disjunctor MCB TOQCB2-JLT-2C63. Descrierea: întrerupător TO-Q-SY2-JLT. Tipul și modelul livrat trebuie confirmate.'],
'43085':['Titlul 4P folosește codul TOQCB2-JLT-2C63, iar descrierea TO-Q-SY2-JLT. Codul 2C63 și familia nu sunt coerente cu identificarea 4P.'],
'43086':['Titlul MCB+RCBO folosește TOQCB2-JLT-2C63 fără L de familie RCBO; descrierea indică TO-Q-SY2-JLT. Modelul exact și protecția diferențială trebuie confirmate.'],
'43087':['Titlul 4P MCB+RCBO folosește TOQCB2-JLT-2C63; descrierea TO-Q-SY2-JLT. Neconcordanțe de model, familie și cod 2C63.'],
'43092':['Conex: RCBO, curba C. Declarația oficială TORD4-63: RCCB. Protecția la supracurent/scurtcircuit nu este confirmată pentru SKU. Nu echivala cu RCBO.']
}
rows=[]
for p in raw:
    sku=p['sku'];name=p['structured']['name'];desc=p['description'];text=p['text'];lower=(name+'\n'+desc).lower()
    smart='smart' in name.lower();spd='SPD' in name;rcbo=('RCBO' in name or sku=='43099') and sku!='43092'
    group='Descărcătoare SPD' if spd else 'Întrerupătoare smart' if name.startswith('INTRERUPATOR') else 'Diferențial RCCB / RCBO de clarificat' if sku=='43092' else 'Disjunctoare diferențiale RCBO' if rcbo else 'Disjunctoare MCB'
    m=re.search(r'([1-4])P\s*\+\s*N',name)
    poles='1P+N' if m else (re.search(r'([1-4])P',name).group(0) if re.search(r'([1-4])P',name) else '1P+N' if '1P+N' in desc else '?')
    sheet=1 if poles=='1P+N' else int(poles[0])
    def find(pattern,default=UNKNOWN,body=desc):
        m=re.search(pattern,body,re.I);return m.group(1).strip(' .,:;') if m else default
    model=find(r'Model:\s*([^\n]+)')
    if model==UNKNOWN:
        model=find(r'\b(TO[A-Z0-9-]*[0-9][A-Z0-9-]*)\b',body=name)
        if model in [UNKNOWN,'TONGOU']:model=find(r'Tip produs:\s*(TO[A-Z0-9-]+)')
    proto='4G/LTE' if '4G' in name else 'Zigbee' if 'ZIGBEE' in name else 'Wi-Fi' if 'WIFI' in name else 'Fără comunicație smart'
    i_delta=('10–100' if sku in ['43073','43082'] else '30–500' if rcbo and smart else 30 if rcbo or sku=='43092' else NA)
    current=NA if spd else ('1–20 / 1–40 (neconcordant)' if sku=='43073' else '1–40' if sku=='43082' else '1–63' if smart else 40 if sku in ['43091','43099'] else 63)
    voltage=find(r'(?:Tensiune nominala|Tensiune de functionare|Interval tensiune de functionare)\s*:?\s*([^\n]+)')
    if spd:voltage=find(r'Tensiune maxima:\s*([^\n]+)')
    technical={
      'Model / serie':model,
      'Configurație în titlu':poles,
      'Configurație în descriere':find(r'(?:Numar poli|Descriere poli)\s*:?\s*([^\n]+)',poles),
      'Tip aparat':('RCBO' if rcbo else 'MCB' if group=='Disjunctoare MCB' else 'RCCB la fabricant; RCBO la Conex' if sku=='43092' else 'SPD DC' if spd and 'DC' in name else 'SPD AC' if spd else 'Întrerupător smart'),
      'Comunicație SKU':proto,
      'Curent nominal / reglaj (A)':current,
      'Curent diferențial (mA)':i_delta,
      'Tensiune declarată (V)':voltage,
      'Frecvență rețea (Hz)':find(r'Frecventa nominala\s*:?\s*([^\n]+)',NA if spd and 'DC' in name else UNKNOWN),
      'Curba de declanșare':find(r'Curba de declansare:\s*([^\n]+)',NA if spd else UNKNOWN),
      'Capacitate de rupere (kA)':find(r'Capacitate de rupere:\s*([^\n]+)',NA if spd else UNKNOWN),
      'Tip diferențial A / AC / B':UNKNOWN if rcbo or sku=='43092' else NA,
      'Protecție la supracurent':YES if 'supracurent' in lower or (not smart and group=='Disjunctoare MCB') or (not smart and rcbo) else NA if spd else UNKNOWN,
      'Protecție la scurtcircuit':YES if 'scurtcircuit' in lower else '✓ Prin tip RCBO/MCB' if not smart and (rcbo or group=='Disjunctoare MCB') else NA if spd else UNKNOWN,
      'Protecție diferențială':YES if rcbo or sku=='43092' else 'Nu (MCB)' if group=='Disjunctoare MCB' and sku not in ['43084','43085'] else NA if spd else UNKNOWN,
      'Protecție la supratensiune susținută':YES if 'supratensiune' in desc.lower() else NA if spd else UNKNOWN,
      'Protecție la subtensiune':YES if 'subtensiune' in lower else NA if spd else UNKNOWN,
      'Protecție la supraputere':YES if 'supraputere' in lower else NA if spd else UNKNOWN,
      'Protecție la temperatură':YES if any(x in lower for x in ['supratemperatura','temperatura terminal','temperatura ridicata']) else NA if spd else UNKNOWN,
      'Prag supratensiune (V)':find(r'Prag (?:setabil pentru |de )supratensiune\s*(?:\(V\))?\s*:?\s*([^\n]+)',NA if not smart else UNKNOWN),
      'Prag subtensiune (V)':find(r'Prag (?:setabil pentru |de )subtensiune\s*(?:\(V\))?\s*:?\s*([^\n]+)',NA if not smart else UNKNOWN),
      'Prag supracurent (A)':find(r'Prag (?:setabil pentru |de )supracurent\s*(?:\(A\))?\s*:?\s*([^\n]+)',NA if not smart else UNKNOWN),
      'Prag supraputere (W)':find(r'Prag (?:setabil pentru |de )supraputere\s*(?:\(W\))?\s*:?\s*([^\n]+)',NA if not smart else UNKNOWN),
      'Prag temperatură terminal (°C)':find(r'Prag (?:setabil pentru |de )temperatura terminal\s*(?:\(℃\))?\s*:?\s*([^\n]+)',NA if not smart else UNKNOWN),
      'Wi-Fi':YES if proto=='Wi-Fi' else 'Nu (varianta SKU)',
      'Zigbee':YES if proto=='Zigbee' else 'Nu (varianta SKU)',
      '4G / LTE':YES if proto=='4G/LTE' else 'Nu (varianta SKU)',
      'Cartelă SIM necesară':YES if proto=='4G/LTE' else NA,
      'Gateway Zigbee':YES if 'Gateway Zigbee' in desc else '? De confirmat' if proto=='Zigbee' else NA,
      'Comandă de la distanță':YES if smart and ('remote' in lower or 'telecomanda' in lower or 'de la distanta' in lower) else '? Smart, mod neprecizat' if smart else NO,
      'Comandă manuală':YES if 'manual' in desc.lower() or (not smart and not spd) else NA if spd else UNKNOWN,
      'Măsurare putere / consum':YES if any(x in lower for x in ['power meter','masurare','consum de energie','cu contor']) else UNKNOWN if smart else NO,
      'Temporizare':YES if 'temporiz' in lower else UNKNOWN if smart else NO,
      'Numărătoare inversă / buclă':YES if 'numaratoare inversa' in lower else UNKNOWN if smart else NO,
      'Scenarii smart':YES if 'scenarii' in lower else UNKNOWN if smart else NO,
      'Reînchidere automată':YES if 'reinchidere' in lower else UNKNOWN if smart else NO,
      'Aplicație / cloud':find(r'Aplicatie\s+([^\n]+)', 'Tuya Cloud' if 'Tuya Cloud' in desc else UNKNOWN if smart else NA),
      'Home Assistant / Zigbee2MQTT':YES if 'Home Assistant' in desc else UNKNOWN if smart else NA,
      'Asistenți vocali':find(r'Suport vocal\s+([^\n]+)',UNKNOWN if smart else NA),
      'Sisteme de operare':find(r'Sistem de operare\s*:?\s*(?:compatibil|suportat)?\s*([^\n]+)',UNKNOWN if smart else NA),
      'Limba aplicației':find(r'Limba (?:aplicatie|de operare)\s*[:;]?\s*([^\n]+)',UNKNOWN if smart else NA),
      'Montaj': 'Șină DIN' if 'sina DIN' in desc else UNKNOWN,
      'Grad de protecție':find(r'Grad de protectie:\s*([^\n]+)'),
      'Standarde declarate':find(r'Standard:\s*([^\n]+)'),
      'Protecție impulsuri SPD':YES if spd else '? Nu este indicat SPD',
      'Curent descărcare nominal/maxim (kA)':find(r'Curent descarcare nominal/maxim:\s*([^\n]+)',NA),
      'Distanță între eclatoare (mm)':find(r'Distanta intre eclatori:\s*([^\n]+)',UNKNOWN if spd else NA),
      'Greutate (kg)':p['structured'].get('weight',{}).get('value',UNKNOWN),
      'Preț cu TVA (RON)':p['structured']['offers']['price'],
      'Status stoc':'STOC EPUIZAT' if p['stock_qty']==0 else 'În stoc',
      'Cantitate disponibilă (buc.)':p['stock_qty'] if p['stock_qty'] is not None else UNKNOWN,
      'PN Conex':find(r'PN:\s*(\d+)',body=text),
      'EAN':p['structured'].get('gtin13',UNKNOWN)
    }
    if sku in ['43084','43085','43086','43087']:
        technical['Model / serie']='TOQCB2-JLT-2C63 în titlu / TO-Q-SY2-JLT în descriere'
        technical['Protecție la scurtcircuit']='? Tip/model neconcordant'
    if sku in ['43086','43087']:technical['Protecție diferențială']='✓ Declarată; model de confirmat'
    if sku=='43092':
        technical['Protecție la supracurent']='? RCBO/RCCB neconcordant'
        technical['Protecție la scurtcircuit']='? RCBO/RCCB neconcordant'
        technical['Curba de declanșare']='C la Conex; neconfirmată'
    obs=issues.get(sku,[]).copy()
    if p['files']:obs.append('Linkurile PDF Conex sunt indisponibile (HTTP 404). Vezi Documentație pentru fișiere oficiale alternative.')
    elif not spd:obs.append('Pagina Conex nu publică un fișier tehnic asociat pentru acest SKU.')
    if sku=='43082':obs.append('Funcțiile omise din descrierea Conex rămân „?” în matrice; manualul de familie este salvat separat.')
    if sku in ['43097','43098']:obs.append('SPD DC: nu se compară ca înlocuitor al variantei AC. Tensiunea DC și curentul de descărcare sunt distincte.')
    if sku=='43074':obs.append('Stoc epuizat: 0 bucăți. Prețul este cel afișat, fără disponibilitate pentru comandă imediată.')
    rows.append(dict(sku=sku,name=name,poles=poles,sheet=sheet,group=group,smart=smart,spd=spd,rcbo=rcbo,technical=technical,observations=obs,issues=issues.get(sku,[]),source=p['url'],source_text=p['text'],description=p['description'],files=p['files'],stock_source=p['stock_source']))
assert len(rows)==29 and len({p['sku'] for p in rows})==29
(D/'Date structurate/2026.10.08 produse-normalizate.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (D/'Date structurate/2026.10.08 caracteristici.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Data','SKU','Denumire','Grupă','Poli','Caracteristică','Valoare','Sursă'])
    for p in rows:
        for key,value in p['technical'].items():w.writerow(['2026.10.08',p['sku'],p['name'],p['group'],p['poles'],key,value,p['source']])
print('STRUCTURAT',len(rows),'produse', {i:sum(p['sheet']==i for p in rows) for i in range(1,5)})
