# Submission Readiness Audit v5

Paper: 116 `visual_servoing_foundation_model_hybrid`

Date: 2026-06-23

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Integrity Gates

- `cell_metrics.csv`: 409,600 rows.
- `main_group_metrics.csv`: 2,560 rows.
- `seed_metrics.csv`: 640 rows.
- `hard_aggregate_metrics.csv`: 16 rows.
- `hard_pairwise_stats.csv`: 15 rows.
- `ablation_cell_metrics.csv`: 8,000 rows.
- `stress_sweep_cell_metrics.csv`: 48,000 rows.
- `fixed_risk_cell_metrics.csv`: 51,200 rows.
- `failure_cases.csv`: 24 rows.
- Numeric sanity: validator passed.

## Result Gates

- Strongest non-oracle baseline: `proposed_servo_foundation_arbiter_v4`.
- Hard success: `0.79741` proposed vs `0.73322` baseline.
- Hard utility: `0.92520` proposed vs `0.79004` baseline.
- Paired hard-utility gain: `0.13516`, wins `10/10` seeds.
- Strict fixed-risk coverage/breach: `0.94313` / `0.00000`.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/116.pdf`.
- PDF SHA256: `CA7E461EA945742063982464BED4E7C1358F34F5881535AE1A0C664C849CA398`.
- PDF pages: 27.
- Desktop PDF copy: absent.
- Bright boxed clickable citations: present.
- Visual PDF QA: pages 1, 4, 9, 16, 23, and 27 rendered and inspected.

## Submission Decision

The local evidence clears the strong-revise gate. The paper is not ICLR-main ready because real robot/high-fidelity validation and release artifacts are absent.
