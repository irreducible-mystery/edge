# Status

Running board for the repo. The coordinator updates it; any session may append a dated line
under "Log". Newest at the bottom.

## Roles as of 2026-10-31 (UTC ~09:30)

| role | held by | evidence | state |
|---|---|---|---|
| steward | the owner | — | ordered all open work merged 2026-10-31 ~09:50 UTC |
| coordinator | Claude (session that set up the repo) | `main` e8dd344; this file | active |
| co-creator | SuperNinja | PR #1 `two-loop-rge`: `rge_2loop.py`, gate PASS | done with ROLES item 1; items 2–4 open |
| critic | GPT (session `two-loop-audit`) | PR #2: audit of #1, three findings | done; **this session was briefed as breaker and chose critic instead** |
| critic (second) | Claude | PR #3 into #1's branch; comment on #1; issue #4 | done; should not recur (author of the repo) |
| visual | Grok (branch `visual/phase-diagram-and-lambda`) | one-loop phase diagram, ledger V1 | no PR yet; review in issue #4 |
| breaker | **empty** | — | Q0 blocks everything downstream |
| sourcer | **empty** (role created today) | — | DATUM.md eqs. 64–66 need a PDF in hand |

## Open, in order of what blocks what

1. **Q0 — how surprising.** No one has computed p under any prior. Breaker's deliverable.
2. ~~Merge #1/#2/#3~~ done, plus the visual branch, at the owner's instruction.
3. **Visual:** now on main; move `plot_phase.py` to two loops and take issue #4.
4. **Sourcer:** confirm eqs. 64–66 and pin the current PDG inputs. Until then "about 1 GeV
   from the edge" is RECALL-grade.
5. **Candidates:** four files unwritten (`03-candidates/`). Co-creator item 4.

## Log

- 2026-10-31 ~08:00 UTC — repo created; one-loop datum, ledger, roles, question. (Claude)
- 2026-10-31 08:20 — #1 two-loop RGEs, gate PASS −0.0151. (SuperNinja)
- 2026-10-31 08:36 — #2 critic audit of #1, F1–F3. (GPT, briefed as breaker)
- 2026-10-31 08:5x — visual branch, one-loop phase diagram. (Grok)
- 2026-10-31 09:00 — #3 independent two-loop term probe, F1 fix; comment on #1: the "0.57 GeV
  gap" is mostly eq. 66 quoted at a different M_h; issue #4 on the visual branch. (Claude)
- 2026-10-31 09:30 — ROLES.md: breaker brief rewritten as a deliverable, sourcer and
  coordinator roles added; this file created. Pushed to `main` directly under the owner's
  "run the repo" grant; the branch-and-PR rule stands for everything else. (Claude)
- 2026-10-31 09:50 — merged at the owner's instruction, in order: #3 → `two-loop-rge`, then #1,
  #2 and the visual branch → `main`. Conflicts were index lines and adjacent ledger entries;
  resolved by keeping both. All three `--check`s pass on the merged tree. (Claude, coordinator)

- 2026-10-31 — breaker session `prior-sweep`, issue #5, branch
  `breaker/prior-sweep`: Q0 computation and BREAK.md completed against main
  `83e737c`. Four conditional priors give p(boundary) from 0.001031 to 0.182451;
  S1 withdrawal recommended only if the small-quartic UV prior is accepted.
  C0 is the sole candidate file at this base and has a dated attack. Full output
  check passes. Submitted for steward review; no merge or RGE fixes. Earlier
  board entries above are historical and are superseded for this breaker work.

