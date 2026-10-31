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

## Breaker result, 2026-10-31 — prior-sweep

The brief above is retained as written. The computation is now in
[`surprise.py`](surprise.py), its complete output in [`surprise.json`](surprise.json),
and the argument and limitations in [`BREAK.md`](BREAK.md).

**DERIVED in the stated local model:** delta_t = 1.572857 GeV for the repo's
inputs. The four conditional prior probabilities are 0.008987755, 0.001031351,
0.045612857, and 0.182451429. All priors condition on M_t and alpha_s. The
small-quartic UV prior crosses the issue's 0.1 threshold; whether it is accepted
is the explicit remaining assumption. The UV-zero event is reported separately.
The 700 GeV support is preserved as a prior choice, not justified as a
Planck-valid triviality bound; the script includes a scalar-only diagnostic.

```sh
python3 02-how-surprising/surprise.py
python3 02-how-surprising/surprise.py --check
```

