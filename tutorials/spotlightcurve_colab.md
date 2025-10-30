# SpotLightCurve Colab Tutorial

This guide walks through running the SpotLightCurve pipeline end-to-end in Google Colab.

## 1. Launch the notebook

1. Visit [Google Colab](https://colab.research.google.com/).
2. Click **New Notebook** (Python 3).

## 2. Install dependencies

Run the following in the first cell:

```python
!pip install spotlightcurve
```

> If you are developing locally rather than installing from PyPI, clone the repository and run `pip install -e .` in a Colab cell instead.

## 3. Import the package and supporting libraries

```python
import numpy as np
import pymc as pm
import arviz as az
from spotlightcurve.io import load_tess
from spotlightcurve.model import build_gp_transit_model
from spotlightcurve.preprocess import quality_mask, apply_mask
```

## 4. Download a light curve

```python
target = "TIC 206544316"  # replace with your target
lc = load_tess(target, sector=15)
```

## 5. Pre-process the data

```python
mask = quality_mask(lc.flux)
lc = apply_mask(lc, mask)
```

## 6. Build and sample the model

```python
model = build_gp_transit_model(
    lc.time,
    lc.flux,
    lc.flux_err,
    period=3.5347,
    t0=2458325.123,
)

with model:
    trace = pm.sample(draws=1000, tune=1000, target_accept=0.9)
```

## 7. Inspect the posterior

```python
az.summary(trace)
az.plot_trace(trace);
```

## 8. Save results to Google Drive (optional)

```python
from google.colab import drive
drive.mount('/content/drive')
az.to_netcdf(trace, '/content/drive/MyDrive/spotlightcurve/trace.nc')
```

Refer back to the main README for more advanced usage patterns, including the command-line interface and multi-instrument workflows.
