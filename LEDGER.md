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
### V1 — one-loop phase diagram in the (M_h, M_t) plane (DERIVED)
Computed 2026-10-31 by `01-datum/plot_phase.py` (Visual role). Absolute stability boundary
(where λ first reaches zero below M_Pl) at M_h = 125.2 GeV lies at M_t ≈ 168.1 GeV, matching
`results.json`. The measured point (125.20 ± 0.11, 172.57 ± 0.29) GeV sits in the metastable
region, ~4.5 GeV above the one-loop boundary (and ~1 GeV above the three-loop literature
boundary). Regions colored: stable (λ > 0 always), metastable (crosses but λ_min > −0.05),
unstable (λ_min < −0.05). The metastable/unstable split is a rough proxy for vacuum lifetime;
a proper bounce-action calculation is not yet in the repo. The three-loop literature band for
λ(μ) remains pending the co-creator's higher-loop implementation. Figure: `figures/phase_diagram.png`
(regenerated by the script).

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


### D1 / Q1 critic follow-up, 2026-10-31 — two-loop-audit (DERIVED + PROVISIONAL)
Reviewed two-loop-rge at `86191de74886d9ae817dcad303b5f08b0932bb66`, not main.
[Audit and reproduction](01-datum/AUDIT-2LOOP-2026-10-31.md): the actual --check run passes;
λ(M_Pl) = −0.015084551596325877, inside the ±0.003 gate. One-loop endpoint comparison:
5.55 × 10⁻¹⁷; doubling RK4 steps changes λ(M_Pl) by about 9.5 × 10⁻¹⁵.
Manual source comparison found no transcription mismatch in the λ and y_t two-loop brackets
against Appendix B equations 99 and 101 (PROVISIONAL implementation assessment).
Three open findings: F1, a deliberately failed literature gate still returns exit code 0;
F2, the branch's DATUM.md last-digit agreement claim overstates y_t agreement
(0.3832 versus 0.3825); F3, --check does not compare Monte Carlo, slopes, or the running
table with the recorded JSON. These qualify validation and reporting, not the reproduced
central λ result. No fixes or merges performed by this critic. Prior dependence and the
broader breaker brief remain open.

### P1 / S1 / C0 breaker follow-up, 2026-10-31 — prior-sweep (DERIVED + STIPULATED + INFERENCE)

Issue #5, base `83e737c60e97563fb63078794e06cb662f8bea2b`.
[`02-how-surprising/BREAK.md`](02-how-surprising/BREAK.md),
[`surprise.py`](02-how-surprising/surprise.py), and
[`surprise.json`](02-how-surprising/surprise.json) supply Q0's missing prior table.
With the repo's RECALL inputs, eq. 64 gives a potential-boundary distance of
1.572857 top-GeV. In the stated conditional local-linear model, p(boundary band)
is 0.008987755 for flat M_h in (0,700), 0.001031351 for flat lambda(M_t) in
(0,4 pi), 0.045612857 for flat lambda(M_Pl) in (-0.2,0.2), and 0.182451429 for
flat lambda(M_Pl) in (-0.05,0.05). All priors condition on M_t and alpha_s.
The geometric datum survives; the number expressing its surprise depends on
the prior. The separately reported UV-zero event is not the potential-boundary
event. These are not experimental p-values or a joint three-edge probability.

P1's "not yet stated" status is superseded by this dated computation. S1's
p>0.1 removal criterion is met **conditional on accepting the small-quartic UV
prior** (STIPULATED). Breaker's recommendation: withdraw a compulsory quartic
explanation on that assumption; no claim that the prior is uniquely correct,
or that m^2 and cosmological-constant problems have disappeared. S1's original
record is retained for the steward's decision. C0 remains live, but its own
retrospective freedom to choose priors is explicitly attacked in its file.
Only C0 had a candidate file at the base SHA; C1-C4 historical predictions were
not assessed. Look-elsewhere numbers are sensitivities, not a calibrated global p.
Validation: `python3 02-how-surprising/surprise.py --check` passes interval tests,
independent grid integration, and comparison of every recorded output field.

