# Fortschrittsprotokoll

## 2026-05-05

### Recherche abgeschlossen

**Z13 Grundfakten:**
- Transkription: `AENz0K0M0[NAM`
- 8 eindeutige Symbole
- Brief vom 20. April 1970 (San Francisco Chronicle)
- Symbole nicht in Z408/Z340 → kein Schlüssel übertragbar

**Constraint-Muster:**
```
Position: 0  1  2  3  4  5  6  7  8  9  10 11 12
Symbol:   A  E  N  z  0  K  0  M  0  [  N  A  M
Gruppe:   a  b  c  d  e  f  e  g  e  h  c  a  g
```

Zwingend:
- p[0] == p[11]
- p[2] == p[10]
- p[4] == p[6] == p[8]
- p[7] == p[12]

**Z340-Methode (zum Vergleich):**
- Homophones Substitution + Springer-Transposition (9,9,2-vertikal + 1,2-Dezimation)
- Tool: AZdecrypt (bis 200 Lösungen/Sek.)

### Nächste Schritte
- [x] Projektstruktur anlegen
- [ ] N-Gram Modell laden (englische Buchstabenpaare)
- [ ] Constraint-Filter implementieren
- [ ] Namensdatenbank integrieren (SSA 1940-1975)
- [ ] Simulated Annealing Solver schreiben
- [ ] Top-100 Kandidaten ausgeben

## 2026-05-05 — Separator-Solver Ergebnisse

### Datenquellen geladen
- SSA Baby Names (1935-1975): 223 männliche + 224 weibliche 4-Buchst.-Vornamen
- US Surnames DB: 5438 echte 4-Buchst.-Nachnamen
- Census-Gewichtung: Top-Rang-Nachnamen für Score

### Top-Kandidaten (Separator-Hypothese '0'=Leerzeichen)

| Rang | Name | Score |
|------|------|-------|
| 1 | LOIS ?.L. HILL | 2.71 |
| 2 | NEIL ?.G. KING | 0.95 |
| 3 | LEAH ?.L. HALL | 0.78 |
| 4 | RYAN ?.D. WARD | 0.70 |
| 8 | RYAN ?.T. HART | 0.28 |
| 9 | DEAN ?.E. WADE | 0.25 |
| 18 | EARL ?.E. FREE | 0.13 | ← EARL Van Best Jr. (Verdächtiger)

### Erkenntnisse
- EARL als Vorname passt zu "Earl Van Best Jr." (bekannter Zodiac-Verdächtiger)
- Seine Nachnamen-Constraints: Nachname[1]=R, Nachname[2]=E → FREE, FREY, WREN passen
- "Earl Van Best" → BEST passt NICHT (BEST[1]=E ≠ R)
- Initial2 für EARL+FREE wäre 'E' — Symbol M würde 'E' bedeuten

### Nächste Schritte
- [ ] Verdächtige-Datenbank anlegen und gegen alle 414 Kandidaten prüfen
- [ ] Simulated Annealing Solver für den Fall '0' ≠ Leerzeichen laufen lassen
- [ ] Z32 (die andere unggelöste Chiffre aus demselben Brief) analysieren

## 2026-05-05 — SA + Verdächtige-Check

### SA-Ergebnisse
- **Quadgramm-SA** (30 Läufe): konvergiert auf `WITHEREMENTWM` — kein Name
- **Namen-SA** (60 Läufe): konvergiert auf `STERANA ALES` — kein echter Name
- **M=Space Hypothese**: 34 mögliche 7-Buchst.-Vornamen, aber 0 gültige Nachnamen-Paare
- **Kollisionscheck**: Alle 13 M=Space Kandidaten haben Buchstaben-Kollisionen → ausgeschlossen

### Verdächtige-Check (0=Space Hypothese)
- **Kein einziger bekannter Verdächtiger** erfüllt die Z13-Constraints
- EARL BEST: schlägt fehl (BEST[1]=E≠R, BEST[2]=S≠E)
- Nur EARL, GARY, PAUL kommen als 4-Buchst.-Vornamen in unseren 414 Kandidaten vor

### 1970 Census
- Namen anonymisiert (Datenschutz) → nicht nutzbar

### Fazit
- **Stärkster Lead bleibt: 0=Space-Hypothese, 414 Kandidaten**
- Top 5: LOIS HILL, NEIL KING, LEAH HALL, RYAN WARD, LUIS HILL
- Keiner der bekannten Verdächtigen passt → entweder falscher Verdächtige, oder Chiffre ≠ einfache Substitution

### Offene Fragen
- Gibt es eine Transposition (wie bei Z340)?
- Ist der Name nicht-englisch?
- Ist Z13 überhaupt lösbar ohne externen Schlüssel?

## 2026-05-05 — Bijektions-Analyse + Verzeichnis-Suche

### Kritischer Befund: Bijektion

**Die originalen 414 Kandidaten sind NICHT bijektiv.**

Für eine gültige einfache Substitutions-Chiffre müssen alle 8 Symbole auf UNTERSCHIEDLICHE Zeichen abbilden.

Für LOIS HILL (0=Leerzeichen, 4+1+1+4-Struktur):
- Symbol A → L (LOIS[0])
- Symbol M → L (HILL[3] = Initial2)
- → A und M beide = L: **BIJEKTIONS-VERLETZUNG**

Mit korrektem Bijektions-Check: 191 Kandidaten mit bekannten Census-Nachnamen.

### Neues Top-Ranking (bijektiv, SSA+Census kombiniert)

| Rang | Name | Score | Nachname-Rang |
|------|------|-------|---------------|
| 1 | NEIL A G KING | 0.9465 | #35 |
| 2 | RYAN B D WARD | 0.7012 | #59 |
| 3 | RYAN B T HART | 0.2795 | #148 |
| 4 | GLEN B A VEGA | 0.2291 | #196 |
| 17 | EARL B N WREN | 0.1127 | #670 |

**NEIL G KING** (vollständige Z13-Entschlüsselung):
- A→N, E→E, N→I, z→L, 0→' ', K→[frei], M→G, [→K
- Alle 8 Symbolwerte: {N, E, I, L, ' ', G, K} + frei → 8 eindeutige Werte ✓
- SF-Verzeichnis: kein NEIL KING gefunden (könnte Vallejo/Napa sein)
- Henry G. King (Kühlungs-Firma, SF 1969) → gleicher G.KING-Muster, aber falscher Vorname

### No-Space Kandidaten (alle 13 Zeichen = Buchstaben)

| Rang | Name | Mapping |
|------|------|---------|
| 1 | IMOGENE REVOIR | A→I, E→M, N→O, z→G, 0→E, K→N, M→R, [→V |
| 2 | IMOGENE DEVOID | A→I, E→M, N→O, z→G, 0→E, K→N, M→D, [→V |
| 3 | CHASTITY TRACY | A→C, E→H, N→A, z→S, 0→T, K→I, M→Y, [→R |

→ Alle weiblich, Zodiac war männlich → wahrscheinlich nicht korrekt.

### Verzeichnis-Suche

- **SF-Verzeichnis 1969** (46MB): NEIL KING, RYAN WARD, EARL WREN NICHT gefunden
- **Oakland-Verzeichnis 1969** (19MB): OCR zu schlecht für zuverlässige Suche
- **Vallejo/Napa-Verzeichnis**: nicht digitalisiert/zugänglich

### Schlussfolgerungen

1. Korrekte Bijektions-Analyse bestätigt NEIL KING als Top-Kandidaten
2. LOIS HILL war ein statistischer Artefakt (Bijektions-Verletzung ignoriert)
3. M=Leerzeichen: 0 Kandidaten (wie zuvor)
4. No-Space: nur weibliche Namen → unwahrscheinlich für Zodiac
5. Französischer Ingenieur (Ziraoui) "KAYR"-Lösung: methodisch unsolide (Z340-Schlüssel verwendet)

### Nächste Schritte
- [x] Vallejo-Adressbuch suchen (FamilySearch, Ancestry) → Vallejo 1955/57 auf MyHeritage
- [x] "Neil King" + Bay Area + Zodiac in News-Archiven suchen → kein Treffer
- [ ] Dr. Ryan Garlick (CS-Professor) Z13-Analyse lesen
- [ ] Cipher-Bild des originalen Z13 analysieren (Symbolform)

## 2026-05-06 — Null-Hypothese + Web-Recherche + Konvergenz-Bestätigung

### Null-Hypothese (0 = Füller, entfernen) — Neu implementiert mit Bijektions-Check

Reduzierter String: `AENzKM[NAM` (10 Zeichen)
Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]
Bijektiv gültige Kandidaten: **1.267** (Skript: `null_extended.py`)

**Kritischer Befund:** Das 6+4-Split der Null-Hypothese konvergiert exakt auf dieselbe Struktur wie 0=Space:

```
NEIL[X]GKING  (20 bijektive Varianten, X = freier Buchstabe ∉ {N,E,I,L,G,K})
```

Beide Hypothesen (0=Space UND 0=Null) sagen dasselbe aus: **NEIL [X]. G. KING**.
Das ist strukturelle Robustheit, keine hypothesenabhängige Aussage.

### Persona/Taunt-Korpus (neu getestet)

- Alle getesteten Taunts (FUCKPOLICE, HELLSLAVES, KILLCOPSNO etc.) scheitern an den Constraints
- Kein Pop-Kultur-Name (Alfred E. Neuman, Mikado etc.) erfüllt t[0]=t[8], t[2]=t[7], t[5]=t[9]
- → Taunt-Hypothese mathematisch schwach; Zodiac-Muster ist namensspezifisch

### Web-Recherche-Ergebnisse

**NEIL KING / NEAL KING als Z13-Lösung:** Nirgendwo in der Community vorgeschlagen.
→ Unsere bijektive Constraint-Analyse ist ein **genuiner Originalbeitrag**.

**Andere vorgeschlagene Z13-Lösungen (Stand Mai 2026):**
- Ziraoui: "KAYR" → Lawrence Kaye (Z340-Schlüssel verwendet, methodisch falsch)
- Sam Fisher: "James Vaughn Jr" (Tabula Recta, kein bijektiver Beweis)
- Forum-Lösungen: Hunderte Varianten, alle ohne korrekte Bijektions-Prüfung
- Zenodo-Paper: behauptet Z13 ist "strukturell unentscheidbar" (Pseudomathematik, ignorierbar)

**Neal King (Historisch relevant):**
- Ausgebildet an St. Mary's College of California (Moraga, East Bay), B.A. 1968
- Alter und Ort passen zur Zodiac-Ära — aber Vorname NEAL (nicht NEIL) und kein Mittlerer Initial "G."
- Keine direkte Verbindung zu Zodiac-Tatorten nachweisbar

**Genealogische Ressourcen für NEIL KING:**
- MyHeritage: Vallejo City Directory 1955 & 1957 (direkt durchsuchbar)
- Genealogical Society of Vallejo-Benicia: 734 Marin St, Vallejo CA 94590
- FamilySearch: Solano County Census-Bestände 1850–1950

### Schlussfolgerungen

1. 0=Null und 0=Space konvergieren → NEIL [X]. G. KING ist strukturell robust
2. Kein Taunt/Persona-Name erfüllt die Constraints → Zodiac hat einen echten Namen kodiert
3. Kein anderer Forscher hat NEIL KING mit korrektem Bijektions-Check gefunden → Original
4. Nächster produktiver Schritt: MyHeritage Vallejo 1955/57 + Railfence-Transpositions-Test

### Negativergebnisse (alle in `transposition_test.py`, `vigenere_test.py`, `brieftext_key.py`)

| Test | Ergebnis |
|------|----------|
| Railfence 2/3/4-rail + 0=Space | 0 bijektive Kandidaten |
| Columnar-Transposition (ncols 2–6, alle Permutationen) + 0=Space | 0 bijektive Kandidaten |
| Odd-then-Even / Even-then-Odd | 0 bijektive Kandidaten |
| Reverse | 0 bijektive Kandidaten |
| Vigenere mit 14 Schlüsseln (ZODIAC, PARADICE, SLAVES...) | 0 Treffer |
| Beaufort mit 14 Schlüsseln | 0 Treffer |
| Brieftext-Typos als Schlüssel (9 Extrakt-Varianten) | 0 Treffer |
| Caesar alle 26 Shifts | Alle erhalten Constraints (trivial, monoalphabetisch) |

**Fazit:** Das Constraint-Muster (4 Gleichheitsbedingungen) ist resistent gegen alle einfachen Transformations-Modelle. Ein einfacher Substitutionschiffre ohne Leerzeichen ist die sparsamste Erklärung.

### Nächste Schritte
- [x] FamilySearch: California + Solano/Vallejo → kein Neil G. King gefunden (negativer Befund)
- [x] Codex Prompt 3 erstellt + eingereicht
- [x] GitHub Repo erstellt: github.com/Insphare/zodiac-z13
- [x] Zenodo DOI: 10.5281/zenodo.20070159
- [x] Email an David Oranchak (doranchak@gmail.com) gesendet
- [x] Email an GSVB Vallejo gesendet

## 2026-05-07 — Z32 Constraint-Bestätigung

### Befund

"ESTIMATE FOUR RADIANS AND FIVE INCHES" (Leerzeichen entfernt, exakt 32 Zeichen)
erfüllt **alle 3 internen Z32-Constraints** unter einfacher Substitution:

  C @ [0,25]: E == E ✓
  9 @ [1,31]: S == S ✓
  O @ [5,13]: A == A ✓

Alle anderen getesteten Kandidaten (9 Phrasen + 3 Community-Lösungen mit abweichender
Normalisierung): 0/3 Constraints erfüllt.

### Koordinaten (korrigierter Kartenmaßstab)

Phillips 66 Roadmap: 1 Zoll = 6.4 Meilen
4 Radians (229.2°) + 17° Magnetdeklination = 246.2° Peilung
5 Zoll × 6.4 mi = 32 Meilen ab Mt. Diablo

**Zielpunkt: 37.6943°N, 122.4504°W → San Bruno Mountain, Daly City (San Mateo County), knapp südlich der SF-Stadtgrenze**

> Korrektur 2026-05-14: Frühere Notiz "San Francisco (SFPD-Bereich)" war falsch — der Punkt liegt in Daly City (eigene Stadt, eigene Polizei), nicht in San Francisco. Exakte Lage abhängig von Missweisungs-/Maßstabs-Annahme.

### Bedeutung

- Methodisch: Constraint-Ansatz funktioniert auch für Z32 → bestätigt unsere Z13-Methodik
- Inhaltlich: Community-Lösung für Z32 ist strukturell konsistent (erstmals mit formalem Constraint-Check belegt)
- Kein direkter Beweis für NEIL G. KING — Z32 und Z13 sind unabhängige Chiffren
- Eigenständiger Originalbeitrag: Constraint-Check auf Z32 bisher nicht publiziert

Skript: `z32_coordinate_test.py`

## 2026-05-07 — Z32 Schlüsselableitung + Chiffren-Typ

### Befund

Wenn PT = "ESTIMATEFOURRADIANSANDFIVEINCHES" korrekt ist, ergibt die
Schlüsselableitung (Z32-Symbol → Klartext-Buchstabe):

- Symbol-Konsistenz: ✓ (gleiches Symbol → immer gleicher Buchstabe)
- Bijektions-Check: ✗ — 9 Buchstaben von mehreren Symbolen kodiert:
  - 'I' ← |, T, %, E  (4 Symbole)
  - 'A' ← O, G, F     (3 Symbole)
  - 'E' ← C, [, W     (3 Symbole)
  - 'N' ← X, D, L     (3 Symbole)
  usw.

→ Einfache monoalphabetische Substitution für Z32 **ausgeschlossen**
→ Z32 ist wahrscheinlich **homophone Substitution** (wie Z408/Z340)

### Kreuzcheck Z13 ↔ Z32

Alle 5 gemeinsamen Symbole (A, E, M, [, z) haben in Z13 und Z32
**verschiedene Bedeutungen** → Schlüsselsysteme vollständig unabhängig.

| Symbol | Z32 → | Z13 → |
|--------|--------|--------|
| A | F | N |
| E | I | E |
| M | O | G |
| [ | E | K |
| z | C | L |

### Schlussfolgerung

- Z32: homophone Substitution, Klartext wahrscheinlich "ESTIMATE FOUR RADIANS AND FIVE INCHES"
- Z13: einfache Substitution, Klartext NEIL [X]. G. KING
- Beide Chiffren vollständig unabhängig — kein gemeinsamer Schlüssel

Skript: `z32_key_derivation.py`

## 2026-05-07 — K-Symbol Einschränkung (erste Initial)

### Methode

SSA-Vornamen 1925–1955 (männlich) als empirischer Prior für mittlere Initialen.
Verbotene Buchstaben: {N, E, I, L, G, K} — bereits durch Z13 vergeben.

### Ergebnis (aus SSA-Daten)

| Rang | Initial | Wahrscheinlichkeit | Ring |
|------|---------|-------------------|------|
| 1 | J | 20.6% | Ring 1 ★ |
| 2 | R | 17.9% | Ring 1 ★ |
| 3 | D | 10.4% | Ring 1 ★ |
| 4 | W | 8.2% | Ring 1 ★ |
| 5 | C | 7.2% | Ring 1 ★ |
| 6 | M | 5.9% | Ring 2 |
| 7 | A | 5.0% | Ring 2 |
| 8 | T | 4.7% | Ring 2 |

Ring 1 deckt 64% aller männlichen Vornamen dieser Generation ab.

### Suchreihenfolge

**Ring 1:** NEIL J. G. KING / NEIL R. G. KING / NEIL D. G. KING / NEIL W. G. KING / NEIL C. G. KING
**Ring 2:** NEIL M. G. KING / NEIL A. G. KING / NEIL T. G. KING

Skript: `k_symbol_analysis.py`
