"""Pre-processing utilities for SpotLightCurve."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import numpy as np
from scipy import stats

try:
    from lightkurve.correctors import PLDCorrector
except ImportError:  # pragma: no cover
    PLDCorrector = None


@dataclass
class PreprocessConfig:
    sigma_clip: float = 5.0
    window_length: Optional[int] = None


def quality_mask(flux: np.ndarray, sigma: float = 5.0) -> np.ndarray:
    """Return a boolean mask selecting inliers via sigma clipping."""

    z_scores = np.abs(stats.zscore(flux, nan_policy="omit"))
    mask = np.isfinite(z_scores) & (z_scores < sigma)
    return mask


def apply_mask(light_curve, mask: np.ndarray):
    """Apply a boolean mask to a :class:`~exospot_analyzer.io.LightCurve`."""

    from .io import LightCurve  # local import to avoid cycle

    if not isinstance(light_curve, LightCurve):
        raise TypeError("light_curve must be a LightCurve instance")

    return LightCurve(
        time=light_curve.time[mask],
        flux=light_curve.flux[mask],
        flux_err=light_curve.flux_err[mask],
        mission=light_curve.mission,
        metadata=light_curve.metadata,
    )


def correct_with_pld(light_curve, design_matrix) -> np.ndarray:
    """Apply pixel-level decorrelation if Lightkurve is available."""

    if PLDCorrector is None:
        raise ImportError(
            "PLDCorrector requires lightkurve; install it with `pip install lightkurve`."
        )

    corr = PLDCorrector(time=light_curve.time, flux=light_curve.flux, design_matrix_collection=design_matrix)
    return corr.correct()


__all__ = ["PreprocessConfig", "quality_mask", "apply_mask", "correct_with_pld"]
