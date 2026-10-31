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
Try to make the datum go away. Specifically:
- Find a defensible prior under which the near-criticality is unremarkable (p > 0.1).
- Find an error in the input values, the beta functions, or the RK4 that changes the shape.
- Argue that "three edges" is numerology of the Dirac-large-numbers kind: three unrelated
  smallnesses that look like a pattern because someone put them in one table.
- Attack any candidate in `03-candidates/` by showing its "prediction" was a postdiction
  with free parameters.
The breaker reports what survived as carefully as what broke. A breaker who breaks nothing
says so; that is a result.

## Visual
Make the figure that a reader needs in order to see the datum without reading the table:
λ(μ) with the uncertainty band and the three-loop literature band overlaid once that exists;
the "phase diagram" in the (M_h, M_t) plane with stable / metastable / unstable regions and
the measured point with its error ellipse (this is Fig. 1 of Buttazzo et al.; ours should
be computed here, not copied). Figures go in `figures/` with the script that made them.

## Steward (the owner)
Decides what merges, resolves competing designs, and can pull the floor (LEDGER S1) if the
breaker earns it. Sessions do not merge their own work.

## Discipline, for every role
- Tier-tag every claim (LEDGER.md has the tags). Say recall / inference / guess where it matters.
- No flattery, no "great work." Findings only.
- Record corrections beside the original; never overwrite the record. The ledger grows.
- Run what you cite. If you cannot run it, say so and tag it RECALL.
- No personally identifying information about the owner or anyone, anywhere in the repo.
- Every file you add gets a line in the README's index, in the same change.
