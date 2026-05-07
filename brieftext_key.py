"""
Brieftext-Schlüssel-Extraktion: Zodiac-Brief 20.04.1970.

Zodiac machte im Brief absichtliche (oder unabsichtliche) Schreibfehler.
Diese könnten als Key-Material für Z13 dienen.

Bekannte Fehler im April-1970-Brief:
  "cerous"   statt "serious"   → fehlendes 's', oder 'c' für 's'
  "cid"      statt "did"       → 'c' für 'd'
  "doo"      statt "do"        → extra 'o'
  "elses"    statt "else"      → extra 's'
  "teritory" statt "territory" → fehlendes 'r'
  "figgure"  statt "figure"    → extra 'g'

Extraktions-Strategien:
  A. Erste Buchstaben der Fehlwörter: CCDETF
  B. Falsche Buchstaben (Substitutionen): C, C, O, S, -, G
  C. Fehlende Buchstaben: S, D, -, -, R, -
  D. Extra Buchstaben: -, -, O, S, -, G
  E. Position-Differenzen (ASCII-Differenz): ...

Dann: Diese Schlüssel gegen Z13 testen (Vigenere, Beaufort, Caesar-Shift).
"""

import csv
from collections import defaultdict

Z13 = "AENz0K0M0[NAM"

# Bekannte Fehler: (wrong, correct)
TYPOS = [
    ("CEROUS",   "SERIOUS"),
    ("CID",      "DID"),
    ("DOO",      "DO"),
    ("ELSES",    "ELSE"),
    ("TERITORY", "TERRITORY"),
    ("FIGGURE",  "FIGURE"),
]

print("=== Brieftext-Typo-Analyse ===\n")
print(f"{'Fehler':<12}  {'Korrekt':<12}  {'Typ':<20}  {'Extrakt'}")
print("-"*60)

# Typen von Fehlern analysieren
extracted = []
for wrong, correct in TYPOS:
    if len(wrong) < len(correct):
        # Fehlender Buchstabe
        missing = [c for c in correct if c not in wrong or correct.count(c) > wrong.count(c)]
        # Genauer: finde welcher Buchstabe fehlt
        w = list(wrong)
        for c in correct:
            if c in w: w.remove(c)
            else:
                missing_char = c; break
        else:
            missing_char = '?'
        typ = "fehlend"
        ext = missing_char
    elif len(wrong) > len(correct):
        # Extra Buchstabe
        c_list = list(correct)
        for ch in wrong:
            if ch in c_list: c_list.remove(ch)
            else:
                extra_char = ch; break
        else:
            extra_char = '?'
        typ = "extra"
        ext = extra_char
    else:
        # Substitution
        diffs = [(w, c) for w, c in zip(wrong, correct) if w != c]
        if diffs:
            typ = f"subst {diffs[0][1]}→{diffs[0][0]}"
            ext = diffs[0][0]
        else:
            typ = "identisch"
            ext = '?'

    print(f"{wrong:<12}  {correct:<12}  {typ:<20}  {ext}")
    extracted.append(ext)

print(f"\nExtrahierte Buchstaben: {''.join(extracted)}")

# Kandidaten-Schlüssel aus Typos
typo_keys = [
    ('ERSTE_BUCHST', ''.join(t[0][0] for t in TYPOS)),       # C, C, D, E, T, F
    ('EXTRA_BUCHST', ''.join(extracted)),                      # extrahierte Buchstaben
    ('FALSCH_BUCHST', 'COOSRG'),                               # die falschen Buchstaben
    ('FEHLEND',       'SDRRG'),                                # fehlende Buchstaben
    ('GROSS_KLEIN',   'ccDESF'),                               # gemischt
]

print("\n=== Genauer: was fehlt/extra ist ===")
for wrong, correct in TYPOS:
    diff_len = len(wrong) - len(correct)
    if diff_len > 0:
        for ch in wrong:
            pass  # extra Buchstabe
    print(f"  {wrong} → {correct}  (Δ={diff_len:+d})")

# Manuell präzise Schlüssel
PRECISE_KEYS = [
    ("FEHLER_INITIAL",   "CCDETF"),      # Anfangsbuchstaben der Fehlwörter
    ("RICHTIG_INITIAL",  "SDDETT"),      # Anfangsbuchstaben der richtigen Wörter
    ("EXTRA_LETTERS",    "OOSG"),        # Nur die extra Buchstaben (DOO:O, ELSES:S, FIGGURE:G)
    ("MISSING_LETTERS",  "SDR"),         # Nur fehlende Buchstaben (CEROUS:S, CID:D, TERITORY:R)
    ("SUBST_WRONG",      "CC"),          # Substitutions-Buchstaben falsch
    ("SUBST_RIGHT",      "SD"),          # Substitutions-Buchstaben richtig
    ("ALL_EXTRACTED",    "COOSRG"),      # Alle abnormalen Buchstaben
    ("REVERSE_ALL",      "GROOSOC"),     # Reverse
    ("FIRST_LETTERS_ALL","CDDETF"),      # alle Fehlwörter Anfangsbuchstabe
]

print("\n=== Vigenere/Caesar mit Typo-Schlüsseln ===\n")

def key_to_nums(key):
    return [ord(c.upper()) - ord('A') for c in key if c.upper().isalpha()]

def vigenere_decrypt(cipher_nums, key_nums):
    n = len(key_nums)
    return [(c - key_nums[i % n]) % 26 for i, c in enumerate(cipher_nums)]

def beaufort_decrypt(cipher_nums, key_nums):
    n = len(key_nums)
    return [(key_nums[i % n] - c) % 26 for i, c in enumerate(cipher_nums)]

def caesar_all(cipher_nums):
    results = []
    for shift in range(26):
        plain = [(c - shift) % 26 for c in cipher_nums]
        results.append((shift, plain))
    return results

ALPHA_CODES_Z13 = {
    'A': 0, 'E': 4, 'N': 13, 'z': 25,
    '0': 14, 'K': 10, 'M': 12, '[': 0
}

cipher_nums = [ALPHA_CODES_Z13[c] for c in Z13]
print(f"Z13 numerisch (Basis-Kodierung): {cipher_nums}")

# Namen-DB
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

def check_name(plain_nums):
    """Prüft ob die 13 entschlüsselten Zahlen einen 4+1+1+4-Namen ergeben."""
    text = ''.join(chr(n % 26 + ord('A')) for n in plain_nums)
    # Constraints müssen noch gelten (für monoalphabetische Substitution gelten sie trivial)
    # Für Vigenere: nur wenn t[4]=t[6]=t[8] (same space symbol) → Constraint erfüllt
    if not (text[4] == text[6] == text[8]):
        return None
    if text[0] != text[11] or text[2] != text[10] or text[7] != text[12]:
        return None
    fname = text[0:4]
    init2 = text[7]
    lname = text[9:13]
    if fname not in first4 or lname not in last4:
        return None
    known = {text[0], text[1], text[2], text[3], text[4], text[7], text[9]}
    if len(known) != 7:
        return None
    return text

hits = []

# Caesar-Shift (alle 26)
for shift, plain in caesar_all(cipher_nums):
    result = check_name(plain)
    if result:
        hits.append((first4.get(result[0:4], 0), f"CAESAR-{shift}", result))

# Vigenere + Beaufort mit Typo-Schlüsseln
for key_name, key_str in PRECISE_KEYS:
    knums = key_to_nums(key_str)
    if not knums:
        continue
    for method_name, method in [('VIG', vigenere_decrypt), ('BEA', beaufort_decrypt)]:
        plain = method(cipher_nums, knums)
        result = check_name(plain)
        if result:
            hits.append((first4.get(result[0:4], 0), f"{method_name}-{key_name}", result))

if hits:
    hits.sort(reverse=True)
    print("TREFFER:")
    for score, desc, text in hits:
        fname = text[0:4]
        init2 = text[7]
        lname = text[9:13]
        print(f"  [{desc}] {fname} *. {init2}. {lname}  score={score:.5f}")
else:
    print("Kein Treffer mit Typo-Schlüsseln.")
    print("\n→ Brieftext-Typos als direktes Schlüsselmaterial: ausgeschlossen.")
    print("\nZeigt: Die Fehlschreibungen im April-Brief sind kein einfacher Vigenere-Schlüssel für Z13.")

# Extra: Welche Caesar-Shifts produzieren interessante Texte (auch ohne Namens-Match)?
print("\n=== Caesar-Shifts → erzeugte Texte (alle 26) ===")
for shift in range(26):
    plain = [(c - shift) % 26 for c in cipher_nums]
    text = ''.join(chr(n + ord('A')) for n in plain)
    # Nur wenn Constraints noch sichtbar
    tags = []
    if text[4] == text[6] == text[8]: tags.append("0-triple")
    if text[0] == text[11]: tags.append("A-pair")
    if text[2] == text[10]: tags.append("N-pair")
    if text[7] == text[12]: tags.append("M-pair")
    tag_str = ','.join(tags) if tags else ''
    marker = " ←" if len(tags) == 4 else ""
    print(f"  shift={shift:2}: {text}  {tag_str}{marker}")
