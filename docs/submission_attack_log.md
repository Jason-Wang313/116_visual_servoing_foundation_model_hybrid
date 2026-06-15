# Submission Attack Log

Paper: 116 visual_servoing_foundation_model_hybrid

This v4.1 pass replaces the v3 archive decision with a local empirical rebuild and expanded continuation audit. The result is `STRONG_REVISE`, not final ICLR-main readiness.

## Attack 1: No real robot validation.

Verdict: Still a blocker for readiness.

Action: Preserve `ICLR main ready: no`.

## Attack 2: Classical visual servoing novelty is crowded.

Verdict: Addressed locally.

Action: Reframed around calibrated arbitration between servo loops and foundation actions.

## Attack 3: Weak baselines.

Verdict: Addressed locally.

Action: Added foundation-only, IBVS, PBVS, fixed hybrid, uncertainty gate, CBF shield, ensemble risk gate, and oracle arbiter.

## Attack 4: Ensemble risk gate may be enough.

Verdict: Addressed locally.

Action: Proposed beats ensemble risk by `0.100 +/- 0.007`, wins `7/7` seeds, and improves precision/safety/tracking/cost diagnostics.

## Attack 5: Components may be unnecessary.

Verdict: Addressed locally.

Action: Best ablation trails the full method by `0.037`, clearing the `0.020` gate.

## Attack 6: Missing controller/checkpoints.

Verdict: Still a blocker for readiness.

Action: Document as required next evidence.

## Attack 7: Main-conference decision.

Verdict: STRONG_REVISE.

Action: Keep and expand; do not mark as submission-ready.

## Attack 8: Stress/failure coverage is thin.

Verdict: Addressed locally in v4.1.

Action: Expanded stress evidence to `5,880` task/regime/seed rows and failure documentation to `8` concrete visual-servo/foundation-policy boundary cases.
