"""
Polyalphabetischer Test: Vigenere / Beaufort auf Z13.

Problem: Z13 enthält nicht-alphabetische Symbole (0, [, z).
Lösung: Wir testen mehrere Kodierungen für die 8 Symbole.

Symbol-Kodierung (Nummer → Alphabetposition 0-25):
  A=0, E=4, N=13, z=25, 0=14(O)/24(Y)/0, K=10, M=12, [=26→0/1/27

Vigenere-Entschlüsselung: p[i] = (c[i] - k[i%keylen]) mod 26

Getestete Schlüssel (Zodiac-Briefkorpus):
  ZODIAC, PARADICE, SLAVES, KILL, MYNAMEIS, ZODIAC KILLER,
  SFPD, BOMB, GAS, KNIFE, GUN
"""

import csv
from collections import defaultdict
from itertools import product

Z13 = "AENz0K0M0[NAM"

# Symbole → Alphabet-Indizes
# Für nicht-alphabetische Symbole testen wir mehrere Mappings
ALPHA_CODES = {
    'A': [0],    # A=0
    'E': [4],    # E=4
    'N': [13],   # N=13
    'z': [25],   # z→Z=25
    '0': [14, 0, 15],  # O=14, oder A=0, oder P=15
    'K': [10],   # K=10
    'M': [12],   # M=12
    '[': [26 % 26, 1, 27 % 26],  # 0, B=1, 1
}

KEYS = [
    "ZODIAC",
    "PARADICE",
    "SLAVES",
    "KILL",
    "MYNAMEIS",
    "SFPD",
    "BOMB",
    "GAS",
    "KNIFE",
    "ZODIACKILR",
    "DEADMAN",
    "CIPHER",
    "CRYPTIC",
    "SLAVE",
]

def key_to_nums(key):
    return [ord(c) - ord('A') for c in key.upper() if c.isalpha()]

def vigenere_decrypt(cipher_nums, key_nums):
    out = []
    n = len(key_nums)
    for i, c in enumerate(cipher_nums):
        p = (c - key_nums[i % n]) % 26
        out.append(p)
    return out

def beaufort_decrypt(cipher_nums, key_nums):
    out = []
    n = len(key_nums)
    for i, c in enumerate(cipher_nums):
        p = (key_nums[i % n] - c) % 26
        out.append(p)
    return out

def nums_to_text(nums):
    return ''.join(chr(n + ord('A')) for n in nums)

# ── Namen-Datenbank laden ─────────────────────────────────────────────────────

print("Lade Daten...")
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

known_first = set(first4.keys())
print(f"  {len(first4)} Vornamen, {len(last4)} Nachnamen")

# ── Alle Symbol-Kodierungs-Kombinationen ─────────────────────────────────────

# Positionen der Symbole in Z13
sym_at_pos = [ALPHA_CODES[c] for c in Z13]  # Liste von Listen

# Zähle Kombinationen
total_encodings = 1
for codes in sym_at_pos:
    total_encodings *= len(codes)
print(f"Symbol-Kodierungs-Kombinationen: {total_encodings}")
print(f"Schlüssel getestet: {len(KEYS)}")
print(f"Methoden: Vigenere + Beaufort = 2")
print(f"Gesamt Tests: {total_encodings * len(KEYS) * 2:,}\n")

# ── Hauptsuche ────────────────────────────────────────────────────────────────

hits = []

for encoding in product(*sym_at_pos):
    # encoding ist ein Tupel von 13 Zahlen (0-25)
    for key_str in KEYS:
        key_nums = key_to_nums(key_str)
        if not key_nums:
            continue

        for method_name, method in [('Vigenere', vigenere_decrypt),
                                     ('Beaufort', beaufort_decrypt)]:
            plain = method(list(encoding), key_nums)
            text = nums_to_text(plain)

            # Prüfe 0=Space Struktur: Zeichen an Positionen 4,6,8 müssen gleich sein
            # (das sind die Positionen des '0'-Symbols in Z13)
            if not (text[4] == text[6] == text[8]):
                continue

            # 4+1+1+4 Extraktion
            fname = text[0:4]
            init1 = text[5]
            init2 = text[7]
            lname = text[9:13]

            # Prüfe Kreuz-Constraints (A: text[0]=text[11], N: text[2]=text[10])
            if text[0] != text[11]:
                continue
            if text[2] != text[10]:
                continue
            if text[7] != text[12]:
                continue

            # Namen-DB-Check
            if fname not in known_first:
                continue
            if lname not in last4:
                continue

            # Bijektions-Check
            known_vals = {text[0], text[1], text[2], text[3], text[4], text[7], text[9]}
            if len(known_vals) != 7:
                continue

            hits.append({
                'text': text,
                'fname': fname,
                'init1': init1,
                'init2': init2,
                'lname': lname,
                'key': key_str,
                'method': method_name,
                'score': first4.get(fname, 0),
                'encoding': encoding,
            })

# ── Ausgabe ───────────────────────────────────────────────────────────────────

print(f"{'='*70}")
print(f"VIGENERE/BEAUFORT TEST: {len(hits)} Treffer")
print(f"{'='*70}\n")

if not hits:
    print("Kein einziger bijektiver Namens-Treffer unter allen getesteten")
    print("Schlüsseln und Symbol-Kodierungen.")
    print("\n→ Polyalphabetische Modelle mit diesen Schlüsseln scheiden aus.")
else:
    hits.sort(key=lambda h: -h['score'])
    print(f"{'Rang':>4}  {'Methode':<10}  {'Schlüssel':<12}  {'Name':<25}  Score")
    print("-"*65)
    seen = set()
    rank = 0
    for h in hits:
        key = (h['fname'], h['lname'], h['key'], h['method'])
        if key in seen:
            continue
        seen.add(key)
        rank += 1
        name_str = f"{h['fname']} {h['init1']}. {h['init2']}. {h['lname']}"
        print(f"{rank:>4}.  {h['method']:<10}  {h['key']:<12}  {name_str:<25}  {h['score']:.5f}")
        if rank >= 20:
            break

print(f"\nFazit: {'Kein Polyalphabetisches Modell bestätigt sich.' if not hits else str(len(hits)) + ' Treffer — Details oben.'}")
