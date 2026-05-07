"""
Z32 Kreuz-Dekodierung mit bekanntem Z13-Schlüssel.

Z13-Schlüssel (NEIL G. KING, bijektiv):
  A → N
  E → E
  N → I
  z → L
  0 → ' ' (Leerzeichen)
  K → [frei]
  M → G
  [ → K

Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"

Frage: Wenn Z32 denselben Schlüssel wie Z13 verwendet,
ergibt die Teilentschlüsselung ein kohärentes Muster?
"""

Z13 = "AENz0K0M0[NAM"
Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"

# Bekannter Z13-Schlüssel (Cipher-Symbol → Plaintext-Buchstabe)
KEY = {
    'A': 'N',
    'E': 'E',
    'N': 'I',
    'z': 'L',
    '0': ' ',
    'M': 'G',
    '[': 'K',
    # 'K': [frei] — unbekannt
}

print("=" * 60)
print("Z32 KREUZ-DEKODIERUNG (Z13-Schlüssel angewandt)")
print("=" * 60)

print(f"\nZ32:  {Z32}")
partial = []
unknowns = []
for i, c in enumerate(Z32):
    if c in KEY:
        partial.append(KEY[c])
    else:
        partial.append('_')
        if c not in unknowns:
            unknowns.append(c)

partial_str = ''.join(partial)
print(f"Teilk: {partial_str}")
print(f"       ", end="")
for ch in partial_str:
    print("^" if ch != '_' else " ", end="")
print()

print(f"\nBekannte Positionen:")
for i, (cipher, plain) in enumerate(zip(Z32, partial_str)):
    if plain != '_':
        print(f"  Z32[{i:2}] = '{cipher}' → '{plain}'")

print(f"\nUnbekannte Symbole in Z32: {sorted(unknowns)}")
print(f"Anzahl: {len(unknowns)} unbekannte Symbole (von 29 eindeutigen)")

# ── Z32-interne Constraints ───────────────────────────────────────────────────

print(f"\n{'='*60}")
print("Z32-INTERNE CONSTRAINTS (wiederholte Symbole)")
from collections import Counter
freq32 = Counter(Z32)
for sym, cnt in freq32.items():
    if cnt > 1:
        positions = [i for i, c in enumerate(Z32) if c == sym]
        known_val = KEY.get(sym, None)
        if known_val:
            print(f"  '{sym}' @ {positions} → beide = '{known_val}' ✓")
        else:
            print(f"  '{sym}' @ {positions} → beide = [unbekannt, aber gleich]")

# ── Welche Buchstaben fehlen noch im Schlüssel? ───────────────────────────────

print(f"\n{'='*60}")
print("VERBLEIBENDE FREIHEITSGRADE")

used_values = set(KEY.values()) - {' '}
print(f"Bereits vergebene Buchstaben: {sorted(used_values)}")
remaining = sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - used_values)
print(f"Noch verfügbar: {remaining}")
print(f"Zu belegen: {len(unknowns)} Symbole × 1 Buchstabe (bijektiv)")

# ── Kontextfenster um bekannte Positionen ─────────────────────────────────────

print(f"\n{'='*60}")
print("KONTEXT-ANALYSE")
print()
print(f"Z32:   {Z32}")
print(f"Teilk: {partial_str}")
print()

# Cluster bekannter Buchstaben
known_positions = [(i, partial_str[i]) for i in range(len(partial_str)) if partial_str[i] != '_']

print("Bekannte Cluster (aufeinanderfolgende bekannte Positionen):")
clusters = []
current = []
for i, ch in known_positions:
    if current and i > current[-1][0] + 2:
        clusters.append(current)
        current = []
    current.append((i, ch))
if current:
    clusters.append(current)

for cluster in clusters:
    positions = [p for p, _ in cluster]
    letters = [l for _, l in cluster]
    start = max(0, positions[0] - 2)
    end = min(len(Z32), positions[-1] + 3)
    context_cipher = Z32[start:end]
    context_plain = partial_str[start:end]
    print(f"  Positionen {positions}: {''.join(letters)}")
    print(f"    Cipher:  ...{context_cipher}...")
    print(f"    Teilk:   ...{context_plain}...")
    print()

# ── Hypothesen-Test ───────────────────────────────────────────────────────────

print(f"{'='*60}")
print("HYPOTHESEN")
print()

print("H1: Gleicher Schlüssel → Z32 teilweise bekannt:")
print(f"  Pos 7-9: K N G (konsekutiv)")
print(f"  Pos 26:  E")
print(f"  Pos 28:  L")
print()
print("  'KNG' an Position 7-9 ist auffällig.")
print("  Wenn Z32[6]='k' → 'I', dann lautet Pos 6-9: I K N G = 'IKING'?")
print("  Wenn Z32[10]='f' → 'I', dann lautet Pos 7-10: K N G I = 'KNGI'")
print()
print("  Englische Wörter mit KNG: KING (K-I-N-G), THINKING (-NKING), MAKING (-KING)")
print("  → 'KNG' allein ergibt keinen sinnvollen Wortstamm.")
print()

print("H2: Verschiedene Schlüssel:")
print("  Z32 = Koordinatencode (Radians + inches, Mt. Diablo)")
print("  → 'A'→'N', 'M'→'G', '['→'K' in Z32 hätten keine Buchstaben-Bedeutung")
print("  → Überschneidung zufällig aus gemeinsamem Symbol-Vorrat")
print()

# ── Koordinaten-Hypothese testen ──────────────────────────────────────────────

print(f"{'='*60}")
print("KOORDINATEN-HYPOTHESE (Z32 = Radian/Inch Code)")
print()

# Ziraoui/Garlick: Z32 könnte Mt. Diablo Koordinaten kodieren
# Mt. Diablo: 37.8816° N, 121.9142° W
# In Radians: 0.6608 N, 2.1286 W
# Zodiac: "Radians & # inches along the radians"

print("Mt. Diablo: 37.8816° N, 121.9142° W")
import math
lat_rad = math.radians(37.8816)
lon_rad = math.radians(121.9142)
print(f"  In Radian: {lat_rad:.4f} N, {lon_rad:.4f} W")
print()
print("Wenn Z32 Koordinaten kodiert:")
print("  - Benötigte Zeichen: 0-9, N/S/E/W, Punkt, evtl. Leerzeichen")
print("  - Z32 hat 29 eindeutige Symbole → zu viele für reine Ziffern")
print("  - Eher: kombiniertes Buchstaben+Zahlen System")
print()

# ── Symbolüberschneidung Z13 mit Z340 ─────────────────────────────────────────

print(f"{'='*60}")
print("BONUS: Z13-Symbole vs Z340-Symbolsatz")
print()
# Z340 verwendet einen bekannten Satz von ~63 Symbolen
# Einige davon überschneiden sich mit Z13
# (Aus dem öffentlichen Z340-Schlüssel von Oranchak 2020)
Z340_KNOWN_MAPPINGS = {
    # Ausgewählte bekannte Z340-Symbole (aus dem veröffentlichten Schlüssel)
    # Format: Z340_Symbol → Plaintext_Buchstabe
    'A': 'I',   # A in Z340 → I
    'E': 'N',   # E in Z340 → N  (vermutlich, nicht 100% sicher)
    'N': 'O',
    # z, 0, K, M, [ haben in Z340 andere/unbekannte Bedeutungen
}

print("Hinweis: Z340-Schlüssel ist öffentlich (Oranchak 2020).")
print("Z13-Symbole A, E, N, z, 0, K, M, [ kommen in Z340 teilweise vor,")
print("aber mit ANDEREN Plaintext-Buchstaben → Schlüssel ist NICHT übertragbar.")
print()
print("Das war Ziraouis Fehler: Er hat den Z340-Schlüssel direkt auf Z13 angewandt.")
print("→ Methodisch falsch, da verschiedene Chiffren-Systeme.")

print(f"\n{'='*60}")
print("FAZIT")
print(f"{'='*60}")
print("""
Mit Z13-Schlüssel (NEIL G. KING) auf Z32 angewandt:
  - Pos 7-9 ergibt K-N-G (auffällig, aber kein eindeutiges Wort)
  - Zu wenige bekannte Positionen (5 von 32) für kohärente Dekodierung
  - H2 (verschiedene Schlüssel) wahrscheinlicher

Empfehlung: Z32 als eigenständige Chiffre behandeln.
Z13-Schlüssel hilft nicht weiter bei Z32-Analyse.
""")
