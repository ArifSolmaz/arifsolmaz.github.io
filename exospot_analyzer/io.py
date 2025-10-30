"""Data access utilities for SpotLightCurve."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np

try:  # Optional imports for specific missions
    import lightkurve as lk
except ImportError:  # pragma: no cover
    lk = None

try:
    import eleanor
except ImportError:  # pragma: no cover
    eleanor = None


@dataclass
class LightCurve:
    """Container for a single light-curve segment."""

    time: np.ndarray
    flux: np.ndarray
    flux_err: np.ndarray
    mission: str
    metadata: dict


def load_tess(target: str, sector: Optional[int] = None) -> LightCurve:
    """Download and normalize a TESS light curve using Lightkurve.

    Parameters
    ----------
    target: str
        TIC identifier or common star name.
    sector: int, optional
        Specific TESS sector to download. If omitted, all available sectors are
        stitched together.
    """

    if lk is None:
        raise ImportError(
            "lightkurve is required for load_tess; install it with `pip install lightkurve`."
        )

    search = lk.search_lightcurve(target, mission="TESS", sector=sector)
    lc = search.download_all().stitch().remove_nans().normalize()

    return LightCurve(
        time=lc.time.value,
        flux=lc.flux.value,
        flux_err=lc.flux_err.value,
        mission="TESS",
        metadata={"sector": sector, "targetid": getattr(lc, "targetid", None)},
    )


def load_kepler(target: str, quarter: Optional[int] = None) -> LightCurve:
    """Download and normalize a Kepler/K2 light curve."""

    if lk is None:
        raise ImportError(
            "lightkurve is required for load_kepler; install it with `pip install lightkurve`."
        )

    search = lk.search_lightcurve(target, mission="Kepler", quarter=quarter)
    lc = search.download_all().stitch().remove_nans().normalize()

    return LightCurve(
        time=lc.time.value,
        flux=lc.flux.value,
        flux_err=lc.flux_err.value,
        mission="Kepler",
        metadata={"quarter": quarter},
    )


def from_arrays(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: Optional[np.ndarray] = None,
    mission: str = "Custom",
    metadata: Optional[dict] = None,
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


__all__ = ["LightCurve", "load_tess", "load_kepler", "from_arrays"]
