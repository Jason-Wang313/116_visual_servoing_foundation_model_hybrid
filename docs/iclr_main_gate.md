# ICLR Main Gate

Paper: 116 visual_servoing_foundation_model_hybrid

v5 gate verdict: STRONG_REVISE

Evidence digest: visual-servo-foundation-hybrid-local-v5-expanded

## Passed Local Gates

- Hard success margin over retained v4 baseline: `0.06419 >= 0.030`.
- Hard utility margin: `0.13516 >= 0.050`.
- Override-precision delta: `0.07045 >= 0.030`.
- Unsafe-action delta: `-0.03636 <= -0.020`.
- Tracking, damage, latency, and calibration errors all decrease.
- Paired hard-utility wins: `10/10 >= 8/10`.
- Ablation success margin: `0.03195 >= 0.020`.
- Ablation utility margin: `0.06447 >= 0.040`.
- Stress endpoint margins are positive.
- Fixed-risk breach is zero and coverage is non-trivial.
- Numeric integrity, LaTeX/PDF, artifact-location, visual-QA, and citation-box gates pass.

## Remaining Main-Conference Blockers

- No real robot validation.
- No accepted external high-fidelity simulator benchmark.
- No released controller/foundation-policy checkpoint artifacts.
- No calibrated camera, Jacobian, latency, or deployment logs.
- No hardware rollout videos.
- Related work still needs complete manual full-paper synthesis.

The only honest main-conference-safe terminal state is STRONG_REVISE.
