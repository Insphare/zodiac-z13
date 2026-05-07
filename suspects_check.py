"""
Alle bekannten Zodiac-Verdächtigen gegen Z13-Constraints prüfen.
Struktur (0=Space): VORNAME(4) INIT1(1) INIT2(1) NACHNAME(4)

Constraints:
  Vorname[0] = Nachname[2]
  Vorname[2] = Nachname[1]
  Initial2   = Nachname[3]
"""

Z13 = "AENz0K0M0[NAM"

# Alle je namentlich genannten Zodiac-Verdächtigen (Wikipedia + Fallakten)
SUSPECTS = [
    # (Vorname, Nachname, Quelle)
    ("ARTHUR",   "ALLEN",      "Hauptverdächtiger (SFPD)"),
    ("LEIGH",    "ALLEN",      "Hauptverdächtiger (SFPD)"),
    ("EARL",     "BEST",       "Earl Van Best Jr."),
    ("GARY",     "POSTE",      "Case Breakers 2021"),
    ("GARY",     "FRANCIS",    "Gary Francis Poste"),
    ("PAUL",     "DOERR",      "Amateur-Verdächtiger"),
    ("ROSS",     "SULLIVAN",   "Bibliotheksarbeiter CA"),
    ("JACK",     "TARRANCE",   "Howard Davis Jr. Theorie"),
    ("LOUIE",    "MYERS",      "Louie Joseph Myers"),
    ("DAVID",    "CARPENTER",  "Trailside Killer"),
    ("KJELL",    "QVALE",      "Brit. Autoimporteur CA"),
    ("MARVIN",   "MARGOLIS",   "alias Merrill"),
    ("RICHARD",  "MARSHALL",   "Fallakten"),
    ("RICHARD",  "GAIKOWSKI",  "Journalist SF"),
    ("RICHARD",  "HOFFMAN",    "Fallakten"),
    ("LAWRENCE", "KANE",       "Verdächtiger"),
    ("JIM",      "MORDECAI",   "Fallakten"),
    ("TED",      "KACZYNSKI",  "Unabomber-Theorie"),
    ("TED",      "BUNDY",      "Serientäter"),
    ("CHARLES",  "MANSON",     "Manson Family"),
    # Zusätzlich: Vornamen die zu Verdächtigen passen
    ("KANE",     "LAWRENCE",   "Lawrence Kane (umgekehrt)"),
    ("ALLEN",    "ARTHUR",     "Arthur Allen (umgekehrt)"),
    # Nicknames / Kurzformen
    ("RICK",     "MARSHALL",   "Richard Marshall"),
    ("DICK",     "MARSHALL",   "Richard Marshall"),
    ("RUSS",     "SULLIVAN",   "Ross Sullivan"),
]

def check_constraint(fname, lname):
    """Prüft ob Vor- und Nachname die Z13 0=Space Constraints erfüllen."""
    if len(fname) != 4 or len(lname) != 4:
        return None
    ok1 = fname[0] == lname[2]
    ok2 = fname[2] == lname[1]
    return ok1 and ok2

def check_4letter_variants(full_first, full_last, info):
    """Prüft alle 4-Buchstaben-Substrings der Namen."""
    results = []
    # Alle 4-buchst. Substrings des Vornamens
    firsts = set()
    if len(full_first) == 4:
        firsts.add(full_first)
    for i in range(len(full_first)-3):
        firsts.add(full_first[i:i+4])

    lasts = set()
    if len(full_last) == 4:
        lasts.add(full_last)
    for i in range(len(full_last)-3):
        lasts.add(full_last[i:i+4])

    for f in firsts:
        for l in lasts:
            ok = check_constraint(f, l)
            if ok:
                # Initial2 = Last[3]
                i2 = l[3]
                results.append((f, i2, l))
    return results

print("=== Zodiac-Verdächtige vs. Z13-Constraints ===")
print("Struktur (0=Space): VORNAME(4) INIT1 INIT2 NACHNAME(4)")
print(f"Constraints: Vorname[0]=Nachname[2], Vorname[2]=Nachname[1], Initial2=Nachname[3]")
print()

found_any = False
for fname, lname, info in SUSPECTS:
    matches = check_4letter_variants(fname, lname, info)
    if matches:
        found_any = True
        for f, i2, l in matches:
            print(f"  ★ {f} ?. {i2}. {l}  ← aus: {fname} {lname} ({info})")
            # Zeige vollständiges Mapping
            print(f"    Mapping: A→{f[0]}, E→{f[1]}, N→{f[2]}, z→{f[3]}, "
                  f"0→' ', K→(?), M→{i2}, [→{l[0]}")
    else:
        # Zeige warum es nicht passt (für 4-Buchst. Namen)
        if len(fname) == 4 and len(lname) == 4:
            need = f"Nachname[1]={fname[2]}, Nachname[2]={fname[0]}"
            got  = f"Nachname[1]={lname[1]}, Nachname[2]={lname[2]}"
            print(f"  ✗ {fname} {lname}: braucht {need}, hat {got}")

if not found_any:
    print("  Kein einziger bekannter Verdächtiger erfüllt die Z13-Constraints!")

print()
print("=== Bekannte Verdächtige die 4-Buchst. Namen haben ===")
for fname, lname, info in SUSPECTS:
    f4 = len(fname) == 4
    l4 = len(lname) == 4
    if f4 or l4:
        tag = []
        if f4: tag.append(f"Vorname '{fname}' ist 4 Buchst.")
        if l4: tag.append(f"Nachname '{lname}' ist 4 Buchst.")
        print(f"  {fname} {lname}: {', '.join(tag)}  ({info})")

print()
print("=== Cross-Check: Top-414-Kandidaten vs. Verdächtige ===")
# Lade unsere besten Kandidaten
try:
    with open("candidates_filtered.txt") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    candidates = [l.split()[0:4] for l in lines[:414]]
    candidate_names = set()
    for parts in candidates:
        if len(parts) >= 2:
            candidate_names.add(parts[0])  # Vorname

    suspect_fnames = {fname for fname, _, _ in SUSPECTS if len(fname) == 4}
    overlap = suspect_fnames & candidate_names
    if overlap:
        print(f"  Vornamen die sowohl in Kandidaten als auch bei Verdächtigen vorkommen:")
        for n in sorted(overlap):
            print(f"    {n}")
    else:
        print("  Keine Überschneidung zwischen Kandidaten-Vornamen und 4-Buchst.-Verdächtigen.")
except FileNotFoundError:
    print("  candidates_filtered.txt nicht gefunden.")
