# 116 Visual Servoing Foundation-Model Hybrid

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive/template scaffold with a paper-specific local benchmark for calibrated arbitration between foundation-policy actions and classical visual servo loops. The evidence supports a strong-revise direction, but the paper is not yet ICLR-main ready because it lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 5 visual manipulation tasks x 7 visual/geometry regimes x 5 deployment splits x 9 controllers, 7 paired seeds, 84 rollout episodes per group.
- Strongest non-oracle baseline: `ensemble_risk_gate`.
- Combined-stress success: proposed `0.698 +/- 0.008` vs baseline `0.598 +/- 0.008`.
- Paired difference: `0.100 +/- 0.007`, wins `7/7` seeds.
- Override-precision delta: `+0.092`.
- Unsafe learned-action delta: `-0.065`.
- Tracking-error delta: `-0.025`; damage delta: `-0.022`; latency-cost delta: `-0.022`.
- Best ablation gap: `0.037`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/116.pdf`
