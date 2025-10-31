"""Model comparison utilities leveraging ArviZ information criteria."""

from __future__ import annotations

from typing import Mapping, Optional

try:
    import arviz as az
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "SpotLightCurve's model comparison helpers require arviz. Install it via `pip install arviz`."
    ) from exc

import pandas as pd

InferenceData = az.InferenceData


def compare_models(
    idata_map: Mapping[str, InferenceData],
    *,
    ic: str = "loo",
    scale: str = "deviance",
    method: str = "BB-pseudo-BMA",
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """Compare multiple fitted models using WAIC or LOO.

    Parameters
    ----------
    idata_map
        Mapping of model labels to :class:`arviz.InferenceData` results. At least two
        entries are required.
    ic
        Information criterion to use for comparison. Supported values are ``"loo"``
        and ``"waic"``. The default is ``"loo"``.
    scale
        Scale of the information criterion; forwarded to :func:`arviz.compare`.
    method
        Model weight combination method used by :func:`arviz.compare`. The default
        ``"BB-pseudo-BMA"`` is numerically stable for most photometric applications.
    seed
        Optional random seed for the weight resampling procedure used by some
        methods.

    Returns
    -------
    pandas.DataFrame
        A DataFrame summarising relative model fit according to the requested
        information criterion.

    Raises
    ------
    ValueError
        If fewer than two models are supplied or if an unsupported information
        criterion is requested.
    RuntimeError
        If ArviZ reports a failure to compute the requested criterion, usually
        because the inference data are missing a ``log_likelihood`` group.
    """

    if len(idata_map) < 2:
        raise ValueError("At least two models are required for comparison.")

    ic_normalised = ic.lower()
    if ic_normalised not in {"loo", "waic"}:
        raise ValueError("ic must be either 'loo' or 'waic'.")

    try:
        return az.compare(
            idata_map,
            ic=ic_normalised,
            scale=scale,
            method=method,
            seed=seed,
        )
    except (TypeError, ValueError) as err:  # pragma: no cover - surface informative error
        missing_ll = [name for name, idata in idata_map.items() if "log_likelihood" not in idata]
        if missing_ll:
            raise RuntimeError(
                "Model comparison requires the log_likelihood group in each InferenceData. "
                f"Missing for: {', '.join(missing_ll)}"
            ) from err
        raise
