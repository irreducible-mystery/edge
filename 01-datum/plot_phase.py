#!/usr/bin/env python3
"""plot_phase.py — phase diagram in the (M_h, M_t) plane, one loop and two loops.

Left panel is the one-loop result (the previous figure). Right panel swaps in
rge_2loop.run at two loops, same inputs, same definition of the regions.
Both panels are contourf of lambda_min on one vectorised grid (the same batching
as analyse_batch), not a scatter of markers.

Regions, from that grid:
  stable      lambda stays non-negative up to M_Pl          (lambda_min >= 0)
  metastable  lambda crosses zero, but not deeply           (-0.05 <= lambda_min < 0)
  unstable    lambda_min < -0.05

The -0.05 cut is a proxy for vacuum lifetime, not a convention and not a computed
bounce. RECALL: the tunnelling rate goes as exp(-8 pi^2 / (3|lambda|)) at the scale
where lambda is most negative, and a lifetime longer than the age of the universe
works out to |lambda| less than or about 0.05-0.06. The dashed contour is that
estimate drawn on the same grid; it is not a second calculation.

The absolute-stability boundary drawn on each panel is the lambda_min = 0 contour
of the same grid. A bisection in M_t at M_h = 125.2 GeV (analyse(), one trajectory
at a time) is printed as a check on that contour and is not plotted over it.

The measured point is an axis-aligned ellipse with semi-axes equal to the quoted
1-sigma uncertainties, taken as uncorrelated. No error bar: the ellipse is the
uncertainty.

alpha_s is fixed at 0.1180 (the 2024-era central value used in results.json).
Its uncertainty is not on the ellipse.

Tier: DERIVED. Writes ../figures/phase_diagram.png.
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Patch

import rge_1loop
import rge_2loop

A3 = 0.1180
MH_MEAS, S_MH = 125.20, 0.11
MT_MEAS, S_MT = 172.57, 0.29
# unstable / metastable / stable — same colours as the one-loop scatter
REGION_COLORS = ["#e76f51", "#e9c46a", "#2d6a4f"]
LAM_SPLIT = -0.05


def lambda_min_grid(mod, Mh_vals, Mt_vals, loops=None):
    """Min of lambda(mu) on [M_t, M_Pl] for every (M_h, M_t). Shape (n_Mt, n_Mh)."""
    MH, MT = np.meshgrid(Mh_vals, Mt_vals)
    c0 = np.stack([mod.inputs(float(m), float(h), A3)[0]
                   for m, h in zip(MT.ravel(), MH.ravel())])
    kw = {} if loops is None else {"loops": loops}
    # One start for the batch, as in analyse_batch. The M_t spread is checked
    # against a true-start bisection at the end of this script.
    _, cs = mod.run(c0, math.log(float(np.mean(Mt_vals))), mod.LN_MPL, **kw)
    return cs[:, :, 4].min(axis=0).reshape(MT.shape)


def column_at_Mh(Mh_vals, lam, Mh):
    j = int(np.searchsorted(Mh_vals, Mh))
    j = min(max(j, 1), len(Mh_vals) - 1)
    w = (Mh - Mh_vals[j - 1]) / (Mh_vals[j] - Mh_vals[j - 1])
    return (1.0 - w) * lam[:, j - 1] + w * lam[:, j]


def zero_crossing(Mt_vals, column):
    """M_t where column, ordered in increasing M_t, crosses from >=0 to <0."""
    positive = column >= 0.0
    flips = np.where(positive[:-1] & ~positive[1:])[0]
    if flips.size == 0:
        return float("nan")
    i = int(flips[0])
    y0, y1 = float(column[i]), float(column[i + 1])
    frac = 0.0 if y0 == y1 else y0 / (y0 - y1)
    return float(Mt_vals[i] + frac * (Mt_vals[i + 1] - Mt_vals[i]))


def bisect_Mt(analyse, Mh, lo=160.0, hi=180.0, steps=30):
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if analyse(mid)["lambda_crosses_zero"]:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def draw(ax, Mh_vals, Mt_vals, lam, levels, title, edge_Mt):
    cf = ax.contourf(Mh_vals, Mt_vals, lam, levels=levels,
                     cmap=ListedColormap(REGION_COLORS), extend="neither")
    ax.contour(Mh_vals, Mt_vals, lam, levels=[0.0], colors="#1a1a1a", linewidths=1.05)
    ax.contour(Mh_vals, Mt_vals, lam, levels=[LAM_SPLIT], colors="#1a1a1a",
               linewidths=0.75, linestyles="--")
    ell = Ellipse((MH_MEAS, MT_MEAS), width=2 * S_MH, height=2 * S_MT,
                  edgecolor="white", facecolor="none", lw=1.7, zorder=5)
    ax.add_patch(ell)
    ell = Ellipse((MH_MEAS, MT_MEAS), width=2 * S_MH, height=2 * S_MT,
                  edgecolor="#1a1a1a", facecolor="none", lw=0.85, zorder=6)
    ax.add_patch(ell)
    ax.plot(MH_MEAS, MT_MEAS, "o", ms=4.2, color="white", zorder=7)
    ax.plot(MH_MEAS, MT_MEAS, "o", ms=2.2, color="#1a1a1a", zorder=8)
    ax.set_xlim(Mh_vals[0], Mh_vals[-1])
    ax.set_ylim(Mt_vals[0], Mt_vals[-1])
    ax.set_xlabel(r"$M_h$ (GeV)")
    ax.set_title(title, loc="left", fontsize=11, pad=8)
    # lower right is the stable region on both panels: uniform, away from the
    # measured point and from both contours
    ax.text(139.3, 161.15,
            f"edge at $M_h=125.2$:\n$M_t={edge_Mt:.2f}$ GeV",
            ha="right", va="bottom", color="white", fontsize=8)
    return cf


def main():
    Mh_vals = np.linspace(120.0, 140.0, 81)
    Mt_vals = np.linspace(160.0, 180.0, 81)

    lam1 = lambda_min_grid(rge_1loop, Mh_vals, Mt_vals)
    lam2 = lambda_min_grid(rge_2loop, Mh_vals, Mt_vals, loops=2)

    edge1_contour = zero_crossing(Mt_vals, column_at_Mh(Mh_vals, lam1, 125.2))
    edge2_contour = zero_crossing(Mt_vals, column_at_Mh(Mh_vals, lam2, 125.2))
    edge1 = bisect_Mt(lambda Mt: rge_1loop.analyse(Mt, 125.2, A3)[0], 125.2)
    edge2 = bisect_Mt(lambda Mt: rge_2loop.analyse(Mt, 125.2, A3, loops=2)[0], 125.2)

    # shared breaks so a colour is the same claim on both panels
    lo = min(float(lam1.min()), float(lam2.min()), LAM_SPLIT) - 1e-6
    hi = max(float(lam1.max()), float(lam2.max()), 0.0) + 1e-6
    levels = [lo, LAM_SPLIT, 0.0, hi]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.55), dpi=160, sharey=True)
    draw(axes[0], Mh_vals, Mt_vals, lam1, levels, "one loop", edge1)
    draw(axes[1], Mh_vals, Mt_vals, lam2, levels, "two loops", edge2)
    axes[0].set_ylabel(r"$M_t$ (GeV)")

    handles = [
        Patch(facecolor=REGION_COLORS[2], edgecolor="none", label="stable"),
        Patch(facecolor=REGION_COLORS[1], edgecolor="none", label="metastable"),
        Patch(facecolor=REGION_COLORS[0], edgecolor="none", label="unstable"),
        Line2D([0], [0], linestyle="none", marker="o", markerfacecolor="none",
               markeredgecolor="#1a1a1a", markeredgewidth=1.2, markersize=8,
               label="measured, 1σ"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, 0.012), fontsize=9)
    fig.suptitle(r"Standard Model vacuum in the $(M_h, M_t)$ plane", fontsize=13, y=0.975)
    fig.text(0.5, 0.915,
             r"$\alpha_s=0.1180$ fixed.  "
             r"Solid line: $\lambda_{\min}=0$.  Dashed: $\lambda_{\min}=-0.05$, "
             r"a lifetime proxy (see the script docstring), not a computed bounce.",
             ha="center", va="center", fontsize=7.5, color="#333333")
    fig.subplots_adjust(left=0.07, right=0.985, top=0.84, bottom=0.18, wspace=0.08)

    out = "../figures/phase_diagram.png"
    fig.savefig(out)
    print(f"wrote {out}")
    print(f"one-loop  contour  Mh=125.2: Mt = {edge1_contour:.4f} GeV")
    print(f"one-loop  bisection Mh=125.2: Mt = {edge1:.4f} GeV   |diff| = {abs(edge1 - edge1_contour):.4f}")
    print(f"two-loop  contour  Mh=125.2: Mt = {edge2_contour:.4f} GeV")
    print(f"two-loop  bisection Mh=125.2: Mt = {edge2:.4f} GeV   |diff| = {abs(edge2 - edge2_contour):.4f}")
    print(f"measured Mt is {MT_MEAS - edge1:.2f} GeV above the one-loop edge")
    print(f"measured Mt is {MT_MEAS - edge2:.2f} GeV above the two-loop edge")
    # the contour is the figure; if it disagrees with the bisection the grid is too coarse
    if not (abs(edge1 - edge1_contour) < 0.15 and abs(edge2 - edge2_contour) < 0.15):
        raise SystemExit("contour and bisection disagree by >= 0.15 GeV; not writing a ledger number from this grid")


if __name__ == "__main__":
    main()
