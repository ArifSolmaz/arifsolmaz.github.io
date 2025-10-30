"""Transit + starspot modeling utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

try:  # pragma: no cover - import guard mirrors other modules
    import pymc as pm
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "SpotLightCurve's spot modeling utilities require PyMC. Install it via `pip install pymc`."
    ) from exc

try:  # pragma: no cover - optional dependency
    import starry
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "SpotLightCurve's spot modeling utilities require starry. Install it via `pip install starry`."
    ) from exc

from pytensor import tensor as pt
from pytensor.compile.ops import as_op


def _kipping_to_quad(q1: float, q2: float) -> tuple[float, float]:
    """Convert Kipping (2013) quadratic LD reparameterisation to (u1, u2)."""

    sqrt_q1 = math.sqrt(q1)
    u1 = 2.0 * sqrt_q1 * q2
    u2 = sqrt_q1 * (1.0 - 2.0 * q2)
    return u1, u2


def _evaluate_one_spot_flux(
    time: np.ndarray,
    period: float,
    t0: float,
    exptime: float,
    supersample: int,
    ydeg: int,
    r: float,
    a_rs: float,
    cos_i: float,
    q1: float,
    q2: float,
    spot_lat: float,
    spot_lon: float,
    spot_radius: float,
    spot_contrast: float,
) -> np.ndarray:
    """Compute the starry flux for a single circular starspot and transiting planet."""

    u1, u2 = _kipping_to_quad(q1, q2)

    starry.config.lazy = False
    starry.config.quiet = True

    stellar_map = starry.Map(ydeg=ydeg)
    stellar_map.limb_dark = [u1, u2]

    if spot_radius > 0.0:
        stellar_map.add_spot(
            lat=float(spot_lat),
            lon=float(spot_lon),
            radius=float(spot_radius),
            contrast=float(spot_contrast),
        )

    star = starry.Primary(map=stellar_map, r=1.0, m=1.0)
    inc = math.degrees(math.acos(np.clip(cos_i, 0.0, 1.0)))
    planet = starry.Secondary(
        r=float(r),
        m=0.0,
        porb=float(period),
        prot=float(period),
        t0=float(t0),
        inc=float(inc),
        a=float(a_rs),
        ecc=0.0,
        w=90.0,
    )

    system = starry.System(star, planet)
    flux = system.flux(time, dt=exptime, oversample=supersample)
    return np.asarray(flux).reshape(-1)


@dataclass
class SpotModelConfig:
    """Configuration for the transit + starspot model."""

    period: float
    t0: float
    exposure_time: float
    supersample: int = 7
    ydeg: int = 15
    r_bounds: tuple[float, float] = (0.01, 0.2)
    a_rs_log_mu: float = math.log(15.0)
    a_rs_log_sigma: float = 0.4
    spot_radius_bounds: tuple[float, float] = (1.0, 30.0)
    spot_contrast_bounds: tuple[float, float] = (-0.9, 0.9)


def fit_transit_spot(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    config: SpotModelConfig,
    *,
    draws: int = 1000,
    tune: int = 1000,
    chains: int = 2,
    target_accept: float = 0.9,
    random_seed: Optional[int] = None,
    progressbar: bool = True,
):
    """Fit a single-spot transit model using PyMC and starry."""

    time = np.asarray(time, dtype=float)
    flux = np.asarray(flux, dtype=float)
    flux_err = np.asarray(flux_err, dtype=float)

    if time.ndim != 1:
        raise ValueError("`time` must be a one-dimensional array.")
    if flux.shape != time.shape or flux_err.shape != time.shape:
        raise ValueError("`flux` and `flux_err` must match the shape of `time`.")
    if np.any(flux_err <= 0):
        raise ValueError("All entries of `flux_err` must be positive.")
    if config.supersample < 1:
        raise ValueError("`supersample` must be >= 1.")
    if config.exposure_time <= 0:
        raise ValueError("`exposure_time` must be positive.")

    compute_flux = as_op(  # type: ignore[misc]
        itypes=[
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
            pt.dscalar,
        ],
        otypes=[pt.dvector],
    )(
        lambda r, a_rs, cos_i, q1, q2, spot_lat, spot_lon, spot_radius, spot_contrast: _evaluate_one_spot_flux(
            time=time,
            period=config.period,
            t0=config.t0,
            exptime=config.exposure_time,
            supersample=config.supersample,
            ydeg=config.ydeg,
            r=float(r),
            a_rs=float(a_rs),
            cos_i=float(cos_i),
            q1=float(q1),
            q2=float(q2),
            spot_lat=float(spot_lat),
            spot_lon=float(spot_lon),
            spot_radius=float(spot_radius),
            spot_contrast=float(spot_contrast),
        )
    )

    coords = {"time": np.arange(time.size)}

    with pm.Model(coords=coords) as model:
        pm.Data("time", time, dims="time")
        pm.Data("flux", flux, dims="time")
        pm.Data("flux_err", flux_err, dims="time")

        r = pm.Uniform("r", lower=config.r_bounds[0], upper=config.r_bounds[1])
        a_rs = pm.LogNormal("a_rs", mu=config.a_rs_log_mu, sigma=config.a_rs_log_sigma)
        cos_i = pm.Uniform("cos_i", lower=0.0, upper=1.0)

        q1 = pm.Uniform("q1", lower=0.0, upper=1.0)
        q2 = pm.Uniform("q2", lower=0.0, upper=1.0)

        sqrt_q1 = pm.math.sqrt(q1)
        u1 = pm.Deterministic("u1", 2.0 * sqrt_q1 * q2)
        u2 = pm.Deterministic("u2", sqrt_q1 * (1.0 - 2.0 * q2))

        spot_lat = pm.Uniform("spot_lat", lower=-90.0, upper=90.0)
        spot_lon = pm.Uniform("spot_lon", lower=0.0, upper=360.0)
        spot_radius = pm.Uniform(
            "spot_radius",
            lower=config.spot_radius_bounds[0],
            upper=config.spot_radius_bounds[1],
        )
        spot_contrast = pm.Uniform(
            "spot_contrast",
            lower=config.spot_contrast_bounds[0],
            upper=config.spot_contrast_bounds[1],
        )

        model_flux = pm.Deterministic(
            "model_flux",
            compute_flux(r, a_rs, cos_i, q1, q2, spot_lat, spot_lon, spot_radius, spot_contrast),
            dims="time",
        )

        impact = pm.Deterministic("impact", a_rs * cos_i)
        inclination = pm.Deterministic("inclination", pm.math.arccos(cos_i) * 180.0 / np.pi)

        pm.Normal("obs", mu=model_flux, sigma=flux_err, observed=flux, dims="time")

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=progressbar,
            return_inferencedata=True,
        )

    return trace


__all__ = [
    "SpotModelConfig",
    "fit_transit_spot",
]
