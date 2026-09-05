# Validation protocol

## Central question

**At what distance from the healthy gait domain does GaitDynamics-derived kinetics become unreliable for rehabilitation research?**

The protocol is intentionally stricter than showing aggregate RMSE.

## Stage A — software verification

- Parser round-trip fixtures.
- Timestamp alignment.
- Unit checks.
- Deterministic feature extraction.
- Provenance completeness.

Exit criterion: CI green across supported Python versions.

## Stage B — published-model reproduction

Goal: reproduce the upstream healthy/held-out force-estimation task before claiming any extension.

Report by subject and study:
- vertical, AP and ML GRF MAE/RMSE normalised to body weight;
- peak-force error;
- centre-of-pressure error if supported;
- error versus walking/running speed;
- error under missing-joint masks.

Exit criterion: results within a predeclared tolerance of the published benchmark or discrepancies fully explained.

## Stage C — capture-domain validation

Paired acquisition for the same trials:
1. laboratory kinematics → GaitDynamics;
2. OpenCap-derived kinematics → GaitDynamics;
3. optional OpenCap/physics baseline;
4. force plate as truth.

Primary hypothesis: camera-domain kinematic error does not push GRF error beyond the predeclared research threshold.

Report Bland–Altman analysis, subject-level confidence intervals and failure cases—not only correlation.

## Stage D — stroke/pathological validation

Stratify by impairment and walking support. Recommended variables:
- gait speed;
- Fugl-Meyer lower-extremity or equivalent impairment measure;
- assistive device;
- orthosis;
- stance-time asymmetry;
- kinematic asymmetry;
- affected side.

Primary analysis:

`domain distance → external-force prediction error`

Secondary analysis:
- identify which features dominate failure;
- compare original model, simple recalibration and fine-tuned model;
- estimate calibration curves for probability that error exceeds a predeclared threshold.

## Stage E — prospective shadow mode

Run RehabDynamics beside normal clinical/robotic workflows without controlling treatment or devices. Compare predictions with available sensor truth and clinician interpretation.

No autonomous control authority is allowed in this stage.

## Leakage controls

- Subject-level splits minimum.
- Prefer site/study holdout.
- Do not tune thresholds on the final clinical test cohort.
- Lock preprocessing before prospective validation.
- Keep model checkpoint SHA and code commit with every result.

## Reporting standard

Always report:
- cohort and exclusions;
- capture source;
- missing-data rate;
- prediction provider/checkpoint;
- OOD method/version;
- performance distribution, not just mean;
- worst decile and subgroup failures;
- whether force truth was directly measured.
