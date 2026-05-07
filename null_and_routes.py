"""
Ansatz 1: Symbol '0' als Null/Füller entfernen
Ansatz 2: Prime-Routen-Transposition (13 ist prim)

Nach Entfernen der drei '0' an Positionen 4,6,8:
  Original: A E N z [0] K [0] M [0] [ N A M
  Reduziert: A E N z K M [ N A M   (10 Zeichen)

Neue Constraints:
  A: Pos 0 und 8  → p[0]=p[8]
  N: Pos 2 und 7  → p[2]=p[7]
  M: Pos 5 und 9  → p[5]=p[9]
  E, z, K, [: je einmalig

7 eindeutige Symbole, 10 Zeichen — viel lösbarer!
"""

import csv, math, random, string, time
from collections import defaultdict

Z13     = "AENz0K0M0[NAM"
SYMBOLS_FULL = list(dict.fromkeys(Z13))
ALPHA   = string.ascii_uppercase + ' '

# ── Ansatz 1: Null-Entfernung ─────────────────────────────────────────────────

NULL_SYM  = '0'   # das häufigste Symbol als Null-Kandidat
REDUCED   = ''.join(c for c in Z13 if c != NULL_SYM)  # "AENzKM[NAM"
SYMS_R    = list(dict.fromkeys(REDUCED))
PATTERN_R = [SYMS_R.index(c) for c in REDUCED]

print(f"Original  Z13: {Z13}  ({len(Z13)} Zeichen, {len(SYMBOLS_FULL)} Symbole)")
print(f"Reduziert    : {REDUCED}  ({len(REDUCED)} Zeichen, {len(SYMS_R)} Symbole)")
print(f"Muster       : {PATTERN_R}")
print()

# Constraints im reduzierten String
from collections import Counter
freq_r = Counter(REDUCED)
print("Constraints nach Null-Entfernung:")
for sym, cnt in freq_r.items():
    if cnt > 1:
        pos = [i for i, c in enumerate(REDUCED) if c == sym]
        print(f"  '{sym}': Positionen {pos} → gleicher Buchstabe")
print()

# ── Namen-Datenbank laden ─────────────────────────────────────────────────────

def load_first(path="ssa_names.csv", y0=1930, y1=1980):
    names = defaultdict(float)
    with open(path) as f:
        for row in csv.DictReader(f):
            if y0 <= int(row["year"]) <= y1:
                n = row["name"].upper()
                if n.isalpha():
                    names[n] += float(row["percent"])
    return names

def load_last(path="us_surnames.txt"):
    s = set()
    with open(path) as f:
        for line in f:
            n = line.strip().upper()
            if n.isalpha(): s.add(n)
    return s

print("Lade Namen...")
FIRST = load_first()
LAST  = load_last()
print(f"  {len(FIRST)} Vornamen, {len(LAST)} Nachnamen\n")

# ── Ansatz 1a: Direkte Constraint-Suche im reduzierten String ─────────────────

def search_reduced():
    """
    Reduzierter String: A E N z K M [ N A M  (Muster: a b c d f g h c a g)
    Constraints:
      p[0]=p[8]  (Symbol A)
      p[2]=p[7]  (Symbol N)
      p[5]=p[9]  (Symbol M)

    Mögliche Strukturen für 10 Zeichen:
      5+5:  XXXXX XXXXX  (Vorname 5, Nachname 5)
      4+6:  XXXX XXXXXX
      6+4:  XXXXXX XXXX
      3+7:  XXX XXXXXXX
      10:   XXXXXXXXXX   (ein Wort)
      4+1+5, 5+1+4, etc. (mit Initial)
    """
    print("=== Ansatz 1: Null-Entfernung — Constraint-Suche ===")
    print(f"Reduziert: {REDUCED}")
    print(f"Constraints: p[0]=p[8], p[2]=p[7], p[5]=p[9]\n")

    candidates = []

    # Alle Vor+Nachname Kombinationen (5+5, 4+6, 6+4, 5+4 mit space, etc.)
    # Wir probieren alle Splits: word1 der Länge 2-8, word2 der Länge 2-8
    # Gesamtlänge = 10 (inkl. kein Leerzeichen) oder mit einem Leerzeichen

    def check_name(text):
        """Prüft ob text die 10-Zeichen Constraints erfüllt."""
        if len(text) != 10:
            return False
        t = text.replace(' ', '')  # für Buchstaben-Check
        # p[0]=p[8]: text[0] == text[8]
        if text[0] != text[8]: return False
        # p[2]=p[7]: text[2] == text[7]
        if text[2] != text[7]: return False
        # p[5]=p[9]: text[5] == text[9]
        if text[5] != text[9]: return False
        return True

    # Alle Vornamen 4-6 Buchstaben
    for fname, fscore in FIRST.items():
        if not (3 <= len(fname) <= 7): continue

        for lname in LAST:
            if not (3 <= len(lname) <= 7): continue

            # Kein Leerzeichen: fname direkt an lname
            combined = fname + lname
            if len(combined) == 10 and check_name(combined):
                candidates.append({
                    'text': fname + ' ' + lname,
                    'raw': combined,
                    'score': fscore,
                    'type': f'{len(fname)}+{len(lname)}'
                })

            # Mit Leerzeichen: fname + ' ' + lname = 10 Zeichen (fname+lname=9)
            combined_sp = fname + ' ' + lname
            if len(combined_sp) == 10 and check_name(combined_sp):
                candidates.append({
                    'text': combined_sp,
                    'raw': combined_sp,
                    'score': fscore,
                    'type': f'{len(fname)}+sp+{len(lname)}'
                })

    candidates.sort(key=lambda x: -x['score'])

    # Deduplizieren
    seen = set()
    unique = []
    for c in candidates:
        if c['raw'] not in seen:
            seen.add(c['raw'])
            unique.append(c)

    print(f"Gefunden: {len(unique)} Kandidaten\n")

    known_first = {"JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES",
                   "DONALD","GEORGE","THOMAS","JOSEPH","EDWARD","HENRY",
                   "FRANK","WALTER","HAROLD","PAUL","JACK","CARL","ARTHUR",
                   "ALBERT","PETER","RAYMOND","GARY","LARRY","JERRY","DENNIS",
                   "GERALD","ROGER","KEITH","ALAN","MARK","BRUCE","RALPH",
                   "FRED","ERIC","NEIL","DALE","DEAN","GLEN","CHAD","EARL",
                   "TROY","SEAN","RYAN","KURT","GENE","LOIS","MARY","LINDA",
                   "BARBARA","PATRICIA","CAROL","SANDRA","HELEN","BETTY",
                   "RUTH","JEAN","ALICE","JOAN","JANE","ANNE","LISA","LEAH"}
    known_last  = {"SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE",
                   "TAYLOR","JACKSON","WHITE","HARRIS","MARTIN","THOMPSON",
                   "GARCIA","ROBINSON","CLARK","LEWIS","KING","WRIGHT","HILL",
                   "SCOTT","GREEN","ADAMS","BAKER","NELSON","CARTER","MITCHELL",
                   "TURNER","PHILLIPS","CAMPBELL","PARKER","EVANS","EDWARDS",
                   "COLLINS","STEWART","SANCHEZ","MORRIS","ROGERS","REED",
                   "COOK","MORGAN","BELL","MURPHY","BAILEY","RIVERA","COOPER",
                   "WARD","COX","FOSTER","GRAY","WOOD","ROSS","HUNT","COLE",
                   "WEST","FORD","RYAN","LONG","SHAW","WEBB","WADE","BOYD",
                   "RICE","LANE","NASH","MANN","CARR","SNOW","WALL","HOLT",
                   "HART","WARE","ROTH","NEAL","HALE","WISE","RICH","REID"}

    print(f"{'Rang':>4}  {'Name':<22}  {'Typ':<10}  {'Score':>8}  Hinweis")
    print("-"*65)
    for i, c in enumerate(unique[:40], 1):
        parts = c['text'].split()
        flag = ""
        if parts[0] in known_first: flag += "★Vorname "
        if parts[-1] in known_last:  flag += "★Nachname"
        print(f"{i:>4}.  {c['text']:<22}  {c['type']:<10}  "
              f"{c['score']:>8.5f}  {flag}")

    with open("null_candidates.txt", "w") as f:
        f.write(f"# Null-Hypothese: '0' entfernt, 10-Zeichen-Muster '{REDUCED}'\n")
        f.write(f"# Constraints: p[0]=p[8], p[2]=p[7], p[5]=p[9]\n\n")
        for i, c in enumerate(unique, 1):
            f.write(f"{i:4}. {c['text']:<22}  type={c['type']}  score={c['score']:.5f}\n")
    print(f"\n→ {len(unique)} Kandidaten in null_candidates.txt")

    return unique

# ── Ansatz 2: Prime-Routen (mod-13 Sprünge) ──────────────────────────────────

def search_prime_routes():
    """
    Da 13 prim ist, gibt es für jeden Schrittweite s (1..12) genau eine
    Permutation die alle 13 Positionen durchläuft.
    s=1 ist trivial (Identität). Teste s=2..12.
    """
    print("\n=== Ansatz 2: Prime-Routen (mod-13) ===")
    print("Für jede Schrittweite s: lies Z13 an Positionen 0, s, 2s, ... mod 13\n")

    results = []
    for s in range(1, 13):
        route = [(k * s) % 13 for k in range(13)]
        routed = ''.join(Z13[i] for i in route)
        syms   = list(dict.fromkeys(routed))
        pat    = [syms.index(c) for c in routed]
        freq   = Counter(routed)
        repeats = {c: cnt for c, cnt in freq.items() if cnt > 1}

        print(f"  s={s:2}: {routed}  Wiederholungen: {repeats}  Muster: {pat}")
        results.append((s, routed, pat, repeats))

    print()
    print("Interessante Routen (veränderte Wiederholungsmuster):")
    original_repeats = {'A':2,'N':2,'0':3,'M':2}
    for s, routed, pat, repeats in results:
        if repeats != original_repeats:
            print(f"  s={s}: {routed}  ANDERES MUSTER: {repeats}")

    return results

# ── Kombiniert: Routen + Null-Entfernung ─────────────────────────────────────

def search_routes_with_nulls(routes):
    """
    Für jede Prime-Route: entferne das häufigste Symbol und
    prüfe ob der reduzierte String Namens-Constraints erfüllt.
    """
    print("\n=== Kombiniert: Routen + Null-Entfernung ===")

    all_candidates = []
    for s, routed, pat, repeats in routes:
        if not repeats: continue
        # Häufigstes Symbol als Null-Kandidat
        null_sym = max(repeats, key=repeats.get)
        reduced = ''.join(c for c in routed if c != null_sym)
        if len(reduced) < 8: continue

        # Constraints im reduzierten String
        freq_red = Counter(reduced)
        constraints = {sym: [i for i,c in enumerate(reduced) if c==sym]
                       for sym, cnt in freq_red.items() if cnt > 1}

        # Suche direkt: prüfe ob Top-Vornamen passen
        matches = []
        for fname, fscore in FIRST.items():
            for lname in LAST:
                combined = fname + lname
                if len(combined) != len(reduced): continue
                ok = all(
                    all(combined[p] == combined[positions[0]] for p in positions)
                    for sym, positions in constraints.items()
                )
                if ok:
                    matches.append((fscore, fname + ' ' + lname))

        if matches:
            matches.sort(reverse=True)
            print(f"\n  Route s={s}, Null='{null_sym}', Reduziert='{reduced}':")
            for score, name in matches[:5]:
                print(f"    '{name}'  score={score:.5f}")
            all_candidates.extend(matches[:10])

    if not all_candidates:
        print("  Keine Treffer bei kombinierten Routen+Nulls.")

    return all_candidates


if __name__ == "__main__":
    t0 = time.time()

    # Ansatz 1
    null_cands = search_reduced()

    # Ansatz 2
    routes = search_prime_routes()

    # Kombiniert
    search_routes_with_nulls(routes)

    print(f"\nGesamtlaufzeit: {time.time()-t0:.1f}s")
