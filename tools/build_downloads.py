"""Build the four A4 download resources; needs reportlab and Pillow."""
from pathlib import Path
from io import BytesIO
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'downloads'
OUT.mkdir(exist_ok=True)
FONT = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('Body', str(FONT/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Bold', str(FONT/'DejaVuSans-Bold.ttf')))
INK = colors.HexColor('#202723')
MUTED = colors.HexColor('#59675e')
ACCENT = colors.HexColor('#925e3b')
LINE = colors.HexColor('#ccd3c9')
SOFT = colors.HexColor('#f2f1eb')
W,H=A4
M=43
WIDTH=W-M*2
LOGO=ROOT/'assets/helfernetz-logo-telefon.webp'
logo_bytes=BytesIO()
Image.open(LOGO).convert('RGB').save(logo_bytes,format='JPEG',quality=75,optimize=True)
logo_bytes.seek(0)
LOGO_PDF=ImageReader(logo_bytes)
STYLE=ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=15.4,textColor=INK)


def text(c, value, x, y, size=10, font='Body', color=INK):
 c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,value)

def para(c, value, x, top, width=WIDTH, size=10.2, color=INK, leading=None):
 style=ParagraphStyle('paragraph',parent=STYLE,fontSize=size,leading=leading or size*1.4,textColor=color)
 p=Paragraph(value,style);_,height=p.wrap(width,1000);p.drawOn(c,x,top-height)
 return top-height

def header(c, category):
 c.drawImage(LOGO_PDF,M,H-86,56,56,mask='auto',preserveAspectRatio=True)
 text(c,'KLEINES HELFERNETZ',M+70,H-46,10,'Bold')
 text(c,'Berlin-Brandenburg · Team Köpenick',M+70,H-63,9,color=MUTED)
 text(c,'Notfallkontakt: 030 81451625',M+70,H-80,9,'Bold')
 c.setStrokeColor(LINE);c.line(M,H-101,W-M,H-101)
 text(c,category,M,H-124,8,'Bold',ACCENT)

def footer(c):
 c.setStrokeColor(LINE);c.line(M,47,W-M,47)
 text(c,'HELFERNETZ · TEAM KÖPENICK',M,31,7,'Bold',MUTED)
 text(c,'Suchhilfe · Stand Oktober 2026',W-219,31,7,color=MUTED)

def doc(name,title,subtitle):
 c=canvas.Canvas(str(OUT/name),pagesize=A4)
 c.setTitle(title);c.setAuthor('Kleines Helfernetz · Team Köpenick');c.setSubject('Suchhilfe für vermisste Katzen')
 header(c,'WISSEN FÜR DIE SUCHE')
 y=para(c,title,M,H-142,size=27,leading=30)
 y=para(c,subtitle,M,y-14,size=10.5,color=MUTED)-18
 return c,y

def block(c,y,title,body):
 y=para(c,title,M,y,size=12,leading=16)-6
 y=para(c,body,M,y,size=9.8)-13
 return y

def note(c,y,title,body):
 p=Paragraph(body,ParagraphStyle('note',parent=STYLE,fontSize=9.8,leading=14))
 _,h=p.wrap(WIDTH-30,1000)
 c.setFillColor(SOFT);c.rect(M,y-h-43,WIDTH,h+43,fill=1,stroke=0)
 text(c,title,M+15,y-19,11,'Bold',ACCENT)
 p.drawOn(c,M+15,y-h-31)
 return y-h-56

def finish(c,y):
 assert y>57, f'Content reaches footer: {y}'
 footer(c);c.showPage();c.save()

c,y=doc('nachtsuche.pdf','Katze entlaufen?\nSo suchst du richtig.'.replace('\n','<br/>'),'Besonders in der Nacht: Ruhe, Geduld und genaues Hinsehen.')
y=block(c,y,'Direkt am Entlaufort beginnen','Wohnungskatzen verstecken sich häufig ganz in der Nähe und bleiben aus Angst still - auch wenn vertraute Menschen direkt vor ihnen stehen. Kontrolliere Verstecke gründlich. Verlasse dich nicht allein darauf, dass die Katze auf Rufen reagiert.')
y=block(c,y,'Ruhige Zeiten nutzen','Suche zum Beispiel zwischen 22 und 2 Uhr oder vor Sonnenaufgang. Gehe langsam, rufe leise, bleibe stehen und lausche. Nimm Rücksicht auf die Nachtruhe.')
for item in [
 'Taschenlampe und Warnweste oder sichtbare Kennzeichnung als Katzensuchteam mitnehmen.',
 'Unter Autos, in Hecken, Kellerschächten, Garagen, Schuppen und Gartenhäusern nachsehen.',
 'Nachbarn bitten, Verstecke zu kontrollieren. Fremde Grundstücke nur mit Erlaubnis betreten.',
 'Wenige geschützte Futterstellen beobachten. Eine Wildkamera zeigt, welches Tier dort frisst.',
 'Jede Sichtung mit Ort, Uhrzeit, Merkmalen und Laufrichtung notieren.'
]:
 c.setStrokeColor(MUTED);c.rect(M,y-12,9,9,fill=0,stroke=1)
 y=para(c,item,M+22,y,WIDTH-22,size=9.8)-7
y-=8
y=note(c,y,'Gesichtet? Nicht hinterherlaufen.','Nicht verfolgen, einkreisen oder durch hektische Suchaktionen verscheuchen. Standort notieren und die Sicherung gezielt mit dem Helferteam vorbereiten.')
y=para(c,'Für weitere Runden kann eine ruhige Suche von außen zum Haus sinnvoll sein. Das ist eine mögliche Taktik, keine allgemeingültige Regel.',M,y,size=9,color=MUTED)-12
finish(c,y)

c,y=doc('heimwegschleppe.pdf','Vertrauter Geruch.<br/>Ein Weg nach Hause.','Heimwegschleppe mit getragenem Kleidungsstück; optionale Urinvariante.')
y=note(c,y,'Erst die unmittelbare Umgebung absuchen.','Eine Geruchsspur ist eine mögliche Ergänzung. Sie ersetzt weder die ruhige Suche in Verstecken noch Sichtungsmeldungen. Es gibt keine Erfolgsgarantie.')
y=block(c,y,'Vorbereiten','Nutze ein stark getragenes T-Shirt der engsten Bezugsperson, möglichst mindestens 24 Stunden getragen. Dazu: eine Schnur und eine verschließbare Tüte. Das Kleidungsstück bleibt bis zum Startpunkt in der Tüte.')
y=block(c,y,'Sichere Wege abstimmen','Wähle mit dem Helferteam eine Strecke, die von außen zum Zuhause oder passenden Entlaufort führt. Entfernung und Route hängen von Katze, Sichtungen und Umgebung ab. Nicht über Bahngleise oder stark befahrene Straßen führen. Fremde Grundstücke nur mit Erlaubnis betreten.')
y=block(c,y,'Die Spur Richtung Zuhause legen','Nimm das T-Shirt erst am äußeren Startpunkt aus der Tüte. Befestige es an der Schnur und ziehe es auf dem Rückweg Richtung Zuhause über den Boden. Weitere sichere Wege können aus anderen Richtungen zum gleichen Ziel führen.')
y=block(c,y,'Optional: Urin der Bezugsperson','Das Infoblatt des Helfernetzes nennt optional Eigenurin, mit Wasser im Verhältnis 1:3 verdünnt: ein Teil Urin, drei Teile Wasser. T-Shirt nur leicht anfeuchten oder stellenweise sehr wenig auf geeigneten Boden geben. Nicht auf fremdem Eigentum verteilen. Methode vorher mit dem Helferteam abstimmen.')
y=block(c,y,'Am Ziel beobachten','Wenn vor Ort sicher möglich, einen Zugang nach Hause ermöglichen. Besuche gegebenenfalls mit einer Wildkamera beobachten. Eine Erneuerung nach Regen abstimmen. Die aktive Suche beginnt weiterhin am Entlaufort.')
y=para(c,'Grundlage: Suchhinweise und Infoblätter des Helfernetzes. Weitere Suchhinweise: tasso.net/Service/Wissensportal/Katze/Katze-entlaufen',M,y,size=8,color=MUTED)-8
footer(c);c.showPage()
header(c,'HEIMWEGSCHLEPPE · SCHEMATISCHE ORIENTIERUNG')
para(c,'Auf dem Rückweg<br/>die Spur legen.',M,H-142,size=27,leading=30)
from math import sin, cos, radians
cx,cy= W/2,415
c.setFillColor(SOFT);c.circle(cx,cy,62,fill=1,stroke=0)
text(c,'Zuhause',cx-35,cy+3,15,'Bold')
text(c,'oder Entlaufort',cx-39,cy-17,10)
def arrow(x1,y1,x2,y2,color,dashed=False):
 c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(2)
 c.setDash(5,4) if dashed else c.setDash()
 c.line(x1,y1,x2,y2);c.setDash()
 import math
 a=math.atan2(y2-y1,x2-x1)
 for offset in [-.5,.5]:c.line(x2,y2,x2-10*math.cos(a+offset),y2-10*math.sin(a+offset))
for angle in [0,90,180,270]:
 a=radians(angle);u,v=cos(a),sin(a);px,py=-v,u
 arrow(cx+u*82+px*10,cy+v*82+py*10,cx+u*185+px*10,cy+v*185+py*10,MUTED,True)
 arrow(cx+u*185-px*10,cy+v*185-py*10,cx+u*82-px*10,cy+v*82-py*10,colors.HexColor('#32664e'))
arrow(M,181,M+50,181,MUTED,True)
text(c,'Hinweg: Kleidungsstück in der Tüte',M+70,177,10)
arrow(M,152,M+50,152,colors.HexColor('#32664e'))
text(c,'Rückweg: Duftspur Richtung Zuhause',M+70,148,10,'Bold')
para(c,'Keine Spur auf Fahrbahnen oder über Gleise legen. Sichere Wege und den passenden Zeitpunkt mit dem Helferteam abstimmen. Die Darstellung legt keinen Suchradius fest.',M,113,size=9.5)
footer(c);c.showPage();c.save()

c,y=doc('futtergeruch.pdf','Wenige Tropfen.<br/>Gezielt beobachten.','Futtergeruch mit Thunfischwasser und kontrollierte Futterstellen.')
y=note(c,y,'Auch andere Tiere werden angelockt.','Stimme vorher mit dem Helferteam ab, ob eine Futtergeruchsspur vor Ort sinnvoll ist. Eine Spur ist keine Garantie und ersetzt die Suche in der direkten Umgebung nicht.')
y=block(c,y,'Das brauchst du','Thunfisch im eigenen Saft oder in Wasser, nicht in Öl. Verwende nur die Flüssigkeit aus der Dose, bei Bedarf mit Wasser verdünnt. Eine Flasche mit kleiner Öffnung hilft beim sparsamen Dosieren.')
y=block(c,y,'Den Weg planen','Die Strecke führt von einem äußeren Startpunkt Richtung Zuhause. Entfernung und Verlauf sind keine feste Vorgabe, sondern richten sich nach der Situation. Keine Spur über Bahngleise oder stark befahrene Straßen legen. Bei Wohnungskatzen zuerst nahe Verstecke kontrollieren.')
y=block(c,y,'Sparsam dosieren','Auf dem Rückweg nach Hause nur wenige Tropfen auf geeignete Bodenstellen geben. Das Infoblatt nennt Abstände von etwa 10-20 Metern. Keine Futterstücke entlang der Strecke verteilen. Fremdes Eigentum respektieren.')
y=block(c,y,'Wenige Futterstellen einrichten','Am abgestimmten Ziel etwas Nassfutter und frisches Wasser an einem geschützten Platz anbieten. Nur wenige, kontrollierbare Stellen nutzen. Eine Wildkamera kann helfen zu erkennen, welches Tier dort frisst.')
y=block(c,y,'Beobachten und anpassen','Kontrolliere die Stellen und stimme weitere Schritte anhand der Beobachtungen ab. Eine Erneuerung nach Regen ebenfalls absprechen. Eine gesichtete Katze nicht verfolgen oder einkreisen; Standort und Uhrzeit notieren.')
y=para(c,'Futterstellen und Geruchsspuren sind unterschiedliche Maßnahmen. Entscheidend ist, dass die Situation kontrollierbar bleibt. Grundlage: Infoblätter und Suchhinweise des Helfernetzes.',M,y,size=9,color=MUTED)-14
finish(c,y)

c=canvas.Canvas(str(OUT/'suchflyer.pdf'),pagesize=A4)
c.setTitle('Katze vermisst - ausfüllbarer Suchflyer');c.setAuthor('Kleines Helfernetz · Team Köpenick')
header(c,'SUCHMELDUNG')
text(c,'KATZE VERMISST',M,H-181,43,'Bold')

def field(name,label,x,y,w,h=32,multiline=False,size=13):
 text(c,label,x,y+h+8,8,'Bold',MUTED)
 c.acroForm.textfield(name=name,tooltip=label,x=x,y=y,width=w,height=h,value='',fontName='Courier',fontSize=size,textColor=INK,borderColor=LINE,fillColor=colors.white,borderWidth=1,borderStyle='solid',forceBorder=True,fieldFlags='multiline' if multiline else '',maxlen=int((w-8)/(size*.6)) * (max(1,int((h-6)/(size*1.3))) if multiline else 1))

field('name','NAME DER KATZE',M,598,WIDTH,32,size=20)
photo_x,photo_y,photo_w,photo_h=M,292,275,282
c.setFillColor(SOFT);c.setStrokeColor(LINE);c.rect(photo_x,photo_y,photo_w,photo_h,fill=1,stroke=1)
text(c,'DEIN KATZENFOTO',photo_x+55,photo_y+154,12,'Bold',MUTED)
para(c,'Aktuelles, scharfes Foto.<br/>Die ganze Katze gut erkennbar.<br/><br/>Hier nach dem Ausdruck aufkleben.',photo_x+28,photo_y+130,photo_w-56,size=10,color=MUTED)
x=M+294;w=WIDTH-294
field('entlaufort','ENTLAUFORT / UMGEBUNG',x,496,w,58,True,12)
field('datum','VERMISST SEIT',x,433,w,32,False,12)
field('aussehen','FARBE / MUSTER',x,354,w,48,True,12)
field('merkmale','BESONDERE MERKMALE',M,208,WIDTH,55,True,13)
field('kontakt','SICHTUNGEN BITTE AN: TELEFON / E-MAIL',M,127,WIDTH,48,False,21)
text(c,'Bitte nicht verfolgen oder einfangen.',M,93,15,'Bold',ACCENT)
text(c,'Ruhig bleiben. Sichtung mit genauem Ort und Uhrzeit melden.',M,72,10,color=INK)
c.setStrokeColor(LINE);c.line(M,48,W-M,48)
para(c,'Vor dem Aushang ausfüllen und Foto ergänzen. Nur erlaubte Aushangflächen nutzen. Wähle bewusst, welche Kontaktdaten öffentlich sichtbar sein sollen.',M,39,WIDTH,size=7.5,color=MUTED,leading=10)
c.showPage();c.save()
print('Created:', ', '.join(p.name for p in OUT.glob('*.pdf')))
