#!/usr/bin/env python3
"""rge_2loop.py — run the Standard Model couplings from M_t to M_Planck at two loops.

Same interface as rge_1loop.py (inputs / beta / run / analyse / analyse_batch / montecarlo,
--check self-test), with the two-loop terms added and the small bottom and tau Yukawas
carried along, as Buttazzo et al. do.

Tier: DERIVED (two loops). Regression target set in ROLES.md / LEDGER Q1: lambda(M_Pl) at
(M_t, M_h, alpha_s) = (173.34, 125.15, 0.1184) must land within 0.003 of -0.0143, the
three-loop literature value (arXiv:1307.3536 eq. 61e). Whatever number comes out is recorded
in results_2loop.json and printed; the gate is reported as PASS or FAIL, never hidden.

Source of the beta functions: Buttazzo, Degrassi, Giardino, Giudice, Sala, Salvio, Strumia,
JHEP 12 (2013) 089, arXiv:1307.3536, appendix B, eqs. 96-99 and 101-103, transcribed on
2026-10-31 from the rendered PDF pages (36-39), not from memory. The paper writes
d g^2 / d ln mu^2 and d lambda / d ln mu^2 in GUT normalisation g_1^2 = (5/3) g_Y^2; this
file converts to d g / d ln mu and keeps g_Y in SM normalisation at the interface so that
rge_1loop.py and plot_lambda.py can be swapped for it. The one-loop pieces, after conversion,
agree term by term with rge_1loop.py; the two-loop lambda and y_t pieces were also checked
against the g_Y-normalised forms in Degrassi et al. 2012 (arXiv:1205.6497) from recall.
`--loops 1` must reproduce rge_1loop.py (with the light Yukawas off); `--check` tests this.

Conventions: V = lambda (H^dag H)^2 - m^2 H^dag H, m_h^2 = 2 lambda v^2 at tree level.
t = ln(mu / GeV). State vector: [g_Y, g_2, g_3, y_t, lambda, y_b, y_tau]; index 4 is lambda,
as in the one-loop script.

Inputs at mu = M_t: eqs. 55-60 of the same paper (two-loop matching, plus 3-loop QCD for y_t
and g_3), as in rge_1loop.py. The paper does not print y_b(M_t) and y_tau(M_t); it says they
come from m_b(m_b) = 4.2 GeV and M_tau = 1.777 GeV. The values used here, y_b = 0.0162 and
y_tau = 0.0100, are RECALL (m_b(M_t) ~ 2.8 GeV, m_tau(M_t) ~ 1.74 GeV, y = sqrt(2) m / 246.22).
Their effect on lambda(M_Pl) is computed and printed (--no-light-yukawas) so the reader can
see it is below the fourth decimal.

Usage:  python3 rge_2loop.py                 # central values + Monte Carlo, writes results_2loop.json
        python3 rge_2loop.py --check         # exit 1 if results_2loop.json no longer reproduces,
                                             #   or if --loops 1 disagrees with rge_1loop.py
        python3 rge_2loop.py --loops 1       # one-loop terms only (for the comparison)
        python3 rge_2loop.py --no-light-yukawas
Standard library + numpy only.
"""
from __future__ import annotations
import json, math, sys
import numpy as np

K1 = 1.0 / (16 * math.pi ** 2)          # 1/(4 pi)^2
K2 = K1 * K1                             # 1/(4 pi)^4
M_PL = 1.2209e19                         # GeV; Buttazzo et al. use M_Pl ~ 1.2e19 (their sec. 5), same as rge_1loop.py
LN_MPL = math.log(M_PL)
S53 = math.sqrt(5.0 / 3.0)               # g_1 (GUT) = S53 * g_Y

GATE_TARGET, GATE_TOL = -0.0143, 0.003   # LEDGER Q1 / ROLES.md item 1
# Buttazzo et al. eq. 61a-e, central 2013 inputs, three-loop running. 61a is g_1 in GUT normalisation.
LIT_MPL_3LOOP = {"g1_GUT": 0.6154, "g2": 0.5055, "g3": 0.4873, "yt": 0.3825, "lambda": -0.0143}

# --- inputs at mu = M_t (Buttazzo et al. 2013, eqs. 55-60), as functions of the measured masses
def inputs(Mt=173.34, Mh=125.15, a3=0.1184, MW=80.384, light_yukawas=True):
    da3 = (a3 - 0.1184) / 0.0007
    dMW = (MW - 80.384) / 0.014
    lam = 0.12604 + 0.00206 * (Mh - 125.15) - 0.00004 * (Mt - 173.34)
    yt  = 0.93690 + 0.00556 * (Mt - 173.34) - 0.00042 * da3
    g3  = 1.1666  + 0.00314 * da3 - 0.00046 * (Mt - 173.34)
    g2  = 0.64779 + 0.00004 * (Mt - 173.34) + 0.00011 * dMW
    gY  = 0.35830 + 0.00011 * (Mt - 173.34) - 0.00020 * dMW
    yb, ytau = (0.0162, 0.0100) if light_yukawas else (0.0, 0.0)   # RECALL, see docstring
    return np.array([gY, g2, g3, yt, lam, yb, ytau]), Mt

# --- beta functions, d c / d ln mu, one and two loops
def beta(c, loops=2):
    """c has shape (..., 7) = [g_Y, g_2, g_3, y_t, lambda, y_b, y_tau]. Returns d c / d ln mu.

    Transcribed from arXiv:1307.3536 appendix B. The paper gives B_X = d X^2 / d ln mu^2 for the
    gauge and Yukawa couplings and B_lam = d lambda / d ln mu^2, in terms of g_1^2 = 5 g_Y^2 / 3.
    Conversions: d g / d ln mu = B_g / g ;  d lambda / d ln mu = 2 B_lam ;  d g_Y / d ln mu
    = sqrt(3/5) d g_1 / d ln mu.
    """
    c = np.asarray(c, dtype=float)
    gY, g2, g3, yt, lam, yb, ytau = (c[..., i] for i in range(7))
    g1 = S53 * gY
    g1s, g2s, g3s = g1 ** 2, g2 ** 2, g3 ** 2
    yts, ybs, yas = yt ** 2, yb ** 2, ytau ** 2

    # ---- one loop (eqs. 96-99, 101-103, first bracket) ----
    B_g1 = g1s ** 2 * K1 * (41 / 10)
    B_g2 = g2s ** 2 * K1 * (-19 / 6)
    B_g3 = g3s ** 2 * K1 * (-7)
    B_yt = yts * K1 * (4.5 * yts + 1.5 * ybs + yas - 8 * g3s - 2.25 * g2s - (17 / 20) * g1s)
    B_yb = ybs * K1 * (1.5 * yts + 4.5 * ybs + yas - 8 * g3s - 2.25 * g2s - 0.25 * g1s)
    B_ya = yas * K1 * (3 * yts + 3 * ybs + 2.5 * yas - 2.25 * g2s - 2.25 * g1s)
    B_lam = K1 * (lam * (12 * lam + 6 * yts + 6 * ybs + 2 * yas - 4.5 * g2s - 0.9 * g1s)
                  - 3 * yts ** 2 - 3 * ybs ** 2 - yas ** 2
                  + (9 / 16) * g2s ** 2 + (27 / 400) * g1s ** 2 + (9 / 40) * g2s * g1s)

    if loops >= 2:
        # ---- two loop (second bracket of each equation) ----
        B_g1 = B_g1 + g1s ** 2 * K2 * ((44 / 5) * g3s + (27 / 10) * g2s + (199 / 50) * g1s
                                       - (17 / 10) * yts - 0.5 * ybs - 1.5 * yas)
        B_g2 = B_g2 + g2s ** 2 * K2 * (12 * g3s + (35 / 6) * g2s + (9 / 10) * g1s
                                       - 1.5 * yts - 1.5 * ybs - 0.5 * yas)
        B_g3 = B_g3 + g3s ** 2 * K2 * (-26 * g3s + 4.5 * g2s + (11 / 10) * g1s - 2 * yts - 2 * ybs)
        B_yt = B_yt + yts * K2 * (
            yts * (-12 * yts - (11 / 4) * ybs - (9 / 4) * yas - 12 * lam + 36 * g3s + (225 / 16) * g2s + (393 / 80) * g1s)
            + ybs * (-0.25 * ybs + 1.25 * yas + 4 * g3s + (99 / 16) * g2s + (7 / 80) * g1s)
            + yas * (-2.25 * yas + (15 / 8) * g2s + (15 / 8) * g1s)
            + 6 * lam ** 2 - 108 * g3s ** 2 - (23 / 4) * g2s ** 2 + (1187 / 600) * g1s ** 2
            + 9 * g3s * g2s + (19 / 15) * g3s * g1s - (9 / 20) * g2s * g1s)
        B_yb = B_yb + ybs * K2 * (
            yts * (-0.25 * yts - (11 / 4) * ybs + 1.25 * yas + 4 * g3s + (99 / 16) * g2s + (91 / 80) * g1s)
            + ybs * (-12 * ybs - 2.25 * yas - 12 * lam + 36 * g3s + (225 / 16) * g2s + (237 / 80) * g1s)
            + yas * (-2.25 * yas + (15 / 8) * g2s + (15 / 8) * g1s)
            + 6 * lam ** 2 - 108 * g3s ** 2 - (23 / 4) * g2s ** 2 - (127 / 600) * g1s ** 2
            + 9 * g3s * g2s + (31 / 15) * g3s * g1s - (27 / 20) * g2s * g1s)
        B_ya = B_ya + yas * K2 * (
            6 * lam ** 2 - (23 / 4) * g2s ** 2 + (1371 / 200) * g1s ** 2 + (27 / 20) * g2s * g1s
            + yts * (-(27 / 4) * yts + 1.5 * ybs - (27 / 4) * yas + 20 * g3s + (45 / 8) * g2s + (17 / 8) * g1s)
            + ybs * (-(27 / 4) * ybs - (27 / 4) * yas + 20 * g3s + (45 / 8) * g2s + (5 / 8) * g1s)
            + yas * (-3 * yas - 12 * lam + (165 / 16) * g2s + (537 / 80) * g1s))
        B_lam = B_lam + K2 * (
            lam ** 2 * (-156 * lam - 72 * yts - 72 * ybs - 24 * yas + 54 * g2s + (54 / 5) * g1s)
            + lam * yts * (-1.5 * yts - 21 * ybs + 40 * g3s + (45 / 4) * g2s + (17 / 4) * g1s)
            + lam * ybs * (-1.5 * ybs + 40 * g3s + (45 / 4) * g2s + (5 / 4) * g1s)
            + lam * yas * (-0.5 * yas + (15 / 4) * g2s + (15 / 4) * g1s)
            + lam * (-(73 / 16) * g2s ** 2 + (1887 / 400) * g1s ** 2 + (117 / 40) * g2s * g1s)
            + yts ** 2 * (15 * yts - 3 * ybs - 16 * g3s - 0.8 * g1s)
            + yts * (-(9 / 8) * g2s ** 2 - (171 / 200) * g1s ** 2 + (63 / 20) * g2s * g1s)
            + ybs ** 2 * (-3 * yts + 15 * ybs - 16 * g3s + 0.4 * g1s)
            + ybs * (-(9 / 8) * g2s ** 2 + (9 / 40) * g1s ** 2 + (27 / 20) * g2s * g1s)
            + yas ** 2 * (5 * yas - 1.2 * g1s)
            + yas * (-(3 / 8) * g2s ** 2 - (9 / 8) * g1s ** 2 + (33 / 20) * g2s * g1s)
            + (305 / 32) * g2s ** 3 - (3411 / 4000) * g1s ** 3
            - (289 / 160) * g2s ** 2 * g1s - (1677 / 800) * g2s * g1s ** 2)

    # convert d X^2 / d ln mu^2 -> d X / d ln mu, and g_1 -> g_Y
    with np.errstate(divide="ignore", invalid="ignore"):
        d_gY = np.where(gY != 0, B_g1 / g1, 0.0) / S53
        d_g2 = B_g2 / g2
        d_g3 = B_g3 / g3
        d_yt = B_yt / yt
        d_yb = np.where(yb != 0, B_yb / np.where(yb != 0, yb, 1.0), 0.0)
        d_ya = np.where(ytau != 0, B_ya / np.where(ytau != 0, ytau, 1.0), 0.0)
    d_lam = 2.0 * B_lam
    return np.stack([d_gY, d_g2, d_g3, d_yt, d_lam, d_yb, d_ya], axis=-1)

def run(c0, t0, t1, n=800, loops=2):
    """RK4 from ln mu = t0 to t1 (step ~0.05 in ln mu). c0 may be (7,) or (batch,7)."""
    h = (t1 - t0) / n
    c = np.asarray(c0, dtype=float).copy()
    ts = np.empty(n + 1); cs = np.empty((n + 1,) + c.shape)
    t = t0
    ts[0], cs[0] = t, c
    for i in range(1, n + 1):
        k1 = beta(c, loops); k2 = beta(c + 0.5 * h * k1, loops)
        k3 = beta(c + 0.5 * h * k2, loops); k4 = beta(c + h * k3, loops)
        c = c + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4); t += h
        ts[i], cs[i] = t, c
    return ts, cs

def analyse(Mt=173.34, Mh=125.15, a3=0.1184, loops=2, light_yukawas=True):
    c0, mt = inputs(Mt, Mh, a3, light_yukawas=light_yukawas)
    ts, cs = run(c0, math.log(mt), LN_MPL, loops=loops)
    lam = cs[:, 4]
    betas = beta(cs, loops)[:, 4]
    out = {}
    neg = np.where(lam < 0)[0]
    out["lambda_crosses_zero"] = bool(neg.size)
    out["log10_mu_zero_GeV"] = float(ts[neg[0]] / math.log(10)) if neg.size else None
    imin = int(np.argmin(lam))
    out["lambda_min"] = float(lam[imin]); out["log10_mu_lambda_min_GeV"] = float(ts[imin] / math.log(10))
    out["lambda_MPl"] = float(lam[-1]); out["beta_lambda_MPl"] = float(betas[-1])
    # scale where beta_lambda vanishes (if it does): first sign change of beta_lambda
    sgn = np.sign(betas); flips = np.where(sgn[1:] * sgn[:-1] < 0)[0]
    out["log10_mu_beta_lambda_zero_GeV"] = float(ts[flips[0]] / math.log(10)) if flips.size else None
    out["yt_MPl"] = float(cs[-1, 3]); out["g3_MPl"] = float(cs[-1, 2])
    out["g2_MPl"] = float(cs[-1, 1]); out["g1_GUT_MPl"] = float(S53 * cs[-1, 0])
    out["lambda_Mt"] = float(c0[4]); out["yt_Mt"] = float(c0[3])
    return out, ts, cs

def analyse_batch(Mt, Mh, a3, loops=2):
    c0 = np.stack([inputs(m, h, a)[0] for m, h, a in zip(Mt, Mh, a3)])
    ts, cs = run(c0, math.log(float(np.mean(Mt))), LN_MPL, loops=loops)
    lam = cs[:, :, 4]
    crosses = (lam < 0).any(axis=0)
    first = np.where(crosses, np.argmax(lam < 0, axis=0), -1)
    return {"lambda_MPl": lam[-1], "crosses": crosses,
            "log10_mu_zero": np.where(crosses, ts[np.clip(first, 0, None)] / math.log(10), np.nan)}

def montecarlo(n=4000, seed=20261031, Mt=172.57, sMt=0.29, Mh=125.20, sMh=0.11, a3=0.1180, sa3=0.0009, loops=2):
    """Draw the measured inputs (PDG-2024-era central values, see DATUM.md) and run each."""
    rng = np.random.default_rng(seed)
    b = analyse_batch(rng.normal(Mt, sMt, n), rng.normal(Mh, sMh, n), rng.normal(a3, sa3, n), loops=loops)
    lam_pl, crosses = b["lambda_MPl"], b["crosses"]
    return {
        "n": n, "seed": seed,
        "inputs": {"Mt": [Mt, sMt], "Mh": [Mh, sMh], "alpha_s": [a3, sa3]},
        "frac_lambda_negative_below_MPl": float(crosses.mean()),
        "lambda_MPl_mean": float(lam_pl.mean()), "lambda_MPl_sd": float(lam_pl.std()),
        "lambda_MPl_p05_p95": [float(np.percentile(lam_pl, 5)), float(np.percentile(lam_pl, 95))],
        "log10_mu_zero_median": float(np.nanmedian(b["log10_mu_zero"])) if crosses.any() else None,
    }

def stability_edge_Mt(Mh, a3, loops=2, lo=165.0, hi=180.0):
    """Bisect for the M_t at which lambda just touches zero below M_Pl."""
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if analyse(mid, Mh, a3, loops=loops)[0]["lambda_crosses_zero"]: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)

def stability_edge_Mh(Mt, a3, loops=2, lo=115.0, hi=140.0):
    """Bisect for the M_h above which lambda stays positive up to M_Pl."""
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if analyse(Mt, mid, a3, loops=loops)[0]["lambda_crosses_zero"]: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def check_against_1loop():
    """--loops 1 with the light Yukawas off must reproduce rge_1loop.py to ~1e-10."""
    try:
        import rge_1loop
    except ImportError:
        return None
    c5, mt = rge_1loop.inputs()
    _, cs1 = rge_1loop.run(c5, math.log(mt), LN_MPL)
    c7, _ = inputs(light_yukawas=False)
    _, cs2 = run(c7, math.log(mt), LN_MPL, loops=1)
    return float(np.max(np.abs(cs1[-1] - cs2[-1, :5])))

def main(argv):
    loops = 1 if "--loops" in argv and argv[argv.index("--loops") + 1] == "1" else 2
    light = "--no-light-yukawas" not in argv
    outfile = "results_2loop.json" if loops == 2 else "results_2loop_at1loop.json"

    central_2013, ts, cs = analyse(loops=loops, light_yukawas=light)
    central_now, _, _ = analyse(172.57, 125.20, 0.1180, loops=loops, light_yukawas=light)
    no_light, _, _ = analyse(loops=loops, light_yukawas=False)
    mc = montecarlo(loops=loops)
    edge_Mt_2024 = stability_edge_Mt(125.20, 0.1180, loops)
    edge_Mt_2013 = stability_edge_Mt(125.15, 0.1184, loops)
    edge_Mh_2013 = stability_edge_Mh(173.34, 0.1184, loops)
    # finite-difference slopes of lambda(M_Pl), to compare with eq. 61e's coefficients
    d_Mt = (analyse(174.34, 125.15, 0.1184, loops=loops)[0]["lambda_MPl"] - analyse(172.34, 125.15, 0.1184, loops=loops)[0]["lambda_MPl"]) / 2
    d_Mh = (analyse(173.34, 126.15, 0.1184, loops=loops)[0]["lambda_MPl"] - analyse(173.34, 124.15, 0.1184, loops=loops)[0]["lambda_MPl"]) / 2
    d_a3 = (analyse(173.34, 125.15, 0.1191, loops=loops)[0]["lambda_MPl"] - analyse(173.34, 125.15, 0.1177, loops=loops)[0]["lambda_MPl"]) / 2
    gate_pass = abs(central_2013["lambda_MPl"] - GATE_TARGET) <= GATE_TOL
    diff1 = check_against_1loop()

    results = {
        "loop_order": loops,
        "light_yukawas_included": light,
        "central_2013_inputs": central_2013,
        "central_2024_inputs": central_now,
        "central_2013_inputs_no_light_yukawas": no_light,
        "gate": {"target": GATE_TARGET, "tol": GATE_TOL, "got": central_2013["lambda_MPl"],
                 "miss": central_2013["lambda_MPl"] - GATE_TARGET, "pass": gate_pass},
        "literature_3loop_MPl_2013_inputs": LIT_MPL_3LOOP,
        "slopes_lambda_MPl": {"per_GeV_Mt": d_Mt, "per_GeV_Mh": d_Mh, "per_0.0007_alpha_s": d_a3,
                              "literature_61e": {"per_GeV_Mt": -0.0066, "per_GeV_Mh": 0.0029, "per_0.0007_alpha_s": 0.0018}},
        "Mt_stability_edge_GeV_2024_Mh_a3": round(edge_Mt_2024, 3),
        "Mt_stability_edge_GeV_2013_Mh_a3": round(edge_Mt_2013, 3),
        "Mh_stability_edge_GeV_2013_Mt_a3": round(edge_Mh_2013, 3),
        "literature_3loop_edge_Mt_GeV": [171.53, 0.42],
        "literature_3loop_edge_Mh_GeV": [129.6, 1.5],
        "max_abs_diff_vs_rge_1loop_at_1loop": diff1,
        "montecarlo": mc,
        "running_table": [[float(t / math.log(10)), float(c[4]), float(beta(c, loops)[4])] for t, c in zip(ts[::100], cs[::100])],
    }

    if "--check" in argv:
        rc = 0
        try:
            old = json.load(open(outfile))
        except FileNotFoundError:
            print(f"no {outfile} to check against"); return 1
        keys = ["central_2013_inputs", "central_2024_inputs", "Mt_stability_edge_GeV_2024_Mh_a3", "Mt_stability_edge_GeV_2013_Mh_a3", "Mh_stability_edge_GeV_2013_Mt_a3"]
        bad = [k for k in keys if json.dumps(old[k], sort_keys=True) != json.dumps(results[k], sort_keys=True)]
        print("check vs recorded json:", "ok" if not bad else "FAILED: " + ", ".join(bad)); rc |= bool(bad)
        if diff1 is None:
            print("check vs rge_1loop.py: skipped (module not importable)")
        else:
            ok = diff1 < 1e-9
            print(f"check vs rge_1loop.py at one loop: max |diff| = {diff1:.2e}", "ok" if ok else "FAILED"); rc |= (not ok)
        print("gate lambda(M_Pl) within", GATE_TOL, "of", GATE_TARGET, ":", "PASS" if gate_pass else "FAIL", f"(got {central_2013['lambda_MPl']:.4f})")
        return rc

    json.dump(results, open(outfile, "w"), indent=1)
    p = lambda k, v: print(f"{k:50s} {v}")
    print(f"SM running at {loops} loop(s), M_t -> M_Pl = {M_PL:.4e} GeV, light Yukawas {'on' if light else 'off'}")
    for name, o in ((f"2013 central inputs (Mt 173.34, Mh 125.15, a3 0.1184)", central_2013),
                    (f"2024 central inputs (Mt 172.57, Mh 125.20, a3 0.1180)", central_now)):
        print(name)
        p("  lambda(M_t)", f"{o['lambda_Mt']:.5f}")
        p("  lambda crosses zero at log10(mu/GeV)", o["log10_mu_zero_GeV"] and f"{o['log10_mu_zero_GeV']:.2f}")
        p("  lambda minimum", f"{o['lambda_min']:.4f} at log10 mu = {o['log10_mu_lambda_min_GeV']:.2f}")
        p("  beta_lambda = 0 at log10(mu/GeV)", o["log10_mu_beta_lambda_zero_GeV"] and f"{o['log10_mu_beta_lambda_zero_GeV']:.2f}")
        p("  lambda(M_Pl)", f"{o['lambda_MPl']:.4f}")
        p("  beta_lambda(M_Pl)", f"{o['beta_lambda_MPl']:.5f}")
        p("  g1_GUT, g2, g3, yt at M_Pl", f"{o['g1_GUT_MPl']:.4f}, {o['g2_MPl']:.4f}, {o['g3_MPl']:.4f}, {o['yt_MPl']:.4f}")
    print("three-loop literature at M_Pl, 2013 inputs (eq. 61a-e)")
    p("  g1_GUT, g2, g3, yt", f"{LIT_MPL_3LOOP['g1_GUT']}, {LIT_MPL_3LOOP['g2']}, {LIT_MPL_3LOOP['g3']}, {LIT_MPL_3LOOP['yt']}")
    p("  lambda", f"{LIT_MPL_3LOOP['lambda']}")
    p("GATE lambda(M_Pl) at 2013 inputs", f"{'PASS' if gate_pass else 'FAIL'}: got {central_2013['lambda_MPl']:.4f}, target {GATE_TARGET} +- {GATE_TOL}, miss {central_2013['lambda_MPl'] - GATE_TARGET:+.4f}")
    p("effect of light Yukawas on lambda(M_Pl)", f"{central_2013['lambda_MPl'] - no_light['lambda_MPl']:+.6f}")
    p("slopes d lambda(M_Pl): per GeV Mt, Mh; per 0.0007 a3", f"{d_Mt:+.4f}, {d_Mh:+.4f}, {d_a3:+.4f}   (lit. 61e: -0.0066, +0.0029, +0.0018)")
    p("stability edge in Mt (Mh 125.20, a3 0.1180)", f"{edge_Mt_2024:.2f} GeV")
    p("stability edge in Mt (Mh 125.15, a3 0.1184)", f"{edge_Mt_2013:.2f} GeV  (3-loop literature: 171.53 +- 0.42)")
    p("stability edge in Mh (Mt 173.34, a3 0.1184)", f"{edge_Mh_2013:.2f} GeV  (3-loop literature: 129.6 +- 1.5)")
    p("Monte Carlo: P(lambda<0 somewhere below M_Pl)", f"{mc['frac_lambda_negative_below_MPl']:.3f}")
    p("Monte Carlo: lambda(M_Pl) mean, sd", f"{mc['lambda_MPl_mean']:.4f}, {mc['lambda_MPl_sd']:.4f}")
    p("Monte Carlo: lambda(M_Pl) 5-95%", f"{mc['lambda_MPl_p05_p95'][0]:.4f} .. {mc['lambda_MPl_p05_p95'][1]:.4f}")
    if diff1 is not None:
        p("this file at 1 loop vs rge_1loop.py, max |diff|", f"{diff1:.2e}")
    print(f"wrote {outfile}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
