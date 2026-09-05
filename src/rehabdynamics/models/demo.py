from __future__ import annotations

import numpy as np
import pandas as pd

from rehabdynamics.models.base import DynamicsModel
from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


class DemoDynamicsModel(DynamicsModel):
    """Non-clinical synthetic provider used only to exercise the software pipeline."""

    name = "demo-synthetic-NOT-A-BIOMECHANICS-MODEL"

    def predict(self, trial: MovementTrial) -> DynamicsPrediction:
        t = trial.time.to_numpy(dtype=float)
        phase = 2 * np.pi * (t - t[0]) / max(trial.duration_s, 1e-6) * 2.0
        values = pd.DataFrame(
            {
                "demo_vertical_force_bw": 1.0 + 0.15 * np.sin(phase),
                "demo_ap_force_bw": 0.08 * np.sin(phase - np.pi / 2),
                "demo_ml_force_bw": np.zeros_like(phase),
            }
        )
        return DynamicsPrediction(
            time=trial.time.copy(),
            values=values,
            provider=self.name,
            provenance={
                "warning": "Synthetic software-test output; never use clinically or scientifically."
            },
        )
