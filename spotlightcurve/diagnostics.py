"""Diagnostic utilities for SpotLightCurve."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import arviz as az
import matplotlib.pyplot as plt
import numpy as np


def summary(trace, var_names=None) -> az.data.inference_data.InferenceData:
    """Return an ArviZ summary table."""

    return az.summary(trace, var_names=var_names)


def corner_plot(trace, var_names=None, save: Optional[Path] = None):
    """Create a corner plot using ArviZ's pair plot."""

    grid = az.plot_pair(trace, var_names=var_names, kind="kde", marginals=True)
    if save:
        grid.figure.savefig(save, dpi=200, bbox_inches="tight")
    return grid


def residual_plot(time: np.ndarray, flux: np.ndarray, model_flux: np.ndarray, save: Optional[Path] = None):
    """Plot residuals of the fit."""

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, flux - model_flux, ".k", markersize=2)
    ax.axhline(0, color="C1", lw=1)
    ax.set_xlabel("Time [BJD_TDB]")
    ax.set_ylabel("Residual Flux")
    ax.set_title("SpotLightCurve Residuals")
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=200)
    return fig


__all__ = ["summary", "corner_plot", "residual_plot"]
