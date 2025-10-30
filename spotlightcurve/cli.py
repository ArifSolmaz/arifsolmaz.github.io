"""Command-line entry points for SpotLightCurve."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import arviz as az
import numpy as np
import pymc as pm
import typer

from . import __version__
from .io import LightCurve, LightCurveBundle, load_tess
from .model import build_gp_transit_model
from .preprocess import apply_mask, quality_mask

app = typer.Typer(help="SpotLightCurve: analyze stellar activity in transit light curves")


@app.command()
def version() -> None:
    """Print the SpotLightCurve version."""

    typer.echo(__version__)


@app.command()
def download(target: str, sector: Optional[int] = None, output: Path = Path("light_curve.json")):
    """Download a TESS light curve and save it to disk."""

    bundle: LightCurveBundle = load_tess(target, sector=sector)
    lc = bundle.light_curve
    payload = {
        "time": lc.time.tolist(),
        "flux": lc.flux.tolist(),
        "flux_err": lc.flux_err.tolist(),
        "metadata": lc.metadata,
        "mission": lc.mission,
        "quality_mask": bundle.quality_mask.tolist(),
        "combined_mask": bundle.combined_mask.tolist(),
        "quality_preset": bundle.quality_preset,
    }
    output.write_text(json.dumps(payload))
    typer.echo(f"Saved light curve to {output}")


@app.command()
def run(
    light_curve_path: Path = typer.Argument(..., help="Path to a JSON light curve"),
    period: float = typer.Option(..., help="Planet orbital period in days"),
    t0: float = typer.Option(..., help="Transit midpoint [BJD_TDB]"),
    rot_period: Optional[float] = typer.Option(None, help="Stellar rotation period prior"),
    draws: int = typer.Option(2000, help="Posterior samples"),
    tune: int = typer.Option(2000, help="NUTS tuning steps"),
    output: Path = typer.Option(Path("results"), help="Output directory"),
):
    """Run the joint GP+transit model on a saved light curve."""

    output.mkdir(parents=True, exist_ok=True)

    payload = json.loads(light_curve_path.read_text())
    lc = LightCurve(
        time=np.array(payload["time"]),
        flux=np.array(payload["flux"]),
        flux_err=np.array(payload["flux_err"]),
        mission=payload.get("mission", "Custom"),
        metadata=payload.get("metadata", {}),
    )

    mask = quality_mask(lc.flux)
    lc = apply_mask(lc, mask)

    model = build_gp_transit_model(
        lc.time,
        lc.flux,
        lc.flux_err,
        period=period,
        t0=t0,
        rot_period_prior=rot_period,
    )

    with model:
        trace = pm.sample(draws=draws, tune=tune, target_accept=0.9, chains=2)

    az.to_netcdf(trace, output / "trace.nc")
    typer.echo(f"Saved posterior samples to {output / 'trace.nc'}")


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
