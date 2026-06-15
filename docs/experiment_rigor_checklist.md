# Experiment Rigor Checklist

## v4 Local Empirical Rigor

- [x] Paper-specific visual servo/foundation-policy hybrid benchmark.
- [x] 5 visual manipulation tasks.
- [x] 7 visual/geometry shift regimes.
- [x] 5 deployment splits.
- [x] 9 controllers including strong baselines and oracle upper bound.
- [x] 7 paired seeds and 84 rollout episodes per group.
- [x] Pairwise seed differences and win counts.
- [x] Stress sweep over visual aliasing and Jacobian mismatch with task/regime/seed detail.
- [x] Core ablations with a predeclared margin gate.
- [x] Eight failure cases, figures, and LaTeX tables.

## ICLR Main Remaining Gaps

- [ ] Real robot validation.
- [ ] External high-fidelity simulator benchmark.
- [ ] Released controller/checkpoint artifacts.
- [ ] Manual full-paper related-work synthesis.
- [ ] Hardware qualitative rollouts or failure videos.

Decision: STRONG_REVISE, not submission-ready.
