# Child Status 116

Current stage: expanded-standard v5 terminal
Last update: 2026-06-23 16:23:00 +08:00
PDF: C:/Users/wangz/Downloads/116.pdf
PDF SHA256: CA7E461EA945742063982464BED4E7C1358F34F5881535AE1A0C664C849CA398
PDF pages: 27
Desktop copy present: no
GitHub: https://github.com/Jason-Wang313/116_visual_servoing_foundation_model_hybrid
Submission-hardening version: v5_expanded
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- `stability_calibrated_servo_foundation_arbiter_v5` beats retained v4 baseline `proposed_servo_foundation_arbiter_v4`.
- Hard success is `0.79741` vs `0.73322`; hard utility is `0.92520` vs `0.79004`.
- Paired hard-utility gain is `0.13516` with `10/10` seed wins.
- Override precision improves by `+0.07045`; unsafe actions, tracking error, damage, latency, and calibration error decrease.
- Ablation, stress endpoint, and fixed-risk gates pass.
- Strict fixed-risk coverage is `0.94313` with zero breach.
- Evidence scale: `409,600` main cells, `8,000` ablation cells, `48,000` stress cells, `51,200` fixed-risk cells, and `24` failure cases.
- Remaining blocker: no real robot or accepted high-fidelity validation, released controller/checkpoint artifacts, calibrated deployment logs, rollout videos, or complete manual related-work synthesis.
