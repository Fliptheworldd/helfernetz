from pathlib import Path
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
R=Path(__file__).resolve().parents[1];W,H=A4
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
b=BytesIO();im=Image.open(R/'assets/helfernetz-logo-telefon.webp').convert('RGB');im.thumbnail((400,400));im.save(b,format='JPEG',quality=80);b.seek(0);logo=ImageReader(b)
def start(name,title,intro):
 c=canvas.Canvas(str(R/'downloads'/name),pagesize=A4);c.setTitle(title);c.setAuthor('Kleines Helfernetz · Team Köpenick');c.drawImage(logo,42,744,66,66);c.setFillColorRGB(.03,.11,.37);c.setFont('Bold',13);c.drawString(122,789,'KLEINES HELFERNETZ');c.setFont('Body',10);c.drawString(122,770,'Berlin-Brandenburg · Team Köpenick');c.drawString(122,752,'030 81451625 · info@helfernetz.com');c.setStrokeColorRGB(.8,.9,.95);c.line(42,730,553,730);y=para(c,title,710,24,True)-15;y=para(c,intro,y,10)-25;return c,y

def para(c,s,y,size=11,bold=False):
 p=Paragraph(s,ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.5,textColor='#081d60'));_,h=p.wrap(511,900);p.drawOn(c,42,y-h);return y-h

def finish(c,y):
 assert y>65,y;c.setFont('Body',8);c.setFillColorRGB(.2,.3,.45);c.drawString(42,38,'helfernetz.com · Ehrenamtlich & kostenfrei · Stand Oktober 2026');c.save()
c,y=start('suchcheckliste.pdf','Meine Katze fehlt – Checkliste','Ruhig beginnen. Maßnahmen abstimmen. Bei Sichtung nicht verfolgen.')
for t in ['Letzten sicheren Sichtungsort und Zeitpunkt festhalten.','Wohnung, Haus, Keller und Garten gründlich kontrollieren.','Direkte Umgebung und geschützte Verstecke absuchen.','Nachbarn bitten, Garagen, Schuppen und Keller zu öffnen.','Foto, Beschreibung, Chipnummer und Kontaktdaten bereithalten.','TASSO, FINDEFIX und Tierheim / Fundtierstelle informieren.','Suchplakate erstellen und erlaubte Aushänge vereinbaren.','Ruhige Suchrunden mit Taschenlampe und Warnweste planen.','Sichtungen mit Zeit, Ort und Laufrichtung dokumentieren.','Futterstellen und weitere Maßnahmen mit Helfern abstimmen.','Nach Rückkehr alle Meldestellen informieren, Aushänge entfernen.']:
 c.rect(42,y-13,10,10);p=Paragraph(t,ParagraphStyle('i',fontName='Body',fontSize=10,leading=15,textColor='#081d60'));_,h=p.wrap(488,100);p.drawOn(c,65,y-h);y-=max(h,18)+14
finish(c,y)
c,y=start('sichtungsprotokoll.pdf','Sichtungsprotokoll','Nicht verfolgen. Abstand halten. Hinweise möglichst genau notieren und telefonisch weitergeben.')
for title in ['Datum und Uhrzeit','Genauer Ort / Orientierungspunkt','Aussehen / besondere Merkmale','Laufrichtung / mögliches Versteck','Verhalten / Zustand der Katze','Foto vorhanden? Wer hat die Katze gesehen?','Rückrufnummer / an wen wurde gemeldet?']:
 y=para(c,title,y,10,True)-20;c.setStrokeColorRGB(.65,.75,.83);c.line(42,y,553,y);y-=23
finish(c,y)
c,y=start('anlaufstellen.pdf','Kontakte für die Suche','Eigene Angaben ergänzen. Aktuelle Erreichbarkeit auf den jeweiligen Websites prüfen.')
for t,b in [('Helfernetz · Team Köpenick','030 81451625 · info@helfernetz.com<br/>Ehrenamtliche Suchhilfe, keine ständig besetzte Notrufzentrale.'),('TASSO','tasso.net/Tierregister/Tier-vermisst<br/>Vermisstmeldung, Registrierung und Suchplakat.'),('FINDEFIX','findefix.com<br/>Haustierregister des Deutschen Tierschutzbundes.'),('Amtliche Tiersammelstelle Berlin','030 76888-200 oder -201<br/>tiersammelstelle@tierschutz-berlin.de<br/>tierschutz-berlin.de/tier-gefunden/'),('Eigene Tierarztpraxis / Notdienst','Name: ______________________________________________<br/>Telefon: _____________________________________________'),('Ansprechperson für die Suche','Name: ______________________________________________<br/>Telefon: _____________________________________________')]:
 y=para(c,t,y,12,True)-7;y=para(c,b,y,10)-22
finish(c,y)
c,y=start('katzensicherheit.pdf','Zuhause sicher machen','Regelmäßig prüfen – besonders vor Umzug, Urlaub und Besuch.')
for t,b in [('Fenster und Balkon','Kippfenster sichern. Netze und Befestigungen auf Lücken oder Beschädigungen prüfen. Ungesicherte Fenster nicht zugänglich lassen.'),('Türen und Handwerker','Vor Arbeiten oder viel Besuch einen ruhigen, geschlossenen Raum vorbereiten. Alle Beteiligten über die Katze informieren.'),('Transport','Stabile Transportbox und Verschlüsse prüfen. Die Box draußen nicht ungesichert öffnen.'),('Chip und Registrierung','Chipnummer bei einem Haustierregister registrieren. Telefonnummer und Anschrift aktuell halten. Ein Chip ist kein GPS-Sender.'),('Für eine Suche vorbereitet sein','Aktuelle Fotos, besondere Merkmale, Chipnummer und Ansprechpartner griffbereit halten.'),('Beschäftigung und Rückzug','Sichere Verstecke und Kratzmöglichkeiten anbieten. Schnüre und verschluckbare Spielzeugteile nach dem Spielen wegräumen.')]:
 y=para(c,t,y,12,True)-7;y=para(c,b,y,10)-20
finish(c,y)
print('4 PDFs created')
