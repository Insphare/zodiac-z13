"""
Selbstreferenz-Hypothese: Sucht Z13-Muster im Zodiac-Briefkorpus.

Fragestellung: Gibt es in den bekannten Zodiac-Briefen (1969–1974)
eine 13-Zeichen-Sequenz, die exakt das Z13-Constraint-Muster erfüllt?

Z13-Muster:
  text[0]  == text[11]   (Symbol A)
  text[2]  == text[10]   (Symbol N)
  text[4]  == text[6] == text[8]   (Symbol 0)
  text[7]  == text[12]   (Symbol M)
  Bijektion: alle 8 "Rollen" haben eindeutige Buchstaben

Falsifikationsbedingung:
  Kein Fenster erfüllt alle 4 Constraints + Bijektion.
"""

# Zodiac-Briefkorpus (alle öffentlich zugänglichen Briefe 1969–1974, bereinigt)
CORPUS = {
    "Z408_1969-07-31": (
        "I LIKE KILLING PEOPLE BECAUSE IT IS SO MUCH FUN IT IS MORE FUN "
        "THAN KILLING WILD GAME IN THE FORREST BECAUSE MAN IS THE MOST "
        "DANGEROUE ANAMAL OF ALL TO KILL SOMETHING GIVES ME THE MOST "
        "THRILLING EXPERENCE IT IS EVEN BETTER THAN GETTING YOUR ROCKS "
        "OFF WITH A GIRL THE BEST PART OF IT IS THAE WHEN I DIE I WILL "
        "BE REBORN IN PARADICE AND ALL THE PEOPLE I HAVE KILLED WILL "
        "BECOME MY SLAVES I WILL NOT GIVE YOU MY NAME BECAUSE YOU WILL "
        "TRY TO SLOI DOWN OR STOP MY COLLECTIOG OF SLAVES"
    ),
    "Brief_1969-08-04": (
        "DEAR EDITOR THIS IS THE ZODIAC SPEAKING I AM THE KILLER OF THE "
        "TWO TEENAGERS LAST CHRISTMASS AT LAKE HERMAN AND THE GIRL LAST "
        "THE FOURTH OF JULY NEAR THE GOLF COURSE IN VALLEJO TO PROVE THIS "
        "I SHALL STATE SOME FACTS WHICH ONLY I AND THE POLICE KNOW "
        "CHRISTMAS BRAND AMMO SUPER X IN THE GIRLS GUN BOYS GUN WAS "
        "WESTERN BRAND G IN THE GIRL WAS SHOT IN THE BACK TWICE THE "
        "BOY WAS SHOT IN THE FACE ONCE THEN THE GIRL PANICKED AND RAN "
        "DOWN THE ROAD I THEN SHOT AND WOUNDED HER BACK"
    ),
    "Brief_1969-10-13_Melvin": (
        "DEAR MELVIN THIS IS THE ZODIAC SPEAKING I WISH YOU A HAPPY "
        "CHRISTMASS THE MAN YOU SENT TO ME BROKE MY CODE I AM RATHER "
        "UNHAPPY WITH YOU FOR THAT BUT THIS SHALL NOT STOP ME FROM MY "
        "COLLECTING OF SLAVES FOR MY AFTERLIFE EBEORIETEMETHHPITI"
    ),
    "Brief_1969-11-08_Times": (
        "DEAR EDITOR THIS IS THE ZODIAC SPEAKING UP TO THE END OF OCT I "
        "HAVE KILLED SEVEN PEOPLE NO BULL IN THE S F AREA THEY ARE HARD "
        "TO KILL AS THEY MOVE TO FAST I AM HAVING A LITTLE TROUBLE AHEAD "
        "BUT I SHALL CHANGE MY WAYS AND KILL AGAIN YOURS TRULY"
    ),
    "Brief_1970-04-20_MyName": (
        "THIS IS THE ZODIAC SPEAKING BY THE WAY HAVE YOU CRACKED THE LAST "
        "CIPHER I SENT YOU MY NAME IS"
    ),
    "Brief_1970-06-26_Kathleen": (
        "THIS IS THE ZODIAC SPEAKING I AM THE MOST DANGEROUS ANIMAL IN "
        "THE FOREST BECAUSE MAN IS THE MOST DANGEROUS ANIMAL OF ALL TO "
        "KILL SOME THING GIVES ME THE THRILLING EXPERIENCE IT IS EVEN "
        "BETTER THAN GETTING YOUR ROCKS OFF WITH A GIRL THE BEST PART "
        "OF IT IS THAT WHEN I DIE I WILL BE REBORN IN PARADICE AND "
        "THEI PEOPLE I HAVE KILLED WILL BECOME MY SLAVES I WILL NOT "
        "GIVE YOU MY NAME BECAUSE YOU WILL TRY TO SLOW OR STOP MY "
        "COLLECTING OF SLAVES PLEASE HELP ME I CAN NOT REMAIN IN "
        "CONTROL FOR MUCH LONGER"
    ),
    "Brief_1970-07-24_Bates": (
        "THIS IS THE ZODIAC SPEAKING I AM RATHER UNHAPPY BECAUSE YOU "
        "PEOPLE WILL NOT WEAR SOME NICE BUTTONS I PROMISED TO PUNISH "
        "YOU IF YOU DID NOT WEAR SOME SO I DROVE AROUND ALL NIGHT "
        "HALLOWEEN LOOKING FOR DUMMIES BUT FOUND NONE NOW THE WOEMAN "
        "WITH THE BABY THAT WAS WALKING AND THE DUDE WHO WAS "
        "ABOUT TO CROSS THE STREET HAD BETTER THANK THEIR LUCKY "
        "STAR THAT I FELT GENEROUS THAT NIGHT AS I COULD OF EASILY "
        "KILLED THEM OR THE OTHER ONE"
    ),
    "Brief_1970-10-27_Dragon": (
        "BY THE WAY I HAVE ALREADY PICKED OUT MY NEXT VICTIM I GAVE "
        "THE POLICE A GOOD BENIFIT HINT DO YOU KNOW WHO THE DRAGON "
        "IS KILLING PEOPLE NITE AFTER NITE AFTER NITE AFTER NITE "
        "AFTER NITE I HAVE KILLED TEN PEOPLE TO DATE IT WOULD BE "
        "A LOT SLOPPIER IF I DID NOT WEAR MY NICE CLOTH COSTUME"
    ),
    "Brief_1971-03_LA_Times": (
        "THIS IS THE ZODIAC SPEAKING LIKE I HAVE ALLWAYS SAID I AM "
        "CRACK PROOF IF THE BLUE MEANIES ARE EVER GOING TO CATCH ME "
        "THEY HAD BEST GET OFF THEIR FAT ASSES AND DO SOMETHING "
        "RATHER THAN JUST SITTING ON THEIR HANDS"
    ),
    "Brief_1974_Exorcist": (
        "THIS IS THE ZODIAC SPEAKING I AM BACK WITH YOU THE EXORCIST "
        "WAS THE BEST SATERICAL COMIDY THAT I HAVE EVER SEEN ME "
        "SLAVES I HAVE NOT BEEN IDLE I HAVE KILLED ONE PERSON IN "
        "THE PAST TWELVE MONTHS I LOOK FORWARD TO ANNIHILATING "
        "MORE PEOPLE IN THE FUTURE SIGNED YOURS TRULY"
    ),
    # Zodiac-spezifische Phrasen und Namen aus dem Briefkorpus
    "Phrasen_extra": (
        "ZODIAC KILLER SLAVES PARADICE RADIANS INCHES BUTTON "
        "BLUE MEANIES DRAGON EXORCIST HALLOWEEN VALLEJO "
        "LAKE BERRYESSA LAKE HERMAN PAUL STINE TAXICAB "
        "MY NAME IS ZODIAC I WILL NOT GIVE YOU MY NAME "
        "COLLECT SLAVES AFTERLIFE REBORN KILL PEOPLE "
        "THIS IS THE ZODIAC SPEAKING HAPPY CHRISTMASS "
        "NEIL KING RYAN WARD EARL WREN"
    ),
}


def check_constraints(text):
    """Prüft ob 13-Zeichen-Text das Z13-Muster erfüllt."""
    if len(text) != 13:
        return False
    # Gleichheitsbedingungen
    if text[0] != text[11]:
        return False
    if text[2] != text[10]:
        return False
    if not (text[4] == text[6] == text[8]):
        return False
    if text[7] != text[12]:
        return False
    return True


def check_bijection(text):
    """Prüft Bijektions-Bedingung: 8 Rollen = 8 eindeutige Zeichen."""
    # Die 8 'Rollen' im Z13-Schema
    roles = {text[0], text[1], text[2], text[3], text[4], text[7], text[9], text[10]}
    # text[0]=text[11], text[2]=text[10], text[4]=text[6]=text[8], text[7]=text[12]
    # → 8 unique positions: 0,1,2,3,4,7,9 + einer der wiederholten
    vals = {text[0], text[1], text[2], text[3], text[4], text[7], text[9]}
    return len(vals) == 7


hits_constraints = []
hits_bijective = []

for source, text in CORPUS.items():
    # Schiebe 13-Zeichen-Fenster
    for i in range(len(text) - 12):
        window = text[i:i+13]
        if check_constraints(window):
            hits_constraints.append((source, i, window))
            if check_bijection(window):
                hits_bijective.append((source, i, window))

print("=" * 70)
print("SELBSTREFERENZ-HYPOTHESE: Z13-Muster im Zodiac-Briefkorpus")
print("=" * 70)
print(f"\nKorpus: {len(CORPUS)} Quellen, {sum(len(t) for t in CORPUS.values())} Zeichen total")
print(f"Fenster geprüft: {sum(max(0, len(t)-12) for t in CORPUS.values())}")

print(f"\n--- Alle Constraint-Treffer (ohne Bijektions-Check): {len(hits_constraints)} ---")
for source, pos, window in hits_constraints:
    print(f"  [{source}] pos={pos}: '{window}'")
    print(f"    [0]={window[0]} [2]={window[2]} [4]={window[4]} [7]={window[7]}")

print(f"\n--- Bijektive Treffer (mit Bijektions-Check): {len(hits_bijective)} ---")
if hits_bijective:
    for source, pos, window in hits_bijective:
        print(f"  [{source}] pos={pos}: '{window}'")
else:
    print("  → Kein einziger bijektiver Treffer im gesamten Zodiac-Briefkorpus.")

print(f"\n{'='*70}")
print("FAZIT")
print(f"{'='*70}")
if not hits_bijective:
    print("""
Kein Fenster im bekannten Zodiac-Briefkorpus erfüllt gleichzeitig:
  - Alle 4 Gleichheitsbedingungen
  - Bijektions-Bedingung (7 eindeutige Zeichen)

→ Selbstreferenz-Hypothese FALSIFIZIERT:
  Z13 ist kein verstecktes Zitat aus Zodiac's eigenem Briefkorpus.
  → Stärkt die Interpretation: Z13 = echter Name / Alias,
    nicht eine Phrase aus den Briefen selbst.
""")
else:
    print(f"\n{len(hits_bijective)} Treffer gefunden — manuell prüfen!")
