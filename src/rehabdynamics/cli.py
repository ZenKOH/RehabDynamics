from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from rehabdynamics.io.opensim import parse_mot
from rehabdynamics.models.file_adapter import GaitDynamicsFileAdapter
from rehabdynamics.pipeline import analyse_trial

app = typer.Typer(help="RehabDynamics research CLI")


@app.command()
def analyse(
    motion: Path = typer.Argument(..., exists=True, readable=True),
    reference: Path = typer.Option(Path("configs/reference_envelope.yaml"), "--reference"),
    predictions: Optional[Path] = typer.Option(None, "--predictions", exists=True, readable=True),
    pathology: Optional[str] = typer.Option(None, "--pathology"),
    assistive_device: Optional[str] = typer.Option(None, "--assistive-device"),
) -> None:
    """Analyse an OpenSim .mot file and optionally attach external dynamics predictions."""
    metadata = {k: v for k, v in {"pathology": pathology, "assistive_device": assistive_device}.items() if v}
    trial = parse_mot(motion, metadata=metadata)
    model = GaitDynamicsFileAdapter(predictions) if predictions else None
    result = analyse_trial(trial, reference_config=reference, model=model)
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    app()
