# Ledger

Every claim this repo makes, with its standing. Nothing is removed from this file; a claim
that dies gets its death recorded under it, with what killed it. A claim reopens only by
citing its death and saying what the new attack does differently.

## Tags

| tag | meaning |
|---|---|
| **STANDARD** | textbook or published, with a citation we have checked against the source |
| **RECALL** | from a model's memory, not yet checked against a source; may be wrong in detail |
| **DERIVED** | computed in this repo from stated inputs; the script and its check are named |
| **STIPULATED** | a floor we chose on purpose, and say so; can be swapped out |
| **PROVISIONAL** | survived the checks we have run; not yet attacked by a breaker |
| **CONJECTURE** | a proposed explanation, with what it predicts and what would kill it |
| **OPEN** | a question no one here has an answer to |
| **DEAD** | killed; the entry says by what |

Where it matters, a claim also says whether it came from recall, inference, or a guess.

## Claims

### D1 — λ runs to approximately zero near M_Pl (STANDARD + DERIVED)
Three-loop literature: λ(M_Pl) = −0.0143 at 2013 central inputs, crossing zero near 10¹⁰ GeV,
β_λ ≈ 0 near 10¹⁷–10¹⁸ GeV (Buttazzo et al. 2013, checked 2026-10-31). Our one-loop run
reproduces the shape and misses the numbers by ~2× (see `01-datum/DATUM.md`). Standing:
the fact is STANDARD; our own reproduction is DERIVED at one loop only.

### D2 — the measured top mass is about 1 GeV above the stability edge (STANDARD, inputs RECALL)
Edge: M_t < 171.53 ± 0.42 GeV (three loop, 2013). Measured now ≈ 172.57 ± 0.29 (RECALL of
PDG-2024-era averages; to be pinned). ≈ 2σ from absolute stability. The 2013 paper quoted
2.8σ with M_t = 173.34; the measured value has moved toward the edge since.

### D3 — three parameters of the Higgs potential each sit near a critical value (RECALL of framing)
Quartic near the stability boundary; mass parameter near the electroweak critical point
(the hierarchy problem); constant term near zero (the cosmological constant problem).
Framing from Steingasser 2023/2024 (abstract checked). Whether "three edges" is one fact or
three unrelated ones is OPEN and is the first question in `QUESTIONS.md`.

### S1 — this repo's floor (STIPULATED)
We treat D1–D3 as a datum to be explained, not a coincidence to be shrugged at. This is a
choice. The alternative (it is a coincidence, or an anthropic selection) is a live candidate
in `03-candidates/` and is not excluded by taking this floor. If the breaker shows the
coincidence is unremarkable under a defensible prior, the floor comes out.

### P1 — the "edge" is prior-dependent and the prior has not been written down (PROVISIONAL)
"Near-critical" means close relative to some range. Nobody in this repo has yet stated the
range. `02-how-surprising/` exists to do that explicitly, with more than one prior, so the
number is honest about what it depends on.

### Q1 — one loop understates the closeness; two/three loops are required (DERIVED)
At one loop the edge is at M_t = 168.1 GeV, 3.4 GeV below the three-loop edge. Any session
quoting "how close" must use ≥ two loops or quote the literature. Regression target for the
implementer: λ(M_Pl) = −0.0143 at (M_t, M_h, α_s) = (173.34, 125.15, 0.1184).

### Q1 follow-up, 2026-10-31 — two loops implemented; gate passed (DERIVED)
`01-datum/rge_2loop.py` (beta functions transcribed from arXiv:1307.3536 appendix B off the
rendered PDF, not from memory) gives λ(M_Pl) = −0.0151 at (173.34, 125.15, 0.1184), against
the target −0.0143 ± 0.003: **PASS**, miss −0.0008. The slopes of eq. 61e (−0.0066, +0.0029,
+0.0018) come out −0.0065, +0.0028, +0.0019; g₁, g₂, g₃, y_t at M_Pl match eq. 61a–d to the
last digit or within one. With 2024-era inputs λ(M_Pl) = −0.0110 ± 0.0030 (Monte Carlo).
Running-coupling M_t edge: 170.96 GeV (2013 M_h, α_s), 0.57 GeV below the literature's
171.53 ± 0.42; the gap is part missing three-loop terms, part a difference of definition
(sign of running λ(μ) vs. sign of the effective potential λ_eff, see DATUM.md). Q1's rule
stands: quote the literature for the edge; this run can now be quoted for λ(M_Pl), its
slopes, and the shape. D1's standing moves from "DERIVED at one loop only" to "DERIVED at
two loops, within 0.001 of the three-loop literature". Not yet attacked by a breaker.

### C1 — multiple point criticality (CONJECTURE, Froggatt & Nielsen 1996)
Predicted M_h = 135 ± 9 GeV before measurement (RECALL). Says parameters sit at phase
boundaries because the vacuum is degenerate between phases. Predictions, kills, and status
in `03-candidates/multiple-point-criticality.md`.

### C2 — asymptotic safety of gravity (CONJECTURE, Shaposhnikov & Wetterich 2010)
Predicted M_h ≈ 126 GeV before measurement (RECALL). λ(M_Pl) ≈ 0 and β_λ ≈ 0 because the
Planck-scale theory sits at a UV fixed point where λ is irrelevant. `03-candidates/asymptotic-safety.md`.

### C3 — dynamical relaxation to criticality (CONJECTURE; "selfish Higgs" and relatives, 2020s)
A field scans parameters in the early universe and stops at a phase boundary.
`03-candidates/dynamical-selection.md`.

### C4 — anthropic / landscape selection (CONJECTURE)
We live where the vacuum lasts long enough; the edge is where most viable vacua sit.
`03-candidates/selection.md`.

### C0 — coincidence (the null)
Always listed. The breaker's job is to keep this alive as long as it deserves to be.
