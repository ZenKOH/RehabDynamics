import pytest

from rehabdynamics.metrics.gait import compute_trial_metrics


def test_metrics(trial):
    metrics = compute_trial_metrics(trial)
    assert metrics["forward_speed_m_s"] == pytest.approx(1.2, rel=1e-3)
    assert metrics["knee_rom_r_deg"] > 45
    assert metrics["knee_rom_asymmetry_pct"] is not None
