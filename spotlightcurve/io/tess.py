"""TESS-specific light-curve download helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Union

import numpy as np

from . import LightCurve

try:  # Optional dependency used for data access
    import lightkurve as lk
except ImportError:  # pragma: no cover - handled by load_tess
    lk = None


if lk is not None:  # pragma: no branch - evaluated at import time
    _QUALITY_PRESETS = {
        "default": lk.TessQualityFlags.DEFAULT_BITMASK,
        "conservative": lk.TessQualityFlags.CONSERVATIVE_BITMASK,
        "lenient": lk.TessQualityFlags.LENIENT_BITMASK,
    }
else:  # lightkurve unavailable during import
    _QUALITY_PRESETS = {}


@dataclass
class LightCurveBundle:
    """Bundle containing raw and cleaned TESS light-curve data."""

    light_curve: LightCurve
    raw_lightcurve: "lk.LightCurve"
    quality_mask: np.ndarray
    combined_mask: np.ndarray
    quality_preset: str
    metadata: Dict[str, object]

    def to_light_curve(self) -> LightCurve:
        """Return the normalized :class:`~spotlightcurve.io.LightCurve`."""

        return self.light_curve


def apply_quality_masks(
    quality: Optional[np.ndarray],
    preset: Union[str, int] = "default",
) -> np.ndarray:
    """Return a boolean mask for the provided QUALITY bits.

    Parameters
    ----------
    quality
        QUALITY bit field from a TESS light curve.
    preset
        Either a named preset (``"default"``, ``"conservative"``, ``"lenient"``,
        or ``"none"``) or an explicit integer bitmask.
    """

    if quality is None:
        return np.array([], dtype=bool)

    quality = np.asarray(quality)

    if isinstance(preset, str):
        key = preset.lower()
        if key == "none":
            return np.ones_like(quality, dtype=bool)
        if lk is None:  # pragma: no cover - requires optional dependency
            raise ImportError(
                "lightkurve is required for TESS quality masking; install it with `pip install lightkurve`."
            )
        if key not in _QUALITY_PRESETS:
            presets = ", ".join(sorted(_QUALITY_PRESETS)) or "none"
            raise ValueError(f"Unknown quality preset '{preset}'. Available presets: {presets}.")
        bitmask = _QUALITY_PRESETS[key]
    else:
        bitmask = int(preset)

    return (quality & bitmask) == 0


def load_tess(
    target: str,
    sector: Optional[int] = None,
    *,
    quality: str = "default",
    author: Optional[str] = None,
    download_kwargs: Optional[Dict[str, object]] = None,
) -> LightCurveBundle:
    """Download and normalize a TESS light curve using Lightkurve.

    The returned :class:`LightCurveBundle` exposes both the cleaned data (as a
    :class:`~spotlightcurve.io.LightCurve`) and the raw
    :class:`lightkurve.lightcurve.LightCurve` with boolean masks documenting the
    applied quality filtering.
    """

    if lk is None:  # pragma: no cover - requires optional dependency
        raise ImportError(
            "lightkurve is required for load_tess; install it with `pip install lightkurve`."
        )

    search = lk.search_lightcurve(target, mission="TESS", sector=sector, author=author)
    if len(search) == 0:
        raise ValueError(f"No TESS light curves found for target '{target}'.")

    download_kwargs = download_kwargs or {}
    raw_lc = search.download_all(**download_kwargs).stitch()

    raw_time = raw_lc.time.value
    raw_flux = raw_lc.flux.value
    raw_flux_err_attr = getattr(raw_lc, "flux_err", None)
    if raw_flux_err_attr is not None:
        raw_flux_err = (
            raw_flux_err_attr.value if hasattr(raw_flux_err_attr, "value") else np.asarray(raw_flux_err_attr)
        )
    else:
        raw_flux_err = np.full_like(raw_flux, np.nanmedian(raw_flux) * 0.001)

    quality_mask = apply_quality_masks(getattr(raw_lc, "quality", None), preset=quality)
    if quality_mask.size == 0:
        quality_mask = np.ones_like(raw_flux, dtype=bool)

    finite_mask = (
        np.isfinite(raw_time)
        & np.isfinite(raw_flux)
        & np.isfinite(raw_flux_err)
    )

    combined_mask = quality_mask & finite_mask
    if not np.any(combined_mask):
        raise ValueError("No cadences remain after applying the requested quality mask.")

    time = raw_time[combined_mask]
    flux = raw_flux[combined_mask]
    flux_err = raw_flux_err[combined_mask]

    median_flux = np.nanmedian(flux)
    if not np.isfinite(median_flux) or median_flux == 0:
        median_flux = 1.0

    normalized_flux = flux / median_flux
    normalized_flux_err = flux_err / median_flux

    metadata: Dict[str, object] = {
        "target": target,
        "sector": sector,
        "author": author,
        "quality_preset": quality,
        "targetid": getattr(raw_lc, "targetid", None),
        "mission": "TESS",
    }

    light_curve = LightCurve(
        time=time,
        flux=normalized_flux,
        flux_err=normalized_flux_err,
        mission="TESS",
        metadata=metadata,
    )

    return LightCurveBundle(
        light_curve=light_curve,
        raw_lightcurve=raw_lc,
        quality_mask=quality_mask,
        combined_mask=combined_mask,
        quality_preset=quality,
        metadata=metadata,
    )


__all__ = ["LightCurveBundle", "apply_quality_masks", "load_tess"]
