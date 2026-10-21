from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for name,file in [('Guide','DejaVuSans.ttf'),('GuideBold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
navy=HexColor('#081d60'); blue=HexColor('#eaf8ff'); red=HexColor('#c41330')
c=canvas.Canvas(str(ROOT/'downloads/notfallkarte.pdf'),pagesize=(595.28,841.89))
c.setTitle('Meine persönliche Notfallkarte für meine Katze');c.setAuthor('Kleines Helfernetz - Team Köpenick')
im=Image.open(ROOT/'assets/helfernetz-logo-telefon.webp');im.thumbnail((400,400));buf=BytesIO();im.save(buf,format='PNG');buf.seek(0)
c.setFillColor(blue);c.rect(0,704,596,138,fill=1,stroke=0)
c.drawImage(ImageReader(buf),440,718,108,108,mask='auto',preserveAspectRatio=True)
c.setFillColor(navy);c.setFont('GuideBold',23);c.drawString(42,785,'Meine persönliche')
c.drawString(42,754,'Notfallkarte')
c.setFont('Guide',10);c.drawString(42,731,'Für meine Katze. Für den Fall der Fälle.')
c.setFont('Guide',10);c.drawString(42,681,'Ausfüllen und gut erreichbar aufbewahren. Kontaktdaten aktuell halten.')
labels=[('katze','Name meiner Katze'),('chip','Chipnummer'),('register','Registriert bei'),('praxis','Meine Tierarztpraxis'),('praxis_telefon','Telefon der Tierarztpraxis'),('klinik','Meine nächste Tierklinik'),('klinik_telefon','Notfalltelefon der Tierklinik'),('kontakt','Vertrauensperson für Notfälle'),('kontakt_telefon','Telefon der Vertrauensperson')]
y=652
for key,label in labels:
 c.setFillColor(navy);c.setFont('GuideBold',10);c.drawString(42,y,label)
 c.acroForm.textfield(name=key,tooltip=label,x=42,y=y-30,width=511,height=24,fontName='Helvetica',fontSize=11,borderWidth=.7,borderColor=HexColor('#aacbdc'),fillColor=white,textColor=navy,forceBorder=True,maxlen=120)
 y-=49
c.setFont('GuideBold',10);c.drawString(42,211,'Besondere Erkrankungen oder Medikamente meiner Katze')
c.acroForm.textfield(name='medizin',tooltip='Erkrankungen und Medikamente',x=42,y=143,width=511,height=58,fontName='Helvetica',fontSize=11,borderWidth=.7,borderColor=HexColor('#aacbdc'),fillColor=white,textColor=navy,forceBorder=True,fieldFlags='multiline',maxlen=600)
c.setFillColor(red);c.setFont('GuideBold',10);c.drawString(42,116,'Bei Atemnot, fehlendem Urinabsatz oder Vergiftungsverdacht:')
c.setFont('Guide',10);c.drawString(42,100,'sofort eine Tierarztpraxis oder Tierklinik mit Notdienst kontaktieren.')
c.setStrokeColor(HexColor('#bfdbe8'));c.line(42,82,553,82)
c.setFillColor(navy);c.setFont('Guide',9);c.drawString(42,64,'helfernetz.com/notfallkontakte/  |  info@helfernetz.com')
c.drawString(42,47,'Hilfe bei vermissten Katzen: 030 81451625 (kein tierärztlicher Notdienst)')
c.showPage();c.save()
from pypdf import PdfReader
r=PdfReader(ROOT/'downloads/notfallkarte.pdf');assert len(r.pages)==1;assert len(r.get_fields())==10
print('PDF created; 10 interactive fields validated.')
