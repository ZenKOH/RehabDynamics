import numpy as np
import pytest

from rehabdynamics.metrics.gait import compute_trial_metrics


def test_metrics(trial):
    metrics = compute_trial_metrics(trial)
    assert metrics["forward_speed_m_s"] == pytest.approx(1.2, rel=1e-3)
    assert metrics["knee_rom_r_deg"] > 45
    assert metrics["knee_rom_asymmetry_pct"] is not None


def test_radian_opensim_angles_are_reported_in_degrees(trial):
    trial.header["inDegrees"] = "no"
    angle_columns = [
        column
        for column in trial.kinematics.columns
        if any(term in column for term in ("hip", "knee", "ankle"))
    ]
    trial.kinematics[angle_columns] = np.deg2rad(trial.kinematics[angle_columns])
    metrics = compute_trial_metrics(trial)
    assert metrics["knee_rom_r_deg"] > 45


def test_treadmill_does_not_infer_speed_from_pelvis_translation(trial):
    trial.metadata["environment"] = "instrumented treadmill"
    metrics = compute_trial_metrics(trial)
    assert metrics["forward_speed_m_s"] is None


def test_explicit_treadmill_speed_is_used(trial):
    trial.metadata.update({"environment": "treadmill", "treadmill_speed_m_s": 0.8})
    metrics = compute_trial_metrics(trial)
    assert metrics["forward_speed_m_s"] == pytest.approx(0.8)
