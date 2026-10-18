'use strict';

// Supply the team's confirmed number here. Never use example phone numbers.
const CONTACT = { number: '+493081451625', display: '030 81451625', availability: '' };
const dialog = document.querySelector('#help-dialog');
const content = document.querySelector('#dialog-content');
const icon = (name) => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
const tassoLink = '<a class="download-link" href="https://www.tasso.net/Service/Wissensportal/Katze/Katze-entlaufen" target="_blank" rel="noopener noreferrer">Weiterlesen bei TASSO <small>Externe Suchhinweise <svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a>';
let lastTrigger = null;
let checklistState = new Set();
let sightingDraft = '';

const checklist = [
  'Am Entlaufort und in der unmittelbaren Umgebung beginnen.',
  'Eine ruhige Suchzeit wählen, zum Beispiel 22–2 Uhr oder vor Sonnenaufgang.',
  'Taschenlampe und Warnweste oder eine gut sichtbare Kennzeichnung mitnehmen.',
  'Verstecke unter Autos, in Hecken, Kellern, Garagen und Schuppen gründlich prüfen.',
  'Nachbarn einbeziehen. Fremde Grundstücke und Gebäude nur mit Erlaubnis betreten.',
  'Langsam gehen, leise rufen, stehen bleiben und lauschen. Nicht hinterherlaufen oder einkreisen.',
  'Wenige geschützte Futterstellen kontrollieren; mit einer Wildkamera prüfen, welches Tier frisst.',
  'Sichtungen mit Ort, Uhrzeit und Laufrichtung notieren. Weitere Suche und Sicherung abstimmen.'
];
const section = (title, text) => `<section class="dialog-section"><h3>${title}</h3>${text}</section>`;
const pdfLink = (file, label) => `<a class="download-link" href="/downloads/${file}.pdf" download>${label}<small>PDF · A4 ${icon('download')}</small></a>`;
const caution = (title, text) => `<aside class="dialog-callout"><strong>${title}</strong><p>${text}</p></aside>`;
const view = {
  register: () => `<span class="guide-tag">VERMISSTMELDUNG</span><h2 class="dialog-heading" id="dialog-title">Auch online melden.</h2><p class="dialog-intro">Melden Sie Ihre Katze beim Haustierregister als vermisst. Halten Sie ein aktuelles Foto, den Entlaufort und die Chipnummer bereit, sofern vorhanden.</p><a class="download-link" href="https://www.tasso.net/Tierregister/Tier-vermisst" target="_blank" rel="noopener noreferrer">TASSO <small>Vermisstmeldung ${icon('diagonal')}</small></a><a class="download-link" href="https://www.findefix.com/" target="_blank" rel="noopener noreferrer">FINDEFIX <small>Haustierregister ${icon('diagonal')}</small></a><p class="guide-note">Informieren Sie zusätzlich Tierheime und örtliche Suchgruppen. Online-Meldungen ergänzen die Suche vor Ort.</p>`,
  arrival: () => `<span class="guide-tag">KATZENRATGEBER</span><h2 class="dialog-heading" id="dialog-title">Eine Katze zieht ein.</h2><p class="dialog-intro">Ein gutes Zuhause beginnt mit Vorbereitung, Zeit und Geduld.</p>${section('Vor dem Einzug','<p>Planen Sie die laufenden Kosten und die Versorgung während Urlaub oder Krankheit. Stimmen Sie die Entscheidung mit allen Personen im Haushalt ab.</p>')}${section('Alles bereitstellen','<p>Transportbox, Katzentoiletten, vertrautes Futter, Wasser, Kratzmöglichkeiten, sichere Rückzugsorte und geeignetes Spielzeug gehören zur Grundausstattung.</p>')}${section('In Ruhe ankommen','<p>Bereiten Sie einen ruhigen Raum vor. Lassen Sie die Katze selbst aus der Transportbox kommen und ihre Umgebung in ihrem eigenen Tempo entdecken. Nicht bedrängen oder aus einem Versteck ziehen.</p>')}${section('Passende Gesellschaft','<p>Ob eine weitere Katze passt, hängt von Alter, Charakter und bisherigen Erfahrungen ab. Lassen Sie sich dazu von der vermittelnden Pflegestelle oder dem Tierheim beraten.</p>')}<button class="text-button" data-open="prevention">Das Zuhause sichern ${icon('arrow')}</button>`,
  prevention: () => `<span class="guide-tag">KATZENRATGEBER</span><h2 class="dialog-heading" id="dialog-title">Wohnungskatzen schützen.</h2><p class="dialog-intro">Sicherheit beginnt vor dem ersten Ausflug durch eine offene Tür.</p>${section('Fenster und Balkon','<p>Sichern Sie Fenster und Balkon mit geeigneten, stabil befestigten Schutzsystemen. Prüfen Sie Befestigungen und mögliche Lücken regelmäßig. Ein gewöhnliches Insektengitter ist kein Katzenschutz.</p><p>Lassen Sie eine Katze nicht an ungesicherte Kippfenster.</p>')}${section('Türen im Blick','<p>Kontrollieren Sie vor dem Öffnen der Wohnungstür, wo sich die Katze befindet. Informieren Sie Besuch und Handwerker. Bei Umzügen oder offenen Türen hilft ein sicherer, geschlossener Rückzugsraum.</p>')}${section('Kennzeichnung und Registrierung','<p>Besprechen Sie die Kennzeichnung mit Ihrer Tierarztpraxis. Registrieren Sie die Chipnummer bei TASSO oder FINDEFIX und halten Sie Ihre Kontaktdaten aktuell. Ein Chip allein ersetzt keine Registrierung.</p>')}${section('Für den Ernstfall','<p>Bewahren Sie aktuelle Fotos, Chipnummer und besondere Merkmale griffbereit auf.</p>')}`,
  homecoming: () => `<span class="guide-tag">KATZENRATGEBER</span><h2 class="dialog-heading" id="dialog-title">Endlich wieder zu Hause.</h2><p class="dialog-intro">Geben Sie Ihrer Katze Zeit, Ruhe und einen vertrauten Rückzugsort.</p>${section('In Ruhe ankommen','<p>Stellen Sie frisches Wasser bereit und vermeiden Sie Trubel. Beobachten Sie Verhalten und Allgemeinzustand. Bei Verletzungen oder auffälligem Verhalten wenden Sie sich an eine Tierarztpraxis; bei einem akuten Notfall an den tierärztlichen Notdienst.</p>')}${section('Versorgung abstimmen','<p>Nach längerer Abwesenheit oder bei deutlicher Abmagerung stimmen Sie Untersuchung und Fütterung mit einer Tierarztpraxis ab.</p>')}${section('Suchmeldung beenden','<p>Informieren Sie TASSO beziehungsweise FINDEFIX, beteiligte Helfer, Tierheime und Suchgruppen über die Rückkehr. Entfernen Sie Suchplakate und aktualisieren Sie Online-Meldungen.</p>')}${section('Für die Zukunft','<p>Prüfen Sie den Entlaufweg, verbessern Sie die Sicherung und kontrollieren Sie die hinterlegten Registrierungsdaten.</p>')}`,

  contact: () => `<span class="guide-tag">NOTFALLKONTAKT</span><h2 class="dialog-heading" id="dialog-title">Wir sind dein<br>Kontakt im Kiez.</h2><p class="dialog-intro">Für vermisste und gefundene Katzen in Berlin-Köpenick.</p>${CONTACT.number ? `<a class="button button-dark dialog-button" href="tel:${CONTACT.number}">${icon('phone')} ${CONTACT.display}</a>` : `<div class="dialog-callout"><strong>Unsere Nummer folgt.</strong><p>Die gemeinsame Telefonnummer wird noch eingerichtet. In diesem Entwurf ist deshalb noch kein Anruf beim Helfernetz möglich.</p></div>`}<a class="download-link" href="mailto:info@helfernetz.com">info@helfernetz.com <small>E-Mail schreiben</small></a><p class="dialog-muted">Für aktuelle Sichtungen bitte anrufen. Für allgemeine Fragen und Unterstützung kannst du uns eine E-Mail schreiben.</p><p class="dialog-muted">Halte möglichst den genauen Ort, die Uhrzeit, ein Foto und besondere Merkmale der Katze bereit.</p>${section('Zusätzlich: Informationen für die Suche','<p>Unsere Nacht-Suchhilfe und die Checkliste sind bereits hier auf der Seite verfügbar. Ein vermisstes Tier kannst du zusätzlich bei einem Haustierregister melden.</p><a class="download-link" href="https://www.tasso.net/Tierregister/Tier-vermisst" target="_blank" rel="noopener noreferrer">TASSO <small>Tier vermisst melden <svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a><a class="download-link" href="https://www.findefix.com/" target="_blank" rel="noopener noreferrer">FINDEFIX <small>Haustierregister <svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a>')}<button class="button button-dark dialog-button" data-open="checklist">Nacht-Checkliste öffnen ${icon('arrow')}</button>`,

  found: () => `<span class="guide-tag">KATZE GESICHTET</span><h2 class="dialog-heading" id="dialog-title">Ein Hinweis kann<br>viel verändern.</h2><p class="dialog-intro">Notiere möglichst genau, wo und wann du die Katze gesehen hast. Ein Foto hilft, wenn du es aus ruhiger Entfernung aufnehmen kannst.</p>${caution('Bitte nicht hinterherlaufen.','Bleibe ruhig, notiere den Standort und bereite eine Sicherung gemeinsam mit dem Helferteam vor. Nicht einkreisen und keine hektische Suche starten.')}<label class="notes-field" for="sighting-notes">Deine Notizen zur Sichtung<textarea id="sighting-notes" placeholder="Ort / nächster Orientierungspunkt:\nDatum und Uhrzeit:\nAussehen / besondere Merkmale:\nLaufrichtung / Versteck:"></textarea></label><p class="dialog-muted">Die Notiz bleibt nur während dieser geöffneten Seite erhalten. Hier wird nichts an das Helfernetz übermittelt.</p><button class="button button-dark dialog-button" id="copy-sighting">Notiz kopieren ${icon('arrow')}</button><p class="dialog-status" id="copy-status" role="status"></p><button class="text-button" data-open="contact">Kontakt zum Helfernetz ${icon('arrow')}</button>`,

  chip: () => `<span class="guide-tag">CHIP AUSLESEN</span><h2 class="dialog-heading" id="dialog-title">Eine kleine Nummer.<br>Eine große Hilfe.</h2><p class="dialog-intro">Wir helfen beim Auslesen des Chips, damit eine gefundene Katze ihrem Zuhause zugeordnet werden kann.</p>${section('Das hilft bei der Abstimmung','<ul><li>Der genaue Fundort und die Uhrzeit.</li><li>Ein Foto oder eine Beschreibung der Katze.</li><li>Die Information, ob die Katze gesichert ist oder nur gesichtet wurde.</li></ul>')}${caution('Ein Chip ist kein GPS-Sender.','Er liefert eine Kennnummer. Über eine vorhandene Registrierung kann das Haustierregister die Halterzuordnung prüfen.')}<button class="button button-dark dialog-button" data-open="contact">Kontakt zum Helfernetz ${icon('arrow')}</button><a class="download-link" href="https://www.tasso.net/Tierregister/Tier-gefunden" target="_blank" rel="noopener noreferrer">Tier gefunden – Hinweise von TASSO <small><svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a>`,

  checklist: () => `<span class="guide-tag">FÜR DEINE SUCHRUNDE</span><h2 class="dialog-heading" id="dialog-title">Ruhe. Geduld.<br>Genau hinsehen.</h2><p class="dialog-intro">Deine Nacht-Checkliste für entlaufene Wohnungskatzen.</p>${pdfLink("nachtsuche","Suchhilfe zum Ausdrucken")}<div class="check-progress" role="progressbar" aria-label="Checkliste erledigt" aria-valuemin="0" aria-valuemax="${checklist.length}" aria-valuenow="${checklistState.size}"><span></span></div><p class="check-count" aria-live="polite"></p><div class="checklist">${checklist.map((item,i)=>`<label class="check-item"><input type="checkbox" data-check="${i}" ${checklistState.has(i)?'checked':''}><span>${item}</span></label>`).join('')}</div><p class="dialog-muted">Die Häkchen bleiben während dieser geöffneten Seite erhalten. Für eine neue Suchrunde kannst du die Liste zurücksetzen.</p><button class="text-button" id="reset-checklist">Checkliste zurücksetzen</button>`,

  scent: () => `<span class="guide-tag">GERUCHSSPUREN · HEIMWEGSCHLEPPE</span><h2 class="dialog-heading" id="dialog-title">Ein vertrauter<br>Geruch nach Hause.</h2><p class="dialog-intro">Eine Heimwegschleppe ist ein möglicher zusätzlicher Baustein der Suche. Sie ersetzt weder die Suche in Verstecken noch Sichtungsmeldungen.</p>${caution('Erst in der Nähe suchen.','Gerade entlaufene Wohnungskatzen verstecken sich häufig in der unmittelbaren Umgebung. Suche dort zuerst gründlich und ruhig. Für Geruchsspuren gibt es keine Erfolgsgarantie.')}<img class="scent-diagram" src="/assets/heimwegschleppe.svg" alt="Hinweg nach außen mit dem Kleidungsstück in der Tüte; Duftspur erst auf dem Rückweg Richtung Zuhause legen.">${section('Vorbereiten','<p>Die Anleitung des Helfernetzes nutzt ein stark getragenes T-Shirt der engsten Bezugsperson, möglichst mindestens 24 Stunden getragen. Dazu kommen eine Schnur und eine verschließbare Tüte, in der das Kleidungsstück bis zum Startpunkt bleibt.</p>')}${section('Eine sichere Strecke wählen','<p>Plane Wege, die zum Zuhause beziehungsweise zum passenden Entlaufort zurückführen. Die im Infoblatt genannten 500 Meter bis 2 Kilometer sind keine feste Vorgabe: Strecke und Entfernung müssen zur Katze, zu Sichtungen und zur Umgebung passen.</p><p>Keine Spur über Bahngleise oder stark befahrene Straßen führen. Fremde Grundstücke nur mit Erlaubnis betreten.</p>')}${section('Die Spur nach Hause legen','<p>Bring das T-Shirt in der geschlossenen Tüte zum äußeren Startpunkt. Nimm es erst dort heraus, befestige es an der Schnur und ziehe es auf dem Rückweg Richtung Zuhause über den Boden. Weitere sichere Wege können aus anderen Richtungen ebenfalls zum Ziel führen.</p>')}${section('Die optionale Urinvariante','<p>Das Infoblatt unseres Helfernetzes nennt ergänzend Eigenurin der Bezugsperson, mit Wasser im Verhältnis 1:3 verdünnt: ein Teil Urin, drei Teile Wasser. Damit kann das T-Shirt leicht angefeuchtet oder stellenweise sehr wenig Flüssigkeit auf geeigneten Boden getropft werden.</p><p>Diese Variante ist optional. Verwende keine Flüssigkeit auf fremdem Eigentum. Stimme die Wahl der Methode und die Strecke mit dem Helferteam ab.</p>')}${section('Am Ziel beobachten','<p>Ermögliche einen sicheren Zugang nach Hause, soweit das vor Ort möglich ist. Eine Wildkamera kann helfen, Besuche zu erkennen. Kontrolliere die Situation und stimme eine Erneuerung der Spur nach Regen ab.</p>')}<p class="guide-note">Die Richtung der Geruchsspur ist nicht mit einer allgemeinen Suchregel gleichzusetzen: Die aktive Suche beginnt am Entlaufort. Von außen nach innen zu suchen ist lediglich eine mögliche Taktik für weitere Runden.</p>${pdfLink("heimwegschleppe","Anleitung herunterladen")}${tassoLink}`,

  food: () => `<span class="guide-tag">FUTTERGERUCH &amp; FUTTERSTELLEN</span><h2 class="dialog-heading" id="dialog-title">Wenige Tropfen.<br>Gezielt beobachten.</h2><p class="dialog-intro">Die Futtergeruchsspur aus der Anleitung unseres Helfernetzes verwendet Thunfischwasser. Ob diese Methode vor Ort sinnvoll ist, sollte mit dem Helferteam abgestimmt werden.</p>${caution('Auch andere Tiere können angelockt werden.','Das gilt auch für Futtergeruch. Lege keine unkontrollierten Futterspuren aus. Eine Geruchsspur ist keine Garantie und ersetzt die Suche in der direkten Umgebung nicht.')}${section('Das brauchst du','<ul><li>Thunfisch im eigenen Saft beziehungsweise in Wasser, nicht in Öl.</li><li>Nur die Flüssigkeit aus der Dose, bei Bedarf mit Wasser verdünnt.</li><li>Eine Flasche mit kleiner Öffnung zum sparsamen Dosieren.</li><li>Für eine abgestimmte Futterstelle am Ziel: etwas Nassfutter und frisches Wasser an einem geschützten Platz.</li></ul>')}${section('Den Weg festlegen','<p>Plane sichere Strecken, die von einem äußeren Startpunkt Richtung Zuhause führen. Die auf dem Infoblatt genannten 500 Meter bis 2 Kilometer sind keine allgemeine Empfehlung. Entfernung und Route hängen von der Situation ab.</p><p>Keine Spur über Bahngleise oder stark befahrene Straßen legen. Bei Wohnungskatzen zunächst Verstecke unmittelbar am Entlaufort absuchen.</p>')}${section('Sparsam dosieren','<p>Gib auf dem Rückweg nach Hause nur wenige Tropfen auf geeignete Bodenstellen. Das Infoblatt nennt Abstände von etwa 10–20 Metern. Verteile keine Futterstücke entlang der Strecke.</p>')}${section('Die Futterstelle kontrollieren','<p>Nutze nur wenige geschützte, kontrollierbare Stellen. Mit einer Wildkamera lässt sich prüfen, welches Tier dort frisst. Passe die weitere Vorgehensweise an die Beobachtungen an und stimme eine Erneuerung nach Regen ab.</p>')}<p class="guide-note">Futterstellen und Geruchsspuren sind unterschiedliche Maßnahmen. Entscheidend ist, dass die Situation kontrollierbar bleibt und eine gesichtete Katze nicht verfolgt oder weiter verscheucht wird.</p>${pdfLink("futtergeruch","Anleitung herunterladen")}${tassoLink}`,

  flyers: () => `<span class="guide-tag">SUCHFLYER &amp; NACHBARSCHAFT</span><h2 class="dialog-heading" id="dialog-title">Mehr Augen.<br>Mehr Hinweise.</h2><p class="dialog-intro">Ein gut lesbarer Suchflyer macht aus Nachbarn aufmerksame Mithelfer. Beginne möglichst früh und halte die Informationen aktuell.</p><a class="download-link" href="#flyer" data-flyer-link>Eigenen Flyer mit Foto erstellen ${icon("arrow")}</a>${pdfLink("suchflyer","Leere Vorlage herunterladen")}${section('Das Foto entscheidet','<p>Nutze ein aktuelles, scharfes und helles Foto ohne Filter. Die ganze Katze sollte erkennbar sein; ein zusätzliches Porträt kann helfen. Natürliche Farben und eine Aufnahme auf Augenhöhe zeigen wichtige Merkmale.</p>')}${section('Diese Angaben gehören darauf','<ul><li>Eine große, klare Überschrift wie „Katze vermisst“.</li><li>Name, Fellfarbe, Muster, Größe und besondere Merkmale.</li><li>Entlaufort und Datum; gegebenenfalls der Hinweis auf eine ängstliche Wohnungskatze.</li><li>Ein geeigneter Kontakt für Sichtungen.</li><li>Der gut sichtbare Hinweis: „Nicht verfolgen. Sichtung mit Ort und Uhrzeit melden.“</li></ul>')}${section('Gut lesbar gestalten','<p>Verwende große Schrift, kräftige Kontraste und stabiles, wettergeschütztes Papier. Ein A4-Blatt lässt sich mit abtrennbaren Kontaktstreifen gestalten. Vermeide überladene Texte, die im Vorbeigehen kaum lesbar sind.</p>')}${section('Gezielt verteilen','<p>Beginne in der unmittelbaren Umgebung und erweitere die Suche anhand der Situation und eingehender Sichtungen. Das Infoblatt nennt als Orientierung zunächst etwa 500 Meter, später 1–2 Kilometer – das ist kein fester Suchradius.</p><p>Frage bei Geschäften, Tierarztpraxen, Cafés und Nachbarn nach, ob du einen Aushang anbringen darfst. Beachte die Regeln am jeweiligen Ort. Keine Plakate an Ampeln oder Verkehrszeichen befestigen.</p>')}${section('Nachbarn persönlich ansprechen','<p>Bitte freundlich darum, Garagen, Schuppen, Keller, Gartenhäuser und andere Verstecke zu kontrollieren. Betritt fremde Grundstücke und Gebäude nur mit Erlaubnis. Nimm auch kurze Sichtungen ernst.</p>')}${section('Aktuell halten &amp; online teilen','<p>Ersetze beschädigte oder unleserliche Flyer. Informiere Haustierregister und Tierheime und teile die Suchmeldung in passenden örtlichen Gruppen. Das Infoblatt rät davon ab, eine Belohnung auf dem Flyer anzubieten, da dadurch unerwünschte Meldungen entstehen können.</p>')}${caution('Kontaktdaten bewusst wählen.','TASSO bietet Suchplakate mit der eigenen Notrufnummer an. So muss deine private Telefonnummer nicht öffentlich auf dem Flyer stehen. Veröffentliche keine unnötigen persönlichen Daten.')}<a class="download-link" href="https://www.tasso.net/Tierregister/Tier-vermisst" target="_blank" rel="noopener noreferrer">Suchmeldung bei TASSO starten <small><svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a><a class="download-link" href="https://www.findefix.com/" target="_blank" rel="noopener noreferrer">FINDEFIX <small>Haustierregister <svg class="icon" aria-hidden="true"><use href="#i-diagonal"/></svg></small></a>`,

  join: () => `<span class="guide-tag">TEIL DES HELFERNETZES WERDEN</span><h2 class="dialog-heading" id="dialog-title">Hilfe beginnt<br>mit Hinschauen.</h2><p class="dialog-intro">Du möchtest dich in Köpenick für vermisste und gefundene Katzen einsetzen? Auch mit Zeit, Ausrüstung oder Sachmitteln kannst du helfen.</p><a class="button button-dark dialog-button" href="mailto:info@helfernetz.com?subject=Ich%20m%C3%B6chte%20das%20Helfernetz%20unterst%C3%BCtzen">Unterstützung per E-Mail anbieten</a>${section('So kannst du dich einbringen','<ul><li>Bei abgestimmten, ruhigen Suchrunden unterstützen.</li><li>Sichtungen aufmerksam dokumentieren.</li><li>Nachbarn ansprechen und Suchmeldungen teilen.</li><li>Mit Erfahrung oder Ausrüstung nach Absprache helfen.</li></ul>')}${caution('Gemeinsam abstimmen.','Eine Suche sollte koordiniert sein. Besonders wichtig: Eine gesichtete Katze nicht verfolgen oder einkreisen.')}<button class="button button-dark dialog-button" data-open="contact">Kontakt zum Helfernetz ${icon('arrow')}</button>`,

  imprint: () => `<span class="guide-tag">ANGABEN GEMÄSS § 5 DDG</span><h2 class="dialog-heading" id="dialog-title">Impressum</h2><p class="dialog-intro">Diese Website des Kleinen Helfernetzes Berlin-Brandenburg · Team Köpenick wird von VachSystems betrieben.</p>${section('Betreiber','<p><strong>VachSystems · Inhaber Patrick Vach</strong><br>Charlottenburger Str. 142<br>13086 Berlin<br>Deutschland</p>')}${section('Kontakt','<p>Zum Website-Betreiber: <a href="mailto:contact@vachsystems.de">contact@vachsystems.de</a><br>Website: <a href="https://vachsystems.de/">vachsystems.de</a></p><p>Zum Helfernetz: <a href="mailto:info@helfernetz.com">info@helfernetz.com</a><br>Telefon: <a href="tel:+493081451625">030 81451625</a></p>')}${section('Verantwortlich für redaktionelle Inhalte','<p>Patrick Vach, Anschrift wie oben (§ 18 Abs. 2 MStV).</p>')}${section('Konzeption, Gestaltung & Umsetzung','<a class="imprint-studio" href="https://vachsystems.de/"><img src="/assets/vachsystems-logo.webp" width="48" height="48" alt="VachSystems-Logo"><span><strong>VachSystems</strong><br>Webdesign aus Berlin – entdecke, was für deinen Auftritt möglich ist.</span></a>')}`,

  privacy: () => `<span class="guide-tag">DESIGNENTWURF</span><h2 class="dialog-heading" id="dialog-title">Datenschutz</h2><p class="dialog-intro">Diese Website wird von Patrick Vach, VachSystems, Charlottenburger Str. 142, 13086 Berlin, betrieben und über GitHub Pages bereitgestellt. Kontakt zum Betreiber: <a href="mailto:contact@vachsystems.de">contact@vachsystems.de</a>. Weitere Hinweise stehen in den <a href="https://vachsystems.de/datenschutz.html">Datenschutzhinweisen von vachsystems</a>.</p>${section('Notizen und Checkliste','<p>Die Eingaben der Sichtungsnotiz und die Häkchen der Checkliste werden ausschließlich im Arbeitsspeicher dieser geöffneten Seite gehalten. Sie werden durch diese Funktionen nicht an das Helfernetz gesendet und beim Neuladen verworfen.</p>')}${section('Flyer-Generator','<p>Foto und Formulareingaben werden ausschließlich lokal im Browser verarbeitet. Der Generator sendet diese Daten nicht an einen Server und speichert sie nicht dauerhaft. Die heruntergeladene PDF enthält die von dir eingegebenen Angaben.</p>')}${section('Externe Links','<p>Links zu TASSO und FINDEFIX öffnen die jeweiligen externen Websites. Dort gelten deren Datenschutzhinweise.</p>')}<p class="dialog-muted">Diese Hinweise werden noch um die konkreten Abläufe der E-Mail- und Telefonbearbeitung im Helferteam ergänzt.</p>`
};

function updateChecklist(){
  const progress = content.querySelector('.check-progress');
  if(!progress) return;
  progress.setAttribute('aria-valuenow',String(checklistState.size));
  progress.firstElementChild.style.width=`${checklistState.size/checklist.length*100}%`;
  content.querySelector('.check-count').textContent=`${checklistState.size} von ${checklist.length} Punkten abgehakt`;
}
function openView(name,trigger){
  if(!view[name]) return;
  const currentNotes=content.querySelector('#sighting-notes');
  if(currentNotes) sightingDraft=currentNotes.value;
  if(!dialog.open) lastTrigger=trigger?.closest("#site-menu") ? document.querySelector(".menu-toggle") : trigger;
  content.innerHTML=view[name]();
  if(!dialog.open){dialog.showModal();document.body.style.overflow='hidden';}
  dialog.scrollTop=0;
  if(name==='checklist') updateChecklist();
  if(name==='found') content.querySelector('#sighting-notes').value=sightingDraft;
  const title=content.querySelector('#dialog-title');
  title.setAttribute('tabindex','-1');title.focus({preventScroll:true});
}
document.addEventListener('click',event=>{
  const trigger=event.target.closest('[data-open]');
  if(trigger){event.preventDefault();if(siteMenu.open){menuFocusTarget=menuToggle;siteMenu.close();}openView(trigger.dataset.open,trigger);}
});
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
dialog.addEventListener('close',()=>{const notes=content.querySelector('#sighting-notes');if(notes)sightingDraft=notes.value;document.body.style.overflow='';lastTrigger?.focus({preventScroll:true});});
content.addEventListener('change',event=>{if(event.target.matches('[data-check]')){const i=Number(event.target.dataset.check);event.target.checked?checklistState.add(i):checklistState.delete(i);updateChecklist();}});
content.addEventListener('input',event=>{if(event.target.id==='sighting-notes')sightingDraft=event.target.value;});
content.addEventListener('click',async event=>{
  if(event.target.closest('#reset-checklist')){checklistState.clear();content.querySelectorAll('[data-check]').forEach(input=>input.checked=false);updateChecklist();}
  if(event.target.closest('#copy-sighting')){
    const field=content.querySelector('#sighting-notes');const status=content.querySelector('#copy-status');
    if(!field.value.trim()){status.textContent='Trage zuerst deine Beobachtung ein.';field.focus();return;}
    try{if(!navigator.clipboard)throw new Error('Clipboard unavailable');await navigator.clipboard.writeText(field.value);status.textContent='Kopiert. Du kannst die Notiz jetzt in deine Nachricht einfügen.';}
    catch{field.focus();field.select();status.textContent='Bitte kopiere die markierte Notiz über die Kopierfunktion deines Geräts.';}
  }
});
if(CONTACT.display) document.querySelectorAll('[data-phone-label]').forEach(node=>node.textContent=CONTACT.display);

// Native modal navigation: focus stays inside the menu until it is closed.
const siteMenu = document.querySelector('#site-menu');
const menuToggle = document.querySelector('.menu-toggle');
const menuClose = document.querySelector('.menu-close');
let menuFocusTarget = null;
menuToggle.addEventListener('click', () => {
  menuFocusTarget = null;
  siteMenu.showModal();
  menuToggle.setAttribute('aria-expanded', 'true');
  document.body.style.overflow = 'hidden';
  menuClose.focus({preventScroll:true});
});
menuClose.addEventListener('click', () => siteMenu.close());
siteMenu.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (!link) return;
  menuFocusTarget = document.querySelector(link.getAttribute('href'));
  if (menuFocusTarget) menuFocusTarget.setAttribute('tabindex', '-1');
  siteMenu.close();
});
siteMenu.addEventListener('close', () => {
  menuToggle.setAttribute('aria-expanded', 'false');
  if (dialog.open) return;
  document.body.style.overflow = '';
  (menuFocusTarget || menuToggle).focus({preventScroll:true});
  menuFocusTarget = null;
});

document.addEventListener('click', event => { if(event.target.closest('[data-flyer-link]')) { event.preventDefault(); dialog.close(); const flyer = document.querySelector('#flyer'); if (flyer) flyer.scrollIntoView({behavior:'smooth'}); else window.location.href = '/#flyer'; } });

// A deliberate, short moment of play. Never runs over content or the emergency dock.
(() => {
  const stage = document.querySelector('#cat-walk');
  const button = document.querySelector('#cat-walk-button');
  const runner = document.querySelector('#cat-runner');
  const status = document.querySelector('#cat-walk-status');
  if (!stage || !button || !runner) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let timer;
  function finish() {
    clearTimeout(timer);
    stage.classList.remove('is-walking');
    stage.classList.add('is-home');
    button.disabled = false;
    button.firstChild.textContent = 'Noch eine Runde auf Samtpfoten ';
    status.textContent = 'Angekommen. Genau das wünschen wir jeder Katze.';
  }
  button.addEventListener('click', () => {
    stage.classList.remove('is-home');
    status.textContent = '';
    if (reduced.matches) { finish(); return; }
    button.disabled = true;
    stage.classList.add('is-walking');
    timer = setTimeout(finish, 4000);
  });
  runner.addEventListener('animationend', event => {
    if (event.animationName === 'cat-cross') finish();
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches && stage.classList.contains('is-walking')) finish();
  });
})();
