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
    dict(key="av", file="av.html", kurz="AV", nr=1, color="#2fb7c9",
         name="Ausbildungsvorbereitung", alias=None,
         claim="Für dich, wenn du (noch) keinen Abschluss hast.",
         voraussetzung="Kein Abschluss nötig", dauer="1 Jahr", abschluss="Erster Schulabschluss",
         punkte=["3 Tage Praktikum (Mo–Mi), 2 Tage Schule (Do + Fr)", "Unterricht nah an echten Betriebssituationen",
                 "Schulsozialarbeit und persönliche Beratung", "Hilfe bei Berufswahl und Praktikumssuche"],
         hinweis="Den Praktikumsplatz suchst du dir vor Schuljahresbeginn selbst – am besten in einem Betrieb, der auch ausbildet. Die AV kann auch als 10. Pflichtschuljahr besucht werden.",
         danach="Mit dem Ersten Schulabschluss weiter in die Berufsfachschule 1 (Handelsschule HS 9) – oder direkt in eine Ausbildung.",
         next="bfs1", bild="bg-av", gruppe="schule",
         wahl="Noch keinen Abschluss", wahl_info="Schulpflicht in der Sek. I erfüllt"),
    dict(key="bfs1", file="bfs1.html", kurz="BFS 1", nr=2, color="#46a0f0",
         name="Berufsfachschule 1", alias="Handelsschule HS 9",
         claim="Kaufmännische Grundlagen – und dein nächster Abschluss.",
         voraussetzung="Erster Schulabschluss", dauer="1 Jahr", abschluss="Erweiterter Erster Schulabschluss",
         punkte=["Geschäftsprozesse, Mathe, Englisch, Deutsch", "30 Praktikumstage: 1 Woche im Herbst, dann 1 Tag pro Woche",
                 "Kleine Klassen, Schwerpunkt Einzelhandel", "Enge Zusammenarbeit mit der Agentur für Arbeit"],
         danach="Weiter in die Berufsfachschule 2 (Handelsschule HS 10) zum Mittleren Schulabschluss – oder in eine Ausbildung.",
         next="bfs2", bild="bg-bfs1", gruppe="schule",
         wahl="Erster Schulabschluss", wahl_info="früher: Hauptschulabschluss nach Klasse 9"),
    dict(key="bfs2", file="bfs2.html", kurz="BFS 2", nr=3, color="#9a8cff",
         name="Berufsfachschule 2", alias="Handelsschule HS 10",
         claim="Dein Weg zum Mittleren Schulabschluss.",
         voraussetzung="Erweiterter Erster Schulabschluss", dauer="1 Jahr", abschluss="Mittlerer Schulabschluss (FOR)",
         punkte=["Geschäftsprozesse, Wirtschaft, Mathe, Englisch", "30 Praktikumstage im kaufmännischen Bereich",
                 "Mit guten Noten: Berechtigung für die Oberstufe", "Unterstützung bei der Ausbildungsplatzsuche"],
         hinweis="Auch möglich: nach Klasse 9 des Gymnasiums mit der Berechtigung für die Oberstufe.",
         danach="Weiter in die Höhere Berufsfachschule oder die gymnasiale Oberstufe – oder in eine Ausbildung.",
         next="hbfs", bild="bg-bfs2", gruppe="schule",
         wahl="Erweiterter Erster Schulabschluss", wahl_info="früher: Hauptschulabschluss nach Klasse 10"),
    dict(key="hbfs", file="hoehere-berufsfachschule.html", kurz="HBFS", nr=4, color="#5fd0b0",
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
    dict(key="if", file="internationale-foerderklassen.html", kurz="IF", nr=5, color="#f08aa8",
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
    dict(key="bs", file="berufsschule.html", kurz="BS", nr=6, color="#f0c060",
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
    dict(key="fs", file="fachschule.html", kurz="FS", nr=7, color="#f0915a",
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
@font-face{font-family:"Dosis";src:url("fonts/dosis-latin.woff2") format("woff2");font-weight:200 800;font-display:swap}
:root{
  --bg:#080b20; --bg2:#0d1130; --text:#c9d2e3; --muted:#8e99b3; --white:#fff;
  --accent:#46a0f0; --mint:#5fd0b0;
  --glass:rgba(22,28,62,.52); --glass-b:rgba(255,255,255,.12);
  --r:22px; --shadow:0 18px 48px rgba(0,0,0,.32);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Dosis",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:18px;line-height:1.55;-webkit-text-size-adjust:100%;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:var(--accent)}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
@media (min-width:720px){.wrap{padding:0 28px}}
h1,h2,h3{color:var(--white);margin:0}
.eyebrow{display:block;text-transform:uppercase;letter-spacing:.22em;font-size:.78rem;font-weight:600;color:var(--accent);margin:0 0 14px}
.chev{display:inline-block;color:var(--accent);font-weight:400;font-size:1.5em;line-height:0;vertical-align:-.32em;transform:scaleX(1.5);margin-right:.45em}
.display{font-weight:200;text-transform:uppercase;letter-spacing:.08em;line-height:1.08}
h2.display{font-size:clamp(1.8rem,6vw,3rem);margin-bottom:12px}
.lead{font-size:1.1rem;color:var(--text);max-width:680px;margin:0 0 28px}

/* Header */
.site-header{position:fixed;inset:0 0 auto 0;z-index:50;transition:background .25s,backdrop-filter .25s,border-color .25s;border-bottom:1px solid transparent}
.site-header.scrolled{background:rgba(8,11,32,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom-color:var(--glass-b)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px;height:72px}
.site-header img{height:44px;width:auto}
.hdr-right{display:flex;align-items:center;gap:22px}
.nav{display:flex;gap:22px}
.nav a{color:var(--text);text-decoration:none;text-transform:uppercase;letter-spacing:.12em;font-weight:600;font-size:.85rem}
.nav a:hover{color:var(--white)}
@media (max-width:820px){.nav{display:none}}

/* Buttons */
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:12px 22px;text-decoration:none;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.82rem;border:1px solid var(--accent);color:var(--white);background:transparent;transition:background .2s,color .2s;cursor:pointer}
.btn:hover{background:var(--accent);color:#06102a}
.btn.solid{background:var(--accent);color:#06102a}
.btn.solid:hover{background:#7cc0ff}
button.btn{font-family:inherit}
.btn.small{padding:9px 16px;font-size:.75rem}
.btns{display:flex;flex-wrap:wrap;gap:12px}

/* Hero */
.hero{position:relative;min-height:100svh;display:flex;align-items:flex-end;padding:120px 0 56px;isolation:isolate}
.hero-bg{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:
  radial-gradient(60% 50% at 75% 30%,rgba(70,160,240,.28),transparent 70%),
  linear-gradient(180deg,rgba(8,11,32,.55) 0%,rgba(8,11,32,.78) 45%,var(--bg) 100%)}
.hero h1.display{font-size:clamp(2.4rem,9vw,5.2rem);letter-spacing:.1em;margin-bottom:18px}
.hero .q{font-size:clamp(1.35rem,4.5vw,2rem);font-weight:500;color:var(--white);margin:34px 0 6px}
.hero .qsub{color:var(--text);margin:0 0 20px}

/* Glass */
.glass{background:var(--glass);border:1px solid var(--glass-b);border-radius:var(--r);box-shadow:var(--shadow);backdrop-filter:blur(16px) saturate(1.25);-webkit-backdrop-filter:blur(16px) saturate(1.25)}

/* Auswahl */
.choices{display:grid;gap:14px;grid-template-columns:1fr}
@media (min-width:760px){.choices{grid-template-columns:1fr 1fr}}
.choice{display:flex;align-items:center;gap:16px;padding:18px 20px;text-decoration:none;color:var(--text);position:relative;overflow:hidden;transition:transform .15s,border-color .15s}
.choice::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--c)}
.choice:hover{transform:translateY(-2px);border-color:var(--c)}
.choice .num{flex:none;width:44px;height:44px;border-radius:50%;border:1px solid var(--c);color:var(--c);display:grid;place-items:center;font-weight:700;font-size:1.1rem}
.choice b{display:block;color:var(--white);font-size:1.15rem;font-weight:600}
.choice small{display:block;color:var(--muted);font-size:.9rem}
.choice .to{display:block;color:var(--c);font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.75rem;margin-top:4px}
.choice .go{margin-left:auto;color:var(--c);font-size:1.6rem;font-weight:300}
.group-label{color:var(--white);font-weight:600;font-size:1.1rem;margin:26px 0 12px}
.job small{display:block;color:var(--muted);font-weight:400;font-size:.85rem}
/* Schulberater */
.berater{scroll-margin-top:90px}
button.choice{font:inherit;width:100%;text-align:left;cursor:pointer;border:1px solid var(--glass-b)}
button.choice:focus-visible,.b-back:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.b-top{display:flex;justify-content:space-between;align-items:center;margin:0 0 6px;min-height:34px}
.b-back{background:none;border:0;color:var(--text);font:inherit;text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;font-weight:600;cursor:pointer;padding:6px 0}
.b-back:hover{color:var(--white)}
.dots{display:flex;gap:8px}.dot{width:28px;height:4px;border-radius:2px;background:rgba(255,255,255,.18)}.dot.on{background:var(--accent)}
.result{padding:26px;border-color:var(--c)}
.result .badge{display:inline-block;background:var(--c);color:#06102a;font-weight:800;border-radius:999px;padding:6px 16px;margin-bottom:12px}
.result h2{font-size:clamp(1.7rem,6vw,2.6rem);font-weight:300;text-transform:uppercase;letter-spacing:.08em;line-height:1.1;hyphens:auto;overflow-wrap:break-word}
.result .alias{color:var(--muted);text-transform:uppercase;letter-spacing:.14em;font-size:.82rem;margin:6px 0 0}
.result .claim{color:var(--white);font-size:1.1rem;margin:12px 0 18px}
.result .beruf{margin:-6px 0 18px}
.result h3{font-size:.8rem;text-transform:uppercase;letter-spacing:.2em;color:var(--c);margin:24px 0 12px}
.path{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.chip{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--c);border-radius:999px;padding:6px 14px 6px 6px;color:var(--white);text-decoration:none;font-weight:600;font-size:.95rem;background:rgba(255,255,255,.03)}
.chip .lvl{background:var(--c);color:#06102a;border-radius:999px;padding:2px 9px;font-size:.78rem;font-weight:800}
a.chip:hover{background:rgba(255,255,255,.08)}
.arrow{color:var(--muted)}
.tips{margin:18px 0 0;padding-left:20px;color:var(--text)}.tips li{margin:6px 0}
.btn.ghost-muted{border-color:rgba(255,255,255,.25);color:var(--text)}
.btn.ghost-muted:hover{background:rgba(255,255,255,.1);color:var(--white)}
.hint{color:var(--muted);font-size:.95rem;margin-top:16px}
.hint a{color:var(--white)}

/* Sections */
section{padding:72px 0;position:relative}
section.alt{background:linear-gradient(180deg,var(--bg) 0%,var(--bg2) 50%,var(--bg) 100%)}
.cards3{display:grid;gap:16px;grid-template-columns:1fr}
@media (min-width:760px){.cards3{grid-template-columns:repeat(3,1fr)}}
.card{padding:26px}
.card .ic{width:46px;height:46px;border-radius:50%;background:rgba(70,160,240,.14);display:grid;place-items:center;margin-bottom:16px}
.card .ic img{width:26px;height:26px;filter:brightness(0) invert(1)}
.card h3{font-size:1.15rem;font-weight:600;margin-bottom:6px}
.card p{margin:0;color:var(--muted)}

/* Galerie */
.gallery{display:grid;gap:14px;grid-template-columns:1fr}
@media (min-width:760px){.gallery{grid-template-columns:repeat(2,1fr)}}
.gallery figure:first-child{grid-column:1/-1;aspect-ratio:16/9}
.gallery figure{margin:0;border-radius:var(--r);overflow:hidden;border:1px solid var(--glass-b);position:relative;aspect-ratio:3/2}
.gallery img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.gallery figure:hover img{transform:scale(1.04)}
.gallery figcaption{position:absolute;left:0;right:0;bottom:0;padding:28px 16px 12px;background:linear-gradient(transparent,rgba(8,11,32,.85));color:var(--white);font-size:.95rem}

/* Treppe */
.stairs{display:grid;gap:12px}
.step{display:flex;align-items:center;gap:16px;padding:16px 20px;text-decoration:none;color:var(--text);border-left:4px solid var(--c)}
.step b{color:var(--white);font-weight:600;font-size:1.08rem}
.step .lvl{flex:none;min-width:64px;text-align:center;font-weight:700;color:var(--c);border:1px solid var(--c);border-radius:999px;padding:4px 10px;font-size:.85rem}
@media (min-width:760px){.step:nth-child(2){margin-left:5%}.step:nth-child(3){margin-left:10%}.step:nth-child(4){margin-left:15%}.step:nth-child(5){margin-left:20%}}
.note{padding:18px 20px;margin-top:20px;border-left:4px solid var(--accent)}
.note b{color:var(--white)}

/* Berufe */
.jobs{display:grid;gap:12px;grid-template-columns:1fr 1fr}
@media (min-width:760px){.jobs{grid-template-columns:repeat(3,1fr)}}
.job{min-width:0;hyphens:auto;overflow-wrap:break-word;padding:16px;color:var(--white);font-weight:600;border-radius:16px}

/* Infotag */
.infotag{display:flex;gap:24px;align-items:center;padding:26px;border-color:rgba(95,208,176,.45)}
.it-date{flex:none;width:96px;text-align:center;border:1px solid var(--mint);color:var(--mint);border-radius:18px;padding:10px 0;line-height:1.1;font-weight:600;text-transform:uppercase;letter-spacing:.12em;font-size:.75rem}
.it-date b{display:block;font-size:2.4rem;font-weight:300;letter-spacing:0;color:var(--white)}
.infotag .eyebrow{color:var(--mint);margin-bottom:6px}
.infotag h2{font-size:clamp(1.25rem,4vw,1.7rem);font-weight:500;margin-bottom:6px}
.placeholder-note{color:var(--muted);font-style:italic;margin:0}
@media (max-width:520px){.infotag{flex-direction:column;align-items:flex-start}}

/* Anmeldung */
.reg{display:grid;gap:22px;grid-template-columns:1fr}
@media (min-width:860px){.reg{grid-template-columns:1.5fr 1fr}}
.regstep{display:flex;gap:16px;margin-bottom:20px}
.regstep .n{flex:none;width:42px;height:42px;border-radius:50%;border:1px solid var(--accent);color:var(--accent);display:grid;place-items:center;font-weight:700}
.regstep h3{font-size:1.1rem;font-weight:600;margin:0 0 2px}
.regstep p{margin:0;color:var(--muted)}
.regstep a{color:var(--white)}

/* Präsentation */
.viewer{padding:14px}
.viewer img{width:100%;border-radius:12px;aspect-ratio:16/9;object-fit:contain;background:#eef0f5}
.vctrl{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:12px;color:var(--muted)}
.dl{margin-top:18px}

/* Kontakt / Footer */
.contact{display:grid;gap:12px;font-size:1.15rem}
.contact a{color:var(--white);text-decoration:none}
.contact a:hover{color:var(--accent)}
footer{border-top:1px solid var(--glass-b);color:var(--muted);font-size:.9rem;padding:22px 0}
footer a{color:var(--text)}

/* Bildungsgang-Seite */
.bg-hero{position:relative;padding:130px 0 56px;isolation:isolate;min-height:62svh;display:flex;align-items:flex-end}
.bg-hero::before{content:"";position:absolute;inset:0;z-index:-1;background:
  radial-gradient(55% 60% at 80% 20%,color-mix(in srgb,var(--c) 38%,transparent),transparent 70%),
  linear-gradient(180deg,rgba(8,11,32,.6) 0%,rgba(8,11,32,.82) 55%,var(--bg) 100%)}
.bg-hero .eyebrow{color:var(--c)}
.bg-hero .chev{color:var(--c)}
.bg-hero h1.display{font-size:clamp(2.1rem,8vw,4.4rem);hyphens:auto;overflow-wrap:break-word;margin-bottom:6px}
.bg-hero .alias{color:var(--muted);text-transform:uppercase;letter-spacing:.14em;font-size:.85rem;margin:0 0 14px}
.bg-hero .claim{font-size:clamp(1.1rem,3vw,1.35rem);color:var(--white);margin:0 0 24px;max-width:640px}
.bg-hero .btn{border-color:var(--c)}
.bg-hero .btn.solid{background:var(--c);color:#06102a}
.back{display:inline-flex;align-items:center;gap:6px;color:var(--text);text-decoration:none;text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;font-weight:600;margin-bottom:26px}
.back:hover{color:var(--white)}
.facts{display:grid;gap:12px;grid-template-columns:repeat(3,1fr)}
@media (max-width:680px){.facts{grid-template-columns:1fr}}
.fact{padding:16px 18px;border-top:2px solid var(--c);border-radius:16px}
.fact span{display:block;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:600}
.fact b{color:var(--white);font-weight:600;font-size:1.08rem}
.textbox{padding:22px 24px;border-left:4px solid var(--c)}
.two{display:grid;gap:18px;grid-template-columns:1fr}
@media (min-width:860px){.two{grid-template-columns:1.4fr 1fr}}
.panel{padding:24px}
.panel h2{font-size:1.3rem;font-weight:500;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px}
.panel ul{margin:0;padding-left:0;list-style:none}
.panel li{padding:8px 0 8px 28px;position:relative;border-bottom:1px solid rgba(255,255,255,.06)}
.panel li::before{content:"›";position:absolute;left:6px;top:6px;color:var(--c);font-weight:700}
.next{padding:24px;border:1px solid var(--c);background:color-mix(in srgb,var(--c) 14%,rgba(22,28,62,.6))}
.next h2{color:var(--c)}
.next a{color:var(--white);font-weight:700}
.stack>*+*{margin-top:18px}
section.tight{padding:36px 0}
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
<meta name="theme-color" content="#080b20">
<link rel="icon" href="assets/icon-abschluss.png">
<link rel="preload" href="assets/fonts/dosis-latin.woff2" as="font" type="font/woff2" crossorigin>
{pl}
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
"""


def header(nav):
    return f"""<header class="site-header"><div class="wrap">
  <a href="index.html" aria-label="Zur Startseite"><img src="assets/logo-hell.png" alt="Berufskolleg Rheydt-Mülfort – für Wirtschaft und Verwaltung" width="655" height="217"></a>
  <div class="hdr-right"><nav class="nav">{nav}</nav><a class="btn small" href="{ANMELDE_URL}" target="_blank" rel="noopener">Anmelden</a></div>
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
  <span class="eyebrow">Berufskolleg Rheydt-Mülfort · Mönchengladbach</span>
  <h1 class="display">Dein Weg.<br>Dein Abschluss.</h1>
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
</div></section>

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
  {back}
  <span class="eyebrow">Bildungsangebot · {e(p['kurz'])}</span>
  <h1 class="display">{e(p['name'])}</h1>
  {f'<p class="alias">{e(p["alias"])}</p>' if p['alias'] else ''}
  <p class="claim">{e(p['claim'])}</p>
  <div class="btns"><a class="btn solid" href="{p.get('anmelde_url', ANMELDE_URL)}" target="_blank" rel="noopener">{e(p.get('anmelde_label', 'Jetzt anmelden'))}</a><a class="btn" href="#infotag">Infotag 13.02.2027</a></div>
</div></section>

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
    <div class="panel next" style="border-radius:var(--r)"><h2>Und danach?</h2><p style="margin:0">{e(p['danach'])}</p>{next_link}</div>
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
