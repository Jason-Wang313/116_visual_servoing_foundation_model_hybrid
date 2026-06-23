# 116 Visual Servoing Foundation-Model Hybrid

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This v5 rebuild expands the earlier short report into a 27-page local submission audit for stability-calibrated arbitration between foundation-policy actions and classical visual servo loops. The local result is strong, but the paper is still not ICLR-main ready because it lacks real robot or accepted high-fidelity validation.

## Evidence Snapshot

- Proposed method: `stability_calibrated_servo_foundation_arbiter_v5`.
- Strongest non-oracle baseline retained by name: `proposed_servo_foundation_arbiter_v4`.
- Hard success: `0.79741` proposed vs `0.73322` strongest non-oracle.
- Hard utility: `0.92520` proposed vs `0.79004` strongest non-oracle.
- Paired hard-utility gain: `0.13516`, wins `10/10` seeds.
- Override-precision delta: `+0.07045`.
- Unsafe-action delta: `-0.03636`.
- Tracking-error delta: `-0.01964`; damage delta: `-0.01331`; latency delta: `-0.02029`; calibration delta: `-0.01735`.
- Ablation margin: `+0.03195` success and `+0.06447` utility over the best ablation.
- Stress endpoint margin: `+0.07524` success and `+0.14991` utility.
- Strict fixed-risk budget: `0.10`; coverage `0.94313`; breach `0.00000`; fixed-risk utility margin `0.32190`.
- Row counts: `409,600` main cells, `8,000` ablation cells, `48,000` stress cells, `51,200` fixed-risk cells, and `24` failure cases.
- Final PDF: `C:/Users/wangz/Downloads/116.pdf`, 27 pages, SHA256 `CA7E461EA945742063982464BED4E7C1358F34F5881535AE1A0C664C849CA398`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Validate

```powershell
python scripts\validate_submission_artifacts.py
```

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
