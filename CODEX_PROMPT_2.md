# Codex-Prompt: Z13 — Neue Impulse nach Konvergenz-Befund

## Kontext

Ich arbeite an der Z13-Chiffre des Zodiac-Killers ("My name is —" Brief, 20. April 1970):

```
AENz0K0M0[NAM
```

13 Zeichen, 8 eindeutige Symbole. Zwingend durch Symbolwiederholung:
- text[0] = text[11]   (Symbol A)
- text[2] = text[10]   (Symbol N)
- text[4] = text[6] = text[8]   (Symbol 0)
- text[7] = text[12]   (Symbol M)

## Was wir wissen

### Robuster Hauptbefund

Beide Interpretationen der 0-Symbole (0=Leerzeichen UND 0=Füller/Null) konvergieren auf dieselbe Lösung:

**NEIL [X]. G. KING**

Symbol-Mapping:
- A → N
- E → E
- N → I
- z → L
- 0 → Leerzeichen (oder Null)
- K → [frei, 1. Initial]
- M → G
- [ → K

Alle 7 bekannten Werte {N, E, I, L, ' ', G, K} sind bijektiv eindeutig. ✓

### Was vollständig ausgeschlossen ist

- M = Leerzeichen: 0 bijektive Kandidaten
- Alle bekannten Zodiac-Verdächtigen (Earl Van Best, Lawrence Kane, Arthur Leigh Allen etc.): keiner erfüllt die Constraints
- Taunt-Phrasen (FUCKPOLICE, HELLSLAVES etc.): alle scheitern an t[0]=t[8] und t[2]=t[7]
- Mod-13-Transpositionen: erhalten Wiederholungsmuster unverändert
- No-Space (13 Buchstaben): nur 3 Kandidaten, alle weiblich

### Was noch offen ist

- NEIL KING nicht in SF-Adressbuch 1969 gefunden; Vallejo/Napa nicht durchsucht
- Kein externer Beweis (DNA, Dokument, Fingerabdruck)
- Railfence und Columnar-Transposition noch nicht systematisch mit Space/Null-Modell kombiniert
- Brieftext als Schlüsselmaterial noch nicht getestet
- Polyalphabetische Modelle (Vigenere, Beaufort) noch nicht erschöpfend

## Konkrete Fragen an dich

Ich suche **neue, umsetzbare Ansätze** — keine Wiederholung bereits ausgeschlossener Methoden.

### Frage 1: Transposition + Struktur-Kombination

Welche konkreten Transpositions-Familien sollte ich systematisch mit dem 0=Space-Modell kombinieren?

Ich denke an:
- 2-rail und 3-rail Railfence auf den vollen 13-Zeichen-String
- Columnar-Transposition mit Spaltenbreiten 2,3,4,5,6,7
- "Odd-then-even positions" (Positionen 0,2,4,6,8,10,12 dann 1,3,5,7,9,11)

Wie würde ich das effizient testen? Wie viele Kombinationen sind das wirklich?

### Frage 2: Brieftext-Extraktion

Der Brief vom 20.04.1970 enthält absichtliche Schreibfehler:
- "cerous" statt "serious"
- "cid" statt "did"
- "doo" statt "do"
- "elses" statt "else"
- "teritory" statt "territory"
- "figgure" statt "figure"

Wie würdest du aus diesen Fehlern systematisch Schlüsselmaterial extrahieren? Welche Encoding-Regeln sind historisch plausibel für manuell erstellte Chiffren aus den 1960ern?

### Frage 3: Polyalphabetisch mit engen Priors

Ich will Vigenere/Beaufort mit wenigen Schlüsselkandidaten testen:
- ZODIAC (6 Zeichen)
- PARADICE (8 Zeichen)
- SLAVES (6 Zeichen)
- KILL (4 Zeichen)
- MYNAMEIS (8 Zeichen)

Problem: Die nicht-alphabetischen Symbole (0 und [) müssen numerisch kodiert werden. Welche Kodierung ist sinnvoll? Und: Bei einem 13-Zeichen-Cipher mit 6-8-Zeichen-Schlüssel — wie viele Freiheitsgrade bleiben, und reicht das für einen eindeutigen Test?

### Frage 4: Selbstreferenz

Was wenn "My name is —" nicht der Name des Killers ist, sondern ein Alias, den er sich im Brief-Corpus selbst gegeben hat? Welche Terme aus den bekannten Zodiac-Briefen (1969-1974) würde NEIL G. KING strukturell erklären können? Und welche anderen Terme hätten die richtige Länge und das richtige Muster?

### Frage 5: Genealogische Suchstrategie

Ich habe Zugang zu:
- MyHeritage (Vallejo City Directory 1955, 1957)
- FamilySearch (Solano County Census)
- Ancestry (mit Account)

Was ist die effizienteste Suchstrategie für NEIL [X]. G. KING, männlich, plausibles Geburtsjahr ca. 1930–1950, Bay Area Wohnort 1968–1970? Welche Einträge außer Adressbüchern wären am aufschlussreichsten?

## Wichtig

- Ich bin an konkreten, falsifizierbaren Tests interessiert, nicht an offenen Spekulationen
- Jeder neue Ansatz soll eine klare Falsifikationsbedingung haben
- Die Bijektions-Bedingung ist zwingend und darf nicht aufgeweicht werden
