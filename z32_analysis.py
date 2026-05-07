"""
Z13 + Z32 Kreuzanalyse
-----------------------
Z13 = AENz0K0M0[NAM  (Brief 20. Apr 1970, "My name is —")
Z32 = C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9  (Brief 26. Jun 1970, "Bomben-Code")

Zentrale Frage: Teilen Z13 und Z32 denselben Substitutionsschlüssel?
"""

Z13 = "AENz0K0M0[NAM"
Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"

# --- Grundstatistik ---

def analyze(name, cipher):
    from collections import Counter
    freq = Counter(cipher)
    unique = len(freq)
    repeated = {s: c for s, c in freq.items() if c > 1}
    print(f"\n=== {name} ({len(cipher)} Zeichen) ===")
    print(f"  Eindeutige Symbole: {unique}")
    print(f"  Wiederholte Symbole: {repeated}")
    print(f"  Wiederholungsrate: {1 - unique/len(cipher):.1%}")
    return set(freq.keys()), freq

print("=" * 60)
syms13, freq13 = analyze("Z13", Z13)
syms32, freq32 = analyze("Z32", Z32)

# --- Überschneidung ---
overlap = syms13 & syms32
print(f"\n=== Gemeinsame Symbole (Z13 ∩ Z32) ===")
print(f"  Anzahl: {len(overlap)}")
print(f"  Symbole: {sorted(overlap)}")

print(f"\n  In Z13 nur: {sorted(syms13 - syms32)}")
print(f"  In Z32 nur: {sorted(syms32 - syms13)}")

# --- Positionen der Überschneidungs-Symbole ---
print(f"\n=== Positionen der gemeinsamen Symbole ===")
for sym in sorted(overlap):
    pos13 = [i for i, c in enumerate(Z13) if c == sym]
    pos32 = [i for i, c in enumerate(Z32) if c == sym]
    print(f"  '{sym}': Z13 Pos {pos13}  |  Z32 Pos {pos32}")

# --- Strukturvergleich ---
print(f"\n=== Strukturanalyse ===")

# Z32 Kontext um überlappende Symbole
print(f"\nZ32 Kontext (±2 Zeichen) um gemeinsame Symbole:")
for sym in sorted(overlap):
    for pos in [i for i, c in enumerate(Z32) if c == sym]:
        start = max(0, pos-2)
        end = min(len(Z32), pos+3)
        ctx = Z32[start:end]
        arrow = " " * (pos - start) + "^"
        print(f"  '{sym}' @ Z32[{pos:2}]: ...{ctx}... ({arrow})")

# --- Hypothese 1: Gleicher Schlüssel ---
print(f"\n=== Hypothese: Gleicher Substitutionsschlüssel ===")
print(f"  Wenn Z13 und Z32 denselben Schlüssel nutzen:")
print(f"  → {len(overlap)} Symbole haben in beiden Chiffren denselben Buchstaben")
print()

# Z32 repeated symbols geben uns Constraints
print("  Z32-Constraints (wiederholte Symbole):")
for sym, cnt in freq32.items():
    if cnt > 1:
        positions = [i for i, c in enumerate(Z32) if c == sym]
        in_z13 = sym in syms13
        flag = " ← auch in Z13!" if in_z13 else ""
        print(f"    '{sym}': {cnt}×  Positionen {positions}{flag}")

print()
print("  Z13-Constraints (wiederholte Symbole):")
for sym, cnt in freq13.items():
    if cnt > 1:
        positions = [i for i, c in enumerate(Z13) if c == sym]
        in_z32 = sym in syms32
        flag = " ← auch in Z32!" if in_z32 else ""
        print(f"    '{sym}': {cnt}×  Positionen {positions}{flag}")

# --- Hypothese 2: Z32 = Koordinaten ---
print(f"\n=== Hypothese: Z32 = Koordinaten ('Bombencode') ===")
print(f"  Z32 kam mit einer Straßenkarte, Mt. Diablo markiert.")
print(f"  Zodiac schrieb: 'The Mt. Diablo code concerns Radians & # inches'")
print(f"  → Wenn Z32 Koordinaten/Zahlen kodiert, dann:")
print(f"     - Viele Einmalzeichen = viele verschiedene Ziffern → plausibel")
print(f"     - Ziffern 0-9 + N/S/E/W + Dezimalpunkt = ~16 Zeichen")
print(f"     - 29 eindeutige Symbole bei 32 Zeichen → Koordinaten möglich")
print()

# Wenn Z32 = Koordinaten, was bedeuten dann die überlappenden Symbole in Z13?
print(f"  Problem: Wenn Z32 Koordinaten, dann kodieren A, E, z, M, [ in Z32")
print(f"  Ziffern oder Richtungsangaben — NICHT Buchstaben.")
print(f"  → Dann NICHT derselbe Schlüssel wie Z13!")
print()

# Mögliche Koordinaten-Dekodierung von Z32
print(f"  Beispiel-Dekodierung (French Engineer, 2023):")
print(f"  'LABOR DAY FIND 45.069 NORT 58.719 WEST'")
print(f"  → Ort: South Lake Tahoe (wo Lawrence Kane lebte)")

# --- Zusammenfassung ---
print(f"\n{'='*60}")
print("ZUSAMMENFASSUNG")
print(f"{'='*60}")
print(f"""
Z13 und Z32 teilen 5 Symbole: {sorted(overlap)}

SZENARIO A: Gleicher Schlüssel
  → 5 gemeinsame Symbole geben direkte Buchstaben-Constraints
  → Z32 (32 Zeichen) könnte helfen, Z13 einzugrenzen
  → Problem: Z32 hat kaum Wiederholungen → schwer zu lösen

SZENARIO B: Verschiedene Schlüssel
  → Z32 = Koordinaten (Bombencode), anderes Schema
  → Z13 = Namens-Chiffre, anderes Schema
  → Überschneidung ist zufällig / Zodiac nutzte dasselbe "Symbol-Alphabet"
  → Dann kein Informationsgewinn aus Z32 für Z13

WAHRSCHEINLICHSTE EINSCHÄTZUNG:
  Verschiedene Schlüssel. Z32 ist wahrscheinlich ein Koordinatencode.
  Z13 ist wahrscheinlich eine einfache Substitutionschifffre für einen Namen.
  Die gemeinsamen Symbole bedeuten: Zodiac hatte einen "Symbol-Vorrat"
  aus dem er schöpfte — nicht notwendig mit einheitlichem Schlüssel.
""")
