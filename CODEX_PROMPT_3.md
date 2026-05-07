# Codex-Prompt 3: Z13 — Nächste Schritte nach Erschöpfung einfacher Modelle

## Kontext

Ich arbeite an der Z13-Chiffre des Zodiac-Killers ("My name is —" Brief, 20. April 1970):

```
AENz0K0M0[NAM
```

13 Zeichen, 8 eindeutige Symbole. Zwingend durch Symbolwiederholung:
- text[0] = text[11]   (Symbol A, 2×)
- text[2] = text[10]   (Symbol N, 2×)
- text[4] = text[6] = text[8]   (Symbol 0, 3×)
- text[7] = text[12]   (Symbol M, 2×)

## Robuster Hauptbefund (bestätigt)

Beide Interpretationen der 0-Symbole konvergieren auf dieselbe Lösung:

**NEIL [X]. G. KING**

Symbol-Mapping (A→N, E→E, N→I, z→L, 0→Leerzeichen, K→[frei], M→G, [→K).
Alle 7 bekannten Werte {N, E, I, L, ' ', G, K} sind bijektiv eindeutig. ✓

## Vollständig ausgeschlossene Methoden

Alle folgenden Ansätze wurden implementiert und ergaben **0 bijektive Treffer**:

| Methode | Getestet | Ergebnis |
|---|---|---|
| Railfence 2/3/4-rail | Alle Varianten mit 0=Space | 0 Treffer |
| Columnar-Transposition ncols 2–6 | Alle Permutationen | 0 Treffer |
| Odd-then-Even / Even-then-Odd | Beide Richtungen | 0 Treffer |
| Reverse | — | 0 Treffer |
| Vigenere (14 Zodiac-Schlüssel) | ZODIAC, PARADICE, SLAVES, KILL, MYNAMEIS, SFPD, BOMB, GAS, KNIFE, u.a. | 0 Treffer |
| Beaufort (dieselben 14 Schlüssel) | — | 0 Treffer |
| Brieftext-Typos als Schlüssel | 9 Varianten aus 6 Fehlschreibungen | 0 Treffer |
| Caesar (alle 26 Shifts) | Preserviert alle 4 Constraints trivial | 0 Namens-Treffer |
| M=Leerzeichen | — | 0 Treffer |
| No-Space (13 Buchstaben) | — | Nur 3 Kandidaten, alle weiblich |
| Bekannte Verdächtige (Van Best, Kane, Allen u.a.) | — | Kein einziger erfüllt Constraints |
| Taunts/Phrasen (FUCKPOLICE etc.) | — | Alle scheitern an t[0]=t[8] |

## Was noch offen ist

1. Symbol K (erste Initial) ist frei — welcher Buchstabe aus {A,B,C,D,F,H,J,O,P,Q,R,S,T,U,V,W,X,Y,Z}?
2. Historische Verifikation: NEIL [X]. G. KING in Vallejo/Bay Area 1968–1970 nicht gefunden
3. Z32 ("C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9") als eigenständige Chiffre ungelöst
4. Selbstreferenz-Hypothese nicht formal getestet

---

## Frage 1: Einschränkung des freien Symbols K (erste Initial)

Symbol K kommt in Z13 genau 1× vor (Position 5). Es muss auf einen Buchstaben abbilden,
der **nicht** in {N, E, I, L, G, K, ' '} liegt — also aus:
{A, B, C, D, F, H, J, O, P, Q, R, S, T, U, V, W, X, Y, Z}

19 mögliche Werte.

**Frage:** Gibt es einen statistischen oder linguistischen Test, der die 19 Kandidaten für
die erste Initial weiter einschränkt? Zum Beispiel:
- Häufigkeitsverteilung von Mittleren Initialen in US-Männern 1930–1950 (J, W, R dominieren?)
- Strukturelle Hinweise aus dem Brief-Kontext ("My name is —")?
- Irgendwelche Constraints aus Z32, falls die Chiffren verwandt sind?

Wie würdest du den K-Raum rational auf ≤5 Kandidaten einschränken?

---

## Frage 2: Genealogische Suchstrategie (konkret, Schritt für Schritt)

Ziel: NEIL [X]. G. KING verifizieren oder falsifizieren.
Bekannte Parameter: männlich, Bay Area (Vallejo/SF/Napa), Geburtsjahr ca. 1930–1950.

Verfügbare Ressourcen:
- MyHeritage (Vallejo City Directory 1955, 1957)
- FamilySearch (Solano County Census 1940/1950)
- Ancestry (mit Account)
- Genealogical Society of Vallejo-Benicia (gsvb.org, Email raus)
- California Death Index (kostenfrei, StanislausGenWeb)
- SSDI (Social Security Death Index, kostenfrei online)

**Frage:** Was ist die effizienteste Suchreihenfolge und welche konkreten Suchbegriffe/Filter
soll ich verwenden? Welche Einträge außer Adressbüchern (z.B. Wählerregistrierung, Todesregister,
Militärdienst, Steuerlisten) wären besonders aufschlussreich für jemanden der 1968–1970 in Vallejo lebte?

---

## Frage 3: Jenseits einfacher Substitution — welche Modelle sind noch ungetestet?

Alle einfachen monoalphabetischen und polyalphabetischen Modelle sind ausgeschlossen.
Das Constraint-Muster (4 Gleichheitsbedingungen) ist resistent gegen alle getesteten Transformationen.

**Frage:** Welche Chiffren-Familien jenseits einfacher Substitution könnten theoretisch
das beobachtete Muster erzeugen, während NEIL [X]. G. KING als Klartext funktioniert?

Konkret interessiert mich:
- Polygraphische Chiffren (Playfair, Four-Square): Wie würde ein manuell-erstelltes Playfair
  die 13-Zeichen-Ausgabe erzeugen? Ist das kompatibel mit den Constraints?
- Affine Chiffre: c = (a·p + b) mod 26 — erfüllt sie das Constraint-Muster automatisch?
- Nihilist-Chiffre oder einfache numerische Kodierung?
- Gibt es einen mathematisch minimalen Beweis, dass bei diesen 4 Constraints + Bijektions-Bedingung
  die einfache Substitution die einzige mögliche Chiffren-Klasse ist?

---

## Frage 4: Selbstreferenz-Hypothese

Zodiac schrieb "My name is —" und setzte Z13 ein. Annahme bisher: Z13 = echter bürgerlicher Name.

**Hypothese:** Z13 = ein Alias/Pseudonym, das Zodiac sich selbst gegeben hat,
aber das nicht in Einwohnermelderegistern auftaucht.

**Frage:**
- Welche Terme aus dem bekannten Zodiac-Briefkorpus (1969–1974) hätten die richtige Struktur
  XXXX·X·X·XXXX (4+1+1+4 mit Bijektions-Bedingung)?
- Gibt es einen "NEIL G KING" in Zodiac-Briefen als versteckten Hinweis?
- Wie hoch ist die A-priori-Wahrscheinlichkeit, dass ein Serienmörder 1970 einen echten Namen
  vs. ein Pseudonym verschlüsselt — gibt es Präzedenzfälle?

---

## Frage 5: Z32 als eigenständige Chiffre

Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9" (32 Zeichen, 29 eindeutige Symbole)
Aus dem Brief vom 26. Juni 1970 ("Bombencode"), zusammen mit einer Straßenkarte,
auf der Mt. Diablo markiert war.

Zodiac schrieb: "The Mt. Diablo code concerns Radians & # inches along the radians"

Interne Constraints (wiederholte Symbole):
- 'C' an Positionen [0, 25]
- '9' an Positionen [1, 31]
- 'O' an Positionen [5, 13]

**Frage:** Wie würde man einen 32-Zeichen-Code systematisch analysieren, der:
- Möglicherweise GPS/Radian-Koordinaten + Distanz kodiert
- 29 von 32 eindeutige Symbole hat (sehr wenig Redundanz)
- Aus einem gemischten Alphabet (Buchstaben, Ziffern, Sonderzeichen) besteht

Gibt es bekannte Kodierungsschemas der 1960er/70er für Koordinaten in verschlüsselter Form?
Was wäre der erste analytische Schritt?

---

## Wichtig

- Ich bin an **konkreten, falsifizierbaren Tests** interessiert, nicht an offenen Spekulationen
- Jeder neue Ansatz soll eine klare Falsifikationsbedingung haben
- Die Bijektions-Bedingung ist zwingend und darf nicht aufgeweicht werden
- Bereits getestete Methoden (Tabelle oben) bitte **nicht** erneut vorschlagen
