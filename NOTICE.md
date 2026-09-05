# Third-party notice and boundary

RehabDynamics is an independent research project. It is **not** affiliated with, endorsed by, or a clinical product of Stanford University.

The project is designed to interoperate with open biomechanics tools and datasets, including GaitDynamics, AddBiomechanics, OpenSim, Nimble Physics and OpenCap. Their code, model weights, datasets and trademarks remain subject to their own licences, terms and attribution requirements.

RehabDynamics intentionally does not vendor the Stanford GaitDynamics source code or pretrained checkpoints. The v0.1 integration boundary accepts OpenSim-compatible inputs and precomputed prediction files. This separation is deliberate so that upstream licensing, environment requirements and model updates remain explicit.

Before commercial use, independently verify the licence and provenance of every upstream model checkpoint and dataset used in a deployed workflow.
