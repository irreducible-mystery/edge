#!/usr/bin/env python3
"""probe_2loop_limits.py — independent check of every two-loop term in rge_2loop.py.

rge_2loop.py transcribes its beta functions from arXiv:1307.3536 appendix B. The critic
audit of 2026-10-31 (AUDIT-2LOOP-2026-10-31.md) compared the transcription against the
same paper. This probe is the other kind of check: it evaluates the two-loop piece of
beta() numerically in limits where the standard-literature coefficients are known
independently (Machacek & Vaughn 1983-85; Luo, Wang & Xiao 2003; Ford, Jack & Jones 1992),
written here from recall of those sources, NOT from Buttazzo et al. Agreement of two
independent transcriptions to all printed digits is evidence that both are right.

Conventions: V = lambda (H^dag H)^2; g_Y in SM normalisation; the gauge matrix below is in
GUT normalisation g_1^2 = (5/3) g_Y^2 because that is how it is usually printed.

Tier of the expected values: RECALL (standard, but from memory). Tier of the result: DERIVED.
Exit 0 iff every probe agrees to 1e-6 relative; prints each. numpy only.
"""
import sys, numpy as np
import rge_2loop as R

def two(c):
    c = np.array(c, float)
    return (R.beta(c, loops=2) - R.beta(c, loops=1)) / R.K2   # two-loop piece, times (16 pi^2)^2

gY, g2, g3, yt, lam = 0.36, 0.65, 1.17, 0.9, 0.13
g1 = R.S53 * gY; gs = np.array([g1, g2, g3])
probes = []

# A. pure-gauge two-loop matrix b_ij (GUT normalisation): dg_i/dt ⊃ g_i^3 sum_j b_ij g_j^2 / (16pi^2)^2
b = np.array([[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]])
got = two([gY, g2, g3, 0, 0, 0, 0])[:3]; got[0] *= R.S53
exp = gs**3 * (b @ gs**2)
for i, n in enumerate(("g1", "g2", "g3")): probes.append((f"A gauge matrix row {n}", got[i], exp[i]))

# B. Yukawa term in the gauge betas: coefficient of y_t^2 g_i^3 is (-17/10, -3/2, -2)
ga = two([gY, g2, g3, yt, 0, 0, 0])[:3]; ga[0] *= R.S53
coef = (ga - exp) / (gs**3 * yt**2)
for i, (n, e) in enumerate(zip(("g1", "g2", "g3"), (-1.7, -1.5, -2.0))): probes.append((f"B yt^2 term in beta_{n}", coef[i], e))

# C. y_t two-loop, gauge off: y_t ( -12 yt^4 + 6 lam^2 - 12 lam yt^2 )
probes.append(("C beta_yt gauge-off", two([0, 0, 0, yt, lam, 0, 0])[3] / yt, -12*yt**4 + 6*lam**2 - 12*lam*yt**2))

# D. lambda two-loop, gauge off: -312 lam^3 - 144 lam^2 yt^2 - 3 lam yt^4 + 30 yt^6
probes.append(("D beta_lambda gauge-off", two([0, 0, 0, yt, lam, 0, 0])[4], -312*lam**3 - 144*lam**2*yt**2 - 3*lam*yt**4 + 30*yt**6))

# E. y_t two-loop, pure gauge (y_t -> 0 limit extracted by subtraction)
pureE = 1187/216*gY**4 - 23/4*g2**4 - 108*g3**4 - 3/4*gY**2*g2**2 + 19/9*gY**2*g3**2 + 9*g2**2*g3**2
mixE = yt**2 * (131/16*gY**2 + 225/16*g2**2 + 36*g3**2)
gotE = two([gY, g2, g3, yt, 0, 0, 0])[3] / yt
probes.append(("E+F beta_yt gauge and mixed terms", gotE, -12*yt**4 + pureE + mixE))

# G. lambda two-loop, yt = 0: lambda-gauge terms
pureG = (-312*lam**3 + 36*lam**2*(3*g2**2 + gY**2) + lam*(-73/8*g2**4 + 39/4*g2**2*gY**2 + 629/24*gY**4)
         + 305/16*g2**6 - 289/48*g2**4*gY**2 - 559/48*g2**2*gY**4 - 379/48*gY**6)
probes.append(("G beta_lambda yt=0", two([gY, g2, g3, 0, lam, 0, 0])[4], pureG))

# H. lambda two-loop, mixed yt-gauge terms
mixH = (lam*yt**2*(45/2*g2**2 + 85/6*gY**2 + 80*g3**2) - yt**4*(32*g3**2 + 8/3*gY**2)
        + yt**2*(-9/4*g2**4 + 21/2*g2**2*gY**2 - 19/4*gY**4))
full = two([gY, g2, g3, yt, lam, 0, 0])[4]
probes.append(("H beta_lambda mixed yt-gauge", full - pureG - (-144*lam**2*yt**2 - 3*lam*yt**4 + 30*yt**6), mixH))

ok = True
for name, g, e in probes:
    rel = abs(g - e) / max(abs(e), 1e-12)
    good = rel < 1e-6; ok &= good
    print(f"{'ok  ' if good else 'FAIL'} {name:36s} code {g:+.6f}  standard {e:+.6f}  rel {rel:.1e}")
print("probe:", "all two-loop terms agree with the standard coefficients" if ok else "DISAGREEMENT")
sys.exit(0 if ok else 1)
