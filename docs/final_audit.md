# Final Audit

Paper: 116 visual_servoing_foundation_model_hybrid

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE

## Evidence

The archive scaffold was replaced with a visual servo/foundation-policy hybrid benchmark. The benchmark evaluates 5 visual tasks, 7 visual/geometry regimes, 5 deployment splits, 9 controllers, 7 seeds, and 84 rollout episodes per group. The proposed calibrated arbiter beats the strongest non-oracle baseline, `ensemble_risk_gate`, under combined stress.

Key results:
- Success: `0.698 +/- 0.008` proposed vs `0.598 +/- 0.008` strongest baseline.
- Paired difference: `0.100 +/- 0.007`; wins `7/7`.
- Override-precision delta: `+0.092`.
- Unsafe-action delta: `-0.065`.
- Tracking-error delta: `-0.025`.
- Damage delta: `-0.022`.
- Latency-cost delta: `-0.022`.
- Best ablation gap: `0.037`.
- Stress sweep coverage: `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure cases: `8` documented visual-servo/foundation-policy boundary cases.
- Numeric integrity: no NaN or infinite values found across result CSVs.
- Canonical PDF: `C:/Users/wangz/Downloads/116.pdf`.
- PDF SHA256: `AC3D68DDC3424ECCE788994F5B6147232F5A6FF50EE9C6C4454D9B2A207FA91D`.
- PDF size: `385597` bytes.
- Desktop PDF copy: absent.

## Remaining Risk

The result is local benchmark evidence. It lacks real robot experiments, external high-fidelity simulator transfer, released controller artifacts, and hardware videos. The correct terminal action is strong revise, not ICLR-main-ready submission.
