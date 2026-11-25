#!/usr/bin/env python3
"""Erzeugt die Website "Dein Weg. Dein Abschluss." (index.html + je Bildungsgang eine Seite).

Aufruf: python3 gen2.py <repo-ordner>
Inhalte ändern (optional pro Bildungsgang: intro="Einführungstext"): unten in PAGES, PHOTOS, INFOTAG_TEXT usw. – nicht in den HTML-Dateien.
"""
import html, json, pathlib, sys

OUT = pathlib.Path(sys.argv[1])
e = html.escape
ANMELDE_URL = "https://www.berufskolleg.biz/schuelerinnen-und-schueler/anmeldung/"

# ---------------------------------------------------------------- Inhalte
PAGES = [
    dict(key="av", file="av.html", kurz="AV", nr=1, color="#0e8fa0",
         name="Ausbildungsvorbereitung", alias=None,
         claim="Für dich, wenn du (noch) keinen Abschluss hast.",
         voraussetzung="Kein Abschluss nötig", dauer="1 Jahr", abschluss="Erster Schulabschluss",
         punkte=["3 Tage Praktikum (Mo–Mi), 2 Tage Schule (Do + Fr)", "Unterricht nah an echten Betriebssituationen",
                 "Schulsozialarbeit und persönliche Beratung", "Hilfe bei Berufswahl und Praktikumssuche"],
         hinweis="Den Praktikumsplatz suchst du dir vor Schuljahresbeginn selbst – am besten in einem Betrieb, der auch ausbildet. Die AV kann auch als 10. Pflichtschuljahr besucht werden.",
         danach="Mit dem Ersten Schulabschluss weiter in die Berufsfachschule 1 (Handelsschule HS 9) – oder direkt in eine Ausbildung.",
         next="bfs1", bild="bg-av", gruppe="schule",
         wahl="Noch keinen Abschluss", wahl_info="Schulpflicht in der Sek. I erfüllt"),
    dict(key="bfs1", file="bfs1.html", kurz="BFS 1", nr=2, color="#0c71c3",
         name="Berufsfachschule 1", alias="Handelsschule HS 9",
         claim="Kaufmännische Grundlagen – und dein nächster Abschluss.",
         voraussetzung="Erster Schulabschluss", dauer="1 Jahr", abschluss="Erweiterter Erster Schulabschluss",
         punkte=["Geschäftsprozesse, Mathe, Englisch, Deutsch", "30 Praktikumstage: 1 Woche im Herbst, dann 1 Tag pro Woche",
                 "Kleine Klassen, Schwerpunkt Einzelhandel", "Enge Zusammenarbeit mit der Agentur für Arbeit"],
         danach="Weiter in die Berufsfachschule 2 (Handelsschule HS 10) zum Mittleren Schulabschluss – oder in eine Ausbildung.",
         next="bfs2", bild="bg-bfs1", gruppe="schule",
         wahl="Erster Schulabschluss", wahl_info="früher: Hauptschulabschluss nach Klasse 9"),
    dict(key="bfs2", file="bfs2.html", kurz="BFS 2", nr=3, color="#6a4fd8",
         name="Berufsfachschule 2", alias="Handelsschule HS 10",
         claim="Dein Weg zum Mittleren Schulabschluss.",
         voraussetzung="Erweiterter Erster Schulabschluss", dauer="1 Jahr", abschluss="Mittlerer Schulabschluss (FOR)",
         punkte=["Geschäftsprozesse, Wirtschaft, Mathe, Englisch", "30 Praktikumstage im kaufmännischen Bereich",
                 "Mit guten Noten: Berechtigung für die Oberstufe", "Unterstützung bei der Ausbildungsplatzsuche"],
         hinweis="Auch möglich: nach Klasse 9 des Gymnasiums mit der Berechtigung für die Oberstufe.",
         danach="Weiter in die Höhere Berufsfachschule oder die gymnasiale Oberstufe – oder in eine Ausbildung.",
         next="hbfs", bild="bg-bfs2", gruppe="schule",
         wahl="Erweiterter Erster Schulabschluss", wahl_info="früher: Hauptschulabschluss nach Klasse 10"),
    dict(key="hbfs", file="hoehere-berufsfachschule.html", kurz="HBFS", nr=4, color="#1a9070",
         name="Höhere Berufsfachschule", alias="Höhere Handelsschule",
         claim="Wirtschaft verstehen – mit Fachhochschulreife.",
         voraussetzung="Mittlerer Schulabschluss (FOR)", dauer="2 Jahre", abschluss="Fachhochschulreife (schulischer Teil)",
         punkte=["Abschlussfächer: BWL mit Rechnungswesen, Deutsch, Mathe, Englisch",
                 "Zur Wahl: Gesundheitscoaching, Spanisch oder Französisch",
                 "2 Wochen Betriebspraktikum im ersten Jahr", "Aufnahme mit FOR – mit oder ohne Q-Vermerk"],
         danach="Mit Praktikum oder Ausbildung zur vollen Fachhochschulreife – dann Ausbildung oder Studium an einer FH.",
         next="bs", bild="bg-hbfs", gruppe="schule",
         wahl="Mittlerer Schulabschluss (FOR)", wahl_info="oder Versetzung in die Oberstufe (Gymnasium)",
         hinweis="Bei der Anmeldung brauchst du einen tabellarischen Lebenslauf und eine Kopie deines letzten Zeugnisses."),
    dict(key="if", file="internationale-foerderklassen.html", kurz="IF", nr=5, color="#d0466f",
         name="Internationale Förderklassen", alias=None, gruppe="schule",
         claim="Für dich, wenn du neu in Deutschland bist und Deutsch lernst.",
         voraussetzung="Neu zugewandert, ab 16 Jahren", dauer="1 Jahr (bei wenig Deutsch: 2 Jahre)", abschluss="Erster Schulabschluss (vergleichbar)",
         punkte=["Deutsch lernen – auch die Fachsprache", "Mathe, Englisch und kaufmännische Fächer",
                 "Zwei Wochen Praktikum und Berufsorientierung", "Begleitung durch Schulsozialarbeit und Berufsorientierungsbüro (BOB)"],
         danach="Mit dem Abschluss weiter in einen anderen Bildungsgang am Berufskolleg – oder in eine Ausbildung.",
         next="bfs1", bild="bg-if",
         wahl="Neu in Deutschland", wahl_info="und du lernst noch Deutsch",
         anmelde_url="tel:+4921612553784", anmelde_label="Beratung: Kommunale Integrationsstelle",
         hinweis="Die Aufnahme läuft nicht direkt über uns, sondern über die Kommunale Integrationsstelle (KI) der Stadt Mönchengladbach: Telefon 02161 / 25-53784, ki@moenchengladbach.de."),
    dict(key="bs", file="berufsschule.html", kurz="BS", nr=6, color="#c58500",
         name="Berufsschule", alias="Duale Ausbildung", gruppe="beruf",
         claim="Du machst eine kaufmännische Ausbildung – wir sind deine Berufsschule.",
         voraussetzung="Ausbildungsvertrag", dauer="2 bis 3 Jahre", abschluss="Berufsabschluss + Berufsschulabschluss",
         punkte=["Unterricht an 1 bis 2 Tagen pro Woche, die übrige Zeit im Betrieb", "Fächer passend zu deinem Beruf, dazu Deutsch, Englisch, Politik",
                 "Einzelhandel, Groß- und Außenhandel, Büromanagement am Teilstandort Bruchstraße", "Dein Betrieb meldet dich bei uns an"],
         danach="Mit Berufsabschluss und Berufserfahrung weiter zur Fachschule für Wirtschaft – bis zum Bachelor Professional.",
         next="fs", bild="schule-front",
         wahl="Ich habe einen Ausbildungsplatz", wahl_info="kaufmännische Ausbildung",
         anmelde_url="https://www.berufskolleg.biz/schuelerinnen-und-schueler/anmeldung/anmeldung-berufsschule/", anmelde_label="Anmeldung Berufsschule (für Betriebe)",
         berufe=[("Kaufleute im Einzelhandel", "3 Jahre", "https://www.berufskolleg.biz/einzelhandelskaufleute/"),
                 ("Verkäuferin / Verkäufer", "2 Jahre", "https://www.berufskolleg.biz/verkaeuferinnen-und-verkaeufer/"),
                 ("Automobilkaufleute", "3 Jahre", "https://www.berufskolleg.biz/automobilkaufleute/"),
                 ("Industriekaufleute", "3 Jahre", "https://www.berufskolleg.biz/industriekaufleute/"),
                 ("Kaufleute im Groß- und Außenhandel", "3 Jahre", "https://www.berufskolleg.biz/gross-und-aussenhandelskaufleute/"),
                 ("Kaufleute für Büromanagement", "3 Jahre", "https://www.berufskolleg.biz/kaufleute-fuer-bueromanagement/")]),
    dict(key="fs", file="fachschule.html", kurz="FS", nr=7, color="#d8622a",
         name="Fachschule für Wirtschaft", alias="Schwerpunkt Personalwirtschaft · Weiterbildung", gruppe="beruf",
         claim="Weiterbildung neben dem Beruf – für Führungsaufgaben im mittleren Management.",
         voraussetzung="Ausbildung + 1 Jahr Beruf + FOR", dauer="8 Semester (mit FHR ggf. 6)", abschluss="Bachelor Professional (Staatl. gepr. Betriebswirt/in)",
         punkte=["Personalwirtschaft, BWL, Rechnungswesen, Wirtschaftsinformatik", "Befreiung von der Ausbildereignungsprüfung möglich",
                 "Vorbereitung auf Selbstständigkeit (Existenzgründung)", "Ohne FOR: Aufnahme mit 5 Jahren Berufserfahrung möglich"],
         danach="Mehr Verantwortung im Beruf: Führungsaufgaben, Personalverantwortung oder der Schritt in die Selbstständigkeit.",
         next=None, bild="schule-eingang",
         wahl="Ausbildung abgeschlossen", wahl_info="und du willst dich weiterbilden",
         anmelde_url="https://www.berufskolleg.biz/schuelerinnen-und-schueler/anmeldung/weiterbildung-buttons/anmeldung-fachschule/", anmelde_label="Anmeldung Fachschule"),
]
BY = {p["key"]: p for p in PAGES}

# Bildergalerie "Unsere Schule": weitere Fotos einfach hier ergänzen
# (Datei als assets/img/<name>-1200.webp und -640.webp ablegen).
PHOTOS = [
    ("schulhof-gruppe", "Pause vor dem Schulgebäude"),
    ("schueler-gruppe", "Gemeinsam lernen im Klassenraum"),
    ("teamuebung", "Teamübung auf dem Schulgelände"),
    ("schule-front", "Das Schulgebäude des Berufskollegs Rheydt-Mülfort"),
    ("schule-eingang", "Der Eingang zum Schulgelände"),
]

INFOTAG_TEXT = "Weitere Infos zum Infotag folgen."  # TEXT VON HERRN ELSEN FOLGT

# ---------------------------------------------------------------- Design
CSS = """
/* Design angelehnt an klare Hochschul-Webseiten: hell, sachlich, weiße Karten, Fotos mit Titelbalken */
:root{
  --bg:#f5f5f5; --white:#fff; --text:#1d1d1f; --muted:#5f6470; --line:#e2e3e7;
  --navy:#090058; --blue:#0c71c3; --accent:#0c71c3; --accent-h:#095ea3;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 6px 18px rgba(0,0,0,.06);
  --r:3px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;font-size:17px;line-height:1.55;-webkit-text-size-adjust:100%;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:var(--blue)}
.wrap{max-width:1160px;margin:0 auto;padding:0 16px}
@media (min-width:720px){.wrap{padding:0 28px}}
h1,h2,h3{color:var(--text);margin:0;font-weight:700;line-height:1.2}
.eyebrow{display:block;text-transform:uppercase;letter-spacing:.08em;font-size:.8rem;font-weight:700;color:var(--blue);margin:0 0 8px}
.display{font-weight:700}
h2.display{font-size:clamp(1.6rem,4.5vw,2.3rem);margin-bottom:10px;color:var(--navy)}
.lead{font-size:1.08rem;color:var(--muted);max-width:700px;margin:0 0 26px}

/* Kopfzeile */
.site-header{position:sticky;top:0;z-index:50;background:var(--white);border-bottom:1px solid var(--line);transition:box-shadow .2s}
.site-header.scrolled{box-shadow:0 2px 10px rgba(0,0,0,.08)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px;height:76px}
.site-header img{height:50px;width:auto}
.hdr-right{display:flex;align-items:center;gap:26px}
.nav{display:flex;gap:24px}
.nav a{color:var(--text);text-decoration:none;font-size:1rem;padding:6px 0;border-bottom:2px solid transparent}
.nav a:hover{color:var(--blue);border-bottom-color:var(--blue)}
@media (max-width:860px){.nav{display:none}.site-header .wrap{height:64px}.site-header img{height:40px}}

/* Buttons */
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:var(--r);padding:11px 20px;text-decoration:none;font-weight:700;font-size:.95rem;border:2px solid var(--blue);color:var(--blue);background:var(--white);transition:background .15s,color .15s;cursor:pointer;line-height:1.2}
.btn:hover{background:var(--blue);color:#fff}
.btn.solid{background:var(--blue);color:#fff}
.btn.solid:hover{background:var(--accent-h);border-color:var(--accent-h)}
button.btn{font-family:inherit}
.btn.small{padding:8px 14px;font-size:.88rem}
.btns{display:flex;flex-wrap:wrap;gap:12px}

/* Foto-Kopf mit Titelbalken */
.hero,.bg-hero{position:relative;isolation:isolate;background:#222;min-height:clamp(300px,52vw,520px);display:flex;align-items:flex-end;padding:0 0 32px}
.hero-bg{position:absolute;inset:0;z-index:-1}
.hero::after,.bg-hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.35))}
.hero .wrap,.bg-hero .wrap{width:100%}
.titlebar{display:inline-block;background:var(--navy);color:#fff;padding:14px 22px 16px;max-width:100%;box-shadow:0 4px 18px rgba(0,0,0,.25)}
.titlebar .eyebrow{color:#9fd0ff;margin-bottom:4px}
.titlebar h1{color:#fff;font-size:clamp(1.6rem,5vw,2.6rem);font-weight:700;hyphens:auto;overflow-wrap:break-word}
.titlebar .alias{color:#d6dcf5;margin:4px 0 0;font-size:1rem}
.bg-hero .titlebar{border-left:8px solid var(--c)}
@media (max-width:600px){.hero,.bg-hero{min-height:300px;padding-bottom:18px}.titlebar{padding:10px 14px 12px}.titlebar .eyebrow{font-size:.68rem;letter-spacing:.05em}.titlebar h1{font-size:1.5rem}.titlebar .alias{font-size:.9rem}}

/* Karten */
.glass{background:var(--white);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}

/* Schulberater */
.berater-sec{padding:0 0 56px}
.berater-box{background:var(--white);box-shadow:var(--shadow);padding:26px 22px 28px;margin-top:-1px;border-top:4px solid var(--blue)}
@media (min-width:720px){.berater-box{padding:34px 36px 36px}}
.berater{scroll-margin-top:90px}
.q{font-size:clamp(1.35rem,3.8vw,1.85rem);color:var(--navy);margin:6px 0 4px}
.qsub{color:var(--muted);margin:0 0 18px}
.choices{display:grid;gap:12px;grid-template-columns:1fr}
@media (min-width:760px){.choices{grid-template-columns:1fr 1fr}}
.choice{display:flex;align-items:center;gap:16px;padding:16px 18px;text-decoration:none;color:var(--text);position:relative;overflow:hidden;transition:box-shadow .15s,transform .15s,border-color .15s;border-left:5px solid var(--c)}
.choice:hover{box-shadow:0 6px 22px rgba(0,0,0,.12);transform:translateY(-1px);border-color:var(--c)}
.choice .num{flex:none;width:40px;height:40px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:700;font-size:1.05rem}
.choice b{display:block;color:var(--text);font-size:1.08rem}
.choice small{display:block;color:var(--muted);font-size:.9rem}
.choice .to{display:block;color:var(--c);font-weight:700;font-size:.9rem;margin-top:3px;filter:brightness(.8)}
.choice .go{margin-left:auto;color:var(--c);font-size:1.7rem;font-weight:400}
.group-label{color:var(--navy);font-weight:700;font-size:1.05rem;margin:24px 0 10px}
button.choice{font:inherit;width:100%;text-align:left;cursor:pointer;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
button.choice:focus-visible,.b-back:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.b-top{display:flex;justify-content:space-between;align-items:center;margin:0 0 6px;min-height:34px}
.b-back{background:none;border:0;color:var(--blue);font:inherit;font-weight:700;font-size:.95rem;cursor:pointer;padding:6px 0}
.b-back:hover{text-decoration:underline}
.dots{display:flex;gap:6px}.dot{width:30px;height:5px;background:var(--line)}.dot.on{background:var(--blue)}
.result{padding:24px;border-top:5px solid var(--c)}
.result .badge{display:inline-block;background:var(--c);color:#fff;font-weight:700;padding:4px 12px;margin-bottom:10px;border-radius:var(--r)}
.result h2{font-size:clamp(1.6rem,5vw,2.3rem);color:var(--navy);hyphens:auto;overflow-wrap:break-word}
.result .alias{color:var(--muted);margin:4px 0 0}
.result .claim{font-size:1.1rem;margin:10px 0 18px}
.result .beruf{margin:-6px 0 18px}
.result h3{font-size:1.05rem;color:var(--navy);margin:24px 0 10px}
.result .fact{box-shadow:none}
.path{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.chip{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);border-left:4px solid var(--c);padding:6px 12px 6px 8px;color:var(--text);text-decoration:none;font-weight:600;font-size:.95rem;background:var(--white);border-radius:var(--r)}
.chip .lvl{background:var(--c);color:#fff;padding:1px 7px;font-size:.78rem;font-weight:700;border-radius:2px}
a.chip:hover{box-shadow:var(--shadow)}
.arrow{color:var(--muted)}
.tips{margin:18px 0 0;padding-left:20px}.tips li{margin:6px 0}
.btn.ghost-muted{border-color:var(--line);color:var(--muted)}
.btn.ghost-muted:hover{background:var(--bg);color:var(--text)}
.hint{color:var(--muted);font-size:.95rem;margin:16px 0 0}

/* Abschnitte */
section{padding:60px 0;position:relative}
section.alt{background:var(--white)}
.cards3{display:grid;gap:18px;grid-template-columns:1fr}
@media (min-width:760px){.cards3{grid-template-columns:repeat(3,1fr)}}
.card{padding:24px;border-top:4px solid var(--blue)}
.card .ic{width:48px;height:48px;border-radius:50%;background:#e6f1fb;display:grid;place-items:center;margin-bottom:14px}
.card .ic img{width:26px;height:26px;filter:brightness(0) saturate(100%) invert(27%) sepia(89%) saturate(1500%) hue-rotate(195deg)}
.card h3{font-size:1.15rem;margin-bottom:6px;color:var(--navy)}
.card p{margin:0;color:var(--muted)}

/* Galerie */
.gallery{display:grid;gap:18px;grid-template-columns:1fr}
@media (min-width:760px){.gallery{grid-template-columns:repeat(2,1fr)}}
.gallery figure:first-child{grid-column:1/-1;aspect-ratio:16/8}
.gallery figure{margin:0;background:var(--white);box-shadow:var(--shadow);position:relative;aspect-ratio:3/2;overflow:hidden}
.gallery img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.gallery figure:hover img{transform:scale(1.03)}
.gallery figcaption{position:absolute;left:0;bottom:16px;max-width:90%;padding:8px 14px;background:var(--navy);color:#fff;font-size:.95rem;font-weight:600}

/* Stufen */
.stairs{display:grid;gap:10px}
.step{display:flex;align-items:center;gap:16px;padding:14px 18px;text-decoration:none;color:var(--muted);border-left:5px solid var(--c)}
.step:hover{box-shadow:0 6px 22px rgba(0,0,0,.12)}
.step b{color:var(--text);font-size:1.05rem}
.step .lvl{flex:none;min-width:64px;text-align:center;font-weight:700;color:#fff;background:var(--c);padding:4px 10px;font-size:.85rem;border-radius:2px}
@media (min-width:760px){.step:nth-child(2){margin-left:5%}.step:nth-child(3){margin-left:10%}.step:nth-child(4){margin-left:15%}.step:nth-child(5){margin-left:20%}.step:nth-child(6){margin-left:25%}}
.note{padding:16px 20px;margin-top:20px;border-left:5px solid var(--blue);background:#eef5fc;box-shadow:none;border-top:0;border-right:0;border-bottom:0}
.note b{color:var(--navy)}

/* Berufe */
.jobs{display:grid;gap:12px;grid-template-columns:1fr 1fr}
@media (min-width:760px){.jobs{grid-template-columns:repeat(3,1fr)}}
.job{min-width:0;hyphens:auto;overflow-wrap:break-word;padding:14px 16px;color:var(--text);font-weight:700;border-left:4px solid var(--blue)}
.job small{display:block;color:var(--muted);font-weight:400;font-size:.85rem}
a.job:hover{box-shadow:0 6px 22px rgba(0,0,0,.12)}

/* Infotag */
.infotag{display:flex;gap:24px;align-items:center;padding:24px;border-left:6px solid var(--blue)}
.it-date{flex:none;width:92px;text-align:center;background:var(--navy);color:#fff;padding:10px 0;line-height:1.1;font-weight:700;text-transform:uppercase;font-size:.78rem}
.it-date b{display:block;font-size:2.4rem;font-weight:700}
.infotag h2{font-size:clamp(1.2rem,3.5vw,1.6rem);color:var(--navy);margin-bottom:6px}
.placeholder-note{color:var(--muted);margin:0}
@media (max-width:520px){.infotag{flex-direction:column;align-items:flex-start}}

/* Anmeldung */
.reg{display:grid;gap:22px;grid-template-columns:1fr}
@media (min-width:860px){.reg{grid-template-columns:1.5fr 1fr}}
.regstep{display:flex;gap:16px;margin-bottom:20px}
.regstep .n{flex:none;width:40px;height:40px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center;font-weight:700}
.regstep h3{font-size:1.1rem;margin:0 0 2px;color:var(--navy)}
.regstep p{margin:0;color:var(--muted)}

/* Präsentation */
.viewer{padding:14px}
.viewer img{width:100%;aspect-ratio:16/9;object-fit:contain;background:#0b0e24}
.vctrl{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:12px;color:var(--muted)}
.dl{margin-top:18px}

/* Kontakt / Fußzeile */
#kontakt{background:var(--navy);color:#dfe3f5}
#kontakt h2.display{color:#fff}
#kontakt .eyebrow{color:#9fd0ff}
#kontakt .lead{color:#c9cfea}
.contact{display:grid;gap:10px;font-size:1.15rem}
.contact a{color:#fff;text-decoration:none;font-weight:700}
.contact a:hover{text-decoration:underline}
footer{background:#393939;color:#d0d0d0;font-size:.9rem;padding:20px 0}
footer a{color:#fff}

/* Bildungsgang-Seite */
.pagebar{background:var(--white);border-bottom:1px solid var(--line);padding:22px 0 24px}
.back{display:inline-flex;align-items:center;gap:6px;color:var(--blue);text-decoration:none;font-weight:700;font-size:.95rem;margin-bottom:12px}
.back:hover{text-decoration:underline}
.pagebar .claim{font-size:clamp(1.1rem,2.6vw,1.3rem);margin:0 0 18px;max-width:720px}
.facts{display:grid;gap:12px;grid-template-columns:repeat(3,1fr)}
@media (max-width:680px){.facts{grid-template-columns:1fr}}
.fact{padding:14px 18px;border-top:4px solid var(--c)}
.fact span{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.fact b{color:var(--text);font-size:1.05rem}
.textbox{padding:20px 22px;border-left:5px solid var(--c)}
.two{display:grid;gap:18px;grid-template-columns:1fr}
@media (min-width:860px){.two{grid-template-columns:1.4fr 1fr}}
.panel{padding:22px 24px}
.panel h2{font-size:1.25rem;color:var(--navy);margin-bottom:10px}
.panel ul{margin:0;padding-left:0;list-style:none}
.panel li{padding:8px 0 8px 26px;position:relative;border-bottom:1px solid var(--line)}
.panel li:last-child{border-bottom:0}
.panel li::before{content:"›";position:absolute;left:6px;top:5px;color:var(--c);font-weight:700;font-size:1.2em}
.next{padding:22px 24px;background:var(--navy);color:#e3e6f6;border-top:5px solid var(--c)}
.next h2{color:#fff}
.next a{color:#fff;font-weight:700}
.stack>*+*{margin-top:18px}
section.tight{padding:32px 0}
"""

JS_HEADER = """<script>
(()=>{const h=document.querySelector('.site-header');const f=()=>h.classList.toggle('scrolled',scrollY>20);f();addEventListener('scroll',f,{passive:true});})();
</script>"""


# ---------------------------------------------------------------- Bausteine
def head(title, desc, preload=None):
    pl = f'<link rel="preload" as="image" href="assets/img/{preload}-1200.webp" imagesrcset="assets/img/{preload}-640.webp 640w, assets/img/{preload}-1200.webp 1200w" imagesizes="100vw">' if preload else ""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#090058">
<link rel="icon" href="assets/icon-abschluss.png">
{pl}
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
"""


def header(nav):
    return f"""<header class="site-header"><div class="wrap">
  <a href="index.html" aria-label="Zur Startseite"><img src="assets/logo.png" alt="Berufskolleg Rheydt-Mülfort – für Wirtschaft und Verwaltung" width="655" height="217"></a>
  <div class="hdr-right"><nav class="nav">{nav}</nav><a class="btn small solid" href="{ANMELDE_URL}" target="_blank" rel="noopener">Anmelden</a></div>
</div></header>
"""


def hero_bg(name):
    # <img> statt CSS-Hintergrund, damit das Handy die kleine Version lädt
    return f"""<img class="hero-bg" src="assets/img/{name}-1200.webp" srcset="assets/img/{name}-640.webp 640w, assets/img/{name}-1200.webp 1200w" sizes="100vw" alt="" style="width:100%;height:100%;object-fit:cover" fetchpriority="high">"""


INFOTAG = f"""<section id="infotag" class="tight"><div class="wrap">
  <div class="infotag glass">
    <div class="it-date">Sa<b>13</b>Feb 2027</div>
    <div>
      <span class="eyebrow">Infotag</span>
      <h2>Komm vorbei: Infotag am Samstag, 13. Februar 2027</h2>
      <p class="placeholder-note">{e(INFOTAG_TEXT)}</p>
    </div>
  </div>
</div></section>
"""

ANMELDUNG_STEPS = """<div class="regstep"><div class="n">1</div><div><h3>Online bewerben</h3><p>Auf <a href="https://www.schulbewerbung.de" target="_blank" rel="noopener">schulbewerbung.de</a> – mit dem Startcode deiner jetzigen Schule.</p></div></div>
      <div class="regstep"><div class="n">2</div><div><h3>Ausdrucken und unterschreiben</h3><p>Anmeldeformular und Datenschutz-Einwilligung im Sekretariat abgeben. Unter 18: Eltern unterschreiben mit.</p></div></div>
      <div class="regstep"><div class="n">3</div><div><h3>Zeugnis mitbringen</h3><p>Kopie deines letzten Zeugnisses. Höhere Berufsfachschule: dazu ein tabellarischer Lebenslauf.</p></div></div>"""


def anmeldung(extra=""):
    return f"""<section id="anmeldung" class="alt"><div class="wrap">
  <span class="eyebrow">Anmeldung</span>
  <h2 class="display">So meldest du dich an</h2>
  <div class="reg" style="margin-top:28px">
    <div>
      {ANMELDUNG_STEPS}
    </div>
    <div class="glass card">
      <h3>Alle Infos zur Anmeldung</h3>
      <p style="margin-bottom:18px">Formulare, Fristen und Details findest du auf unserer Homepage.</p>
      <a class="btn solid" href="{ANMELDE_URL}" target="_blank" rel="noopener">Zur Anmeldung ›</a>
    </div>
  </div>
  {extra}
</div></section>
"""


KONTAKT = """<section id="kontakt"><div class="wrap">
  <span class="eyebrow">Kontakt</span>
  <h2 class="display">Dein Weg beginnt hier.</h2>
  <p class="lead">Wir beraten dich gern – auch direkt an deiner Schule.</p>
  <div class="contact">
    <a href="tel:+492166917920">02166-917920</a>
    <a href="mailto:info@berufskolleg.biz">info@berufskolleg.biz</a>
    <a href="https://www.berufskolleg.biz" target="_blank" rel="noopener">www.berufskolleg.biz</a>
  </div>
</div></section>
<footer><div class="wrap">Berufskolleg Rheydt-Mülfort · Mönchengladbach · <a href="https://www.berufskolleg.biz">www.berufskolleg.biz</a></div></footer>
"""


def full_name(p):
    return p["name"] + (f" ({p['alias']})" if p["alias"] else "")


def gallery():
    figs = "".join(
        f"""<figure><img src="assets/img/{n}-640.webp" srcset="assets/img/{n}-640.webp 640w, assets/img/{n}-1200.webp 1200w" sizes="(min-width:760px) 50vw, 100vw" alt="{e(alt)}" loading="lazy"><figcaption>{e(alt)}</figcaption></figure>"""
        for n, alt in PHOTOS)
    return f'<div class="gallery">{figs}</div>'


def berater_json():
    keys = ["kurz", "name", "alias", "claim", "voraussetzung", "dauer", "abschluss", "color", "file", "anmelde_url", "anmelde_label", "berufe"]
    data = {p["key"]: {k: p.get(k) for k in keys} for p in PAGES}
    for d in data.values():
        if d["berufe"]:
            d["berufe"] = [[n, dur] for n, dur, _ in d["berufe"]]
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


# ---------------------------------------------------------------- Seiten
def index():
    ORDER = ["av", "if", "bfs1", "bfs2", "hbfs", "bs", "fs"]
    def ch(i, p):
        return f"""<a class="choice glass" style="--c:{p['color']}" href="{p['file']}"><span class="num">{i}</span>
      <span><b>{e(p['wahl'])}</b><small>{e(p['wahl_info'])}</small><span class="to">→ {e(p['name'])}</span></span><span class="go" aria-hidden="true">›</span></a>
    """
    ordered = [BY[k] for k in ORDER]
    schule = [p for p in ordered if p["gruppe"] == "schule"]
    beruf = [p for p in ordered if p["gruppe"] == "beruf"]
    choices = "".join(ch(i, p) for i, p in enumerate(schule, 1))
    choices_beruf = "".join(ch(i, p) for i, p in enumerate(beruf, len(schule) + 1))
    stairs = "".join(
        f"""<a class="step glass" style="--c:{p['color']}" href="{p['file']}"><span class="lvl">{e(p['kurz'])}</span><span><b>{e(full_name(p))}</b><br><span>→ {e(p['abschluss'])}</span></span></a>"""
        for p in [BY[k] for k in ["av", "bfs1", "bfs2", "hbfs", "bs", "fs"]])
    redirect = ",".join(f'"{k}":"{v}"' for k, v in
                        {"av": "av.html", "hs9": "bfs1.html", "hs10": "bfs2.html", "hoeha": "hoehere-berufsfachschule.html"}.items())
    return head("Dein Weg. Dein Abschluss. – Berufskolleg Rheydt-Mülfort",
                "Mit welchem Schulabschluss kommst du zu uns? Finde deinen Bildungsgang am Berufskolleg Rheydt-Mülfort in Mönchengladbach.",
                preload="schueler-gruppe") \
        + header('<a href="#schule">Unsere Schule</a><a href="#infotag">Infotag</a><a href="#praesentation">Präsentation</a><a href="#kontakt">Kontakt</a>') + f"""
<section class="hero">{hero_bg("schueler-gruppe")}<div class="wrap">
  <div class="titlebar"><span class="eyebrow">Berufskolleg Rheydt-Mülfort · Mönchengladbach</span>
  <h1>Dein Weg. Dein Abschluss.</h1></div>
</div></section>
<section class="berater-sec"><div class="wrap"><div class="berater-box">
  <span class="eyebrow">Schulberater</span>
  <div id="berater" class="berater" aria-live="polite">
  <h2 class="q">Mit welchem Schulabschluss kommst du zu uns?</h2>
  <p class="qsub">Wähle deinen Abschluss – oder den, den du im Sommer bekommst.</p>
  <p class="group-label" style="margin-top:0">Du kommst von der Schule?</p>
  <div class="choices">
    {choices}</div>
  <p class="group-label">Du bist schon im Beruf?</p>
  <div class="choices">
    {choices_beruf}</div>
  </div>
  <p class="hint">Du bist unsicher? Ruf uns an unter <a href="tel:+492166917920">02166-917920</a> – wir beraten dich gern.</p>
</div></div></section>

{INFOTAG}
<section id="schule"><div class="wrap">
  <span class="eyebrow">Wer wir sind</span>
  <h2 class="display">Berufskolleg für Wirtschaft und Verwaltung</h2>
  <p class="lead">In Mönchengladbach – mitten zwischen Schule und Beruf.</p>
  <div class="cards3">
    <div class="glass card"><div class="ic"><img src="assets/icon-abschluss.png" alt=""></div><h3>Abschlüsse nachholen</h3><p>Vom Ersten Schulabschluss bis zur Fachhochschulreife – Schritt für Schritt.</p></div>
    <div class="glass card"><div class="ic"><img src="assets/icon-praxis.png" alt=""></div><h3>Praxis von Anfang an</h3><p>Praktika in echten Betrieben und Unterricht an echten kaufmännischen Aufgaben.</p></div>
    <div class="glass card"><div class="ic"><img src="assets/icon-begleitung.png" alt=""></div><h3>Begleitung bis zum Ziel</h3><p>Kleine Klassen, Schulsozialarbeit und enge Zusammenarbeit mit der Agentur für Arbeit.</p></div>
  </div>
  <div style="margin-top:22px">{gallery()}</div>
</div></section>

<section id="wege" class="alt"><div class="wrap">
  <span class="eyebrow">Entwicklungsmöglichkeiten</span>
  <h2 class="display">Schritt für Schritt nach oben</h2>
  <p class="lead">Tippe auf eine Stufe, um mehr zu erfahren.</p>
  <div class="stairs">{stairs}</div>
  <p class="note glass"><b>Reibungsloser Übergang:</b> Nach jeder Stufe kannst du weitermachen – oder direkt in eine Ausbildung starten. In der Ausbildung sind wir deine Berufsschule, danach geht es mit der Fachschule weiter. Neu in Deutschland? Dann startest du in den <a href="internationale-foerderklassen.html">Internationalen Förderklassen</a>.</p>
</div></section>

<section id="berufe"><div class="wrap">
  <span class="eyebrow">Ausbildungsberufe</span>
  <h2 class="display">Mit Abschluss in die Ausbildung</h2>
  <p class="lead">Als Berufsschule begleiten wir Azubis in diesen Berufen:</p>
  <div class="jobs">
    <div class="job glass">Einzelhandelskaufleute</div><div class="job glass">Verkäuferin / Verkäufer</div><div class="job glass">Automobilkaufleute</div>
    <div class="job glass">Industriekaufleute</div><div class="job glass">Groß- und Außenhandelskaufleute</div><div class="job glass">Kaufleute für Büromanagement</div>
  </div>
  <p class="btns" style="margin-top:18px"><a class="btn" href="berufsschule.html">Mehr zur Berufsschule ›</a></p>
  <p class="note glass"><b>Und noch viel mehr:</b> Bank, Versicherung, Steuer- und Rechtsanwaltskanzlei, Verwaltung, Immobilien, Arzt- und Zahnarztpraxis (MFA, ZFA), Polizei-Verwaltung …</p>
</div></section>

{anmeldung()}
<section id="praesentation"><div class="wrap">
  <span class="eyebrow">Präsentation</span>
  <h2 class="display">Die ganze Präsentation</h2>
  <p class="lead">Blättere durch alle Folien oder lade die Präsentation herunter.</p>
  <div class="viewer glass">
    <img id="slide" src="assets/folie-01.jpg" alt="Folie 1 der Präsentation" loading="lazy">
    <div class="vctrl">
      <button class="btn small" id="prev" aria-label="Vorherige Folie">‹ Zurück</button>
      <span id="slideNo">Folie 1 / 13</span>
      <button class="btn small" id="next" aria-label="Nächste Folie">Weiter ›</button>
    </div>
  </div>
  <div class="btns dl">
    <a class="btn solid" href="assets/Dein-Weg-Dein-Abschluss.pdf" download>PDF herunterladen</a>
    <a class="btn" href="assets/Dein-Weg-Dein-Abschluss.pptx" download>PowerPoint herunterladen</a>
  </div>
</div></section>

{KONTAKT}
{JS_HEADER}
<script>window.BILDUNGSGAENGE={berater_json()};window.ANMELDE_URL={json.dumps(ANMELDE_URL)};</script>
<script src="assets/berater.js" defer></script>
<script>
const R={{{redirect}}};const m=location.hash.match(/^#berater-(\\w+)$/);if(m&&R[m[1]])location.replace(R[m[1]]);
const N=13;let cur=1;const img=document.getElementById("slide"),no=document.getElementById("slideNo");
function show(n){{cur=(n+N-1)%N+1;const s=String(cur).padStart(2,"0");img.src=`assets/folie-${{s}}.jpg`;img.alt=`Folie ${{cur}} der Präsentation`;no.textContent=`Folie ${{cur}} / ${{N}}`;}}
document.getElementById("prev").onclick=()=>show(cur-1);document.getElementById("next").onclick=()=>show(cur+1);
let sx=null;img.addEventListener("touchstart",e=>sx=e.touches[0].clientX,{{passive:true}});
img.addEventListener("touchend",e=>{{if(sx===null)return;const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40)show(cur+(d<0?1:-1));sx=null;}});
</script>
</body>
</html>
"""


def berufe_html(p):
    if not p.get("berufe"):
        return ""
    items = "".join(f'<a class="job glass" href="{u}" target="_blank" rel="noopener" style="text-decoration:none">{e(n)}<small>{e(d)}</small></a>' for n, d, u in p["berufe"])
    return f'<div class="panel glass"><h2>Diese Berufe begleiten wir</h2><div class="jobs" style="margin-top:6px">{items}</div><p style="margin:14px 0 0;color:var(--muted)">Und noch viel mehr: Bank, Versicherung, Steuer- und Rechtsanwaltskanzlei, Verwaltung, Immobilien, Arzt- und Zahnarztpraxis (MFA, ZFA), Polizei-Verwaltung …</p></div>'


def page(p):
    nxt = BY[p["next"]] if p["next"] else None
    next_link = f'<p style="margin-top:14px"><a href="{nxt["file"]}">Weiter: {e(nxt["name"])} ›</a></p>' if nxt else ""
    back = '<a class="back" href="index.html">‹ Zur Startseite</a>'
    return head(f"{full_name(p)} – Berufskolleg Rheydt-Mülfort",
                f"{p['name']} am Berufskolleg Rheydt-Mülfort: {p['claim']}", preload=p["bild"]) \
        + header('<a href="index.html">Startseite</a><a href="#infotag">Infotag</a><a href="#kontakt">Kontakt</a>') + f"""
<section class="bg-hero" style="--c:{p['color']}">{hero_bg(p['bild'])}<div class="wrap">
  <div class="titlebar"><span class="eyebrow">Bildungsangebot · {e(p['kurz'])}</span>
  <h1>{e(p['name'])}</h1>
  {f'<p class="alias">{e(p["alias"])}</p>' if p['alias'] else ''}</div>
</div></section>
<div class="pagebar"><div class="wrap">
  {back}
  <p class="claim">{e(p['claim'])}</p>
  <div class="btns"><a class="btn solid" href="{p.get('anmelde_url', ANMELDE_URL)}" target="_blank" rel="noopener">{e(p.get('anmelde_label', 'Jetzt anmelden'))}</a><a class="btn" href="#infotag">Infotag 13.02.2027</a></div>
</div></div>

<section class="tight" style="--c:{p['color']}"><div class="wrap stack">
  {f'<div class="textbox glass"><p>{e(p["intro"])}</p></div>' if p.get('intro') else ''}

  <div class="facts">
    <div class="fact glass"><span>Voraussetzung</span><b>{e(p['voraussetzung'])}</b></div>
    <div class="fact glass"><span>Dauer</span><b>{e(p['dauer'])}</b></div>
    <div class="fact glass"><span>Abschluss</span><b>{e(p['abschluss'])}</b></div>
  </div>

  {f'<div class="glass note" style="margin-top:0"><b>Gut zu wissen:</b> {e(p["hinweis"])}</div>' if p.get('hinweis') else ''}
  {berufe_html(p)}
  <div class="two">
    <div class="panel glass"><h2>Was dich erwartet</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in p['punkte'])}</ul></div>
    <div class="panel next"><h2>Und danach?</h2><p style="margin:0">{e(p['danach'])}</p>{next_link}</div>
  </div>
</div></section>

{INFOTAG}
{anmeldung('<p style="margin-top:30px">' + back + '</p>')}
{KONTAKT}
{JS_HEADER}
</body>
</html>
"""


# ---------------------------------------------------------------- Schreiben
(OUT / "assets" / "style.css").write_text(CSS)
(OUT / "index.html").write_text(index())
for p in PAGES:
    (OUT / p["file"]).write_text(page(p))
print("ok")
