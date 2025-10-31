# SpotLightCurve

SpotLightCurve is an open-source toolkit for analyzing photometric observations of exoplanet host stars with stellar activity (spots, faculae, rotational modulation). It wraps community libraries such as `lightkurve`, `pymc`, `exoplanet`, and `starry` inside a cohesive workflow so you can download light curves, preprocess them, and infer both planetary and stellar parameters.

## Features

- Download TESS and Kepler/K2 light curves with a consistent API
- Perform sigma-clipping, pixel-level decorrelation, and other preprocessing steps
- Build joint Gaussian Process + transit models with PyMC/exoplanet or a
  NumPyro+tinygp backend
- Generate diagnostic plots, posterior summaries, and NetCDF outputs
- Produce HTML reports summarizing parameters and saved figures
- Command-line interface for automated runs and reproducible analyses
- Ready-to-run tutorial for Google Colab users
- Run injection--recovery experiments with quasi-periodic (stellar rotation)
  noise

## Installation

Clone the repository and install the package in editable mode. The `pymc`
extra pulls in the PyMC/exoplanet/starry stack used by the flagship backend:

```bash
git clone https://github.com/arifsolmaz/arifsolmaz.github.io.git
cd arifsolmaz.github.io
pip install -e .[pymc]
```

> SpotLightCurve requires Python 3.9+ and depends on the scientific Python stack.
> Installing inside a virtual environment (e.g., `venv` or `conda`) is recommended.

## Quickstart

### 1. Download a light curve

```bash
spotlightcurve download "TIC 206544316" --sector 15 --output lc.json
```

### 2. Run the joint model

```bash
spotlightcurve run lc.json --period 3.5347 --t0 2458325.123 --draws 1000 --tune 1000
```

This command will produce posterior samples in `results/<run_name>/trace.nc`,
figures under `results/<run_name>/figures/`, and an HTML report summarising the
fit. Inspect the NetCDF file in Python with ArviZ:

```python
import arviz as az
trace = az.from_netcdf("results/trace.nc")
az.summary(trace)
```

### YAML-driven analyses and alternative backends

For reproducible runs, capture your inputs in a YAML file and execute:

```bash
spotlightcurve analyze config.yaml --backend pymc
```

Swap `--backend numpyro` to run the lightweight NumPyro/tinygp backend. The
generated directory mirrors the quickstart artefacts and includes an HTML
report linking to saved figures and tables.

### Programmatic API

```python
from spotlightcurve.io import load_tess

bundle = load_tess("HAT-P-36", sector=49, quality="lenient")
lc = bundle.light_curve  # numpy arrays ready for modeling
```

`load_tess` returns a `LightCurveBundle` that retains the raw Lightkurve
download, the boolean quality masks that were applied, and the normalized flux
arrays used elsewhere in the package.

## Google Colab

Prefer working in the cloud? Launch the ready-to-run [Colab notebook](tutorials/spotlightcurve_colab.ipynb) or browse the [markdown walkthrough](tutorials/spotlightcurve_colab.md) for a step-by-step guide that mirrors the CLI workflow.

## Package Structure

```
spotlightcurve/
├── backends/         # PyMC and NumPyro runtime implementations
├── __init__.py
├── cli.py             # Typer-based command-line interface
├── diagnostics.py     # Plotting and posterior summaries
├── io/
│   ├── __init__.py    # Core dataclasses and re-exports
│   └── tess.py        # TESS download helpers and quality masks
├── model/
│   ├── __init__.py    # GP, spot, and comparison utilities
│   ├── compare.py
│   ├── gp.py
│   └── spot.py
├── preprocess.py      # Quality masks and detrending hooks
├── report/            # HTML report generation helpers
└── sim/
    ├── __init__.py    # Simulation helpers
    └── inject.py      # Injection--recovery with QP noise
```

## Development

1. Fork and clone the repository.
2. Create a new virtual environment and install in editable mode: `pip install -e .[dev]` (coming soon).
3. Run the CLI or import the modules in notebooks as you iterate.
4. Open pull requests with improvements or new instrument loaders.

## License

SpotLightCurve is released under the MIT License. See [LICENSE](LICENSE) for details.
