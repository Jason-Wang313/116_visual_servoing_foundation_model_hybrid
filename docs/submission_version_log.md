# Submission Version Log

## v1

Generated draft scaffold.

## v2

Workshop-level synthetic stress-test pass.

## v3

ICLR-main gate archive pass. Decision: KILL_ARCHIVE because the paper lacked paper-specific empirical evidence, implemented baselines, and real robot/high-fidelity validation.

## v4

Rebuilt as a visual servo/foundation-policy hybrid empirical package. Added paper-specific benchmark, strong baselines, paired-seed tests, stress sweep, ablations, figures, tables, revised docs, and an evidence manuscript.

Terminal decision: STRONG_REVISE.

Remaining gap: real robot or external high-fidelity validation.

## v4.1

Reran the experiment under low-RAM thread caps, expanded `stress_sweep_seed_metrics.csv` to 5,880 task/regime/seed rows, expanded `failure_cases.csv` to 8 documented boundaries, rechecked row counts and numeric integrity, and hardened manuscript/docs around the same evidence-bound terminal state.

Terminal decision: STRONG_REVISE.

Remaining gap: real robot or independent high-fidelity validation, released controller/checkpoint artifacts, and deeper manual related-work synthesis.
