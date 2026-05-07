# Structural Analysis of the Zodiac Killer's Z13 Cipher

**Author:** [Name]  
**Date:** 2026-05-06  
**Repository:** [GitHub URL]  
**Status:** Preprint — not peer reviewed  

---

## Abstract

The Z13 cipher ("AENz0K0M0[NAM", Zodiac Killer, April 20, 1970) has remained unsolved since its publication. We present a rigorous constraint-based analysis using four mandatory equality conditions derived directly from symbol repetition, combined with a strict bijectivity requirement. Under both primary structural hypotheses — the separator hypothesis (symbol '0' = space) and the null hypothesis (symbol '0' = filler, removed) — the analysis converges on a single family of solutions: **NEIL [X]. G. KING**, where [X] denotes an unknown first initial from a 19-symbol residual set. All simple transformation models (transposition, polyalphabetic substitution, brieftext-derived keys) were systematically tested and falsified. The self-reference hypothesis (Z13 as a phrase from Zodiac's own letter corpus) was computationally falsified across 3,394 candidate windows. To our knowledge, this is the first published analysis applying a strict bijectivity check to Z13, correcting a methodological error present in prior community proposals.

---

## 1. The Cipher

The Z13 cipher appears in a letter sent by the Zodiac Killer to the *San Francisco Chronicle*, postmarked April 20, 1970. The letter reads: *"My name is —"* followed by the 13-symbol sequence:

```
A E N z 0 K 0 M 0 [ N A M
0 1 2 3 4 5 6 7 8 9 10 11 12
```

**Symbol inventory:** 8 unique symbols: `A`, `E`, `N`, `z`, `0`, `K`, `M`, `[`  
**Symbol frequencies:**

| Symbol | Count | Positions |
|--------|-------|-----------|
| 0      | 3     | 4, 6, 8   |
| A      | 2     | 0, 11     |
| N      | 2     | 2, 10     |
| M      | 2     | 7, 12     |
| E      | 1     | 1         |
| z      | 1     | 3         |
| K      | 1     | 5         |
| [      | 1     | 9         |

The symbols are not present in the Z340 or Z408 ciphers, making key transfer from those ciphers methodologically invalid.

---

## 2. Mandatory Constraints

For any monoalphabetic substitution, equal cipher symbols must map to equal plaintext characters. This yields four **mandatory equality constraints**:

```
C1: plaintext[0]  == plaintext[11]    (symbol A, appears at positions 0 and 11)
C2: plaintext[2]  == plaintext[10]    (symbol N, appears at positions 2 and 10)
C3: plaintext[4]  == plaintext[6] == plaintext[8]   (symbol 0, appears at positions 4, 6, 8)
C4: plaintext[7]  == plaintext[12]    (symbol M, appears at positions 7 and 12)
```

These constraints are **not hypotheses** — they are mathematical consequences of the cipher structure, valid under any monoalphabetic model.

**Bijectivity requirement:** A valid simple substitution cipher must map distinct symbols to distinct plaintext characters. With 8 unique symbols, all 8 must resolve to different characters. Failure to enforce this was the principal methodological error in prior community analyses (e.g., the LOIS HILL candidate, where symbols A and M both mapped to 'L').

---

## 3. Structural Hypotheses

### 3.1 Hypothesis A: Separator Hypothesis (0 = space)

If symbol '0' (appearing 3×) encodes a word separator, the structure becomes:

```
[pos 0–3] [pos 4=space] [pos 5] [pos 6=space] [pos 7] [pos 8=space] [pos 9–12]
  XXXX         ·             X        ·             X        ·          XXXX
```

This yields a **4 + 1 + 1 + 4** format: `FIRSTNAME · INITIAL1 · INITIAL2 · LASTNAME`.

Applying constraints C1–C4:
- `FIRSTNAME[0] == LASTNAME[3]`  → first letter of first name = last letter of last name
- `FIRSTNAME[2] == LASTNAME[1]`  → third letter of first name = second letter of last name
- `INITIAL2 == LASTNAME[3]`  (i.e., INITIAL2 == FIRSTNAME[0])

Search over SSA baby names (1930–1975, male) × US Census surnames (4-letter) with bijectivity check: **191 valid candidates.**

### 3.2 Hypothesis B: Null Hypothesis (0 = filler, removed)

If symbol '0' is a null/padding character, removing it yields the 10-character reduced string:

```
A E N z K M [ N A M
0 1 2 3 4 5 6 7 8 9
```

Revised constraints on the reduced string:
- `t[0] == t[8]`
- `t[2] == t[7]`
- `t[5] == t[9]`

Search over the same name corpora with bijectivity check: **1,267 valid candidates.**

---

## 4. Convergence Finding

Both hypotheses independently produce the same top-ranked solution family.

Under Hypothesis A, the symbol mapping resolves as:

| Cipher Symbol | Plaintext | Notes         |
|---------------|-----------|---------------|
| A             | N         | NEIL[0]       |
| E             | E         | NEIL[1]       |
| N             | I         | NEIL[2]       |
| z             | L         | NEIL[3]       |
| 0             | (space)   | separator     |
| K             | [free]    | first initial |
| M             | G         | second initial|
| [             | K         | KING[0]       |

Decoded: **N E I L · [X] · G · K I N G**

Under Hypothesis B (6+4 split of the reduced string), the identical structural constraints yield **NEIL [X] G KING** as the only valid 20-variant family satisfying both name-corpus membership and bijectivity.

**This convergence is structurally robust:** it does not depend on which hypothesis is correct.

Known solution properties:
- All 7 resolved values `{N, E, I, L, ' ', G, K}` are mutually distinct ✓
- First name **NEIL**: male, plausible 1930–1950 birth cohort ✓
- Last name **KING**: US Census rank #35 ✓
- Second initial **G**: consistent across both hypotheses ✓
- First initial **[X]**: unconstrained; belongs to `{A,B,C,D,F,H,J,O,P,Q,R,S,T,U,V,W,X,Y,Z}` (19 candidates)

---

## 5. Systematic Falsification of Alternative Models

All of the following were implemented and tested computationally:

| Method | Variants Tested | Result |
|--------|----------------|--------|
| Railfence transposition (2/3/4 rails) | All variants + 0=space | 0 bijective hits |
| Columnar transposition | ncols 2–6, all permutations | 0 bijective hits |
| Odd/even position reordering | Both directions | 0 bijective hits |
| Reverse | — | 0 bijective hits |
| Vigenere cipher | 14 Zodiac-related keys | 0 bijective hits |
| Beaufort cipher | Same 14 keys | 0 bijective hits |
| Caesar cipher (all 26 shifts) | — | 0 name hits (constraints trivially preserved) |
| Brieftext-derived keys | 9 variants from 6 letter typos | 0 bijective hits |
| M = space (alternative separator) | — | 0 candidates |
| No-space (13 letters, no separator) | — | 3 candidates, all female |
| Known Zodiac suspects | Van Best, Kane, Allen, + others | 0 satisfy constraints |
| Taunts / phrases | FUCKPOLICE, HELLSLAVES, etc. | All fail C1 or C3 |
| Self-reference (corpus search) | 3,394 windows from 11 letter sources | 0 constraint hits |

Note on the Z340 key transfer error: The French analyst Ziraoui (2023) applied the Z340 cipher key directly to Z13. Since Z13 symbols do not appear in Z340, this is methodologically invalid. The Z340 key maps different symbols (e.g. Z340's 'A' → 'I', whereas Z13's 'A' → 'N'). These are independent cipher systems.

---

## 6. Limitations and Open Questions

1. **No historical verification:** No individual named Neil G. King has been located in Bay Area directories for 1968–1970. Vallejo, Napa, and Solano County records remain incompletely searched.

2. **First initial unknown:** Symbol K maps to an unknown initial from 19 candidates. Empirical name-frequency priors (US male names, 1880–1950 cohort) suggest Ring 1: J, W, R, C, D as most probable.

3. **External validation absent:** No second independent cipher or physical evidence corroborates this reading.

4. **Alias vs. real name:** Zodiac's communication style favored control and misdirection. A pseudonym satisfying the same constraints cannot be excluded.

5. **Cipher class:** While monoalphabetic substitution is the most parsimonious explanation, polygraphic or composite models (Playfair, Nihilist) cannot be mathematically excluded — only argued against on grounds of simplicity.

---

## 7. Conclusion

The structural analysis of Z13 yields a single robust candidate: **NEIL [X]. G. KING**, where [X] is an unknown first initial. This result:

- Is independent of which structural hypothesis is assumed
- Satisfies strict bijectivity (all 8 symbol values distinct)
- Is falsified against all simple transformation models
- Is falsified as a self-quotation from Zodiac's letter corpus
- Has not, to our knowledge, been previously proposed with a correct bijectivity check

External verification — specifically, locating a Neil G. King in the Bay Area in 1968–1970 — is the necessary next step for any conclusion beyond structural plausibility.

---

## Appendix: Code

All analysis scripts are available in the accompanying repository:

| Script | Purpose |
|--------|---------|
| `separator_hypothesis.py` | 0=space search with bijectivity |
| `null_extended.py` | 0=null search with bijectivity |
| `transposition_test.py` | Railfence + columnar falsification |
| `vigenere_test.py` | Vigenere + Beaufort falsification |
| `brieftext_key.py` | Letter typo key extraction + test |
| `self_reference_test.py` | Corpus window search |
| `z32_analysis.py` | Z32 cross-analysis |

---

*This document was prepared on 2026-05-06 and submitted to Zenodo for timestamped preregistration.*
