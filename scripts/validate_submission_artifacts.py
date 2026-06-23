import csv
import hashlib
import json
import math
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS = Path.home() / "Downloads"
DESKTOP = Path.home() / "Desktop"

EXPECTED_COUNTS = {
    "dataset_summary": 160,
    "main_cell": 409600,
    "main_group": 2560,
    "seed_metric": 640,
    "metric": 64,
    "hard_seed": 160,
    "hard_metric": 16,
    "hard_pairwise": 15,
    "ablation_cell": 8000,
    "ablation_seed": 100,
    "ablation_metric": 10,
    "stress_cell": 48000,
    "stress_seed": 960,
    "stress_metric": 96,
    "fixed_risk_cell": 51200,
    "fixed_risk_seed": 320,
    "fixed_risk_metric": 32,
    "fixed_risk_pairwise": 28,
    "failure_cases": 24,
}

CSV_FILES = [
    "dataset_summary.csv",
    "cell_metrics.csv",
    "main_group_metrics.csv",
    "seed_metrics.csv",
    "metrics.csv",
    "hard_seed_metrics.csv",
    "hard_aggregate_metrics.csv",
    "hard_pairwise_stats.csv",
    "ablation_cell_metrics.csv",
    "ablation_seed_metrics.csv",
    "ablation_metrics.csv",
    "stress_sweep_cell_metrics.csv",
    "stress_sweep_seed_metrics.csv",
    "stress_sweep.csv",
    "fixed_risk_cell_metrics.csv",
    "fixed_risk_seed_metrics.csv",
    "fixed_risk_metrics.csv",
    "fixed_risk_pairwise_stats.csv",
    "failure_cases.csv",
]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def count_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def check_numeric_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            for key, value in row.items():
                if value is None or value == "":
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                check(math.isfinite(number), f"nonfinite numeric value in {path.name}:{row_number}:{key}")


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    check(summary["version"] == "v5_expanded", "wrong summary version")
    check(summary["terminal_decision"] == "STRONG_REVISE", "unexpected terminal decision")
    check(summary["local_gates_pass"] is True, "local gates did not pass")
    check(summary["iclr_main_ready"] is False, "ICLR readiness must remain false")
    check(summary["scope_gate_pass"] is False, "scope gate must fail without external evidence")
    for key, expected in EXPECTED_COUNTS.items():
        check(summary["row_counts"][key] == expected, f"row count mismatch for {key}")
    check(summary["strongest_non_oracle"] == "proposed_servo_foundation_arbiter_v4", "v4 must remain strongest named non-oracle comparator")
    check(summary["metrics"]["strict_fixed_risk_budget"] == 0.10, "strict fixed-risk budget must be 0.10")
    check(0.30 < summary["metrics"]["strict_fixed_risk_coverage"] < 0.95, "fixed-risk coverage should be meaningful, not automatic")
    check(summary["metrics"]["strict_fixed_risk_breach"] == 0.0, "strict fixed-risk breach must be zero")
    for gate, passed in summary["gates"].items():
        check(passed is True, f"gate failed: {gate}")

    for name in CSV_FILES:
        path = RESULTS / name
        check(path.exists(), f"missing CSV {name}")
        check(count_csv_rows(path) > 0, f"empty CSV {name}")
        check_numeric_csv(path)

    main_tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    check("pdfborder={0 0 1.4}" in main_tex, "bright citation boxes not configured")
    check("citebordercolor={0 0.82 0}" in main_tex, "bright cite border missing")
    check("generated_main_table.tex" in main_tex, "main generated table not included")
    check("STRONG\\_REVISE" in main_tex, "terminal decision missing from manuscript")

    paper_pdf = PAPER / "main.pdf"
    downloads_pdf = DOWNLOADS / "116.pdf"
    check(paper_pdf.exists(), "paper/main.pdf missing")
    check(downloads_pdf.exists(), "Downloads/116.pdf missing")
    check(not (DESKTOP / "116.pdf").exists(), "Desktop/116.pdf must be absent")
    check(not (ROOT / "116.pdf").exists(), "repo-root 116.pdf must be absent")
    pages = len(PdfReader(str(downloads_pdf)).pages)
    check(pages >= 25, f"PDF has only {pages} pages")
    digest = sha256(downloads_pdf)
    check(sha256(paper_pdf) == digest, "paper/main.pdf and Downloads/116.pdf differ")

    log_path = PAPER / "main.log"
    check(log_path.exists(), "LaTeX log missing")
    log_text = log_path.read_text(encoding="utf-8", errors="ignore")
    bad_patterns = [
        "Citation `",
        "undefined references",
        "There were undefined",
        "Rerun to get cross-references",
        "LaTeX Error",
        "Emergency stop",
        "Overfull \\hbox",
    ]
    for pattern in bad_patterns:
        check(pattern not in log_text, f"LaTeX log contains {pattern}")
    print(f"Paper 116 validation passed. SHA256={digest} pages={pages}")


if __name__ == "__main__":
    main()
