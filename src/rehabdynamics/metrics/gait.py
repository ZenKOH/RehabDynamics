from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


def _header_value(header: dict[str, str], key: str) -> str | None:
    target = key.lower()
    for name, value in header.items():
        if name.lower() == target:
            return value
    return None


def _angles_are_degrees(trial: MovementTrial) -> bool:
    declared = _header_value(trial.header, "inDegrees")
    if declared is None:
        return True
    return declared.strip().lower() not in {"no", "false", "0"}


def _rom_deg(series: pd.Series, *, input_in_degrees: bool) -> float | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None
    value = float(clean.max() - clean.min())
    return value if input_in_degrees else float(np.rad2deg(value))


def _asymmetry(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or (abs(a) + abs(b)) == 0:
        return None
    return float(200.0 * abs(a - b) / (abs(a) + abs(b)))


def _metadata_speed(metadata: dict[str, Any]) -> float | None:
    for key in ("walking_speed_m_s", "speed_m_s", "treadmill_speed_m_s"):
        value = metadata.get(key)
        if value in (None, ""):
            continue
        try:
            speed = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(speed) and speed >= 0:
            return speed
    return None


def _is_treadmill_trial(metadata: dict[str, Any]) -> bool:
    if metadata.get("treadmill") is True:
        return True
    context = " ".join(
        str(metadata.get(key, "")).lower()
        for key in ("environment", "locomotion_context", "capture_context")
    )
    return "treadmill" in context


def compute_trial_metrics(trial: MovementTrial) -> dict[str, float | None]:
    kin = trial.kinematics
    metrics: dict[str, float | None] = {
        "duration_s": trial.duration_s,
        "sample_rate_hz": trial.sample_rate_hz,
        "forward_speed_m_s": None,
    }

    supplied_speed = _metadata_speed(trial.metadata)
    if supplied_speed is not None:
        metrics["forward_speed_m_s"] = supplied_speed
    elif not _is_treadmill_trial(trial.metadata) and "pelvis_tx" in kin.columns:
        if trial.duration_s > 0:
            tx = pd.to_numeric(kin["pelvis_tx"], errors="coerce").dropna()
            if len(tx) >= 2:
                displacement = abs(float(tx.iloc[-1] - tx.iloc[0]))
                metrics["forward_speed_m_s"] = displacement / trial.duration_s

    input_in_degrees = _angles_are_degrees(trial)
    for joint in ("hip_flexion", "knee_angle", "ankle_angle"):
        sides: dict[str, float | None] = {}
        for side in ("r", "l"):
            col = f"{joint}_{side}"
            value = (
                _rom_deg(kin[col], input_in_degrees=input_in_degrees)
                if col in kin.columns
                else None
            )
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
