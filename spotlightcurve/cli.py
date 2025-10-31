"""Command-line entry points for SpotLightCurve."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, Optional

import arviz as az
import numpy as np
import pymc as pm
import typer
import yaml

from . import __version__
from .diagnostics import corner_plot, residual_plot, summary as summary_table
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


@app.command()
def pipeline(
    config: Path = typer.Argument(..., help="YAML configuration describing the run"),
    results_root: Path = typer.Option(Path("results"), help="Base directory for pipeline outputs"),
    overwrite: bool = typer.Option(False, help="Allow overwriting an existing results directory"),
) -> None:
    """Execute an end-to-end analysis as configured in a YAML file."""

    if not config.exists():
        raise typer.BadParameter(f"Configuration file '{config}' does not exist.")

    raw_config = yaml.safe_load(config.read_text()) or {}

    run_name = raw_config.get("run_name") or raw_config.get("name")
    timestamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    if run_name:
        results_dir = results_root / run_name
    else:
        results_dir = results_root / f"run_{timestamp}"

    if results_dir.exists() and not overwrite:
        raise typer.BadParameter(
            f"Results directory '{results_dir}' already exists. Use --overwrite to replace it."
        )

    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    config_dir = config.parent
    data_cfg: Dict[str, Any] = raw_config.get("data", {})

    lc: LightCurve
    bundle_metadata: Dict[str, Any] = {}

    if "light_curve_path" in data_cfg:
        lc_path = Path(data_cfg["light_curve_path"])
        if not lc_path.is_absolute():
            lc_path = (config_dir / lc_path).resolve()
        if not lc_path.exists():
            raise typer.BadParameter(f"Light-curve file '{lc_path}' does not exist.")

        payload = json.loads(lc_path.read_text())
        lc = LightCurve(
            time=np.asarray(payload["time"]),
            flux=np.asarray(payload["flux"]),
            flux_err=np.asarray(payload["flux_err"]),
            mission=payload.get("mission", "Custom"),
            metadata=payload.get("metadata", {}),
        )
    else:
        source = data_cfg.get("source", "tess").lower()
        if source != "tess":
            raise typer.BadParameter("Only 'tess' source is currently supported for pipeline downloads.")

        target = data_cfg.get("target")
        if not target:
            raise typer.BadParameter("TESS configuration requires a 'target' field.")

        sector = data_cfg.get("sector")
        quality = data_cfg.get("quality", "default")
        author = data_cfg.get("author")
        download_kwargs = data_cfg.get("download_kwargs")

        bundle: LightCurveBundle = load_tess(
            target,
            sector=sector,
            quality=quality,
            author=author,
            download_kwargs=download_kwargs,
        )
        lc = bundle.light_curve
        bundle_metadata = {
            "quality_mask": bundle.quality_mask.tolist(),
            "combined_mask": bundle.combined_mask.tolist(),
            "quality_preset": bundle.quality_preset,
            **bundle.metadata,
        }

    preprocess_cfg: Dict[str, Any] = raw_config.get("preprocess", {})
    sigma_clip = preprocess_cfg.get("sigma_clip")
    if sigma_clip:
        mask = quality_mask(lc.flux, sigma=sigma_clip)
        lc = apply_mask(lc, mask)

    model_cfg: Dict[str, Any] = raw_config.get("model", {})
    try:
        period = float(model_cfg["period"])
        t0 = float(model_cfg["t0"])
    except KeyError as exc:
        raise typer.BadParameter("Model configuration requires 'period' and 't0'.") from exc

    rot_period = model_cfg.get("rot_period_prior")
    sample_kwargs = {
        "draws": int(model_cfg.get("draws", 2000)),
        "tune": int(model_cfg.get("tune", 2000)),
        "chains": int(model_cfg.get("chains", 2)),
        "target_accept": float(model_cfg.get("target_accept", 0.9)),
    }

    model = build_gp_transit_model(
        lc.time,
        lc.flux,
        lc.flux_err,
        period=period,
        t0=t0,
        rot_period_prior=rot_period,
    )

    with model:
        trace = pm.sample(**sample_kwargs)
        posterior_predictive = pm.sample_posterior_predictive(
            trace, var_names=["obs"], extend_inferencedata=True
        )

    if isinstance(posterior_predictive, az.InferenceData):
        trace = posterior_predictive
        obs_pred = trace.posterior_predictive["obs"].mean(dim=("chain", "draw")).values
    else:
        obs_pred = np.asarray(posterior_predictive["obs"]).mean(axis=0)

    az.to_netcdf(trace, results_dir / "trace.nc")

    summary_df = summary_table(trace)
    summary_path = results_dir / "summary.csv"
    summary_df.to_csv(summary_path)

    corner_vars = model_cfg.get("corner_vars")
    corner_plot(trace, var_names=corner_vars, save=figures_dir / "corner.png")
    residual_plot(lc.time, lc.flux, obs_pred, save=figures_dir / "residuals.png")

    resolved_config = {
        "run_name": run_name or f"run_{timestamp}",
        "data": data_cfg,
        "preprocess": preprocess_cfg,
        "model": {**model_cfg, "sample_kwargs": sample_kwargs},
        "metadata": {
            "results_dir": str(results_dir.resolve()),
            "generated_at_utc": timestamp,
            "bundle": bundle_metadata,
        },
    }

    config_out = results_dir / "config.yaml"
    config_out.write_text(yaml.safe_dump(resolved_config, sort_keys=False))

    typer.echo(f"Trace saved to {results_dir / 'trace.nc'}")
    typer.echo(f"Summary saved to {summary_path}")
    typer.echo(f"Figures written to {figures_dir}")
    typer.echo(f"Configuration snapshot saved to {config_out}")


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
