# Reproduction and benchmark scope

A complete CSV training/export path now saves the population-fitted preprocessing/PCA/K-means pipeline, numeric feature order and customer representation table, with reload parity.

## Execute a recorded profile

```sh
python run_reproduction.py --profile checks --output reproduced/checks
```

Use a new output directory for each run. The driver writes command logs, source/input SHA-256 values, versions and an explicit outcome. It does not silently download data or turn generated fixtures into dataset-performance claims.

| Profile | Actual scope | Required inputs |
|---|---|---|
| `checks` | Offline behavioral regressions; not a fresh dataset benchmark | None |
| `train-csv` | Population-fitted segmentation and customer representation; no hidden customer refit | population, customers |

Supply named paths with `--input name=/absolute/path`. Exact commands are versioned in [reproduction.json](reproduction.json); direct training commands and preparation contracts are below.

## Evidence boundary

The historical AZDIAS population/customer inputs were not available. No synthetic fixture has been substituted for that historical segmentation benchmark.

Keep input acquisition and source credits in [DATA.md](DATA.md). Historical results, new reference runs and small contract fixtures have separate evidential scope.

## Recorded command definitions

### checks

```text
{python} smoke_test.py
```

### train-csv

```text
{python} train.py {input:population} {input:customers} --output {output}/training
```

`{python}` is the current interpreter. `{output}` is the new run directory. `{input:name}` refers to a named absolute input path supplied to the driver. Install declared dependencies in a clean environment before executing. Never execute untrusted serialized models or notebooks.
