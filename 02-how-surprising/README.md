# How surprising is it?

Not yet computed. This directory answers QUESTIONS.md Q0 and decides LEDGER C0.

Deliverable: `surprise.py` producing a table of p = P(within δ of the stability boundary)
under at least three stated priors, with δ expressed in the top mass (currently ≈ 1.0 GeV
measured-minus-edge at three loops) and separately in λ(M_Pl). Report every prior; pick none.

Priors to include at minimum:
1. flat in M_h on (0, 700 GeV) with M_t fixed at measured — 700 is roughly the triviality
   bound where λ(M_t) would hit a Landau pole below M_Pl (RECALL; derive it in the script);
2. flat in λ(M_t) on (0, 4π);
3. flat in λ(M_Pl) on (−0.2, 0.2) — i.e. "the UV theory hands down a quartic of order the
   gauge couplings squared";
4. (breaker's choice) the prior that makes the coincidence look weakest, stated honestly.

The three-loop map from (M_h, M_t) to the stability boundary is needed for this; until
`rge_2loop.py` exists, use the literature's linear formula (DATUM.md, eq. 64/66) and say so.
