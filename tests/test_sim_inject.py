"""Tests for the injection--recovery simulation utilities."""

from __future__ import annotations

import pytest

np = pytest.importorskip("numpy")

from spotlightcurve.sim.inject import (
    InjectionRecoveryResult,
    QPNoiseConfig,
    TransitInjection,
    draw_qp_noise,
    inject_box_transit,
    recover_box_depth,
    run_injection_recovery,
)


def test_draw_qp_noise_reproducible() -> None:
    time = np.linspace(0, 1, 5)
    config = QPNoiseConfig(amplitude=0.01, timescale=1.0, period=0.5, gamma=0.3, jitter=1e-6)

    rng = np.random.default_rng(123)
    sample_one = draw_qp_noise(time, config, random_state=rng)
    rng = np.random.default_rng(123)
    sample_two = draw_qp_noise(time, config, random_state=rng)

    np.testing.assert_allclose(sample_one, sample_two)


def test_inject_box_transit_basic_shape() -> None:
    time = np.linspace(0, 2, 10)
    injection = TransitInjection(depth=0.02, duration=0.5, period=1.0, t0=0.1)
    flux = inject_box_transit(time, injection)

    assert flux.shape == time.shape
    assert np.isclose(flux.min(), 1.0 - injection.depth)
    assert np.isclose(flux.max(), 1.0)


def test_recover_box_depth_matches_injected_signal() -> None:
    time = np.linspace(0, 2, 200)
    injection = TransitInjection(depth=0.01, duration=0.3, period=1.0, t0=0.0)
    flux = inject_box_transit(time, injection)
    flux_err = np.full_like(flux, 1e-3)

    recovered_depth, snr = recover_box_depth(time, flux, flux_err, injection)

    assert pytest.approx(recovered_depth, rel=1e-2) == injection.depth
    assert snr > 100


def test_run_injection_recovery_returns_results() -> None:
    time = np.linspace(0, 1, 50)
    injections = [
        TransitInjection(depth=0.01, duration=0.2, period=0.5, t0=0.0),
        TransitInjection(depth=0.015, duration=0.25, period=0.7, t0=0.1),
    ]
    qp_config = QPNoiseConfig(amplitude=0.0, timescale=1.0, period=1.0, gamma=0.3, jitter=1e-6)

    results = run_injection_recovery(
        time,
        flux_err=None,
        injections=injections,
        qp_config=qp_config,
        detection_threshold=0.0,
        random_state=np.random.default_rng(5),
    )

    assert len(results) == len(injections)
    assert all(isinstance(res, InjectionRecoveryResult) for res in results)
    assert all(res.detected for res in results)
    for result, injection in zip(results, injections):
        assert pytest.approx(result.recovered_depth, rel=1e-2) == injection.depth
