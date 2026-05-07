"""
Rankt Z13-Kandidaten nach Realitätswahrscheinlichkeit.
Kombiniert SSA-Vornamen-Score mit bekannten US-Nachnamen-Rängen.
"""

import csv
from collections import defaultdict

# US Census 2000 Top-500 Nachnamen (4 Buchstaben, normalisiert)
# Quelle: census.gov/topics/population/genealogy/data/2000_surnames.html
# rank = niedriger ist häufiger
SURNAME_RANKS = {
    # Häufigste 4-Buchstaben-Nachnamen USA
    'HALL': 26,   'HILL': 36,   'KING': 35,   'WARD': 59,   'WOOD': 93,
    'ROSS': 140,  'HUNT': 107,  'COLE': 131,  'WEST': 117,  'FORD': 278,
    'REED': 96,   'COOK': 65,   'RYAN': 198,  'GRAY': 72,   'LONG': 55,
    'SHAW': 183,  'WEBB': 189,  'WADE': 247,  'BOYD': 214,  'RICE': 132,
    'LANE': 222,  'NASH': 357,  'WOLF': 407,  'ROWE': 494,  'LOVE': 330,
    'MACK': 285,  'MOON': 462,  'HORN': 471,  'BOND': 466,  'PAGE': 276,
    'GOOD': 411,  'TODD': 283,  'BUSH': 301,  'CARR': 261,  'MANN': 354,
    'MAYS': 490,  'TRAN': 433,  'SNOW': 456,  'WALL': 316,  'VOSS': 750,
    'ROBB': 900,  'RUIZ': 163,  'KIRK': 423,  'KERN': 680,  'LAMB': 370,
    'PAUL': 619,  'MARK': 720,  'POPE': 415,  'PIKE': 618,  'SIMS': 231,
    'TATE': 298,  'VEGA': 196,  'WATT': 588,  'FREY': 632,  'RIOS': 300,
    'BRAY': 690,  'BEAL': 701,  'CONN': 660,  'DALE': 510,  'DAME': 820,
    'DALY': 540,  'DARE': 860,  'DARK': 890,  'DEAN': 259,  'DEES': 710,
    'DIAS': 430,  'DICK': 405,  'DILL': 630,  'DION': 770,  'DOVE': 750,
    'DUKE': 383,  'DYER': 430,  'EARL': 494,  'FARR': 608,  'FINK': 562,
    'FISH': 503,  'FONG': 670,  'FOXX': 820,  'FREE': 560,  'GAGE': 710,
    'GALE': 640,  'GANN': 780,  'GARR': 820,  'GEER': 850,  'GISH': 870,
    'GORE': 461,  'GOSS': 590,  'HAHN': 534,  'HALE': 234,  'HANN': 730,
    'HARD': 770,  'HARE': 630,  'HARM': 790,  'HARP': 710,  'HART': 148,
    'HASH': 840,  'HAWK': 525,  'HEAL': 810,  'HECK': 630,  'HELM': 550,
    'HEMP': 900,  'HERD': 750,  'HESS': 372,  'HIBB': 860,  'HICK': 710,
    'HIDE': 870,  'HILT': 820,  'HIRE': 790,  'HOLM': 490,  'HOLT': 266,
    'HOME': 780,  'HOOD': 360,  'HOOK': 520,  'HORN': 471,  'HOST': 810,
    'HOWE': 320,  'HULL': 337,  'HURD': 570,  'HURT': 480,  'HYDE': 453,
    'JACK': 411,  'JOBE': 770,  'JOHN': 580,  'JONE': 790,  'JUNG': 550,
    'KALE': 830,  'KAMP': 790,  'KANE': 367,  'KARP': 720,  'KEEN': 495,
    'KEEL': 720,  'KELL': 690,  'KEMP': 326,  'KERR': 414,  'KEYS': 480,
    'KIDD': 500,  'KILL': 820,  'KIPP': 810,  'KITE': 780,  'KOLB': 740,
    'LAKE': 418,  'LARK': 780,  'LASH': 790,  'LATH': 820,  'LAVE': 850,
    'LAWN': 810,  'LEAK': 760,  'LEAN': 790,  'LEAR': 720,  'LECK': 840,
    'LEFT': 860,  'LEVY': 360,  'LIME': 810,  'LINN': 580,  'LION': 830,
    'LODE': 870,  'LOFT': 840,  'LOIN': 880,  'LORE': 820,  'LUCK': 500,
    'LUND': 480,  'MACE': 590,  'MAIN': 560,  'MAKE': 850,  'MALE': 830,
    'MANE': 840,  'MARE': 780,  'MARR': 710,  'MARS': 790,  'MART': 820,
    'MASH': 840,  'MASK': 860,  'MAST': 790,  'MATE': 820,  'MAZE': 830,
    'MEAD': 560,  'MEAL': 820,  'MECK': 870,  'MELL': 800,  'MESA': 540,
    'METZ': 570,  'MICE': 880,  'MILD': 860,  'MILE': 820,  'MILL': 174,
    'MIND': 870,  'MINE': 850,  'MINK': 840,  'MINT': 830,  'MISS': 880,
    'MOCK': 740,  'MODE': 820,  'MOLD': 850,  'MOLE': 840,  'MOLL': 810,
    'MONK': 590,  'MOOR': 490,  'MORE': 440,  'MORN': 870,  'MORR': 790,
    'MORT': 760,  'MOSS': 310,  'MOTE': 840,  'MUCK': 870,  'MUDD': 780,
    'MUIR': 660,  'MULE': 880,  'MULL': 790,  'MURK': 870,  'MURR': 820,
    'MUTT': 890,  'NAIL': 720,  'NALL': 780,  'NARD': 860,  'NARE': 880,
    'NARK': 880,  'NARR': 890,  'NASH': 357,  'NATE': 830,  'NEAL': 318,
    'NECK': 870,  'NEIL': 490,  'NELL': 720,  'NELS': 660,  'NERD': 890,
    'NESS': 580,  'NICK': 650,  'NOEL': 710,  'NOEL': 710,
    'REID': 276,  'REIN': 760,  'RENT': 830,  'RICH': 267,  'RICK': 640,
    'RIDE': 820,  'RING': 570,  'RISK': 840,  'RITE': 860,  'ROAD': 870,
    'ROAN': 830,  'ROBB': 900,  'ROBE': 840,  'ROCK': 420,  'RODE': 850,
    'ROLL': 810,  'ROME': 790,  'ROOF': 840,  'ROOT': 382,  'ROPE': 860,
    'ROSE': 225,  'ROTH': 363,  'ROUS': 820,  'RUFF': 580,  'RULE': 790,
    'RUSS': 420,  'RUST': 490,
    'SAGE': 620,  'SAIL': 840,  'SALE': 680,  'SALT': 750,  'SAND': 460,
    'SEAL': 660,  'SEED': 820,  'SELF': 520,  'SELL': 710,  'SEND': 860,
    'SHAW': 183,  'SHED': 870,  'SHIP': 750,  'SHOE': 840,  'SHOT': 820,
    'SICK': 880,  'SIDE': 820,  'SILL': 790,  'SILO': 840,  'SIMS': 231,
    'SING': 690,  'SIRE': 840,  'SITE': 820,  'SKIN': 870,  'SLAB': 880,
    'SNOW': 456,  'SOAP': 880,  'SOCK': 890,  'SOLE': 820,  'SONG': 710,
    'SORE': 850,  'SORT': 840,  'SOUL': 790,  'SOUR': 840,  'SPAN': 810,
    'STAR': 630,  'STAY': 820,  'STEM': 840,  'STEP': 830,  'STEW': 700,
    'TAFT': 680,  'TALE': 820,  'TALL': 750,  'TAME': 840,  'TAPP': 760,
    'TARR': 790,  'TASK': 860,  'TATE': 298,  'TEAM': 840,  'TEAR': 850,
    'TEEM': 880,  'TEEN': 870,  'TELL': 740,  'TERM': 820,  'TERN': 840,
    'TEST': 860,  'THAW': 870,  'TIDE': 840,  'TILE': 830,  'TILL': 700,
    'TILT': 820,  'TIME': 840,  'TIRE': 850,  'TOLL': 780,  'TOMB': 860,
    'TOME': 840,  'TONE': 820,  'TOON': 790,  'TORE': 840,  'TORN': 850,
    'TORT': 860,  'TOSS': 820,  'TOUR': 830,  'TOWN': 590,  'TRAP': 840,
    'TRAY': 820,  'TRIM': 840,  'TROD': 860,  'TROY': 510,  'TRUE': 580,
    'TUCK': 470,  'TUNE': 820,  'TURK': 650,  'TURN': 760,
    'VALE': 700,  'VANE': 820,  'VANN': 540,  'VASS': 810,
    'WADE': 247,  'WAHL': 640,  'WAIN': 830,  'WAKE': 640,  'WALD': 550,
    'WALK': 820,  'WARE': 390,  'WARN': 780,  'WARP': 860,  'WART': 880,
    'WATT': 588,  'WAVE': 840,  'WEAL': 870,  'WELD': 580,  'WELL': 740,
    'WEND': 860,  'WENT': 870,  'WEST': 117,  'WILE': 850,  'WILL': 790,
    'WILT': 820,  'WINN': 530,  'WIRE': 850,  'WISE': 370,  'WOLF': 407,
    'WOOD': 93,   'WREN': 670,  'YORK': 440,  'ZAHN': 740,
}


def load_first_names(path="ssa_names.csv", years=(1935, 1975)):
    names = defaultdict(float)
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row['year'])
            if not (years[0] <= year <= years[1]):
                continue
            name = row['name'].upper()
            if len(name) == 4 and name.isalpha():
                names[name] += float(row['percent'])
    return names


def main():
    print("Lade Vornamen...")
    first_names = load_first_names()

    print("Berechne gewichtete Kandidaten...\n")

    candidates = []
    known_surnames = set(SURNAME_RANKS.keys())

    for fname, fname_score in first_names.items():
        lname_ch2 = fname[0]  # Constraint: Vorname[0] == Nachname[2]
        lname_ch1 = fname[2]  # Constraint: Vorname[2] == Nachname[1]

        for lname, lname_rank in SURNAME_RANKS.items():
            if lname[1] != lname_ch1:
                continue
            if lname[2] != lname_ch2:
                continue

            initial2 = lname[3]  # Constraint: Initial2 == Nachname[3]

            # Alle 8 Symbol-Buchstaben müssen verschieden sein (Bijektion)
            fixed = {fname[0], fname[1], fname[2], fname[3], ' ', initial2, lname[0]}
            if len(fixed) != 7:
                continue  # Kollision unter bekannten Symbolen → nicht bijektiv

            for initial1 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if initial1 in fixed:
                    continue

                # Combined score: Vorname-Häufigkeit / Nachname-Rang
                score = fname_score * 1000 / lname_rank

                candidates.append({
                    'decoded': f"{fname} {initial1} {initial2} {lname}",
                    'fname': fname,
                    'lname': lname,
                    'initial1': initial1,
                    'initial2': initial2,
                    'fname_score': fname_score,
                    'lname_rank': lname_rank,
                    'combined': score,
                })

    # Sortieren: nach kombiniertem Score (häufiger Vorname + häufiger Nachname)
    candidates.sort(key=lambda x: -x['combined'])

    print(f"Kandidaten mit bekannten Nachnamen: {len(candidates)}")
    print()

    # Unique Vor+Nachname-Paare, top 50
    seen = set()
    print(f"{'Rang':>4}  {'Vorname':<8} {'I1':>3} {'I2':>3} {'Nachname':<8}  {'Score':>8}  NachnameRang")
    print("-" * 75)
    rank = 0
    for c in candidates:
        key = (c['fname'], c['lname'])
        if key in seen:
            continue
        seen.add(key)
        rank += 1
        if rank > 50:
            break
        print(f"{rank:>4}.  {c['fname']:<8} {c['initial1']:>3} {c['initial2']:>3} "
              f"{c['lname']:<8}  {c['combined']:>8.4f}  #{c['lname_rank']}")

    # Speichern
    with open("candidates_ranked.txt", "w") as f:
        f.write("# Z13 Top-Kandidaten — gewichtet nach SSA-Vornamen + Census-Nachnamen\n")
        f.write("# Separator-Hypothese: '0' = Leerzeichen\n")
        f.write("# Format: RANG. VORNAME I1 I2 NACHNAME (score, nachname_rang)\n\n")
        rank = 0
        seen = set()
        for c in candidates:
            key = (c['fname'], c['lname'])
            if key in seen:
                continue
            seen.add(key)
            rank += 1
            f.write(f"{rank:4}. {c['decoded']:<25}  "
                    f"score={c['combined']:.4f}  lname_rank=#{c['lname_rank']}\n")

    print(f"\n→ Top-{rank} Kandidaten in candidates_ranked.txt")


if __name__ == '__main__':
    main()
