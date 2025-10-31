"""Simulation utilities for SpotLightCurve."""

from .inject import (
    QPNoiseConfig,
    TransitInjection,
    InjectionRecoveryResult,
    draw_qp_noise,
    inject_box_transit,
    recover_box_depth,
    run_injection_recovery,
)

__all__ = [
    "QPNoiseConfig",
    "TransitInjection",
    "InjectionRecoveryResult",
    "draw_qp_noise",
    "inject_box_transit",
    "recover_box_depth",
    "run_injection_recovery",
]
