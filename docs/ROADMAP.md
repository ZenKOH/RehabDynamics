# Development roadmap

## Phase 0 — reproducible core (now)

**Deliverables**
- package, CLI, API and research UI;
- OpenSim parser;
- QC and baseline gait features;
- explicit provenance and limitations;
- conservative OOD guardrail;
- CI and tests;
- file-level GaitDynamics integration boundary.

**Kill criterion**
If the upstream model cannot be reproduced on its own examples and benchmark data, stop clinical extension work and fix reproducibility first.

## Phase 1 — benchmark engine

**Deliverables**
- B3D/AddBiomechanics dataset adapter;
- subject/study-level dataset registry;
- GRF/CoP error suite;
- missing-kinematics experiments;
- benchmark report generator;
- model/checkpoint manifest.

**Decision gate**
Confirm the original model is reproducible and identify its actual performance envelope.

## Phase 2 — OpenCap bridge

**Deliverables**
- OpenCap export adapter;
- paired OpenCap/MoCap/force-plate evaluation;
- capture-domain error decomposition;
- comparison with physics-based/OpenCap dynamics baseline.

**Decision gate**
Determine whether low-cost capture supports acceptable kinetics estimation or whether the input-domain error dominates.

## Phase 3 — GaitDynamics-Neuro

**Deliverables**
- multi-centre stroke dataset schema;
- latent representation extractor;
- OOD distance model;
- error calibration curves;
- baseline vs recalibration vs fine-tuning study;
- locked prospective validation plan.

**Decision gate**
Only advance if uncertainty can identify high-error cases with useful sensitivity/specificity.

## Phase 4 — rehabilitation research platform

**Deliverables**
- longitudinal patient/session model;
- intervention/dose metadata;
- pre/post change analysis;
- trial dashboards and research exports;
- role-based access for protected data deployments.

## Phase 5 — Human–Robot Movement Model

Add robot/exoskeleton assistance as an explicit conditioning variable. Begin with shadow mode and offline counterfactual research.

Autonomous assistance optimisation is a separate safety/regulatory programme and is not unlocked by model accuracy alone.

## 90-day execution sequence

### Days 1–30
- reproduce upstream examples;
- implement B3D benchmark adapter;
- lock metrics/provenance schema;
- create small public benchmark manifest;
- document exact upstream environment.

### Days 31–60
- run healthy held-out benchmark;
- map error vs speed/missing inputs;
- add embedding extraction and first domain-distance experiments;
- design paired OpenCap acquisition.

### Days 61–90
- complete OpenCap pilot dataset;
- pre-register stroke validation protocol;
- identify clinical sites and force-plate reference setup;
- publish benchmark/failure report and next model decision.
