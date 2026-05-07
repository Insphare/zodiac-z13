"""
Null-Hypothese (erweitert): Symbol '0' wird entfernt.
Reduzierter String: AENzKM[NAM (10 Zeichen)

Constraints auf dem reduzierten String:
  t[0] = t[8]   (Symbol A)
  t[2] = t[7]   (Symbol N)
  t[5] = t[9]   (Symbol M)

Bijektion: 7 eindeutige Symbole → 7 verschiedene Zeichen.

Testet drei Korpora:
  A. Echte Namen (SSA + Census)
  B. Persona / Popkultur / Taunt (manuell + Zeitungskorpus)
  C. Literarische / historische Figuren
"""

import csv, time
from collections import defaultdict

REDUCED = "AENzKM[NAM"   # 10 Zeichen nach Entfernung der 0en
CONSTRAINTS = [(0, 8), (2, 7), (5, 9)]

t0 = time.time()

# ── Bijektions-Check ─────────────────────────────────────────────────────────

def is_valid(text):
    """Prüft Constraints UND Bijektion für 10-Zeichen-Text."""
    if len(text) != 10:
        return False
    for i, j in CONSTRAINTS:
        if text[i] != text[j]:
            return False
    # 7 Symbole müssen 7 verschiedene Zeichen sein
    vals = {text[0], text[1], text[2], text[3], text[4], text[5], text[6]}
    return len(vals) == 7

# ── Korpus B: Persona / Taunt / Popkultur ────────────────────────────────────

# Alle Kandidaten als direkte 10-Zeichen-Strings (Leerzeichen erlaubt, zählt als Zeichen)
# Format: (string, beschreibung)
PERSONA_CORPUS = [
    # Zodiac-Eigenbezeichnungen aus Briefen
    ("THEZODIAC!", "Zodiac Selbst"),
    ("ZODIACMANZ", "Zodiac"),
    # MAD Magazine
    ("ALFREDNEUN", "Alfred E. Neuman Kurzform"),
    ("ALFRDNEUMN", "Alfred E. Neuman Anagramm"),
    # Gilbert & Sullivan / Mikado
    ("THEMIKADOX", "Mikado"),
    ("KOKOTHEKAT", "Koko (Mikado)"),
    # Klassische Schurken / Populärkultur 1960er
    ("DRDOOLITLL", "Dr. Dolittle"),
    ("THESPECTRE", "Spectre (Bond)"),
    ("GOLDFINGMZ", "Goldfinger"),
    # Polizei-Taunt
    ("KILLCOPSNO", "Taunt"),
    ("SOLVEMECOP", "Taunt"),
    # Selbst-Referenz
    ("MYSELFRULE", "Selbstreferenz"),
    # Astrologische Terme
    ("ZODIACSTAR", "Astro"),
    ("SAGITTARIX", "Sagittarius"),
    # Bekannte Krimis / Horror
    ("JACKTHERIA", "Jack the Ripper"),
    ("DRACULAREP", "Dracula"),
    # Zeitgenössische TV/Pulp-Figuren
    ("BONANZAJIM", "Bonanza Charakter"),
    ("SPOCKSPLOG", "Star Trek"),
    # Kurze Phrasen
    ("CATCHMEIFX", "Catch me if you can"),
    ("GODBLESSME", "Gottlos Taunt"),
    # Eigene Namens-Experimente
    ("NEILGAKING", "Neil G. A King Variante"),
    ("NEILAKING!", "Neil A. King"),
]

# ── Korpus C: Historische / literarische Figuren ─────────────────────────────

LITERARY_CORPUS = [
    # Sherlock Holmes Figuren
    ("MORIARTYME", "Moriarty"),
    ("IRENEADLRZ", "Irene Adler"),
    # Mark Twain
    ("TOMMSAWYRZ", "Tom Sawyer Anagramm"),
    ("HUCKFINMRZ", "Huck Finn Anagramm"),
    # Jack London
    ("JACKLDN123", "Jack London"),
    # Biblische Namen
    ("LUCIFERMIX", "Lucifer"),
    ("SATANSLAVE", "Satan"),
    # Lokale SF-Kultfiguren
    ("CITYFERLIN", "Lawrence Ferlinghetti"),
]

# ── Daten laden (Korpus A) ────────────────────────────────────────────────────

print("Lade SSA + Census Daten...", end=" ", flush=True)
first_by_len = defaultdict(dict)
with open("ssa_names.csv") as f:
    for row in csv.DictReader(f):
        if 1930 <= int(row["year"]) <= 1980:
            n = row["name"].upper()
            if n.isalpha() and 2 <= len(n) <= 9:
                first_by_len[len(n)][n] = first_by_len[len(n)].get(n, 0) + float(row["percent"])

last_by_len = defaultdict(set)
with open("us_surnames.txt") as f:
    for line in f:
        n = line.strip().upper()
        if n.isalpha() and 2 <= len(n) <= 8:
            last_by_len[len(n)].add(n)
print(f"OK ({time.time()-t0:.1f}s)")

# ── Hauptsuche Korpus A: Namen ────────────────────────────────────────────────

name_results = []  # (score, text, fname, lname, structure)

for fl in range(2, 9):
    for ll in range(2, 9):
        if fl + ll != 10:
            continue
        if fl not in first_by_len or ll not in last_by_len:
            continue

        # Constraints ableiten (text = fname[0..fl-1] + lname[0..ll-1])
        cross = {}     # lname_pos → fname_pos
        lname_eq = []  # (lname_pos, lname_pos)
        skip = False

        for i, j in CONSTRAINTS:
            fi = i < fl
            fj = j < fl
            if fi and fj:
                if fl > i and fl > j and j < fl:
                    if i < fl and j < fl and first_by_len.get(fl) is not None:
                        pass  # fname-intern, wird unten beim fname geprüft
            elif fi and not fj:
                lj = j - fl
                if 0 <= lj < ll:
                    if lj in cross and cross[lj] != i:
                        skip = True; break
                    cross[lj] = i
            elif not fi and fj:
                li = i - fl
                if 0 <= li < ll and j < fl:
                    if li in cross and cross[li] != j:
                        skip = True; break
                    cross[li] = j
            else:
                li = i - fl
                lj = j - fl
                if 0 <= li < ll and 0 <= lj < ll:
                    lname_eq.append((li, lj))

        if skip:
            continue

        # lname-Index bauen
        sorted_lkeys = sorted(cross.keys())
        idx = defaultdict(list)
        for lname in last_by_len[ll]:
            ok = all(lname[p1] == lname[p2] for p1, p2 in lname_eq if p1 < ll and p2 < ll)
            if not ok:
                continue
            key = tuple(lname[k] for k in sorted_lkeys if k < ll)
            idx[key].append(lname)

        # fname-interne Constraints
        fname_self = []
        for i, j in CONSTRAINTS:
            if i < fl and j < fl:
                fname_self.append((i, j))

        for fname, fscore in first_by_len[fl].items():
            if not all(fname[i] == fname[j] for i, j in fname_self if i < fl and j < fl):
                continue

            key = tuple(fname[cross[lk]] for lk in sorted_lkeys if lk < ll and cross[lk] < fl)
            for lname in idx.get(key, []):
                text = fname + lname
                if is_valid(text):
                    name_results.append((fscore, text, fname, lname, f"{fl}+{ll}"))

name_results.sort(reverse=True)

# Deduplizieren
seen = set()
name_unique = []
for score, text, fn, ln, struct in name_results:
    if text not in seen:
        seen.add(text)
        name_unique.append((score, text, fn, ln, struct))

# ── Korpus B+C: Persona / Literatur prüfen ────────────────────────────────────

taunt_matches = []
for (candidate, desc) in PERSONA_CORPUS + LITERARY_CORPUS:
    c = candidate.upper().replace(" ", "").replace("!", "").replace(".", "")
    # Kürzen/Strecken auf 10 falls nötig
    if len(c) != 10:
        continue
    if is_valid(c):
        taunt_matches.append((c, desc))

# ── Ausgabe ───────────────────────────────────────────────────────────────────

KNOWN_FIRST = {
    "JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD","GEORGE",
    "THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER","HAROLD","PAUL","JACK",
    "CARL","ARTHUR","ALBERT","PETER","RAYMOND","GARY","LARRY","JERRY","DENNIS",
    "GERALD","ROGER","KEITH","ALAN","MARK","BRUCE","RALPH","FRED","ERIC","NEIL",
    "DALE","DEAN","GLEN","CHAD","EARL","TROY","SEAN","RYAN","KURT","GENE",
    "LOIS","MARY","LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
    "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH","SCOTT","TERRY",
    "BARRY","LARRY","PERRY","DANNY","RANDY","SANDY","CINDY","WENDY","KENNY",
}
KNOWN_LAST = {
    "SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR",
    "JACKSON","WHITE","HARRIS","MARTIN","THOMPSON","GARCIA","CLARK","LEWIS",
    "KING","HILL","SCOTT","GREEN","ADAMS","BAKER","NELSON","CARTER","EVANS",
    "COLLINS","ROGERS","REED","COOK","MORGAN","BELL","COOPER","WARD","GRAY",
    "WOOD","ROSS","HUNT","COLE","FORD","RYAN","LONG","SHAW","WEBB","WADE",
    "RICE","LANE","NASH","MANN","CARR","SNOW","WALL","HOLT","HART","WARE",
    "HALE","WISE","RICH","REID","MACK","LOVE","PAGE","BOND","TODD","BUSH",
    "HALL","ROSE","DEAN","NEAL","WREN","ROTH","MOON","ROWE","WOLF","MEAD",
}

print(f"\n{'='*70}")
print(f"NULL-HYPOTHESE: '0' entfernt → '{REDUCED}'")
print(f"Bijektive Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]")
print(f"{'='*70}")

print(f"\n── Korpus A: Echte Namen ({len(name_unique)} bijektive Kandidaten) ──")
print(f"{'Rang':>4}  {'Name':<22}  {'Struktur':>6}  {'Score':>8}  Hinweis")
print("-"*65)
for i, (score, text, fn, ln, struct) in enumerate(name_unique[:50], 1):
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {text:<22}  {struct:>6}  {score:>8.5f}  {flag}")

print(f"\n── Korpus B+C: Persona / Popkultur / Literatur ──")
if taunt_matches:
    for c, desc in taunt_matches:
        print(f"  ✓ '{c}'  ({desc})")
else:
    print("  Keine Treffer — alle getesteten Taunt-Strings scheitern an den Constraints.")

print(f"\n{'='*70}")
print(f"Laufzeit: {time.time()-t0:.1f}s")

# ── Alle Ergebnisse speichern ─────────────────────────────────────────────────

with open("null_extended_candidates.txt", "w") as f:
    f.write("# Null-Hypothese (erweitert): '0' entfernt\n")
    f.write(f"# Reduziert: {REDUCED}\n")
    f.write("# Bijektions-Check aktiv\n\n")
    f.write("## Echte Namen\n")
    for i, (score, text, fn, ln, struct) in enumerate(name_unique, 1):
        f.write(f"{i:5}. {text:<22}  {struct}  score={score:.5f}\n")
    f.write("\n## Persona / Popkultur / Literatur\n")
    for c, desc in taunt_matches:
        f.write(f"  {c}  — {desc}\n")
    if not taunt_matches:
        f.write("  (keine Treffer)\n")

print(f"→ {len(name_unique)} Kandidaten in null_extended_candidates.txt")
