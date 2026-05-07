"""
Z13 Simulated Annealing Solver
Keine Annahmen über '0' — sucht alle möglichen Substitutionen.
Scoring via englische Quadgramm-Frequenzen.
"""

import math, random, string, time
from collections import Counter

Z13      = "AENz0K0M0[NAM"
SYMBOLS  = list(dict.fromkeys(Z13))          # 8 eindeutige Symbole in Reihenfolge
PATTERN  = [SYMBOLS.index(c) for c in Z13]   # [0,1,2,3,4,5,4,6,4,7,2,0,6]
ALPHA    = string.ascii_uppercase + ' '       # 27 mögliche Zeichen

# ---------- Quadgramm-Modell ----------
# Häufige englische Quadgramme (log-normiert, Auswahl aus dem Top-500)
# Quelle: praktopedia.com/quadgrams
RAW_QUAD = {
    "TION":7.10,"NTHE":6.44,"ATIO":6.36,"FORT":5.88,"TTHE":5.84,
    "THEM":5.72,"WITH":5.71,"THER":5.71,"THAT":5.68,"THES":5.54,
    "FROM":5.52,"THIS":5.52,"IONS":5.50,"HERE":5.46,"MENT":5.44,
    "HAVE":5.44,"THER":5.43,"TING":5.42,"HEIR":5.42,"THEI":5.41,
    "WERE":5.39,"THER":5.37,"THEY":5.37,"OULD":5.36,"ING ":5.35,
    "THRO":5.35,"NTER":5.34,"GTHE":5.32,"TATE":5.31,"INTE":5.29,
    "ATED":5.28,"STHE":5.28,"OTHE":5.27,"OUGH":5.26,"IGHT":5.26,
    "OVER":5.25,"EACH":5.25,"IGHT":5.24,"UPON":5.23,"ALLY":5.22,
    "EVEN":5.22,"DING":5.21,"HICH":5.20,"OUND":5.20,"FTHE":5.20,
    "THIN":5.18,"SUCH":5.18,"THAN":5.17,"COME":5.16,"WHEN":5.15,
    "EVER":5.15,"ENCE":5.15,"BEEN":5.14,"HAVE":5.14,"ALSO":5.13,
    "OMTH":5.12,"NAND":5.12,"LAND":5.11,"PART":5.11,"IRST":5.10,
    "SAND":5.09,"HAND":5.09,"SOME":5.09,"OULD":5.08,"ITHE":5.08,
    "REAT":5.07,"OUND":5.07,"FORM":5.06,"INES":5.06,"REAL":5.05,
    "HING":5.04,"TAND":5.04,"VERY":5.04,"WORD":5.03,"WELL":5.03,
    "ANCE":5.02,"WHIC":5.02,"LONG":5.01,"SAID":5.01,"HARD":5.00,
    "MOST":4.99,"LIKE":4.99,"JUST":4.98,"YOUR":4.97,"KNOW":4.97,
    "MAKE":4.96,"WILL":4.96,"GOOD":4.95,"INTO":4.95,"THEM":4.94,
    "ONLY":4.93,"TIME":4.93,"ABLE":4.92,"YEAR":4.92,"TAKE":4.91,
    "NAME":4.90,"JOHN":4.85,"JAMES":4.80,"MARK":4.78,"PAUL":4.75,
    "MARY":4.74,"JOAN":4.70,"ALAN":4.68,"GARY":4.65,"DEAN":4.62,
    "RYAN":4.60,"NEIL":4.58,"LEON":4.55,"TROY":4.52,"GLEN":4.50,
    "SEAN":4.48,"CHAD":4.45,"EARL":4.42,"FRED":4.40,"KYLE":4.38,
    "BRAD":4.35,"REID":4.32,"ALEX":4.30,"ERIK":4.28,"HANS":4.25,
    "KURT":4.22,"LARS":4.20,"GENE":4.18,"DALE":4.15,"WADE":4.12,
    "HILL":4.10,"HALL":4.08,"KING":4.06,"WARD":4.04,"WOOD":4.02,
    "ROSS":4.00,"HUNT":3.98,"COLE":3.96,"WEST":3.94,"FORD":3.92,
    "REED":3.90,"COOK":3.88,"GRAY":3.86,"LONG":3.84,"SHAW":3.82,
    "WEBB":3.80,"WADE":3.78,"BOYD":3.76,"RICE":3.74,"LANE":3.72,
    "NASH":3.70,"WOLF":3.68,"ROWE":3.66,"LOVE":3.64,"MACK":3.62,
    "MOON":3.60,"BOND":3.58,"PAGE":3.56,"MANN":3.54,"CARR":3.52,
    "SNOW":3.50,"WALL":3.48,"MILL":3.46,"HOLT":3.44,"HART":3.42,
    "VEGA":3.40,"WARE":3.38,"ROTH":3.36,"NEAL":3.34,"DEAN":3.32,
    "HALE":3.30,"WISE":3.28,"RICH":3.26,"REID":3.24,"ROOT":3.22,
}

FLOOR = math.log(1e-10)

def quad_score(text):
    t = text.upper()
    s = 0.0
    for i in range(len(t) - 3):
        q = t[i:i+4]
        s += math.log(RAW_QUAD.get(q, 1e-10))
    return s

# ---------- SA-Kern ----------

def decode(mapping):
    return ''.join(mapping[i] for i in PATTERN)

def rand_mapping():
    chars = random.sample(list(ALPHA), len(SYMBOLS))
    return chars

def mutate(m):
    m = m[:]
    used = set(m)
    unused = [c for c in ALPHA if c not in used]
    if unused and random.random() < 0.4:
        i = random.randrange(len(m))
        m[i] = random.choice(unused)
    else:
        i, j = random.sample(range(len(m)), 2)
        m[i], m[j] = m[j], m[i]
    return m

def sa_run(n_iter=200_000, t0=8.0, t1=0.002, seed=None):
    if seed is not None:
        random.seed(seed)
    m = rand_mapping()
    best_m, best_s = m[:], quad_score(decode(m))
    s = best_s
    cooling = (t1 / t0) ** (1.0 / n_iter)
    t = t0
    for _ in range(n_iter):
        t *= cooling
        nm = mutate(m)
        ns = quad_score(decode(nm))
        if ns > s or random.random() < math.exp((ns - s) / t):
            m, s = nm, ns
            if s > best_s:
                best_s, best_m = s, m[:]
    return best_m, best_s

# ---------- Ergebnis-Filter ----------

COMMON_NAMES_4 = {
    "JOHN","MARY","PAUL","MARK","ALAN","GARY","DEAN","RYAN","NEIL",
    "LEON","TROY","GLEN","SEAN","CHAD","EARL","FRED","KYLE","BRAD",
    "REID","ALEX","ERIK","HANS","KURT","LARS","GENE","DALE","WADE",
    "LOIS","LEAH","LUIS","JOAN","JANE","RUTH","ROSE","ANNE","BETH",
    "GAIL","KATE","LENA","LISA","LYNN","MARA","NORA","RITA","SARA",
    "TINA","VERA","ALMA","EDNA","ETTA","IDA ","IRMA","LOLA","OLGA",
}

COMMON_SURNAMES_4 = {
    "HALL","HILL","KING","WARD","WOOD","ROSS","HUNT","COLE","WEST",
    "FORD","REED","COOK","RYAN","GRAY","LONG","SHAW","WEBB","WADE",
    "BOYD","RICE","LANE","NASH","WOLF","ROWE","LOVE","MACK","MOON",
    "BOND","PAGE","MANN","CARR","SNOW","WALL","MILL","HOLT","HART",
    "VEGA","WARE","ROTH","NEAL","HALE","WISE","RICH","REID","ROOT",
    "LAMB","DEAN","ROSE","MORE","YORK","TUCK","MOSS","TODD","BUSH",
}

def classify(text):
    """Klassifiziert dekodiertes Ergebnis."""
    t = text.strip()
    flags = []
    parts = t.split()
    if len(parts) == 2 and all(p.isalpha() for p in parts):
        if parts[0] in COMMON_NAMES_4 and parts[1] in COMMON_SURNAMES_4:
            flags.append("★★ BEKANNTER VORNAME + NACHNAME")
        elif parts[0] in COMMON_NAMES_4:
            flags.append("★ BEKANNTER VORNAME")
        elif parts[1] in COMMON_SURNAMES_4:
            flags.append("★ BEKANNTER NACHNAME")
        elif all(p.isalpha() for p in parts):
            flags.append("  zwei Wörter")
    elif len(parts) == 4 and all(p.isalpha() for p in parts):
        if parts[0] in COMMON_NAMES_4 and parts[3] in COMMON_SURNAMES_4:
            flags.append("★★ VORNAME INIT INIT NACHNAME")
        else:
            flags.append("  vier Wörter")
    elif t.isalpha():
        flags.append("  ein Wort (kein Leerzeichen)")
    return ", ".join(flags) if flags else ""

# ---------- Hauptprogramm ----------

if __name__ == "__main__":
    N_RUNS = 50
    print(f"Z13 Simulated Annealing — {N_RUNS} unabhängige Läufe")
    print(f"Chiffre: {Z13}")
    print(f"Muster:  {PATTERN}")
    print(f"Symbole: {SYMBOLS}")
    print()

    results = []
    t_start = time.time()

    for run in range(N_RUNS):
        best_m, best_s = sa_run(seed=run * 137)
        text = decode(best_m)
        mapping = dict(zip(SYMBOLS, best_m))
        results.append((best_s, text, mapping))
        flag = classify(text)
        print(f"  Lauf {run+1:2}/{N_RUNS}: '{text}'  score={best_s:.1f}  {flag}")

    elapsed = time.time() - t_start
    print(f"\nLaufzeit: {elapsed:.1f}s")

    # Top-Ergebnisse (nach Score, dedupliziert)
    results.sort(reverse=True)
    seen = set()
    print(f"\n{'='*65}")
    print("TOP-KANDIDATEN")
    print(f"{'='*65}")
    rank = 0
    for score, text, mapping in results:
        if text in seen:
            continue
        seen.add(text)
        rank += 1
        flag = classify(text)
        print(f"{rank:3}. '{text}'  score={score:.1f}  {flag}")
        print(f"     Mapping: { {s: mapping[s] for s in SYMBOLS} }")

    # In Datei speichern
    with open("sa_results.txt", "w") as f:
        f.write(f"Z13 SA-Ergebnisse — {N_RUNS} Läufe\n")
        f.write(f"Chiffre: {Z13}\n\n")
        rank = 0
        seen2 = set()
        for score, text, mapping in results:
            if text in seen2:
                continue
            seen2.add(text)
            rank += 1
            f.write(f"{rank:3}. '{text}'  score={score:.1f}\n")
            f.write(f"     {mapping}\n")
    print(f"\n→ Ergebnisse in sa_results.txt")
