"""Injection--recovery experiments with quasi-periodic noise."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

import numpy as np


@dataclass
class QPNoiseConfig:
    """Configuration for the quasi-periodic covariance model.

    Parameters
    ----------
    amplitude
        Standard deviation of the correlated component in relative flux units.
    timescale
        Exponential decay timescale (in days) controlling spot evolution.
    period
        Recurrence period (in days) representing the stellar rotation period.
    gamma
        Controls the smoothness of the periodic term. Larger values give more
        harmonic content.
    jitter
        Additional white-noise term (in relative flux units) added on the
        diagonal for numerical stability.
    """

    amplitude: float
    timescale: float
    period: float
    gamma: float
    jitter: float = 0.0


@dataclass
class TransitInjection:
    """Simple box-shaped transit configuration."""

    depth: float
    duration: float
    period: float
    t0: float


@dataclass
class InjectionRecoveryResult:
    """Result summary from an injection--recovery trial."""

    injection: TransitInjection
    recovered_depth: float
    snr: float
    detected: bool
    flux: np.ndarray
    noise: np.ndarray


def _validate_time_array(time: np.ndarray) -> np.ndarray:
    time = np.asarray(time, dtype=float)
    if time.ndim != 1 or time.size == 0:
        raise ValueError("time must be a one-dimensional array with at least one sample")
    if not np.all(np.isfinite(time)):
        raise ValueError("time contains non-finite values")
    return time


def draw_qp_noise(
    time: np.ndarray,
    config: QPNoiseConfig,
    *,
    random_state: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Draw a realization from a quasi-periodic Gaussian Process.

    The kernel has the form

    .. math::

        k_{ij} = A^2 \exp\left(-\frac{(t_i - t_j)^2}{2\tau^2} -
        \frac{\sin^2\left(\pi (t_i - t_j)/P\right)}{2\Gamma^2}\right)

    where ``A`` is :pyattr:`QPNoiseConfig.amplitude`, ``tau`` is the decay
    timescale, ``P`` is the period, and ``Gamma`` sets the periodic coherence.

    Parameters
    ----------
    time
        One-dimensional array of observation times (days).
    config
        Quasi-periodic covariance configuration.
    random_state
        Optional random number generator for reproducibility.
    """

    time = _validate_time_array(time)
    if random_state is None:
        random_state = np.random.default_rng()

    dt = time[:, None] - time[None, :]
    exp_term = np.exp(-0.5 * (dt / max(config.timescale, 1e-6)) ** 2)
    periodic_term = np.exp(
        -np.sin(np.pi * dt / max(config.period, 1e-6)) ** 2
        / (2.0 * max(config.gamma, 1e-6) ** 2)
    )

    cov = (config.amplitude ** 2) * exp_term * periodic_term
    if config.jitter > 0:
        cov = cov + np.eye(time.size) * (config.jitter ** 2)
    else:
        cov = cov + np.eye(time.size) * 1e-12

    try:
        noise = random_state.multivariate_normal(np.zeros(time.size), cov)
    except np.linalg.LinAlgError as exc:  # pragma: no cover - numerical edge case
        # Add an adaptive jitter term and retry
        jitter = max(config.jitter, 1e-6)
        cov = cov + np.eye(time.size) * jitter
        noise = random_state.multivariate_normal(np.zeros(time.size), cov)
    return noise


def inject_box_transit(time: np.ndarray, injection: TransitInjection) -> np.ndarray:
    """Construct a box-shaped transit light curve."""

    time = _validate_time_array(time)
    depth = float(injection.depth)
    if depth <= 0:
        raise ValueError("Transit depth must be positive")
    if injection.duration <= 0 or injection.period <= 0:
        raise ValueError("Transit duration and period must be positive")

    phase = ((time - injection.t0 + 0.5 * injection.period) % injection.period) - (
        0.5 * injection.period
    )
    in_transit = np.abs(phase) <= 0.5 * injection.duration

    flux = np.ones_like(time)
    flux[in_transit] -= depth
    return flux


def recover_box_depth(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: Optional[np.ndarray],
    injection: TransitInjection,
) -> tuple[float, float]:
    """Estimate transit depth and signal-to-noise using weighted means."""

    time = _validate_time_array(time)
    flux = np.asarray(flux, dtype=float)
    if flux.shape != time.shape:
        raise ValueError("flux must match the shape of time")

    if flux_err is None:
        flux_err = np.full_like(flux, np.nanstd(flux))
    else:
        flux_err = np.asarray(flux_err, dtype=float)
        if flux_err.shape != time.shape:
            raise ValueError("flux_err must match the shape of time")

    weights = np.where(np.isfinite(flux_err) & (flux_err > 0), 1.0 / flux_err**2, 0.0)
    if not np.any(weights):
        raise ValueError("flux_err must contain at least one finite, positive entry")

    phase = ((time - injection.t0 + 0.5 * injection.period) % injection.period) - (
        0.5 * injection.period
    )
    in_transit = np.abs(phase) <= 0.5 * injection.duration
    oot = ~in_transit

    if not np.any(in_transit):
        raise ValueError("No samples fall within the transit window for recovery")
    if not np.any(oot):
        raise ValueError("No out-of-transit samples available for baseline estimation")

    wt_in = weights[in_transit]
    wt_oot = weights[oot]

    mean_oot = np.average(flux[oot], weights=wt_oot)
    mean_in = np.average(flux[in_transit], weights=wt_in)
    recovered_depth = mean_oot - mean_in

    var_in = 1.0 / wt_in.sum()
    var_oot = 1.0 / wt_oot.sum()
    snr = recovered_depth / np.sqrt(var_in + var_oot)
    return recovered_depth, snr


def run_injection_recovery(
    time: np.ndarray,
    flux_err: Optional[np.ndarray],
    injections: Iterable[TransitInjection],
    qp_config: QPNoiseConfig,
    *,
    detection_threshold: float = 7.0,
    random_state: Optional[np.random.Generator] = None,
) -> List[InjectionRecoveryResult]:
    """Execute injection--recovery trials with quasi-periodic noise.

    Parameters
    ----------
    time
        Observation times in days.
    flux_err
        Per-point uncertainties used for recovery weighting. If ``None`` a
        constant scatter estimated from the simulated flux is adopted.
    injections
        Iterable of :class:`TransitInjection` objects describing each trial.
    qp_config
        Configuration of the quasi-periodic noise process.
    detection_threshold
        Minimum signal-to-noise ratio required for a detection.
    random_state
        Optional generator for reproducibility.
    """

    time = _validate_time_array(time)
    if random_state is None:
        random_state = np.random.default_rng()

    results: List[InjectionRecoveryResult] = []
    for inj in injections:
        noise = draw_qp_noise(time, qp_config, random_state=random_state)
        signal = inject_box_transit(time, inj)
        flux = signal + noise

        if flux_err is None:
            err = np.full_like(flux, np.nanstd(flux))
        else:
            err = np.asarray(flux_err, dtype=float)
            if err.shape != time.shape:
                raise ValueError("flux_err must match time")

        recovered_depth, snr = recover_box_depth(time, flux, err, inj)
        detected = bool(snr >= detection_threshold)
        results.append(
            InjectionRecoveryResult(
                injection=inj,
                recovered_depth=recovered_depth,
                snr=snr,
                detected=detected,
                flux=flux,
                noise=noise,
            )
        )

    return results


__all__ = [
    "QPNoiseConfig",
    "TransitInjection",
    "InjectionRecoveryResult",
    "draw_qp_noise",
    "inject_box_transit",
    "recover_box_depth",
    "run_injection_recovery",
]
