# Final Audit

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Local Evidence

- Hard success: `0.79741` proposed vs `0.73322` strongest non-oracle.
- Hard utility: `0.92520` proposed vs `0.79004` strongest non-oracle.
- Paired hard-utility wins: `10/10`.
- Override precision delta: `+0.07045`.
- Unsafe-action delta: `-0.03636`.
- Tracking-error delta: `-0.01964`.
- Damage delta: `-0.01331`.
- Latency delta: `-0.02029`.
- Calibration-error delta: `-0.01735`.
- Ablation success/utility margins: `+0.03195` and `+0.06447`.
- Stress endpoint success/utility margins: `+0.07524` and `+0.14991`.
- Strict fixed-risk coverage/breach/utility margin: `0.94313`, `0.00000`, `+0.32190`.
- Final PDF SHA256: `CA7E461EA945742063982464BED4E7C1358F34F5881535AE1A0C664C849CA398`.

## Scope Failure

The scope gate fails because the package is synthetic/local only and lacks real robot or accepted high-fidelity validation and release artifacts.
