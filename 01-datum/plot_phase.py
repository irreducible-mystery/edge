#!/usr/bin/env python3
"""plot_phase.py — one-loop phase diagram in the (M_h, M_t) plane.

Computes the absolute-stability boundary (lambda never goes negative below M_Pl)
and a rough metastable/unstable boundary (min lambda < -0.05, approximating
short vacuum lifetime). Marks the measured point with its 1-sigma error ellipse.
Writes ../figures/phase_diagram.png.

Tier: DERIVED (one loop). The three-loop literature boundary is higher
(stability edge at M_t ~171.5 GeV for M_h=125); see DATUM.md.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from rge_1loop import inputs, run, LN_MPL

def classify(Mt, Mh, a3=0.1180):
    c0, mt = inputs(Mt, Mh, a3)
    ts, cs = run(c0, math.log(mt), LN_MPL)
    lam = cs[:, 4]
    crosses = np.any(lam < 0)
    lam_min = float(np.min(lam))
    # rough: unstable if deeply negative (lifetime << age of universe)
    # literature metastable/unstable boundary is near lambda_min ~ -0.05 or so
    if not crosses:
        return "stable", lam_min
    elif lam_min < -0.05:
        return "unstable", lam_min
    else:
        return "metastable", lam_min

# Grid
Mh_vals = np.linspace(120, 140, 21)  # coarser for speed
Mt_vals = np.linspace(160, 180, 21)
status = np.empty((len(Mt_vals), len(Mh_vals)), dtype=object)
lam_mins = np.empty((len(Mt_vals), len(Mh_vals)))

for i, Mt in enumerate(Mt_vals):
    for j, Mh in enumerate(Mh_vals):
        st, lmin = classify(Mt, Mh)
        status[i, j] = st
        lam_mins[i, j] = lmin
    print(f"done Mt={Mt:.1f}")

# Measured point (2024-era)
Mh_meas, sMh = 125.20, 0.11
Mt_meas, sMt = 172.57, 0.29

fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# Color map
colors = {"stable": "#2d6a4f", "metastable": "#e9c46a", "unstable": "#e76f51"}
for st, col in colors.items():
    mask = status == st
    ys, xs = np.where(mask)
    if len(xs):
        ax.scatter(Mh_vals[xs], Mt_vals[ys], c=col, s=40, alpha=0.7, label=st, marker="s")

# Stability boundary
boundary_Mt = []
for j, Mh in enumerate(Mh_vals):
    lo, hi = 160.0, 180.0
    for _ in range(15):
        mid = 0.5 * (lo + hi)
        st, _ = classify(mid, Mh)
        if st == "stable":
            lo = mid
        else:
            hi = mid
    boundary_Mt.append(0.5 * (lo + hi))
ax.plot(Mh_vals, boundary_Mt, "k-", lw=1.5, label="absolute stability boundary (1-loop)")

# Measured point + error ellipse
ax.errorbar(Mh_meas, Mt_meas, xerr=sMh, yerr=sMt, fmt="o", color="k", ms=6,
            label=f"measured ({Mh_meas:.2f}, {Mt_meas:.2f})")
ell = Ellipse((Mh_meas, Mt_meas), width=2*sMh, height=2*sMt,
              edgecolor="k", facecolor="none", lw=1.2)
ax.add_patch(ell)

ax.set_xlabel(r"$M_h$ (GeV)")
ax.set_ylabel(r"$M_t$ (GeV)")
ax.set_title("One-loop SM vacuum phase diagram in the $(M_h, M_t)$ plane")
ax.set_xlim(120, 140)
ax.set_ylim(160, 180)
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.text(121, 161, "DERIVED at one loop. 3-loop literature moves the\nstability boundary up by ~3.4 GeV in $M_t$.\nMetastable/unstable split is approximate ($\\lambda_{\\rm min}<-0.05$).",
        fontsize=7, color="#333", va="bottom")
fig.tight_layout()
fig.savefig("../figures/phase_diagram.png")
print("wrote ../figures/phase_diagram.png")
print(f"Stability boundary at Mh=125.2: Mt ~ {np.interp(125.2, Mh_vals, boundary_Mt):.2f} GeV")
