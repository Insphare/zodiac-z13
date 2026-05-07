"""
Filtert Z13-Kandidaten gegen echte US-Namen (1940-1975).

Separator-Hypothese: '0' = Leerzeichen
Struktur: VORNAME INITIAL1 INITIAL2 NACHNAME
Pattern:  A  E  N  z  _  K  _  M  _  [  N  A  M
Position: 0  1  2  3  4  5  6  7  8  9 10 11 12

Constraints (Symbol → gleicher Buchstabe):
  p[0] == p[11]  (Symbol A: Vorname[0] == Nachname[2])
  p[2] == p[10]  (Symbol N: Vorname[2] == Nachname[1])
  p[7] == p[12]  (Symbol M: Initial2   == Nachname[3])
"""

import csv
from collections import defaultdict

# --- Vornamen aus SSA-Daten laden (1940-1975) ---

def load_first_names(path="ssa_names.csv", years=(1935, 1975), min_percent=0.0005):
    """Lädt populäre Vornamen aus dem gewünschten Zeitraum."""
    names_m = defaultdict(float)
    names_f = defaultdict(float)

    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row['year'])
            if not (years[0] <= year <= years[1]):
                continue
            pct = float(row['percent'])
            name = row['name'].upper()
            sex = row['sex']
            if sex == 'boy':
                names_m[name] += pct
            else:
                names_f[name] += pct

    # Nur 4-Buchstaben-Namen
    result_m = {n: p for n, p in names_m.items() if len(n) == 4 and n.isalpha()}
    result_f = {n: p for n, p in names_f.items() if len(n) == 4 and n.isalpha()}
    return result_m, result_f


def load_last_names(path="us_surnames.txt"):
    """Lädt US-Nachnamen."""
    names = set()
    with open(path) as f:
        for line in f:
            name = line.strip().upper()
            if len(name) == 4 and name.isalpha():
                names.add(name)
    return names


# --- Constraint-Solver ---

def find_candidates(first_names_m, first_names_f, last_names):
    """
    Findet alle (Vorname, Nachname)-Paare die die Z13-Constraints erfüllen.
    """
    candidates = []

    all_first = dict(first_names_m)
    for n, p in first_names_f.items():
        all_first[n] = all_first.get(n, 0) + p

    for fname, fname_score in all_first.items():
        # Constraint 1: Vorname[0] == Nachname[2]
        lname_ch2 = fname[0]
        # Constraint 2: Vorname[2] == Nachname[1]
        lname_ch1 = fname[2]

        for lname in last_names:
            if lname[1] != lname_ch1:
                continue
            if lname[2] != lname_ch2:
                continue

            # Constraint 3: Initial2 == Nachname[3]
            initial2 = lname[3]

            # Prüfe: alle 8 Symbole auf VERSCHIEDENE Buchstaben?
            # Symbole: A→fname[0], E→fname[1], N→fname[2], z→fname[3],
            #          0→' ', K→initial1, M→initial2, [→lname[0]
            fixed = {
                fname[0],   # Symbol A
                fname[1],   # Symbol E
                fname[2],   # Symbol N
                fname[3],   # Symbol z
                ' ',        # Symbol 0
                initial2,   # Symbol M
                lname[0],   # Symbol [
            }
            # Initial1 (Symbol K) kann alles sein, was noch nicht vergeben ist
            available_initials = [
                c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                if c not in fixed
            ]

            for initial1 in available_initials:
                # Score: Vorname-Häufigkeit als Proxy
                candidates.append({
                    'decoded': f"{fname} {initial1} {initial2} {lname}",
                    'fname': fname,
                    'initial1': initial1,
                    'initial2': initial2,
                    'lname': lname,
                    'fname_score': fname_score,
                    'lname_in_db': lname in last_names,
                })

    return candidates


def main():
    print("Lade SSA-Vornamen (1935-1975)...")
    first_m, first_f = load_first_names()
    print(f"  Männlich (4 Buchst.): {len(first_m)}")
    print(f"  Weiblich (4 Buchst.): {len(first_f)}")

    print("Lade US-Nachnamen...")
    last_names = load_last_names()
    print(f"  Nachnamen (4 Buchst.): {len(last_names)}")

    print("\nBerechne Kandidaten...")
    candidates = find_candidates(first_m, first_f, last_names)
    print(f"Kandidaten gesamt: {len(candidates)}")

    # Nach Vorname-Häufigkeit sortieren
    candidates.sort(key=lambda x: -x['fname_score'])

    # Unique Vorname+Nachname-Paare
    seen = set()
    unique = []
    for c in candidates:
        key = (c['fname'], c['lname'])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    print(f"Eindeutige Vor+Nachname-Paare: {len(unique)}")

    print("\n=== Top-Kandidaten (nach Vorname-Häufigkeit) ===")
    print(f"{'Vorname':<8} {'I1':>3} {'I2':>3} {'Nachname':<8}  Decoded")
    print("-" * 55)
    for c in unique[:50]:
        print(f"{c['fname']:<8} {c['initial1']:>3} {c['initial2']:>3} "
              f"{c['lname']:<8}  → {c['decoded']}")

    # Speichern
    with open("candidates_filtered.txt", "w") as f:
        f.write("# Z13 Kandidaten (Separator-Hypothese, SSA-gefiltert)\n")
        f.write("# Format: VORNAME INITIAL1 INITIAL2 NACHNAME\n")
        f.write("# Sortiert nach Vorname-Häufigkeit (1935-1975)\n\n")
        for c in unique:
            f.write(f"{c['decoded']:<25}  score={c['fname_score']:.6f}\n")

    print(f"\n→ Alle {len(unique)} Paare gespeichert in candidates_filtered.txt")


if __name__ == '__main__':
    main()
