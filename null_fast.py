"""
Schnelle Version: Null-Hypothese + Prime-Routen
Statt O(n²)-Loop: Lookup-Tabellen, nur relevante Nachnamen vorfiltern.
Läuft in Sekunden statt Stunden.
"""

import csv, time
from collections import defaultdict, Counter

Z13    = "AENz0K0M0[NAM"
ALPHA  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

# ── Daten laden ───────────────────────────────────────────────────────────────

def load_first(path="ssa_names.csv", y0=1930, y1=1980):
    d = defaultdict(float)
    with open(path) as f:
        for row in csv.DictReader(f):
            if y0 <= int(row["year"]) <= y1:
                n = row["name"].upper()
                if n.isalpha(): d[n] += float(row["percent"])
    return d

def load_last(path="us_surnames.txt"):
    s = set()
    with open(path) as f:
        for line in f:
            n = line.strip().upper()
            if n.isalpha(): s.add(n)
    return s

print("Lade Daten...", end=" ", flush=True)
t0 = time.time()
FIRST = load_first()
LAST  = load_last()
print(f"{len(FIRST)} Vornamen, {len(LAST)} Nachnamen ({time.time()-t0:.1f}s)")

# ── Ansatz 1: Null-Entfernung (Symbol '0' weglassen) ─────────────────────────
#
# Reduziert: A E N z K M [ N A M  (10 Zeichen)
# Muster:    a b c d f g h c a g
#
# Constraints (im 10-Zeichen-Text t):
#   t[0] == t[8]   (Symbol A)
#   t[2] == t[7]   (Symbol N)
#   t[5] == t[9]   (Symbol M)
#
# Für jeden Split len1+len2=10 (mit oder ohne Leerzeichen):
#   text = VORNAME + NACHNAME  (kein Leerzeichen, 10 Zeichen)
#   oder
#   text = VORNAME + ' ' + NACHNAME  (mit Leerzeichen, 11 Zeichen → nur 10 Buchstaben)
#
# Trick: Wir bauen einen Index der Nachnamen nach den Constraint-Buchstaben.

def build_last_index(last_set, by_chars):
    """
    by_chars: Liste von (position_im_lname, constraint_key_position_im_fname)
    Baut {(char_at_pos0, char_at_pos1, ...): [lname, ...]} Index.
    """
    idx = defaultdict(list)
    for lname in last_set:
        key = tuple(lname[p] if p < len(lname) else None for p in by_chars)
        if None not in key:
            idx[key].append(lname)
    return idx

def search_null(split_lengths, space=False):
    """
    split_lengths: (len_fname, len_lname)
    space: ob ein Leerzeichen zwischen Vor- und Nachname steht

    10-Zeichen-Text t (nach Null-Entfernung):
      t = fname (+ ' ') + lname

    Constraints t[0]=t[8], t[2]=t[7], t[5]=t[9] auf diesen 10-Zeichen-String anwenden.
    """
    lf, ll = split_lengths
    if space:
        if lf + 1 + ll != 10: return []
    else:
        if lf + ll != 10: return []

    # Offset: wo fängt lname im 10-Zeichen-String an?
    lname_start = lf + (1 if space else 0)

    # Constraints: t[i] == t[j] → Buchstabe an Position i im Gesamttext
    # Wir prüfen welche Constraints Buchstaben aus lname mit fname verbinden
    def get_char(text_pos, fname, lname):
        if text_pos < lf:
            return fname[text_pos]
        elif space and text_pos == lf:
            return ' '
        else:
            return lname[text_pos - lname_start]

    candidates = []
    # Für jeden Vornamen der passenden Länge:
    for fname, fscore in FIRST.items():
        if len(fname) != lf: continue

        # Aus Constraints ableiten: welche Buchstaben muss lname haben?
        # t[0]=fname[0], t[8]=lname[8-lname_start]
        # t[2]=fname[2], t[7]=lname[7-lname_start]
        # t[5]=?, t[9]=?

        constraints_ok = True
        lname_reqs = {}  # {position_in_lname: required_char}

        # Constraint 1: t[0] == t[8]
        if 0 < lf and 8 >= lname_start:
            req_pos = 8 - lname_start
            if req_pos < ll:
                lname_reqs[req_pos] = fname[0]
            elif 8 < lf:
                if fname[0] != fname[8]: constraints_ok = False
        elif 0 >= lname_start and 8 >= lname_start:
            # Beide in lname
            lname_reqs_pair = (0 - lname_start, 8 - lname_start)
            # handled below

        # Constraint 2: t[2] == t[7]
        if 2 < lf and 7 >= lname_start:
            req_pos = 7 - lname_start
            if req_pos < ll:
                existing = lname_reqs.get(req_pos)
                if existing and existing != fname[2]:
                    constraints_ok = False
                else:
                    lname_reqs[req_pos] = fname[2]
            elif 7 < lf:
                if fname[2] != fname[7]: constraints_ok = False

        # Constraint 3: t[5] == t[9]
        c5 = fname[5] if 5 < lf else None
        c9_lpos = 9 - lname_start
        if c5 is not None and 0 <= c9_lpos < ll:
            existing = lname_reqs.get(c9_lpos)
            if existing and existing != c5:
                constraints_ok = False
            else:
                lname_reqs[c9_lpos] = c5
        elif 5 >= lname_start and 9 >= lname_start:
            l5 = 5 - lname_start
            l9 = 9 - lname_start
            # Both in lname — handle in loop below

        if not constraints_ok: continue

        # Nachname filtern
        for lname in LAST:
            if len(lname) != ll: continue
            ok = True
            for pos, req in lname_reqs.items():
                if lname[pos] != req:
                    ok = False
                    break
            # Zusatz: falls t[5] und t[9] beide in lname
            if ok and 5 >= lname_start and 9 >= lname_start:
                l5 = 5 - lname_start
                l9 = 9 - lname_start
                if 0 <= l5 < ll and 0 <= l9 < ll:
                    if lname[l5] != lname[l9]: ok = False
            if ok:
                if space:
                    text = fname + ' ' + lname
                else:
                    text = fname + lname
                candidates.append((fscore, text, fname, lname))

    return candidates

print("\n=== Ansatz 1: Null-Entfernung ('0' = Füller) ===")
print(f"Reduzierter String: {''.join(c for c in Z13 if c != '0')}  (10 Zeichen)")
print(f"Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]\n")

all_null = []
for lf in range(3, 8):
    for ll in range(3, 8):
        for sp in [False, True]:
            size = lf + ll + (1 if sp else 0)
            if size != 10: continue
            cands = search_null((lf, ll), space=sp)
            if cands:
                label = f"{lf}+{'+1+' if sp else '+'}{ll}"
                all_null.extend(cands)

all_null.sort(reverse=True)
seen = set()
unique = []
for score, text, fn, ln in all_null:
    if text not in seen:
        seen.add(text)
        unique.append((score, text, fn, ln))

KNOWN_FIRST = {"JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD",
               "GEORGE","THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER",
               "HAROLD","PAUL","JACK","CARL","ARTHUR","ALBERT","PETER","RAYMOND",
               "GARY","LARRY","JERRY","DENNIS","GERALD","ROGER","KEITH","ALAN",
               "MARK","BRUCE","RALPH","FRED","ERIC","NEIL","DALE","DEAN","GLEN",
               "CHAD","EARL","TROY","SEAN","RYAN","KURT","GENE","LOIS","MARY",
               "LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
               "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH",
               "SCOTT","JAMES","LARRY","TERRY","BARRY","PERRY","HENRY","KENNY",
               "BENNY","DANNY","RANDY","SANDY","CANDY","MANDY","CINDY","MINDY",
               "WENDY","TRUDY","JUDY","RUDY","JODY","CODY","BRADY","GRADY"}
KNOWN_LAST  = {"SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE",
               "TAYLOR","JACKSON","WHITE","HARRIS","MARTIN","THOMPSON",
               "GARCIA","CLARK","LEWIS","KING","HILL","SCOTT","GREEN","ADAMS",
               "BAKER","NELSON","CARTER","EVANS","COLLINS","ROGERS","REED",
               "COOK","MORGAN","BELL","COOPER","WARD","GRAY","WOOD","ROSS",
               "HUNT","COLE","FORD","RYAN","LONG","SHAW","WEBB","WADE","RICE",
               "LANE","NASH","MANN","CARR","SNOW","WALL","HOLT","HART","WARE",
               "HALE","WISE","RICH","REID","MACK","LOVE","PAGE","BOND","TODD",
               "BUSH","ROWE","WOLF","MOON","ROTH","NEAL","DEAN","FREE","WREN"}

print(f"Gefunden: {len(unique)} eindeutige Kandidaten\n")
print(f"{'Rang':>4}  {'Name':<22}  {'Score':>8}  Hinweis")
print("-"*60)
for i, (score, text, fn, ln) in enumerate(unique[:30], 1):
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {text:<22}  {score:>8.5f}  {flag}")

# Speichern
with open("null_candidates.txt", "w") as f:
    f.write(f"# Null-Hypothese: '0' entfernt → 10-Zeichen-Muster\n")
    f.write(f"# Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]\n\n")
    for i, (score, text, fn, ln) in enumerate(unique, 1):
        f.write(f"{i:4}. {text:<22}  score={score:.5f}\n")
print(f"\n→ {len(unique)} Kandidaten in null_candidates.txt")

# ── Ansatz 2: Prime-Routen ────────────────────────────────────────────────────

print("\n=== Ansatz 2: Prime-Routen (mod-13 Sprünge) ===")
original = Counter(Z13)
for s in range(1, 13):
    route   = [(k*s) % 13 for k in range(13)]
    routed  = ''.join(Z13[i] for i in route)
    repeats = {c: n for c, n in Counter(routed).items() if n > 1}
    changed = "  ← ANDERES MUSTER" if repeats != dict(original) else ""
    print(f"  s={s:2}: {routed}  Wiederholungen: {repeats}{changed}")

print(f"\nGesamtlaufzeit: {time.time()-t0:.1f}s")
