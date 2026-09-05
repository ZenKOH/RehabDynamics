# Architecture

## Design principles

### 1. Separate measurement from inference
A result must distinguish raw/derived kinematics, measured dynamics and AI-estimated dynamics. Model outputs never overwrite source measurements.

### 2. Separate upstream research environments
GaitDynamics is treated as a provider rather than imported wholesale. This avoids dependency collision and makes model provenance explicit.

### 3. Make uncertainty visible
The first release uses conservative, inspectable rules. A model-specific OOD estimator may replace them only after it is calibrated against actual prediction error.

### 4. Preserve provenance
Every result should eventually be reproducible from dataset version, subject/trial ID, preprocessing configuration, model checkpoint SHA and software commit.

## Components

### `io`
OpenSim parsing today; B3D/OpenCap/device adapters later.

### `metrics`
Feature extraction independent of model providers.

### `models`
Provider interface and adapters. Direct GaitDynamics execution should be containerised when implemented.

### `safety`
OOD/domain-shift logic. This package should remain independent of UI presentation.

### `pipeline`
Orchestrates parsing-derived metrics, safety assessment, optional inference and result provenance.

### `api`, `ui`, `cli`
Thin interfaces. Scientific logic stays in package modules.

## Future data-flow for GaitDynamics-Neuro

```text
paired clinical acquisition
  ├── optical MoCap / OpenCap
  ├── force plates / instrumented treadmill
  └── clinical impairment labels
           ↓
canonical OpenSim representation
           ↓
original GaitDynamics ──→ prediction error
           ↓                    ↓
representation embedding ──→ domain distance
           ↓                    ↓
        calibration: P(error > clinically relevant threshold | distance, cohort)
           ↓
uncertainty-aware neuro gait model
```
