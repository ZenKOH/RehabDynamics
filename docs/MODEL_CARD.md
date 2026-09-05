# Model and safety card

RehabDynamics v0.1 is a software framework, not one trained model.

## Supported inference providers

### GaitDynamics file adapter
Consumes external prediction tables produced by a separately managed GaitDynamics workflow. RehabDynamics does not assert that those predictions are clinically valid.

### Demo provider
Synthetic values used solely to test plumbing. Its provider identifier includes `NOT-A-BIOMECHANICS-MODEL` by design.

## OOD screen

The default screen is a transparent ruleset in `configs/reference_envelope.yaml`. It is **not** derived from the original GaitDynamics latent distribution and must not be described as calibrated uncertainty.

Pathological and assistive-device metadata are escalated because transfer from predominantly healthy gait must be demonstrated rather than assumed.

## Intended use

Research software for reproducible gait-data handling, benchmarking, validation and failure analysis.

## Prohibited interpretation

A green screen is not evidence of diagnosis, treatment suitability, patient safety or model correctness.
