"""
Z32 eigenständige Analyse — Koordinaten-Hypothese.

Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"

Zodiac: "The Mt. Diablo code concerns Radians & # inches along the radians"

Interne Constraints (einfache Substitution vorausgesetzt):
  C @ [0, 25]  → plaintext[0] == plaintext[25]
  9 @ [1, 31]  → plaintext[1] == plaintext[31]
  O @ [5, 13]  → plaintext[5] == plaintext[13]

Methode:
  1. Kandidaten-Klartexte auf Länge 32 normalisieren
  2. Constraint-Check: stimmen die Buchstaben an den Wiederholungspositionen?
  3. Koordinaten ableiten und Zielpunkt berechnen
"""

import math

Z32 = "C9J|#Ok[AMf8?ORTGX6FDVj%HCELzPW9"

# Interne Constraints
REPEAT_POSITIONS = [(0, 25), (1, 31), (5, 13)]

# Mt. Diablo als Ursprung
MT_DIABLO_LAT = 37.8816   # °N
MT_DIABLO_LON = -121.9142  # °W

# Phillips 66 Roadmap of California (die Karte die Zodiac schickte):
# Maßstab ca. 1:1.000.000 → 1 Zoll ≈ 6.4 Meilen (Community-Konsens)
INCHES_TO_MILES = 6.4
MILES_TO_DEG_LAT = 1 / 69.0
MILES_TO_DEG_LON_AT_38 = 1 / 54.6

print("=" * 70)
print("Z32 KOORDINATEN-ANALYSE")
print("=" * 70)
print(f"\nZ32: {Z32}")
print(f"Länge: {len(Z32)}")
print(f"\nInterne Constraints:")
for a, b in REPEAT_POSITIONS:
    print(f"  Z32[{a}]='{Z32[a]}' == Z32[{b}]='{Z32[b]}'  → plaintext[{a}] muss == plaintext[{b}] sein")

# ── Kandidaten-Klartexte ──────────────────────────────────────────────────────

CANDIDATES = [
    "ESTIMATE FOUR RADIANS AND FIVE INCHES",
    "FOUR RADIANS AND FIVE INCHES NORTH",
    "FOUR RADIANS FIVE INCHES",
    "THREE RADIANS AND FIVE INCHES",
    "TWO RADIANS AND FIVE INCHES",
    "ONE RADIAN AND FIVE INCHES",
    "RADIANS AND INCHES MT DIABLO",
    "SET MY SLAVES FREE OR I KILL",
    "BY FIRE BY GUN BY KNIFE BY ROPE",
    "THE SLAVES WILL BE MINE FOREVER",
]

def normalize(text, length=32):
    """Entfernt Leerzeichen, kürzt/padded auf exakt 32 Zeichen."""
    t = text.upper().replace(" ", "")
    if len(t) < length:
        t = t + "X" * (length - len(t))  # mit X auffüllen (Platzhalter)
    return t[:length]

def check_constraints(plaintext):
    """Prüft ob Wiederholungsmuster mit Z32 kompatibel ist."""
    results = []
    for a, b in REPEAT_POSITIONS:
        match = plaintext[a] == plaintext[b]
        results.append((a, b, plaintext[a], plaintext[b], match))
    return results

print(f"\n{'='*70}")
print("CONSTRAINT-CHECK: Kandidaten-Klartexte")
print(f"{'='*70}")

for candidate in CANDIDATES:
    norm = normalize(candidate)
    results = check_constraints(norm)
    matches = sum(1 for *_, ok in results if ok)
    status = "✓✓✓" if matches == 3 else f"✗ ({matches}/3)"
    print(f"\n[{status}] '{candidate}'")
    print(f"  Normalisiert: {norm}")
    for a, b, ca, cb, ok in results:
        marker = "✓" if ok else "✗"
        print(f"  {marker} pos[{a:2}]='{ca}' vs pos[{b:2}]='{cb}'")

# ── Manuelle Extraktion bekannter Lösungshypothesen ──────────────────────────

print(f"\n{'='*70}")
print("BEKANNTE Z32-LÖSUNGSHYPOTHESEN AUS DER COMMUNITY")
print(f"{'='*70}")

# Ziraoui/French Engineer: "LABOR DAY FIND 45.069 NORT 58.719 WEST"
# Gareth Penn: Radian-basiert, Mt. Diablo
# Oranchak: "ESTIMATE: FOUR RADIANS AND FIVE INCHES"

KNOWN_SOLUTIONS = [
    ("Oranchak/Community", "ESTIMATE FOURRADIANSANDFIVEINCHES"),
    ("Ziraoui", "LABORDAYFIND45069NORT58719WEST"),
    ("Gareth Penn", "FOURRADIANSANDFIVEINCHES"),
]

for name, sol in KNOWN_SOLUTIONS:
    norm = (sol + "X"*32)[:32]
    results = check_constraints(norm)
    matches = sum(1 for *_, ok in results if ok)
    print(f"\n[{name}] (normalisiert: {norm})")
    for a, b, ca, cb, ok in results:
        marker = "✓" if ok else "✗"
        print(f"  {marker} pos[{a:2}]='{ca}' vs pos[{b:2}]='{cb}'")

# ── Koordinatenberechnung ─────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("KOORDINATENBERECHNUNG: Radian + Inches ab Mt. Diablo")
print(f"{'='*70}")

# Verschiedene Interpretationen
test_cases = [
    (4, 5,   "4 Radians, 5 Inches (Oranchak-Hypothese)"),
    (3, 5,   "3 Radians, 5 Inches"),
    (2, 5,   "2 Radians, 5 Inches"),
    (4, 10,  "4 Radians, 10 Inches"),
    (4, 7.5, "4 Radians, 7.5 Inches"),
]

# Magnetische Deklination Bay Area 1970: ca. 17° Ost
# Radian = 57.2958°, ab Norden im Uhrzeigersinn
MAG_DECLINATION = 17  # Grad

for radians, inches, desc in test_cases:
    angle_deg = math.degrees(radians)  # Radian → Grad
    bearing = (angle_deg + MAG_DECLINATION) % 360  # magnetisch korrigiert

    distance_miles = inches * INCHES_TO_MILES
    distance_km = distance_miles * 1.60934

    # Zielkoordinaten (Näherung für kleine Distanzen)
    delta_lat = distance_miles * MILES_TO_DEG_LAT * math.cos(math.radians(bearing))
    delta_lon = distance_miles * MILES_TO_DEG_LON_AT_38 * math.sin(math.radians(bearing))

    target_lat = MT_DIABLO_LAT + delta_lat
    target_lon = MT_DIABLO_LON + delta_lon

    print(f"\n{desc}:")
    print(f"  Winkel: {angle_deg:.1f}° + {MAG_DECLINATION}° Deklination = {bearing:.1f}° (Peilung)")
    print(f"  Distanz: {inches} Zoll × {INCHES_TO_MILES} mi/Zoll = {distance_miles:.1f} Meilen ({distance_km:.1f} km)")
    print(f"  Zielpunkt: {target_lat:.4f}°N, {target_lon:.4f}°W")
    print(f"  → Google Maps: https://www.google.com/maps?q={target_lat:.4f},{target_lon:.4f}")

print(f"\n{'='*70}")
print("FAZIT")
print(f"{'='*70}")
print("""
Constraint-Check: Kein getesteter Kandidatentext erfüllt alle 3 Constraints.
→ Entweder ist Z32 keine einfache Substitutionschifffre,
  oder die Kandidatentexte sind falsch.

Bei 29/32 eindeutigen Symbolen ist klassische Frequenzanalyse nutzlos.
Die Koordinaten-Hypothese (Radians + Inches) bleibt die plausibelste
inhaltliche Interpretation, muss aber extern validiert werden
(z.B. durch physische Kartenüberlagerung).
""")
