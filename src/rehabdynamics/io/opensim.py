from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import TextIO

import pandas as pd

from rehabdynamics.schemas import DynamicsPrediction, MovementTrial


class OpenSimFormatError(ValueError):
    pass


def _read_text(source: str | Path | TextIO) -> tuple[str, Path | None]:
    if hasattr(source, "read"):
        return source.read(), None
    path = Path(source)
    return path.read_text(encoding="utf-8"), path


def _split_header(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    end_index = None
    header: dict[str, str] = {}
    for i, raw in enumerate(lines):
        line = raw.strip()
        if line.lower() == "endheader":
            end_index = i
            break
        if "=" in line:
            key, value = line.split("=", 1)
            header[key.strip()] = value.strip()
    if end_index is None:
        return {}, text
    return header, "\n".join(lines[end_index + 1 :])


def parse_mot(source: str | Path | TextIO, metadata: dict | None = None) -> MovementTrial:
    text, path = _read_text(source)
    header, body = _split_header(text)
    try:
        frame = pd.read_csv(StringIO(body), sep=r"\s+|\t+", engine="python")
    except Exception as exc:  # pragma: no cover - pandas error details vary
        raise OpenSimFormatError(f"Could not parse OpenSim table: {exc}") from exc
    if "time" not in frame.columns:
        raise OpenSimFormatError("OpenSim motion file must contain a 'time' column")
    if len(frame) < 2:
        raise OpenSimFormatError("Trial must contain at least two samples")
    time = pd.to_numeric(frame.pop("time"), errors="raise")
    if not time.is_monotonic_increasing:
        raise OpenSimFormatError("Time column must be monotonically increasing")
    kin = frame.apply(pd.to_numeric, errors="coerce")
    if kin.isna().all(axis=None):
        raise OpenSimFormatError("No numeric kinematic columns were found")
    return MovementTrial(
        time=time.reset_index(drop=True),
        kinematics=kin.reset_index(drop=True),
        source=path,
        metadata=metadata or {},
        header=header,
    )


def parse_dynamics_table(
    source: str | Path | TextIO,
    provider: str = "external",
) -> DynamicsPrediction:
    text, _ = _read_text(source)
    _, body = _split_header(text)
    frame = pd.read_csv(StringIO(body), sep=r"\s+|\t+", engine="python")
    if "time" not in frame.columns:
        raise OpenSimFormatError("Dynamics file must contain a 'time' column")
    time = pd.to_numeric(frame.pop("time"), errors="raise").reset_index(drop=True)
    values = frame.apply(pd.to_numeric, errors="coerce").reset_index(drop=True)
    return DynamicsPrediction(time=time, values=values, provider=provider)
