#!/usr/bin/env python3
"""rge_1loop.py — run the Standard Model couplings from M_t to M_Planck at one loop.

The datum this repo starts from: with the measured Higgs and top masses, the Higgs
quartic coupling lambda runs to approximately zero near the Planck scale, and its
beta function is approximately zero there too. This script reproduces the SHAPE of
that at one loop, with a Monte Carlo over the input uncertainties, and prints the
numbers the ledger quotes.

Tier: DERIVED (one loop). The precise numbers in the literature are three-loop
(Buttazzo et al. 2013, arXiv:1307.3536); their eq. 61e, lambda(M_Pl) = -0.0143 at
central inputs, is the regression target a two/three-loop implementation must hit.
One loop is expected to miss it by some amount; the miss is recorded, not hidden.

Conventions: V = lambda (H^dag H)^2 - m^2 H^dag H, so m_h^2 = 2 lambda v^2 at tree
level. g_Y is the hypercharge coupling in SM normalization (not GUT-normalized g_1).
t = ln(mu / GeV). All one-loop beta functions are standard (e.g. Machacek & Vaughn
1983-85; any QFT textbook); 16 pi^2 d g / dt = ... as written in beta().

Inputs: MS-bar couplings at mu = M_t from Buttazzo et al. 2013 eqs. 55-60
(fetched and checked 2026-10-31; see 01-datum/DATUM.md for the exact expressions).

Usage:  python3 rge_1loop.py            # central values + Monte Carlo, writes results.json
        python3 rge_1loop.py --check    # exit 1 if the recorded numbers no longer reproduce
Standard library + numpy only.
"""
from __future__ import annotations
import json, math, sys
import numpy as np

PI2_16 = 16 * math.pi ** 2
M_PL = 1.2209e19          # reduced? no: this is the full Planck mass sqrt(hbar c / G); Buttazzo use M_Pl = 1.2209e19 GeV
LN_MPL = math.log(M_PL)

# --- inputs at mu = M_t (Buttazzo et al. 2013, eqs. 55-60), as functions of the measured masses
def inputs(Mt=173.34, Mh=125.15, a3=0.1184, MW=80.384):
    da3 = (a3 - 0.1184) / 0.0007
    dMW = (MW - 80.384) / 0.014
    lam = 0.12604 + 0.00206 * (Mh - 125.15) - 0.00004 * (Mt - 173.34)
    yt  = 0.93690 + 0.00556 * (Mt - 173.34) - 0.00042 * da3
    g3  = 1.1666  + 0.00314 * da3 - 0.00046 * (Mt - 173.34)
    g2  = 0.64779 + 0.00004 * (Mt - 173.34) + 0.00011 * dMW
    gY  = 0.35830 + 0.00011 * (Mt - 173.34) - 0.00020 * dMW
    return np.array([gY, g2, g3, yt, lam]), Mt

# --- one-loop beta functions, 16 pi^2 dg/dt
def beta(c):
    c = np.asarray(c, dtype=float)
    gY, g2, g3, yt, lam = (c[..., i] for i in range(5))
    b_gY = (41 / 6) * gY ** 3
    b_g2 = (-19 / 6) * g2 ** 3
    b_g3 = -7 * g3 ** 3
    b_yt = yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2 - (17 / 12) * gY ** 2)
    b_lam = (24 * lam ** 2 - 6 * yt ** 4
             + (3 / 8) * (2 * g2 ** 4 + (g2 ** 2 + gY ** 2) ** 2)
             + lam * (12 * yt ** 2 - 9 * g2 ** 2 - 3 * gY ** 2))
    return np.stack([b_gY, b_g2, b_g3, b_yt, b_lam], axis=-1) / PI2_16

def run(c0, t0, t1, n=800):
    """RK4 from ln mu = t0 to t1 (step ~0.05 in ln mu). c0 may be (5,) or (batch,5).
    Returns arrays of t and couplings, shape (n+1, ...)."""
    h = (t1 - t0) / n
    c = np.asarray(c0, dtype=float).copy()
    ts = np.empty(n + 1); cs = np.empty((n + 1,) + c.shape)
    t = t0
    ts[0], cs[0] = t, c
    for i in range(1, n + 1):
        k1 = beta(c); k2 = beta(c + 0.5 * h * k1)
        k3 = beta(c + 0.5 * h * k2); k4 = beta(c + h * k3)
        c = c + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4); t += h
        ts[i], cs[i] = t, c
    return ts, cs

def analyse(Mt=173.34, Mh=125.15, a3=0.1184):
    c0, mt = inputs(Mt, Mh, a3)
    ts, cs = run(c0, math.log(mt), LN_MPL)
    lam = cs[:, 4]
    betas = np.array([beta(c)[4] for c in cs])
    out = {}
    # scale where lambda first crosses zero (if it does)
    neg = np.where(lam < 0)[0]
    out["lambda_crosses_zero"] = bool(neg.size)
    out["log10_mu_zero_GeV"] = float(ts[neg[0]] / math.log(10)) if neg.size else None
    imin = int(np.argmin(lam))
    out["lambda_min"] = float(lam[imin]); out["log10_mu_lambda_min_GeV"] = float(ts[imin] / math.log(10))
    out["lambda_MPl"] = float(lam[-1]); out["beta_lambda_MPl"] = float(betas[-1])
    out["yt_MPl"] = float(cs[-1, 3]); out["g3_MPl"] = float(cs[-1, 2])
    out["lambda_Mt"] = float(c0[4]); out["yt_Mt"] = float(c0[3])
    return out, ts, cs

def analyse_batch(Mt, Mh, a3):
    """Vectorized analyse() over arrays of inputs; returns dict of arrays."""
    c0 = np.stack([inputs(m, h, a)[0] for m, h, a in zip(Mt, Mh, a3)])
    # all runs start at their own M_t; the spread (<1 GeV) is negligible on a log scale, start at the mean
    ts, cs = run(c0, math.log(float(np.mean(Mt))), LN_MPL)
    lam = cs[:, :, 4]
    crosses = (lam < 0).any(axis=0)
    first = np.where(crosses, np.argmax(lam < 0, axis=0), -1)
    return {"lambda_MPl": lam[-1], "crosses": crosses,
            "log10_mu_zero": np.where(crosses, ts[np.clip(first, 0, None)] / math.log(10), np.nan)}

def montecarlo(n=4000, seed=20261031, Mt=172.57, sMt=0.29, Mh=125.20, sMh=0.11, a3=0.1180, sa3=0.0009):
    """Draw the measured inputs (PDG-2024-era central values, see DATUM.md) and run each."""
    rng = np.random.default_rng(seed)
    b = analyse_batch(rng.normal(Mt, sMt, n), rng.normal(Mh, sMh, n), rng.normal(a3, sa3, n))
    lam_pl, crosses = b["lambda_MPl"], b["crosses"]
    return {
        "n": n, "seed": seed,
        "inputs": {"Mt": [Mt, sMt], "Mh": [Mh, sMh], "alpha_s": [a3, sa3]},
        "frac_lambda_negative_below_MPl": float(crosses.mean()),
        "lambda_MPl_mean": float(lam_pl.mean()), "lambda_MPl_sd": float(lam_pl.std()),
        "lambda_MPl_p05_p95": [float(np.percentile(lam_pl, 5)), float(np.percentile(lam_pl, 95))],
        "log10_mu_zero_median": float(np.nanmedian(b["log10_mu_zero"])) if crosses.any() else None,
    }

def main(argv):
    central_2013, ts, cs = analyse()                     # Buttazzo 2013 central inputs
    central_now, _, _ = analyse(172.57, 125.20, 0.1180)  # PDG-2024-era central inputs
    mc = montecarlo()
    # the stability edge in the top mass: bisect for the Mt at which lambda just touches zero below M_Pl
    lo, hi = 165.0, 180.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if analyse(mid, 125.20, 0.1180)[0]["lambda_crosses_zero"]: hi = mid
        else: lo = mid
    results = {
        "loop_order": 1,
        "central_2013_inputs": central_2013,
        "central_2024_inputs": central_now,
        "Mt_stability_edge_1loop_GeV": round(0.5 * (lo + hi), 3),
        "literature_3loop_edge_Mt_GeV": [171.53, 0.42],
        "literature_3loop_lambda_MPl_central_2013": -0.0143,
        "montecarlo": mc,
        "running_table": [[float(t / math.log(10)), float(c[4]), float(beta(c)[4])] for t, c in zip(ts[::400], cs[::400])],
    }
    if "--check" in argv:
        try:
            old = json.load(open("results.json"))
        except FileNotFoundError:
            print("no results.json to check against"); return 1
        keys = ["central_2013_inputs", "central_2024_inputs", "Mt_stability_edge_1loop_GeV"]
        bad = [k for k in keys if json.dumps(old[k], sort_keys=True) != json.dumps(results[k], sort_keys=True)]
        print("check", "ok" if not bad else "FAILED: " + ", ".join(bad)); return 1 if bad else 0
    json.dump(results, open("results.json", "w"), indent=1)
    p = lambda k, v: print(f"{k:44s} {v}")
    print("one-loop SM running, M_t -> M_Pl")
    for name, o in (("2013 central inputs (Mt 173.34, Mh 125.15)", central_2013), ("2024 central inputs (Mt 172.57, Mh 125.20)", central_now)):
        print(name)
        p("  lambda(M_t)", f"{o['lambda_Mt']:.5f}")
        p("  lambda crosses zero at log10(mu/GeV)", o["log10_mu_zero_GeV"] and f"{o['log10_mu_zero_GeV']:.2f}")
        p("  lambda minimum", f"{o['lambda_min']:.4f} at log10 mu = {o['log10_mu_lambda_min_GeV']:.2f}")
        p("  lambda(M_Pl)", f"{o['lambda_MPl']:.4f}   (3-loop literature, 2013 inputs: -0.0143)")
        p("  beta_lambda(M_Pl)", f"{o['beta_lambda_MPl']:.5f}")
    p("stability edge in Mt, one loop", f"{results['Mt_stability_edge_1loop_GeV']} GeV  (3-loop literature: 171.53 +- 0.42)")
    p("Monte Carlo: P(lambda<0 somewhere below M_Pl)", f"{mc['frac_lambda_negative_below_MPl']:.3f}")
    p("Monte Carlo: lambda(M_Pl) mean, sd", f"{mc['lambda_MPl_mean']:.4f}, {mc['lambda_MPl_sd']:.4f}")
    p("Monte Carlo: lambda(M_Pl) 5-95%", f"{mc['lambda_MPl_p05_p95'][0]:.4f} .. {mc['lambda_MPl_p05_p95'][1]:.4f}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
