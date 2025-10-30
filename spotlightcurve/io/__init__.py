"""Data access utilities for SpotLightCurve."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np

try:  # Optional import used by load_kepler
    import lightkurve as lk
except ImportError:  # pragma: no cover - optional dependency
    lk = None


@dataclass
class LightCurve:
    """Container for a single light-curve segment."""

    time: np.ndarray
    flux: np.ndarray
    flux_err: np.ndarray
    mission: str
    metadata: Dict[str, object]


def load_kepler(target: str, quarter: Optional[int] = None) -> LightCurve:
    """Download and normalize a Kepler/K2 light curve."""

    if lk is None:  # pragma: no cover - guarded by optional dependency
        raise ImportError(
            "lightkurve is required for load_kepler; install it with `pip install lightkurve`."
        )

    search = lk.search_lightcurve(target, mission="Kepler", quarter=quarter)
    lc = search.download_all().stitch().remove_nans().normalize()

    return LightCurve(
        time=lc.time.value,
        flux=lc.flux.value,
        flux_err=getattr(lc, "flux_err", np.full_like(lc.flux.value, np.nan)),
        mission="Kepler",
        metadata={"quarter": quarter},
    )


def from_arrays(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: Optional[np.ndarray] = None,
    mission: str = "Custom",
    metadata: Optional[Dict[str, object]] = None,
) -> LightCurve:
    """Create a :class:`LightCurve` from numpy arrays."""

    if flux_err is None:
        flux_err = np.full_like(flux, np.nanmedian(flux) * 0.001)

    return LightCurve(
        time=np.asarray(time),
        flux=np.asarray(flux),
        flux_err=np.asarray(flux_err),
        mission=mission,
        metadata=metadata or {},
    )


from .tess import LightCurveBundle, apply_quality_masks, load_tess

__all__ = [
    "LightCurve",
    "LightCurveBundle",
    "load_tess",
    "load_kepler",
    "apply_quality_masks",
    "from_arrays",
]
