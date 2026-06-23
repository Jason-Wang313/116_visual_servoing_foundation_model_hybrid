# Paper 116 Expanded Submission Plan

Date: 2026-06-23

Paper: `116_visual_servoing_foundation_model_hybrid`

Objective: transform the earlier short report into a 25+ page v5 expanded submission audit with maximal local rigor under CPU-only, RAM-light constraints.

## Reviewer-Threat Model

- A hostile reviewer will ask whether the method is just a nicer switch between learned actions and visual servoing.
- A hostile reviewer will ask whether the old v4 method is hidden rather than beaten.
- A hostile reviewer will ask whether success gains come with worse unsafe learned actions, tracking error, damage, latency, or calibration.
- A hostile reviewer will ask whether gains survive compound visual shift, Jacobian mismatch, occlusion, depth-scale error, field-of-view loss, and latency.
- A hostile reviewer will ask whether the result is submission-ready without real robot or high-fidelity evidence.

## Planned Response

- Keep v4 as a named baseline and require v5 to beat it on hard success and hard utility.
- Include foundation-only, IBVS, PBVS, fixed switching, uncertainty gating, CBF shielding, ensemble risk gating, robust MPC handoff, conformal abstention, model-predictive servoing, learned residual servoing, v4, v5, and oracle variants.
- Add theory that defines arbitration risk, a stability margin, a fixed-risk selector, and a negative identifiability result showing why image uncertainty alone is insufficient.
- Add seed-level paired tests and fixed-risk deployment accounting so the method cannot win by accepting every hard case.
- Make the scope gate explicit: even a strong local result is `STRONG_REVISE` without external validation.

## Frozen Deliverables

- `results/summary.json` with `version = v5_expanded`, `terminal_decision = STRONG_REVISE`, `iclr_main_ready = false`, and `scope_gate_pass = false`.
- CSVs for main, hard-slice, ablation, stress, fixed-risk, and failure-case evidence.
- Generated tables in `paper/`.
- Bright boxed clickable citations using `hyperref` border settings.
- Validated `paper/main.pdf` and `C:/Users/wangz/Downloads/116.pdf` with identical SHA256.
- Updated child docs, public GitHub commit, and root ledgers.
