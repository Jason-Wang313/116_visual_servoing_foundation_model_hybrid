# Paper 116 Rebuild Plan

Started: 2026-06-15 03:14:00 +0100

## Goal

Rebuild `visual_servoing_foundation_model_hybrid` from an archive memo into a real local empirical submission package. The paper must test whether a calibrated arbitration layer can decide when classical image-based visual servoing should override a learned foundation-policy action decoder.

## Claim To Test

Foundation policies are useful for semantic reach and manipulation, while classical visual servo loops are safer for local image-error correction. A hybrid controller should switch based on action-critical visual error, geometry uncertainty, and servo stability margin, improving success under visual/geometry shift while reducing unsafe learned actions.

## Evidence Design

- Benchmark dimensions: 5 visual manipulation tasks, 7 visual/geometry shift regimes, 5 deployment splits, 9 controllers, 7 paired seeds, 84 rollout episodes per group.
- Methods: foundation policy only, classical IBVS only, position-based visual servoing, fixed hybrid switch, uncertainty-gated foundation policy, CBF safety shield, ensemble risk gate, proposed calibrated servo-foundation arbiter, and oracle arbiter.
- Metrics: task success, override precision, unsafe learned-action rate, tracking error, damage rate, latency/control cost, calibration error, and paired-seed wins.
- Stress sweep: increasing visual aliasing and servo Jacobian mismatch.
- Ablations: remove stability margin, remove action-critical visual error, remove geometry uncertainty, remove learned-action risk model, remove latency penalty, and threshold-only switch.

## Terminal Gates

The paper may become `STRONG_REVISE` only if all gates clear against the strongest non-oracle baseline:

- Combined-stress success margin is at least 0.030.
- Override precision increases by at least 0.030.
- Unsafe learned-action rate decreases by at least 0.020.
- Tracking error and damage do not increase.
- Latency/control cost does not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal decision remains `KILL_ARCHIVE` with the negative result documented.

## Execution Steps

1. Replace the generic branch scaffold with a visual-servo/foundation-policy hybrid benchmark.
2. Generate per-seed/task/regime/split evidence, aggregate metrics, pairwise tests, stress sweep, ablations, tables, and figures.
3. Remove stale branch-template artifacts if superseded.
4. Rewrite README, status docs, novelty docs, attack logs, reproducibility docs, and final audit around the v4 evidence.
5. Rewrite the manuscript as an ICLR-style evidence report with honest limitations.
6. Compile the PDF and copy `116.pdf` to Downloads only.
7. Audit Python, LaTeX, CSV finiteness, stale outputs, Git status, Downloads-only PDF placement, and GitHub visibility.
8. Update root reports only after Paper 116 reaches a terminal decision.
