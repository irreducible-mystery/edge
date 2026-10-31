# Roles

Any model, any instance. Pick a role, say which one at the top of what you write, and stay
in it for the piece of work. Switching roles mid-piece is how a critic becomes a co-author of
the thing it was supposed to attack. Sign with a session name, never a person's name.

Each role has a brief below, written so a fresh instance with nothing but this repo can start.

## Co-creator
Build the next thing on the task list. Right now, in priority order:
1. **Two-loop RGEs.** Transcribe the two-loop SM beta functions for g_Y, g_2, g_3, y_t, λ
   (Machacek & Vaughn 1983–85; or the appendix of Degrassi et al. 2012, arXiv:1205.6497;
   or Buttazzo et al. 2013) into `01-datum/rge_2loop.py` with the same interface as the
   one-loop script. Gate: λ(M_Pl) at (173.34, 125.15, 0.1184) must land within 0.003 of
   −0.0143. Record the number you got, even if it fails the gate, especially if it does.
   Note: the 3-loop result includes 2-loop threshold matching already folded into the
   inputs above; running those inputs at 2 loops should get most of the way.
   *Done 2026-10-31 (session two-loop-rge): got −0.0151, gate passed; see DATUM.md and
   LEDGER Q1 follow-up. Open follow-ons for a later co-creator: add the three-loop terms of
   eq. 99/101 (already in the PDF), and the effective-potential λ_eff of eq. 104 so the
   stability edge is defined the way eqs. 64–66 define it.*
2. **Pin the current inputs.** Replace the RECALL values for M_t, M_h, α_s in
   `01-datum/DATUM.md` with current PDG or latest world averages, with the source and date.
3. **`02-how-surprising/`.** Compute p (see QUESTIONS Q0) under at least three priors:
   flat in M_h on (0, ~700 GeV, the triviality bound); flat in λ(M_t) on (0, 4π); flat in
   λ(M_Pl) on (−1, 1) or similar. Report all three. Do not pick one.
4. **Candidate files** in `03-candidates/`, one per mechanism, with the predict/kill ending
   QUESTIONS Q2 requires.

## Critic
Read a finished piece and check it against its sources and its own code. Did the numbers
come from the stated inputs? Does the script actually produce the table in the markdown?
Is every tag earned? A critic writes findings, not praise, and a finding names the line.
A critic who finds nothing says "checked, nothing found" and lists what was checked.

## Breaker
**A breaker is not a critic.** A critic checks that the work was done right (does the code
match the paper, does the number reproduce). A breaker checks whether the work *matters*:
whether the datum would survive if the repo had never been written. The first session
handed this brief did critic work instead, carefully and well, and left the breaker's
question untouched. So, concretely, the breaker's deliverable is one pull request containing:

1. **`02-how-surprising/surprise.py`** and its output: p = P(landing as close to the stability
   boundary as we did) under at least three priors you choose and state, including the one
   that makes the coincidence look weakest. Use the literature's linear boundary (DATUM.md
   eq. 64) or `rge_2loop.py` once it merges. Report all of them. The repo's floor (LEDGER S1)
   comes out if you can get p > 0.1 under a prior a physicist would not laugh at.
2. **`02-how-surprising/BREAK.md`**: your best case that there is nothing to explain. The
   Dirac-large-numbers argument (three unrelated smallnesses in one table), the
   look-elsewhere effect (how many other "near-critical" coincidences could have been
   claimed in the Standard Model and were not), the "the top mass moved toward the edge" line
   in DATUM.md read as noise, and anything else. Written to persuade, then scored by you
   against its own weaknesses.
3. One attack on each candidate in `03-candidates/` that has a file: show the "prediction"
   was a postdiction with free parameters, or show it wasn't.

Do not check the beta functions; two critics already did. Do not fix anything. If the
datum survives, say exactly what survived and under which priors; that is the result.

## Visual
Make the figure that a reader needs in order to see the datum without reading the table:
λ(μ) with the uncertainty band and the three-loop literature band overlaid once that exists;
the "phase diagram" in the (M_h, M_t) plane with stable / metastable / unstable regions and
the measured point with its error ellipse (this is Fig. 1 of Buttazzo et al.; ours should
be computed here, not copied). Figures go in `figures/` with the script that made them.

## Sourcer
Every RECALL tag in the repo is a debt. The sourcer pays them: open the actual paper (PDF in
hand, not a text fetch), confirm or correct the value, and flip the tag to STANDARD with the
page/equation, or to DEAD with what the paper really says. First targets: DATUM.md eqs.
64–66 (is the 2.0 slope right, and at which M_h is 171.53 quoted?), the PDG-2024-era inputs
(M_t, M_h, α_s with the PDG edition), the Froggatt–Nielsen 1996 Higgs-mass prediction and
its error bar, the Shaposhnikov–Wetterich 2010 number, Weinberg 1987. One PR, one table:
claim, source, page, verdict.

## Steward (the owner)
Decides what merges, resolves competing designs, and can pull the floor (LEDGER S1) if the
breaker earns it. Sessions do not merge their own work.

## Coordinator
Keeps `STATUS.md` current (who holds which role, what is open, what blocks what), writes
and sharpens briefs, gives merge-readiness reads for the steward, and builds whatever no one
else is building. Does **not** review other sessions' work except at the steward's request:
a repo's author is the wrong critic for it. Currently held by the session that set up the
repo (Claude).

## Who should hold which role
Critic and breaker should be the models *least* like the authors of what they are checking,
and never the session that wrote the thing. Co-creator and visual can be anyone. One model
per role at a time; a session that wants to change role says so in `STATUS.md` first.

## Discipline, for every role
- Tier-tag every claim (LEDGER.md has the tags). Say recall / inference / guess where it matters.
- No flattery, no "great work." Findings only.
- Record corrections beside the original; never overwrite the record. The ledger grows.
- Run what you cite. If you cannot run it, say so and tag it RECALL.
- No personally identifying information about the owner or anyone, anywhere in the repo.
- Every file you add gets a line in the README's index, in the same change.
