"""
M=Space Hypothese
-----------------
Der SA konvergiert konsistent auf M=Leerzeichen (56/60 Läufe hatten M→' ').

Wenn M=Leerzeichen, ergibt sich diese Struktur:

  A  E  N  z  0  K  0 [SP] 0  [  N  A [SP]
  0  1  2  3  4  5  6   7  8  9 10 11  12

  Wort1: Positionen 0-6  (7 Buchstaben)
  Wort2: Positionen 8-11 (4 Buchstaben)
  + trailing space (pos 12, ignorierbar)

CONSTRAINTS:
  Symbol A: pos 0 (Wort1[0]) = pos 11 (Wort2[3])  → Wort1[0] = Wort2[3]
  Symbol N: pos 2 (Wort1[2]) = pos 10 (Wort2[2])  → Wort1[2] = Wort2[2]
  Symbol 0: pos 4 (Wort1[4]) = pos 6 (Wort1[6]) = pos 8 (Wort2[0])
               → Wort1[4] = Wort1[6] = Wort2[0]
"""

import csv
from collections import defaultdict

Z13     = "AENz0K0M0[NAM"
SYMBOLS = list(dict.fromkeys(Z13))
PATTERN = [SYMBOLS.index(c) for c in Z13]

def load_ssa(path="ssa_names.csv", y0=1930, y1=1980):
    names = defaultdict(float)
    with open(path) as f:
        for row in csv.DictReader(f):
            if y0 <= int(row["year"]) <= y1:
                n = row["name"].upper()
                if n.isalpha():
                    names[n] += float(row["percent"])
    return names

def load_surnames(path="us_surnames.txt"):
    s = set()
    with open(path) as f:
        for line in f:
            n = line.strip().upper()
            if n.isalpha():
                s.add(n)
    return s

def search(first_names, last_names):
    """
    Sucht alle (7-Buchst. Vorname, 4-Buchst. Nachname)-Paare die
    die M=Space Constraints erfüllen.
    """
    candidates = []
    last4 = {n for n in last_names if len(n) == 4}
    first7 = {n: s for n, s in first_names.items() if len(n) == 7 and n.isalpha()}

    for fname, fscore in first7.items():
        # Constraint: Wort1[4] = Wort1[6]
        if fname[4] != fname[6]:
            continue

        # Constraint: Wort2[0] = Wort1[4]
        lname_ch0 = fname[4]
        # Constraint: Wort2[2] = Wort1[2]
        lname_ch2 = fname[2]
        # Constraint: Wort2[3] = Wort1[0]
        lname_ch3 = fname[0]

        for lname in last4:
            if lname[0] != lname_ch0: continue
            if lname[2] != lname_ch2: continue
            if lname[3] != lname_ch3: continue

            # Symbol z = Wort1[3] (einmaliges Symbol, kein Constraint)
            # Symbol K = Wort1[5] (einmaliges Symbol, kein Constraint)
            # Symbol [ = Wort2[1] (einmaliges Symbol, kein Constraint)
            # Alle 8 Symbolwerte müssen eindeutig sein:
            mapping_values = {
                fname[0],   # A
                fname[1],   # E
                fname[2],   # N
                fname[3],   # z
                fname[4],   # 0 (= Wort1[4] = Wort1[6] = Wort2[0])
                fname[5],   # K
                ' ',        # M
                lname[1],   # [
            }
            if len(mapping_values) != 8:
                continue    # Kollision → kein gültiges Substitutionsmapping

            decoded = (fname + ' ' + lname).ljust(13)[:13]
            candidates.append({
                'decoded': fname + ' ' + lname,
                'fname':   fname,
                'lname':   lname,
                'score':   fscore,
            })

    candidates.sort(key=lambda x: -x['score'])
    return candidates

# Bekannte Verdächtige (Vornamen mit 7 Buchstaben)
SUSPECT_FIRST = {
    "RICHARD", "WILLIAM", "CHARLES", "RAYMOND", "KENNETH", "DONALD ",
    "MICHAEL", "STEPHEN", "PHILLIP", "LEONARD", "GILBERT", "DOUGLAS",
    "RAYMOND", "STANLEY", "BRADLEY", "TIMOTHY", "PATRICK", "JEFFREY",
    "VINCENT", "RANDALL", "CHESTER", "SPENCER", "BERNARD", "CLIFTON",
    "CLINTON", "MAXWELL", "FREDRIC", "AURELIO", "BRENDAN",
}
SUSPECT_LAST = {
    "KANE", "ALLEN", "BEST", "GRAYSMITH", "TOSCHI",
    "HALL", "HILL", "KING", "WARD", "WOOD", "ROSS",
    "HUNT", "COLE", "WEST", "FORD", "REED", "COOK",
    "RYAN", "GRAY", "LONG", "SHAW", "WEBB", "WADE",
    "RICE", "LANE", "NASH", "WOLF", "MANN", "CARR",
}

if __name__ == "__main__":
    print("Lade Daten...")
    first = load_ssa()
    last  = load_surnames()
    print(f"  SSA-Vornamen: {len(first)}, davon 7-buchstabig: "
          f"{sum(1 for n in first if len(n)==7 and n.isalpha())}")
    print(f"  Nachnamen: {len(last)}, davon 4-buchstabig: "
          f"{sum(1 for n in last if len(n)==4)}")

    print("\nSuche M=Space Kandidaten...")
    candidates = search(first, last)
    print(f"Gefunden: {len(candidates)} Kandidaten\n")

    if not candidates:
        print("KEINE Kandidaten — Constraint zu eng für 7-Buchst.-Namen in der DB.")
        print("\nDiagnose:")
        first7 = [(n, s) for n, s in first.items() if len(n)==7 and n.isalpha()]
        print(f"  7-Buchst.-Vornamen gesamt: {len(first7)}")
        same_46 = [(n, s) for n, s in first7 if n[4]==n[6]]
        print(f"  Mit Wort1[4]=Wort1[6]:     {len(same_46)}")
        print(f"\n  Beispiele (Wort1[4]=Wort1[6]):")
        for name, _ in sorted(same_46, key=lambda x: -x[1])[:30]:
            print(f"    {name}  "
                  f"[4]={name[4]} [6]={name[6]} "
                  f"→ braucht Nachname: {name[4]}?{name[2]}{name[0]}")
    else:
        print(f"{'Rang':>4}  {'Name':<25}  {'Score':>8}  Hinweis")
        print("-" * 60)
        for i, c in enumerate(candidates[:50], 1):
            fn, ln = c['fname'], c['lname']
            flag = ""
            if fn in SUSPECT_FIRST: flag += "  ★ VERDÄCHTIG (Vorname)"
            if ln in SUSPECT_LAST:  flag += "  ★ VERDÄCHTIG (Nachname)"
            print(f"{i:>4}.  {c['decoded']:<25}  {c['score']:>8.5f}{flag}")

        print(f"\n→ Alle {len(candidates)} in m_space_candidates.txt")
        with open("m_space_candidates.txt", "w") as f:
            f.write("# M=Space Hypothese: 7-Buchst. Vorname + 4-Buchst. Nachname\n\n")
            for i, c in enumerate(candidates, 1):
                f.write(f"{i:4}. {c['decoded']:<25}  score={c['score']:.5f}\n")
