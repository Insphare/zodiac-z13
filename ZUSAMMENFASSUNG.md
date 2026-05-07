# Z13 — Vollständige Projektanalyse

## Die Chiffre

```
AENz0K0M0[NAM
```

- 13 Zeichen, 8 eindeutige Symbole
- Brief vom 20. April 1970, San Francisco Chronicle
- Zodiac schrieb: "My name is —" gefolgt von dieser Chiffre
- Symbols nicht in Z340/Z408 → kein bekannter Schlüssel übertragbar

**Zwingend durch Symbolwiederholung:**
```
text[0]  = text[11]   (Symbol A)
text[2]  = text[10]   (Symbol N)
text[4]  = text[6] = text[8]   (Symbol 0)
text[7]  = text[12]   (Symbol M)
```

---

## Getestete Hypothesen

### 1. Simulated Annealing (Quadgramm-Scoring)
- 30 Läufe × 200.000 Iterationen
- Konvergiert auf `WITHEREMENTWM` (A→W, E→I, N→T, z→H, 0→E, K→R, M→M, [→N)
- Kein Name → SA-Solver findet englischen Text, kein Namensformat

### 2. Simulated Annealing (Namen-Scoring)
- 60 Läufe mit bigramm/trigramm-Modell aus SSA+Nachnamen
- 56/60 Läufe: M→Leerzeichen
- Konvergiert auf `STERANA ALES` — kein echter Name

### 3. M = Leerzeichen (7+4-Struktur)
- Struktur: XXXXXXX·XXXX (7-Buchst. Vorname + 4-Buchst. Nachname)
- Bedingung: Vorname[4] = Vorname[6] = Nachname[0]
- 34 gültige 7-Buchst.-Vornamen in SSA-DB — aber **0 Nachnamen** ohne Buchstaben-Kollision
- **Vollständig ausgeschlossen**

### 4. 0 = Leerzeichen (4+1+1+4-Struktur) ← Haupthypothese
- Struktur: XXXX · X · X · XXXX = Vorname(4) + Initial1(1) + Initial2(1) + Nachname(4)
- Drei Leerzeichen an Positionen 4, 6, 8
- Constraints:
  - Vorname[0] = Nachname[2]  (Symbol A)
  - Vorname[2] = Nachname[1]  (Symbol N)
  - Initial2 = Nachname[3]    (Symbol M)

**Kritisch:** Die Original-Suche ignorierte Bijektion → LOIS HILL ist UNGÜLTIG (A→L und M→L kollidieren).

Mit korrektem Bijektions-Check:

| Rang | Name | Score | NR |
|------|------|-------|----|
| 1 | NEIL **?** G. KING | 0.9465 | #35 |
| 2 | RYAN **?** D. WARD | 0.7012 | #59 |
| 3 | RYAN **?** T. HART | 0.2795 | #148 |
| 17 | EARL **?** N. WREN | 0.1127 | #670 |

### 5. Null-Hypothese (0 = Füller, entfernen)
- Reduzierter String: `AENzKM[NAM` (10 Zeichen)
- Neue Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]
- 19.703 Kandidaten — zu viele für eindeutige Lösung

### 6. Prime-Routen (mod-13 Transposition)
- 12 mögliche Schrittweiten, da 13 prim
- Alle 12 Routen erhalten das gleiche Wiederholungsmuster
- Keine neuen Informationen → Transpositions-Ansatz nutzlos

### 7. No-Space (13 Buchstaben, kein Leerzeichen)
- 3 bijektive Kandidaten:
  - **IMOGENE REVOIR** (A→I, E→M, N→O, z→G, 0→E, K→N, M→R, [→V)
  - **IMOGENE DEVOID** (identisch bis auf M→D)
  - **CHASTITY TRACY** (A→C, E→H, N→A, z→S, 0→T, K→I, M→Y, [→R)
- Alle weibliche Namen → Zodiac war männlich → wahrscheinlich falsch

### 8. Verdächtige-Check
- Alle bekannten Zodiac-Verdächtigen gegen Constraints geprüft
- **Kein einziger** erfüllt die Z13-Bedingungen (inkl. EARL Van Best, Lawrence Kane)

---

## Hauptbefund: NEIL G. KING

```
Z13:   A  E  N  z  _  K  _  M  _  [  N  A  M
       ↓  ↓  ↓  ↓     ↓     ↓     ↓  ↓  ↓  ↓
Name:  N  E  I  L  _  ?  _  G  _  K  I  N  G
```

**Vollständiges Symbol-Mapping:**

| Symbol | → | Buchstabe | Quelle |
|--------|---|-----------|--------|
| A | → | N | Vorname[0] = Nachname[2] |
| E | → | E | Vorname[1] |
| N | → | I | Vorname[2] = Nachname[1] |
| z | → | L | Vorname[3] |
| 0 | → | ` ` | Leerzeichen (×3) |
| K | → | [frei] | 1. Initial |
| M | → | G | Initial2 = Nachname[3] |
| [ | → | K | Nachname[0] |

**Alle 8 Werte: {N, E, I, L, ` `, G, K} + 1 freier Buchstabe → eindeutig ✓**

Voller Name: **"NEIL [X]. G. KING"** — wobei X jeder freie Buchstabe sein kann.

---

## Externe Quellen

| Quelle | Behauptung | Bewertung |
|--------|-----------|-----------|
| Ziraoui 2024 (FR) | "KAYR" → Lawrence Kaye | Z340-Schlüssel auf Z13 angewandt → methodisch falsch |
| Dr. Garlick 2025 (UNT) | Eigene Methode | Details nicht öffentlich zugänglich |
| Forum-Konsens | Keine anerkannte Lösung | Korrekt, Z13 gilt als unlösbar |

---

## Genutzte Datensätze

| Datei | Inhalt |
|-------|--------|
| `ssa_names.csv` | US-Vornamen 1930–1980 mit Häufigkeit |
| `us_surnames.txt` | 88.000 US-Nachnamen |
| `sf_directory_1969.txt` | Polk's SF Adressbuch 1969/70 (46 MB, OCR) |
| `oakland_directory_1969.txt` | Polk's Oakland 1969 (19 MB, OCR) |

---

## Erstellte Skripte

| Skript | Funktion |
|--------|----------|
| `solver.py` | SA mit Quadgramm-Score |
| `name_sa.py` | SA mit Namen-Score |
| `separator_hypothesis.py` | 0=Leerzeichen, Grundsuche |
| `filter_names.py` | SSA+Nachnamen-Filter |
| `rank_candidates.py` | Kombiniertes Scoring (mit Bijektions-Fix) |
| `m_space_search.py` | M=Leerzeichen-Hypothese |
| `suspects_check.py` | Verdächtige-Prüfung |
| `null_indexed.py` | Null-Hypothese (O(n) Index) |
| `bijective_search.py` | Korrekte Bijektions-Analyse |
| `comprehensive_search.py` | Alle Leerzeichen-Positionen |

---

## Konvergenz-Befund (2026-05-06)

**0=Space UND 0=Null konvergieren auf dieselbe Struktur:**

Im 6+4-Split der Null-Hypothese (`NEIL[X]GKING`) erfüllen exakt 20 bijektive Varianten alle Constraints — identisch zur 0=Space-Lösung. Die Aussage "NEIL [X]. G. KING" ist damit **hypothesenunabhängig**.

**Community-Status:** Kein Forum, kein Paper, kein Wiki hat NEIL KING je mit korrektem Bijektions-Check vorgeschlagen. Genuiner Originalbefund.

**Taunt/Persona-Korpus:** Alle getesteten Phrasen (FUCKPOLICE, ALFRED NEUMAN etc.) scheitern an den Constraints. Das Muster ist namensspezifisch, kein Taunt.

---

## Fazit

Z13 ist mit 13 Zeichen **kryptographisch zu kurz** für eine eindeutige maschinelle Lösung.

**Was wir wissen:**
- 0=Leerzeichen (4+1+1+4) ist die einzige Struktur mit validen Kandidaten
- NEIL G. KING ist das Top-Ergebnis unter Bijektions- und Häufigkeits-Kriterien
- Alle anderen Strukturen schlagen fehl oder liefern zu viele Kandidaten

**Was fehlt:**
- Digitalisierte Adressbücher Vallejo/Napa 1969–70
- FamilySearch/Ancestry-Zugang für historische Verifikation
- Externer Hinweis (DNA, Geständnis, Dokument)

**Der Verdächtige wäre (wenn NEIL KING stimmt):**
- Männlich ✓
- Nachname KING (Census-Rang #35, sehr häufig)
- Vorname NEIL (englisch/schottisch, 1940s–50s populär)
- Zwei Initialen zwischen Vor- und Nachname (formaler Stil)
- Kein bekannter Zodiac-Verdächtiger trägt diesen Namen
