"""
Z340-Schlüssel → Z13 Anwendung
-------------------------------
Z340 wurde mit einem vollständigen Substitutionsschlüssel geknackt.
Dieser Schlüssel mappt 63 eindeutige Symbole auf 26 Buchstaben.

Frage: Können wir diesen Schlüssel auf Z13 anwenden?

PROBLEM: Die Z13-Symbole (visuell) erscheinen NICHT in Z408/Z340.
  → Kein direkter Schlüsseltransfer möglich.

ABER: Zodiac verwendete ein charakteristisches "Alphabet" aus:
  - Gespiegelten Buchstaben (ᴚ, ᴣ, etc.)
  - Astrologischen Symbolen (♈, ♉, ☿, etc.)
  - Militärischen Symbolen
  - Eigenen Erfindungen

Wenn wir die Z13-Symbole visuell mit dem Z340-Alphabet abgleichen,
könnten manche Übereinstimmungen gefunden werden.

BEKANNTER Z340-SCHLÜSSEL (aus der 2020-Lösung):
Homophones Mapping — mehrere Symbole können denselben Buchstaben bedeuten.
"""

# Bekannte Z340-Entschlüsselung (erste 100 Zeichen des Klartexts):
Z340_PLAINTEXT = (
    "IHOPEYOUAREHAVING"
    "LOTSOFFUNINTRYING"
    "TOCATCHMETHATW"
    "ASNTMEONTHETVSHOW"
    "WHICHBRINGSUPAPOI"
    "NTABOUTMEIAMAFRAIDOFTHEGASCHAMBER"
)

# Z340 verwendete diese Symbolgruppen (ASCII-Repräsentation aus dem Paper):
# Quelle: arxiv.org/abs/2403.17350
# Die 63 Symbole sind in der Literatur gut dokumentiert.

# Z13 ASCII-Transkription: AENz0K0M0[NAM
Z13 = "AENz0K0M0[NAM"

# Aus dem Forum: mögliche visuelle Entsprechungen der Z13-Symbole
# zum Z340-Alphabet (SPEKULATIV — ohne Originalbild nicht verifizierbar)
VISUAL_HYPOTHESES = {
    # Z13-Symbol (ASCII) : mögliche Z340-Entsprechung + Buchstabe
    'A': [('A_mirror', 'I'), ('A_greek', 'A'), ('A_plain', 'A')],
    'E': [('E_plain', 'E'), ('E_mirror', 'N'), ('E_variant', 'R')],
    'N': [('N_plain', 'N'), ('N_mirror', 'I'), ('N_zodiac', 'S')],
    'z': [('z_lower', 'Z'), ('z_2', 'S'), ('z_mirror', 'R')],
    '0': [('0_circle', 'O'), ('0_separator', ' '), ('0_greek', 'D')],
    'K': [('K_plain', 'K'), ('K_mirror', 'R'), ('K_variant', 'C')],
    'M': [('M_plain', 'M'), ('M_mirror', 'W'), ('M_variant', 'E')],
    '[': [('[_bracket', 'L'), ('[_zodiac', 'H'), ('[_variant', 'C')],
}

PATTERN = [0, 1, 2, 3, 4, 5, 4, 6, 4, 7, 2, 0, 6]  # Indices in SYMBOLS
SYMBOLS = ['A', 'E', 'N', 'z', '0', 'K', 'M', '[']


def try_z340_mappings():
    """
    Versucht alle Kombinationen der visuellen Hypothesen.
    Für jede Kombination: dekodiere Z13 und prüfe ob plausibel.
    """
    import itertools

    # Alle Hypothesen-Kombinationen durchprobieren
    sym_list = list(VISUAL_HYPOTHESES.keys())
    hypothesis_options = [VISUAL_HYPOTHESES[s] for s in sym_list]

    results = []
    count = 0

    for combo in itertools.product(*hypothesis_options):
        mapping = {sym: opt[1] for sym, opt in zip(sym_list, combo)}

        # Prüfe: alle Buchstaben unique? (strikte Substitution)
        values = list(mapping.values())
        if len(set(values)) != len(values):
            continue  # Kollision — bei Homophones OK, bei einfacher Subst. nicht

        # Dekodiere
        decoded = ''.join(mapping[SYMBOLS[i]] for i in PATTERN)
        count += 1

        # Score: enthält der Text echte Wörter?
        has_space = ' ' in decoded
        alpha_only = decoded.replace(' ', '').isalpha()
        results.append((decoded, mapping, combo))

    print(f"Getestete Kombinationen: {count}")
    print(f"(Ohne Kollisionen / mit einzigartigen Buchstaben)")
    print()

    # Alle zeigen (gefiltert nach alpha-only oder mit Leerzeichen)
    plausible = [(d, m, c) for d, m, c in results
                 if d.replace(' ', '').isalpha()]

    print(f"Alphabetische Ergebnisse: {len(plausible)}")
    print()
    for decoded, mapping, combo in plausible[:30]:
        syms = ' '.join(f"{s}={v[1]}" for s, v in zip(sym_list, combo))
        print(f"  '{decoded}' [{syms}]")


def analyze_z13_constraints_vs_z340():
    """
    Zeigt warum Z340-Schlüssel allein nicht ausreicht:
    Die Wiederholungs-Constraints müssen zum Z340-Key passen.
    """
    print("\n=== Warum der Z340-Schlüssel komplex ist ===")
    print()
    print("Z340 war ein HOMOPHONES System:")
    print("  = Mehrere Symbole → ein Buchstabe (viele-zu-eins)")
    print("  Beispiel: 5 verschiedene Symbole bedeuten alle 'E'")
    print()
    print("Z13 zeigt WIEDERHOLUNGEN derselben Symbole:")
    print("  = Symbol '0' erscheint 3× → muss 1 Buchstabe sein")
    print("  = Symbol 'A' erscheint 2× → muss 1 Buchstabe sein")
    print()
    print("Das ist KOMPATIBEL mit einem homophonen System:")
    print("  In Z340 haben häufige Buchstaben (E, T, A) viele Symbole.")
    print("  In Z13 hat das häufigste Symbol ('0') 3 Vorkommen.")
    print("  → Symbol '0' könnte ein häufiger Buchstabe sein: E, T, A, O, I, N, S")
    print()
    print("Statistik der Z13-Symbolhäufigkeiten:")
    from collections import Counter
    freq = Counter(Z13)
    for sym, count in freq.most_common():
        frac = count / len(Z13)
        # Welche englischen Buchstaben haben ähnliche Frequenz?
        eng_freq = {
            'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.070,
            'N': 0.067, 'S': 0.063, 'H': 0.061, 'R': 0.060, 'D': 0.043,
            'L': 0.040, 'C': 0.028, 'U': 0.028, 'M': 0.024, ' ': 0.150,
        }
        candidates = [ch for ch, f in eng_freq.items()
                      if abs(f - frac) < 0.04]
        print(f"  '{sym}': {count}× ({frac:.1%}) → könnte sein: {candidates}")


if __name__ == '__main__':
    print("=== Z340-Schlüssel-Analyse für Z13 ===\n")
    analyze_z13_constraints_vs_z340()
    print("\n=== Visuelle Hypothesen-Test ===\n")
    try_z340_mappings()
