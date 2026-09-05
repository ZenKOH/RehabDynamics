from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from rehabdynamics.schemas import OODAssessment


DEFAULT_WARNING = (
    "This is a transparent rule-based screening layer, not a calibrated GaitDynamics "
    "out-of-distribution probability."
)


def load_reference_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def assess_ood(
    metrics: dict[str, float | None],
    metadata: dict[str, Any],
    config: dict[str, Any],
) -> OODAssessment:
    score = 0.0
    violations: list[str] = []
    warnings = [DEFAULT_WARNING]

    for name, rule in config.get("metrics", {}).items():
        value = metrics.get(name)
        if value is None:
            continue
        if value < float(rule["min"]) or value > float(rule["max"]):
            weight = float(rule.get("weight", 1.0))
            score += weight
            violations.append(f"{name}={value:.3g} outside [{rule['min']}, {rule['max']}]")

    flag_text = " ".join(str(v).lower().replace(" ", "_") for v in metadata.values())
    matched = [flag for flag in config.get("metadata_red_flags", []) if flag in flag_text]
    if matched:
        score = max(score, float(config.get("thresholds", {}).get("amber_max", 2.0)) + 1.0)
        detail = "population/domain flag requires pathological-gait validation: "
        violations.append(detail + ", ".join(matched))

    thresholds = config.get("thresholds", {})
    green_max = float(thresholds.get("green_max", 0.0))
    amber_max = float(thresholds.get("amber_max", 2.0))
    if score <= green_max:
        status = "green"
    elif score <= amber_max:
        status = "amber"
    else:
        status = "red"

    if status == "green":
        warnings.append(
            "Green means no configured rule was violated; it does not prove model validity."
        )
    if metadata.get("pathology"):
        warnings.append(
            "Pathological gait requires cohort-specific validation before "
            "kinetic estimates are trusted."
        )

    return OODAssessment(
        status=status,
        score=score,
        violations=violations,
        warnings=warnings,
        config_version=str(config.get("version", "unknown")),
    )
