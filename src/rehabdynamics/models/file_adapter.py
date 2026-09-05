from __future__ import annotations

from pathlib import Path

import numpy as np

from rehabdynamics.io.opensim import parse_dynamics_table
from rehabdynamics.models.base import DynamicsModel
from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


class GaitDynamicsFileAdapter(DynamicsModel):
    """Consume a prediction exported by the upstream Stanford workflow.

    v0.1 deliberately integrates through files rather than importing Stanford's research
    module into the production process. This keeps dependency and licensing boundaries clear.
    """

    name = "gaitdynamics-file"

    def __init__(self, prediction_path: str | Path):
        self.prediction_path = Path(prediction_path)

    def predict(self, trial: MovementTrial) -> DynamicsPrediction:
        pred = parse_dynamics_table(self.prediction_path, provider=self.name)
        if len(pred.time) != len(trial.time) or not np.allclose(
            pred.time.to_numpy(), trial.time.to_numpy(), rtol=1e-4, atol=1e-4
        ):
            raise ValueError("Prediction timestamps must align with the kinematics trial")
        pred.provenance = {
            "path": str(self.prediction_path),
            "integration": "file-boundary",
            "upstream": "stanfordnmbl/GaitDynamics",
        }
        return pred
