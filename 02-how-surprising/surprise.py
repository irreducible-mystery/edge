#!/usr/bin/env python3
"""Q0 breaker: exact interval probabilities in a stated local linear model.

Role: breaker; session: prior-sweep; 2026-10-31.
Run: python3 02-how-surprising/surprise.py
Check: python3 02-how-surprising/surprise.py --check
Standard library only. No RGE code is imported, changed, or audited.

Sources: https://arxiv.org/pdf/1307.3536 (v4), eqs. 55, 61e, 64.
All priors condition on Mt and alpha_s. Only Mh (or its local coupling
coordinate) scans. These are prior predictive probabilities, not experimental
p-values, posterior probabilities of coincidence, or a joint three-edge test.
The broad supports specify normalization, not a claim that the local fits
describe an entire broad-support SM phase diagram. See BREAK.md.
"""

import argparse
import json
import math
from pathlib import Path

BASE_SHA = "83e737c60e97563fb63078794e06cb662f8bea2b"
INPUTS = {"mh_GeV": 125.20, "mt_GeV": 172.57, "alpha_s": 0.1180}
PRIORS = (
    ("flat_Mh_0_700", "mh_GeV", 0.0, 700.0),
    ("flat_lambda_EW_0_4pi", "lambda_EW", 0.0, 4.0 * math.pi),
    ("flat_lambda_UV_pm_0p2", "lambda_UV", -0.2, 0.2),
    ("flat_lambda_UV_pm_0p05", "lambda_UV", -0.05, 0.05),
)


def critical_higgs(mt, alpha_s, theory_shift=0.0):
    """Eq. 64; theory_shift is an additive displacement in Higgs GeV."""
    return 129.6 + 2.0 * (mt - 173.34) - 0.5 * (alpha_s - 0.1184) / 0.0007 + theory_shift


def lambda_ew(mh, mt):
    """Eq. 55, used locally, not extrapolated to Mh=0 or 700."""
    return 0.12604 + 0.00206 * (mh - 125.15) - 0.00004 * (mt - 173.34)


def lambda_uv(mh, mt, alpha_s):
    """Eq. 61e, MS-bar quartic at the unreduced Planck scale."""
    return (-0.0143 - 0.0066 * (mt - 173.34)
            + 0.0018 * (alpha_s - 0.1184) / 0.0007
            + 0.0029 * (mh - 125.15))


def uniform_probability(event, support):
    """Exact measure of an interval intersected with a uniform support."""
    lo, hi = event
    a, b = support
    if not all(math.isfinite(x) for x in (lo, hi, a, b)) or hi < lo or b <= a:
        raise ValueError("finite ordered event and nonzero support required")
    return max(0.0, min(hi, b) - max(lo, a)) / (b - a)


def geometry(mh, mt, alpha_s, theory_shift=0.0):
    hc = critical_higgs(mt, alpha_s, theory_shift)
    dt = abs(mh - hc) / 2.0
    hband = (hc - 2.0 * dt, hc + 2.0 * dt)
    uv_obs = lambda_uv(mh, mt, alpha_s)
    uv_edge = lambda_uv(hc, mt, alpha_s)
    return {
        "critical_mh_GeV": hc,
        "critical_mt_at_observed_mh_GeV": mt + (mh - hc) / 2.0,
        "delta_top_GeV": dt,
        "lambda_UV_observed": uv_obs,
        "lambda_UV_at_potential_boundary_on_fixed_mt_slice": uv_edge,
        "delta_lambda_UV_to_boundary_on_fixed_mt_slice": abs(uv_obs - uv_edge),
        "delta_lambda_UV_to_zero": abs(uv_obs),
        "boundary_bands": {
            "mh_GeV": list(hband),
            "lambda_EW": [lambda_ew(h, mt) for h in hband],
            "lambda_UV": [lambda_uv(h, mt, alpha_s) for h in hband],
        },
    }


def prior_rows(g, mt, alpha_s):
    # A second, distinct event: |lambda_UV| <= |lambda_UV_observed|.
    # Translate only its nearby endpoints to the other local coordinates.
    d = g["delta_lambda_UV_to_zero"]
    hzero = [(u - lambda_uv(125.15, mt, alpha_s)) / 0.0029 + 125.15
             for u in (-d, d)]
    zero_bands = {"mh_GeV": hzero,
                  "lambda_EW": [lambda_ew(h, mt) for h in hzero],
                  "lambda_UV": [-d, d]}
    return [
        {"prior": name, "coordinate": coord, "support": [a, b],
         "p_boundary": uniform_probability(g["boundary_bands"][coord], (a, b)),
         "p_lambda_UV_near_zero": uniform_probability(zero_bands[coord], (a, b))}
        for name, coord, a, b in PRIORS
    ]


def scalar_triviality_diagnostic(mt):
    # A stipulated large-lambda scalar approximation, NOT an SM RGE audit:
    # d lambda/d ln(mu) = 24 lambda^2/(16 pi^2), lambda=Mh^2/(2 v^2).
    # Thus ln(Lambda_pole/mt)=2 pi^2/(3 lambda(mt)).
    v, mpl = 246.21971, 1.2209e19
    lmax = 2.0 * math.pi**2 / (3.0 * math.log(mpl / mt))
    l700 = 700.0**2 / (2.0 * v**2)
    return {"model": "large-lambda scalar-only one-loop toy; not a full SM bound",
            "v_GeV": v, "M_Pl_GeV": mpl,
            "lambda_EW_pole_at_Planck": lmax,
            "mh_pole_at_Planck_GeV": math.sqrt(2.0 * v**2 * lmax),
            "pole_scale_for_mh_700_GeV": mt * math.exp(2.0 * math.pi**2 / (3.0 * l700))}


def calculate():
    mh, mt, a = INPUTS.values()
    g = geometry(mh, mt, a)
    rows = prior_rows(g, mt, a)
    width_sweep = [
        {"UV_half_width": w,
         "p_boundary": uniform_probability(g["boundary_bands"]["lambda_UV"], (-w, w)),
         "p_lambda_UV_near_zero": uniform_probability(
             (-g["delta_lambda_UV_to_zero"], g["delta_lambda_UV_to_zero"]), (-w, w))}
        for w in (0.02, 0.05, 0.1, 0.2, 1.0)
    ]
    variations = []
    for name, sigma in (("mh_GeV", 0.11), ("mt_GeV", 0.29), ("alpha_s", 0.0009),
                        ("boundary_theory_mh_GeV", 0.3)):
        for sign in (-1, 1):
            case = dict(INPUTS)
            shift = sign * sigma if name == "boundary_theory_mh_GeV" else 0.0
            if name in case:
                case[name] += sign * sigma
            gg = geometry(case["mh_GeV"], case["mt_GeV"], case["alpha_s"], shift)
            variations.append({"changed": name, "offset": sign * sigma,
                               "delta_top_GeV": gg["delta_top_GeV"],
                               "p_boundary": {r["prior"]: r["p_boundary"]
                                              for r in prior_rows(gg, case["mt_GeV"], case["alpha_s"])}})
    trials = [{"prior": r["prior"], "illustrative_independent_trials": n,
               "p_at_least_one_if_iid": -math.expm1(n * math.log1p(-r["p_boundary"])),
               "union_bound_if_each_marginal_p_equal": min(1.0, n * r["p_boundary"])}
              for r in rows for n in (1, 3, 10, 30)]
    return {"role": "breaker", "session": "prior-sweep", "base_commit": BASE_SHA,
            "source": "arXiv:1307.3536v4, equations 55, 61e, 64",
            "input_status": "repo 2024-era RECALL inputs; not asserted current",
            "inputs": INPUTS,
            "conditioning": "Mt, alpha_s fixed; Mh/local quartic coordinate scans",
            "event": "abs(Mh - critical_higgs(Mt,alpha_s))/2 <= observed delta_top",
            "method": "analytic interval intersection; local linear boundary model",
            "geometry": g, "priors": rows, "UV_width_sensitivity": width_sweep,
            "one_at_a_time_input_sensitivity": variations,
            "look_elsewhere_sensitivity_not_calibrated_global_p": trials,
            "scalar_triviality_diagnostic": scalar_triviality_diagnostic(mt)}


def self_test():
    """Boundary, normalization, clipping and independent integration checks."""
    assert uniform_probability((-1, 1), (-1, 1)) == 1.0
    assert uniform_probability((2, 3), (-1, 1)) == 0.0
    assert uniform_probability((0, 2), (-1, 1)) == 0.5
    assert uniform_probability((0, 0), (-1, 1)) == 0.0
    for event, support in [((1, 0), (0, 1)), ((0, 1), (1, 1)),
                           ((0, math.nan), (0, 1))]:
        try:
            uniform_probability(event, support)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid interval accepted")
    mt, a = INPUTS["mt_GeV"], INPUTS["alpha_s"]
    hc = critical_higgs(mt, a)
    assert geometry(hc, mt, a)["delta_top_GeV"] == 0.0
    g = geometry(**{"mh": INPUTS["mh_GeV"], "mt": mt, "alpha_s": a})
    for h in g["boundary_bands"]["mh_GeV"]:
        # Recompute the top edge independently from algebraic inversion.
        tc = 173.34 + (h - 129.6 + 0.5 * (a - 0.1184) / 0.0007) / 2.0
        assert math.isclose(abs(mt - tc), g["delta_top_GeV"], abs_tol=1e-12)
    # Integrate predicate on a deterministic midpoint grid in each prior's own
    # coordinate. This catches endpoint and Jacobian errors without RNG noise.
    n = 100000
    for r in prior_rows(g, mt, a):
        lo, hi = r["support"]
        hits = 0
        for i in range(n):
            x = lo + (i + 0.5) * (hi - lo) / n
            if r["coordinate"] == "mh_GeV":
                h = x
            elif r["coordinate"] == "lambda_EW":
                h = 125.15 + (x - lambda_ew(125.15, mt)) / 0.00206
            else:
                h = 125.15 + (x - lambda_uv(125.15, mt, a)) / 0.0029
            hits += abs(h - hc) / 2.0 <= g["delta_top_GeV"]
        assert abs(hits / n - r["p_boundary"]) <= 2.0 / n
    diag = scalar_triviality_diagnostic(mt)
    pole = mt * math.exp(2.0 * math.pi**2 / (3.0 * diag["lambda_EW_pole_at_Planck"]))
    assert math.isclose(pole, diag["M_Pl_GeV"], rel_tol=1e-12)


def same_record(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_record(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_record(x, y) for x, y in zip(a, b))
    if isinstance(a, float):
        return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14)
    return a == b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="self-test and compare every output field; never overwrite")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("surprise.json"))
    args = parser.parse_args()
    result = calculate()
    if args.check:
        self_test()
        try:
            recorded = json.loads(args.output.read_text())
        except (OSError, ValueError) as e:
            parser.exit(1, f"FAIL: cannot read recorded output: {e}\n")
        if not same_record(result, recorded):
            parser.exit(1, "FAIL: recorded output differs (all fields compared)\n")
    else:
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    g = result["geometry"]
    print(f"delta_top = {g['delta_top_GeV']:.9f} GeV")
    print(f"delta_lambda_UV_to_boundary = {g['delta_lambda_UV_to_boundary_on_fixed_mt_slice']:.9f}")
    print(f"delta_lambda_UV_to_zero = {g['delta_lambda_UV_to_zero']:.9f}")
    print("prior                              p_boundary     p_lambda_UV_near_zero")
    for row in result["priors"]:
        print(f"{row['prior']:34} {row['p_boundary']:.9f}    {row['p_lambda_UV_near_zero']:.9f}")
    if args.check:
        print("PASS: interval tests, independent grid integration, and every recorded field")


if __name__ == "__main__":
    main()
