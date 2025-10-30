"""Probabilistic modeling utilities for SpotLightCurve."""

from __future__ import annotations

from typing import Optional

import numpy as np

try:
    import pymc as pm
    import exoplanet as xo
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "SpotLightCurve's modeling module requires pymc and exoplanet. Install them via `pip install pymc exoplanet`."
    ) from exc


def build_gp_transit_model(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    period: float,
    t0: float,
    rot_period_prior: Optional[float] = None,
):
    """Construct a PyMC model combining a GP rotation term with a transit."""

    with pm.Model() as model:
        log_sigma = pm.Normal("log_sigma", mu=np.log(np.std(flux)), sigma=5.0)
        log_amp = pm.Normal("log_amp", mu=np.log(np.var(flux)), sigma=5.0)

        if rot_period_prior is None:
            rot_period = pm.LogNormal("rot_period", mu=np.log(period), sigma=0.5)
        else:
            rot_period = pm.Normal("rot_period", mu=rot_period_prior, sigma=0.2 * rot_period_prior)

        kernel = xo.gp.terms.RotationTerm(
            log_amp=log_amp,
            period=rot_period,
            Q0=pm.InverseGamma("Q0", alpha=2, beta=0.5),
            dQ=pm.HalfNormal("dQ", sigma=5.0),
            f=pm.Uniform("mixing", lower=0.01, upper=1.0),
        )

        gp = xo.gp.GP(kernel, time, flux_err ** 2 + pm.math.exp(2.0 * log_sigma))

        orbit = xo.orbits.KeplerianOrbit(
            period=pm.Normal("period", mu=period, sigma=1e-3),
            t0=pm.Normal("t0", mu=t0, sigma=1e-3),
            b=pm.Uniform("impact", lower=0.0, upper=1.0),
        )

        u = xo.distributions.QuadLimbDark("u")
        r = pm.Uniform("r", lower=0.01, upper=0.2)

        light_curve = (
            xo.LimbDarkLightCurve(u)
            .get_light_curve(orbit=orbit, r=r, t=time)
            .flatten()
        )

        pm.Normal("obs", mu=gp.predict() + light_curve, sigma=flux_err, observed=flux)

    return model


__all__ = ["build_gp_transit_model"]

from .gp import RotationPeriodResult, estimate_rotation_period, fit_qp_gp  # noqa: E402
from .spot import SpotModelConfig, fit_transit_spot  # noqa: E402

__all__ += [
    "RotationPeriodResult",
    "estimate_rotation_period",
    "fit_qp_gp",
    "SpotModelConfig",
    "fit_transit_spot",
]
