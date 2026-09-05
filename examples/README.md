# Examples

Do not commit patient data here.

Generate or use a de-identified OpenSim `.mot` file, then run:

```bash
rehabdynamics analyse walk.mot
```

For Stanford GaitDynamics interoperability, first generate a prediction file in the separately managed upstream environment, then attach it:

```bash
rehabdynamics analyse walk.mot --predictions gaitdynamics_prediction.mot
```

A direct upstream runner will only be added after its environment and input/output contract are made reproducible in CI or a pinned container.
