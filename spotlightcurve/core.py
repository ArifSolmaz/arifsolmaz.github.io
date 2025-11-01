from __future__ import annotations
import numpy as np

def simulate_spot_curve(t, period: float = 3.0, amplitude: float = 0.01, noise: float = 5e-4, seed: int | None = 42):
    """Simulate a simple spot-modulated light curve.

    Parameters
    ----------
    t : array-like
        Time array (days).
    period : float
        Rotation period (days).
    amplitude : float
        Semi-amplitude of modulation (relative flux).
    noise : float
        White noise sigma (relative flux).
    seed : int or None
        Random seed for noise.

    Returns
    -------
    flux : ndarray
        Simulated relative flux.
    """
    t = np.asarray(t, dtype=float)
    phase = 2 * np.pi * (t / period)
    clean = 1.0 - amplitude * np.cos(phase)  # one-spot cosine toy model
    rng = np.random.default_rng(seed)
    return clean + rng.normal(0.0, noise, size=t.size)

def phase_fold(t, y, period: float, t0: float = 0.0):
    """Phase-fold times and values by a period.

    Returns
    -------
    phase : ndarray in [-0.5, 0.5)
    y_sorted : ndarray sorted by phase
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    phase = ((t - t0) / period) % 1.0
    phase[phase >= 0.5] -= 1.0
    order = np.argsort(phase)
    return phase[order], y[order]
