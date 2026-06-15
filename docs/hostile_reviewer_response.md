# Hostile Reviewer Response

## Reviewer Attack: Classical visual servoing already solves this.

Response: IBVS-only reaches `0.445` combined-stress success and PBVS reaches `0.463`, because classical loops fail under degeneracy, occlusion, and Jacobian mismatch.

## Reviewer Attack: A learned risk gate is enough.

Response: The strongest non-oracle baseline is `ensemble_risk_gate` at `0.598 +/- 0.008`. The proposed arbiter reaches `0.698 +/- 0.008`, a paired `0.100 +/- 0.007` gain with `7/7` seed wins.

## Reviewer Attack: The switch components may be decorative.

Response: Ablations reject that. The full method reaches `0.703 +/- 0.007`; the best removed-component variant reaches `0.666 +/- 0.008`.

## Reviewer Attack: The paper is not ready for ICLR main.

Response: Agreed. The honest decision is `STRONG_REVISE`, not ready. The v4.1 evidence has 5,880 detailed stress rows and 8 failure cases, but it still needs real robot or external high-fidelity validation and released controller artifacts.
