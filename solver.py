"""
Zodiac Z13 Solver
-----------------
Versucht alle Substitutionen zu finden, die:
1. Die Constraint-Muster erfüllen (gleiche Symbole → gleiche Buchstaben)
2. Sprachlich plausibel sind (N-Gram Scoring)
3. Mit bekannten Namen aus den 1960/70ern übereinstimmen
"""

import math
import random
import string
from collections import Counter, defaultdict

# Z13 Transkription (ASCII-Repräsentation der Originalsymbole)
Z13 = "AENz0K0M0[NAM"

# Eindeutige Symbole in Reihenfolge
SYMBOLS = list(dict.fromkeys(Z13))  # ['A', 'E', 'N', 'z', '0', 'K', 'M', '[']

# Muster als Indices
PATTERN = [SYMBOLS.index(c) for c in Z13]
# [0, 1, 2, 3, 4, 5, 4, 6, 4, 7, 2, 0, 6]

# Constraints: welche Positionen müssen gleich sein
CONSTRAINTS = defaultdict(list)
for pos, sym in enumerate(Z13):
    CONSTRAINTS[sym].append(pos)

print(f"Symbole: {SYMBOLS}")
print(f"Muster:  {PATTERN}")
print(f"Constraints:")
for sym, positions in CONSTRAINTS.items():
    if len(positions) > 1:
        print(f"  Symbol '{sym}' → Positionen {positions} müssen gleichen Buchstaben haben")


# --- N-Gram Modell (englische Bigramme, approximiert) ---

# Häufigkeiten englischer Buchstaben (Näherung)
LETTER_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07, ' ': 15.0   # Leerzeichen häufig in Namen
}

# Häufige englische Bigramme (normiert)
BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'EN': 1.75, 'AT': 1.49, 'ES': 1.46,
    'ED': 1.41, 'OR': 1.34, 'TI': 1.31, 'HI': 1.28, 'ST': 1.25,
    'AR': 1.07, 'TE': 1.00, 'LE': 0.95, 'SA': 0.90, 'AL': 0.87,
    'LI': 0.85, 'LD': 0.83, 'HA': 0.82, 'ET': 0.81, 'SE': 0.80,
    'IT': 0.79, 'ND': 0.78, 'RI': 0.73, 'NG': 0.72, 'IS': 0.70,
    'EA': 0.69, 'TO': 0.68, 'RO': 0.68, 'RA': 0.66, 'LA': 0.63,
    'NT': 0.62, 'IC': 0.60, 'AS': 0.59, 'RN': 0.58, 'CH': 0.57,
    'ME': 0.56, 'MA': 0.54, 'NA': 0.53, 'EL': 0.53, 'LL': 0.52,
    'LO': 0.51, 'EY': 0.50, 'OL': 0.49, 'VE': 0.48, 'RD': 0.47,
}


def score_text(text):
    """Bewertet einen Text nach englischer Sprachwahrscheinlichkeit."""
    text = text.upper()
    score = 0.0

    # Einzelbuchstaben-Score
    for ch in text:
        if ch in LETTER_FREQ:
            score += math.log(LETTER_FREQ[ch] + 0.01)
        elif ch.isalpha():
            score += math.log(0.01)

    # Bigramm-Score
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in BIGRAMS:
            score += math.log(BIGRAMS[bigram])
        else:
            score += math.log(0.01)

    return score


def decode(mapping):
    """Dekodiert Z13 mit einem gegebenen Mapping (Liste von 8 Buchstaben)."""
    return ''.join(mapping[i] for i in PATTERN)


def is_valid_name(text):
    """Prüft ob der Text ein plausibles englisches Name-Format hat."""
    parts = text.strip().split(' ')
    if len(parts) == 2:
        return all(len(p) >= 2 and p.isalpha() for p in parts)
    if len(parts) == 3:
        return all(len(p) >= 1 and p.isalpha() for p in parts)
    if len(parts) == 1:
        return len(parts[0]) == 13 and parts[0].isalpha()
    return False


# --- Simulated Annealing Solver ---

ALPHABET = string.ascii_uppercase + ' '

def random_mapping():
    """Zufälliges Mapping von 8 Symbolen auf 8 verschiedene Zeichen."""
    chars = random.sample(list(ALPHABET), len(SYMBOLS))
    return chars


def swap_mapping(mapping):
    """Tauscht einen Eintrag im Mapping gegen einen nicht genutzten Buchstaben."""
    new_mapping = mapping.copy()
    used = set(new_mapping)
    unused = [c for c in ALPHABET if c not in used]

    if random.random() < 0.5 and unused:
        # Ersetze einen zufälligen Slot durch ungenutzten Buchstaben
        i = random.randint(0, len(new_mapping) - 1)
        new_mapping[i] = random.choice(unused)
    else:
        # Tausche zwei Slots
        i, j = random.sample(range(len(new_mapping)), 2)
        new_mapping[i], new_mapping[j] = new_mapping[j], new_mapping[i]

    return new_mapping


def simulated_annealing(n_iterations=500_000, temp_start=10.0, temp_end=0.001):
    """Simulated Annealing zur Suche des besten Mappings."""
    mapping = random_mapping()
    best_mapping = mapping.copy()
    best_score = score_text(decode(mapping))
    current_score = best_score

    results = []

    temp = temp_start
    cooling = (temp_end / temp_start) ** (1 / n_iterations)

    for i in range(n_iterations):
        temp *= cooling
        new_mapping = swap_mapping(mapping)
        new_text = decode(new_mapping)
        new_score = score_text(new_text)

        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(delta / temp):
            mapping = new_mapping
            current_score = new_score

            if current_score > best_score:
                best_score = current_score
                best_mapping = mapping.copy()
                decoded = decode(best_mapping)
                results.append((best_score, decoded))

        if i % 100_000 == 0:
            decoded = decode(best_mapping)
            print(f"  Iteration {i:>7}: Score={best_score:.2f} → '{decoded}'")

    return best_mapping, best_score, results


def constraint_search():
    """
    Direkte Constraint-Suche: Probiert alle Kombinationen für den
    'e'-Slot (Symbol '0', 3x wiederholt) und sucht passende Namen.
    Wenn '0' = Leerzeichen → Muster: XXXX_X_X_XXX
    """
    print("\n=== Constraint-Analyse ===")
    print(f"Pattern: {decode(['A','E','N','z','0','K','0','M','0','[','N','A','M'])}")
    print()

    # Zeige alle Möglichkeiten wenn '0' = Leerzeichen
    print("Falls Symbol '0' = Leerzeichen:")
    print(f"  Position 4, 6, 8 wären Leerzeichen")
    print(f"  Struktur: [0-3] [5] [7] [9-12]")
    print(f"  = 4-buchst. + 1-buchst. + 1-buchst. + 4-buchst. (unwahrsch.)")
    print()

    # Zeige Möglichkeiten wenn ein anderes Symbol = Leerzeichen
    for space_sym in ['E', 'z', 'K', '[']:
        idx = SYMBOLS.index(space_sym)
        positions = [p for p, i in enumerate(PATTERN) if i == idx]
        print(f"Falls Symbol '{space_sym}' = Leerzeichen (Position {positions}):")
        sample = ['?' for _ in range(13)]
        for p in positions:
            sample[p] = ' '
        print(f"  {''.join(sample)}")
        print()


if __name__ == '__main__':
    print("=== Zodiac Z13 Solver ===")
    print(f"Chiffre: {Z13}")
    print(f"Symbole: {SYMBOLS}")
    print(f"Muster:  {PATTERN}")
    print()

    constraint_search()

    print("\n=== Starte Simulated Annealing ===")
    print("(10 unabhängige Läufe, je 500k Iterationen)\n")

    all_results = []
    for run in range(10):
        print(f"--- Lauf {run + 1}/10 ---")
        mapping, score, results = simulated_annealing()
        decoded = decode(mapping)
        print(f"  Bestes Ergebnis: '{decoded}' (Score: {score:.2f})")
        all_results.append((score, decoded, mapping))

    # Top-Kandidaten sortiert nach Score
    all_results.sort(reverse=True)
    print("\n=== Top-Kandidaten ===")
    seen = set()
    for score, text, mapping in all_results[:20]:
        if text not in seen:
            seen.add(text)
            name_flag = "✓ NAME" if is_valid_name(text) else ""
            print(f"  Score: {score:>8.2f}  '{text}'  {name_flag}")
            print(f"         Mapping: {dict(zip(SYMBOLS, mapping))}")
