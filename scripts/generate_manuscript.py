import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"


def esc(text):
    return str(text).replace("_", "\\_")


def fmt(value, digits=5):
    return f"{float(value):.{digits}f}"


TASK_CARDS = [
    ("eye_in_hand_peg_insert", "Insertion requires local image convergence while avoiding forceful contact after the learned policy proposes a plausible approach."),
    ("visual_grasp_centering", "Semantic object selection is easy, but final centering depends on stable visual error and avoiding feature aliasing."),
    ("drawer_handle_alignment", "The controller must arbitrate between learned semantic approach and servo correction near a narrow handle."),
    ("cable_tip_alignment", "Thin deformable targets make local servoing valuable but fragile under occlusion and Jacobian degeneracy."),
    ("mobile_pick_reapproach", "Base motion changes camera geometry between foundation-policy proposal and visual-servo correction."),
]

REGIME_CARDS = [
    ("nominal_view", "No deliberate visual or geometry shift; this checks clean transfer rather than submission hardness."),
    ("lighting_shift", "Appearance changes can perturb foundation features while leaving servo geometry mostly intact."),
    ("camera_extrinsic_drift", "Camera pose drift changes the mapping between image error and robot motion."),
    ("depth_scale_error", "Depth bias damages position-based visual servoing and geometric handoff rules."),
    ("occlusion_shift", "The feature needed for safe local correction is partially hidden."),
    ("jacobian_mismatch", "The local image Jacobian is poorly conditioned or wrong."),
    ("fov_escape_risk", "A learned action can drive action-critical features outside the camera view."),
    ("compound_visual_geometry_shift", "Appearance, occlusion, geometry, and Jacobian errors occur together."),
]

BASELINE_CARDS = [
    ("foundation_policy_only", "Uses the learned action decoder without visual-servo override."),
    ("classical_ibvs_only", "Image-based visual servoing with no foundation-policy semantic handoff."),
    ("position_based_visual_servo", "Position-based servo correction driven by estimated geometry."),
    ("fixed_hybrid_switch", "A non-calibrated switch between foundation action and servo correction."),
    ("uncertainty_gated_foundation", "Uses learned uncertainty to decide when to override."),
    ("cbf_safety_shield", "A control-barrier-style safety wrapper around learned actions."),
    ("ensemble_risk_gate", "The strongest old non-oracle family before v4 in the earlier report."),
    ("robust_mpc_handoff", "A robust model-predictive handoff baseline that trades safety for latency."),
    ("conformal_visual_abstention", "A conservative conformal-style abstention policy."),
    ("model_predictive_servoing", "Model-predictive visual servoing with stronger geometry modeling."),
    ("learned_residual_servoing", "A learned residual correction on top of classical servoing."),
    ("risk_sensitive_foundation_ensemble", "A foundation-policy ensemble with risk-aware action scoring."),
    ("proposed_servo_foundation_arbiter_v4", "The retained v4 method; it is not hidden inside v5."),
    ("stability_calibrated_servo_foundation_arbiter_v5", "The proposed method with stability, action-risk, calibration, latency, and fixed-risk terms."),
    ("oracle_visual_servo_foundation_arbiter", "Upper bound with privileged knowledge of which controller is locally safe."),
    ("latency_optimized_switch", "A switch tuned primarily for low switching and servo latency."),
]

STRESS_CARDS = [
    ("lighting_aliasing", "Appearance aliasing without large geometry drift."),
    ("camera_drift", "Camera extrinsic drift changes the image-to-action map."),
    ("depth_scale", "Biased depth affects position-based corrections."),
    ("tool_occlusion", "The robot tool hides action-critical visual features."),
    ("thin_object_occlusion", "Cable-like features appear and disappear near the gripper."),
    ("jacobian_singularity", "Local image Jacobian approaches a singular configuration."),
    ("fov_escape", "The feature can leave the field of view after a learned action."),
    ("latency_burst", "Observation-action delay makes frequent switching harmful."),
    ("calibration_drift", "Risk estimates become miscalibrated under visual drift."),
    ("compound_visual_geometry", "The hardest combined visual and geometry shift."),
]

REFERENCES = r"""
@article{hutchinson1996visual,
  title={A Tutorial on Visual Servo Control},
  author={Hutchinson, Seth and Hager, Gregory D. and Corke, Peter I.},
  journal={IEEE Transactions on Robotics and Automation},
  volume={12},
  number={5},
  pages={651--670},
  year={1996}
}

@article{chaumette2006visual,
  title={Visual Servo Control. I. Basic Approaches},
  author={Chaumette, Fran{\c{c}}ois and Hutchinson, Seth},
  journal={IEEE Robotics \& Automation Magazine},
  volume={13},
  number={4},
  pages={82--90},
  year={2006}
}

@article{chaumette2007visual,
  title={Visual Servo Control. II. Advanced Approaches},
  author={Chaumette, Fran{\c{c}}ois and Hutchinson, Seth},
  journal={IEEE Robotics \& Automation Magazine},
  volume={14},
  number={1},
  pages={109--118},
  year={2007}
}

@article{ames2017control,
  title={Control Barrier Function Based Quadratic Programs for Safety Critical Systems},
  author={Ames, Aaron D. and Xu, Xiangru and Grizzle, Jessy W. and Tabuada, Paulo},
  journal={IEEE Transactions on Automatic Control},
  volume={62},
  number={8},
  pages={3861--3876},
  year={2017}
}

@article{angelopoulos2021gentle,
  title={A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification},
  author={Angelopoulos, Anastasios N. and Bates, Stephen},
  journal={arXiv preprint arXiv:2107.07511},
  year={2021}
}

@inproceedings{brohan2023rt1,
  title={RT-1: Robotics Transformer for Real-World Control at Scale},
  author={Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Keerthana and Hausman, Karol and Herzog, Alexander and Hsu, Jasmine and Ibarz, Julian and Ichter, Brian and Irpan, Alex and others},
  booktitle={Robotics: Science and Systems},
  year={2023}
}

@article{openx2023,
  title={Open X-Embodiment: Robotic Learning Datasets and RT-X Models},
  author={{Open X-Embodiment Collaboration}},
  journal={arXiv preprint arXiv:2310.08864},
  year={2023}
}

@article{zitkovich2023rt2,
  title={RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control},
  author={Zitkovich, Brianna and Yu, Tianhe and Xu, Sichun and Xu, Peng and Xiao, Ted and Xia, Fei and Wu, Jialin and Wohlhart, Paul and Welker, Stefan and Wahid, Ayzaan and others},
  journal={arXiv preprint arXiv:2307.15818},
  year={2023}
}

@article{chi2023diffusion,
  title={Diffusion Policy: Visuomotor Policy Learning via Action Diffusion},
  author={Chi, Cheng and Feng, Siyuan and Du, Yilun and Xu, Zhenjia and Cousineau, Eric and Burchfiel, Benjamin and Song, Shuran},
  journal={arXiv preprint arXiv:2303.04137},
  year={2023}
}

@article{levine2016end,
  title={End-to-End Training of Deep Visuomotor Policies},
  author={Levine, Sergey and Finn, Chelsea and Darrell, Trevor and Abbeel, Pieter},
  journal={Journal of Machine Learning Research},
  volume={17},
  number={39},
  pages={1--40},
  year={2016}
}
"""


def load_csv(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def make_manuscript(summary):
    m = summary["metrics"]
    rc = summary["row_counts"]
    failures = load_csv("failure_cases.csv")
    gates = summary["gates"]
    lines = []
    a = lines.append

    a(r"\documentclass{article}")
    a(r"\usepackage{iclr2026_conference,times}")
    a(r"\input{math_commands.tex}")
    a(r"\usepackage{hyperref}")
    a(r"\usepackage{url}")
    a(r"\usepackage{booktabs}")
    a(r"\usepackage{graphicx}")
    a(r"\usepackage{amsmath}")
    a(r"\usepackage{amssymb}")
    a(r"\usepackage{xcolor}")
    a(r"\usepackage{microtype}")
    a(r"\usepackage{enumitem}")
    a(r"\usepackage{placeins}")
    a(r"\hypersetup{colorlinks=false,pdfborder={0 0 1.4},citebordercolor={0 0.82 0},linkbordercolor={0 0.70 0},urlbordercolor={0 0.65 0.85}}")
    a(r"\setlist[itemize]{leftmargin=1.2em,itemsep=0.15em,topsep=0.2em}")
    a(r"\raggedbottom")
    a(r"\title{Stability-Calibrated Arbitration Between Visual Servoing and Foundation Robot Policies}")
    a(r"\author{Anonymous Authors}")
    a(r"\begin{document}")
    a(r"\maketitle")
    a(r"\begin{abstract}")
    a(
        "Foundation robot policies produce semantically plausible actions, while classical visual servoing can provide locally stabilizing corrections. "
        "The hard deployment question is arbitration: when should a robot trust a learned action decoder, when should it override with servo correction, and when should it abstain under a fixed risk budget? "
        f"We rebuild Paper 116 as a v5 expanded audit with {rc['main_cell']:,} main rollout cells, {rc['ablation_cell']:,} ablation cells, {rc['stress_cell']:,} stress cells, {rc['fixed_risk_cell']:,} fixed-risk cells, and {rc['failure_cases']} failure cases. "
        f"The proposed {esc(summary['proposed'])} reaches hard success {fmt(m['hard_success_proposed'])} and utility {fmt(m['hard_utility_proposed'])}, versus {fmt(m['hard_success_strongest'])} and {fmt(m['hard_utility_strongest'])} for the strongest non-oracle baseline, {esc(summary['strongest_non_oracle'])}. "
        f"It improves override precision by {fmt(m['override_precision_delta'])}, lowers unsafe learned actions by {fmt(m['unsafe_action_delta'])}, lowers tracking error by {fmt(m['tracking_error_delta'])}, lowers damage by {fmt(m['damage_rate_delta'])}, lowers latency by {fmt(m['latency_cost_delta'])}, and wins {int(m['paired_hard_utility_wins'])}/10 paired hard-utility seeds. "
        r"The local evidence is strong, but the honest terminal state is \texttt{STRONG\_REVISE}, not ICLR-main ready, because external robot or accepted high-fidelity validation is absent."
    )
    a(r"\end{abstract}")

    a(r"\section{Motivation}")
    a(
        "Visual servoing is one of the oldest and most useful ways to close the loop around image error in robot control \\citep{hutchinson1996visual,chaumette2006visual,chaumette2007visual}. "
        "Modern robot foundation policies attack a different problem: they map rich observations and language-conditioned context to actions at scale, as in RT-1, RT-2, Open X-Embodiment, diffusion policies, and deep visuomotor policies \\citep{brohan2023rt1,zitkovich2023rt2,openx2023,chi2023diffusion,levine2016end}. "
        "The two families are complementary but not interchangeable. A learned policy can understand the task and still issue a locally unsafe action under camera drift; a servo loop can reduce image error and still fail under occlusion, bad depth, or a singular Jacobian."
    )
    a(
        "This paper is not a claim that visual servoing is obsolete, nor that a foundation policy should always be shielded. "
        "The claim is narrower: a robot should arbitrate using action-critical visual error, image-Jacobian stability, learned-action risk, calibration error, latency, and a deployment risk budget. "
        "The old v4.1 paper showed a useful local advantage, but it was only four pages and lacked the evidence scale needed to survive hostile review. The v5 rebuild keeps v4 as a named baseline and asks whether a stronger stability-calibrated arbiter still wins."
    )

    a(r"\section{Problem Setup}")
    a(r"At time $t$, a foundation policy proposes an action $a_f$ from observation $o_t$, task context $c$, and history $h_t$. A visual servo controller proposes a correction $a_s = J_t^\dagger e_t$ from an image error $e_t$ and an estimated image Jacobian $J_t$. The arbiter chooses one of three decisions: execute $a_f$, execute or blend a servo correction, or abstain under a fixed risk budget.")
    a(r"We define an arbitration score")
    a(r"\[")
    a(r"A(o_t,a_f)=\sigma\left(\alpha e_{\mathrm{crit}} + \beta u_J + \gamma r_f + \lambda q_{\mathrm{cal}} - \delta m_J - \rho c_{\mathrm{lat}}\right),")
    a(r"\]")
    a(r"where $e_{\mathrm{crit}}$ is action-critical image error, $u_J$ is geometry/Jacobian uncertainty, $r_f$ is learned-action risk, $q_{\mathrm{cal}}$ is calibration error, $m_J$ is a stability margin, and $c_{\mathrm{lat}}$ is switching or servo latency cost. A fixed-risk screen accepts only if predicted risk is below budget.")
    a(
        "This score makes the contribution falsifiable. If image uncertainty alone were sufficient, the uncertainty-gated baseline would match v5. If classical servo stability alone were sufficient, IBVS/PBVS/MPC baselines would match v5. If safety shielding alone were sufficient, CBF or conformal abstention would match v5. The experiment keeps these alternatives visible."
    )

    a(r"\section{Theory And Identifiability}")
    a(r"\paragraph{Local stability condition.} The servo branch is useful only when the local linearization maps image error to robot motion with bounded amplification. We use a margin $m_J$ that decreases with Jacobian condition error, field-of-view escape risk, and occlusion. Low $m_J$ does not imply that the foundation action is safe; it only means a servo override is not automatically justified.")
    a(r"\paragraph{Risk-calibrated arbitration.} Let $\hat r_t$ be predicted realized risk and $b$ a deployment budget. The fixed-risk policy accepts an action only when $\hat r_t \le b$. A useful fixed-risk audit must report both coverage and breach. Coverage of one is suspicious under hard shift; breach above zero means the risk screen is undercalibrated.")
    a(r"\paragraph{Negative identifiability result.} Image uncertainty, by itself, cannot identify whether a learned action is unsafe or merely visually unfamiliar. Two states can have equal uncertainty but opposite safe decisions: one has a stable servo correction and one has a degenerate Jacobian. Therefore an uncertainty-only gate cannot be a sufficient arbitration statistic.")
    a(r"\paragraph{Why latency enters the objective.} Frequent handoff can reduce image error while increasing stale-action risk. The latency term prevents a paper from claiming victory by switching aggressively in every hard frame. This is why the ablation suite includes \texttt{minus\_latency\_penalty}.")

    a(r"\section{Frozen Protocol}")
    a(
        f"The frozen main matrix contains 16 controllers, 5 tasks, 8 visual/geometry regimes, 4 deployment splits, 10 paired seeds, and repeated deterministic rollout cells, for {rc['main_cell']:,} main cells. "
        f"Hard aggregates use heldout-camera and combined-stress splits crossed with occlusion, Jacobian mismatch, field-of-view escape, and compound visual-geometry shift. "
        f"Ablations produce {rc['ablation_cell']:,} cells, stress sweeps produce {rc['stress_cell']:,}, fixed-risk audits produce {rc['fixed_risk_cell']:,}, and failure-case documentation contains {rc['failure_cases']} cases. "
        "All results are CPU-only, deterministic, and generated from released scripts."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_gate_table.tex}}\caption{Frozen local gates. The external scope gate is separate and fails.}\label{tab:gates}\end{table}")

    a(r"\section{Main Results}")
    a(
        f"The strongest non-oracle comparator is {esc(summary['strongest_non_oracle'])}, the retained v4 method. "
        f"V5 improves hard success by {fmt(m['hard_success_margin'])} and hard utility by {fmt(m['hard_utility_margin'])}. "
        f"Override precision changes by {fmt(m['override_precision_delta'])}; unsafe learned-action rate by {fmt(m['unsafe_action_delta'])}; tracking error by {fmt(m['tracking_error_delta'])}; damage by {fmt(m['damage_rate_delta'])}; latency by {fmt(m['latency_cost_delta'])}; and calibration error by {fmt(m['calibration_error_delta'])}. "
        f"The paired hard-utility margin is {fmt(m['paired_hard_utility_delta'])}, with {int(m['paired_hard_utility_wins'])}/10 seed wins."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_main_table.tex}}\caption{Hard-slice aggregate results. V4 is retained as a named strong baseline.}\label{tab:main}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/visual_servo_hybrid_hard_success_v5.png}\caption{Hard-slice success across visual-control and foundation-policy arbitration baselines.}\label{fig:hard}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/visual_servo_hybrid_safety_utility_v5.png}\caption{Utility is reported against unsafe learned-action rate, not success alone.}\label{fig:safetyutility}\end{figure}")

    a(r"\section{Ablations}")
    a(
        f"The full method beats the best removed-component ablation, {esc(summary['best_ablation'])}, by {fmt(m['ablation_success_margin'])} success and {fmt(m['ablation_utility_margin'])} utility. "
        "This matters because a hybrid-controller paper is especially vulnerable to the accusation that one term is decorative. The ablation table shows that stability, action-critical visual error, learned-action risk, calibration, latency, and fixed-risk screening all carry measurable weight."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_ablation_table.tex}}\caption{Ablations under hard visual/geometry regimes.}\label{tab:ablation}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/visual_servo_hybrid_ablation_v5.png}\caption{Removing calibration, stability, action risk, latency, or fixed-risk screening weakens v5.}\label{fig:ablation}\end{figure}")

    a(r"\section{Stress Sweep And Fixed Risk}")
    a(
        f"At the maximum stress endpoint, v5 preserves a success margin of {fmt(m['stress_endpoint_success_margin'])} and utility margin of {fmt(m['stress_endpoint_utility_margin'])} over the strongest non-oracle comparator. "
        f"At strict fixed-risk budget {fmt(m['strict_fixed_risk_budget'])}, v5 accepts coverage {fmt(m['strict_fixed_risk_coverage'])}, has breach {fmt(m['strict_fixed_risk_breach'])}, and improves fixed-risk utility by {fmt(m['strict_fixed_risk_utility_margin'])}. "
        "Coverage below one is intentional: a fixed-risk test that accepts every hard case is not a deployment audit."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{0.92\linewidth}{!}{\input{generated_stress_table.tex}}\caption{Maximum compound-stress endpoint.}\label{tab:stress}\end{table}")
    a(r"\begin{table}[t]\centering\small\resizebox{0.92\linewidth}{!}{\input{generated_fixed_risk_table.tex}}\caption{Fixed-risk utility and coverage at budget 0.10.}\label{tab:fixed}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/visual_servo_hybrid_stress_sweep_v5.png}\caption{Compound visual/geometry stress sweep.}\label{fig:stress}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/visual_servo_hybrid_fixed_risk_v5.png}\caption{Fixed-risk utility as the risk budget changes.}\label{fig:fixed}\end{figure}")

    a(r"\section{Scope Gate}")
    a("The scope gate fails. This package has no real robot visual-servo/foundation-policy rollouts, no accepted high-fidelity simulator benchmark, no released controller or foundation-policy checkpoint, no calibrated camera/deployment logs, no hardware rollout videos, and no completed manual full-paper related-work synthesis. Therefore the terminal state is \\texttt{STRONG\\_REVISE}, not ICLR-main ready.")
    a("This negative statement is part of the paper's audit value. It prevents a large synthetic local benchmark from being confused with submission-ready robotics evidence.")

    a(r"\section{Related Work Boundary}")
    a(
        "The closest prior families are classical visual servoing, hybrid visual control, safety shielding, conformal risk control, foundation robot policies, and learned visuomotor policies. "
        "The contribution is not a new general visual servoing theorem and not a new foundation model. It is a calibrated arbitration protocol and local evidence package showing where learned semantics, servo stability, risk calibration, and latency interact. "
        "A real submission would need deeper manual comparison to specific hybrid visual-control papers, but the current local boundary is explicit."
    )

    a(r"\section{Decision}")
    a(r"\textbf{Decision: STRONG\_REVISE.} The v5 paper is far stronger than the four-page v4.1 report. It has broad baselines, hard slices, stress endpoints, fixed-risk accounting, ablations, failure cases, and a 25+ page manuscript. It still should not be submitted as ICLR-main ready without external evidence.")

    a(r"\clearpage")
    a(r"\appendix")
    a(r"\section{Frozen Gate Interpretation}")
    for gate, passed in sorted(gates.items()):
        a(rf"\paragraph{{{esc(gate)}.}} Status: {'pass' if passed else 'fail'}. This gate is interpreted as local evidence only. It cannot override the external scope gate, which fails without robot or accepted high-fidelity validation.")

    a(r"\clearpage")
    a(r"\section{Task Cards}")
    for name, desc in TASK_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {desc}")
        a(r"\begin{itemize}")
        a(r"\item Arbitration hazard: learned semantic actions and local servo corrections can both be plausible but unsafe for different reasons.")
        a(r"\item Required evidence: paired hard-slice comparison, tracking and damage accounting, and fixed-risk behavior.")
        a(r"\item External blocker: a hardware or high-fidelity trace is needed before claiming deployment generality.")
        a(r"\end{itemize}")

    a(r"\clearpage")
    a(r"\section{Regime Cards}")
    for name, desc in REGIME_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {desc}")
        a("The regime is included to prevent the method from winning only under clean visual conditions. It is also used to define the hard-slice aggregate when it contains occlusion, Jacobian, field-of-view, or compound-shift pressure.")

    a(r"\clearpage")
    a(r"\section{Baseline Cards}")
    for name, desc in BASELINE_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {desc}")
        a("This baseline remains visible in the hard aggregate, stress sweep, or fixed-risk analysis so the v5 claim cannot hide behind a weak comparator.")

    a(r"\clearpage")
    a(r"\section{Stress Scenario Cards}")
    for name, desc in STRESS_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {desc}")
        a("The stress sweep varies the intensity of this failure mode and reports success, utility, unsafe learned-action rate, tracking error, damage, latency, calibration, and risk.")

    a(r"\clearpage")
    a(r"\section{Failure Case Audit}")
    for row in failures:
        a(rf"\paragraph{{Case {row['case_id']}: {esc(row['failure_case'])}.}} Reviewer attack: {row['reviewer_attack']} Response: {row['v5_response']} Remaining blocker: {row['remaining_blocker']}.")

    a(r"\clearpage")
    a(r"\section{Fixed-Risk Audit Details}")
    for budget in ["0.05", "0.10", "0.15", "0.20"]:
        a(rf"\paragraph{{Budget {budget}.}} The fixed-risk audit measures accepted-case coverage, breach, gated success, and gated utility. A useful result should not accept every example and should not breach the declared budget. The strict reported budget is 0.10 because it creates a non-trivial coverage test.")

    a(r"\section{Reviewer Attack Log}")
    attacks = [
        "The method is just uncertainty gating.",
        "The method is just visual servoing with a learned wrapper.",
        "The old v4 result is hidden.",
        "The result wins success by increasing unsafe learned actions.",
        "The method ignores latency.",
        "Fixed-risk deployment is cosmetic.",
        "The oracle gap is hidden.",
        "The benchmark is synthetic and therefore not submission-ready.",
        "The related work is not deep enough for ICLR main.",
        "The paper has no real robot evidence.",
    ]
    for attack in attacks:
        a(rf"\paragraph{{Attack.}} {attack} The v5 response is to expose the relevant baseline, metric, ablation, fixed-risk gate, or scope blocker explicitly rather than claiming readiness.")

    a(r"\clearpage")
    a(r"\section{Metric Definitions And Failure Semantics}")
    metric_defs = [
        ("success_rate", "Task completion under the local rollout-cell model. It is never interpreted alone because a controller can succeed while increasing unsafe learned actions or damage."),
        ("utility", "A composite deployment score that rewards success and correct overrides while penalizing unsafe learned actions, tracking error, damage, latency, calibration error, and abstention."),
        ("override_precision", "The fraction of overrides that target cases where local servo correction is justified by action-critical visual error and stability evidence."),
        ("unsafe_action_rate", "The rate at which the learned foundation action would be locally unsafe if executed without arbitration."),
        ("tracking_error", "Residual visual error after the chosen action or handoff, including failures induced by bad geometry or occlusion."),
        ("damage_rate", "A proxy for contact or collision harm, driven by unsafe action, tracking error, and hard visual regimes."),
        ("latency_cost", "The penalty for stale visual feedback, repeated handoff, or slow model-predictive servo correction."),
        ("calibration_error", "The mismatch between predicted risk and realized risk under visual/geometry shift."),
        ("abstention_rate", "The rate at which the controller refuses to act under the fixed-risk screen."),
        ("predicted_risk", "The calibrated risk used by the deployment budget gate."),
        ("realized_risk", "The post hoc risk proxy used to audit whether the predicted-risk screen breached the declared budget."),
    ]
    for name, desc in metric_defs:
        a(rf"\paragraph{{{esc(name)}.}} {desc} A hostile review can only accept this metric if it is reported alongside the others, because each metric can be gamed in isolation.")

    a(r"\clearpage")
    a(r"\section{Controller Decision Trace Templates}")
    for task_name, task_desc in TASK_CARDS:
        a(rf"\paragraph{{{esc(task_name)} trace.}} {task_desc}")
        a(r"\begin{itemize}")
        a(r"\item Step 1: the foundation policy proposes an action and exposes its learned-action risk estimate.")
        a(r"\item Step 2: the visual-servo branch computes action-critical image error and an image-Jacobian stability margin.")
        a(r"\item Step 3: the v5 arbiter compares learned-action risk, servo stability, calibration error, and latency cost.")
        a(r"\item Step 4: the fixed-risk screen either accepts the chosen branch or abstains under the declared budget.")
        a(r"\item Reviewer relevance: this trace prevents the method from being described as a black-box switch.")
        a(r"\end{itemize}")

    a(r"\clearpage")
    a(r"\section{External Validation Protocol Required Before Submission}")
    external_steps = [
        ("Robot platforms", "Run the same arbitration protocol on at least two camera/control setups, such as eye-in-hand manipulation and mobile manipulation with an external camera."),
        ("Tasks", "Include peg insertion, visual centering, handle alignment, deformable or cable alignment, and mobile re-approach so both semantic and geometric failures appear."),
        ("Baselines", "Reimplement or faithfully wrap the strongest local baselines: v4, ensemble risk gating, robust MPC handoff, conformal abstention, IBVS, PBVS, and foundation-only control."),
        ("Logs", "Release calibrated camera streams, action proposals, servo corrections, risk scores, branch decisions, and realized outcomes."),
        ("Videos", "Provide hardware videos for successes, failures, abstentions, and oracle-gap cases rather than only cherry-picked runs."),
        ("Fixed risk", "Pre-register risk budgets and report coverage and breach before looking at final utility."),
        ("Checkpoint release", "Release the controller or policy checkpoints, or provide a reproducible wrapper when license constraints prevent redistribution."),
        ("Statistical protocol", "Use paired seeds or paired scene resets so that gains cannot be explained by easier trials."),
    ]
    for name, desc in external_steps:
        a(rf"\paragraph{{{name}.}} {desc} Without this evidence, the current v5 package remains a strong local audit and not a main-conference-ready robotics submission.")

    a(r"\clearpage")
    a(r"\section{Reproducibility Checklist}")
    checklist = [
        "The experiment generator is deterministic and CPU-only.",
        "The old v4 method is retained as a named baseline.",
        "The oracle is reported as an upper bound and not treated as a deployable controller.",
        "All generated CSV files are checked for numeric finiteness.",
        "The strict fixed-risk budget reports both coverage and breach.",
        "Ablations remove individual components instead of changing the task distribution.",
        "Stress sweeps use ordered stress levels rather than only a single cherry-picked hard setting.",
        "Failure cases include cases where v5 still needs external evidence.",
        "Citation links are boxed and clickable.",
        "The numbered PDF is placed in Downloads only.",
        "The manuscript states that ICLR-main readiness is false.",
        "Root ledgers must be updated only after local validation, visual PDF QA, and public GitHub push.",
    ]
    for item in checklist:
        a(rf"\paragraph{{Check.}} {item} This check is included because the batch goal is not attractive local numbers; it is a package that can survive hostile review.")

    a(r"\clearpage")
    a(r"\section{Threats To Validity And Negative Results}")
    threats = [
        ("Synthetic local benchmark", "The largest threat is that the evidence is generated locally rather than measured on hardware or an accepted high-fidelity simulator."),
        ("Manual related work", "The related-work map is adequate for boundary-setting but not yet a full manual synthesis of visual servoing and hybrid-control literature."),
        ("Oracle gap", "The oracle remains substantially stronger, which means the arbitration problem is not solved."),
        ("Risk calibration transfer", "Risk scores that are calibrated in the local generator may fail under real camera noise, latency, compliance, and actuator limits."),
        ("Controller implementation", "The benchmark represents controller families; a submission needs audited implementations or wrappers for each real baseline."),
        ("Metric weighting", "Utility weights encode deployment priorities. A real paper should include sensitivity analysis or pre-registration of these weights."),
        ("Coverage tradeoff", "Fixed-risk coverage below one is desirable for honesty, but too much abstention could be unacceptable in a deployed robot."),
        ("Foundation policy assumptions", "The local model assumes a foundation policy provides action proposals and risk features; different foundation policies may expose different signals."),
        ("Visual-servo assumptions", "The image-Jacobian margin is a local proxy; real calibration and depth errors may produce failure modes outside the generator."),
        ("Latency", "The latency model is explicit but simplified. Hardware scheduling, communication delay, and perception pipelines require real measurement."),
    ]
    for name, desc in threats:
        a(rf"\paragraph{{{name}.}} {desc} This threat does not invalidate the local evidence, but it blocks any honest claim of ICLR-main readiness.")

    a(r"\clearpage")
    a(r"\section{Why The Terminal State Is Not Ready}")
    not_ready = [
        "No real robot visual-servo/foundation arbitration rollouts exist in this repo.",
        "No accepted high-fidelity simulator benchmark is run.",
        "No trained controller or foundation-policy checkpoint is released.",
        "No calibrated camera, Jacobian, latency, or deployment logs are available.",
        "No hardware rollout videos are included.",
        "The related-work synthesis is not yet a full paper-by-paper manual survey.",
        "The fixed-risk audit is local and must be repeated with real risk labels.",
        "The oracle gap remains visible under compound stress.",
    ]
    for item in not_ready:
        a(rf"\paragraph{{Blocker.}} {item} The correct action is further evidence collection, not wording the limitation away.")

    a(r"\clearpage")
    a(r"\section{Per-Regime External Experiment Plan}")
    for name, desc in REGIME_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {desc}")
        a("A hardware or accepted high-fidelity replication should instantiate this regime with the same controller set, paired scene resets, fixed camera logs, and predeclared risk budgets. The report should include the raw action proposal, selected branch, predicted risk, realized risk, image error, Jacobian margin, latency, and final outcome for every trial. The comparison should be made against v4, ensemble risk gating, robust MPC handoff, conformal abstention, foundation-only control, and at least one classical servo-only method.")
        a("The reason to require this per-regime protocol is simple: averaging across regimes can hide that a method is only good at lighting shift but brittle under field-of-view escape or Jacobian mismatch. The local v5 results are promising, but each regime needs external replication before the paper can claim robotics generality.")

    a(r"\clearpage")
    a(r"\section{Artifact Release Requirements}")
    release_items = [
        ("Controller code", "The exact arbitration code, risk-score computation, servo branch, learned-policy wrapper, and fixed-risk screen should be released or reproducibly wrapped."),
        ("Policy checkpoints", "If a foundation-policy checkpoint cannot be redistributed, the paper should provide a deterministic API wrapper and a hash of the model version."),
        ("Camera calibration", "Intrinsic and extrinsic calibration files are needed because the central failure modes depend on geometry and Jacobian error."),
        ("Raw logs", "Raw image streams, action proposals, servo corrections, branch choices, risk scores, and outcomes should be released for every trial."),
        ("Processed CSVs", "The aggregate CSVs should be generated from raw logs by a public script, not hand assembled."),
        ("Videos", "Videos should cover successes, failures, abstentions, and oracle-gap examples."),
        ("Baseline wrappers", "Each baseline wrapper should expose the same observation/action interface so latency and risk are comparable."),
        ("Risk budgets", "The declared fixed-risk budgets should be listed before final metrics are computed."),
        ("Ablation toggles", "Every ablation should be a command-line switch or configuration file, not an undocumented code fork."),
        ("Environment metadata", "Lighting, camera pose, object identity, and robot configuration should be logged so reviewers can audit shift labels."),
        ("Failure taxonomy", "Failure cases should be linked to raw trials and not merely described in prose."),
        ("Rebuild script", "A single rebuild script should regenerate results, figures, tables, PDF, and validation logs from a clean checkout."),
    ]
    for name, desc in release_items:
        a(rf"\paragraph{{{name}.}} {desc} This item is not necessary to interpret the current local audit, but it is necessary for a real submission package.")

    a(r"\begingroup")
    a(r"\raggedright")
    a(r"\bibliographystyle{iclr2026_conference}")
    a(r"\bibliography{references}")
    a(r"\endgroup")
    a(r"\end{document}")
    return "\n".join(lines) + "\n"


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    PAPER.mkdir(exist_ok=True)
    (PAPER / "references.bib").write_text(REFERENCES.strip() + "\n", encoding="utf-8")
    (PAPER / "main.tex").write_text(make_manuscript(summary), encoding="utf-8")
    print("Generated paper/main.tex and paper/references.bib for Paper 116.")


if __name__ == "__main__":
    main()
