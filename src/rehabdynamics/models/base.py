from __future__ import annotations

from abc import ABC, abstractmethod

from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


class DynamicsModel(ABC):
    """Provider boundary for learned or physics-based dynamics estimators."""

    name: str

    @abstractmethod
    def predict(self, trial: MovementTrial) -> DynamicsPrediction:
        raise NotImplementedError
