"""Tests for the ArviZ-based model comparison utilities."""

from __future__ import annotations

import pytest

np = pytest.importorskip("numpy")
pd = pytest.importorskip("pandas")

import arviz as az

from spotlightcurve.model.compare import compare_models


def _fake_idata(seed: int) -> az.InferenceData:
    rng = np.random.default_rng(seed)
    posterior = {"theta": rng.normal(size=(2, 5))}
    log_likelihood = {"flux": rng.normal(size=(2, 5))}
    return az.from_dict(posterior=posterior, log_likelihood=log_likelihood)


def test_compare_models_returns_dataframe() -> None:
    idata_a = _fake_idata(0)
    idata_b = _fake_idata(1)

    result = compare_models({"model_a": idata_a, "model_b": idata_b}, ic="waic")

    assert isinstance(result, pd.DataFrame)
    assert {"model_a", "model_b"}.issubset(result.index)


def test_compare_models_requires_valid_ic() -> None:
    idata = _fake_idata(42)
    with pytest.raises(ValueError):
        compare_models({"only": idata, "other": idata}, ic="bic")


def test_compare_models_missing_log_likelihood_raises_runtime_error() -> None:
    idata = az.from_dict(posterior={"theta": np.zeros((2, 5))})
    with pytest.raises(RuntimeError):
        compare_models({"bad": idata, "other": _fake_idata(2)})
