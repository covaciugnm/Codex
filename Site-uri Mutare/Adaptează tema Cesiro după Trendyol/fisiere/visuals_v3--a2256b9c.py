from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random

O=Path(__file__).parent/'visuals-v3'; O.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/calibri.ttf'; BOLD='C:/Windows/Fonts/calibrib.ttf'; SERIF='C:/Windows/Fonts/cambria.ttc'
def font(n,b=False,serif=False):return ImageFont.truetype(SERIF if serif else (BOLD if b else FONT),n)
W,H=1500,1730
def txt(d,x,y,t,n=30,fill='#232526',b=False,serif=False):d.text((x,y),t,font=font(n,b,serif),fill=fill,spacing=10)
def wrap(d,x,y,t,width,n=30,fill='#232526',b=False):
    words=t.split();line='';yy=y
    for w in words:
        test=line+' '+w if line else w
        if d.textlength(test,font=font(n,b))>width:
            txt(d,x,yy,line,n,fill,b);yy+=int(n*1.35);line=w
        else:line=test
    txt(d,x,yy,line,n,fill,b);return yy+int(n*1.35)
def plate(d,x,y,r,col,inner='#F2ECE1'):
    d.ellipse((x-r+9,y-r+13,x+r+9,y+r+13),fill='#D1CCC1')
    d.ellipse((x-r,y-r,x+r,y+r),fill=col)
    for f in [.88,.82]:d.ellipse((x-r*f,y-r*f,x+r*f,y+r*f),outline=inner,width=3)
    d.ellipse((x-r*.68,y-r*.68,x+r*.68,y+r*.68),fill=inner)
def pill(d,box,t,color='#365A4A',textcol='white',n=30):
    d.rounded_rectangle(box,18,fill=color)
    bb=d.textbbox((0,0),t,font=font(n,True)); x=(box[0]+box[2]-(bb[2]-bb[0]))/2;y=(box[1]+box[3]-n)/2-2
    txt(d,x,y,t,n,textcol,True)
def mood(i,title,colors,tag,sub):
    im=Image.new('RGB',(W,H),colors[0]);d=ImageDraw.Draw(im)
    txt(d,65,48,f'CONCEPT 0{i}',25,colors[1],True)
    txt(d,65,110,title,67,colors[1],serif=True)
    txt(d,65,205,tag,29,colors[1])
    d.rectangle((65,295,1435,1015),fill=colors[4])
    if i==1:
        for k in range(18):
            d.arc((140+k*7,385+k*4,855-k*7,950-k*4),0,360,fill=colors[2],width=2)
        plate(d,550,630,245,colors[2],colors[0]);plate(d,1090,700,190,colors[3],colors[0])
        txt(d,950,340,'LUT / FORMĂ',24,colors[1],True)
        txt(d,950,380,'GLAZURĂ / LUMINĂ',24,colors[1],True)
    elif i==2:
        d.rounded_rectangle((150,365,1360,960),80,fill=colors[0])
        for x,y,c in [(430,585,colors[2]),(1065,585,colors[3]),(745,815,colors[2])]:plate(d,x,y,155,c,colors[0])
        for x in [200,1265]:d.line((x,465,x,835),fill=colors[1],width=8)
        txt(d,620,400,'ACASĂ',22,colors[1],True)
    else:
        d.rectangle((65,295,750,1015),fill=colors[2]);d.rectangle((750,295,1435,1015),fill=colors[3])
        plate(d,460,660,245,colors[0],colors[4]);plate(d,1120,655,170,colors[1],colors[0])
        txt(d,850,350,'FORME SIMPLE',29,colors[0],True)
        txt(d,850,395,'DECOR DISTINCT',29,colors[0],True)
    for k,c in enumerate(colors):
        x=65+k*280;d.rectangle((x,1070,x+240,1160),fill=c,outline='#B0ADA7',width=1)
        txt(d,x,1177,c.upper(),25,colors[1])
    txt(d,65,1260,'CESIRO',50,colors[1],serif=True)
    wrap(d,65,1335,sub,820,33,colors[1])
    pill(d,(1005,1290,1435,1375),'Vezi colecțiile',colors[1])
    txt(d,1010,1410,'Titluri serif • text clar',24,colors[1])
    txt(d,1010,1452,'Spațiu generos • focus vizibil',24,colors[1])
    txt(d,65,1580,'ILUSTRAȚII DE DIRECȚIE VIZUALĂ',22,colors[1],True)
    txt(d,65,1625,'Fotografiile reale și glazurile se validează în producția de conținut.',25,colors[1])
    im.save(O/f'plan-{i}.png')
mood(1,'Atelier și glazură',['#F2E9DE','#4B372E','#AE6848','#85927C','#DBCCB9'],'Origine verificabilă și materialitate','Povestea fabricii însoțește produsul. Texturile de lut și detaliile de glazură construiesc încredere fără să încarce navigarea.')
mood(2,'Masa de acasă',['#F5F0E6','#304A3E','#C68866','#95A799','#E1D6C4'],'Utilizare, oameni și ocazii de cumpărare','O masă pentru fiecare zi. Clientul începe de la ocazie, număr de persoane sau decor și poate completa doar piesele care îi lipsesc.')
mood(3,'Colecția contemporană',['#F3EFE7','#252D42','#B55E4D','#7387A3','#DDD5C7'],'Culoare și compoziție grafică','Colecțiile devin ușor de recunoscut. Culoarea atrage atenția, iar etichetele, filtrele și informațiile de produs susțin alegerea.')

def base(title,subtitle):
    im=Image.new('RGB',(W,H),'#F4F5F6');d=ImageDraw.Draw(im)
    txt(d,65,40,title,48,b=True);txt(d,65,110,subtitle,28)
    d.rounded_rectangle((70,195,805,1640),50,fill='white',outline='#68747D',width=3)
    for yy in [242,252,262]:d.line((110,yy,137,yy),fill='#232526',width=3)
    txt(d,155,230,'CESIRO',36,b=True);txt(d,620,235,'Coș 0',30)
    d.line((95,295,780,295),fill='#D4DADD',width=2)
    return im,d
def note(d,y,num,title,t):
    d.ellipse((870,y,921,y+51),fill='#304A3E');txt(d,885,y+7,str(num),27,'white',True)
    txt(d,945,y,title,32,b=True);wrap(d,945,y+50,t,480,28)
im,d=base('Homepage mobil','Ordine de conținut propusă • reper de proiectare 390 px')
d.rounded_rectangle((110,320,765,390),10,fill='#EFF1F2');txt(d,135,335,'Caută produs, decor sau ocazie',30)
txt(d,110,430,'O masă pentru',52,serif=True);txt(d,110,492,'fiecare zi',52,serif=True)
d.rectangle((110,585,765,875),fill='#E1D6C4');plate(d,320,725,105,'#95A799');plate(d,580,735,88,'#C68866')
pill(d,(110,905,765,985),'Compune masa ta')
txt(d,110,1025,'Cu ce ocazie alegi?',35,b=True)
for x,y,t in [(110,1090,'Zi de zi'),(445,1090,'Cadou'),(110,1190,'Prima casă'),(445,1190,'În familie')]:pill(d,(x,y,x+320,y+78),t,'#EEE9DF','#232526')
txt(d,110,1310,'Completează decorul tău',35,b=True)
for x,c in [(180,'#95A799'),(380,'#C68866'),(580,'#7387A3')]:plate(d,x+20,1440,61,c)
txt(d,110,1540,'Colecții   •   Cadouri   •   Pro / HoReCa',27)
note(d,350,1,'Căutare la îndemână','Aceeași intrare pentru SKU, decor, tip de produs și utilizare.')
note(d,630,2,'O singură acțiune','Configurare după persoane și buget, fără carusel obligatoriu.')
note(d,965,3,'Intenții de cumpărare','Ocaziile completează categoriile fizice. El și ea rămân filtre opționale în cadouri.')
note(d,1300,4,'Completare de serie','Decor exact când există dovadă; alternativa este numită explicit.')
im.save(O/'plan-4.png')
im,d=base('Produs mobil','Prioritate pentru identificare, preț și decizie')
txt(d,110,325,'Căni și cești / Decor G242',27)
d.rectangle((110,390,765,800),fill='#F2ECE1');plate(d,430,600,157,'#AE6848')
txt(d,145,744,'Galerie și scară reală',25)
txt(d,110,830,'Ceașcă cu farfurioară',38,b=True);txt(d,110,885,'220 ml • decor verificat',29)
txt(d,110,950,'Preț din catalog',40,b=True);txt(d,110,1010,'Disponibilitate și livrare actualizate',26)
pill(d,(110,1070,765,1155),'Adaugă în coș')
for y,t in [(1200,'Componente și dimensiuni'),(1290,'Producător și siguranță'),(1380,'Îngrijire și documente'),(1470,'Completează decorul tău')]:
    txt(d,110,y,t,31,b=True);d.line((110,y+60,765,y+60),fill='#D4DADD',width=2)
note(d,390,1,'Imagini fidele','Fotografii reale, detalii de glazură și obiect la scară. Ilustrația din schiță nu este fotografie de produs.')
note(d,820,2,'Date verificabile','Capacitatea aparține piesei. Materialul și originea au surse, iar necunoscut nu înseamnă zero.')
note(d,1120,3,'Acțiune accesibilă','Total și livrare explicite. Stocul și prețul sunt reverificate de backend.')
note(d,1400,4,'Dovezi la vedere','Informațiile obligatorii sunt accesibile înainte de cumpărare; documentele nu înlocuiesc etichetele relevante.')
im.save(O/'plan-5.png')
im,d=base('Masa completă mobil','Compoziție 2D și alternativă accesibilă prin listă')
txt(d,110,325,'Pentru câte persoane?',36,b=True)
for k,t in enumerate(['2','4','6','8']):pill(d,(110+k*170,390,255+k*170,460),t,'#304A3E' if t=='4' else '#EEE9DF','white' if t=='4' else '#232526')
txt(d,110,500,'Decor / buget / ce ai deja',28)
d.rounded_rectangle((110,560,765,940),35,fill='#E1D6C4')
for x,y,c in [(290,670,'#95A799'),(590,670,'#95A799'),(290,830,'#C68866'),(590,830,'#C68866')]:plate(d,x,y,65,c)
txt(d,110,980,'Piesele mesei tale',35,b=True)
for y,t in [(1050,'Farfurii întinse'),(1150,'Boluri'),(1250,'Căni')]:
    txt(d,115,y,t,31);pill(d,(510,y-3,750,y+62),'−   4   +','#EEE9DF','#232526',29)
txt(d,110,1380,'Total calculat din catalog',31,b=True)
pill(d,(110,1450,765,1540),'Adaugă piesele în coș')
note(d,340,1,'Cantități explicite','Persoanele ajustează rolurile și piesele. Seturile comerciale rămân distincte.')
note(d,650,2,'Vizual și fidel','Decupaje fotografice aprobate. Produsele indisponibile sunt semnalate înainte de confirmare.')
note(d,1010,3,'Listă accesibilă','Același rezultat prin butoane și tastatură. Actualizările cantităților sunt anunțate cititorului de ecran.')
note(d,1370,4,'Total server','Preț, TVA și cantități reverificate. Fără substituirea tacită a decorului sau a materialului.')
im.save(O/'plan-6.png')
print('6 planșe salvate')
