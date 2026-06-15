# Novelty Boundary Map

## Inside The Claim

- Calibrated arbitration between learned action decoding and visual servo correction.
- Action-critical visual error and geometry uncertainty.
- Servo stability margin and learned-action risk.
- Latency-aware switching.
- Downstream control metrics under visual/geometry shift.

## Outside The Claim

- New visual servoing theory.
- Real hardware SOTA.
- Universal VLA safety.
- Replacing CBF shields.
- External benchmark generality.

## Closest Baseline Boundary

The closest local competitor is `ensemble_risk_gate`. It detects risky learned actions but does not model servo stability and action-critical visual error jointly. The proposed arbiter wins by `0.100 +/- 0.007` combined-stress success.
