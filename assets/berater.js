/* Schulberater: fragt Schritt für Schritt und empfiehlt einen Bildungsgang.
   Die Daten der Bildungsgänge kommen aus window.BILDUNGSGAENGE (von tools/generate.py erzeugt).
   Ohne JavaScript funktionieren die Auswahl-Links weiterhin als normale Links. */
(function () {
  const root = document.getElementById("berater");
  if (!root || !window.BILDUNGSGAENGE) return;
  const BG = window.BILDUNGSGAENGE;
  const ANMELDUNG = window.ANMELDE_URL;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---------- Fragen
  const STEPS = {
    start: {
      frage: "Mit welchem Abschluss kommst du zu uns?",
      sub: "Wähle deinen Abschluss – oder den, den du im Sommer bekommst.",
      gruppen: [
        ["Du kommst von der Schule?", [
          { id: "kein", t: "Noch keinen Abschluss", s: "Schulpflicht in der Sek. I erfüllt", c: BG.av.color, href: BG.av.file, next: "ziel" },
          { id: "esa", t: "Erster Schulabschluss", s: "früher: Hauptschulabschluss nach Klasse 9", c: BG.bfs1.color, href: BG.bfs1.file, next: "ziel" },
          { id: "eesa", t: "Erweiterter Erster Schulabschluss", s: "früher: Hauptschulabschluss nach Klasse 10", c: BG.bfs2.color, href: BG.bfs2.file, next: "ziel" },
          { id: "for", t: "Mittlerer Schulabschluss (FOR)", s: "oder Versetzung in die Oberstufe (Gymnasium)", c: BG.hbfs.color, href: BG.hbfs.file, next: "ziel" },
          { id: "neu", t: "Neu in Deutschland", s: "und du lernst noch Deutsch", c: BG.if.color, href: BG.if.file, next: "ergebnis" },
        ]],
        ["Du bist schon im Beruf?", [
          { id: "azubi", t: "Ich habe einen Ausbildungsplatz", s: "kaufmännische Ausbildung", c: BG.bs.color, href: BG.bs.file, next: "beruf" },
          { id: "fertig", t: "Ausbildung abgeschlossen", s: "und du willst dich weiterbilden", c: BG.fs.color, href: BG.fs.file, next: "for" },
        ]],
      ],
    },
    ziel: {
      frage: "Was ist dein Ziel?",
      sub: "Es gibt kein Richtig oder Falsch – du kannst später immer noch umsteigen.",
      optionen: [
        { id: "ausbildung", t: "Möglichst bald eine Ausbildung", s: "Ich will ins Berufsleben starten" },
        { id: "abschluss", t: "Erst einen höheren Schulabschluss", s: "Ich will meine Chancen verbessern" },
        { id: "studium", t: "Später studieren", s: "Ich will die Fachhochschulreife" },
        { id: "unsicher", t: "Weiß ich noch nicht", s: "Ich will mich erst orientieren" },
      ],
    },
    beruf: {
      frage: "In welchem Beruf machst du deine Ausbildung?",
      sub: "Wir sind deine Berufsschule.",
      optionen: (BG.bs.berufe || []).map((b, i) => ({ id: "b" + i, t: b[0], s: b[1] }))
        .concat([{ id: "anderer", t: "Ein anderer kaufmännischer Beruf", s: "z. B. Bank, Verwaltung, MFA" }]),
    },
    for: {
      frage: "Hast du den Mittleren Schulabschluss (FOR)?",
      sub: "Das ist eine der Voraussetzungen für die Fachschule.",
      optionen: [
        { id: "ja", t: "Ja", s: "FOR oder höher" },
        { id: "nein", t: "Nein", s: "aber Berufserfahrung" },
      ],
    },
  };

  // ---------- Empfehlung
  const KETTE = ["av", "bfs1", "bfs2", "hbfs"];
  const START = { kein: "av", esa: "bfs1", eesa: "bfs2", for: "hbfs" };

  function empfehlung(a) {
    if (a.start === "neu") return { key: "if", weg: ["if", "bfs1", "ausbildung"], hinweise: [] };
    if (a.start === "azubi") {
      const b = (BG.bs.berufe || [])[parseInt((a.beruf || "").slice(1), 10)];
      return { key: "bs", weg: ["bs", "fs"], beruf: b, hinweise: a.beruf === "anderer"
        ? ["Für Berufe, die wir nicht selbst unterrichten, sagt dir dein Betrieb, welche Berufsschule zuständig ist. Ruf uns gern an."] : [] };
    }
    if (a.start === "fertig") return { key: "fs", weg: ["fs"], hinweise: a.for === "nein"
      ? ["Ohne FOR kannst du trotzdem aufgenommen werden, wenn du mindestens 5 Jahre einschlägig berufstätig warst."] : [] };

    const key = START[a.start];
    const i = KETTE.indexOf(key);
    let weg, hinweise = [];
    if (a.ziel === "ausbildung") {
      weg = [key, "ausbildung", "fs"];
      hinweise.push("Du hast schon einen Ausbildungsplatz? Dann kannst du direkt starten – wir sind deine Berufsschule.");
      if (key === "av") hinweise.push("In der AV bist du 3 Tage pro Woche im Praktikum – oft wird daraus ein Ausbildungsplatz.");
      else hinweise.push(`Mit dem Abschluss der ${BG[key].name} hast du bessere Chancen auf einen guten Ausbildungsplatz.`);
    } else if (a.ziel === "studium") {
      weg = KETTE.slice(i).concat(["studium"]);
      if (key !== "hbfs") hinweise.push("Schritt für Schritt kommst du bei uns bis zur Fachhochschulreife.");
      if (key === "hbfs") hinweise.push("Mit Q-Vermerk kannst du alternativ auch in die gymnasiale Oberstufe gehen (Abitur).");
    } else {
      weg = KETTE.slice(i, i + 2).concat(["ausbildung"]);
      if (key === "hbfs") weg = ["hbfs", "studium"];
      if (a.ziel === "unsicher") hinweise.push("Nach jeder Stufe kannst du neu entscheiden: weitermachen oder in eine Ausbildung starten.");
    }
    return { key, weg, hinweise };
  }

  const ZIELE = {
    ausbildung: { name: "Ausbildung", kurz: "Beruf", color: "#c58500", file: BG.bs.file },
    studium: { name: "Studium an einer FH", kurz: "FH", color: "#090058", file: null },
  };

  // ---------- Darstellung
  let antworten = {}, verlauf = [];

  function kopf(nr, gesamt) {
    const dots = Array.from({ length: gesamt }, (_, k) => `<span class="dot${k < nr ? " on" : ""}"></span>`).join("");
    return `<div class="b-top">${verlauf.length ? '<button class="b-back" type="button">‹ Zurück</button>' : "<span></span>"}<span class="dots" aria-label="Schritt ${nr} von ${gesamt}">${dots}</span></div>`;
  }
  function option(o, i, color) {
    return `<button type="button" class="choice glass" style="--c:${color || o.c || "var(--accent)"}" data-id="${o.id}">
      <span class="num">${i}</span><span><b>${esc(o.t)}</b><small>${esc(o.s || "")}</small></span><span class="go" aria-hidden="true">›</span></button>`;
  }
  function gesamtSchritte() {
    const s = antworten.start;
    if (!s) return 3;
    return s === "neu" ? 2 : 3;
  }

  function zeige(step) {
    const d = STEPS[step];
    let html = kopf(verlauf.length + 1, gesamtSchritte());
    html += `<h2 class="q">${esc(d.frage)}</h2><p class="qsub">${esc(d.sub)}</p>`;
    if (d.gruppen) {
      let n = 1;
      d.gruppen.forEach(([label, opts], gi) => {
        html += `<p class="group-label"${gi === 0 ? ' style="margin-top:0"' : ""}>${esc(label)}</p><div class="choices">`;
        opts.forEach((o) => { html += option(o, n++); });
        html += "</div>";
      });
    } else {
      const col = antworten.start ? findeStart(antworten.start).c : null;
      html += '<div class="choices">' + d.optionen.map((o, i) => option(o, i + 1, col)).join("") + "</div>";
    }
    root.innerHTML = html;
    root.querySelectorAll(".choice").forEach((b) => b.addEventListener("click", () => antwort(step, b.dataset.id)));
    const back = root.querySelector(".b-back");
    if (back) back.addEventListener("click", zurueck);
  }

  function findeStart(id) {
    for (const [, opts] of STEPS.start.gruppen) for (const o of opts) if (o.id === id) return o;
  }

  function antwort(step, id) {
    antworten[step] = id;
    verlauf.push(step);
    let next;
    if (step === "start") next = findeStart(id).next;
    else next = "ergebnis";
    if (next === "ergebnis") ergebnis(); else zeige(next);
    root.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function zurueck() {
    const last = verlauf.pop();
    delete antworten[last];
    zeige(last);
  }

  function chip(k) {
    const b = BG[k] || ZIELE[k];
    const inner = `<span class="lvl">${esc(b.kurz)}</span><span>${esc(b.name)}</span>`;
    return b.file ? `<a class="chip" style="--c:${b.color}" href="${b.file}">${inner}</a>` : `<span class="chip" style="--c:${b.color}">${inner}</span>`;
  }

  function ergebnis() {
    const e = empfehlung(antworten);
    const b = BG[e.key];
    const anmelde = b.anmelde_url || ANMELDUNG;
    const label = b.anmelde_label || "Jetzt anmelden";
    let html = kopf(gesamtSchritte(), gesamtSchritte());
    html += `<p class="eyebrow" style="margin-top:6px">Deine Empfehlung</p>
      <div class="result glass" style="--c:${b.color}">
        <span class="badge">${esc(b.kurz)}</span>
        <h2>${esc(b.name)}</h2>
        ${b.alias ? `<p class="alias">${esc(b.alias)}</p>` : ""}
        <p class="claim">${esc(b.claim)}</p>
        ${e.beruf ? `<p class="beruf">Dein Beruf: <b>${esc(e.beruf[0])}</b> (${esc(e.beruf[1])})</p>` : ""}
        <div class="facts">
          <div class="fact glass"><span>Voraussetzung</span><b>${esc(b.voraussetzung)}</b></div>
          <div class="fact glass"><span>Dauer</span><b>${esc(b.dauer)}</b></div>
          <div class="fact glass"><span>Abschluss</span><b>${esc(b.abschluss)}</b></div>
        </div>
        <h3>Dein Weg</h3>
        <div class="path">${e.weg.map(chip).join('<span class="arrow" aria-hidden="true">→</span>')}</div>
        ${e.hinweise.length ? `<ul class="tips">${e.hinweise.map((h) => `<li>${esc(h)}</li>`).join("")}</ul>` : ""}
        <div class="btns" style="margin-top:20px">
          <a class="btn solid" href="${b.file}">Alles zu ${esc(b.name)} ›</a>
          <a class="btn" href="${anmelde}" target="_blank" rel="noopener">${esc(label)}</a>
          <button type="button" class="btn ghost-muted b-restart">Neu starten</button>
        </div>
      </div>
      <p class="hint">Infotag am Samstag, 13.02.2027 – komm vorbei und lass dich persönlich beraten. Oder ruf an: <a href="tel:+492166917920">02166-917920</a></p>`;
    root.innerHTML = html;
    root.querySelector(".b-back").addEventListener("click", zurueck);
    root.querySelector(".b-restart").addEventListener("click", () => { antworten = {}; verlauf = []; zeige("start"); root.scrollIntoView({ behavior: "smooth", block: "start" }); });
  }

  zeige("start");
})();
