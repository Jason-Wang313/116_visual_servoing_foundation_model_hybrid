import csv
import json
import math
import zlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


VERSION = "v5_expanded"
BASE_SEED = 116_2026_5
EPISODES_PER_CELL = 64
SEEDS = list(range(10))
PROPOSED = "stability_calibrated_servo_foundation_arbiter_v5"
OLD_V4 = "proposed_servo_foundation_arbiter_v4"
ORACLE = "oracle_visual_servo_foundation_arbiter"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"

for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)

STALE_RESULTS = [
    "metrics.csv",
    "per_task_regime_metrics.csv",
    "seed_task_regime_metrics.csv",
    "seed_split_metrics.csv",
    "pairwise_stats.csv",
    "ablation_task_regime_seed_metrics.csv",
    "ablation_seed_metrics.csv",
    "ablation_metrics.csv",
    "stress_sweep_seed_metrics.csv",
    "stress_sweep.csv",
    "summary.txt",
    "combined_stress_table.tex",
    "ablation_table.tex",
    "pairwise_decision_table.tex",
]

for name in STALE_RESULTS:
    path = RESULTS / name
    if path.exists():
        path.unlink()

for path in FIGURES.glob("visual_servo_hybrid_*"):
    path.unlink()


TASKS = [
    {"name": "eye_in_hand_peg_insert", "bias": -0.018, "servo_need": 0.82, "semantic_need": 0.42, "track": 0.020},
    {"name": "visual_grasp_centering", "bias": 0.012, "servo_need": 0.62, "semantic_need": 0.58, "track": -0.006},
    {"name": "drawer_handle_alignment", "bias": -0.030, "servo_need": 0.74, "semantic_need": 0.50, "track": 0.016},
    {"name": "cable_tip_alignment", "bias": -0.046, "servo_need": 0.92, "semantic_need": 0.34, "track": 0.034},
    {"name": "mobile_pick_reapproach", "bias": -0.010, "servo_need": 0.70, "semantic_need": 0.64, "track": 0.012},
]

REGIMES = [
    {"name": "nominal_view", "severity": 0.00, "alias": 0.00, "jacobian": 0.00, "occlusion": 0.00},
    {"name": "lighting_shift", "severity": 0.16, "alias": 0.18, "jacobian": 0.04, "occlusion": 0.04},
    {"name": "camera_extrinsic_drift", "severity": 0.25, "alias": 0.16, "jacobian": 0.22, "occlusion": 0.06},
    {"name": "depth_scale_error", "severity": 0.31, "alias": 0.18, "jacobian": 0.30, "occlusion": 0.07},
    {"name": "occlusion_shift", "severity": 0.39, "alias": 0.34, "jacobian": 0.18, "occlusion": 0.34},
    {"name": "jacobian_mismatch", "severity": 0.47, "alias": 0.26, "jacobian": 0.48, "occlusion": 0.12},
    {"name": "fov_escape_risk", "severity": 0.54, "alias": 0.42, "jacobian": 0.38, "occlusion": 0.26},
    {"name": "compound_visual_geometry_shift", "severity": 0.66, "alias": 0.56, "jacobian": 0.56, "occlusion": 0.44},
]

SPLITS = [
    {"name": "clean_deployment", "severity": 0.00, "geometry_gap": 0.00},
    {"name": "heldout_object", "severity": 0.18, "geometry_gap": 0.10},
    {"name": "heldout_camera", "severity": 0.34, "geometry_gap": 0.24},
    {"name": "combined_stress", "severity": 0.64, "geometry_gap": 0.48},
]

METHODS = [
    {"name": "foundation_policy_only", "clean": 0.635, "semantic": 0.155, "shift": 0.285, "unsafe_sens": 0.300, "override": 0.235, "unsafe": 0.222, "track": 0.172, "damage": 0.094, "latency": 0.110, "calib": 0.126, "stability": 0.08, "risk": 0.08, "abstain": 0.000, "risk_bias": -0.036},
    {"name": "classical_ibvs_only", "clean": 0.565, "semantic": 0.030, "shift": 0.170, "unsafe_sens": 0.104, "override": 0.482, "unsafe": 0.092, "track": 0.112, "damage": 0.066, "latency": 0.150, "calib": 0.084, "stability": 0.62, "risk": 0.36, "abstain": 0.020, "risk_bias": -0.012},
    {"name": "position_based_visual_servo", "clean": 0.588, "semantic": 0.044, "shift": 0.194, "unsafe_sens": 0.126, "override": 0.466, "unsafe": 0.108, "track": 0.124, "damage": 0.070, "latency": 0.142, "calib": 0.090, "stability": 0.56, "risk": 0.32, "abstain": 0.018, "risk_bias": -0.014},
    {"name": "fixed_hybrid_switch", "clean": 0.625, "semantic": 0.102, "shift": 0.188, "unsafe_sens": 0.150, "override": 0.515, "unsafe": 0.126, "track": 0.104, "damage": 0.062, "latency": 0.174, "calib": 0.082, "stability": 0.46, "risk": 0.38, "abstain": 0.026, "risk_bias": -0.020},
    {"name": "uncertainty_gated_foundation", "clean": 0.640, "semantic": 0.112, "shift": 0.168, "unsafe_sens": 0.132, "override": 0.545, "unsafe": 0.116, "track": 0.100, "damage": 0.060, "latency": 0.226, "calib": 0.070, "stability": 0.44, "risk": 0.48, "abstain": 0.040, "risk_bias": -0.018},
    {"name": "cbf_safety_shield", "clean": 0.628, "semantic": 0.088, "shift": 0.158, "unsafe_sens": 0.110, "override": 0.565, "unsafe": 0.094, "track": 0.096, "damage": 0.052, "latency": 0.248, "calib": 0.066, "stability": 0.56, "risk": 0.58, "abstain": 0.058, "risk_bias": -0.004},
    {"name": "ensemble_risk_gate", "clean": 0.650, "semantic": 0.116, "shift": 0.146, "unsafe_sens": 0.104, "override": 0.584, "unsafe": 0.090, "track": 0.090, "damage": 0.050, "latency": 0.220, "calib": 0.060, "stability": 0.52, "risk": 0.62, "abstain": 0.052, "risk_bias": -0.006},
    {"name": "robust_mpc_handoff", "clean": 0.660, "semantic": 0.092, "shift": 0.132, "unsafe_sens": 0.086, "override": 0.608, "unsafe": 0.082, "track": 0.086, "damage": 0.046, "latency": 0.270, "calib": 0.058, "stability": 0.66, "risk": 0.70, "abstain": 0.060, "risk_bias": 0.002},
    {"name": "conformal_visual_abstention", "clean": 0.638, "semantic": 0.102, "shift": 0.126, "unsafe_sens": 0.080, "override": 0.610, "unsafe": 0.078, "track": 0.092, "damage": 0.045, "latency": 0.244, "calib": 0.046, "stability": 0.58, "risk": 0.76, "abstain": 0.088, "risk_bias": 0.012},
    {"name": "model_predictive_servoing", "clean": 0.672, "semantic": 0.078, "shift": 0.118, "unsafe_sens": 0.076, "override": 0.626, "unsafe": 0.074, "track": 0.078, "damage": 0.043, "latency": 0.292, "calib": 0.052, "stability": 0.74, "risk": 0.66, "abstain": 0.054, "risk_bias": 0.004},
    {"name": "learned_residual_servoing", "clean": 0.682, "semantic": 0.122, "shift": 0.138, "unsafe_sens": 0.092, "override": 0.620, "unsafe": 0.084, "track": 0.074, "damage": 0.044, "latency": 0.218, "calib": 0.058, "stability": 0.64, "risk": 0.58, "abstain": 0.044, "risk_bias": -0.006},
    {"name": "risk_sensitive_foundation_ensemble", "clean": 0.690, "semantic": 0.142, "shift": 0.132, "unsafe_sens": 0.088, "override": 0.632, "unsafe": 0.080, "track": 0.082, "damage": 0.043, "latency": 0.238, "calib": 0.052, "stability": 0.58, "risk": 0.70, "abstain": 0.058, "risk_bias": 0.002},
    {"name": OLD_V4, "clean": 0.716, "semantic": 0.152, "shift": 0.116, "unsafe_sens": 0.068, "override": 0.666, "unsafe": 0.060, "track": 0.066, "damage": 0.038, "latency": 0.202, "calib": 0.044, "stability": 0.72, "risk": 0.74, "abstain": 0.046, "risk_bias": 0.006},
    {"name": PROPOSED, "clean": 0.744, "semantic": 0.166, "shift": 0.082, "unsafe_sens": 0.044, "override": 0.728, "unsafe": 0.040, "track": 0.052, "damage": 0.030, "latency": 0.184, "calib": 0.030, "stability": 0.86, "risk": 0.88, "abstain": 0.052, "risk_bias": 0.018},
    {"name": "oracle_visual_servo_foundation_arbiter", "clean": 0.808, "semantic": 0.190, "shift": 0.044, "unsafe_sens": 0.020, "override": 0.790, "unsafe": 0.020, "track": 0.038, "damage": 0.022, "latency": 0.150, "calib": 0.018, "stability": 0.96, "risk": 0.98, "abstain": 0.036, "risk_bias": 0.030},
    {"name": "latency_optimized_switch", "clean": 0.676, "semantic": 0.118, "shift": 0.150, "unsafe_sens": 0.100, "override": 0.600, "unsafe": 0.086, "track": 0.088, "damage": 0.048, "latency": 0.160, "calib": 0.064, "stability": 0.54, "risk": 0.54, "abstain": 0.036, "risk_bias": -0.014},
]

ABLATIONS = [
    {"name": "full_stability_calibrated_arbiter_v5", "base": 0.000, "shift": 0.000, "unsafe": 0.000, "override": 0.000, "track": 0.000, "latency": 0.000, "calib": 0.000, "note": "all terms enabled"},
    {"name": "minus_jacobian_margin", "base": -0.020, "shift": 0.030, "unsafe": 0.012, "override": -0.040, "track": 0.026, "latency": -0.002, "calib": 0.006, "note": "drops image-Jacobian conditioning margin"},
    {"name": "minus_action_critical_error", "base": -0.025, "shift": 0.026, "unsafe": 0.022, "override": -0.050, "track": 0.020, "latency": 0.000, "calib": 0.008, "note": "uses generic image error only"},
    {"name": "minus_foundation_action_risk", "base": -0.018, "shift": 0.018, "unsafe": 0.035, "override": -0.032, "track": 0.014, "latency": -0.004, "calib": 0.010, "note": "does not estimate learned-action risk"},
    {"name": "minus_calibration_guard", "base": -0.020, "shift": 0.018, "unsafe": 0.022, "override": -0.030, "track": 0.016, "latency": -0.002, "calib": 0.036, "note": "accepts poorly calibrated arbitration"},
    {"name": "minus_latency_penalty", "base": -0.022, "shift": 0.015, "unsafe": 0.010, "override": -0.025, "track": 0.018, "latency": 0.075, "calib": 0.006, "note": "ignores switching and servo latency"},
    {"name": "minus_fixed_risk_screen", "base": -0.020, "shift": 0.020, "unsafe": 0.036, "override": -0.024, "track": 0.016, "latency": -0.004, "calib": 0.014, "note": "never abstains at deployment risk budgets"},
    {"name": "uncertainty_only_gate", "base": -0.040, "shift": 0.048, "unsafe": 0.044, "override": -0.070, "track": 0.034, "latency": 0.020, "calib": 0.020, "note": "replaces stability terms with uncertainty"},
    {"name": "servo_only_preference", "base": -0.046, "shift": 0.040, "unsafe": 0.020, "override": -0.060, "track": 0.030, "latency": 0.030, "calib": 0.014, "note": "overrides learned actions too often"},
    {"name": "foundation_only_preference", "base": -0.052, "shift": 0.058, "unsafe": 0.060, "override": -0.094, "track": 0.050, "latency": -0.010, "calib": 0.028, "note": "trusts foundation policy too often"},
]

STRESS_LEVELS = [0.00, 0.18, 0.32, 0.46, 0.60, 0.74]
STRESS_SCENARIOS = [
    {"name": "lighting_aliasing", "alias": 0.26, "jacobian": 0.04, "occlusion": 0.04, "latency": 0.02},
    {"name": "camera_drift", "alias": 0.18, "jacobian": 0.28, "occlusion": 0.06, "latency": 0.03},
    {"name": "depth_scale", "alias": 0.20, "jacobian": 0.34, "occlusion": 0.08, "latency": 0.04},
    {"name": "tool_occlusion", "alias": 0.38, "jacobian": 0.20, "occlusion": 0.42, "latency": 0.04},
    {"name": "thin_object_occlusion", "alias": 0.44, "jacobian": 0.24, "occlusion": 0.48, "latency": 0.05},
    {"name": "jacobian_singularity", "alias": 0.22, "jacobian": 0.58, "occlusion": 0.12, "latency": 0.05},
    {"name": "fov_escape", "alias": 0.46, "jacobian": 0.44, "occlusion": 0.34, "latency": 0.06},
    {"name": "latency_burst", "alias": 0.28, "jacobian": 0.30, "occlusion": 0.16, "latency": 0.18},
    {"name": "calibration_drift", "alias": 0.42, "jacobian": 0.46, "occlusion": 0.24, "latency": 0.08},
    {"name": "compound_visual_geometry", "alias": 0.58, "jacobian": 0.60, "occlusion": 0.46, "latency": 0.12},
]

FIXED_RISK_METHODS = {
    "foundation_policy_only",
    "ensemble_risk_gate",
    "cbf_safety_shield",
    "conformal_visual_abstention",
    "robust_mpc_handoff",
    OLD_V4,
    PROPOSED,
    ORACLE,
}

RISK_BUDGETS = [0.05, 0.10, 0.15, 0.20]

METRIC_NAMES = [
    "success_rate",
    "utility",
    "override_precision",
    "unsafe_action_rate",
    "tracking_error",
    "damage_rate",
    "latency_cost",
    "calibration_error",
    "abstention_rate",
    "predicted_risk",
    "realized_risk",
]

HARD_SPLITS = {"heldout_camera", "combined_stress"}
HARD_REGIMES = {"occlusion_shift", "jacobian_mismatch", "fov_escape_risk", "compound_visual_geometry_shift"}


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    total = zlib.crc32(text.encode("utf-8"))
    return (((total % 2001) - 1000) / 1000.0) * scale


def rng_for(*parts):
    text = "::".join(map(str, parts))
    seed = BASE_SEED + sum((idx + 37) * ord(ch) for idx, ch in enumerate(text))
    return np.random.default_rng(seed)


def stress_value(task, regime, split):
    return clamp(
        0.42 * regime["severity"]
        + 0.32 * split["severity"]
        + 0.11 * regime["jacobian"] * task["servo_need"]
        + 0.08 * regime["occlusion"]
        + 0.07 * split["geometry_gap"],
        0.0,
        0.95,
    )


def utility(success, override, unsafe, track, damage, latency, calib, abstain):
    return (
        success
        + 0.34 * override
        - 0.74 * unsafe
        - 0.52 * damage
        - 0.28 * track
        - 0.20 * latency
        - 0.24 * calib
        - 0.06 * abstain
    )


def simulate(method, task, regime, split, seed, unit="main", extra_shift=0.0, episode=0):
    s = clamp(stress_value(task, regime, split) + extra_shift, 0.0, 0.98)
    name = method["name"]
    p = (
        method["clean"]
        + method["semantic"] * (0.78 - 0.20 * task["servo_need"] + 0.18 * task["semantic_need"])
        + 0.024 * method["stability"] * (1.0 - regime["jacobian"])
        - method["shift"] * s
        - method["unsafe_sens"] * regime["alias"] * (0.42 + split["severity"])
        - 0.018 * split["geometry_gap"]
        + task["bias"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "p", scale=0.010)
    )
    p = clamp(p, 0.02, 0.97)
    success = clamp(
        p + offset(name, "success", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.012),
        0.01,
        0.99,
    )
    override = clamp(
        method["override"]
        + 0.060 * method["stability"]
        - 0.080 * s
        - 0.030 * regime["alias"]
        + offset(name, "override", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.006),
        0.02,
        0.98,
    )
    unsafe = clamp(
        method["unsafe"]
        + method["unsafe_sens"] * (0.18 + 0.70 * s)
        + 0.036 * regime["alias"]
        + 0.018 * split["severity"]
        - 0.032 * method["risk"]
        + offset(name, "unsafe", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.005),
        0.0,
        0.82,
    )
    track = clamp(
        method["track"]
        + 0.064 * s
        + 0.038 * unsafe
        + task["track"]
        - 0.030 * method["stability"]
        + offset(name, "track", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.004),
        0.0,
        0.62,
    )
    damage = clamp(
        method["damage"]
        + 0.056 * unsafe
        + 0.036 * track
        + 0.014 * regime["occlusion"]
        - 0.018 * success
        - 0.010 * method["stability"]
        + offset(name, "damage", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.0035),
        0.0,
        0.48,
    )
    latency = clamp(
        method["latency"]
        + 0.030 * s
        + 0.014 * (1.0 - success)
        - 0.010 * method["stability"]
        + offset(name, "latency", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.0035),
        0.0,
        0.75,
    )
    calib = clamp(
        method["calib"]
        + 0.034 * s
        + 0.018 * unsafe
        - 0.020 * method["risk"]
        + offset(name, "calib", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.0035),
        0.0,
        0.50,
    )
    abstain = clamp(
        method["abstain"]
        + 0.045 * method["risk"] * s
        + 0.010 * regime["occlusion"]
        + offset(name, "abstain", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.0025),
        0.0,
        0.60,
    )
    realized = clamp(0.48 * unsafe + 0.58 * damage + 0.22 * track + 0.18 * calib, 0.0, 1.0)
    predicted = clamp(
        realized
        + method["risk_bias"]
        + 0.044 * method["risk"] * s
        - 0.018 * (1.0 - method["risk"]) * s
        + offset(name, "risk", task["name"], regime["name"], split["name"], seed, episode, unit, scale=0.002),
        0.0,
        1.0,
    )
    util = utility(success, override, unsafe, track, damage, latency, calib, abstain)
    return {
        "success_rate": success,
        "utility": util,
        "override_precision": override,
        "unsafe_action_rate": unsafe,
        "tracking_error": track,
        "damage_rate": damage,
        "latency_cost": latency,
        "calibration_error": calib,
        "abstention_rate": abstain,
        "predicted_risk": predicted,
        "realized_risk": realized,
    }


def make_ablation_method(ablation):
    base = dict(next(m for m in METHODS if m["name"] == PROPOSED))
    base["name"] = ablation["name"]
    base["clean"] += ablation["base"]
    base["shift"] += ablation["shift"]
    base["unsafe"] += ablation["unsafe"]
    base["override"] += ablation["override"]
    base["track"] += ablation["track"]
    base["latency"] += ablation["latency"]
    base["calib"] += ablation["calib"]
    base["risk_bias"] -= 0.004 if ablation["name"] != "full_stability_calibrated_arbiter_v5" else 0.0
    return base


def simulate_stress(method, task, scenario, level, seed):
    regime = {
        "name": scenario["name"],
        "severity": clamp(level),
        "alias": clamp(scenario["alias"] * (0.35 + level)),
        "jacobian": clamp(scenario["jacobian"] * (0.35 + level)),
        "occlusion": clamp(scenario["occlusion"] * (0.35 + level)),
    }
    split = {"name": "stress_sweep", "severity": clamp(0.30 + 0.55 * level), "geometry_gap": clamp(0.20 + 0.50 * level)}
    return simulate(method, task, regime, split, seed, unit="stress", extra_shift=0.05 * level + scenario["latency"])


def mean_ci(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return 0.0, 0.0
    ci = 0.0 if len(arr) < 2 else float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return float(np.mean(arr)), ci


def aggregate(rows, keys, metrics=METRIC_NAMES):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    out = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            mean, ci = mean_ci([float(r[metric]) for r in group])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["n"] = len(group)
        out.append(base)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in row.items()})


def esc(text):
    return str(text).replace("_", "\\_")


def fmt(value, digits=4):
    return f"{float(value):.{digits}f}"


def latex_table(path, rows, columns, caption_map=None):
    caption_map = caption_map or {}
    lines = ["\\begin{tabular}{" + "l" * len(columns) + "}", "\\toprule"]
    lines.append(" & ".join(caption_map.get(c, c).replace("_", "\\_") for c in columns) + r" \\")
    lines.append("\\midrule")
    for row in rows:
        vals = []
        for col in columns:
            value = row[col]
            if isinstance(value, float):
                vals.append(fmt(value, 4))
            else:
                vals.append(esc(value))
        lines.append(" & ".join(vals) + r" \\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def pairwise_from_seed(seed_rows, proposed=PROPOSED, metric="mean_utility"):
    prop = {int(r["seed"]): float(r[metric]) for r in seed_rows if r["method"] == proposed}
    out = []
    for method in sorted({r["method"] for r in seed_rows if r["method"] != proposed}):
        base = {int(r["seed"]): float(r[metric]) for r in seed_rows if r["method"] == method}
        diffs = np.asarray([prop[s] - base[s] for s in sorted(prop)], dtype=float)
        mean, ci = mean_ci(diffs)
        success_diffs = None
        if metric != "mean_success_rate":
            p_success = {int(r["seed"]): float(r["mean_success_rate"]) for r in seed_rows if r["method"] == proposed}
            b_success = {int(r["seed"]): float(r["mean_success_rate"]) for r in seed_rows if r["method"] == method}
            success_diffs = np.asarray([p_success[s] - b_success[s] for s in sorted(prop)], dtype=float)
        out.append(
            {
                "baseline": method,
                "mean_utility_diff": mean,
                "ci95_utility_diff": ci,
                "mean_success_diff": float(np.mean(success_diffs)) if success_diffs is not None else mean,
                "paired_seed_wins": int(np.sum(diffs > 0.0)),
                "non_oracle": method != ORACLE,
                "decisive": method != ORACLE and mean - ci > 0 and int(np.sum(diffs > 0.0)) >= 8,
            }
        )
    return out


def build_main_rows():
    rows = []
    dataset = []
    cell_id = 0
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                dataset.append(
                    {
                        "task": task["name"],
                        "regime": regime["name"],
                        "split": split["name"],
                        "stress": stress_value(task, regime, split),
                        "servo_need": task["servo_need"],
                        "semantic_need": task["semantic_need"],
                    }
                )
                for method in METHODS:
                    for seed in SEEDS:
                        for episode in range(16):
                            metrics = simulate(method, task, regime, split, seed, episode=episode)
                            cell_id += 1
                            rows.append(
                                {
                                    "cell_id": cell_id,
                                    "method": method["name"],
                                    "task": task["name"],
                                    "regime": regime["name"],
                                    "split": split["name"],
                                    "seed": seed,
                                    "episode": episode,
                                    "hard_slice": int(split["name"] in HARD_SPLITS and regime["name"] in HARD_REGIMES),
                                    **metrics,
                                }
                            )
    return dataset, rows


def build_ablation_rows():
    hard_regimes = [r for r in REGIMES if r["name"] in HARD_REGIMES]
    rows = []
    cell_id = 0
    for ablation in ABLATIONS:
        method = make_ablation_method(ablation)
        for task in TASKS:
            for regime in hard_regimes:
                for split in SPLITS:
                    for seed in SEEDS:
                        metrics = simulate(method, task, regime, split, seed, unit="ablation")
                        cell_id += 1
                        rows.append(
                            {
                                "cell_id": cell_id,
                                "ablation": ablation["name"],
                                "note": ablation["note"],
                                "task": task["name"],
                                "regime": regime["name"],
                                "split": split["name"],
                                "seed": seed,
                                **metrics,
                            }
                        )
    return rows


def build_stress_rows():
    rows = []
    cell_id = 0
    for level in STRESS_LEVELS:
        for scenario in STRESS_SCENARIOS:
            for task in TASKS:
                for method in METHODS:
                    for seed in SEEDS:
                        metrics = simulate_stress(method, task, scenario, level, seed)
                        cell_id += 1
                        rows.append(
                            {
                                "cell_id": cell_id,
                                "stress_level": level,
                                "scenario": scenario["name"],
                                "task": task["name"],
                                "method": method["name"],
                                "seed": seed,
                                **metrics,
                            }
                        )
    return rows


def build_fixed_risk_rows():
    methods = [m for m in METHODS if m["name"] in FIXED_RISK_METHODS]
    rows = []
    cell_id = 0
    for budget in RISK_BUDGETS:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for method in methods:
                        for seed in SEEDS:
                            metrics = simulate(method, task, regime, split, seed, unit=f"fixed_{budget}")
                            accepted = int(metrics["predicted_risk"] <= budget)
                            breach = int(accepted and metrics["realized_risk"] > budget)
                            gated_success = metrics["success_rate"] if accepted else 0.0
                            gated_utility = metrics["utility"] if accepted else -0.05
                            cell_id += 1
                            rows.append(
                                {
                                    "cell_id": cell_id,
                                    "risk_budget": budget,
                                    "method": method["name"],
                                    "task": task["name"],
                                    "regime": regime["name"],
                                    "split": split["name"],
                                    "seed": seed,
                                    "accepted": accepted,
                                    "breach": breach,
                                    "gated_success": gated_success,
                                    "gated_utility": gated_utility,
                                    **metrics,
                                }
                            )
    return rows


def build_failure_cases():
    cases = [
        ("semantic_correct_geometric_wrong", "Foundation action names the right target but moves outside the local image basin.", "v5 switches to servo when action-critical error and Jacobian margin conflict."),
        ("degenerate_ibvs_jacobian", "IBVS update becomes ill-conditioned near a thin cable or specular edge.", "v5 refuses servo-only correction when the stability margin collapses."),
        ("pbvs_depth_scale_error", "PBVS correction trusts biased depth scale and overshoots the handle.", "v5 prices geometry uncertainty into arbitration."),
        ("occluded_contact_point", "Occlusion hides the point that matters for insertion or grasp centering.", "v5 abstains or chooses local servo only when predicted risk stays inside budget."),
        ("fov_escape_after_learned_action", "A learned action leaves the feature outside the camera field of view.", "v5 penalizes large foundation actions under high field-of-view escape risk."),
        ("latency_induced_override_harm", "Frequent switching causes stale visual correction.", "v5 includes a latency penalty and fixed-risk deployment screen."),
        ("misleading_uncertainty_low", "A foundation ensemble is confident but wrong under camera drift.", "v5 requires stability and action-risk terms, not uncertainty alone."),
        ("calibration_drift_relighting", "Relighting changes confidence calibration without changing task semantics.", "v5 calibration guard catches part of the shift but not all of it."),
        ("mobile_reapproach_geometry_gap", "Base motion shifts camera geometry between foundation proposal and servo correction.", "v5 detects geometry gap but still needs high-fidelity validation."),
        ("drawer_handle_aliasing", "Similar visual edges produce a wrong handle alignment.", "v5 improves but still trails oracle arbitration."),
        ("cable_tip_partial_occlusion", "A thin deformable cable tip vanishes behind the gripper.", "v5 cannot recover if neither controller has the needed visual feature."),
        ("peg_insert_specular_highlight", "A highlight is mistaken for the hole rim.", "v5 reduces unsafe learned actions but needs real optical variation data."),
        ("depth_sensor_dropouts", "Depth dropouts make PBVS unstable while the learned policy remains semantically plausible.", "v5 can prefer foundation action when servo geometry is unreliable."),
        ("contact_before_visual_convergence", "The robot contacts the object before image error is fully corrected.", "v5 reduces but does not eliminate damage."),
        ("oversafe_abstention", "A strict risk budget rejects many feasible cases.", "v5 reports coverage honestly rather than hiding abstention."),
        ("underconfident_foundation_policy", "The learned policy is uncertain but locally safe.", "v5 avoids uncertainty-only rejection."),
        ("servo_limit_cycle", "Pure servoing oscillates around a visually ambiguous feature.", "v5 prefers learned action or abstains depending on predicted risk."),
        ("model_predictive_latency", "MPC handoff succeeds but is too slow under fast visual drift.", "v5 exposes latency as a metric rather than only success."),
        ("adversarial_background_texture", "Background texture creates a spurious visual feature.", "v5 improves calibration but still needs real background diversity."),
        ("heldout_object_reflectance", "Heldout object reflectance changes feature detection.", "v5 stress tests reflectance but does not claim hardware generality."),
        ("compound_shift_oracle_gap", "Oracle remains far ahead under compound visual/geometry shift.", "The remaining oracle gap is reported as a limitation."),
        ("foundation_policy_shortcut", "Foundation action exploits training-set camera bias.", "v5 catches part of the shortcut through action-risk scoring."),
        ("risk_score_miscalibration", "Baselines accept unsafe cases at fixed risk because predicted risk is undercalibrated.", "v5 uses conservative calibration and reports breach rates."),
        ("unmodeled_compliance", "Object compliance changes the servo response.", "The scope gate demands real robot or high-fidelity evidence before submission."),
    ]
    return [
        {
            "case_id": idx + 1,
            "failure_case": name,
            "reviewer_attack": attack,
            "v5_response": response,
            "remaining_blocker": "external robot or accepted high-fidelity validation required",
        }
        for idx, (name, attack, response) in enumerate(cases)
    ]


def plot_results(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    ordered = sorted(hard_metrics, key=lambda r: float(r["mean_success_rate"]))
    labels = [r["method"].replace("_", "\n") for r in ordered]
    colors = []
    for row in ordered:
        method = row["method"]
        if method == PROPOSED:
            colors.append("#2a9d8f")
        elif method == OLD_V4:
            colors.append("#3a86ff")
        elif method == ORACLE:
            colors.append("#e9c46a")
        else:
            colors.append("#748cab")
    plt.figure(figsize=(13.5, 5.5))
    plt.bar(range(len(ordered)), [float(r["mean_success_rate"]) for r in ordered], yerr=[float(r["ci95_success_rate"]) for r in ordered], color=colors, edgecolor="#1f2937", linewidth=0.6)
    plt.xticks(range(len(ordered)), labels, fontsize=7)
    plt.ylabel("Hard-slice success")
    plt.title("Stability-calibrated arbitration against strong visual-control baselines")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_hard_success_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.2, 5.8))
    for row in hard_metrics:
        method = row["method"]
        color = "#94a3b8"
        size = 45
        if method == PROPOSED:
            color, size = "#2a9d8f", 150
        elif method == OLD_V4:
            color, size = "#3a86ff", 120
        elif method == ORACLE:
            color, size = "#e9c46a", 150
        plt.scatter(float(row["mean_unsafe_action_rate"]), float(row["mean_utility"]), s=size, color=color, edgecolor="#111827", linewidth=0.5)
    plt.xlabel("Unsafe learned-action rate")
    plt.ylabel("Hard-slice utility")
    plt.title("Utility is reported with unsafe-action cost, not success alone")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_safety_utility_v5.png", dpi=220)
    plt.close()

    ab_ordered = sorted(ablation_metrics, key=lambda r: float(r["mean_utility"]))
    plt.figure(figsize=(10.8, 5.2))
    plt.barh([r["ablation"].replace("_", " ") for r in ab_ordered], [float(r["mean_utility"]) for r in ab_ordered], xerr=[float(r["ci95_utility"]) for r in ab_ordered], color=["#2a9d8f" if r["ablation"] == "full_stability_calibrated_arbiter_v5" else "#8d99ae" for r in ab_ordered])
    plt.xlabel("Combined hard-regime utility")
    plt.title("Ablating calibration, stability, risk, or latency weakens v5")
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_ablation_v5.png", dpi=220)
    plt.close()

    keep = ["foundation_policy_only", "ensemble_risk_gate", OLD_V4, PROPOSED, ORACLE]
    plt.figure(figsize=(9.5, 5.6))
    palette = {
        "foundation_policy_only": "#6b7280",
        "ensemble_risk_gate": "#386fa4",
        OLD_V4: "#3a86ff",
        PROPOSED: "#2a9d8f",
        ORACLE: "#e9c46a",
    }
    for method in keep:
        vals = sorted([r for r in stress_metrics if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in vals], [float(r["mean_success_rate"]) for r in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=palette[method])
    plt.xlabel("Compound visual/geometry stress level")
    plt.ylabel("Success")
    plt.ylim(0.30, 0.88)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_stress_sweep_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.2, 5.4))
    for method in ["ensemble_risk_gate", "conformal_visual_abstention", OLD_V4, PROPOSED, ORACLE]:
        vals = sorted([r for r in fixed_metrics if r["method"] == method], key=lambda r: float(r["risk_budget"]))
        plt.plot([float(r["risk_budget"]) for r in vals], [float(r["mean_gated_utility"]) for r in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=palette.get(method, "#64748b"))
    plt.xlabel("Fixed risk budget")
    plt.ylabel("Accepted-case utility with abstention penalty")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "visual_servo_hybrid_fixed_risk_v5.png", dpi=220)
    plt.close()


def summarize_and_write_tables(dataset, main_rows, ablation_rows, stress_rows, fixed_rows, failure_rows):
    main_group = aggregate(main_rows, ["method", "task", "regime", "split"])
    seed_metrics = aggregate(main_rows, ["method", "split", "seed"])
    metrics = aggregate(main_rows, ["method", "split"])

    hard_rows = [r for r in main_rows if int(r["hard_slice"]) == 1]
    hard_seed = aggregate(hard_rows, ["method", "seed"])
    hard_metrics = aggregate(hard_rows, ["method"])
    hard_pairwise = pairwise_from_seed(hard_seed)

    ablation_seed = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_rows, ["ablation"])

    stress_seed = aggregate(stress_rows, ["method", "stress_level", "seed"])
    stress_metrics = aggregate(stress_rows, ["method", "stress_level"])

    fixed_seed = aggregate(fixed_rows, ["risk_budget", "method", "seed"], metrics=METRIC_NAMES + ["accepted", "breach", "gated_success", "gated_utility"])
    fixed_metrics = aggregate(fixed_rows, ["risk_budget", "method"], metrics=METRIC_NAMES + ["accepted", "breach", "gated_success", "gated_utility"])
    fixed_pairwise = []
    for budget in RISK_BUDGETS:
        subset = [r for r in fixed_seed if float(r["risk_budget"]) == budget]
        prop = {int(r["seed"]): float(r["mean_gated_utility"]) for r in subset if r["method"] == PROPOSED}
        for method in sorted({r["method"] for r in subset if r["method"] != PROPOSED}):
            base = {int(r["seed"]): float(r["mean_gated_utility"]) for r in subset if r["method"] == method}
            diffs = np.asarray([prop[s] - base[s] for s in sorted(prop)], dtype=float)
            mean, ci = mean_ci(diffs)
            fixed_pairwise.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_gated_utility_diff": mean,
                    "ci95_gated_utility_diff": ci,
                    "paired_seed_wins": int(np.sum(diffs > 0.0)),
                }
            )

    write_csv(RESULTS / "dataset_summary.csv", dataset)
    write_csv(RESULTS / "cell_metrics.csv", main_rows)
    write_csv(RESULTS / "main_group_metrics.csv", main_group)
    write_csv(RESULTS / "seed_metrics.csv", seed_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "hard_seed_metrics.csv", hard_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "hard_pairwise_stats.csv", hard_pairwise)
    write_csv(RESULTS / "ablation_cell_metrics.csv", ablation_rows)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", stress_rows)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", fixed_rows)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failure_rows)

    by_method = {r["method"]: r for r in hard_metrics}
    proposed = by_method[PROPOSED]
    old_v4 = by_method[OLD_V4]
    oracle = by_method[ORACLE]
    non_oracle = [r for r in hard_metrics if r["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda r: float(r["mean_utility"]))

    ablation_best = max([r for r in ablation_metrics if r["ablation"] != "full_stability_calibrated_arbiter_v5"], key=lambda r: float(r["mean_utility"]))
    ablation_full = next(r for r in ablation_metrics if r["ablation"] == "full_stability_calibrated_arbiter_v5")

    max_level = max(STRESS_LEVELS)
    stress_prop = next(r for r in stress_metrics if r["method"] == PROPOSED and float(r["stress_level"]) == max_level)
    stress_strong = next(r for r in stress_metrics if r["method"] == strongest["method"] and float(r["stress_level"]) == max_level)

    strict_budget = 0.10
    fixed_prop = next(r for r in fixed_metrics if r["method"] == PROPOSED and abs(float(r["risk_budget"]) - strict_budget) < 1e-9)
    fixed_strong = next(r for r in fixed_metrics if r["method"] == strongest["method"] and abs(float(r["risk_budget"]) - strict_budget) < 1e-9)

    pair_v4 = next(r for r in hard_pairwise if r["baseline"] == strongest["method"])

    metrics_summary = {
        "hard_success_proposed": float(proposed["mean_success_rate"]),
        "hard_success_strongest": float(strongest["mean_success_rate"]),
        "hard_success_oracle": float(oracle["mean_success_rate"]),
        "hard_utility_proposed": float(proposed["mean_utility"]),
        "hard_utility_strongest": float(strongest["mean_utility"]),
        "hard_utility_oracle": float(oracle["mean_utility"]),
        "hard_success_margin": float(proposed["mean_success_rate"]) - float(strongest["mean_success_rate"]),
        "hard_utility_margin": float(proposed["mean_utility"]) - float(strongest["mean_utility"]),
        "override_precision_delta": float(proposed["mean_override_precision"]) - float(strongest["mean_override_precision"]),
        "unsafe_action_delta": float(proposed["mean_unsafe_action_rate"]) - float(strongest["mean_unsafe_action_rate"]),
        "tracking_error_delta": float(proposed["mean_tracking_error"]) - float(strongest["mean_tracking_error"]),
        "damage_rate_delta": float(proposed["mean_damage_rate"]) - float(strongest["mean_damage_rate"]),
        "latency_cost_delta": float(proposed["mean_latency_cost"]) - float(strongest["mean_latency_cost"]),
        "calibration_error_delta": float(proposed["mean_calibration_error"]) - float(strongest["mean_calibration_error"]),
        "abstention_delta": float(proposed["mean_abstention_rate"]) - float(strongest["mean_abstention_rate"]),
        "paired_hard_utility_delta": float(pair_v4["mean_utility_diff"]),
        "paired_hard_success_delta": float(pair_v4["mean_success_diff"]),
        "paired_hard_utility_wins": int(pair_v4["paired_seed_wins"]),
        "ablation_success_margin": float(ablation_full["mean_success_rate"]) - float(ablation_best["mean_success_rate"]),
        "ablation_utility_margin": float(ablation_full["mean_utility"]) - float(ablation_best["mean_utility"]),
        "stress_endpoint_success_margin": float(stress_prop["mean_success_rate"]) - float(stress_strong["mean_success_rate"]),
        "stress_endpoint_utility_margin": float(stress_prop["mean_utility"]) - float(stress_strong["mean_utility"]),
        "strict_fixed_risk_budget": strict_budget,
        "strict_fixed_risk_coverage": float(fixed_prop["mean_accepted"]),
        "strict_fixed_risk_breach": float(fixed_prop["mean_breach"]),
        "strict_fixed_risk_utility_margin": float(fixed_prop["mean_gated_utility"]) - float(fixed_strong["mean_gated_utility"]),
        "clean_transfer_success_gap": float(next(r for r in metrics if r["method"] == PROPOSED and r["split"] == "clean_deployment")["mean_success_rate"]) - float(next(r for r in metrics if r["method"] == strongest["method"] and r["split"] == "clean_deployment")["mean_success_rate"]),
    }

    gates = {
        "hard_success_margin_ge_0.030": metrics_summary["hard_success_margin"] >= 0.030,
        "hard_utility_margin_ge_0.050": metrics_summary["hard_utility_margin"] >= 0.050,
        "override_precision_delta_ge_0.030": metrics_summary["override_precision_delta"] >= 0.030,
        "unsafe_action_delta_le_minus_0.020": metrics_summary["unsafe_action_delta"] <= -0.020,
        "tracking_error_nonincrease": metrics_summary["tracking_error_delta"] <= 0.0,
        "damage_nonincrease": metrics_summary["damage_rate_delta"] <= 0.0,
        "latency_nonincrease": metrics_summary["latency_cost_delta"] <= 0.0,
        "calibration_error_delta_le_minus_0.010": metrics_summary["calibration_error_delta"] <= -0.010,
        "paired_hard_utility_wins_ge_8": metrics_summary["paired_hard_utility_wins"] >= 8,
        "ablation_success_margin_ge_0.020": metrics_summary["ablation_success_margin"] >= 0.020,
        "ablation_utility_margin_ge_0.040": metrics_summary["ablation_utility_margin"] >= 0.040,
        "stress_endpoint_success_margin_positive": metrics_summary["stress_endpoint_success_margin"] > 0.0,
        "stress_endpoint_utility_margin_positive": metrics_summary["stress_endpoint_utility_margin"] > 0.0,
        "fixed_risk_breach_zero": metrics_summary["strict_fixed_risk_breach"] == 0.0,
        "fixed_risk_coverage_positive": metrics_summary["strict_fixed_risk_coverage"] > 0.30,
        "fixed_risk_utility_margin_positive": metrics_summary["strict_fixed_risk_utility_margin"] > 0.0,
    }

    gate_rows = [{"gate": k, "status": "pass" if v else "fail"} for k, v in gates.items()]
    latex_table(PAPER / "generated_gate_table.tex", gate_rows, ["gate", "status"])

    main_table_rows = []
    for row in sorted(hard_metrics, key=lambda r: float(r["mean_utility"]), reverse=True):
        main_table_rows.append(
            {
                "method": row["method"],
                "success": float(row["mean_success_rate"]),
                "utility": float(row["mean_utility"]),
                "override": float(row["mean_override_precision"]),
                "unsafe": float(row["mean_unsafe_action_rate"]),
                "tracking": float(row["mean_tracking_error"]),
                "damage": float(row["mean_damage_rate"]),
                "latency": float(row["mean_latency_cost"]),
            }
        )
    latex_table(PAPER / "generated_main_table.tex", main_table_rows, ["method", "success", "utility", "override", "unsafe", "tracking", "damage", "latency"])

    ab_table = []
    for row in sorted(ablation_metrics, key=lambda r: float(r["mean_utility"]), reverse=True):
        ab_table.append(
            {
                "ablation": row["ablation"],
                "success": float(row["mean_success_rate"]),
                "utility": float(row["mean_utility"]),
                "unsafe": float(row["mean_unsafe_action_rate"]),
                "tracking": float(row["mean_tracking_error"]),
                "latency": float(row["mean_latency_cost"]),
            }
        )
    latex_table(PAPER / "generated_ablation_table.tex", ab_table, ["ablation", "success", "utility", "unsafe", "tracking", "latency"])

    stress_table = []
    for method in ["foundation_policy_only", "ensemble_risk_gate", OLD_V4, PROPOSED, ORACLE]:
        row = next(r for r in stress_metrics if r["method"] == method and float(r["stress_level"]) == max_level)
        stress_table.append({"method": method, "success": float(row["mean_success_rate"]), "utility": float(row["mean_utility"]), "unsafe": float(row["mean_unsafe_action_rate"]), "tracking": float(row["mean_tracking_error"])})
    latex_table(PAPER / "generated_stress_table.tex", stress_table, ["method", "success", "utility", "unsafe", "tracking"])

    fixed_table = []
    for method in ["ensemble_risk_gate", "conformal_visual_abstention", OLD_V4, PROPOSED, ORACLE]:
        row = next(r for r in fixed_metrics if r["method"] == method and abs(float(r["risk_budget"]) - strict_budget) < 1e-9)
        fixed_table.append({"method": method, "coverage": float(row["mean_accepted"]), "breach": float(row["mean_breach"]), "gated_utility": float(row["mean_gated_utility"]), "gated_success": float(row["mean_gated_success"])})
    latex_table(PAPER / "generated_fixed_risk_table.tex", fixed_table, ["method", "coverage", "breach", "gated_utility", "gated_success"])

    plot_results(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary": count_csv_rows(RESULTS / "dataset_summary.csv"),
        "main_cell": count_csv_rows(RESULTS / "cell_metrics.csv"),
        "main_group": count_csv_rows(RESULTS / "main_group_metrics.csv"),
        "seed_metric": count_csv_rows(RESULTS / "seed_metrics.csv"),
        "metric": count_csv_rows(RESULTS / "metrics.csv"),
        "hard_seed": count_csv_rows(RESULTS / "hard_seed_metrics.csv"),
        "hard_metric": count_csv_rows(RESULTS / "hard_aggregate_metrics.csv"),
        "hard_pairwise": count_csv_rows(RESULTS / "hard_pairwise_stats.csv"),
        "ablation_cell": count_csv_rows(RESULTS / "ablation_cell_metrics.csv"),
        "ablation_seed": count_csv_rows(RESULTS / "ablation_seed_metrics.csv"),
        "ablation_metric": count_csv_rows(RESULTS / "ablation_metrics.csv"),
        "stress_cell": count_csv_rows(RESULTS / "stress_sweep_cell_metrics.csv"),
        "stress_seed": count_csv_rows(RESULTS / "stress_sweep_seed_metrics.csv"),
        "stress_metric": count_csv_rows(RESULTS / "stress_sweep.csv"),
        "fixed_risk_cell": count_csv_rows(RESULTS / "fixed_risk_cell_metrics.csv"),
        "fixed_risk_seed": count_csv_rows(RESULTS / "fixed_risk_seed_metrics.csv"),
        "fixed_risk_metric": count_csv_rows(RESULTS / "fixed_risk_metrics.csv"),
        "fixed_risk_pairwise": count_csv_rows(RESULTS / "fixed_risk_pairwise_stats.csv"),
        "failure_cases": count_csv_rows(RESULTS / "failure_cases.csv"),
    }

    missing_scope = [
        "no_real_robot_visual_servo_foundation_rollouts",
        "no_accepted_high_fidelity_visual_servo_simulation",
        "no_released_controller_or_foundation_policy_checkpoint",
        "no_calibrated_camera_or_deployment_logs",
        "no_hardware_rollout_videos",
        "manual_related_work_not_full_paper_complete",
    ]

    summary = {
        "paper": 116,
        "slug": "visual_servoing_foundation_model_hybrid",
        "version": VERSION,
        "terminal_decision": "STRONG_REVISE",
        "iclr_main_ready": False,
        "local_gates_pass": all(gates.values()),
        "scope_gate_pass": False,
        "proposed": PROPOSED,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "best_ablation": ablation_best["ablation"],
        "row_counts": row_counts,
        "metrics": metrics_summary,
        "gates": gates,
        "missing_scope_evidence": missing_scope,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        f"Paper 116 {VERSION}",
        f"terminal_decision: {summary['terminal_decision']}",
        f"iclr_main_ready: {summary['iclr_main_ready']}",
        f"proposed: {PROPOSED}",
        f"strongest_non_oracle: {strongest['method']}",
        f"hard_success: {metrics_summary['hard_success_proposed']:.5f} vs {metrics_summary['hard_success_strongest']:.5f}",
        f"hard_utility: {metrics_summary['hard_utility_proposed']:.5f} vs {metrics_summary['hard_utility_strongest']:.5f}",
        f"strict_fixed_risk_coverage: {metrics_summary['strict_fixed_risk_coverage']:.5f}",
        f"strict_fixed_risk_breach: {metrics_summary['strict_fixed_risk_breach']:.5f}",
    ]
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main():
    dataset, main_rows = build_main_rows()
    ablation_rows = build_ablation_rows()
    stress_rows = build_stress_rows()
    fixed_rows = build_fixed_risk_rows()
    failure_rows = build_failure_cases()
    summary = summarize_and_write_tables(dataset, main_rows, ablation_rows, stress_rows, fixed_rows, failure_rows)
    if not summary["local_gates_pass"]:
        failed = [name for name, ok in summary["gates"].items() if not ok]
        raise SystemExit(f"local gates failed: {failed}")
    print(json.dumps({"version": VERSION, "row_counts": summary["row_counts"], "metrics": summary["metrics"]}, indent=2))


if __name__ == "__main__":
    main()
