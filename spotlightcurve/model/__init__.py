"""Probabilistic modeling utilities for SpotLightCurve."""

from __future__ import annotations

from typing import Optional

import numpy as np

from ..backends import get_backend


def build_gp_transit_model(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    period: float,
    t0: float,
    rot_period_prior: Optional[float] = None,
):
    """Construct the PyMC GP+transit model for compatibility."""

    backend = get_backend("pymc")
    return backend.build_model(  # type: ignore[no-any-return]
        np.asarray(time, dtype=float),
        np.asarray(flux, dtype=float),
        np.asarray(flux_err, dtype=float),
        period=float(period),
        t0=float(t0),
        rot_period_prior=rot_period_prior,
    )


__all__ = ["build_gp_transit_model"]

from .compare import compare_models  # noqa: E402
from .gp import RotationPeriodResult, estimate_rotation_period, fit_qp_gp  # noqa: E402
from .spot import SpotModelConfig, fit_transit_spot  # noqa: E402

__all__ += [
    "compare_models",
    "RotationPeriodResult",
    "estimate_rotation_period",
    "fit_qp_gp",
    "SpotModelConfig",
    "fit_transit_spot",
]
