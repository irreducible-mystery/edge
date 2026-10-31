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
| M_t at the stability edge | 168.1 GeV | 168.1 GeV | 171.53 ± 0.42 GeV |

Monte Carlo over M_t, M_h, α_s at 2024 central values (4000 draws): λ(M_Pl) = −0.029 ± 0.003,
and λ goes negative below M_Pl in 100% of draws at one loop.

**Read the table honestly.** One loop gets the *shape* right (λ falls through zero, bottoms
out just below the Planck scale with nearly zero slope, and stays small) and the *numbers*
wrong by a factor of two in λ(M_Pl) and by 3.4 GeV in the M_t edge. One loop makes the
coincidence look *weaker* than it is: at one loop the top would need to be 4.5 GeV lighter
for stability, at three loops only 1 GeV. The two- and three-loop terms matter, and the
regression target for whoever implements them is eq. 61e above: **−0.0143 at
(173.34, 125.15, 0.1184)**. Until a session hits that number, every quantitative claim in
this repo about "how close to the edge" rests on the literature, not on our own run.

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
