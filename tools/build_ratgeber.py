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
    page=page.replace('</head>','<script src="/ratgeber.js?v=2" defer></script></head>')
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
main='<main id="main-content" class="lexicon"><section class="lexicon-cover"><div><p class="lexicon-eyebrow">DAS WISSEN UNSERES HELFERNETZES</p><h1>Katzen verstehen.<br><em>Ein Leben lang.</em></h1><p class="lexicon-lead">Dein Katzenlexikon. Vom ersten Gedanken an eine Katze bis ins hohe Alter – finde die Antworten, die du gerade brauchst.</p><span class="lexicon-edition">14 ausführliche Artikel · Für dich und deine Katze</span></div><figure><img src="/assets/cat-care.webp" alt="Eine Katze genießt eine sanfte Berührung – Symbolbild" width="1122" height="1402"><figcaption>Mit Wissen. Mit Geduld. Mit Herz. <span>Symbolbild</span></figcaption></figure></section><div class="lexicon-library" id="themen"><div class="lexicon-tools"><div class="lexicon-search" hidden><label for="lexicon-query">Was möchtest du wissen?</label><div><svg class="icon" aria-hidden="true"><use href="#i-search"/></svg><input id="lexicon-query" type="search" placeholder="Zum Beispiel: Balkon, Kitten, Futter …" autocomplete="off"><button type="button" id="lexicon-clear" aria-label="Suche löschen" hidden>×</button></div></div><div class="lexicon-filters" role="group" aria-label="Themen auswählen" hidden><button type="button" data-category="all" aria-pressed="true">Alles entdecken</button><button type="button" data-category="vorbereiten" aria-pressed="false">Vor dem Einzug</button><button type="button" data-category="alltag" aria-pressed="false">Zusammenleben</button><button type="button" data-category="vorsorgen" aria-pressed="false">Gesundheit &amp; Vorsorge</button></div><p id="lexicon-results" class="lexicon-count" role="status" aria-live="polite">Alle 14 Artikel</p></div>'
for start,end,id,title,caption in [(0,6,'vorbereiten','Bevor ihr euch findet','Eine Entscheidung mit Herz und Verstand.'),(6,11,'alltag','Das Leben miteinander','Verstehen, versorgen, gemeinsam wachsen.'),(11,14,'vorsorgen','An ihrer Seite bleiben','Gut vorbereitet. Auch wenn sich das Leben verändert.')]:
    main+=f'<section class="lexicon-section" id="{id}"><header><h2>{title}</h2><p>{caption}</p></header><div class="lexicon-entries">'
    for i in range(start,end):
        c=chapters[i]; minutes=max(2,round(len(c['body'].split())/180))
        search=E(' '.join((c['title']+' '+c['body']).split()),quote=True)
        # Health and safety articles also belong in the health filter.
        category=id+(' vorsorgen' if i in [4,5] else '')
        main+=f'<a class="lexicon-entry" data-category="{category}" data-search="{search}" href="/katzenratgeber/{c["slug"]}/"><div><h3>{E(short[i])}</h3><p>{E(desc[i])}</p><span class="lexicon-reading">{minutes} Min. Lesezeit</span></div><span class="lexicon-arrow" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="m9 5 7 7-7 7"/></svg></span></a>'
    main+='</div></section>'
main+='<div class="lexicon-empty" hidden><h2>Dazu haben wir noch keinen Treffer.</h2><p>Versuche einen kürzeren Begriff, zum Beispiel „Futter“ oder „Fenster“, oder wähle „Alles entdecken“.</p><button type="button" id="lexicon-reset">Alle Artikel anzeigen</button></div><aside class="lexicon-afterword"><span aria-hidden="true">♥</span><div><h2>Für ein ganzes Katzenleben.</h2><p>Unsere Texte sind für dich da – zum Nachschlagen, Weiterdenken und Wiederkommen. Kostenlos und mit viel Herz vom Team Köpenick.</p><a href="/katzenratgeber/wieder-zuhause/">Nach einer Suche: Endlich wieder zu Hause →</a><a href="/downloads/notfallkarte.pdf" download>Deine persönliche Notfallkarte (PDF) ↓</a><a href="/notfallkontakte/">Tierärztliche Notfallkontakte →</a></div></aside></div></main>'
save('katzenratgeber','Katzenlexikon – Wissen für ein ganzes Katzenleben','Dein Katzenlexikon: 14 ausführliche Artikel zu Anschaffung, Alltag, Gesundheit und Vorsorge. Kostenlos vom Helfernetz-Team Köpenick.',main)
raw=(ROOT/'content/notfallkontakte.md').read_text();title,body=raw.split('\n',1)
save('notfallkontakte',title[2:],'Tierkliniken, Notdienste, Haustierregister und deine persönliche Notfallkarte für Berlin und Brandenburg.',article(title[2:],body,'BERLIN & BRANDENBURG · WICHTIGE KONTAKTE',emergency=True))
print(f'Built {len(chapters)} complete chapters, guide overview and emergency contacts.')
