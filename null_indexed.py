"""
Null-Hypothese: Symbol '0' = Füller/Null entfernen.
Reduzierter Text: AENzKM[NAM (10 Zeichen)
Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]

Für jede (len_fname, len_lname) Kombination:
  → Ableiten welche lname-Positionen gleich sein müssen
  → Surname-Index bauen: O(n) statt O(n²)
"""

import csv, time
from collections import defaultdict, Counter

Z13 = "AENz0K0M0[NAM"
REDUCED = ''.join(c for c in Z13 if c != '0')  # AENzKM[NAM

# Constraints im 10-Zeichen reduzierten Text
CONSTRAINTS_10 = [(0, 8), (2, 7), (5, 9)]   # (i,j): t[i]==t[j]

t0 = time.time()

# ── Daten laden (nur relevante Längen) ───────────────────────────────────────

print("Lade Daten...")
first_by_len = defaultdict(dict)   # {length: {name: score}}
with open("ssa_names.csv") as f:
    for row in csv.DictReader(f):
        if 1930 <= int(row["year"]) <= 1980:
            n = row["name"].upper()
            if n.isalpha() and 3 <= len(n) <= 8:
                first_by_len[len(n)][n] = first_by_len[len(n)].get(n, 0) + float(row["percent"])

last_by_len = defaultdict(set)     # {length: {name, ...}}
with open("us_surnames.txt") as f:
    for line in f:
        n = line.strip().upper()
        if n.isalpha() and 2 <= len(n) <= 8:
            last_by_len[len(n)].add(n)

print(f"  Vornamen:  { {l: len(d) for l, d in first_by_len.items()} }")
print(f"  Nachnamen: { {l: len(s) for l, s in last_by_len.items()} }")
print(f"  Geladen in {time.time()-t0:.1f}s\n")

# ── Kern: für eine (fname_len, lname_len, has_space) Kombi suchen ─────────────

def analyze_combo(fl, ll, sp):
    """
    t = fname[0..fl-1] + (' ' if sp else '') + lname[0..ll-1]
    Länge: fl + (1 if sp) + ll = 10

    Leitet ab:
      - fname_constraints: {i: j}  → fname[i] == fname[j]  (beide in fname)
      - cross_constraints: {lname_pos: fname_pos}  → lname[lp] == fname[fp]
      - lname_constraints: {lp1: lp2}  → lname[lp1] == lname[lp2]
    """
    offset = fl + (1 if sp else 0)   # wo fängt lname im t-Array an

    def t_to_source(ti):
        if ti < fl: return ('f', ti)
        if sp and ti == fl: return (' ', None)
        return ('l', ti - offset)

    fname_eq = {}    # lname_pos → fname_pos
    lname_eq = {}    # lname_pos → lname_pos (erster Auftritt der Gruppe)
    fname_self = {}  # fname_pos → fname_pos

    valid = True
    for (i, j) in CONSTRAINTS_10:
        si, sj = t_to_source(i), t_to_source(j)
        if si[0] == ' ' or sj[0] == ' ':
            continue   # Leerzeichen-Position hat keinen Buchstaben

        if si[0] == 'f' and sj[0] == 'f':
            # Beide in fname: nur gültig wenn fname selbst konsistent
            fname_self[(si[1], sj[1])] = True
        elif si[0] == 'f' and sj[0] == 'l':
            fname_eq[sj[1]] = si[1]   # lname[sj] muss == fname[si]
        elif si[0] == 'l' and sj[0] == 'f':
            fname_eq[si[1]] = sj[1]
        elif si[0] == 'l' and sj[0] == 'l':
            lname_eq[(si[1], sj[1])] = True

    return fname_self, fname_eq, lname_eq

def build_lname_index(lname_set, fname_eq_keys, lname_eq_pairs):
    """
    Baut Index: {key_tuple: [lname, ...]}
    key = (lname[pos] for pos in sorted(fname_eq_keys)) + lname-interne Constraints als Bool
    """
    idx = defaultdict(list)
    sorted_keys = sorted(fname_eq_keys)   # lname-Positionen die von fname abhängen

    for lname in lname_set:
        # Prüfe lname-interne Constraints
        ok = True
        for (p1, p2) in lname_eq_pairs:
            if p1 < len(lname) and p2 < len(lname):
                if lname[p1] != lname[p2]:
                    ok = False
                    break
            else:
                ok = False
                break
        if not ok: continue

        key = tuple(lname[p] if p < len(lname) else '?' for p in sorted_keys)
        if '?' not in key:
            idx[key].append(lname)

    return idx, sorted_keys

# ── Hauptsuche ────────────────────────────────────────────────────────────────

KNOWN_FIRST = {
    "JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD","GEORGE",
    "THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER","HAROLD","PAUL","JACK",
    "CARL","ARTHUR","ALBERT","PETER","RAYMOND","GARY","LARRY","JERRY","DENNIS",
    "GERALD","ROGER","KEITH","ALAN","MARK","BRUCE","RALPH","FRED","ERIC","NEIL",
    "DALE","DEAN","GLEN","CHAD","EARL","TROY","SEAN","RYAN","KURT","GENE",
    "LOIS","MARY","LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
    "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH","SCOTT","LARRY",
    "TERRY","BARRY","HENRY","KENNY","DANNY","RANDY","SANDY","CINDY","WENDY",
}
KNOWN_LAST = {
    "SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR",
    "JACKSON","WHITE","HARRIS","MARTIN","THOMPSON","GARCIA","CLARK","LEWIS",
    "KING","HILL","SCOTT","GREEN","ADAMS","BAKER","NELSON","CARTER","EVANS",
    "COLLINS","ROGERS","REED","COOK","MORGAN","BELL","COOPER","WARD","GRAY",
    "WOOD","ROSS","HUNT","COLE","FORD","RYAN","LONG","SHAW","WEBB","WADE",
    "RICE","LANE","NASH","MANN","CARR","SNOW","WALL","HOLT","HART","WARE",
    "HALE","WISE","RICH","REID","MACK","LOVE","PAGE","BOND","TODD","BUSH",
    "ROWE","WOLF","MOON","ROTH","NEAL","DEAN","WREN","MEAD","HALL","ROSE",
}

all_results = []

for fl in range(3, 9):
    for ll in range(2, 9):
        for sp in [False, True]:
            total = fl + (1 if sp else 0) + ll
            if total != 10: continue
            if fl not in first_by_len: continue
            if ll not in last_by_len: continue

            fname_self, fname_eq, lname_eq = analyze_combo(fl, ll, sp)
            sorted_lkeys = sorted(fname_eq.keys())
            lname_eq_pairs = list(lname_eq.keys())

            # Lname-Index bauen
            idx, lkeys = build_lname_index(last_by_len[ll], fname_eq.keys(), lname_eq_pairs)
            if not idx: continue

            # Jeden Vornamen prüfen
            for fname, fscore in first_by_len[fl].items():
                # Prüfe fname-interne Constraints
                ok = all(fname[i] == fname[j] for (i,j) in fname_self if i<fl and j<fl)
                if not ok: continue

                # Lookup-Key für Nachname aus fname ableiten
                key = tuple(fname[fname_eq[lp]] for lp in lkeys)
                matches = idx.get(key, [])

                for lname in matches:
                    if sp:
                        text = fname + ' ' + lname
                    else:
                        text = fname + lname
                    all_results.append((fscore, text, fname, lname))

# ── Ergebnisse ────────────────────────────────────────────────────────────────

all_results.sort(reverse=True)
seen = set()
unique = []
for score, text, fn, ln in all_results:
    if text not in seen:
        seen.add(text)
        unique.append((score, text, fn, ln))

print(f"=== Null-Hypothese ('0' entfernt) — Ergebnisse ===")
print(f"Reduziert: {REDUCED}  (10 Zeichen)")
print(f"Constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]")
print(f"Kandidaten: {len(unique)}\n")

print(f"{'Rang':>4}  {'Name':<25}  {'Score':>8}  Hinweis")
print("-"*65)
for i, (score, text, fn, ln) in enumerate(unique[:40], 1):
    flag = ""
    if fn in KNOWN_FIRST: flag += "★Vorname "
    if ln in KNOWN_LAST:  flag += "★Nachname"
    print(f"{i:>4}.  {text:<25}  {score:>8.5f}  {flag}")

with open("null_candidates.txt", "w") as f:
    f.write(f"# Null-Hypothese: '0'=Füller, {REDUCED}\n\n")
    for i, (score, text, fn, ln) in enumerate(unique, 1):
        f.write(f"{i:4}. {text:<25}  score={score:.5f}\n")
print(f"\n→ {len(unique)} Kandidaten in null_candidates.txt")

# ── Prime-Routen ──────────────────────────────────────────────────────────────

print(f"\n=== Prime-Routen (mod-13 Sprünge) ===")
orig_reps = dict(Counter(Z13))
for s in range(1, 13):
    route  = [(k*s) % 13 for k in range(13)]
    routed = ''.join(Z13[i] for i in route)
    reps   = {c: n for c, n in Counter(routed).items() if n > 1}
    tag    = "  ← NEUES MUSTER" if reps != {c: n for c, n in orig_reps.items() if n > 1} else ""
    print(f"  s={s:2}: {routed}  {reps}{tag}")

print(f"\nLaufzeit: {time.time()-t0:.1f}s")
