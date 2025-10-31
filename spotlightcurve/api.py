"""High-level programmatic API for running SpotLightCurve analyses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import arviz as az
import numpy as np

from .backends import BackendName, get_backend


@dataclass
class AnalysisResult:
    """Container for end-to-end analysis outputs."""

    backend: str
    inference: az.InferenceData
    predictive_mean: np.ndarray
    metadata: Dict[str, Any]


def run_analysis(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    *,
    period: float,
    t0: float,
    backend: BackendName | str = "pymc",
    rot_period_prior: Optional[float] = None,
    sample_kwargs: Optional[Mapping[str, Any]] = None,
) -> AnalysisResult:
    """Execute the configured backend and return analysis artefacts."""

    backend_mod = get_backend(backend)
    kwargs = {
        "time": np.asarray(time, dtype=float),
        "flux": np.asarray(flux, dtype=float),
        "flux_err": np.asarray(flux_err, dtype=float),
        "period": float(period),
        "t0": float(t0),
        "rot_period_prior": rot_period_prior,
    }
    if sample_kwargs:
        kwargs.update(sample_kwargs)

    result = backend_mod.run(**kwargs)  # type: ignore[arg-type]

    metadata = {
        "backend": str(backend).lower(),
        "period": float(period),
        "t0": float(t0),
        "rot_period_prior": None if rot_period_prior is None else float(rot_period_prior),
        "sample_kwargs": dict(sample_kwargs or {}),
    }

    return AnalysisResult(
        backend=str(backend).lower(),
        inference=result.inference,
        predictive_mean=np.asarray(result.predictive_mean),
        metadata=metadata,
    )


__all__ = ["AnalysisResult", "run_analysis"]
