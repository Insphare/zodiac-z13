# zodiac-z13

Structural analysis of the Zodiac Killer's unsolved Z13 cipher.

## The Cipher

The Z13 cipher appears in a letter sent by the Zodiac Killer to the *San Francisco Chronicle*, postmarked **April 20, 1970**. The letter reads: *"My name is —"* followed by:

```
A E N z 0 K 0 M 0 [ N A M
```

13 characters, 8 unique symbols. Unsolved since 1970.

## Key Finding

Both primary structural hypotheses independently converge on the same solution family:

> **NEIL [X]. G. KING**

where [X] is an unknown first initial (19 candidates remain; empirical prior suggests J, W, R, C, D).

Symbol mapping: `A→N, E→E, N→I, z→L, 0→(space), K→[free], M→G, [→K`

This result satisfies strict bijectivity (all 8 symbol values are mutually distinct) and is independent of which structural hypothesis is assumed.

## Methodology

Four mandatory equality constraints are derived directly from symbol repetition:

```
plaintext[0]  == plaintext[11]                    (symbol A)
plaintext[2]  == plaintext[10]                    (symbol N)
plaintext[4]  == plaintext[6] == plaintext[8]     (symbol 0)
plaintext[7]  == plaintext[12]                    (symbol M)
```

These are mathematical consequences of the cipher structure — not hypotheses.

All candidate names are filtered against:
- SSA baby names database (1930–1975, male)
- US Census surname database
- Strict bijectivity check (all 8 symbols map to distinct characters)

## Falsified Approaches

| Method | Result |
|--------|--------|
| Railfence / Columnar transposition | 0 hits |
| Vigenere / Beaufort (14 keys) | 0 hits |
| Caesar (all 26 shifts) | 0 name hits |
| Brieftext-derived keys | 0 hits |
| Known Zodiac suspects | 0 satisfy constraints |
| Self-reference corpus search (3,394 windows) | 0 hits |

See `ZENODO_PAPER.md` for the full analysis.

## Scripts

| File | Purpose |
|------|---------|
| `separator_hypothesis.py` | 0=space search with bijectivity |
| `null_extended.py` | 0=null search with bijectivity |
| `transposition_test.py` | Railfence + columnar falsification |
| `vigenere_test.py` | Vigenere + Beaufort falsification |
| `brieftext_key.py` | Letter typo key extraction + test |
| `self_reference_test.py` | Corpus window search |
| `z32_analysis.py` | Z32 cross-analysis |

## Status

- [x] Constraint analysis implemented
- [x] Bijectivity check enforced
- [x] All simple transformation models falsified
- [x] Self-reference hypothesis falsified
- [ ] Historical verification pending (Neil G. King, Bay Area 1968–1970)
- [ ] Zenodo DOI pending

## License

MIT
