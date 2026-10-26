# Train and export the iDex classifier

The app already includes the locally trained EfficientNet-B0 **FP32** Core ML package. A normal Git clone includes the weights; building/running iDex needs no Python, API key, separate download or model-hosting account. See [the active model contract](../../iDex/Recognition/MODEL.md), [distribution notices](../../iDex/Recognition/MODEL_NOTICE.md) and [model-manifest.json](model-manifest.json).

These first-party scripts retain the bounded data/training/export workflow. Raw datasets, tensor checkpoints, generated predictions, device reports and rollback copies stay in ignored `artifacts/replacement/`; they are not part of the model upload. Reproducing the campaign requires the pinned source data plus a CUDA training environment. Re-exporting requires a matching locally held or newly trained tensor checkpoint.

## Data and training

Use a fresh artifact root. `acquire.py` fetches pinned data files/metadata without running dataset-provided code. Review [dataset provenance](references/dataset_research.md) and the source terms before use. The original campaign used TorchVision's ImageNet initialization, grouped the source images before splitting, quarantined conflicting labels, and mapped targets to the exact151 Kanto IDs. Public split scores do not certify independent camera performance.

```powershell
# Set this to your existing isolated CUDA environment; no machine-specific path is assumed.
$env:IDEX_TRAIN_PYTHON = 'C:\path\to\venv\Scripts\python.exe'
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py metadata
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py pretrained
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py data --dataset sgtsaughter/pokemon-classification-images-151
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py data --dataset keremberke/pokemon-classification
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py data --dataset JJMack/pokemon-classification-gen1-9
& $env:IDEX_TRAIN_PYTHON scripts/replacement/acquire.py negatives
& $env:IDEX_TRAIN_PYTHON scripts/replacement/data.py
& $env:IDEX_TRAIN_PYTHON scripts/replacement/refine_groups.py
& $env:IDEX_TRAIN_PYTHON scripts/replacement/audit.py
& $env:IDEX_TRAIN_PYTHON scripts/replacement/freeze_eval_scope.py
& $env:IDEX_TRAIN_PYTHON scripts/replacement/train.py train --arch efficientnet_b0 --epochs 8 --max-minutes 35 --out artifacts/replacement/runs/efficientnet224
```

Inspect the acquisition and grouping receipts before training. The historical comparison helpers can use optional reference artifacts, but those artifacts are not app dependencies or part of the upload. Training/selection choices must use validation only; reserve the final group-partitioned test before opening predictions. Use [CAMERA_TEST_PROTOCOL.md](CAMERA_TEST_PROTOCOL.md) for an independent capture study. `run_candidates.ps1`/`followup.ps1` are optional recorded multi-model experiment wrappers, not an unbounded sweep or required app-build step.

The selected checkpoint came from an EfficientNet-B0 continuation of at most12 additional epochs at learning rate.0001, after the initial8-epoch run. Its exact checkpoint and frozen-manifest digests are recorded in `model-manifest.json`. The separate outlier-exposure branch was diagnostic and was not selected. The original observed Windows package versions are in `requirements-windows.txt`; install only into a separate compatible environment, not over another experiment.

## Export on Mac

Use an isolated Python3.11 environment with `requirements-mac.txt`. The recorded tested stack uses coremltools9.0 and torch2.14.1; the converter warns that torch is newer than its tested versions, so numerical parity remains mandatory for a new checkpoint.

```sh
python scripts/replacement/export.py --checkpoint /path/to/your/checkpoint.pt \
  --out artifacts/replacement/new-export --deployment iOS18
```

The loader uses installed TorchVision, `torch.load(weights_only=True)`, strict state-dict keys and semantic label-order equality. It does not load an arbitrary serialized model class or fetch remote implementation code. Normalization is embedded once. Export produces separate FP32 and FP16 diagnostic packages in a fresh folder; it never modifies the bundled default. The published package is the verified FP32 result. Do not choose another precision based only on file size.

## Numerical/device validation

Follow [apple/README.md](apple/README.md). Generate your own authorized validation fixtures, keep images out of the Git commit, and compare source logits on exact Apple-prepared RGB. This checks conversion separately from held-out recognition and unknown-input evaluation. Core ML compute-unit options are permissions, not evidence of actual ANE placement.

The app's unit tests cover the bundled checkpoint identity/FP32 output, known sample recognition, label coverage, and blank-image abstention. Keep model/labels/preprocessing together when replacing a trained artifact. Use a disposable checkout and new export folder for experiments; the active package should change only after a deliberate selection and validation.
