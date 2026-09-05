from __future__ import annotations

from io import StringIO
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from rehabdynamics.io.opensim import OpenSimFormatError, parse_mot
from rehabdynamics.models.demo import DemoDynamicsModel
from rehabdynamics.pipeline import analyse_trial

app = FastAPI(
    title="RehabDynamics API",
    version="0.1.0",
    description="Research API for rehabilitation biomechanics QC, metrics and uncertainty screening.",
)
REFERENCE = Path("configs/reference_envelope.yaml")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/v1/analyse")
async def analyse(
    motion: UploadFile = File(...),
    pathology: str | None = Form(None),
    assistive_device: str | None = Form(None),
    demo_dynamics: bool = Form(False),
) -> dict:
    try:
        text = (await motion.read()).decode("utf-8")
        metadata = {
            k: v
            for k, v in {"pathology": pathology, "assistive_device": assistive_device}.items()
            if v
        }
        trial = parse_mot(StringIO(text), metadata=metadata)
        model = DemoDynamicsModel() if demo_dynamics else None
        result = analyse_trial(trial, reference_config=REFERENCE, model=model)
        return result.model_dump(mode="json")
    except (UnicodeDecodeError, OpenSimFormatError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
