"""
Korrekte bijektive Z13-Suche.

Z13 = "AENz0K0M0[NAM"
8 Symbole: A(pos 0,11), E(pos 1), N(pos 2,10), z(pos 3),
           0(pos 4,6,8), K(pos 5), M(pos 7,12), [(pos 9)

Bijektionspflicht: Jedes Symbol → eindeutiger Buchstabe (oder Leerzeichen).
d.h. alle 8 Symbol-Werte müssen verschieden sein.

Hypothese 0=Leerzeichen → Struktur: XXXX ' ' X ' ' X ' ' XXXX
Positionen: FIRST(0-3) _ INIT1(5) _ INIT2(7) _ LAST(9-12)

Symbol-Werte:
  A  → FIRST[0] = LAST[2]   (Constraint zwingend)
  E  → FIRST[1]
  N  → FIRST[2] = LAST[1]   (Constraint zwingend)
  z  → FIRST[3]
  0  → ' ' (Leerzeichen)
  K  → INIT1   (frei, aber eindeutig)
  M  → INIT2 = LAST[3]       (Constraint zwingend)
  [  → LAST[0]

Bijektionstest:
  {FIRST[0], FIRST[1], FIRST[2], FIRST[3], ' ', INIT2, LAST[0]} alle verschieden
  Dann kann INIT1 auf irgendeinen freien Buchstaben gesetzt werden.
"""

import csv, time
from collections import defaultdict

t0 = time.time()

print("Lade Daten...", end=" ", flush=True)
first_by_len = defaultdict(dict)
with open("ssa_names.csv") as f:
    for row in csv.DictReader(f):
        if 1930 <= int(row["year"]) <= 1980:
            n = row["name"].upper()
            if n.isalpha() and 2 <= len(n) <= 12:
                first_by_len[len(n)][n] = first_by_len[len(n)].get(n, 0) + float(row["percent"])

last_by_len = defaultdict(set)
with open("us_surnames.txt") as f:
    for line in f:
        n = line.strip().upper()
        if n.isalpha() and 2 <= len(n) <= 11:
            last_by_len[len(n)].add(n)

print(f"OK ({time.time()-t0:.1f}s)")

# ── Ansatz 1: 0=Leerzeichen → XXXX X X XXXX (Haupt-Hypothese) ────────────────

print("\n=== Hypothese 0=Leerzeichen (XXXX·X·X·XXXX) ===")
print("Symbol-Werte müssen alle verschieden sein (Bijektion)")

fl, ll = 4, 4

# Lname-Index: lname[1]=fname[2], lname[2]=fname[0]
# → Schlüssel: (lname[1], lname[2])
lname_idx = defaultdict(list)
for lname in last_by_len[ll]:
    lname_idx[(lname[1], lname[2])].append(lname)

candidates_0space = []

for fname, fscore in first_by_len[fl].items():
    key = (fname[2], fname[0])  # lname[1]=fname[2], lname[2]=fname[0]

    for lname in lname_idx.get(key, []):
        init2 = lname[3]  # INIT2 = LAST[3] (M-Constraint)

        # 7 bekannte Symbol-Werte (ohne INIT1, der frei gewählt wird)
        known = {fname[0], fname[1], fname[2], fname[3], ' ', init2, lname[0]}

        if len(known) != 7:
            continue  # Kollision unter bekannten Werten

        # Mindestens ein freier Buchstabe für INIT1?
        all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        free = all_letters - known - {' '}
        if not free:
            continue  # Kein Buchstabe für INIT1 übrig

        candidates_0space.append((fscore, fname, lname, init2, sorted(free)))

candidates_0space.sort(reverse=True)
print(f"Bijektive Kandidaten: {len(candidates_0space)}")

# ── Ansatz 2: M=Leerzeichen → XXXXXXX·XXXX + trailing space ──────────────────

print("\n=== Hypothese M=Leerzeichen (XXXXXXX·XXXX) ===")
# M an Positionen 7 und 12 → beide Leerzeichen
# Struktur: FIRST(7) ' ' LAST(4) ' ' (trailing)
# Positionen: 0-6 = FIRST, 7=Leerzeichen, 8-11 = LAST, 12=trailing Leerzeichen

# Constraints:
# A (pos 0,11): FIRST[0] = LAST[3]
# N (pos 2,10): FIRST[2] = LAST[2]
# 0 (pos 4,6,8): FIRST[4] = FIRST[6] = LAST[0] (LAST[0] = 9-7... wait)

# Position 8 → LAST[0] (lname starts at position 8)
# Position 4 → FIRST[4]
# Position 6 → FIRST[6]
# → FIRST[4] = FIRST[6] = LAST[0]

# Symbol-Werte:
# A → FIRST[0]
# E → FIRST[1]
# N → FIRST[2]
# z → FIRST[3]
# 0 → FIRST[4] = FIRST[6] = LAST[0]
# K → FIRST[5]
# M → ' '
# [ → LAST[1]

fl7, ll4 = 7, 4
lname_idx_m = defaultdict(list)
# LAST[0] determined by FIRST[4]
# LAST[2] = FIRST[2], LAST[3] = FIRST[0]
for lname in last_by_len[ll4]:
    # Index nach (LAST[2], LAST[3])
    lname_idx_m[(lname[2], lname[3])].append(lname)

candidates_mspace = []
for fname, fscore in first_by_len[fl7].items():
    if fname[4] != fname[6]:
        continue  # FIRST[4] = FIRST[6] required

    key = (fname[2], fname[0])  # LAST[2]=FIRST[2], LAST[3]=FIRST[0]

    for lname in lname_idx_m.get(key, []):
        if lname[0] != fname[4]:
            continue  # LAST[0] = FIRST[4]

        # 8 Symbol-Werte: A→FIRST[0], E→FIRST[1], N→FIRST[2], z→FIRST[3],
        #                  0→FIRST[4], K→FIRST[5], M→' ', [→LAST[1]
        vals = {fname[0], fname[1], fname[2], fname[3],
                fname[4], fname[5], ' ', lname[1]}
        if len(vals) == 8:
            candidates_mspace.append((fscore, fname, lname))

candidates_mspace.sort(reverse=True)
print(f"Bijektive Kandidaten: {len(candidates_mspace)}")

# ── Ansatz 3: No-Space (alle 13 Zeichen = Buchstaben) ─────────────────────────

print("\n=== No-Space: XXXXXXXXXXXXX (13 Buchstaben) ===")
# Bereits aus comprehensive_search.py bekannt: 3 Kandidaten
# Trotzdem hier neu berechnen für alle Längen

candidates_nospace = []

for fl_ns in range(3, 11):
    ll_ns = 13 - fl_ns
    if ll_ns < 2 or ll_ns > 11: continue
    if fl_ns not in first_by_len or ll_ns not in last_by_len: continue

    offset = fl_ns  # lname beginnt hier

    # Constraint-Paare im vollen 13-Zeichen-String (ohne Leerzeichen)
    # text = fname + lname
    pairs = [(0,11), (2,10), (4,6), (4,8), (7,12)]

    cross = {}    # lname_index → fname_index
    lname_eq = [] # lname-intern
    fname_eq = [] # fname-intern
    skip = False

    for (pi, pj) in pairs:
        fi = pi < fl_ns; fj = pj < fl_ns

        if fi and fj:
            fname_eq.append((pi, pj))
        elif fi and not fj:
            lj = pj - offset
            if 0 <= lj < ll_ns:
                if lj in cross and cross[lj] != pi:
                    skip = True; break
                cross[lj] = pi
        elif not fi and fj:
            li = pi - offset
            if 0 <= li < ll_ns and pj < fl_ns:
                if li in cross and cross[li] != pj:
                    skip = True; break
                cross[li] = pj
        else:
            li = pi - offset
            lj = pj - offset
            if 0 <= li < ll_ns and 0 <= lj < ll_ns:
                lname_eq.append((li, lj))

    if skip: continue

    sorted_lkeys = sorted(cross.keys())

    idx = defaultdict(list)
    for lname in last_by_len[ll_ns]:
        ok = all(0 <= p1 < ll_ns and 0 <= p2 < ll_ns and lname[p1] == lname[p2]
                 for (p1, p2) in lname_eq)
        if not ok: continue
        key = tuple(lname[k] for k in sorted_lkeys)
        idx[key].append(lname)

    for fname, fscore in first_by_len[fl_ns].items():
        ok = all(fname[i] == fname[j] for (i,j) in fname_eq if i < fl_ns and j < fl_ns)
        if not ok: continue

        key = tuple(fname[cross[lk]] for lk in sorted_lkeys)

        for lname in idx.get(key, []):
            text = fname + lname
            # 8 Symbol-Positionen: 0,1,2,3,4,5,7,9
            vals = {text[0], text[1], text[2], text[3],
                    text[4], text[5], text[7], text[9]}
            if len(vals) == 8:
                candidates_nospace.append((fscore, fname, lname))

candidates_nospace.sort(reverse=True)
print(f"Bijektive Kandidaten: {len(candidates_nospace)}")

# ── Ausgabe ───────────────────────────────────────────────────────────────────

KNOWN_FIRST = {"JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD",
               "GEORGE","THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER",
               "HAROLD","PAUL","JACK","CARL","ARTHUR","ALBERT","PETER","RAYMOND",
               "GARY","LARRY","JERRY","DENNIS","GERALD","ROGER","KEITH","ALAN",
               "MARK","BRUCE","RALPH","FRED","ERIC","NEIL","DALE","DEAN","GLEN",
               "CHAD","EARL","TROY","SEAN","RYAN","KURT","GENE","LOIS","MARY",
               "LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
               "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH","SCOTT",
               "JAMES","LARRY","TERRY","BARRY","PERRY","HENRY","KENNY","BENNY",
               "DANNY","RANDY","SANDY","CANDY","MANDY","CINDY","MINDY","WENDY",
               "IMOGENE","CHASTITY","STEPHEN","MICHAEL","KENNETH","TIMOTHY"}

KNOWN_LAST  = {"SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE",
               "TAYLOR","JACKSON","WHITE","HARRIS","MARTIN","THOMPSON",
               "GARCIA","CLARK","LEWIS","KING","HILL","SCOTT","GREEN","ADAMS",
               "BAKER","NELSON","CARTER","EVANS","COLLINS","ROGERS","REED",
               "COOK","MORGAN","BELL","COOPER","WARD","GRAY","WOOD","ROSS",
               "HUNT","COLE","FORD","RYAN","LONG","SHAW","WEBB","WADE","RICE",
               "LANE","NASH","MANN","CARR","SNOW","WALL","HOLT","HART","WARE",
               "HALE","WISE","RICH","REID","MACK","LOVE","PAGE","BOND","TODD",
               "BUSH","ROWE","WOLF","MOON","ROTH","NEAL","DEAN","FREE","WREN",
               "REVOIR","DEVOID","TRACY"}

print()
print("═"*75)
print("KANDIDATEN-ÜBERSICHT (bijektiv verifiziert)")
print("═"*75)

print(f"\n── 0=Leerzeichen (XXXX·X·X·XXXX): {len(candidates_0space)} Kandidaten ──")
print(f"{'Rang':>4}  {'Name':<30}  {'Score':>8}  Hinweis")
print("-"*65)
for i, (score, fn, ln, init2, free_init1) in enumerate(candidates_0space[:30], 1):
    name_str = f"{fn} * {init2}. {ln}"
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {name_str:<30}  {score:>8.5f}  {flag}")

print(f"\n── M=Leerzeichen (XXXXXXX·XXXX): {len(candidates_mspace)} Kandidaten ──")
for i, (score, fn, ln) in enumerate(candidates_mspace[:10], 1):
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {fn} {ln:<20}  {score:>8.5f}  {flag}")

print(f"\n── No-Space (XXXXXXXXXXXXX): {len(candidates_nospace)} Kandidaten ──")
for i, (score, fn, ln) in enumerate(candidates_nospace[:15], 1):
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {fn+' '+ln:<30}  {score:>8.5f}  {flag}")

# Zusammenfassung
print(f"\n{'═'*75}")
print(f"Gesamt bijektiv gültige Kandidaten:")
print(f"  0=Leerzeichen: {len(candidates_0space)}")
print(f"  M=Leerzeichen: {len(candidates_mspace)}")
print(f"  No-Space:      {len(candidates_nospace)}")

# Speichern
with open("bijective_candidates.txt", "w") as f:
    f.write("# Bijektiv gültige Z13-Kandidaten\n")
    f.write("# Symbol-Werte müssen alle 8 verschieden sein\n\n")

    f.write("## 0=Leerzeichen (XXXX·X·X·XXXX)\n")
    for i, (score, fn, ln, init2, free) in enumerate(candidates_0space, 1):
        f.write(f"{i:5}. {fn} * {init2}. {ln:<20}  score={score:.5f}\n")

    f.write("\n## No-Space (XXXXXXXXXXXXX)\n")
    for i, (score, fn, ln) in enumerate(candidates_nospace, 1):
        f.write(f"{i:5}. {fn} {ln:<20}  score={score:.5f}\n")

    f.write("\n## M=Leerzeichen (XXXXXXX·XXXX)\n")
    for i, (score, fn, ln) in enumerate(candidates_mspace, 1):
        f.write(f"{i:5}. {fn} {ln:<20}  score={score:.5f}\n")

print(f"\n→ bijective_candidates.txt geschrieben")
print(f"Laufzeit: {time.time()-t0:.1f}s")
