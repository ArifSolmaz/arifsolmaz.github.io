"""Gaussian-process helpers for rotational modulation analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from astropy.timeseries import LombScargle

try:
    import pymc as pm
    import exoplanet as xo
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "spotlightcurve.model.gp requires pymc and exoplanet. Install them via `pip install pymc exoplanet`."
    ) from exc


@dataclass
class RotationPeriodResult:
    """Container for Lomb-Scargle rotation-period estimates."""

    period: float
    frequency: np.ndarray
    power: np.ndarray
    false_alarm_probability: float


def estimate_rotation_period(
    time: np.ndarray,
    flux: np.ndarray,
    *,
    min_period: float = 0.1,
    max_period: Optional[float] = None,
    oversample_factor: float = 5.0,
) -> RotationPeriodResult:
    """Estimate the stellar rotation period using a Lomb-Scargle periodogram.

    Parameters
    ----------
    time
        Observation times in days.
    flux
        Flux measurements corresponding to ``time``.
    min_period
        Minimum period (in days) to search. Defaults to 0.1 days.
    max_period
        Maximum period (in days) to search. If ``None``, defaults to the
        observational baseline.
    oversample_factor
        Samples per peak for the Lomb-Scargle frequency grid.

    Returns
    -------
    RotationPeriodResult
        Dataclass containing the best period and periodogram arrays.
    """

    time = np.asarray(time)
    flux = np.asarray(flux)

    finite_mask = np.isfinite(time) & np.isfinite(flux)
    if not np.any(finite_mask):
        raise ValueError("No finite samples provided for period estimation.")

    time = time[finite_mask]
    flux = flux[finite_mask]

    baseline = np.nanmax(time) - np.nanmin(time)
    if max_period is None:
        max_period = baseline if baseline > 0 else min_period * 10

    if max_period <= min_period:
        raise ValueError("max_period must be greater than min_period.")

    min_frequency = 1.0 / max_period
    max_frequency = 1.0 / min_period

    flux_centered = flux - np.nanmedian(flux)

    ls = LombScargle(time, flux_centered)
    frequency, power = ls.autopower(
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        samples_per_peak=oversample_factor,
        method="fast",
    )

    if power.size == 0:
        raise RuntimeError("Lomb-Scargle failed to compute a valid periodogram.")

    best_frequency = frequency[np.argmax(power)]
    best_period = 1.0 / best_frequency

    fap = ls.false_alarm_probability(power.max())

    return RotationPeriodResult(
        period=best_period,
        frequency=frequency,
        power=power,
        false_alarm_probability=fap,
    )


def fit_qp_gp(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: Optional[np.ndarray] = None,
    *,
    init_period: Optional[float] = None,
    draws: int = 1000,
    tune: int = 1000,
    target_accept: float = 0.9,
    chains: int = 2,
    cores: int = 1,
):
    """Fit a quasi-periodic Gaussian Process to the provided light curve.

    The model uses :class:`exoplanet.gp.terms.RotationTerm`, which is a
    quasi-periodic kernel implemented via :mod:`celerite2`.

    Parameters
    ----------
    time, flux, flux_err
        Light-curve arrays. ``flux_err`` defaults to a constant uncertainty
        based on the scatter of ``flux`` if omitted.
    init_period
        Optional prior guess for the rotation period in days.
    draws, tune, target_accept, chains, cores
        Sampling configuration passed to :func:`pymc.sample`.

    Returns
    -------
    dict
        Dictionary containing the PyMC model, the inference data, the GP
        object, and the MAP estimate (if available).
    """

    time = np.asarray(time)
    flux = np.asarray(flux)

    if flux_err is None:
        scatter = np.nanstd(flux)
        if not np.isfinite(scatter) or scatter == 0:
            scatter = 1e-3
        flux_err = np.full_like(flux, scatter)
    else:
        flux_err = np.asarray(flux_err)

    finite_mask = np.isfinite(time) & np.isfinite(flux) & np.isfinite(flux_err)
    if not np.any(finite_mask):
        raise ValueError("No finite samples available for GP fitting.")

    time = time[finite_mask]
    flux = flux[finite_mask]
    flux_err = flux_err[finite_mask]

    baseline = np.nanmax(time) - np.nanmin(time)
    default_period = init_period if init_period is not None else max(baseline / 5.0, 0.5)
    if default_period <= 0:
        default_period = 1.0

    with pm.Model() as model:
        mean_flux = pm.Normal(
            "mean_flux",
            mu=float(np.nanmedian(flux)),
            sigma=float(max(np.nanstd(flux) * 10, 1e-3)),
        )
        log_sigma = pm.Normal(
            "log_sigma",
            mu=float(np.log(np.nanstd(flux) + 1e-6)),
            sigma=5.0,
        )
        log_amp = pm.Normal(
            "log_amp",
            mu=float(np.log(np.nanvar(flux) + 1e-6)),
            sigma=5.0,
        )

        if init_period is None:
            rot_period = pm.Lognormal(
                "rot_period",
                mu=float(np.log(default_period)),
                sigma=1.0,
            )
        else:
            rot_period = pm.Normal(
                "rot_period",
                mu=float(init_period),
                sigma=float(max(0.2 * init_period, 0.1)),
            )

        Q0 = pm.InverseGamma("Q0", alpha=2.0, beta=0.5)
        dQ = pm.HalfNormal("dQ", sigma=5.0)
        mixing = pm.Uniform("mixing", lower=0.01, upper=1.0)

        kernel = xo.gp.terms.RotationTerm(
            log_amp=log_amp,
            period=rot_period,
            Q0=Q0,
            dQ=dQ,
            f=mixing,
        )

        diag = flux_err ** 2 + pm.math.exp(2.0 * log_sigma)
        gp = xo.gp.GP(kernel, time, diag)

        centered_flux = flux - mean_flux
        gp.marginal("gp_obs", observed=centered_flux)

        pm.Deterministic("gp_prediction", mean_flux + gp.predict())

        map_estimate = None
        try:  # pragma: no cover - optional optimisation step
            map_estimate = pm.find_MAP(progressbar=False)
        except Exception:  # pragma: no cover - MAP can fail for complex models
            map_estimate = None

        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=cores,
            target_accept=target_accept,
            start=map_estimate,
            return_inferencedata=True,
            progressbar=False,
        )

    return {
        "model": model,
        "idata": idata,
        "gp": gp,
        "map_estimate": map_estimate,
    }


__all__ = [
    "RotationPeriodResult",
    "estimate_rotation_period",
    "fit_qp_gp",
]
