"""Tests for TESS I/O helpers."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

from spotlightcurve.io import LightCurve
from spotlightcurve.io import tess


@pytest.fixture
def dummy_lightkurve(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """Provide a minimal Lightkurve stub for quality masking and downloads."""

    class DummyFlags:
        DEFAULT_BITMASK = 0b0011
        CONSERVATIVE_BITMASK = 0b0111
        LENIENT_BITMASK = 0b0001

    dummy = SimpleNamespace(TessQualityFlags=DummyFlags)
    monkeypatch.setattr(tess, "lk", dummy, raising=False)
    monkeypatch.setattr(
        tess,
        "_QUALITY_PRESETS",
        {
            "default": DummyFlags.DEFAULT_BITMASK,
            "conservative": DummyFlags.CONSERVATIVE_BITMASK,
            "lenient": DummyFlags.LENIENT_BITMASK,
        },
        raising=False,
    )
    return dummy


def test_apply_quality_masks_named_presets(dummy_lightkurve: SimpleNamespace) -> None:
    quality = np.array([0, 1, 2, 4], dtype=int)
    mask_default = tess.apply_quality_masks(quality, preset="default")
    mask_lenient = tess.apply_quality_masks(quality, preset="lenient")

    np.testing.assert_array_equal(mask_default, np.array([True, False, False, True]))
    np.testing.assert_array_equal(mask_lenient, np.array([True, False, True, True]))


def test_apply_quality_masks_numeric_and_none(dummy_lightkurve: SimpleNamespace) -> None:
    quality = np.array([0, 8, 12], dtype=int)

    mask_numeric = tess.apply_quality_masks(quality, preset=8)
    np.testing.assert_array_equal(mask_numeric, np.array([True, False, True]))

    mask_none = tess.apply_quality_masks(quality, preset="none")
    np.testing.assert_array_equal(mask_none, np.ones_like(quality, dtype=bool))


def test_apply_quality_masks_invalid_preset(dummy_lightkurve: SimpleNamespace) -> None:
    with pytest.raises(ValueError):
        tess.apply_quality_masks(np.array([0]), preset="unknown")


def test_apply_quality_masks_missing_quality() -> None:
    mask = tess.apply_quality_masks(None, preset="default")
    assert mask.size == 0


def test_load_tess_returns_normalised_bundle(dummy_lightkurve: SimpleNamespace, monkeypatch: pytest.MonkeyPatch) -> None:
    time = np.linspace(0, 4, 5)
    flux = np.array([10.0, 11.0, 9.0, 10.5, 10.0])
    flux_err = np.full_like(flux, 0.5)
    quality = np.array([0, 0, 1, 0, 0])

    class FakeLightCurve:
        def __init__(self) -> None:
            self.time = SimpleNamespace(value=time)
            self.flux = SimpleNamespace(value=flux)
            self.flux_err = SimpleNamespace(value=flux_err)
            self.quality = quality
            self.targetid = 123456

    class FakeSearchResult:
        def __init__(self, light_curve: FakeLightCurve) -> None:
            self._light_curve = light_curve

        def __len__(self) -> int:  # pragma: no cover - exercised implicitly
            return 1

        def download_all(self, **_: object) -> "FakeSearchResult":
            return self

        def stitch(self) -> FakeLightCurve:
            return self._light_curve

    fake_lc = FakeLightCurve()
    dummy_lightkurve.search_lightcurve = lambda *args, **kwargs: FakeSearchResult(fake_lc)

    bundle = tess.load_tess("HAT-P-36", sector=49)

    assert isinstance(bundle.light_curve, LightCurve)
    np.testing.assert_allclose(bundle.light_curve.time, time[quality == 0])
    np.testing.assert_allclose(np.median(bundle.light_curve.flux), 1.0)
    np.testing.assert_array_equal(bundle.quality_mask, np.array([True, True, False, True, True]))
    assert bundle.metadata["target"] == "HAT-P-36"
    assert bundle.metadata["sector"] == 49


def test_load_tess_handles_empty_search(dummy_lightkurve: SimpleNamespace) -> None:
    class EmptySearch:
        def __len__(self) -> int:
            return 0

    dummy_lightkurve.search_lightcurve = lambda *args, **kwargs: EmptySearch()

    with pytest.raises(ValueError, match="No TESS light curves"):
        tess.load_tess("Nonexistent")
