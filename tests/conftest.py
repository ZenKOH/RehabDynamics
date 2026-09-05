from __future__ import annotations

from io import StringIO

import numpy as np
import pytest

from rehabdynamics.io.opensim import parse_mot


def make_mot(speed: float = 1.2, seconds: float = 2.0, hz: int = 100) -> str:
    t = np.linspace(0, seconds, int(seconds * hz) + 1)
    rows = [
        "Coordinates",
        "version=1",
        f"nRows={len(t)}",
        "nColumns=8",
        "inDegrees=yes",
        "endheader",
        "time\tpelvis_tx\tknee_angle_r\tknee_angle_l\thip_flexion_r\thip_flexion_l\tankle_angle_r\tankle_angle_l",
    ]
    for x in t:
        phase = 2 * np.pi * x
        rows.append(
            "\t".join(
                f"{v:.6f}"
                for v in [
                    x,
                    speed * x,
                    35 + 25 * np.sin(phase),
                    35 + 23 * np.sin(phase + np.pi),
                    20 + 18 * np.sin(phase + 0.3),
                    20 + 17 * np.sin(phase + np.pi + 0.3),
                    5 + 12 * np.sin(phase - 0.4),
                    5 + 11 * np.sin(phase + np.pi - 0.4),
                ]
            )
        )
    return "\n".join(rows)


@pytest.fixture()
def trial():
    return parse_mot(StringIO(make_mot()))
