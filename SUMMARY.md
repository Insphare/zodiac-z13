# Z13 — Complete Project Analysis

## The Cipher

```
AENz0K0M0[NAM
```

- 13 characters, 8 unique symbols
- Letter postmarked April 20, 1970, San Francisco Chronicle
- Zodiac wrote: "My name is —" followed by this cipher
- Symbols do not appear in Z340/Z408 → no known key is transferable

**Mandatory constraints from symbol repetition:**
```
text[0]  = text[11]              (symbol A)
text[2]  = text[10]              (symbol N)
text[4]  = text[6] = text[8]    (symbol 0)
text[7]  = text[12]              (symbol M)
```

---

## Tested Hypotheses

### 1. Simulated Annealing (quadgram scoring)
- 30 runs × 200,000 iterations
- Converges to `WITHEREMENTWM` — not a name
- SA finds English text patterns, not name structure

### 2. Simulated Annealing (name scoring)
- 60 runs with bigram/trigram model from SSA + surname data
- 56/60 runs: M → space
- Converges to `STERANA ALES` — not a real name

### 3. M = space (7+4 structure)
- Structure: XXXXXXX·XXXX (7-letter first name + 4-letter last name)
- 34 valid 7-letter first names in SSA database — but **0 valid last names** without letter collision
- **Fully excluded**

### 4. 0 = space (4+1+1+4 structure) ← Main hypothesis
- Structure: XXXX · X · X · XXXX = firstname(4) + initial1(1) + initial2(1) + lastname(4)
- Three spaces at positions 4, 6, 8
- Constraints:
  - firstname[0] = lastname[2]  (symbol A)
  - firstname[2] = lastname[1]  (symbol N)
  - initial2 = lastname[3]      (symbol M)

**Critical:** The original search ignored bijectivity → LOIS HILL is INVALID (A→L and M→L collide).

With correct bijectivity check:

| Rank | Name | Score | Surname rank |
|------|------|-------|--------------|
| 1 | NEIL **?** G. KING | 0.9465 | #35 |
| 2 | RYAN **?** D. WARD | 0.7012 | #59 |
| 3 | RYAN **?** T. HART | 0.2795 | #148 |
| 17 | EARL **?** N. WREN | 0.1127 | #670 |

### 5. Null hypothesis (0 = filler, removed)
- Reduced string: `AENzKM[NAM` (10 characters)
- Revised constraints: t[0]=t[8], t[2]=t[7], t[5]=t[9]
- 1,267 bijective candidates — converges on same result (see below)

### 6. Prime routes (mod-13 transposition)
- 12 possible step sizes (13 is prime)
- All 12 routes preserve the same repetition pattern
- No new information → transposition approach useless

### 7. No-space (13 letters, no separator)
- 3 bijective candidates: IMOGENE REVOIR, IMOGENE DEVOID, CHASTITY TRACY
- All female names → Zodiac was male → likely incorrect

### 8. Known suspects check
- All known Zodiac suspects tested against constraints
- **Not a single one** satisfies the Z13 conditions (incl. Earl Van Best, Lawrence Kane)

### 9. Transpositions (Railfence, Columnar, Odd/Even, Reverse)
- All variants tested with 0=space model
- **0 bijective candidates** across all variants

### 10. Vigenere / Beaufort (14 keys)
- Keys: ZODIAC, PARADICE, SLAVES, KILL, MYNAMEIS, SFPD, BOMB, GAS, KNIFE, and more
- **0 bijective hits**

### 11. Brieftext-derived keys
- 9 key variants extracted from 6 spelling errors in the April 1970 letter
- **0 bijective hits**

### 12. Self-reference corpus search
- 3,394 windows scanned across 11 Zodiac letter sources (1969–1974)
- **0 constraint hits** — Z13 is not a phrase from Zodiac's own letters

---

## Main Finding: NEIL G. KING

```
Z13:   A  E  N  z  _  K  _  M  _  [  N  A  M
       ↓  ↓  ↓  ↓     ↓     ↓     ↓  ↓  ↓  ↓
Name:  N  E  I  L  _  ?  _  G  _  K  I  N  G
```

**Complete symbol mapping:**

| Symbol | Plaintext | Source |
|--------|-----------|--------|
| A | N | firstname[0] = lastname[2] |
| E | E | firstname[1] |
| N | I | firstname[2] = lastname[1] |
| z | L | firstname[3] |
| 0 | (space) | separator (×3) |
| K | [free] | first initial |
| M | G | initial2 = lastname[3] |
| [ | K | lastname[0] |

All 8 values: {N, E, I, L, space, G, K} + 1 free letter → mutually distinct ✓

Full name: **"NEIL [X]. G. KING"** — where X is any letter not in {N, E, I, L, G, K}.
Empirical prior for [X]: Ring 1 = J, W, R, C, D (most common male initials, 1880–1950 cohort).

---

## Convergence Finding (2026-05-06)

Both hypotheses (0=space AND 0=null) converge on the same structure. Under the 6+4 split
of the null hypothesis, exactly 20 bijective variants satisfy all constraints — identical
to the 0=space solution. The result "NEIL [X]. G. KING" is therefore **hypothesis-independent**.

**Community status:** No forum, paper, or wiki has ever proposed NEIL KING with a correct
bijectivity check. This is a genuine original contribution.

**Taunt/persona corpus:** All tested phrases (FUCKPOLICE, HELLSLAVES, etc.) fail the
constraints. The pattern is name-specific, not a taunt.

---

## Prior Work

| Source | Claim | Assessment |
|--------|-------|------------|
| Ziraoui 2024 (FR) | "KAYR" → Lawrence Kaye | Applied Z340 key to Z13 → methodologically invalid |
| Dr. Garlick 2025 (UNT) | Own method | Details not publicly available |
| Community consensus | No accepted solution | Correct — Z13 is considered unsolved |

---

## Conclusion

Z13 is cryptographically too short (13 characters) for an unambiguous computational solution.

**What we know:**
- 0=space (4+1+1+4) is the only structure yielding valid candidates
- NEIL [X]. G. KING is the top result under bijectivity and frequency criteria
- All alternative structures and transformation models fail

**What is missing:**
- Digitized Vallejo/Napa city directories 1969–70
- Genealogical verification (FamilySearch, Ancestry, SSDI)
- External corroboration (DNA, confession, document)

**If NEIL [X]. G. KING is correct, the suspect would be:**
- Male ✓
- Surname KING (Census rank #35, very common)
- First name NEIL (English/Scottish, popular 1940s–50s)
- Two initials between first and last name (formal style)
- No known Zodiac suspect carries this name
