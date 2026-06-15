# ICLR Main Gate

Paper: 116 visual_servoing_foundation_model_hybrid

Existing v3 decision: KILL_ARCHIVE

v4 gate verdict: STRONG_REVISE

Evidence digest: visual-servo-foundation-hybrid-local-v4

## Passed Local Gates

- Success margin over strongest non-oracle baseline: `0.100 >= 0.030`.
- Override-precision delta: `0.092 >= 0.030`.
- Unsafe-action delta: `-0.065 <= -0.020`.
- Tracking-error delta: `-0.025 <= 0`.
- Damage delta: `-0.022 <= 0`.
- Latency-cost delta: `-0.022 <= 0`.
- Paired-seed wins: `7/7 >= 5/7`.
- Ablation margin: `0.037 >= 0.020`.

## Remaining Main-Conference Blockers

- No real robot validation.
- No external high-fidelity simulator benchmark.
- No released controller/checkpoint artifacts.
- Related work still needs manual full-paper synthesis.

The only honest main-conference-safe terminal state is STRONG_REVISE.
