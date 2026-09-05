# Data governance

## Default stance

Clinical movement data may be identifiable even when obvious demographics are removed. Video, unusual gait signatures and linked device telemetry can all increase re-identification risk.

## Rules

1. Do not commit clinical raw data, videos or model checkpoints containing restricted data.
2. Do not automatically upload clinical trials to public biomechanics services.
3. Store study identifiers separately from direct identifiers.
4. Record consent scope for secondary model development and public release independently.
5. Preserve source-dataset licences and attribution in derived benchmark manifests.
6. A public-release pipeline must be a separate, explicit action with governance approval.

## Recommended environments

- `data/public/`: pointers/manifests only, not bulk datasets.
- `data/private/`: local or secure compute mount, gitignored.
- `outputs/`: derived local analyses, gitignored unless intentionally de-identified fixtures.

## Commercialisation gate

Before any commercial workflow, conduct an IP/licence audit of upstream model code/checkpoints and a privacy/security assessment of the intended deployment architecture.
