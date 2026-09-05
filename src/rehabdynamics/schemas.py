from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field


@dataclass(slots=True)
class MovementTrial:
    """Canonical in-memory representation of one OpenSim-compatible trial."""

    time: pd.Series
    kinematics: pd.DataFrame
    source: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    header: dict[str, str] = field(default_factory=dict)

    @property
    def duration_s(self) -> float:
        if len(self.time) < 2:
            return 0.0
        return float(self.time.iloc[-1] - self.time.iloc[0])

    @property
    def sample_rate_hz(self) -> float | None:
        if len(self.time) < 2 or self.duration_s <= 0:
            return None
        return float((len(self.time) - 1) / self.duration_s)


@dataclass(slots=True)
class DynamicsPrediction:
    """Predicted or measured external dynamics aligned to a MovementTrial."""

    time: pd.Series
    values: pd.DataFrame
    provider: str
    provenance: dict[str, Any] = field(default_factory=dict)


class OODAssessment(BaseModel):
    status: str = Field(pattern="^(green|amber|red)$")
    score: float
    violations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    config_version: str


class AnalysisResult(BaseModel):
    trial_metrics: dict[str, float | None]
    dynamics_metrics: dict[str, float | None] = Field(default_factory=dict)
    ood: OODAssessment
    provenance: dict[str, Any]
    limitations: list[str]
