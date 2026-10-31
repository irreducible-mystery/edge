#!/usr/bin/env python3
"""plot_lambda.py — lambda(mu) at one loop, central line plus a Monte Carlo band. Writes lambda_running.png."""
import math, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from rge_1loop import inputs, run, LN_MPL, analyse_batch
rng = np.random.default_rng(1)
n = 2000
Mt, Mh, a3 = rng.normal(172.57, 0.29, n), rng.normal(125.20, 0.11, n), rng.normal(0.1180, 0.0009, n)
c0 = np.stack([inputs(m, h, a)[0] for m, h, a in zip(Mt, Mh, a3)])
ts, cs = run(c0, math.log(172.57), LN_MPL)
lam = cs[:, :, 4]; x = ts / math.log(10)
lo, hi = np.percentile(lam, 5, axis=1), np.percentile(lam, 95, axis=1)
c, _ = inputs(172.57, 125.20, 0.1180); _, cc = run(c, math.log(172.57), LN_MPL)
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
ax.fill_between(x, lo, hi, color="#c9a86a", alpha=0.35, lw=0, label="5–95% band over $M_t$, $M_h$, $\\alpha_s$")
ax.plot(x, cc[:, 4], color="#4a3a1a", lw=1.6, label="central ($M_t$=172.57, $M_h$=125.20)")
ax.axhline(0, color="k", lw=0.6)
ax.axvline(math.log10(1.2209e19), color="k", lw=0.6, ls=":"); ax.text(19.0, 0.11, "$M_{Pl}$", ha="right")
ax.set_xlabel("$\\log_{10}(\\mu / \\mathrm{GeV})$"); ax.set_ylabel("Higgs quartic $\\lambda(\\mu)$")
ax.set_title("Standard Model, one loop: the quartic runs to the edge")
ax.set_xlim(2, 19.5); ax.set_ylim(-0.06, 0.14); ax.legend(frameon=False, fontsize=8)
ax.text(2.3, -0.05, "one-loop; three-loop literature puts $\\lambda(M_{Pl})\\approx-0.014$ and the\n$M_t$ edge at 171.5 GeV — see DATUM.md", fontsize=7.5, color="#555")
fig.tight_layout(); fig.savefig("../figures/lambda_running.png"); print("wrote ../figures/lambda_running.png")
