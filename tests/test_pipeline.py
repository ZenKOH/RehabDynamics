from pathlib import Path

from rehabdynamics.models.demo import DemoDynamicsModel
from rehabdynamics.pipeline import analyse_trial


def test_pipeline_without_dynamics(trial):
    result = analyse_trial(trial, reference_config=Path("configs/reference_envelope.yaml"))
    assert result.provenance["dynamics_provider"] is None
    assert result.ood.status == "green"


def test_pipeline_with_demo_is_explicit(trial):
    result = analyse_trial(
        trial,
        reference_config=Path("configs/reference_envelope.yaml"),
        model=DemoDynamicsModel(),
    )
    assert "NOT-A-BIOMECHANICS-MODEL" in result.provenance["dynamics_provider"]
