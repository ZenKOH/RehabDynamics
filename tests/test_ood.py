from pathlib import Path

from rehabdynamics.metrics.gait import compute_trial_metrics
from rehabdynamics.safety.ood import assess_ood, load_reference_config

CFG = Path("configs/reference_envelope.yaml")


def test_nominal_trial_no_rule_violation(trial):
    assessment = assess_ood(compute_trial_metrics(trial), {}, load_reference_config(CFG))
    assert assessment.status == "green"


def test_stroke_escalates_to_red(trial):
    assessment = assess_ood(
        compute_trial_metrics(trial), {"pathology": "stroke"}, load_reference_config(CFG)
    )
    assert assessment.status == "red"
    assert any("stroke" in v for v in assessment.violations)
