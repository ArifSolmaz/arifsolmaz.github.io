# SpotLightCurve Colab Tutorial

This guide walks through running the SpotLightCurve pipeline end-to-end in Google Colab.

## 1. Launch the notebook

1. Visit [Google Colab](https://colab.research.google.com/).
2. Click **New Notebook** (Python 3).

## 2. Install SpotLightCurve from GitHub

The package is published on GitHub. Install it (and its dependencies) in the first notebook cell:

```python
!pip install --quiet "git+https://github.com/arifsolmaz/arifsolmaz.github.io@main"
```

> Pinning to a specific commit hash is recommended for long-lived projects. Replace `@main` with a commit SHA to freeze the environment.

## 3. Import the package and supporting libraries

```python
import numpy as np
import arviz as az
import pymc as pm
import lightkurve as lk
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

from spotlightcurve.io import load_tess
from spotlightcurve.model import build_gp_transit_model
from spotlightcurve.preprocess import quality_mask, apply_mask
```

## 4. Example: HAT-P-36 in TESS Sector 49

The following cells download the light curve for HAT-P-36, obtain published ephemerides, estimate the stellar rotation period, and run the joint Gaussian-process + transit model to infer planetary and spot properties.

### 4.1 Fetch the light curve

```python
target = "HAT-P-36"
sector = 49
lc = load_tess(target, sector=sector)
lc_clean = apply_mask(lc, quality_mask(lc.flux))
```

### 4.2 Retrieve planetary ephemerides

```python
ephem = NasaExoplanetArchive.query_planet("HAT-P-36 b")
period_days = ephem["pl_orbper"][0]
t0_bjd = ephem["pl_tranmid"][0]  # BJD_TDB
t0_btjd = t0_bjd - 2457000.0      # convert to the BTJD system used by TESS
print(f"Period = {period_days:.6f} d, Transit mid-point (BTJD) = {t0_btjd:.6f}")
```

### 4.3 Estimate a stellar rotation prior

```python
lk_lc = lk.LightCurve(time=lc_clean.time, flux=lc_clean.flux)
pg = lk_lc.to_periodogram(method="lombscargle", minimum_period=1, maximum_period=25)
rot_period_guess = pg.period_at_max_power.value
print(f"Rotation-period prior ≈ {rot_period_guess:.2f} d")
```

### 4.4 Build and sample the probabilistic model

```python
model = build_gp_transit_model(
    time=lc_clean.time,
    flux=lc_clean.flux,
    flux_err=lc_clean.flux_err,
    period=period_days,
    t0=t0_btjd,
    rot_period_prior=rot_period_guess,
)

with model:
    trace = pm.sample(
        draws=1000,
        tune=1000,
        target_accept=0.9,
        chains=2,
    )
```

### 4.5 Summarize planetary and spot parameters

```python
planet_vars = ["period", "t0", "r", "impact"]
spot_vars = ["rot_period", "log_amp", "mixing"]

planet_summary = az.summary(trace, var_names=planet_vars)
spot_summary = az.summary(trace, var_names=spot_vars)

display(planet_summary)
display(spot_summary)
```

### 4.6 Visual diagnostics

```python
az.plot_trace(trace, var_names=planet_vars + spot_vars);
pg.plot()
```

## 5. Save results to Google Drive (optional)

```python
from google.colab import drive
drive.mount('/content/drive')
az.to_netcdf(trace, '/content/drive/MyDrive/spotlightcurve/trace.nc')
```

Refer back to the main README for more advanced usage patterns, including the command-line interface and multi-instrument workflows.
