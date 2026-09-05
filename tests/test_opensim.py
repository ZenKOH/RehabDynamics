from io import StringIO

import pytest

from conftest import make_mot
from rehabdynamics.io.opensim import OpenSimFormatError, parse_mot


def test_parse_mot_metadata_and_sampling():
    trial = parse_mot(StringIO(make_mot()), metadata={"pathology": "healthy"})
    assert trial.metadata["pathology"] == "healthy"
    assert trial.sample_rate_hz == pytest.approx(100.0, rel=1e-3)
    assert "knee_angle_r" in trial.kinematics.columns


def test_reject_missing_time():
    with pytest.raises(OpenSimFormatError):
        parse_mot(StringIO("endheader\na\tb\n1\t2\n3\t4"))
