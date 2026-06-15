# Child Status 116

Current stage: ICLR main gate terminal
Last update: 2026-06-15 20:16:20 +0100
PDF: C:/Users/wangz/Downloads/116.pdf
PDF SHA256: AC3D68DDC3424ECCE788994F5B6147232F5A6FF50EE9C6C4454D9B2A207FA91D
PDF size: 385597 bytes
Desktop copy present: no
GitHub: https://github.com/Jason-Wang313/116_visual_servoing_foundation_model_hybrid
Submission-hardening version: v4.1
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed servo-foundation arbiter beats `ensemble_risk_gate` by `0.100 +/- 0.007` combined-stress success with `7/7` paired-seed wins.
- Proposed success is `0.698 +/- 0.008`; strongest baseline success is `0.598 +/- 0.008`.
- Override precision increases; unsafe learned actions, tracking error, damage, and latency cost decrease.
- Best ablation trails the full method by `0.037` success.
- Stress sweep now covers `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure-case documentation now covers `8` visual-servo/foundation-policy boundary cases.
- Remaining blocker: no real robot or external high-fidelity benchmark validation.
