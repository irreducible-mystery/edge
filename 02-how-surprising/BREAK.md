# Q0: the datum survives; compulsory surprise does not

**Role: breaker. Session: prior-sweep. 2026-10-31.**
Scope: issue #5, at main `83e737c60e97563fb63078794e06cb662f8bea2b`.
Tags have the meanings in `../LEDGER.md`. Numbers below are DERIVED in the stated
model; priors and conditioning are STIPULATED; judgments are INFERENCE.

## The case for nothing to explain

**INFERENCE.** A small distance becomes an anomaly only after specifying the space
in which it could have landed. This repo chose a striking description before it
chose a probability measure. The same local band contains 0.10% of a broad weak-scale
quartic prior and 18.25% of a small-quartic UV prior. Neither percentage is a property
of the measured universe alone. Three unrelated small coefficients, a retrospectively
selected boundary, and a downward revision of a noisy mass estimate do not establish
a common cause. The null deserves to remain in contention.

**Recommendation, not a merge decision:** withdraw S1 as a requirement that the
quartic proximity needs an additional explanation **if** the steward accepts the
small-quartic prior below. The issue's p > 0.1 criterion is met there. Keep S1's
original text in the record. Do not declare the hierarchy or cosmological constant
problems solved, or claim coincidence has been demonstrated. The defensibility of
the prior is the remaining substantive disagreement, not another beta-function check.

## Precisely what was computed

**STANDARD (source equations); DERIVED (substitution).** Source:
[Buttazzo et al., arXiv:1307.3536v4](https://arxiv.org/pdf/1307.3536),
eqs. 55, 61e, 64, printed pp. 14, 16, 19. Eq. 64 is a local effective-potential
stability fit. With masses in GeV, define

```
Hc(t,a) = 129.6 + 2(t - 173.34) - 0.5(a - 0.1184)/0.0007
d_t(h,t,a) = |h - Hc(t,a)|/2
```

**STIPULATED inputs:** `(h,t,a) = (125.20,172.57,0.1180)`, exactly the repo's
2024-era RECALL inputs. These are not newly verified world averages. Condition on
`t,a` and scan `h`, or a local quartic coordinate. The event is two-sided:
`d_t <= d_t(observed)`; stable and metastable sides both count. We do not condition
on absolute stability or observer survival. This is a one-dimensional conditional
question, not a joint probability over all Standard Model parameters.

**DERIVED:** `Hc = 128.345714`, `t_edge(h_obs) = 170.997143`, and
`delta_t = 1.572857` GeV. The event is `h in [125.200000,131.491429]`.
Using eq. 64 consistently gives this distance, rather than importing the isolated
171.53 GeV number from eq. 66 or the brief's rounded 1 GeV. This is an input to
Q0, not a repair of DATUM.md or an audit of the running code.

**DERIVED:** Eq. 61e gives `lambda_UV(obs) = -0.010101571` and, at Hc on this
fixed-top slice, `lambda_UV(edge) = -0.000979000`. The boundary interval maps to
`lambda_UV in [-0.010101571,0.008143571]`; its half-width is `0.009122571`.
This coupling distance is along the fixed-top slice, not a top-direction derivative
or a Euclidean normal to a multidimensional surface. Separately, the zero-proximity
event is `|lambda_UV| <= 0.010101571`. Zero at M_Pl and the potential stability
boundary are distinct events; their probabilities are not independent evidence.

## Every prior, including the unfriendly one

**STIPULATED priors; DERIVED probabilities.** All supports are uniform in the
named coordinate. No Monte Carlo error: intersect the event interval with the
support and divide its length by the support length. The coupling maps use the
local slopes `d lambda_EW/dh = 0.00206` and `d lambda_UV/dh = 0.0029`.

| Conditional prior | p(boundary band) | p(UV near zero) | What supplies its scale |
|---|---:|---:|---|
| h uniform on (0,700) GeV | 0.008987755 | 0.009952287 | Requested wide mass support |
| lambda_EW uniform on (0,4 pi) | 0.001031351 | 0.001142032 | Requested perturbative-size normalization |
| lambda_UV uniform on (-0.2,0.2) | 0.045612857 | 0.050507857 | Requested gauge-coupling-scale prior |
| lambda_UV uniform on (-0.05,0.05) | **0.182451429** | **0.202031429** | Breaker's small-quartic UV prior |

**INFERENCE: defense of the last prior.** A UV quartic much smaller than one is a
legitimate weak-coupling hypothesis. The interval includes both signs, is centered
at the algebraically special value zero rather than the measured negative value,
and is broader than the observed magnitude by about five. It posits a small
quartic, not a degenerate vacuum or a critical-point attractor. It can therefore
represent an independently small coefficient without a common cause for all three
potential terms. A physicist can entertain it without accepting any of this repo's
candidate mechanisms.

**INFERENCE: the cost of that defense.** The width 0.05 is a modeling choice made
with the data visible, not a premeasurement prediction or a calculated UV measure.
Zero quartic is not protected merely by being zero; additive interactions make
smallness nontrivial. A UV mechanism that generates this prior would itself explain
something. Thus this is an admissible sensitivity case, not an objectively preferred
ignorance prior and not a proof that no explanation exists. Calling it definitive
would repeat the same prior-selection mistake in the opposite direction.

**DERIVED sensitivity:** for symmetric uniform UV support (-A,A), while the
whole event lies inside it, `p_boundary = 0.009122571/A`.

| A | p(boundary band) |
|---:|---:|
| 0.02 | 0.456128571 |
| 0.05 | 0.182451429 |
| 0.10 | 0.091225714 |
| 0.20 | 0.045612857 |
| 1.00 | 0.009122571 |

The issue's 0.1 threshold is crossed at `A = 0.091225714`. At A=0.1 the
zero-proximity statistic passes 0.1 but the boundary statistic does not: substituting
one for the other would change the verdict. The four headline priors were all kept.
The extra widths are a sensitivity sweep, not extra independent attempts to confirm
coincidence. One-at-a-time shifts of h by 0.11 GeV, t by 0.29 GeV, alpha_s by
0.0009, or Hc by 0.3 GeV leave the A=0.05 boundary probability between 0.1452
and 0.2198. This is not a joint confidence interval; correlated or simultaneous
shifts and mass-scheme uncertainties can change it further.

### Limits of the probability model

**STIPULATED + INFERENCE.** We use the permitted local linear boundary model.
The event is local; the broad prior supports are normalization choices. We have
not established the complete nonlinear phase diagram over h=0..700 or
lambda_EW=0..4 pi, nor excluded additional event components elsewhere. These
numbers are exact for the stated linear model, approximate for the physical SM.
Conditioning on a measured top mass also relinquishes a joint prediction of top
and Higgs. A UV prior on lambda alone is not a distribution for all UV couplings.
In particular we have not computed a joint rarity of small lambda and small beta.

**DERIVED toy diagnostic, not a new SM bound.** The directory brief calls 700 GeV
a Planck-scale triviality cutoff. Retain that support as requested, but do not use
that justification. In the explicitly scalar-only approximation
`d lambda/d ln(mu) = 24 lambda^2/(16 pi^2)` and `lambda = h^2/(2v^2)`,

```
ln(Lambda_pole/t) = 2 pi^2/(3 lambda(t))
lambda_max(t) = 2 pi^2/[3 ln(M_Pl/t)]
```

At v=246.21971 GeV and M_Pl=1.2209e19 GeV this gives h=143.40 GeV for a
pole at M_Pl; h=700 gives a pole at 879.13 GeV. Gauge and Yukawa terms are
omitted, so 143.40 is **not** the SM upper bound. This elementary diagnostic
cannot justify 700 as a Planck-valid cutoff. Likewise much of (0,4 pi) would not
remain perturbative up to M_Pl. A conditional prior that discards such draws
must be renormalized after specifying the survival criterion. We have not done
that and do not hide discarded draws in a Monte Carlo denominator.

## Three attacks on the inference

### The Dirac-large-numbers trap

**INFERENCE, conceptual analogy.** A table can make a pattern without providing
a sampling model. Lambda is a dimensionless running coupling; m^2/M_Pl^2 and
vacuum energy/M_Pl^4 compare dimensionful coefficients with a chosen reference
scale. A common potential is a useful organization, not evidence that these
coefficients are independent identically distributed draws, nor that a single
mechanism controls them. Multiplying three informal smallnesses has no statistical
meaning. Even a small joint probability would need a comparison with alternatives
that put more probability on these observations.

This attack removes the claimed **additional evidence for one common cause** from
the table alone. It does not remove the separate hierarchy and vacuum-energy
questions. Nor does it establish that the coefficients are physically unrelated;
that is C0's hypothesis, not a finding of this calculation.

### How many other edges could we have celebrated?

**STIPULATED search menu, not reconstructed history.** Beyond the selected lambda
stability claim, here are ten families of alternative predicates available to a
storyteller. Scales, tolerances, and flavor indices enlarge this menu further.

| Alternative predicate | Choice that can be made after seeing data |
|---|---|
| m^2/M_Pl^2 close to zero | Scale defining smallness |
| Vacuum energy/M_Pl^4 close to zero | Same, plus cosmological conditioning |
| beta_lambda close to zero | Scale or window of minimization |
| lambda crosses zero near a nominated high scale | GUT, Planck, or another target |
| g1 close to g2 | Scale and normalization |
| g2 close to g3 | Scale and threshold allowance |
| y_t close to a gauge coupling | Which gauge coupling and scale |
| A charged-fermion Yukawa close to zero | Flavor and normalization |
| A quark mixing angle close to zero | Which angle and metric |
| Strong CP angle close to its CP-conserving surface | Prior and tolerance |

**INFERENCE.** Several are already celebrated puzzles; none is claimed here to be
an undocumented historical failed test. We cannot honestly count how many were
actually tried and not reported. These ten alternatives demonstrate selection
freedom, not ten independent trials. Running relations and common inputs strongly
correlate them. A calibrated global probability would require a fixed menu,
a joint prior, and executing the same selection rule on synthetic universes.

**DERIVED illustration only:** with N independent tests each having local
probability p, `P(any) = 1-(1-p)^N`. For p=0.045612857, N=1,3,10,30 gives
0.0456, 0.1307, 0.3730, 0.7535. Without independence but with equal marginals,
the union bound is `P(any) <= min(1,Np)`; it is an upper bound, not a correction
to apply. The output records both. No effective N or global significance is
claimed. The attack is that the repo has not paid this selection cost, not that
we have measured it.

### The top mass moved toward the edge

**DERIVED arithmetic; INFERENCE interpretation.** The two quoted central values,
173.34 and 172.57 GeV, differ by -0.77 GeV. Comparing two estimates of a constant
does not observe the underlying mass moving, much less an attraction mechanism.
The estimates share information and may differ in systematics or definitions.
The repo does not supply their covariance or a model for successive estimates,
so we do not attach an independent p-value to their difference. Choosing the
favorable direction after observing the update adds no clean replication.
Greater precision can strengthen a present proximity claim; a downward update
by itself does not. This is a noise-compatible reading, not a demonstrated
noise model or a claim that later measurements must move away.

## One attack per existing candidate

**Scope checked:** the tree at the base SHA contains only `03-candidates/coincidence.md`
besides its README. The four other candidate filenames in the table do not exist.
Their historical prediction claims remain outside this pass; absence of a file is
not evidence that those predictions were postdictions.

**C0 — attack: the null can also postdict.** Its free choices are the scanning
coordinate, support width and center, conditioning variables, event definition,
and selection procedure. Letting those choices follow the observed point makes
"there is a reasonable prior with large p" cheap to achieve. There is no dated,
quantitative premeasurement distribution in C0 to score; this exercise supplies
an explicit retrospective family, not a successful prediction. The defense is
the full table, width sweep, and disclosure of which assumption produces 18.25%.
An independent premeasurement UV measure could strengthen or defeat that defense.

**Verdict: C0 remains live, not established.** Its stated p<0.01-under-every-tried-prior
kill condition is not met. Conversely a good prediction by a rival would support
that rival, not logically falsify every possible chance model. The extra freedom
must eventually be paid for with a fixed measure or a comparison of predictive
distributions. This attack is also appended to the candidate file.

## Score the breaker against its own weaknesses

**INFERENCE scores:** 0 means no force; 5 means decisive for the narrow target
named. These are judgments, not probabilities.

| Attack | Score | What it earns | Strongest weakness |
|---|---:|---|---|
| Prior sensitivity | 5/5 | No unique prior-free surprise number | Does not choose the right physical prior |
| A=0.05 exceeds 0.1 | 3/5 | Conditional case to withdraw S1's quartic floor | Small-UV assumption itself needs justification |
| Three-smallnesses table | 4/5 | Table alone is not evidence of a common cause | A future common mechanism could predict all three |
| Look elsewhere | 2/5 | Local p cannot be advertised as global p | No calibrated trial count or joint prior |
| Downward top update | 4/5 | Direction alone adds no independent evidence | Better present measurements still matter |
| Attack on C0 | 4/5 | Null is not a parameter-free prediction | Broad model families can still be useful |

**What survived, exactly (DERIVED + INFERENCE):** in the literature's local
model, the repo's stated inputs are 1.572857 top-GeV from the potential boundary.
The proximity is below 1% under the two broad infrared priors, about 4.56% under
the requested A=0.2 UV prior, and 18.25% under A=0.05. A small-quartic prior
makes this particular proximity unremarkable by the issue's criterion. The
geometric datum survives all four; a mandatory, prior-independent demand for an
explanation does not. No result here adjudicates the full lambda/beta coincidence,
all three potential parameters, or the absent mechanisms' historical predictions.

## Reproduction

```sh
python3 02-how-surprising/surprise.py
python3 02-how-surprising/surprise.py --check
```

`surprise.json` contains all priors, supports, event endpoints, both coupling
statistics, width and input sensitivities, illustrative trial factors, and the
scalar toy diagnostic. `--check` tests interval normalization/clipping/invalid
inputs, independently integrates the event in each prior coordinate on a
100,000-point midpoint grid, and compares **every** recorded output field.
No beta functions or existing RGE implementation were checked or changed.
