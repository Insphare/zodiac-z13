"""
Z13 SA mit Namen-spezifischem Scoring.
Baut Bigramm/Trigramm-Modell aus echten US-Namen (SSA + Census).
"""

import math, random, string, csv, time
from collections import Counter, defaultdict

Z13     = "AENz0K0M0[NAM"
SYMBOLS = list(dict.fromkeys(Z13))
PATTERN = [SYMBOLS.index(c) for c in Z13]
ALPHA   = string.ascii_uppercase + ' '

# ── Namen laden ──────────────────────────────────────────────────────────────

def load_names():
    """Lädt alle 4-buchstabigen Vor- und Nachnamen."""
    first = set()
    last  = set()

    # SSA Vornamen
    try:
        with open("ssa_names.csv") as f:
            for row in csv.DictReader(f):
                if 1930 <= int(row["year"]) <= 1980:
                    n = row["name"].upper()
                    if 3 <= len(n) <= 7 and n.isalpha():
                        first.add(n)
    except FileNotFoundError:
        pass

    # US Nachnamen
    try:
        with open("us_surnames.txt") as f:
            for line in f:
                n = line.strip().upper()
                if 3 <= len(n) <= 8 and n.isalpha():
                    last.add(n)
    except FileNotFoundError:
        pass

    return first, last

# ── N-Gram-Modell aus Namen bauen ─────────────────────────────────────────────

def build_name_ngrams(first_names, last_names):
    """Baut Bigramm + Trigramm-Häufigkeiten aus echten Namen."""
    bi  = Counter()
    tri = Counter()

    all_names = list(first_names) + list(last_names)
    for name in all_names:
        n = "^" + name + "$"          # Wortgrenzen-Marker
        for i in range(len(n)-1):
            bi[n[i:i+2]]  += 1
        for i in range(len(n)-2):
            tri[n[i:i+3]] += 1

    total_bi  = sum(bi.values())
    total_tri = sum(tri.values())

    log_bi  = {k: math.log(v/total_bi)  for k, v in bi.items()}
    log_tri = {k: math.log(v/total_tri) for k, v in tri.items()}

    return log_bi, log_tri


def score_as_name(text, log_bi, log_tri,
                  first_set, last_set,
                  known_first, known_last):
    """
    Bewertet einen 13-Zeichen-String als Namen.
    Bonus für bekannte Vornamen/Nachnamen.
    """
    t = text.strip()
    parts = t.split()
    score = 0.0
    floor_bi  = -15.0
    floor_tri = -18.0

    # N-Gram Score über den gesamten String (mit Wortgrenzen)
    for word in (parts if parts else [t]):
        w = "^" + word + "$"
        for i in range(len(w)-1):
            score += log_bi.get(w[i:i+2],  floor_bi)
        for i in range(len(w)-2):
            score += log_tri.get(w[i:i+3], floor_tri)

    # Strukturbonus
    if len(parts) == 2 and all(p.isalpha() for p in parts):
        # Vorname + Nachname (ideal)
        score += 5.0
        if parts[0] in known_first:
            score += 20.0
        elif parts[0] in first_set:
            score += 8.0
        if parts[1] in known_last:
            score += 20.0
        elif parts[1] in last_set:
            score += 8.0

    elif len(parts) == 4 and all(p.isalpha() for p in parts):
        # Vorname Initial Initial Nachname
        score += 3.0
        if parts[0] in known_first:
            score += 15.0
        elif parts[0] in first_set:
            score += 6.0
        if parts[3] in known_last:
            score += 15.0
        elif parts[3] in last_set:
            score += 6.0
        if len(parts[1]) == 1 and len(parts[2]) == 1:
            score += 4.0    # Beide echte Initialen

    elif len(parts) == 3 and all(p.isalpha() for p in parts):
        score += 2.0

    return score


# ── SA-Kern ───────────────────────────────────────────────────────────────────

def decode(mapping):
    return ''.join(mapping[i] for i in PATTERN)

def rand_mapping():
    return random.sample(list(ALPHA), len(SYMBOLS))

def mutate(m):
    m = m[:]
    used = set(m)
    unused = [c for c in ALPHA if c not in used]
    if unused and random.random() < 0.35:
        i = random.randrange(len(m))
        m[i] = random.choice(unused)
    else:
        i, j = random.sample(range(len(m)), 2)
        m[i], m[j] = m[j], m[i]
    return m

def sa_run(score_fn, n_iter=80_000, t0=6.0, t1=0.001, seed=None):
    if seed is not None:
        random.seed(seed)
    m = rand_mapping()
    best_m, best_s = m[:], score_fn(decode(m))
    s = best_s
    cooling = (t1/t0) ** (1.0/n_iter)
    t = t0
    for _ in range(n_iter):
        t *= cooling
        nm = mutate(m)
        ns = score_fn(decode(nm))
        if ns > s or random.random() < math.exp(min(0, (ns-s)/t)):
            m, s = nm, ns
            if s > best_s:
                best_s, best_m = s, m[:]
    return best_m, best_s


# ── Hauptprogramm ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Lade Namen-Datenbanken...")
    first_set, last_set = load_names()
    print(f"  Vornamen: {len(first_set)},  Nachnamen: {len(last_set)}")

    print("Baue Namen-N-Gramm-Modell...")
    log_bi, log_tri = build_name_ngrams(first_set, last_set)
    print(f"  Bigramme: {len(log_bi)},  Trigramme: {len(log_tri)}")

    # Top-Vornamen/Nachnamen für Bonus
    known_first = {
        "JOHN","JAMES","ROBERT","WILLIAM","RICHARD","CHARLES","DONALD",
        "GEORGE","THOMAS","JOSEPH","EDWARD","HENRY","FRANK","WALTER",
        "HAROLD","PAUL","JACK","CARL","ARTHUR","ALBERT","PETER","RAYMOND",
        "GARY","LARRY","JERRY","DENNIS","GERALD","ROGER","KEITH","PHILIP",
        "ALAN","MARK","BRUCE","RALPH","FRED","ERIC","NEIL","DALE","DEAN",
        "GLEN","CHAD","EARL","TROY","SEAN","RYAN","KURT","LARS","GENE",
        "LOIS","MARY","LINDA","BARBARA","PATRICIA","CAROL","SANDRA","HELEN",
        "MARGARET","BETTY","RUTH","VIRGINIA","DOROTHY","JEAN","ALICE","JOAN",
        "JANE","ANNE","ROSA","LISA","LEAH","GAIL","KATE","SARA","TINA",
    }
    known_last = {
        "SMITH","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR",
        "ANDERSON","THOMAS","JACKSON","WHITE","HARRIS","MARTIN","THOMPSON",
        "GARCIA","MARTINEZ","ROBINSON","CLARK","RODRIGUEZ","LEWIS","LEE",
        "WALKER","HALL","ALLEN","YOUNG","HERNANDEZ","KING","WRIGHT","LOPEZ",
        "HILL","SCOTT","GREEN","ADAMS","BAKER","GONZALEZ","NELSON","CARTER",
        "MITCHELL","PEREZ","ROBERTS","TURNER","PHILLIPS","CAMPBELL","PARKER",
        "EVANS","EDWARDS","COLLINS","STEWART","SANCHEZ","MORRIS","ROGERS",
        "REED","COOK","MORGAN","BELL","MURPHY","BAILEY","RIVERA","COOPER",
        "WARD","COX","DIAZ","FOSTER","GRAY","JAMES","WOOD","ROSS","HUNT",
        "COLE","WEST","FORD","RYAN","LONG","SHAW","WEBB","WADE","BOYD",
        "RICE","LANE","NASH","WOLF","MANN","CARR","SNOW","WALL","MILL",
        "HOLT","HART","WARE","ROTH","NEAL","HALE","WISE","RICH","REID",
    }

    score_fn = lambda text: score_as_name(
        text, log_bi, log_tri, first_set, last_set, known_first, known_last
    )

    N_RUNS = 60
    print(f"\nStarte {N_RUNS} SA-Läufe (Namen-Scoring)...\n")
    t_start = time.time()

    results = []
    for run in range(N_RUNS):
        best_m, best_s = sa_run(score_fn, seed=run * 97)
        text = decode(best_m)
        mapping = dict(zip(SYMBOLS, best_m))
        results.append((best_s, text, mapping))
        parts = text.split()
        tag = ""
        if len(parts) == 2 and parts[0] in known_first and parts[1] in known_last:
            tag = "  ★★ VOLLSTÄNDIGER NAME"
        elif len(parts) == 2 and (parts[0] in known_first or parts[1] in known_last):
            tag = "  ★ TEILWEISE BEKANNT"
        print(f"  Lauf {run+1:2}/{N_RUNS}: '{text}'  score={best_s:.1f}{tag}")

    elapsed = time.time() - t_start
    print(f"\nLaufzeit: {elapsed:.1f}s")

    # Top-Ergebnisse
    results.sort(reverse=True)
    seen = set()
    print(f"\n{'='*65}")
    print("TOP-KANDIDATEN (Namen-Scoring)")
    print(f"{'='*65}")
    rank = 0
    for score, text, mapping in results:
        if text in seen:
            continue
        seen.add(text)
        rank += 1
        if rank > 20:
            break
        parts = text.split()
        flag = ""
        if len(parts) >= 2:
            if parts[0] in known_first and parts[-1] in known_last:
                flag = "  ★★ BEKANNTER NAME"
            elif parts[0] in known_first or parts[-1] in known_last:
                flag = "  ★"
        print(f"{rank:3}. '{text}'  score={score:.1f}{flag}")
        print(f"     { {s: mapping[s] for s in SYMBOLS} }")

    with open("name_sa_results.txt", "w") as f:
        f.write("Z13 Namen-SA Ergebnisse\n\n")
        rank = 0
        seen2 = set()
        for score, text, mapping in results:
            if text in seen2: continue
            seen2.add(text)
            rank += 1
            f.write(f"{rank:3}. '{text}'  score={score:.1f}\n     {mapping}\n")
    print(f"\n→ name_sa_results.txt")
