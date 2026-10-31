# The datum: the Higgs quartic runs to approximately zero near the Planck scale

This is the fact the whole repo starts from. Everything here is tier-tagged; see
[`../LEDGER.md`](../LEDGER.md) for the tags and the standing of each claim.

## What is measured (STANDARD; values fetched 2026-10-31)

MS-bar couplings at μ = M_t, from Buttazzo, Degrassi, Giardino, Giudice, Sala, Salvio,
Strumia, *Investigating the near-criticality of the Higgs boson*, JHEP 2013,
arXiv:1307.3536, eqs. 55–60 (two-loop matching; checked against the paper's PDF text
on 2026-10-31, superscripts reconstructed by the fetch tool, so a session with the PDF
in hand should re-verify once):

```
λ(M_t)  = 0.12604 + 0.00206 (M_h − 125.15) − 0.00004 (M_t − 173.34)            ± 0.00030
y_t(M_t)= 0.93690 + 0.00556 (M_t − 173.34) − 0.00042 (α_s − 0.1184)/0.0007     ± 0.00050
g_3(M_t)= 1.1666  + 0.00314 (α_s − 0.1184)/0.0007 − 0.00046 (M_t − 173.34)
g_2(M_t)= 0.64779 + 0.00004 (M_t − 173.34) + 0.00011 (M_W − 80.384)/0.014
g_Y(M_t)= 0.35830 + 0.00011 (M_t − 173.34) − 0.00020 (M_W − 80.384)/0.014
```
(masses in GeV; V = λ(H†H)² convention, m_h² = 2λv² at tree level.)

Their three-loop result at central 2013 inputs (eq. 61e):

```
λ(M_Pl) = −0.0143 − 0.0066 (M_t − 173.34) + 0.0018 (α_s − 0.1184)/0.0007 + 0.0029 (M_h − 125.15)
```
with λ crossing zero near 10¹⁰ GeV and β_λ vanishing near 10¹⁷–10¹⁸ GeV. Absolute
stability up to M_Pl requires M_h > 129.6 ± 1.5 GeV, equivalently M_t < 171.53 ± 0.42 GeV
(eqs. 65–66). With 2013 inputs they quote stability excluded at 2.8σ.

Inputs since 2013 (RECALL, PDG-2024-era; a session should pin these to the current PDG
or the latest world averages and record the source): M_t ≈ 172.57 ± 0.29 GeV (the world
average has moved *down* about 0.8 GeV since 2013), M_h = 125.20 ± 0.11 GeV,
α_s(M_Z) = 0.1180 ± 0.0009. With these, the measured top is about 1.0 GeV above the
three-loop stability edge, roughly 2σ combining the measurement and the edge's error.
**The edge got closer as the measurements improved.** That is worth noticing and is not
yet explained by anything in this repo.

> **Correction (2026-10-31, sourcer, PR #9; the two paragraphs above stay as written).** Eq. 64 gives
> the stability fit; Eq. 65 reports M_h > 129.6 ± 1.5 GeV, and Eq. 66 prints
> M_t < 171.53 ± 0.42 GeV. **They are not equivalent at the same stated inputs.** The
> paper lists M_h = 125.15 ± 0.24 GeV and α_s = 0.1184; substituting those central values
> into Eq. 64 gives M_t < 171.115 GeV, not 171.53 GeV. Eq. 66 does not state which
> central M_h it used. The Eq. 64 fit would imply M_h = 125.98 GeV at M_t = 171.53 GeV
> and central α_s. Do not compare the Eq. 66 number directly with a run at M_h = 125.15.
> See the [source audit](../SOURCE-AUDIT-2026-10-31.md).
> >
> > The PDG 2024 inputs used by the checked-in RGE outputs are M_t = 172.57 ± 0.29 GeV,
> M_h = 125.20 ± 0.11 GeV, and α_s(M_Z) = 0.1180 ± 0.0009; these are now sourced to the
> 2024 PDG edition. The latest PDG 2026 values are M_t = 172.52 ± 0.33 GeV (direct/
> reconstructed mass), M_h = 125.10 ± 0.14 GeV, and α_s(M_Z) = 0.1179 ± 0.0009. The
> existing outputs below remain 2024-input results, not current-input recalculations.
> Using Eq. 64 with the PDG 2026 Higgs and strong-coupling central values gives a
> same-input top-mass edge of 170.91 GeV, about 1.61 GeV below the PDG direct/
> reconstructed top-mass central value. Because the measured direct mass is not itself a
> direct pole-mass determination, that difference is a comparison with an explicit
> mass-definition caveat, not a new significance estimate.

## What this repo has reproduced so far (DERIVED, one loop)

`rge_1loop.py` runs the five couplings from M_t to M_Pl = 1.2209 × 10¹⁹ GeV with one-loop
beta functions and RK4, from the inputs above. Output of the 2026-10-31 run
(`results.json`; `python3 rge_1loop.py --check` re-derives and compares):

| quantity | one loop, 2013 inputs | one loop, 2024 inputs | three-loop literature (2013 inputs) |
|---|---|---|---|
| λ crosses zero at log₁₀(μ/GeV) | 7.97 | 8.37 | ≈ 10 |
| λ minimum | −0.0341 at 10^17.6 | −0.0297 at 10^17.8 | (not quoted; small negative) |
| λ(M_Pl) | −0.0337 | −0.0294 | −0.0143 |
| β_λ(M_Pl) | +0.00022 | +0.00018 | ≈ 0 near 10^17–10^18 |
| M_t at the stability edge | 168.1 GeV | 168.1 GeV | 171.53 ± 0.42 GeV (as first written; corrected 2026-10-31: 171.12 GeV from eq. 64 at M_h 125.15, α_s 0.1184; eq. 66's 171.53 is at an unstated M_h) |

Monte Carlo over M_t, M_h, α_s at 2024 central values (4000 draws): λ(M_Pl) = −0.029 ± 0.003,
and λ goes negative below M_Pl in 100% of draws at one loop.

**Read the table honestly.** One loop gets the *shape* right (λ falls through zero, bottoms
out just below the Planck scale with nearly zero slope, and stays small) and the *numbers*
wrong by a factor of two in λ(M_Pl) and by 3.4 GeV in the M_t edge. One loop makes the
coincidence look *weaker* than it is: at one loop the top would need to be 4.5 GeV lighter
for stability, at three loops only 1 GeV. The two- and three-loop terms matter, and the
(Corrected 2026-10-31, PR #9: against eq. 64 at matched inputs the one-loop miss is about 3.0 GeV, and the measured top would need to be about 1.6 GeV lighter, not 1 GeV.) The
regression target for whoever implements them is eq. 61e above: **−0.0143 at
(173.34, 125.15, 0.1184)**. Until a session hits that number, every quantitative claim in
this repo about "how close to the edge" rests on the literature, not on our own run.

## Two loops (DERIVED, added 2026-10-31; the paragraph above is left as written)

`rge_2loop.py` adds the two-loop terms, transcribed from appendix B of arXiv:1307.3536
(eqs. 96–99, 101–103) off the rendered PDF pages, with the bottom and tau Yukawas carried
along as the paper does. Same inputs, same RK4, same interface. `python3 rge_2loop.py --check`
re-derives the numbers below and also confirms that with the two-loop terms switched off it
reproduces `rge_1loop.py` to 10⁻¹⁶. Output of the 2026-10-31 run (`results_2loop.json`):

| quantity | one loop, 2013 inputs | **two loops, 2013 inputs** | three-loop literature (2013 inputs) | **two loops, 2024 inputs** |
|---|---|---|---|---|
| λ crosses zero at log₁₀(μ/GeV) | 7.97 | **9.69** | ≈ 10 | **10.51** |
| λ minimum | −0.0341 at 10^17.6 | **−0.0155 at 10^17.4** | (small negative) | **−0.0113 at 10^17.6** |
| λ(M_Pl) | −0.0337 | **−0.0151** | −0.0143 | **−0.0110** |
| β_λ = 0 at log₁₀(μ/GeV) | 17.6 | **17.4** | ≈ 17–18 | **17.5** |
| ∂λ(M_Pl)/∂M_t per GeV | −0.0068 | **−0.0065** | −0.0066 | — |
| ∂λ(M_Pl)/∂M_h per GeV | +0.0025 | **+0.0028** | +0.0029 | — |
| ∂λ(M_Pl)/∂α_s per 0.0007 | +0.0019 | **+0.0019** | +0.0018 | — |
| g₁, g₂, g₃, y_t at M_Pl | — | **0.6153, 0.5054, 0.4873, 0.3832** | 0.6154, 0.5055, 0.4873, 0.3825 | — |
| M_t at the stability edge | 168.1 GeV | **170.96 GeV** (M_h 125.15, α_s 0.1184) | 171.53 ± 0.42 GeV (as first written; corrected 2026-10-31: **171.12 GeV** from eq. 64 at M_h 125.15, α_s 0.1184) | **170.83 GeV** (M_h 125.20, α_s 0.1180) |
| M_h at the stability edge | — | **130.07 GeV** (M_t 173.34) | 129.6 ± 1.5 GeV | — |

Monte Carlo over M_t, M_h, α_s at 2024 central values (4000 draws, same seed as the one-loop
run): λ(M_Pl) = −0.0110 ± 0.0030, 5–95% range −0.0162 to −0.0061; λ goes negative below M_Pl
in 100% of draws.

**Gate (ROLES.md item 1, LEDGER Q1): PASS.** λ(M_Pl) = −0.0151 at (173.34, 125.15, 0.1184),
0.0008 below the three-loop value, inside the ±0.003 tolerance. The three slopes in eq. 61e
and the four other couplings at M_Pl (eq. 61a–d) are reproduced to the last quoted digit or
within one unit of it. The light Yukawas move λ(M_Pl) by −6 × 10⁻⁶; they do not matter here.

**Read this table honestly too.** Two things remain between this run and the literature:

1. The residual −0.0008 in λ(M_Pl) is the size expected for the missing three-loop terms
   and is in the direction expected (three-loop terms in β_λ are known to be small and to
   push λ(M_Pl) up slightly; INFERENCE from the sign of the miss, not checked against the
   three-loop coefficients, which are in eq. 99 and could be added by a later session).
2. The M_t edge comes out 0.57 GeV below the literature's 171.53, outside its ±0.42. Part of
   that is the missing loop (the slope −0.0065/GeV turns a λ(M_Pl) shift of 0.0008 into
   (Corrected 2026-10-31, PR #9: eq. 66's 171.53 is at an unstated M_h; against eq. 64 at the
   same M_h and α_s, 171.115, this edge is 0.16 GeV low.)
   ≈ 0.12 GeV). The rest is a **difference in definition**: this script calls the vacuum
   unstable if the MS-bar running λ(μ) is negative anywhere below M_Pl, whereas eqs. 64–66
   use the effective potential λ_eff(h) of their eq. 63 and appendix C, which differs from
   λ(μ = h) by one- and two-loop finite pieces (eq. 104; their size at high scales is
   RECALL, order 10⁻³, and should be computed, not assumed). The edge in this table is therefore the *running-coupling* edge, not the *potential* edge,
   and the two should not be compared to better than ~0.5 GeV. A session that implements
   eq. 104 (λ_eff at one or two loops) would close that gap; until then, quote the literature
   for the edge and this run for everything else.

With the 2024-era inputs, the measured top (172.57) sits 1.7 GeV above this run's
running-coupling edge (170.83) and about 1.0 GeV above the literature's potential edge. Either
way, two loops confirms what one loop understated: the edge is closer than the one-loop table
makes it look, by about 3 GeV in M_t.
(Corrected 2026-10-31, PR #9: against eq. 64 at matched PDG-2024 inputs, 170.997 GeV, the
measured top is about 1.6 GeV above the literature fit, not 1.0 GeV.)

## Three edges, not one (RECALL of the literature's framing; STIPULATED as this repo's framing)

The Higgs potential has three parameters, and each one sits near a critical value
(Steingasser, *Higgs criticality in and beyond the Standard Model*, arXiv:2405.02415,
lecture at Corfu 2023, abstract fetched 2026-10-31):

1. **The quartic λ** runs to ≈ 0 near M_Pl: the boundary between a stable and a metastable
   electroweak vacuum. This file.
2. **The mass parameter m²**: the electroweak scale is 10⁻¹⁷ of the Planck scale, which is
   the statement that m² sits almost exactly at the critical point of the electroweak phase
   transition when measured in Planck units. This is the hierarchy problem restated as a
   criticality.
3. **The constant term** (the cosmological constant): 10⁻¹²² in Planck units, sitting at the
   boundary between a universe that collapses and one that empties out.

One near-critical parameter is a coincidence. Three, in one potential, is a pattern or a
selection effect. Deciding which is the question of this repo.
