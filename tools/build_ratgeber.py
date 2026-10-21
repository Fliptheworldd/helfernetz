"""Build the full editorial guide from versioned Markdown. No third-party dependencies."""
from pathlib import Path
import re, html
ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=(ROOT/'tools/templates/guide.html').read_text()
E=html.escape
FILES=sorted((ROOT/'content/ratgeber').glob('[0-9][0-9]-*.md'))
chapters=[]
for f in FILES:
    raw=f.read_text(); title,body=raw.split('\n',1)
    chapters.append(dict(slug=f.stem[3:],title=title[2:],body=body.strip(),number=int(f.stem[:2])))

def inline(text):
    text=E(text)
    text=re.sub(r'https://[^\s<>]+',lambda m:f'<a href="{m[0]}">{E(m[0].split("/")[2])} ↗</a>',text)
    for host in ['www.tasso.net','www.findefix.com']:
        if 'https://' not in text: text=text.replace(host,f'<a href="https://{host}/">{host}</a>')
    text=re.sub(r'(?<![\w/])(?:tierheim|tiersammelstelle)@(?:tierschutz|tierheim)-berlin\.de',lambda m:f'<a href="mailto:{m[0]}">{m[0]}</a>',text)
    for phone in ['030 5143760','030 9322093','030 83862422','0160 3758447','030 201805750','06190 937300','0228 6049635','030 76888-200','030 76888-201','030 76888-0']:
        text=text.replace(phone,f'<a class="clinic-phone" href="tel:+49{re.sub(chr(92)+"D", "",phone)[1:]}">{phone}</a>')
    return text

def blocks(raw):
    out=[]; para=[]; inlist=False
    def flush():
        if para:
            s=' '.join(para); note=s.startswith(('Wichtig:','Besonders wichtig:','Ganz wichtig:','Unser Tipp:'))
            out.append(f'<p{" class=\"guide-advice\"" if note else ""}>{inline(s)}</p>'); para.clear()
    for line in raw.splitlines()+['']:
        if not line.strip():
            flush()
            if inlist: out.append('</ul>'); inlist=False
        elif line.startswith('### '):
            flush(); out.append('<h3>'+inline(line[4:])+'</h3>')
        elif line.startswith('- '):
            flush()
            if not inlist: out.append('<ul>');inlist=True
            if line.startswith('- [ ] '):out.append('<li class="check-item"><label><input type="checkbox"> <span>'+inline(line[6:])+'</span></label></li>')
            else:out.append('<li>'+inline(line[2:])+'</li>')
        elif line.startswith('> '):
            flush();out.append('<blockquote><p>„'+inline(line[2:])+'“</p></blockquote>')
        else:para.append(line)
    return ''.join(out)

def sections(body):
    parts=re.split(r'^## (.+)$',body,flags=re.M)
    intro=parts[0].strip(); sections=[]
    for i in range(1,len(parts),2):sections.append((f'thema-{(i+1)//2}',parts[i],blocks(parts[i+1])))
    return intro,sections

def support():return '<div class="search-support"><strong>Für vermisste Katzen</strong><a href="tel:+493081451625">030 81451625</a><a class="support-mail" href="mailto:info@helfernetz.com">info@helfernetz.com</a><small>Ehrenamtlich in Berlin-Köpenick &amp; Umgebung. Keine durchgehend besetzte Notrufzentrale.</small><a class="support-mail" href="/notfallkontakte/">Tierärztliche Notfallkontakte →</a></div>'

def intro(title,lead,kicker='WISSEN FÜR EIN GUTES KATZENLEBEN',photo=True):
    image='<figure><img src="/assets/cat-care.webp" width="1122" height="1402" alt="Katzenporträt – Symbolbild"><figcaption>Symbolbild</figcaption></figure>' if photo else ''
    return f'<section class="search-intro guide-intro"><div><p class="guide-kicker">{kicker}</p><h1>{E(title)}</h1><p>{inline(lead)}</p></div>{image}</section>'

def save(path,title,description,main):
    page=TEMPLATE.replace('{{MAIN}}',main)
    page=page.replace('Eine Katze aufnehmen',E(title)).replace('Eine Entscheidung für viele Jahre.',E(description))
    page=page.replace('https://helfernetz.com/katzenratgeber/anschaffung/',f'https://helfernetz.com/{path}/')
    page=page.replace('</head>','<script src="/ratgeber.js?v=1" defer></script></head>')
    page=page.replace('class="search-page"','class="search-page guide-page"')
    if path=='notfallkontakte':
        page=page.replace('<aside class="mobile-dock" aria-label="Notfallkontakt"><a href="tel:+493081451625"><div><span>NOTFALLNUMMER</span><strong data-phone-label>030 81451625</strong></div><span class="dock-action">Kontakt', '<aside class="mobile-dock" aria-label="Tierärztliche Hilfe"><a href="#schnellhilfe"><div><span>TIERÄRZTLICHER NOTFALL</span><strong>Klinik anrufen</strong></div><span class="dock-action">Kontakte')
    dest=ROOT/path/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)

def breadcrumb(title):return '<nav class="guide-breadcrumb" aria-label="Brotkrumennavigation"><a href="/">Startseite</a><span aria-hidden="true">›</span><a href="/katzenratgeber/">Katzenratgeber</a><span aria-hidden="true">›</span><span>'+E(title)+'</span></nav>'

def article(title,body,kicker,extra='',emergency=False):
    opening,items=sections(body)
    ps=opening.split('\n\n');lead=ps[0];rest='\n\n'.join(ps[1:])
    toc=''.join(f'<a href="#{id}">{E(h)}</a>' for id,h,b in items)
    content=('<section id="einleitung">'+blocks(rest)+'</section>') if rest else ''
    for id,h,b in items:
        if h=='Meine persönliche Notfallkarte': b+='<p><a class="button button-primary" href="/downloads/notfallkarte.pdf" download>Notfallkarte als PDF herunterladen ↓</a></p><p>Am Bildschirm ausfüllbar oder leer ausdrucken und von Hand ergänzen.</p>'
        content+=f'<section id="{id}"><h2>{E(h)}</h2>{b}</section>'
    quick=''
    if emergency:
        quick='<section class="clinic-quick" aria-labelledby="schnellhilfe"><h2 id="schnellhilfe">Tierärztliche Hilfe · rund um die Uhr</h2><p>Bei Atemnot, fehlendem Urinabsatz oder Vergiftungsverdacht sofort tierärztliche Hilfe organisieren. Unser Helfernetz ersetzt keinen tierärztlichen Notdienst.</p><div><a href="tel:+49305143760"><small>AniCura · Biesdorf</small><strong>030 5143760</strong><span>Jetzt anrufen →</span></a><a href="tel:+4930201805750"><small>Valera · Zehlendorf</small><strong>030 201805750</strong><span>Jetzt anrufen →</span></a></div><a class="guide-text-link" href="#thema-3">Alle Kliniken, Adressen und Annahmezeiten ↓</a></section>'
    return f'<main id="main-content">{breadcrumb(title)}{intro(title,lead,kicker,photo=not emergency)}{quick}<div class="search-layout"><aside class="search-sidebar"><details class="guide-toc"><summary>In diesem Kapitel <span aria-hidden="true">＋</span></summary><nav aria-label="Inhaltsverzeichnis">{toc}</nav></details>{support()}</aside><article class="search-article">{content}{extra}<p><a class="guide-text-link" href="#main-content">Zurück nach oben ↑</a></p></article></div></main>'

for i,c in enumerate(chapters):
    related='<div class="guide-related"><a href="/notfallkontakte/">Notfallnummern &amp; Tierkliniken →</a><a href="/downloads/notfallkarte.pdf" download>Persönliche Notfallkarte (PDF) ↓</a></div>' if c['number'] in [5,6,12,13,14] else ''
    if c['number']==6:related+='<p><a class="guide-text-link" href="/katzenratgeber/gesundheit/">Mehr zu Tierarzt, Mikrochip und Registrierung →</a></p>'
    links='<nav class="chapter-pagination" aria-label="Weitere Kapitel">'
    if i:links+=f'<a href="/katzenratgeber/{chapters[i-1]["slug"]}/"><small>Vorheriges Kapitel</small>{E(chapters[i-1]["title"])} ←</a>'
    if i+1<len(chapters):links+=f'<a href="/katzenratgeber/{chapters[i+1]["slug"]}/"><small>Nächstes Kapitel</small>{E(chapters[i+1]["title"])} →</a>'
    links+='</nav><a class="guide-text-link" href="/katzenratgeber/">Alle 14 Kapitel im Überblick →</a>'
    extra=related+links
    if i==13:
        closing=(ROOT/'content/ratgeber/abschluss.md').read_text()
        ct,cb=closing.split('\n',1)
        ci,cs=sections(cb)
        extra='<section><h2>'+E(ct[2:])+'</h2>'+blocks(ci)+''.join('<h3>'+E(h)+'</h3>'+b for _,h,b in cs)+'</section>'+extra
    save('katzenratgeber/'+c['slug'],c['title'],c['body'].split('\n')[0],article(c['title'],c['body'],f'KATZENRATGEBER · KAPITEL {i+1} VON 14',extra))

short=['Bin ich bereit für eine Katze?','Eine Katze oder zwei?','Kitten, erwachsen oder älter?','Die Grundausstattung','Tierarzt, Vorsorge & Versicherung','Ein sicheres Zuhause','Der Einzug','Ernährung','Körpersprache & Verhalten','Fell, Krallen & Zähne','Spielen & Beschäftigung','Katzen im Seniorenalter','Krankheit & Warnzeichen','Urlaub & Betreuung']
desc=['Zeit, Kosten und Verantwortung für ein ganzes Katzenleben.','Welche Gesellschaft passt zu deiner Katze?','Alter, Charakter und dein Alltag.','Was vor dem Einzug bereitstehen sollte – mit Checkliste.','Gesundheit, Registrierung und finanzielle Vorsorge.','Fenster, Balkon und Alltagsgefahren im Blick.','Mit Geduld ankommen und Vertrauen aufbauen.','Futter, Wasser und die Bedürfnisse deiner Katze.','Signale erkennen und Grenzen respektieren.','Sanfte Pflege und aufmerksame Kontrollen.','Ideen für Bewegung und Abwechslung.','Mit kleinen Hilfen den Alltag erleichtern.','Veränderungen erkennen und rechtzeitig handeln.','Zuverlässig vorsorgen, wenn du selbst ausfällst.']
main='<main id="main-content">'+intro('Unser großer Katzenratgeber','Für ein glückliches Katzenleben – von Anfang an und ein Leben lang. Entdecke alle 14 Kapitel unseres Helfernetz-Teams.')+'<div class="guide-hub"><a class="guide-emergency" href="/notfallkontakte/"><strong>Deine Katze braucht dringend medizinische Hilfe?</strong><span>Notfallnummern &amp; Tierkliniken →</span></a><nav class="guide-groups" aria-label="Ratgeberbereiche"><a href="#vorbereiten">Vor dem Einzug</a><a href="#alltag">Gemeinsamer Alltag</a><a href="#vorsorgen">Alter &amp; Vorsorge</a></nav>'
for start,end,id,title in [(0,6,'vorbereiten','Gut vorbereitet ins Katzenleben'),(6,11,'alltag','Ein guter Alltag miteinander'),(11,14,'vorsorgen','Für deine Katze da sein')]:
    main+=f'<section class="guide-group" id="{id}"><h2>{title}</h2><div class="guide-cards">'
    for i in range(start,end):
        c=chapters[i];main+=f'<a class="guide-card" href="/katzenratgeber/{c["slug"]}/"><span class="guide-card-kicker">Kapitel {i+1}</span><h3>{E(short[i])}</h3><p>{E(desc[i])}</p><span class="guide-card-arrow" aria-hidden="true">→</span></a>'
    main+='</div></section>'
main+='<section class="guide-extra"><h2>Wieder daheim. Gut vorbereitet.</h2><p>Auch nach einer Suche und für den nächsten Notfall findest du bei uns praktische Hilfe.</p><div class="guide-related"><a href="/katzenratgeber/wieder-zuhause/">Endlich wieder zu Hause! →</a><a href="/downloads/notfallkarte.pdf" download>Notfallkarte zum Ausfüllen (PDF) ↓</a><a href="/katzenratgeber/haltung/">Mehr zur artgerechten Haltung →</a></div></section></div></main>'
save('katzenratgeber','Unser großer Katzenratgeber','Alle 14 Kapitel: Anschaffung, Alltag, Gesundheit und liebevolle Begleitung. Kostenlos vom Helfernetz-Team Köpenick.',main)
raw=(ROOT/'content/notfallkontakte.md').read_text();title,body=raw.split('\n',1)
save('notfallkontakte',title[2:],'Tierkliniken, Notdienste, Haustierregister und deine persönliche Notfallkarte für Berlin und Brandenburg.',article(title[2:],body,'BERLIN & BRANDENBURG · WICHTIGE KONTAKTE',emergency=True))
print(f'Built {len(chapters)} complete chapters, guide overview and emergency contacts.')
