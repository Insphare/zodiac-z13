"""
Z13 Separator-Hypothese
-----------------------
Wenn '0' = Leerzeichen, ergibt sich die Struktur:

  A E N z [SP] K [SP] M [SP] [ N A M
  0 1 2 3  4   5  6   7  8   9 10 11 12

  Gruppen: [0-3] [5] [7] [9-12]
  = Vorname(4) + Initial(1) + Initial(1) + Nachname(4)
  Beispiel: "JOHN A B MANN"

WICHTIGE CONSTRAINTS bei dieser Hypothese:
  - p[0] == p[11]  → Vorname[0] == Nachname[2]
  - p[2] == p[10]  → Vorname[2] == Nachname[1]
  - p[7] == p[12]  → Initial2  == Nachname[3]

Das bedeutet: Vorname und Nachname teilen sich Buchstaben!
"""

import itertools

Z13 = "AENz0K0M0[NAM"
SYMBOLS = list(dict.fromkeys(Z13))
PATTERN = [SYMBOLS.index(c) for c in Z13]

# Häufige 4-buchstabige Vornamen (USA, 1940-1975)
FIRST_NAMES_4 = [
    "ALAN", "ALEX", "BILL", "BRAD", "BRET", "BUCK", "CARL", "CHAD",
    "CHIP", "CLAY", "COLE", "DALE", "DANA", "DAVE", "DEAN", "DICK",
    "DION", "DONG", "EARL", "EDEN", "ERIC", "EVAN", "FORD", "FRED",
    "GARY", "GENE", "GLEN", "GREG", "HANS", "HANK", "HUGO", "IVAN",
    "JACK", "JAKE", "JOEL", "JOHN", "JOSE", "JUAN", "KARL", "KENT",
    "KERN", "KIRK", "KURT", "KYLE", "LANE", "LARS", "LEON", "LYLE",
    "MARC", "MARK", "MATT", "MIKE", "NEIL", "NICK", "NOEL", "NORM",
    "OTTO", "PAUL", "PETE", "PHIL", "RENE", "RICK", "ROBB", "ROLF",
    "ROSS", "RYAN", "SEAN", "SETH", "SKIP", "STAN", "TEDD", "TREY",
    "TROY", "WADE", "WARD", "WILL", "WINN", "ZACH", "ABEL", "ADAM",
    "ALDO", "AMOS", "ARNE", "BART", "BEAU", "BELA", "BENN", "BERT",
    "BION", "BIRL", "BLAIN", "BLAS", "BRAM", "BREN", "BRET", "BRYN",
    "BURL", "BURT", "BUZZ", "CAIN", "CALE", "CASS", "CHET", "CIRO",
    "CLEM", "CLIF", "CLUS", "CODY", "CORY", "CRIS", "CURT", "CYAN",
    "DANA", "DANI", "DANO", "DANY", "DARA", "DARL", "DARN", "DARY",
    "DEEN", "DELF", "DELI", "DELL", "DEMA", "DEMI", "DENN", "DENY",
    "DERN", "DEST", "DEVA", "DIAN", "DIEN", "DINO", "DIOM", "DIRK",
    "DOAN", "DOLE", "DOLL", "DOMI", "DOMO", "DONA", "DONE", "DONG",
    "DONI", "DONN", "DONO", "DONY", "DORA", "DORE", "DORI", "DORN",
    "DORY", "DOSS", "DOTS", "DOUR", "DOVA", "DOVE", "DOWE", "DOYE",
    "DRIN", "DRLA", "DRON", "DROS", "DRUM", "DUAL", "DUAN", "DUBB",
]

# Häufige 4-buchstabige Nachnamen (USA)
LAST_NAMES_4 = [
    "ABEL", "ADAM", "ADDY", "AGER", "AHEM", "AKER", "ALES", "ALIA",
    "ALLS", "ALMO", "ALMY", "ALSO", "ALVA", "ALVY", "AMBY", "AMES",
    "AMOR", "AMOS", "AMPT", "AMSO", "ANDY", "ANEW", "ANGO", "ANIS",
    "ANNA", "ANNE", "ANNY", "ANON", "ANSA", "ANSI", "ANSO", "ANST",
    "ANTS", "ANVY", "APEX", "APSO", "ARAT", "ARCE", "ARCH", "ARDS",
    "ARDY", "ARES", "ARGY", "ARIA", "ARID", "ARIE", "ARIM", "ARIN",
    "ARIS", "ARIV", "ARLA", "ARLE", "ARLS", "ARLY", "ARMA", "ARME",
    "BABB", "BACA", "BAIN", "BAEZ", "BALE", "BALL", "BANE", "BARE",
    "BARR", "BASS", "BEAL", "BEAM", "BEAN", "BECK", "BELL", "BELT",
    "BENN", "BERG", "BEST", "BIRD", "BISE", "BISH", "BIXBY", "BLAB",
    "BLAK", "BLAN", "BLAS", "BLAW", "BLAY", "BLED", "BLEN", "BLEW",
    "CADE", "CAGE", "CAIN", "CAKE", "CALL", "CAME", "CAMP", "CANE",
    "CARE", "CARL", "CARN", "CARR", "CASH", "CASE", "CAST", "CATO",
    "CAVE", "CHAM", "CHAN", "CHAR", "CHEN", "CHEW", "CHOY", "CLAY",
    "COLE", "COMA", "CONE", "COOK", "COOL", "CORD", "CORE", "CORK",
    "CORN", "CORS", "CORT", "CORY", "COST", "COTE", "COTT", "COVE",
    "DALE", "DANA", "DANE", "DARK", "DARR", "DART", "DATA", "DATE",
    "DAVE", "DAWN", "DAYS", "DAZE", "DEAN", "DEAR", "DECK", "DEEM",
    "DEEP", "DEER", "DELL", "DEMO", "DENT", "DICE", "DICK", "DILL",
    "DION", "DISK", "DISS", "DOAN", "DOCK", "DOES", "DOME", "DONE",
    "DUKE", "DUNE", "DUNN", "DYER", "DYKE", "EARL", "EARP", "EAST",
    "EDEN", "EDGE", "EGON", "ELEM", "ELLS", "ELMS", "ELSE", "EVAN",
    "FARE", "FARN", "FARO", "FARR", "FAST", "FATE", "FAWN", "FAYE",
    "FORD", "FORE", "FORK", "FORM", "FORT", "FOXX", "FREE", "FREY",
    "GALE", "GALL", "GAMM", "GANN", "GANO", "GANT", "GANZ", "GARD",
    "GORE", "GORT", "GOSS", "GOTT", "GRAY", "GREG", "GREW", "GREY",
    "GRIM", "GRIN", "GRIP", "GRIZ", "GROB", "GROG", "GRON", "GREW",
    "HAHN", "HAIR", "HALE", "HALL", "HALS", "HALT", "HAMP", "HAND",
    "HANN", "HARD", "HARE", "HARM", "HARN", "HARP", "HARR", "HART",
    "HASH", "HASS", "HAST", "HATE", "HAUL", "HAWK", "HAWN", "HEAD",
    "HEAL", "HEAP", "HEAR", "HEAT", "HECK", "HEEL", "HELD", "HELM",
    "HEMP", "HERD", "HERN", "HERR", "HESS", "HEWN", "HIBB", "HICK",
    "HIDE", "HILL", "HILT", "HIND", "HINE", "HINT", "HIRE", "HIRT",
    "HISE", "HISS", "HIST", "HITE", "HOAG", "HOAR", "HOAX", "HOEK",
    "HOGG", "HOLM", "HOLT", "HOME", "HONE", "HONG", "HONK", "HOOD",
    "HOOK", "HOOP", "HORA", "HORN", "HORR", "HOSS", "HOST", "HOWE",
    "HULL", "HUMP", "HUNT", "HURD", "HURT", "HUSE", "HYDE", "HYND",
    "JACK", "JAHN", "JAKE", "JANE", "JANN", "JANS", "JAPE", "JARD",
    "JARO", "JARR", "JARS", "JATO", "JAUN", "JAWN", "JAYE", "JEAN",
    "JOBE", "JOHN", "JOIN", "JONE", "JORY", "JOSE", "JOSS", "JOST",
    "JOVE", "JUDD", "JUNG", "JUNK", "JUST", "KALE", "KAMP", "KANE",
    "KARP", "KARR", "KEEN", "KEEL", "KEEP", "KELL", "KELP", "KEMP",
    "KERN", "KERR", "KEYS", "KIDD", "KILL", "KING", "KIPP", "KIRK",
    "KITE", "KLAR", "KNEE", "KNOB", "KNOW", "KNOX", "KOLB", "KONG",
    "KOOL", "KORD", "KOSS", "KREM", "KRON", "KROO", "LAKE", "LAMB",
    "LAMP", "LANE", "LANG", "LARK", "LARS", "LASH", "LASS", "LAST",
    "LATE", "LATH", "LAUD", "LAVE", "LAWN", "LAZE", "LEAK", "LEAN",
    "LEAP", "LEAR", "LEAT", "LECK", "LEFT", "LEHR", "LEIS", "LEND",
    "LENZ", "LERM", "LESS", "LEVY", "LEXA", "LICK", "LIDE", "LIME",
    "LINN", "LION", "LIST", "LITT", "LOAM", "LOAN", "LOCK", "LODE",
    "LOFT", "LOGE", "LOIN", "LOLA", "LONE", "LONG", "LOON", "LORE",
    "LOVE", "LOWE", "LOWN", "LUCK", "LUND", "LUNG", "LUNK", "LYNN",
    "MACK", "MAES", "MAHN", "MAIN", "MAKE", "MALE", "MALL", "MANE",
    "MANN", "MARE", "MARK", "MARR", "MARS", "MART", "MASH", "MASK",
    "MAST", "MATE", "MATH", "MAUL", "MAWN", "MAZE", "MEAD", "MEAL",
    "MEAN", "MEAR", "MECK", "MEES", "MELL", "MEMO", "MEND", "MENN",
    "MESA", "METZ", "MICE", "MIKE", "MILD", "MILE", "MILK", "MILL",
    "MIME", "MIND", "MINE", "MINK", "MINT", "MISS", "MIST", "MITT",
    "MOCK", "MODE", "MOKE", "MOLD", "MOLE", "MOLL", "MONK", "MOOD",
    "MOON", "MOOR", "MORE", "MORK", "MORN", "MORR", "MORT", "MOSS",
    "MOST", "MOTE", "MUCK", "MUDD", "MUIR", "MULE", "MULL", "MURK",
    "MURR", "MUSK", "MUSS", "MUST", "MUTT", "MYRA", "NAIL", "NALE",
    "NALL", "NALL", "NANCE", "NARD", "NARE", "NARK", "NARR", "NASH",
    "NASE", "NASR", "NAST", "NATE", "NAUL", "NAWN", "NAZE", "NEAB",
    "NEAL", "NEAP", "NEAR", "NEAT", "NECK", "NEEF", "NEEL", "NEEP",
    "NEIL", "NELL", "NELS", "NERD", "NERN", "NERR", "NESS", "NEST",
    "NETT", "NEVE", "NICK", "NIDE", "NILE", "NILL", "NIMB", "NINE",
    "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL",
    "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL",
    "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL", "NOEL",
    "REIN", "RENT", "RESS", "RHEA", "RICH", "RICK", "RIDE", "RIED",
    "RING", "RINK", "RION", "RISE", "RISK", "RIST", "RITE", "RITZ",
    "ROAD", "ROAN", "ROAR", "ROBB", "ROBE", "ROCK", "RODE", "ROLL",
    "ROME", "ROOF", "ROOM", "ROOT", "ROPE", "ROSE", "ROSS", "ROTH",
    "ROTT", "ROUS", "ROWE", "RUFF", "RULE", "RUSS", "RUST", "RYAL",
    "RYAN", "RYES", "SAGE", "SAHL", "SAIL", "SALE", "SALT", "SAME",
    "SAMP", "SAND", "SANE", "SANG", "SANK", "SARD", "SARK", "SASH",
    "SASS", "SATO", "SAUL", "SAVE", "SEAL", "SEAM", "SEAR", "SEAT",
    "SEED", "SEEK", "SEEM", "SEEN", "SEEP", "SELF", "SELL", "SEND",
    "SHAW", "SHAY", "SHED", "SHEP", "SHIP", "SHOE", "SHON", "SHOP",
    "SHOT", "SHOW", "SHUT", "SICK", "SIDE", "SILL", "SILO", "SIMS",
    "SING", "SINK", "SIRE", "SITE", "SIZE", "SKIN", "SKIP", "SLAB",
    "SLOE", "SLOP", "SLOT", "SLOW", "SLUG", "SMIT", "SNOB", "SNOW",
    "SOAP", "SOCK", "SOLE", "SONG", "SORE", "SORT", "SOUL", "SOUR",
    "SPAN", "SPAR", "SPIN", "SPIT", "SPOT", "STAN", "STAR", "STAY",
    "STEM", "STEP", "STEW", "STIR", "STOP", "STUB", "STUN", "SUCK",
    "SUMO", "SUNG", "SUNK", "SUNN", "SURF", "SURE", "SWAM", "SWAN",
    "TAPE", "TAPP", "TARR", "TASK", "TATE", "TEAM", "TEAR", "TEEM",
    "TEEN", "TELL", "TERM", "TERN", "TEST", "THAW", "THEM", "THEN",
    "THIN", "THOM", "THOR", "TIDE", "TILE", "TILL", "TILT", "TIME",
    "TINK", "TIRE", "TOLL", "TOMB", "TOME", "TONE", "TOOK", "TOOL",
    "TOON", "TORE", "TORN", "TORT", "TOSS", "TOUR", "TOWN", "TOYE",
    "TRAP", "TRAY", "TREE", "TRIM", "TRIP", "TROD", "TROY", "TRUE",
    "TUCK", "TUNE", "TURK", "TURN", "TUTT", "TYRE", "VALE", "VANE",
    "VANN", "VANT", "VARA", "VARK", "VARN", "VARS", "VAST", "VATE",
    "VAUD", "VEAL", "VEER", "VEIL", "VEIN", "VELL", "VEND", "VENN",
    "WADE", "WAHL", "WAIN", "WAKE", "WALD", "WALK", "WALL", "WARE",
    "WARN", "WARP", "WARR", "WART", "WATT", "WAVE", "WEAL", "WEEN",
    "WELD", "WELL", "WEND", "WENT", "WEST", "WILE", "WILL", "WILT",
    "WINN", "WIRE", "WISE", "WISH", "WITT", "WOLF", "WOOD", "WREN",
    "YORK", "YORE", "YOST", "YULE", "ZAHN", "ZALE", "ZANE", "ZAPP",
]


def check_separator_hypothesis():
    """
    Wenn '0' = Leerzeichen:
    Struktur: [Pos 0-3] [SP] [Pos 5] [SP] [Pos 7] [SP] [Pos 9-12]

    Constraints:
    - Vorname[0] (pos 0, Symbol A) == Nachname[2] (pos 11, Symbol A)
    - Vorname[2] (pos 2, Symbol N) == Nachname[1] (pos 10, Symbol N)
    - Initial2  (pos 7, Symbol M) == Nachname[3] (pos 12, Symbol M)
    """
    print("=== Separator-Hypothese: '0' = Leerzeichen ===")
    print("Struktur: VORNAME INITIAL1 INITIAL2 NACHNAME")
    print("          [0123]    [5]     [7]      [9-12]\n")
    print("Constraints:")
    print("  Vorname[0] == Nachname[2]  (Symbol A)")
    print("  Vorname[2] == Nachname[1]  (Symbol N)")
    print("  Initial2   == Nachname[3]  (Symbol M)")
    print()

    candidates = []

    # Alle 4-buchst. Vornamen durchprobieren
    for fname in set(FIRST_NAMES_4):
        if len(fname) != 4:
            continue

        # Constraint: Vorname[0] == Nachname[2]
        lname_pos2 = fname[0]
        # Constraint: Vorname[2] == Nachname[1]
        lname_pos1 = fname[2]

        # Suche passende Nachnamen
        for lname in set(LAST_NAMES_4):
            if len(lname) != 4:
                continue
            if lname[1] != lname_pos1:
                continue
            if lname[2] != lname_pos2:
                continue

            # Initial2 == Nachname[3]
            initial2 = lname[3]

            # Alle möglichen Initial1 (A-Z, muss sich von anderen unterscheiden)
            used_letters = set(fname) | set(lname) | {initial2}

            for initial1 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if initial1 in used_letters:
                    # Erlaubt, aber dann wäre es kein neues Symbol
                    # (bei echter homophoner Substitution könnten Buchstaben mehrfach vorkommen
                    # aber bei einfacher Substitution müssen alle Symbols unique Buchstaben sein)
                    pass

                # Prüfe ob alle 8 Symbole auf VERSCHIEDENE Buchstaben mappen
                mapping = {
                    'A': fname[0],  # pos 0, 11
                    'E': fname[1],  # pos 1
                    'N': fname[2],  # pos 2, 10
                    'z': fname[3],  # pos 3
                    '0': ' ',       # pos 4, 6, 8
                    'K': initial1,  # pos 5
                    'M': initial2,  # pos 7, 12
                    '[': lname[0],  # pos 9
                }

                # Alle Werte müssen einzigartig sein (strikte Substitution)
                values = list(mapping.values())
                if len(set(values)) != len(values):
                    continue  # Kollision

                # Dekodiere
                decoded = ''.join(mapping[c] for c in Z13)
                # Sollte sein: fname + ' ' + initial1 + ' ' + initial2 + ' ' + lname
                expected = f"{fname} {initial1} {initial2} {lname}"
                assert decoded == expected, f"{decoded} != {expected}"

                candidates.append({
                    'decoded': decoded,
                    'fname': fname,
                    'initial1': initial1,
                    'initial2': initial2,
                    'lname': lname,
                    'mapping': mapping,
                })

    print(f"Gefundene Kandidaten: {len(candidates)}\n")

    # Ausgabe (nach Vorname sortiert)
    candidates.sort(key=lambda x: (x['fname'], x['lname']))

    # Nur eindeutige Vor+Nachnamen-Kombinationen zeigen
    seen = set()
    unique_names = []
    for c in candidates:
        key = (c['fname'], c['lname'])
        if key not in seen:
            seen.add(key)
            # Füge Beispiel-Initial2 hinzu
            unique_names.append(c)

    print(f"Eindeutige Vor+Nachname-Paare: {len(unique_names)}\n")

    print("=== Alle Kandidaten (Vorname + Nachname) ===")
    for c in unique_names[:100]:
        print(f"  {c['fname']} ?. {c['initial2']}. {c['lname']}  "
              f"(Constraint: Vorname[0]={c['fname'][0]}, "
              f"Nachname[1]={c['lname'][1]}, Nachname[2]={c['lname'][2]})")

    return candidates


if __name__ == '__main__':
    candidates = check_separator_hypothesis()

    print("\n\n=== Variante: Nur 2 Wörter (kein Separator = kein Space) ===")
    print("Falls '0' KEIN Leerzeichen ist, sondern ein Buchstabe wie 'A' oder 'E':")
    print("Dann ist das gesamte 13-Zeichen-Ergebnis ein einzelner zusammenhängender Text")
    print(f"Mit dem Constraint-Muster: a-b-c-d-e-f-e-g-e-h-c-a-g")
    print("(wobei e an Positionen 4, 6, 8 immer denselben Buchstaben hat)")
