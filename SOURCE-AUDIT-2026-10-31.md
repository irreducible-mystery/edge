# Sourcer audit — 2026-10-31

**Role: Sourcer (session issue-6).**

The audit requested by issue #6. Page numbers below refer to the journal pagination
unless identified as an arXiv PDF page. The source checks distinguish the values printed
in the papers from conclusions inferred by substituting those values into a fit.

| Claim | Source | Page / location | Verdict |
|---|---|---|---|
| The absolute-stability fit has slope 2.0 in \(M_t\). | Buttazzo et al., *JHEP* 12 (2013) 089, [arXiv:1307.3536](https://arxiv.org/abs/1307.3536) | arXiv PDF p. 19, Eq. (64) | **STANDARD.** Eq. (64) prints \(M_h > 129.6 + 2.0(M_t-173.34)-0.5(\alpha_s(M_Z)-0.1184)/0.0007\pm0.3\) GeV. |
| \(M_t<171.53\pm0.42\) GeV is the Eq. (64) edge at \(M_h=125.15\) GeV. | Buttazzo et al., same source | arXiv PDF p. 1 (input \(M_h=125.15\pm0.24\) GeV), p. 19 Eq. (64), p. 20 Eq. (66) | **CORRECTED.** Eq. (66) prints \(171.53\pm0.42\) GeV and says it rewrites Eq. (64), but does not state the central \(M_h\) used. At \(\alpha_s=0.1184\), substituting the paper's stated \(M_h=125.15\) into Eq. (64) gives \(M_t<171.115\) GeV. The Eq. (64) central fit would require \(M_h=125.98\) GeV to give 171.53 GeV. The paper does not explain this mismatch; do not identify Eq. (66) as the same-input equivalent of Eq. (64). |
| PDG 2024 inputs are \(M_t=172.57\pm0.29\) GeV, \(M_h=125.20\pm0.11\) GeV, and \(\alpha_s(M_Z)=0.1180\pm0.0009\). | S. Navas et al. (Particle Data Group), *Phys. Rev. D* 110, 030001 (2024); [top listing](https://pdg.lbl.gov/2024/listings/rpp2024-list-t-quark.pdf), [Higgs listing](https://pdg.lbl.gov/2024/listings/rpp2024-list-higgs-boson.pdf), [QCD review](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-qcd.pdf) | Top and Higgs listings, first-page mass entries; QCD review, Sec. 9 | **STANDARD.** These are the 2024-edition values used by the existing run outputs. The top value is a direct/reconstructed average, not a direct determination of the pole mass. |
| The current PDG inputs are the same as the 2024 values. | F. Takahashi et al. (Particle Data Group), [2026 Particle Properties](https://pdgweb.lbl.gov/2026/listings/particle_properties.html) | 2026 listings: top, Higgs, and QCD | **CORRECTED.** The 2026 release lists \(M_t=172.52\pm0.33\) GeV (direct/Monte-Carlo mass), \(M_h=125.10\pm0.14\) GeV, and \(\alpha_s(M_Z)=0.1179\pm0.0009\). The repository's checked-in numerical outputs remain the explicitly labeled 2024-input runs; they have not been regenerated with 2026 inputs. |
| Froggatt and Nielsen predicted \(M_h=135\pm9\) GeV. | Froggatt & Nielsen, “Standard Model Criticality Prediction: Top mass 173 ± 5 GeV and Higgs mass 135 ± 9 GeV,” *Phys. Lett. B* 368 (1996) 96–102, [hep-ph/9511371](https://arxiv.org/abs/hep-ph/9511371) | p. 96, abstract | **STANDARD.** The abstract states both \(M_t=173\pm5\) GeV and \(M_h=135\pm9\) GeV under the two-degenerate-vacua condition. |
| Shaposhnikov and Wetterich predicted a Higgs mass near 126 GeV. | Shaposhnikov & Wetterich, “Asymptotic safety of gravity and the Higgs boson mass,” *Phys. Lett. B* 683 (2010) 196–200, [arXiv:0912.0208](https://arxiv.org/abs/0912.0208) | arXiv PDF p. 1, abstract | **STANDARD, WITH QUALIFICATION.** The abstract says \(m_H=m_{\min}\simeq126\) GeV “with a few GeV uncertainty”; it does not give a numerical ± uncertainty. |
| Weinberg 1987 showed anthropic selection explains the small cosmological constant. | Weinberg, “Anthropic Bound on the Cosmological Constant,” *Phys. Rev. Lett.* 59 (1987) 2607–2610, [APS record](https://doi.org/10.1103/PhysRevLett.59.2607) | p. 2607, abstract | **OVERSTATED; PDF CHECK PENDING.** The publisher abstract describes an upper bound from avoiding suppression of gravitationally bound structures and says anthropic considerations may not explain the smallness of \(\Lambda\). The APS PDF returned HTTP 403 in this session, so the full paper was not checked; the related ledger claim remains RECALL pending that check. |

For comparison, solving Eq. (64) at the PDG 2026 central \(M_h\) and \(\alpha_s\) gives
\(M_t<170.91\) GeV. This is a calculation from the published linear fit, not a new
three-loop run; comparing it to the PDG direct/reconstructed top mass carries the
mass-definition caveat above.
