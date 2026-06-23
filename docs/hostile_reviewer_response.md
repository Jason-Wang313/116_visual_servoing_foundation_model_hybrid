# Hostile Reviewer Response

## Attack: The method is just a switch.

Response: The v5 method reports explicit stability, action-risk, calibration, latency, and fixed-risk components, then ablates them. The full method beats the best ablation by `0.03195` success and `0.06447` utility.

## Attack: The old v4 result is hidden.

Response: The retained v4 method `proposed_servo_foundation_arbiter_v4` is the strongest non-oracle comparator and is beaten directly: hard success `0.79741` vs `0.73322`, hard utility `0.92520` vs `0.79004`.

## Attack: The method wins by being unsafe.

Response: Unsafe-action rate decreases by `0.03636`, tracking error by `0.01964`, damage by `0.01331`, latency by `0.02029`, and calibration error by `0.01735`.

## Attack: Fixed-risk deployment is cosmetic.

Response: The strict budget `0.10` has non-trivial coverage `0.94313`, zero breach, and positive utility margin `0.32190`.

## Attack: This is still not a real robotics submission.

Response: Agreed. The terminal state is STRONG_REVISE, not ready. The scope gate fails without real robot or accepted high-fidelity validation and release artifacts.
