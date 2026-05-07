"""
Umfassende Z13-Suche:
- Probiert ALLE 8 möglichen Symbole als Leerzeichen-Kandidaten
- Probiert auch No-Space (0=Buchstabe, alle 13 Zeichen sind Buchstaben)
- Für jede Struktur: Lookup-Index für O(n) statt O(n²)

Z13 = "AENz0K0M0[NAM"
Symbole: A(0,11), E(1), N(2,10), z(3), 0(4,6,8), K(5), M(7,12), [(9)

Constraints (erzwungen durch Symbolwiederholung):
  text[0]  = text[11]  (Symbol A)
  text[2]  = text[10]  (Symbol N)
  text[4]  = text[6] = text[8]  (Symbol 0)
  text[7]  = text[12]  (Symbol M)
"""

import csv, time
from collections import defaultdict

Z13 = "AENz0K0M0[NAM"
SYMS = ['A', 'E', 'N', 'z', '0', 'K', 'M', '[']  # 8 eindeutige Symbole
# Positionen pro Symbol:
SYM_POS = {'A': [0,11], 'E': [1], 'N': [2,10], 'z': [3],
           '0': [4,6,8], 'K': [5], 'M': [7,12], '[': [9]}

t0 = time.time()

# ── Daten laden ───────────────────────────────────────────────────────────────
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
print(f"  Vornamen:  { {l: len(d) for l, d in sorted(first_by_len.items())} }")
print(f"  Nachnamen: { {l: len(s) for l, s in sorted(last_by_len.items())} }")

# ── Kern-Constraint-Prüfung ───────────────────────────────────────────────────

def check_text(text):
    """
    Prüft ob ein 13-Zeichen-Text die Z13-Constraints erfüllt
    UND alle 8 Symbole auf eindeutige Werte abbildet.
    """
    if len(text) != 13:
        return False
    # Constraint-Checks
    if text[0] != text[11]: return False
    if text[2] != text[10]: return False
    if not (text[4] == text[6] == text[8]): return False
    if text[7] != text[12]: return False
    # Eindeutigkeits-Check: 8 verschiedene Zeichen für die 8 Symbole
    vals = {text[0], text[1], text[2], text[3], text[4], text[5], text[7], text[9]}
    return len(vals) == 8

# ── Ansatz A: Bestimmtes Symbol = Leerzeichen ─────────────────────────────────

def search_space_sym(space_sym):
    """
    Probiert space_sym = Leerzeichen.
    Alle anderen Symbole → Buchstaben A-Z (eindeutig).

    Baut Text: space_sym-Positionen werden zu ' ', rest zu Buchstaben.
    Ergibt Wörter, die dann gegen Datenbank geprüft werden.
    """
    space_positions = SYM_POS[space_sym]  # z.B. [4,6,8] für '0'

    # Text-Positionen nach Wort aufteilen
    words_positions = []
    current_word = []
    for i, c in enumerate(Z13):
        if c == space_sym:
            if current_word:
                words_positions.append(current_word)
                current_word = []
        else:
            current_word.append(i)
    if current_word:
        words_positions.append(current_word)

    # Filtern: nur Wörter mit 2+ Zeichen (Einzelbuchstaben als Initialen behalten)
    word_lens = [len(w) for w in words_positions]

    # Wir suchen nach VORNAME + NACHNAME aus unseren Datenbanken
    # Für jede Wort-Kombination, die ersten 2 Wörter = Vorname, letztes = Nachname
    # (oder erstes = Vorname, letztes = Nachname, Mittelwörter = Initialen)

    results = []
    n_words = len(words_positions)

    if n_words < 2:
        return results

    # Strategie: Erstes Wort = Vorname, letztes Wort = Nachname
    fname_positions = words_positions[0]
    lname_positions = words_positions[-1]
    middle_positions = words_positions[1:-1]  # Initialen

    fl = len(fname_positions)
    ll = len(lname_positions)

    if fl not in first_by_len or ll not in last_by_len:
        return results

    # Abgeleitete Constraints:
    # Welche Positionen in fname müssen welchen Positionen in lname entsprechen?

    # Constraint A: pos[0]=pos[11] → fname_positions[?] vs lname_positions[?]
    # Constraint N: pos[2]=pos[10] → ...
    # Constraint 0: pos[4]=pos[6]=pos[8] → je nach space_sym
    # Constraint M: pos[7]=pos[12] → ...

    PAIRS = [(0,11), (2,10), (4,6), (4,8), (7,12)]

    fname_set = set(fname_positions)
    lname_set = set(lname_positions)

    cross = {}   # lname_local → fname_local
    lname_int = {}  # lname_local → lname_local
    fname_int = {}  # fname_local → fname_local
    valid = True

    for (pi, pj) in PAIRS:
        # Welche Symbole stecken an diesen Positionen?
        si = Z13[pi]; sj = Z13[pj]
        if si == space_sym or sj == space_sym:
            continue  # beide sind space → kein Buchstaben-Constraint

        # Position im fname/lname
        if pi in fname_set and pj in fname_set:
            li = fname_positions.index(pi)
            lj = fname_positions.index(pj)
            fname_int[(li, lj)] = True
        elif pi in fname_set and pj in lname_set:
            li = fname_positions.index(pi)
            lj = lname_positions.index(pj)
            if lj in cross and cross[lj] != li:
                valid = False; break
            cross[lj] = li
        elif pi in lname_set and pj in fname_set:
            li = lname_positions.index(pi)
            lj = fname_positions.index(pj)
            if li in cross and cross[li] != lj:
                valid = False; break
            cross[li] = lj
        elif pi in lname_set and pj in lname_set:
            li = lname_positions.index(pi)
            lj = lname_positions.index(pj)
            lname_int[(li, lj)] = True

    if not valid:
        return results

    # Lname-Index nach Cross-Constraint-Zeichen
    sorted_lkeys = sorted(cross.keys())
    idx = defaultdict(list)
    lname_int_pairs = list(lname_int.keys())

    for lname in last_by_len[ll]:
        ok = all(
            lp1 < ll and lp2 < ll and lname[lp1] == lname[lp2]
            for (lp1, lp2) in lname_int_pairs
        )
        if not ok: continue
        key = tuple(lname[lp] for lp in sorted_lkeys)
        idx[key].append(lname)

    # Jeden Vornamen prüfen
    for fname, fscore in first_by_len[fl].items():
        ok = all(fname[fi] == fname[fj] for (fi, fj) in fname_int if fi < fl and fj < fl)
        if not ok: continue

        key = tuple(fname[cross[lp]] for lp in sorted_lkeys)

        for lname in idx.get(key, []):
            # Text bauen und komplett prüfen
            text = ['?'] * 13
            for k, pos in enumerate(fname_positions):
                text[pos] = fname[k]
            for k, pos in enumerate(lname_positions):
                text[pos] = lname[k]
            for pos in space_positions:
                text[pos] = ' '
            for word_pos in middle_positions:
                for pos in word_pos:
                    text[pos] = '?'  # Initialen: beliebig

            text = ''.join(text)

            # Eindeutigkeits-Check (ohne Initialen, die noch '?' sind)
            used = set(c for c in text if c not in (' ', '?'))
            if len(used) != len(fname_positions) + len(lname_positions):
                # Buchstaben-Kollision zwischen fname und lname
                continue

            # Initialen müssen eindeutige Buchstaben sein (nicht in used)
            # (wir notieren sie als *)
            label = ''
            parts = [fname]
            for midw in middle_positions:
                parts.append('*')  # Platzhalter für Initial
            parts.append(lname)

            display = ' '.join(parts)
            results.append((fscore, display, fname, lname, space_sym))

    return results

# ── Ansatz B: Kein Leerzeichen (alle 13 Zeichen = Buchstaben) ────────────────

def search_no_space():
    """
    Kein Symbol ist Leerzeichen → alle 13 Positionen sind Buchstaben.
    Sucht (Vorname+Nachname) die direkt aneinandergereiht die Z13-Constraints erfüllen.
    """
    results = []

    # Alle möglichen Längenpaare die zusammen 13 ergeben
    for fl in range(3, 11):
        ll = 13 - fl
        if ll < 2 or ll > 11: continue
        if fl not in first_by_len: continue
        if ll not in last_by_len: continue

        # Constraints für Text = fname + lname (keine Leerzeichen)
        # text[0..fl-1] = fname, text[fl..12] = lname
        # lname_start = fl
        def lname_pos(tp): return tp - fl  # Texposition → lname-Index

        PAIRS = [(0,11), (2,10), (4,6), (4,8), (7,12)]

        cross = {}       # lname_idx → fname_idx
        lname_int = {}   # (lname_idx, lname_idx)
        fname_int = {}   # (fname_idx, fname_idx)
        skip = False

        for (pi, pj) in PAIRS:
            in_f_i = pi < fl
            in_f_j = pj < fl

            if in_f_i and in_f_j:
                fname_int[(pi, pj)] = True
            elif in_f_i and not in_f_j:
                lj = lname_pos(pj)
                if lj < ll:
                    if lj in cross and cross[lj] != pi:
                        skip = True; break
                    cross[lj] = pi
            elif not in_f_i and in_f_j:
                li = lname_pos(pi)
                if li >= 0 and pj < fl:
                    if li in cross and cross[li] != pj:
                        skip = True; break
                    cross[li] = pj
            else:
                li = lname_pos(pi)
                lj = lname_pos(pj)
                if 0 <= li < ll and 0 <= lj < ll:
                    lname_int[(li, lj)] = True

        if skip: continue

        sorted_lkeys = sorted(cross.keys())
        lname_int_pairs = list(lname_int.keys())
        fname_int_pairs = list(fname_int.keys())

        idx = defaultdict(list)
        for lname in last_by_len[ll]:
            ok = all(
                lp1 < ll and lp2 < ll and lname[lp1] == lname[lp2]
                for (lp1, lp2) in lname_int_pairs
            )
            if not ok: continue
            key = tuple(lname[lp] for lp in sorted_lkeys if lp < ll)
            idx[key].append(lname)

        for fname, fscore in first_by_len[fl].items():
            ok = all(fname[fi] == fname[fj] for (fi, fj) in fname_int_pairs if fi < fl and fj < fl)
            if not ok: continue

            key = tuple(fname[cross[lp]] for lp in sorted_lkeys if lp < ll)

            for lname in idx.get(key, []):
                text = fname + lname
                # Eindeutigkeits-Check
                vals = {text[0], text[1], text[2], text[3], text[4], text[5], text[7], text[9]}
                if len(vals) == 8:
                    results.append((fscore, fname + ' ' + lname, fname, lname, 'none'))

    return results

# ── Hauptsuche ────────────────────────────────────────────────────────────────

all_results = []

print("\n=== Suche für alle Leerzeichen-Hypothesen ===")
for sym in ['A', 'E', 'N', 'z', '0', 'K', 'M', '[']:
    r = search_space_sym(sym)
    print(f"  Symbol '{sym}' = Leerzeichen: {len(r)} Kandidaten")
    all_results.extend(r)

print("\n=== No-Space Suche (alle 13 = Buchstaben) ===")
r_ns = search_no_space()
print(f"  No-Space: {len(r_ns)} Kandidaten")
all_results.extend(r_ns)

# ── Ergebnisse ausgeben ───────────────────────────────────────────────────────

all_results.sort(reverse=True)
seen = set()
unique = []
for score, text, fn, ln, sym in all_results:
    key = (fn, ln, sym)
    if key not in seen:
        seen.add(key)
        unique.append((score, text, fn, ln, sym))

print(f"\n=== Zusammenfassung ===")
print(f"Gesamt eindeutige Kandidaten: {len(unique)}")
print()

# Nach Hypothese gruppieren
from collections import Counter
by_sym = Counter(sym for _, _, _, _, sym in unique)
for sym, cnt in sorted(by_sym.items()):
    label = f"'{sym}'" if sym != 'none' else 'No-Space'
    print(f"  {label:12} = Leerzeichen: {cnt:6} Kandidaten")

print()
print(f"{'Rang':>4}  {'Name':<30}  {'Hyp':>5}  {'Score':>8}")
print("-"*60)

KNOWN_FIRST = {"JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD",
               "GEORGE","THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER",
               "HAROLD","PAUL","JACK","CARL","ARTHUR","ALBERT","PETER","RAYMOND",
               "GARY","LARRY","JERRY","DENNIS","GERALD","ROGER","KEITH","ALAN",
               "MARK","BRUCE","RALPH","FRED","ERIC","NEIL","DALE","DEAN","GLEN",
               "CHAD","EARL","TROY","SEAN","RYAN","KURT","GENE","LOIS","MARY",
               "LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
               "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH","SCOTT",
               "JAMES","LARRY","TERRY","BARRY","PERRY","HENRY","KENNY","BENNY",
               "DANNY","RANDY","SANDY","CANDY","MANDY","CINDY","MINDY","WENDY"}

shown = 0
for score, text, fn, ln, sym in unique[:100]:
    flag = ""
    fname_only = fn.split()[0] if ' ' in fn else fn
    if fname_only in KNOWN_FIRST: flag += "★ "
    label = sym if sym != 'none' else 'NS'
    print(f"{shown+1:>4}.  {text:<30}  {label:>5}  {score:>8.5f}  {flag}")
    shown += 1

# Speichern
with open("comprehensive_candidates.txt", "w") as f:
    f.write("# Umfassende Z13-Suche — alle Leerzeichen-Hypothesen\n")
    f.write(f"# Gesamt: {len(unique)} Kandidaten\n\n")
    for i, (score, text, fn, ln, sym) in enumerate(unique, 1):
        label = f"sep={sym}" if sym != 'none' else "no-space"
        f.write(f"{i:5}. {text:<30}  {label}  score={score:.5f}\n")

print(f"\n→ {len(unique)} Kandidaten in comprehensive_candidates.txt")
print(f"Laufzeit: {time.time()-t0:.1f}s")
