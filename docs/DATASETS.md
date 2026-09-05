# Dataset registry and acquisition strategy

RehabDynamics does not redistribute external datasets. Register versions and licences locally and keep raw/private data outside Git.

| Dataset / source | Purpose | Required fields | Governance note |
|---|---|---|---|
| AddBiomechanics | healthy/general movement benchmark, reproduction | OpenSim/B3D kinematics and forces | Public data; preserve attribution/licence metadata |
| GaitDynamics evaluation cohorts | reproduce published tasks | kinematics + force truth | Follow source-study licences |
| OpenCap paired validation | capture-domain transfer | video/OpenCap kinematics + MoCap + force plates | consent must cover video and derived biomechanics |
| Stroke cohort | pathological validation and OOD calibration | kinematics + forces + impairment/assistive metadata | clinical governance; no automatic public upload |
| Robot/exoskeleton cohort | human–robot domain shift | kinematics + dynamics + assistance commands | device telemetry provenance required |

## Minimum dataset manifest

Each registered dataset should include:

```yaml
name: example
version: 1
source_url: ...
licence: ...
subjects: 0
trials: 0
capture: optical_mocap
force_truth: force_plate
population: healthy
allowed_uses: [research]
sha256_manifest: ...
```

## Split policy

Never split random windows from the same subject across train and test. Primary evaluation is subject-level and, where possible, study/site-level holdout. A clinical model should also have an untouched prospective cohort.
