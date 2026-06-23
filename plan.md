# Paper 116 v5 Expanded Rebuild Plan

Goal: rebuild `visual_servoing_foundation_model_hybrid` into an expanded, hostile-review-ready local submission package while keeping the honest terminal state. The final PDF must be at least 25 pages, use bright boxed clickable citations, live as `C:/Users/wangz/Downloads/116.pdf` only, and have a matching public GitHub repo update.

## Frozen Protocol

- Keep CPU-only and RAM-light execution: deterministic NumPy/Pandas-free generator, single-process plotting, no large model downloads, no GPU assumptions.
- Treat the old v4.1 `proposed_servo_foundation_arbiter` as a named strong non-oracle baseline rather than erasing it.
- Add a new v5 method, `stability_calibrated_servo_foundation_arbiter_v5`, with explicit terms for action-critical visual error, Jacobian margin, foundation-action risk, calibration error, latency, and fixed-risk deployment.
- Expand the main matrix to strong baselines, paired seeds, task/regime/split cells, hard slices, ablations, stress sweeps, fixed-risk budgets, and documented failure cases.
- Freeze gates before final interpretation: success, utility, override precision, unsafe-action reduction, tracking/damage/latency non-increase, paired-seed wins, ablation margin, stress endpoint margin, fixed-risk breach, and positive fixed-risk coverage.

## Evidence Targets

- Produce a 25+ page ICLR-style manuscript with generated tables, theory sections, failure analysis, scope gate, and appendix cards.
- Generate CSVs for main cells, grouped metrics, seed metrics, hard aggregate, paired tests, ablations, stress sweep, fixed-risk audit, and failure cases.
- Generate figures for hard-slice success, safety/utility tradeoff, ablations, stress sweep, and fixed-risk behavior.
- Validate PDF page count, hash, citation-box configuration, LaTeX log cleanliness, row counts, numeric integrity, artifact placement, and root-status compatibility.

## Honesty Gate

- Do not mark ICLR-main ready unless external evidence exists.
- Expected final decision is `STRONG_REVISE`, not `READY`, because this repo lacks real robot validation, accepted high-fidelity simulator validation, released controller/checkpoint artifacts, calibrated deployment logs, rollout videos, and a complete manual full-paper related-work synthesis.

## Execution Order

1. Replace the old v4 experiment with the frozen v5 deterministic experiment generator.
2. Add manuscript and artifact validators.
3. Generate all v5 results, figures, tables, `summary.json`, and audit docs.
4. Generate and compile the 25+ page PDF with bright citation boxes.
5. Copy the numbered PDF to Downloads only and verify no Desktop/root numbered copies exist.
6. Run validators and visual PDF QA.
7. Commit and push the public repo.
8. Update root ledgers and stale-scan for Paper 116.
