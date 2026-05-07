"""
K-Symbol Einschränkung: Welcher Buchstabe ist die erste Initial in NEIL [X]. G. KING?

K kommt in Z13 genau 1× vor (Position 5).
Bereits vergebene Buchstaben: {N, E, I, L, ' ', G, K}
Mögliche Werte für K-Symbol: alle anderen Buchstaben des Alphabets.

Methode: SSA-Vornamen 1930–1950 (männlich) als Proxy für mittlere Initialen.
Historisch sind mittlere Namen oft populäre Vornamen derselben Generation.
"""

import csv
from collections import defaultdict

# Bereits vergebene Buchstaben (dürfen nicht nochmal vorkommen)
FORBIDDEN = {'N', 'E', 'I', 'L', 'G', 'K'}

print("=" * 60)
print("K-SYMBOL ANALYSE: Erste Initial in NEIL [X]. G. KING")
print("=" * 60)
print(f"\nVerbotene Buchstaben (bereits vergeben): {sorted(FORBIDDEN)}")

# SSA-Daten laden: männliche Vornamen 1930–1950
initial_freq = defaultdict(float)

with open("ssa_names.csv") as f:
    for row in csv.DictReader(f):
        year = int(row["year"])
        if 1925 <= year <= 1955:  # Geburtsjahre des Täters
            name = row["name"].upper()
            gender = row.get("gender", row.get("sex", "M"))
            if gender.upper() in ("M", "MALE", "BOY"):
                initial = name[0]
                if initial not in FORBIDDEN:
                    initial_freq[initial] += float(row["percent"])

# Sortieren nach Häufigkeit
ranked = sorted(initial_freq.items(), key=lambda x: -x[1])

print(f"\nHäufigkeit männlicher Vornamen nach Anfangsbuchstabe (1925–1955):")
print(f"{'─'*50}")
print(f"{'Rang':<6} {'Initial':<10} {'Gewicht':<12} {'Ring'}")
print(f"{'─'*50}")

total = sum(v for _, v in ranked)
cumulative = 0

for rank, (initial, freq) in enumerate(ranked, 1):
    pct = freq / total * 100
    cumulative += pct
    if rank <= 5:
        ring = "Ring 1 ★"
    elif rank <= 8:
        ring = "Ring 2"
    else:
        ring = "Ring 3"
    print(f"{rank:<6} {initial:<10} {pct:>6.2f}%      {ring}")

print(f"{'─'*50}")
print(f"\nTop 5 (Ring 1): {[i for i, _ in ranked[:5]]}")
print(f"Top 8 (Ring 2): {[i for i, _ in ranked[:8]]}")

# Vollständige Kandidatenliste für NEIL [X]. G. KING
print(f"\n{'='*60}")
print("VOLLSTÄNDIGE KANDIDATENLISTE: NEIL [X]. G. KING")
print(f"{'='*60}")

# Nachnamen-DB laden
last4 = set()
with open("us_surnames.txt") as f:
    for line in f:
        n = line.strip().upper()
        if len(n) == 4 and n.isalpha():
            last4.add(n)

# KING ist unser Kandidat — bereits bestätigt
# Aber: wie viele andere 4-Buchst.-Nachnamen passen zu NEIL [X]. G. KING?
# Constraint: Nachname muss I_G-Muster haben (pos 1=I, pos 3=G) — wait, das ist schon KING

# Eigentlich: die Namensstruktur ist fix (NEIL + ? + G + KING)
# Was wir tun: für jeden möglichen X, zeige den vollständigen Namen

print(f"\nAlle möglichen vollständigen Namen (KING als Nachname):")
print(f"{'─'*40}")
for rank, (initial, freq) in enumerate(ranked, 1):
    pct = freq / total * 100
    ring = "★" if rank <= 5 else ("○" if rank <= 8 else "·")
    print(f"  {ring} NEIL {initial}. G. KING  ({pct:.1f}%)")

print(f"\n{'='*60}")
print("EMPFEHLUNG SUCHREIHENFOLGE")
print(f"{'='*60}")
print(f"""
Genealogische Suche in dieser Reihenfolge:

Ring 1 (höchste Priorität):
  {" / ".join(f"NEIL {i}. G. KING" for i, _ in ranked[:5])}

Ring 2 (mittlere Priorität):
  {" / ".join(f"NEIL {i}. G. KING" for i, _ in ranked[5:8])}

Ring 3 (niedrige Priorität):
  {" / ".join(f"NEIL {i}. G. KING" for i, _ in ranked[8:])}

Falsifikationsbedingung:
  Wenn Ring 1 + Ring 2 in allen verfügbaren Quellen (SSDI, Census,
  City Directories, Voter Rolls) keinen Treffer liefert →
  entweder seltene Initial oder Chiffre-Lösung falsch.
""")
