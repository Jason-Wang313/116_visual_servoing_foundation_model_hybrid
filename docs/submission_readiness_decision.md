# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

Reason: The v4 rebuild adds a paper-specific visual servo/foundation-policy hybrid benchmark with strong local evidence. The proposed arbiter beats `ensemble_risk_gate` by `0.100 +/- 0.007` combined-stress success, wins `7/7` paired seeds, improves override precision, lowers unsafe learned actions, tracking error, damage, and latency cost, and survives ablations.

Honest terminal action: keep and revise aggressively. Do not submit as final ICLR main paper until external validation is added.

Revival-to-ready condition: add real robot or accepted high-fidelity simulator experiments, release controller artifacts, compare to external visual servo/foundation-policy baselines, and deepen related work through manual full-paper reading.
