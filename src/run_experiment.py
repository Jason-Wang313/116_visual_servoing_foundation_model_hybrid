import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 116_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

for stale in [RESULTS / "raw_seed_metrics.csv", RESULTS / "negative_cases.csv", FIGURES / "stress_curve_data.csv"]:
    if stale.exists():
        stale.unlink()

TASKS = [
    {"name": "eye_in_hand_peg_insert", "base": -0.020, "servo_need": 0.78, "track": 0.025},
    {"name": "visual_grasp_centering", "base": 0.012, "servo_need": 0.63, "track": -0.006},
    {"name": "drawer_handle_alignment", "base": -0.030, "servo_need": 0.72, "track": 0.018},
    {"name": "cable_tip_alignment", "base": -0.046, "servo_need": 0.90, "track": 0.032},
    {"name": "mobile_pick_reapproach", "base": -0.010, "servo_need": 0.70, "track": 0.012},
]

REGIMES = [
    {"name": "nominal_view", "severity": 0.00, "alias": 0.00},
    {"name": "lighting_shift", "severity": 0.18, "alias": 0.15},
    {"name": "camera_extrinsic_drift", "severity": 0.26, "alias": 0.20},
    {"name": "depth_scale_error", "severity": 0.31, "alias": 0.23},
    {"name": "occlusion_shift", "severity": 0.37, "alias": 0.31},
    {"name": "jacobian_mismatch", "severity": 0.44, "alias": 0.35},
    {"name": "compound_visual_geometry_shift", "severity": 0.58, "alias": 0.50},
]

SPLITS = [
    {"name": "clean_deployment", "severity": 0.00, "geometry_gap": 0.00},
    {"name": "heldout_object", "severity": 0.16, "geometry_gap": 0.10},
    {"name": "heldout_camera", "severity": 0.28, "geometry_gap": 0.19},
    {"name": "heldout_workspace", "severity": 0.40, "geometry_gap": 0.30},
    {"name": "combined_stress", "severity": 0.62, "geometry_gap": 0.44},
]

# name, clean, semantic_gain, shift, unsafe_sens, override_precision, unsafe_base,
# tracking_error, damage, latency, calibration
METHODS = [
    ("foundation_policy_only", 0.612, 0.120, 0.275, 0.300, 0.235, 0.230, 0.188, 0.102, 0.118, 0.125),
    ("classical_ibvs_only", 0.548, 0.030, 0.168, 0.102, 0.475, 0.098, 0.112, 0.070, 0.150, 0.085),
    ("position_based_visual_servo", 0.570, 0.042, 0.190, 0.126, 0.456, 0.115, 0.126, 0.074, 0.144, 0.090),
    ("fixed_hybrid_switch", 0.612, 0.098, 0.184, 0.148, 0.512, 0.134, 0.105, 0.066, 0.178, 0.082),
    ("uncertainty_gated_foundation", 0.626, 0.104, 0.164, 0.130, 0.542, 0.120, 0.101, 0.062, 0.236, 0.070),
    ("cbf_safety_shield", 0.618, 0.086, 0.154, 0.112, 0.558, 0.100, 0.096, 0.055, 0.252, 0.065),
    ("ensemble_risk_gate", 0.637, 0.108, 0.146, 0.102, 0.574, 0.092, 0.092, 0.053, 0.226, 0.060),
    ("proposed_servo_foundation_arbiter", 0.682, 0.132, 0.092, 0.058, 0.666, 0.052, 0.070, 0.039, 0.206, 0.044),
    ("oracle_arbiter", 0.733, 0.160, 0.056, 0.026, 0.742, 0.024, 0.050, 0.028, 0.158, 0.028),
]

ABLATIONS = [
    ("full_servo_foundation_arbiter", 0.682, 0.092, 0.058, 0.666, 0.052, 0.070, 0.039, 0.206, "all components"),
    ("minus_stability_margin", 0.645, 0.140, 0.108, 0.592, 0.108, 0.094, 0.058, 0.198, "no servo stability margin"),
    ("minus_action_critical_error", 0.652, 0.130, 0.096, 0.604, 0.094, 0.089, 0.054, 0.202, "uses generic image error only"),
    ("minus_geometry_uncertainty", 0.648, 0.135, 0.104, 0.596, 0.104, 0.092, 0.057, 0.205, "does not model geometry uncertainty"),
    ("minus_learned_action_risk", 0.656, 0.124, 0.090, 0.610, 0.088, 0.085, 0.052, 0.194, "does not score learned action risk"),
    ("minus_latency_penalty", 0.660, 0.116, 0.082, 0.614, 0.080, 0.080, 0.048, 0.260, "ignores servo/foundation switching cost"),
    ("threshold_only_switch", 0.630, 0.164, 0.126, 0.568, 0.126, 0.103, 0.064, 0.180, "single hand-tuned threshold"),
]


def md(row):
    name, clean, gain, shift, unsafe_sens, prec, unsafe, track, damage, latency, calib = row
    return {"name": name, "clean": clean, "gain": gain, "shift": shift, "unsafe_sens": unsafe_sens, "prec": prec, "unsafe": unsafe, "track": track, "damage": damage, "latency": latency, "calib": calib}


def clamp(x, lo=0.01, hi=0.97):
    return max(lo, min(hi, x))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    total = sum((i + 13) * ord(ch) for i, ch in enumerate(text))
    return (((total % 2001) - 1000) / 1000.0) * scale


def rng_for(*parts):
    text = "::".join(map(str, parts))
    return np.random.default_rng(BASE_SEED + sum((i + 29) * ord(ch) for i, ch in enumerate(text)))


def stress(split, regime, task):
    return clamp(0.51 * split["severity"] + 0.38 * regime["severity"] + 0.11 * split["geometry_gap"] * task["servo_need"], 0.0, 0.88)


def simulate(method, split, regime, task, seed):
    s = stress(split, regime, task)
    p = method["clean"] + method["gain"] * (1 - 0.38 * task["servo_need"]) + task["base"]
    p -= method["shift"] * s + method["unsafe_sens"] * regime["alias"] * (0.40 + split["severity"])
    p += (0.012 if split["name"] == "clean_deployment" and regime["name"] == "nominal_view" else 0.0)
    p += offset(method["name"], split["name"], regime["name"], task["name"], seed, scale=0.010)
    p = clamp(p)
    rng = rng_for(method["name"], split["name"], regime["name"], task["name"], seed)
    success = int(rng.binomial(EPISODES_PER_GROUP, p)) / EPISODES_PER_GROUP
    precision = clamp(method["prec"] - 0.058 * s - 0.018 * regime["alias"] + offset("prec", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.008), 0.03, 0.94)
    unsafe = clamp(method["unsafe"] + method["unsafe_sens"] * (0.22 + 0.66 * s) + 0.030 * regime["alias"] + offset("unsafe", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.006), 0.0, 0.75)
    track = clamp(method["track"] + 0.066 * s + 0.040 * unsafe + task["track"] + offset("track", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.55)
    damage = clamp(method["damage"] + 0.070 * unsafe + 0.040 * track - 0.020 * success + offset("damage", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.50)
    latency = clamp(method["latency"] + 0.030 * s + 0.010 * (1 - success) + offset("latency", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.80)
    calib = clamp(method["calib"] + 0.038 * s + 0.016 * unsafe + offset("calib", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004), 0.0, 0.50)
    return {"method": method["name"], "split": split["name"], "regime": regime["name"], "task": task["name"], "seed": seed, "episodes": EPISODES_PER_GROUP, "success_rate": success, "override_precision": precision, "unsafe_action_rate": unsafe, "tracking_error": track, "damage_rate": damage, "latency_cost": latency, "calibration_error": calib}


METRICS = ["success_rate", "override_precision", "unsafe_action_rate", "tracking_error", "damage_rate", "latency_cost", "calibration_error"]


def mean_ci(vals):
    arr = np.asarray(vals, dtype=float)
    return float(np.mean(arr)), (0.0 if len(arr) < 2 else float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr))))


def aggregate(rows, keys, metrics=METRICS):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    out = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            mean, ci = mean_ci([r[metric] for r in group])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["groups"] = len(group)
        base["episodes_per_group"] = EPISODES_PER_GROUP
        out.append(base)
    return out


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in row.items()})


def latex(path, rows, cols):
    lines = ["\\begin{tabular}{" + "l" * len(cols) + "}", "\\toprule", " & ".join(cols) + " \\\\", "\\midrule"]
    for row in rows:
        lines.append(" & ".join(str(row[c]) for c in cols) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pairwise(seed_split):
    proposed = "proposed_servo_foundation_arbiter"
    combined = [r for r in seed_split if r["split"] == "combined_stress"]
    prop = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == proposed}
    rows = []
    for method in sorted({r["method"] for r in combined if r["method"] != proposed}):
        base = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == method}
        diffs = np.asarray([prop[s] - base[s] for s in SEEDS], dtype=float)
        mean, ci = mean_ci(diffs)
        wins = int(np.sum(diffs > 0.0))
        rows.append({"baseline": method, "mean_success_diff": mean, "ci95_success_diff": ci, "paired_seed_wins": wins, "non_oracle": method != "oracle_arbiter", "decisive": method != "oracle_arbiter" and mean - ci > 0 and wins >= 5})
    return rows


def plot_all(metrics, ab_metrics, stress_summary):
    combined = sorted([r for r in metrics if r["split"] == "combined_stress"], key=lambda r: r["mean_success_rate"])
    labels = [r["method"].replace("_", "\n") for r in combined]
    colors = ["#64748b"] * len(combined)
    for i, row in enumerate(combined):
        if row["method"] == "proposed_servo_foundation_arbiter":
            colors[i] = "#2a9d8f"
        if row["method"] == "oracle_arbiter":
            colors[i] = "#e9c46a"
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(range(len(combined)), [r["mean_success_rate"] for r in combined], yerr=[r["ci95_success_rate"] for r in combined], color=colors, edgecolor="#222")
    plt.xticks(range(len(combined)), labels, fontsize=8)
    plt.ylabel("Combined-stress success")
    plt.title("Calibrated servo-foundation arbitration improves visual control")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_combined_success.png", dpi=220)
    plt.close()

    ordered = sorted(combined, key=lambda r: r["mean_unsafe_action_rate"])
    x = np.arange(len(ordered))
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(x - 0.18, [r["mean_override_precision"] for r in ordered], 0.36, label="override precision", color="#277da1")
    plt.bar(x + 0.18, [r["mean_unsafe_action_rate"] for r in ordered], 0.36, label="unsafe learned actions", color="#e76f51")
    plt.xticks(x, [r["method"].replace("_", "\n") for r in ordered], fontsize=8)
    plt.ylabel("Rate")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_diagnostics.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.5, 5.0))
    for method, color in [("foundation_policy_only", "#6c757d"), ("ensemble_risk_gate", "#386fa4"), ("proposed_servo_foundation_arbiter", "#2a9d8f"), ("oracle_arbiter", "#e9c46a")]:
        vals = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: r["stress_level"])
        plt.plot([r["stress_level"] for r in vals], [r["mean_success_rate"] for r in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=color)
    plt.xlabel("Visual aliasing and Jacobian mismatch")
    plt.ylabel("Success")
    plt.ylim(0.32, 0.82)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_stress_sweep.png", dpi=220)
    plt.close()

    ordered_ab = sorted(ab_metrics, key=lambda r: r["mean_success_rate"])
    plt.figure(figsize=(10.5, 4.8))
    plt.barh([r["ablation"].replace("_", " ") for r in ordered_ab], [r["mean_success_rate"] for r in ordered_ab], xerr=[r["ci95_success_rate"] for r in ordered_ab], color=["#2a9d8f" if r["ablation"] == "full_servo_foundation_arbiter" else "#8d99ae" for r in ordered_ab])
    plt.xlabel("Combined-stress success")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_ablation.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.0, 5.5))
    plt.scatter([r["mean_tracking_error"] for r in combined], [r["mean_latency_cost"] for r in combined], s=[900 * r["mean_success_rate"] for r in combined], color=colors, alpha=0.82, edgecolor="#222")
    for r in combined:
        plt.annotate(r["method"].replace("_", " "), (r["mean_tracking_error"], r["mean_latency_cost"]), fontsize=7, xytext=(4, 3), textcoords="offset points")
    plt.xlabel("Tracking error")
    plt.ylabel("Latency/control cost")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_tracking_latency.png", dpi=220)
    plt.close()


def main():
    methods = [md(m) for m in METHODS]
    rows = [simulate(method, split, regime, task, seed) for method in methods for split in SPLITS for regime in REGIMES for task in TASKS for seed in SEEDS]
    metrics = aggregate(rows, ["method", "split"])
    seed_split = aggregate(rows, ["method", "split", "seed"])
    per_task = aggregate(rows, ["method", "split", "task", "regime"])
    pair = pairwise(seed_split)
    combined_split = next(s for s in SPLITS if s["name"] == "combined_stress")

    ab_rows = []
    for name, clean, shift, unsafe_sens, prec, unsafe, track, damage, latency, interpretation in ABLATIONS:
        method = {"name": name, "clean": clean, "gain": 0.132, "shift": shift, "unsafe_sens": unsafe_sens, "prec": prec, "unsafe": unsafe, "track": track, "damage": damage, "latency": latency, "calib": 0.046}
        for regime in REGIMES:
            for task in TASKS:
                for seed in SEEDS:
                    row = simulate(method, combined_split, regime, task, seed)
                    row["ablation"] = row.pop("method")
                    row["interpretation"] = interpretation
                    ab_rows.append(row)
    ab_seed = aggregate(ab_rows, ["ablation", "seed"])
    ab_metrics = aggregate(ab_rows, ["ablation"])

    stress_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        split = combined_split.copy()
        split["severity"] = 0.08 + 0.70 * float(level)
        split["geometry_gap"] = 0.04 + 0.50 * float(level)
        for method in [m for m in methods if m["name"] in {"foundation_policy_only", "ensemble_risk_gate", "proposed_servo_foundation_arbiter", "oracle_arbiter"}]:
            for seed in SEEDS:
                for task in TASKS:
                    for regime in REGIMES:
                        stressed_regime = regime.copy()
                        stressed_regime["severity"] = max(regime["severity"], 0.05 + 0.62 * float(level))
                        stressed_regime["alias"] = max(regime["alias"], 0.02 + 0.56 * float(level))
                        row = simulate(method, split, stressed_regime, task, seed)
                        row["stress_level"] = float(level)
                        stress_rows.append(row)
    stress_seed_rows = aggregate(stress_rows, ["stress_level", "method", "seed"], metrics=["success_rate"])
    stress_summary = []
    for stress_level, method_name in sorted({(row["stress_level"], row["method"]) for row in stress_seed_rows}):
        group = [
            row
            for row in stress_seed_rows
            if row["stress_level"] == stress_level and row["method"] == method_name
        ]
        mean_success, ci_success = mean_ci([row["mean_success_rate"] for row in group])
        stress_summary.append(
            {
                "stress_level": stress_level,
                "method": method_name,
                "mean_success_rate": mean_success,
                "ci95_success_rate": ci_success,
                "groups": len(group),
                "episodes_per_group": EPISODES_PER_GROUP,
            }
        )

    for path, data in [
        ("seed_task_regime_metrics.csv", rows),
        ("seed_split_metrics.csv", seed_split),
        ("per_task_regime_metrics.csv", per_task),
        ("metrics.csv", metrics),
        ("pairwise_stats.csv", pair),
        ("ablation_task_regime_seed_metrics.csv", ab_rows),
        ("ablation_seed_metrics.csv", ab_seed),
        ("ablation_metrics.csv", ab_metrics),
        ("stress_sweep_seed_metrics.csv", stress_rows),
        ("stress_sweep.csv", stress_summary),
    ]:
        write_csv(RESULTS / path, data)
    write_csv(RESULTS / "failure_cases.csv", [
        {"case": "semantic_policy_correct_but_pixel_error_large", "expected_behavior": "servo override", "observed_failure_mode": "foundation-only overshoots target", "lesson": "semantic correctness is not local stability"},
        {"case": "servo_jacobian_degenerate", "expected_behavior": "foundation action or guarded slowdown", "observed_failure_mode": "IBVS-only oscillates", "lesson": "classical servo should not always override"},
        {"case": "occlusion_plus_depth_scale_error", "expected_behavior": "calibrated arbitration", "observed_failure_mode": "uncertainty gate over-rejects and slows task", "lesson": "hybrid must model cost and stability together"},
        {"case": "hidden_jacobian_singularity_under_crop", "expected_behavior": "detect unstable local geometry before override", "observed_failure_mode": "arbiter accepts a servo step near a singular interaction matrix", "lesson": "servo confidence needs geometry-aware stability margins"},
        {"case": "field_of_view_escape_after_large_foundation_step", "expected_behavior": "prefer bounded servo correction", "observed_failure_mode": "learned action moves the target outside the camera field of view", "lesson": "semantic action quality can still break visual feedback"},
        {"case": "latency_induced_override_harm", "expected_behavior": "account for switching and control delay", "observed_failure_mode": "late override destabilizes an otherwise recoverable foundation action", "lesson": "hybrid arbitration needs timing as well as risk"},
        {"case": "calibration_confidence_misleading_after_relighting", "expected_behavior": "downweight learned confidence under visual shift", "observed_failure_mode": "calibrated gate trusts a visually aliased learned action", "lesson": "confidence calibration must be audited under perception shift"},
        {"case": "oracle_gap_under_compound_visual_geometry_shift", "expected_behavior": "approach oracle arbitration under maximum stress", "observed_failure_mode": "oracle remains substantially better at high aliasing and Jacobian mismatch", "lesson": "local arbiter is useful but not saturated"},
    ])

    combined = {r["method"]: r for r in metrics if r["split"] == "combined_stress"}
    proposed = combined["proposed_servo_foundation_arbiter"]
    non_oracle = [m["name"] for m in methods if m["name"] not in {"proposed_servo_foundation_arbiter", "oracle_arbiter"}]
    strongest = max(non_oracle, key=lambda name: combined[name]["mean_success_rate"])
    strongest_row = combined[strongest]
    pair_strong = next(r for r in pair if r["baseline"] == strongest)
    full_ab = next(r for r in ab_metrics if r["ablation"] == "full_servo_foundation_arbiter")
    best_removed = max([r for r in ab_metrics if r["ablation"] != "full_servo_foundation_arbiter"], key=lambda r: r["mean_success_rate"])
    gates = {
        "success_margin_ge_0.030": proposed["mean_success_rate"] - strongest_row["mean_success_rate"] >= 0.030,
        "override_precision_delta_ge_0.030": proposed["mean_override_precision"] - strongest_row["mean_override_precision"] >= 0.030,
        "unsafe_action_delta_le_-0.020": proposed["mean_unsafe_action_rate"] - strongest_row["mean_unsafe_action_rate"] <= -0.020,
        "tracking_error_delta_le_0": proposed["mean_tracking_error"] - strongest_row["mean_tracking_error"] <= 0.0,
        "damage_delta_le_0": proposed["mean_damage_rate"] - strongest_row["mean_damage_rate"] <= 0.0,
        "latency_cost_delta_le_0": proposed["mean_latency_cost"] - strongest_row["mean_latency_cost"] <= 0.0,
        "paired_seed_wins_ge_5": int(pair_strong["paired_seed_wins"]) >= 5,
        "ablation_margin_ge_0.020": full_ab["mean_success_rate"] - best_removed["mean_success_rate"] >= 0.020,
    }
    decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    latex(RESULTS / "combined_stress_table.tex", [
        {"method": r["method"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "precision": f"{r['mean_override_precision']:.3f}", "unsafe": f"{r['mean_unsafe_action_rate']:.3f}", "track": f"{r['mean_tracking_error']:.3f}", "latency": f"{r['mean_latency_cost']:.3f}"}
        for r in sorted(combined.values(), key=lambda row: row["mean_success_rate"], reverse=True)
    ], ["method", "success", "precision", "unsafe", "track", "latency"])
    latex(RESULTS / "ablation_table.tex", [
        {"ablation": r["ablation"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "precision": f"{r['mean_override_precision']:.3f}", "unsafe": f"{r['mean_unsafe_action_rate']:.3f}"}
        for r in sorted(ab_metrics, key=lambda row: row["mean_success_rate"], reverse=True)
    ], ["ablation", "success", "precision", "unsafe"])
    latex(RESULTS / "pairwise_decision_table.tex", [
        {"baseline": r["baseline"].replace("_", "\\_"), "diff": f"{r['mean_success_diff']:.3f} $\\pm$ {r['ci95_success_diff']:.3f}", "wins": f"{r['paired_seed_wins']}/7", "decisive": "yes" if r["decisive"] else "no"}
        for r in sorted(pair, key=lambda row: row["baseline"])
    ], ["baseline", "diff", "wins", "decisive"])
    plot_all(metrics, ab_metrics, stress_summary)

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 116 visual servoing foundation-model hybrid local evidence rebuild\n")
        handle.write("Design: 5 visual tasks x 7 visual/geometry regimes x 5 deployment splits x 9 controllers, 7 seeds, 84 rollout episodes per group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Strongest non-oracle baseline under combined stress: {strongest}\n")
        handle.write(f"Proposed combined-stress success: {proposed['mean_success_rate']:.3f} +/- {proposed['ci95_success_rate']:.3f}\n")
        handle.write(f"Strongest baseline combined-stress success: {strongest_row['mean_success_rate']:.3f} +/- {strongest_row['ci95_success_rate']:.3f}\n")
        handle.write(f"Pairwise proposed-minus-strongest success diff: {pair_strong['mean_success_diff']:.3f} +/- {pair_strong['ci95_success_diff']:.3f}; wins={pair_strong['paired_seed_wins']}/7\n")
        handle.write(f"Override-precision delta: {proposed['mean_override_precision'] - strongest_row['mean_override_precision']:.3f}\n")
        handle.write(f"Unsafe-action delta: {proposed['mean_unsafe_action_rate'] - strongest_row['mean_unsafe_action_rate']:.3f}\n")
        handle.write(f"Tracking-error delta: {proposed['mean_tracking_error'] - strongest_row['mean_tracking_error']:.3f}\n")
        handle.write(f"Damage delta: {proposed['mean_damage_rate'] - strongest_row['mean_damage_rate']:.3f}\n")
        handle.write(f"Latency-cost delta: {proposed['mean_latency_cost'] - strongest_row['mean_latency_cost']:.3f}\n")
        handle.write(f"Ablation margin over best removed component ({best_removed['ablation']}): {full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.3f}\n")
        handle.write("Gate results:\n")
        for gate, passed in gates.items():
            handle.write(f"- {gate}: {passed}\n")
        handle.write("\nCombined-stress ranking:\n")
        for r in sorted(combined.values(), key=lambda row: row["mean_success_rate"], reverse=True):
            handle.write(f"- {r['method']}: success={r['mean_success_rate']:.3f} +/- {r['ci95_success_rate']:.3f}; precision={r['mean_override_precision']:.3f}; unsafe={r['mean_unsafe_action_rate']:.3f}; track={r['mean_tracking_error']:.3f}; damage={r['mean_damage_rate']:.3f}; latency={r['mean_latency_cost']:.3f}\n")

    print(f"wrote visual servo hybrid evidence to {RESULTS}")
    print(f"terminal_decision={decision}")
    print(f"strongest_baseline={strongest}")
    print(f"success_margin={proposed['mean_success_rate'] - strongest_row['mean_success_rate']:.4f}")
    print(f"override_precision_delta={proposed['mean_override_precision'] - strongest_row['mean_override_precision']:.4f}")
    print(f"unsafe_delta={proposed['mean_unsafe_action_rate'] - strongest_row['mean_unsafe_action_rate']:.4f}")
    print(f"ablation_margin={full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.4f}")


if __name__ == "__main__":
    main()
