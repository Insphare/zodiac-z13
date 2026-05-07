"""
Z32 Schlüsselableitung — wenn Klartext bekannt ist.

Annahme: Z32 = "ESTIMATEFOURRADIANSANDFIVEINCHES" (Leerzeichen entfernt)
Prüft ob das mit einfacher Substitution vereinbar ist (Bijektions-Check).
"""

Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"
PT  = "ESTIMATEFOURRADIANSANDFIVEINCHES"

assert len(Z32) == len(PT) == 32

print("=" * 70)
print("Z32 SCHLÜSSELABLEITUNG")
print("=" * 70)
print(f"\nZ32: {Z32}")
print(f"PT:  {PT}")

# Vollständige Mapping-Tabelle
mapping = {}
violations = []

for i, (c, p) in enumerate(zip(Z32, PT)):
    if c in mapping:
        if mapping[c] != p:
            violations.append(f"  KOLLISION @ pos {i}: '{c}' → '{mapping[c]}' aber auch '{p}'")
    else:
        mapping[c] = p

print(f"\n{'─'*70}")
print("ABGELEITETER SCHLÜSSEL (Chiffre-Symbol → Klartext-Buchstabe):")
print(f"{'─'*70}")
for cipher, plain in sorted(mapping.items()):
    positions = [i for i, c in enumerate(Z32) if c == cipher]
    print(f"  '{cipher}' → '{plain}'  (pos {positions})")

# Bijektions-Check: verschiedene Symbole → verschiedene Buchstaben?
print(f"\n{'─'*70}")
print("BIJEKTIONS-CHECK:")
print(f"{'─'*70}")

# Umgekehrtes Mapping: Klartext → welche Symbole?
reverse = {}
for c, p in mapping.items():
    reverse.setdefault(p, []).append(c)

bijective = True
for plain, ciphers in sorted(reverse.items()):
    if len(ciphers) > 1:
        bijective = False
        print(f"  ✗ '{plain}' ← {ciphers}  (Kollision: {len(ciphers)} Symbole → selber Buchstabe)")
    else:
        print(f"  ✓ '{plain}' ← {ciphers[0]}")

print(f"\n{'─'*70}")
if violations:
    print(f"Symbol-Konsistenz-Verletzungen (gleicher Chiffre → verschiedene Buchstaben):")
    for v in violations:
        print(v)
else:
    print("Symbol-Konsistenz: ✓ (gleiches Symbol immer gleicher Buchstabe)")

print(f"\n{'─'*70}")
print("FAZIT:")
if bijective and not violations:
    print("  ✓ Vollständig bijektiv — kompatibel mit einfacher Substitution")
elif not violations and not bijective:
    n_collisions = sum(1 for ciphers in reverse.values() if len(ciphers) > 1)
    print(f"  ✗ Nicht bijektiv: {n_collisions} Klartext-Buchstaben von mehreren Symbolen kodiert")
    print(f"  → Einfache Substitution ausgeschlossen")
    print(f"  → Homophone Substitution möglich (wie Z408/Z340)")
    print(f"  → Oder: Klartext enthält Ziffern/Sonderzeichen statt nur Buchstaben")
else:
    print(f"  ✗ Inkonsistente Mappings — Klartext wahrscheinlich falsch")

# Z13-Kreuzcheck: teilen Z32 und Z13 Symbole?
print(f"\n{'─'*70}")
print("KREUZCHECK: Gemeinsame Symbole Z13 ↔ Z32")
Z13 = "AENz0K0M0[NAM"
Z13_KEY = {'A': 'N', 'E': 'E', 'N': 'I', 'z': 'L', '0': ' ', 'M': 'G', '[': 'K'}

overlap = set(mapping.keys()) & set(Z13_KEY.keys())
print(f"  Gemeinsame Symbole: {sorted(overlap)}")
for sym in sorted(overlap):
    z32_val = mapping[sym]
    z13_val = Z13_KEY.get(sym, '?')
    match = "✓" if z32_val == z13_val else "✗"
    print(f"  {match} '{sym}': Z32→'{z32_val}'  vs  Z13→'{z13_val}'")
