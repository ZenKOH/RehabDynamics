from __future__ import annotations

import math

import numpy as np
import pandas as pd

from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


def _rom_deg(series: pd.Series) -> float | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None
    value = float(clean.max() - clean.min())
    # OpenSim files commonly declare inDegrees; the caller converts only when explicit.
    return value


def _asymmetry(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or (abs(a) + abs(b)) == 0:
        return None
    return float(200.0 * abs(a - b) / (abs(a) + abs(b)))


def compute_trial_metrics(trial: MovementTrial) -> dict[str, float | None]:
    kin = trial.kinematics
    metrics: dict[str, float | None] = {
        "duration_s": trial.duration_s,
        "sample_rate_hz": trial.sample_rate_hz,
        "forward_speed_m_s": None,
    }

    if "pelvis_tx" in kin.columns and trial.duration_s > 0:
        tx = pd.to_numeric(kin["pelvis_tx"], errors="coerce").dropna()
        if len(tx) >= 2:
            metrics["forward_speed_m_s"] = abs(float(tx.iloc[-1] - tx.iloc[0])) / trial.duration_s

    for joint in ("hip_flexion", "knee_angle", "ankle_angle"):
        sides: dict[str, float | None] = {}
        for side in ("r", "l"):
            col = f"{joint}_{side}"
            value = _rom_deg(kin[col]) if col in kin.columns else None
            name = f"{joint.replace('angle', '').rstrip('_')}_rom_{side}_deg"
            metrics[name] = value
            sides[side] = value
        metrics[f"{joint.replace('angle', '').rstrip('_')}_rom_asymmetry_pct"] = _asymmetry(
            sides["r"], sides["l"]
        )

    return metrics


def compute_dynamics_metrics(pred: DynamicsPrediction | None) -> dict[str, float | None]:
    if pred is None:
        return {}
    values = pred.values
    result: dict[str, float | None] = {}
    vertical_terms = ("force_vy", "force_vz", "vertical")
    vertical_candidates = [
        column
        for column in values.columns
        if any(term in column.lower() for term in vertical_terms)
    ]
    for col in vertical_candidates[:2]:
        series = pd.to_numeric(values[col], errors="coerce").dropna()
        if not series.empty:
            result[f"peak_{col}"] = float(np.nanmax(series.to_numpy()))
    return result


def finite_metric_dict(metrics: dict[str, float | None]) -> dict[str, float | None]:
    out: dict[str, float | None] = {}
    for key, value in metrics.items():
        if value is None or not math.isfinite(value):
            out[key] = None
        else:
            out[key] = float(value)
    return out
