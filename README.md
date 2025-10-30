# SpotLightCurve

SpotLightCurve is an open-source toolkit for analyzing photometric observations of exoplanet host stars with stellar activity (spots, faculae, rotational modulation). It wraps community libraries such as `lightkurve`, `pymc`, `exoplanet`, and `starry` inside a cohesive workflow so you can download light curves, preprocess them, and infer both planetary and stellar parameters.

## Features

- Download TESS and Kepler/K2 light curves with a consistent API
- Perform sigma-clipping, pixel-level decorrelation, and other preprocessing steps
- Build a joint Gaussian Process + transit model using PyMC and exoplanet
- Generate diagnostic plots, posterior summaries, and NetCDF outputs
- Command-line interface for automated runs and reproducible analyses
- Ready-to-run tutorial for Google Colab users

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/arifsolmaz/arifsolmaz.github.io.git
cd arifsolmaz.github.io
pip install -e .
```

> SpotLightCurve requires Python 3.9+ and depends on scientific Python libraries such as PyMC, exoplanet, lightkurve, and starry. Installing inside a virtual environment (e.g., `venv` or `conda`) is recommended.

## Quickstart

### 1. Download a light curve

```bash
spotlightcurve download "TIC 206544316" --sector 15 --output lc.json
```

### 2. Run the joint model

```bash
spotlightcurve run lc.json --period 3.5347 --t0 2458325.123 --draws 1000 --tune 1000
```

This command will produce posterior samples in `results/trace.nc`. Inspect them in Python with ArviZ:

```python
import arviz as az
trace = az.from_netcdf("results/trace.nc")
az.summary(trace)
```

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
├── __init__.py
├── cli.py             # Typer-based command-line interface
├── diagnostics.py     # Plotting and posterior summaries
├── io/
│   ├── __init__.py    # Core dataclasses and re-exports
│   └── tess.py        # TESS download helpers and quality masks
├── model.py           # PyMC/Exoplanet model construction
└── preprocess.py      # Quality masks and detrending hooks
```

## Development

1. Fork and clone the repository.
2. Create a new virtual environment and install in editable mode: `pip install -e .[dev]` (coming soon).
3. Run the CLI or import the modules in notebooks as you iterate.
4. Open pull requests with improvements or new instrument loaders.

## License

SpotLightCurve is released under the MIT License. See [LICENSE](LICENSE) for details.
