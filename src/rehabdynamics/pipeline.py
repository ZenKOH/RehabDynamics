from __future__ import annotations

from pathlib import Path
from typing import Any

from rehabdynamics.metrics.gait import (
    compute_dynamics_metrics,
    compute_trial_metrics,
    finite_metric_dict,
)
from rehabdynamics.models.base import DynamicsModel
from rehabdynamics.safety.ood import assess_ood, load_reference_config
from rehabdynamics.schemas import AnalysisResult, MovementTrial


LIMITATIONS = [
    "RehabDynamics v0.1 is research software and is not a medical device or diagnostic system.",
    "The rule-based OOD screen is a guardrail, not a calibrated probability of GaitDynamics validity.",
    "Predicted external dynamics must be validated against force-plate data in the intended population.",
    "A pathological-gait label is escalated because the healthy-gait training domain cannot be assumed to transfer.",
]


def analyse_trial(
    trial: MovementTrial,
    *,
    reference_config: str | Path,
    model: DynamicsModel | None = None,
    extra_provenance: dict[str, Any] | None = None,
) -> AnalysisResult:
    trial_metrics = finite_metric_dict(compute_trial_metrics(trial))
    cfg = load_reference_config(reference_config)
    ood = assess_ood(trial_metrics, trial.metadata, cfg)

    prediction = model.predict(trial) if model else None
    dynamics_metrics = finite_metric_dict(compute_dynamics_metrics(prediction))

    provenance: dict[str, Any] = {
        "kinematics_source": str(trial.source) if trial.source else "memory/upload",
        "dynamics_provider": prediction.provider if prediction else None,
        "dynamics_provenance": prediction.provenance if prediction else {},
        "reference_config": str(reference_config),
    }
    provenance.update(extra_provenance or {})

    return AnalysisResult(
        trial_metrics=trial_metrics,
        dynamics_metrics=dynamics_metrics,
        ood=ood,
        provenance=provenance,
        limitations=LIMITATIONS,
    )
