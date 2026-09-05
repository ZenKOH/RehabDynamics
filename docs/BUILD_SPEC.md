# Complete build specification

## Product thesis

RehabDynamics is not positioned as a diagnostic gait AI. It is a validation and movement-intelligence infrastructure layer for rehabilitation research. The system should make it easier to answer four questions:

1. What movement was actually measured?
2. What dynamics were measured versus inferred?
3. Is the trial plausibly within the domain supporting the inference?
4. What evidence is required before the output can influence a clinical or robotic decision?

## Primary users

- Biomechanics and rehabilitation researchers.
- Clinical research teams evaluating gait interventions.
- Rehabilitation robotics/exoskeleton developers operating in shadow mode.
- Multi-centre studies needing reproducible OpenSim-compatible processing.

## Non-users in v0.x

- Patients making self-treatment decisions.
- Clinicians seeking autonomous diagnosis or treatment recommendations.
- Safety-critical robot controllers.

## Functional requirements

### Ingestion
- OpenSim `.mot` and compatible tables.
- Metadata: cohort, pathology, capture method, assistive device, treadmill/overground, anthropometrics.
- Future: B3D, OpenCap API export, IMU-derived kinematics, device telemetry.

### Quality control
- Monotonic timestamps.
- Sampling-rate estimation and GaitDynamics 100 Hz compatibility warning.
- Missing/non-numeric column checks.
- Explicit units and coordinate provenance.

### Features
- Trial duration and sampling rate.
- Pelvis-derived forward speed when valid.
- Joint ROM and side-to-side ROM asymmetry.
- Future: event detection, stance/swing timing, propulsion/braking impulse, symmetry of kinetic variables.

### Model providers
A `DynamicsModel` contract isolates upstream inference from core software.

v0.1 providers:
- `GaitDynamicsFileAdapter`: consumes externally generated prediction tables.
- `DemoDynamicsModel`: synthetic software-test output with an intentionally alarming provider name.

Planned providers:
- isolated GaitDynamics subprocess/container adapter;
- physics-based OpenSim inverse-dynamics baseline;
- OpenCap dynamics adapter;
- fine-tuned GaitDynamics-Neuro checkpoint adapter.

### Safety/OOD
v0.1 implements auditable rules, not false probabilistic confidence. Later versions should add:
- representation-space distance;
- Mahalanobis or kNN density estimates;
- conformal calibration against force error;
- capture-domain classifier;
- cohort- and device-specific thresholds.

### Interfaces
- CLI for reproducible batch research.
- FastAPI for service integration.
- Streamlit UI for exploratory research only.

## Data model

`MovementTrial`
- time
- kinematics
- source
- metadata
- OpenSim header

`DynamicsPrediction`
- time
- dynamics values
- provider
- provenance

`AnalysisResult`
- trial metrics
- dynamics metrics
- OOD assessment
- provenance
- limitations

## Deployment model

Core package and API use modern Python. GaitDynamics direct execution should live in a separate pinned environment/container because upstream was published with older PyTorch/CUDA dependencies. File interchange is the compatibility boundary until the upstream environment is reproducibly packaged.

## Security and privacy

- No telemetry by default.
- No automatic uploads.
- Patient datasets excluded from Git.
- Public AddBiomechanics upload is never a default pathway for protected clinical data.
- Future authenticated deployments should separate identifiable metadata from biomechanics tensors and maintain an audit log.

## Success criteria for v0.1

- Fresh clone installs and tests in CI.
- Real OpenSim-style motion files parse deterministically.
- Analyses expose provenance and limitations.
- Pathological/assistive-device contexts cannot silently appear “green”.
- Upstream predictions can be attached without copying upstream source code.
