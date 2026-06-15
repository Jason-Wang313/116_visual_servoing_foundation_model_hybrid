# Submission Readiness Audit v4.1

Paper: 116 `visual_servoing_foundation_model_hybrid`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\116_visual_servoing_foundation_model_hybrid_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 24 rows.
- `stress_sweep_seed_metrics.csv`: 5,880 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `ensemble_risk_gate`.
- Combined-stress success: `0.698 +/- 0.008` proposed vs `0.598 +/- 0.008` baseline.
- Paired success gain: `0.100 +/- 0.007`, 7/7 seed wins.
- Override precision: `0.633` proposed vs `0.542` baseline.
- Unsafe learned action rate: `0.089` proposed vs `0.154` baseline.
- Tracking error: `0.121` proposed vs `0.145` baseline.
- Damage rate: `0.036` proposed vs `0.058` baseline.
- Latency cost: `0.222` proposed vs `0.244` baseline.
- Ablation margin over best removed component: `0.037`.
- Max stress success: `0.655 +/- 0.004` proposed vs `0.518 +/- 0.005` ensemble risk and `0.773 +/- 0.005` oracle.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/116.pdf`.
- PDF SHA256: `AC3D68DDC3424ECCE788994F5B6147232F5A6FF50EE9C6C4454D9B2A207FA91D`.
- PDF size: `385597` bytes.
- Desktop PDF copy: absent.
- LaTeX/BibTeX scan: clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, override-precision gain, unsafe-action/tracking/damage/latency reductions, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real robot or independent high-fidelity validation, controller/checkpoint release, hardware/video artifacts, and deeper manual related-work synthesis before submission.
