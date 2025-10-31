"""PyMC backend for the SpotLightCurve GP+transit model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import arviz as az
import numpy as np

try:  # pragma: no cover - optional dependency import guard
    import pymc as pm
    import exoplanet as xo
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The PyMC backend requires `pymc` and `exoplanet`. Install the 'pymc' extra via "
        "`pip install spotlightcurve[pymc]`."
    ) from exc


@dataclass
class BackendResult:
    """Container for PyMC backend outputs."""

    model: pm.Model
    inference: az.InferenceData
    predictive_mean: np.ndarray


def build_model(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    *,
    period: float,
    t0: float,
    rot_period_prior: Optional[float] = None,
) -> pm.Model:
    """Construct the PyMC GP+transit model."""

    with pm.Model(coords={"time": np.arange(time.size)}) as model:
        pm.Data("time", time, dims="time")
        pm.Data("flux", flux, dims="time")
        pm.Data("flux_err", flux_err, dims="time")

        log_sigma = pm.Normal("log_sigma", mu=np.log(np.std(flux)), sigma=5.0)
        log_amp = pm.Normal("log_amp", mu=np.log(np.var(flux)), sigma=5.0)

        if rot_period_prior is None:
            rot_period = pm.LogNormal("rot_period", mu=np.log(max(period, 0.1)), sigma=0.5)
        else:
            rot_period = pm.Normal(
                "rot_period", mu=rot_period_prior, sigma=0.2 * max(rot_period_prior, 1e-3)
            )

        kernel = xo.gp.terms.RotationTerm(
            log_amp=log_amp,
            period=rot_period,
            Q0=pm.InverseGamma("Q0", alpha=2, beta=0.5),
            dQ=pm.HalfNormal("dQ", sigma=5.0),
            f=pm.Uniform("mixing", lower=0.01, upper=1.0),
        )

        gp = xo.gp.GP(kernel, time, flux_err**2 + pm.math.exp(2.0 * log_sigma))

        orbit = xo.orbits.KeplerianOrbit(
            period=pm.Normal("period", mu=period, sigma=1e-3),
            t0=pm.Normal("t0", mu=t0, sigma=1e-3),
            b=pm.Uniform("impact", lower=0.0, upper=1.0),
        )

        u = xo.distributions.QuadLimbDark("u")
        r = pm.Uniform("r", lower=0.01, upper=0.2)

        light_curve = (
            xo.LimbDarkLightCurve(u).get_light_curve(orbit=orbit, r=r, t=time).flatten()
        )

        pm.Normal("obs", mu=gp.predict() + light_curve, sigma=flux_err, observed=flux, dims="time")

    return model


def run(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    *,
    period: float,
    t0: float,
    rot_period_prior: Optional[float] = None,
    draws: int = 2000,
    tune: int = 2000,
    chains: int = 2,
    target_accept: float = 0.9,
    random_seed: Optional[int] = None,
    progressbar: bool = True,
) -> BackendResult:
    """Fit the PyMC model and return the inference results."""

    model = build_model(
        time,
        flux,
        flux_err,
        period=period,
        t0=t0,
        rot_period_prior=rot_period_prior,
    )

    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=progressbar,
            return_inferencedata=True,
        )
        posterior_predictive = pm.sample_posterior_predictive(
            trace, var_names=["obs"], extend_inferencedata=True, progressbar=progressbar
        )

    if isinstance(posterior_predictive, az.InferenceData):
        inference = posterior_predictive
        obs_pred = inference.posterior_predictive["obs"].mean(dim=("chain", "draw")).values
    else:  # pragma: no cover - fallback for older PyMC versions
        inference = trace
        obs_pred = np.asarray(posterior_predictive["obs"]).mean(axis=0)

    return BackendResult(model=model, inference=inference, predictive_mean=np.asarray(obs_pred))


__all__ = ["BackendResult", "build_model", "run"]
