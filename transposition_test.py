"""
Transpositions-Test: Alle kompakten Routen gegen Z13 kombiniert mit Space/Null-Modell.

Für jede Transposition T:
  1. Wende T auf "AENz0K0M0[NAM" an → routed_string
  2. Wende Space-Modell (0=Space) auf routed_string an
  3. Prüfe ob die resultierenden Buchstaben-Constraints ein bekanntes Name-Muster ergeben
  4. Suche in SSA+Census-Datenbank nach bijektiven Kandidaten

Transpositions-Familien:
  A. Railfence 2-rail
  B. Railfence 3-rail
  C. Columnar: Breiten 2,3,4,5,6,7 (alle Spaltenreihenfolgen)
  D. Odd-then-even / Even-then-odd
  E. Reverse

Wichtig: Wir testen nicht "Transposition löst alles", sondern ob eine Transposition
die 0=Space-Struktur so umordnet, dass ein anderer plausibler Name entsteht.
"""

import csv, itertools, time
from collections import defaultdict

Z13 = "AENz0K0M0[NAM"
t0 = time.time()

# ── Transpositions-Funktionen ─────────────────────────────────────────────────

def railfence_encode(text, rails):
    """Liest rail-fence in Reihenfolge der Rails."""
    n = len(text)
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in text:
        fence[rail].append(ch)
        if rail == 0: direction = 1
        elif rail == rails - 1: direction = -1
        rail += direction
    return ''.join(''.join(r) for r in fence)

def railfence_decode(text, rails):
    """Rekonstruiert Originalreihenfolge aus rail-fence encoded Text."""
    n = len(text)
    pattern = []
    rail, direction = 0, 1
    for i in range(n):
        pattern.append(rail)
        if rail == 0: direction = 1
        elif rail == rails - 1: direction = -1
        rail += direction
    indices = sorted(range(n), key=lambda i: (pattern[i], i))
    result = [''] * n
    for pos, orig_idx in enumerate(indices):
        result[orig_idx] = text[pos]
    return ''.join(result)

def columnar(text, key_order):
    """Columnar-Transposition: liest Spalten in key_order-Reihenfolge."""
    n = len(text)
    ncols = len(key_order)
    nrows = (n + ncols - 1) // ncols
    grid = [[''] * ncols for _ in range(nrows)]
    idx = 0
    for r in range(nrows):
        for c in range(ncols):
            if idx < n:
                grid[r][c] = text[idx]
                idx += 1
    result = []
    for c in key_order:
        for r in range(nrows):
            if grid[r][c]:
                result.append(grid[r][c])
    return ''.join(result)

def all_permutations(ncols):
    """Alle Spaltenreihenfolgen für ncols Spalten (bis ncols=4 vollständig, sonst sample)."""
    cols = list(range(ncols))
    if ncols <= 4:
        return list(itertools.permutations(cols))
    # Für ncols>4: zu viele → nur kanonische Reihenfolgen
    return [tuple(cols), tuple(reversed(cols))]

# ── Name-Datenbank ────────────────────────────────────────────────────────────

print("Lade Daten...", end=" ", flush=True)
first4 = {}
with open("ssa_names.csv") as f:
    for row in csv.DictReader(f):
        if 1930 <= int(row["year"]) <= 1980:
            n = row["name"].upper()
            if len(n) == 4 and n.isalpha():
                first4[n] = first4.get(n, 0) + float(row["percent"])

last4 = set()
with open("us_surnames.txt") as f:
    for line in f:
        n = line.strip().upper()
        if len(n) == 4 and n.isalpha():
            last4.add(n)

# Schnell-Index für 0=Space 4+1+1+4: lname[1]=fname[2], lname[2]=fname[0]
lname_idx = defaultdict(list)
for ln in last4:
    lname_idx[(ln[1], ln[2])].append(ln)

print(f"OK ({len(first4)} Vornamen, {len(last4)} Nachnamen)")

# ── Bijektions-Check für 4+1+1+4 ─────────────────────────────────────────────

def check_4114(routed):
    """
    Prüft ob 'routed' als 0=Space-String interpretierbar ist.
    Erwartet: 13 Zeichen, routed[4]=routed[6]=routed[8] (das 0-Symbol nach Transposition).

    Gibt (fname, init2, lname, free_count) zurück oder None.
    """
    # Das Symbol das dreimal auftritt, wird als Space-Symbol behandelt
    from collections import Counter
    sym_counts = Counter(routed)
    triple_syms = [s for s, c in sym_counts.items() if c == 3]

    results = []
    for space_sym in triple_syms:
        positions = [i for i, c in enumerate(routed) if c == space_sym]
        if len(positions) != 3:
            continue
        # Für 4+1+1+4: Space muss an Positionen 4,6,8 stehen (oder nach Umbenennung)
        # Wir prüfen alle möglichen Splits die Space erzeugen
        p0, p1, p2 = sorted(positions)

        # Erwarte p0=4, p1=6, p2=8 → 0-3=fname, 5=init1, 7=init2, 9-12=lname
        if p0 != 4 or p1 != 6 or p2 != 8:
            continue

        fname = routed[0:4]
        init1_sym = routed[5]
        init2_sym = routed[7]
        lname_str = routed[9:13]

        if not (fname.isalpha() and init1_sym.isalpha() and
                init2_sym.isalpha() and lname_str.isalpha()):
            continue

        # Cross-Constraints aus dem Original-Z13 (A und N):
        # Nach Transposition können sich die Positionen verschoben haben.
        # Wir prüfen DIREKT gegen Symbole: welches Symbol sitzt an welcher Stelle?
        # Die Z13-Constraints gelten für das ORIGINAL, nicht das Transponierte.
        # Daher: Wir prüfen die Ausgabe gegen die Namens-DB (keine Symbol-Constraints).
        # Stattdessen: direkte Name-DB-Suche.

        results.append((fname, init2_sym, lname_str, init1_sym, space_sym))

    return results

# ── Alle Transpositions-Varianten ────────────────────────────────────────────

def find_names_in_transposed(routed):
    """Sucht bijektive Namen in einem transponierten Z13-String."""
    hits = []
    parts = check_4114(routed)
    if not parts:
        return hits

    for (fname, init2, lname_str, init1_sym, space_sym) in parts:
        # Prüfe ob fname ein SSA-Name ist
        if fname not in first4:
            continue
        fscore = first4[fname]

        # Prüfe ob lname_str in der Datenbank ist
        if lname_str not in last4:
            continue

        # Bijektions-Check: alle 7 bekannten Symbol-Werte verschieden
        known = {fname[0], fname[1], fname[2], fname[3], ' ', init2, lname_str[0]}
        if len(known) != 7:
            continue

        hits.append({
            'fname': fname,
            'init2': init2,
            'lname': lname_str,
            'score': fscore,
            'init1_sym': init1_sym,
            'space_sym': space_sym,
        })
    return hits

# ── Transpositions-Enumeration ────────────────────────────────────────────────

all_hits = []  # (score, description, fname, lname, transposition_desc)

# A. Identität (keine Transposition) — Baseline
hits = find_names_in_transposed(Z13)
for h in hits:
    all_hits.append((h['score'], 'IDENTITY', h['fname'], h['lname'], h['init2']))

# B. Railfence 2-rail
rf2 = railfence_encode(Z13, 2)
hits = find_names_in_transposed(rf2)
for h in hits:
    all_hits.append((h['score'], 'RAILFENCE-2', h['fname'], h['lname'], h['init2']))

# C. Railfence 3-rail
rf3 = railfence_encode(Z13, 3)
hits = find_names_in_transposed(rf3)
for h in hits:
    all_hits.append((h['score'], 'RAILFENCE-3', h['fname'], h['lname'], h['init2']))

# D. Railfence 4-rail
rf4 = railfence_encode(Z13, 4)
hits = find_names_in_transposed(rf4)
for h in hits:
    all_hits.append((h['score'], 'RAILFENCE-4', h['fname'], h['lname'], h['init2']))

# E. Odd-then-Even
odd_even = ''.join(Z13[i] for i in range(0,13,2)) + ''.join(Z13[i] for i in range(1,13,2))
hits = find_names_in_transposed(odd_even)
for h in hits:
    all_hits.append((h['score'], 'ODD-EVEN', h['fname'], h['lname'], h['init2']))

# F. Even-then-Odd
even_odd = ''.join(Z13[i] for i in range(1,13,2)) + ''.join(Z13[i] for i in range(0,13,2))
hits = find_names_in_transposed(even_odd)
for h in hits:
    all_hits.append((h['score'], 'EVEN-ODD', h['fname'], h['lname'], h['init2']))

# G. Reverse
rev = Z13[::-1]
hits = find_names_in_transposed(rev)
for h in hits:
    all_hits.append((h['score'], 'REVERSE', h['fname'], h['lname'], h['init2']))

# H. Columnar-Transpositions (ncols 2-6)
for ncols in range(2, 7):
    for perm in all_permutations(ncols):
        desc = f"COL-{ncols}-{''.join(str(p) for p in perm)}"
        try:
            col = columnar(Z13, list(perm))
            if len(col) != 13:
                continue
            hits = find_names_in_transposed(col)
            for h in hits:
                all_hits.append((h['score'], desc, h['fname'], h['lname'], h['init2']))
        except Exception:
            pass

# ── Ausgabe ───────────────────────────────────────────────────────────────────

all_hits.sort(reverse=True)
seen = set()
unique = []
for score, desc, fn, ln, init2 in all_hits:
    key = (fn, ln, desc)
    if key not in seen:
        seen.add(key)
        unique.append((score, desc, fn, ln, init2))

print(f"\n{'='*70}")
print(f"TRANSPOSITIONS-TEST: {len(unique)} bijektive Kandidaten gesamt")
print(f"{'='*70}\n")

if not unique:
    print("Kein einziger bijektiver Kandidat in transponierten Strings.")
    print("→ Transposition + 0=Space ergibt keinen bekannten Namen.")
else:
    print(f"{'Rang':>4}  {'Transposition':<15}  {'Name':<25}  {'Score':>8}")
    print("-"*65)
    for i, (score, desc, fn, ln, init2) in enumerate(unique[:30], 1):
        print(f"{i:>4}.  {desc:<15}  {fn} *. {init2}. {ln:<12}  {score:>8.5f}")

# Zähle Treffer pro Transposition
from collections import Counter
by_trans = Counter(desc for _, desc, _, _, _ in unique)
print(f"\nTreffer pro Transposition:")
for desc, cnt in sorted(by_trans.items(), key=lambda x: -x[1]):
    print(f"  {desc:<20} {cnt:>4} Kandidaten")

print(f"\nLaufzeit: {time.time()-t0:.1f}s")

with open("transposition_candidates.txt", "w") as f:
    f.write("# Transpositions-Test: Z13 + 0=Space-Modell\n\n")
    for i, (score, desc, fn, ln, init2) in enumerate(unique, 1):
        f.write(f"{i:5}. [{desc:<15}] {fn} *. {init2}. {ln}  score={score:.5f}\n")
print(f"→ transposition_candidates.txt geschrieben")
