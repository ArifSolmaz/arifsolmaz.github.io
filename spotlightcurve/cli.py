"""Command-line entry points for SpotLightCurve."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, Optional

import arviz as az
import numpy as np
import typer
import yaml

from . import __version__
from .api import run_analysis
from .diagnostics import corner_plot, residual_plot, summary as summary_table
from .io import LightCurve, LightCurveBundle, load_tess
from .preprocess import apply_mask, quality_mask
from .report.html import ReportContext, render_report

app = typer.Typer(help="SpotLightCurve: analyze stellar activity in transit light curves")


def _load_light_curve_from_payload(payload: Dict[str, Any]) -> LightCurve:
    return LightCurve(
        time=np.asarray(payload["time"]),
        flux=np.asarray(payload["flux"]),
        flux_err=np.asarray(payload["flux_err"]),
        mission=payload.get("mission", "Custom"),
        metadata=payload.get("metadata", {}),
    )


def _load_light_curve_from_config(
    data_cfg: Dict[str, Any],
    config_dir: Path,
) -> tuple[LightCurve, Dict[str, Any]]:
    bundle_metadata: Dict[str, Any] = {}
    if "light_curve_path" in data_cfg:
        lc_path = Path(data_cfg["light_curve_path"])
        if not lc_path.is_absolute():
            lc_path = (config_dir / lc_path).resolve()
        if not lc_path.exists():
            raise typer.BadParameter(f"Light-curve file '{lc_path}' does not exist.")
        payload = json.loads(lc_path.read_text())
        lc = _load_light_curve_from_payload(payload)
        if "quality_mask" in payload:
            mask = np.asarray(payload["quality_mask"], dtype=bool)
            if mask.size == lc.time.size:
                lc = apply_mask(lc, mask)
        elif data_cfg.get("apply_quality_mask", True):
            lc = apply_mask(lc, quality_mask(lc.flux))
        return lc, bundle_metadata

    source = data_cfg.get("source", "tess").lower()
    if source != "tess":
        raise typer.BadParameter("Only 'tess' source is currently supported.")

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
    bundle_metadata = {
        "quality_mask": bundle.quality_mask.tolist(),
        "combined_mask": bundle.combined_mask.tolist(),
        "quality_preset": bundle.quality_preset,
        **bundle.metadata,
    }
    return bundle.light_curve, bundle_metadata


def _prepare_light_curve(lc: LightCurve, preprocess_cfg: Dict[str, Any]) -> LightCurve:
    sigma_clip = preprocess_cfg.get("sigma_clip")
    if sigma_clip:
        mask = quality_mask(lc.flux, sigma=sigma_clip)
        lc = apply_mask(lc, mask)
    return lc


def _build_sample_kwargs(model_cfg: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "draws": int(model_cfg.get("draws", 2000)),
        "tune": int(model_cfg.get("tune", 2000)),
        "chains": int(model_cfg.get("chains", 2)),
        "target_accept": float(model_cfg.get("target_accept", 0.9)),
        "random_seed": model_cfg.get("random_seed"),
        "progressbar": bool(model_cfg.get("progressbar", True)),
    }


def _export_results(
    *,
    inference: az.InferenceData,
    predictive_mean: np.ndarray,
    lc: LightCurve,
    results_dir: Path,
    run_name: str,
    backend: str,
    model_cfg: Dict[str, Any],
    sample_kwargs: Dict[str, Any],
    preprocess_cfg: Dict[str, Any],
    data_cfg: Dict[str, Any],
    metadata: Dict[str, Any],
) -> None:
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    trace_path = results_dir / "trace.nc"
    az.to_netcdf(inference, trace_path)

    summary_df = summary_table(inference)
    summary_path = results_dir / "summary.csv"
    summary_df.to_csv(summary_path)

    corner_vars = model_cfg.get("corner_vars")
    corner_plot(inference, var_names=corner_vars, save=figures_dir / "corner.png")
    residual_plot(lc.time, lc.flux, predictive_mean, save=figures_dir / "residuals.png")

    timestamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    resolved_config = {
        "run_name": run_name,
        "backend": backend,
        "data": data_cfg,
        "preprocess": preprocess_cfg,
        "model": {**model_cfg, "sample_kwargs": sample_kwargs},
        "metadata": {
            "results_dir": str(results_dir.resolve()),
            "generated_at_utc": timestamp,
            **metadata,
        },
    }

    config_out = results_dir / "config.yaml"
    config_out.write_text(yaml.safe_dump(resolved_config, sort_keys=False))

    parameters = {
        param: f"{row['mean']:.6f} ± {row['sd']:.6f}"
        for param, row in summary_df.iterrows()
        if np.isfinite(row["mean"]) and np.isfinite(row["sd"])
    }

    report_context = ReportContext(
        parameters=parameters,
        figures={
            "Corner Plot": str(Path("figures") / "corner.png"),
            "Residuals": str(Path("figures") / "residuals.png"),
        },
        metadata={
            "run_name": run_name,
            "backend": backend,
            "mission": lc.mission,
            **metadata,
        },
    )
    render_report(report_context, results_dir / "report.html")

    typer.echo(f"Trace saved to {trace_path}")
    typer.echo(f"Summary saved to {summary_path}")
    typer.echo(f"Figures written to {figures_dir}")
    typer.echo(f"Configuration snapshot saved to {config_out}")
    typer.echo(f"HTML report saved to {results_dir / 'report.html'}")


def _determine_results_dir(
    *,
    results_root: Path,
    requested_name: Optional[str],
    overwrite: bool,
) -> tuple[Path, str]:
    timestamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_name = requested_name or f"run_{timestamp}"
    results_dir = results_root / run_name
    if results_dir.exists() and not overwrite:
        raise typer.BadParameter(
            f"Results directory '{results_dir}' already exists. Use --overwrite to replace it."
        )
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir, run_name


def _execute_analysis(
    config_dict: Dict[str, Any],
    *,
    backend: str,
    results_root: Path,
    overwrite: bool,
    config_dir: Path,
) -> Path:
    data_cfg: Dict[str, Any] = config_dict.get("data", {})
    preprocess_cfg: Dict[str, Any] = config_dict.get("preprocess", {})
    model_cfg: Dict[str, Any] = config_dict.get("model", {})

    try:
        period = float(model_cfg["period"])
        t0 = float(model_cfg["t0"])
    except KeyError as exc:
        raise typer.BadParameter("Model configuration requires 'period' and 't0'.") from exc

    rot_period = model_cfg.get("rot_period_prior")

    sample_kwargs = _build_sample_kwargs(model_cfg)
    lc, bundle_metadata = _load_light_curve_from_config(data_cfg, config_dir)
    lc = _prepare_light_curve(lc, preprocess_cfg)

    results_dir, run_name = _determine_results_dir(
        results_root=results_root,
        requested_name=config_dict.get("run_name") or config_dict.get("name"),
        overwrite=overwrite,
    )

    analysis = run_analysis(
        lc.time,
        lc.flux,
        lc.flux_err,
        period=period,
        t0=t0,
        backend=backend,
        rot_period_prior=rot_period,
        sample_kwargs=sample_kwargs,
    )

    metadata = {
        "bundle": bundle_metadata,
        **analysis.metadata,
    }

    _export_results(
        inference=analysis.inference,
        predictive_mean=analysis.predictive_mean,
        lc=lc,
        results_dir=results_dir,
        run_name=run_name,
        backend=analysis.backend,
        model_cfg=model_cfg,
        sample_kwargs=sample_kwargs,
        preprocess_cfg=preprocess_cfg,
        data_cfg=data_cfg,
        metadata=metadata,
    )

    return results_dir


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
    backend: str = typer.Option("pymc", help="Model backend to use"),
    rot_period: Optional[float] = typer.Option(None, help="Stellar rotation period prior"),
    draws: int = typer.Option(2000, help="Posterior samples"),
    tune: int = typer.Option(2000, help="Warmup steps"),
    chains: int = typer.Option(2, help="Number of chains"),
    target_accept: float = typer.Option(0.9, help="Target acceptance for NUTS"),
    results_root: Path = typer.Option(Path("results"), help="Output directory root"),
    overwrite: bool = typer.Option(False, help="Allow overwriting results"),
) -> None:
    """Run the joint model on a saved light curve."""

    payload = json.loads(light_curve_path.read_text())

    config_dict = {
        "run_name": payload.get("metadata", {}).get("target"),
        "data": {"light_curve_path": str(light_curve_path)},
        "preprocess": {},
        "model": {
            "period": period,
            "t0": t0,
            "rot_period_prior": rot_period,
            "draws": draws,
            "tune": tune,
            "chains": chains,
            "target_accept": target_accept,
        },
    }

    _execute_analysis(
        config_dict,
        backend=backend,
        results_root=results_root,
        overwrite=overwrite,
        config_dir=light_curve_path.parent,
    )


@app.command()
def analyze(
    config: Optional[Path] = typer.Argument(
        None,
        help="Optional YAML configuration describing the run",
    ),
    backend: str = typer.Option("pymc", help="Model backend to use"),
    results_root: Path = typer.Option(Path("results"), help="Base directory for outputs"),
    overwrite: bool = typer.Option(False, help="Allow overwriting existing results"),
) -> None:
    """Execute an end-to-end analysis from a YAML config or CLI options."""

    if config:
        if not config.exists():
            raise typer.BadParameter(f"Configuration file '{config}' does not exist.")
        raw_config = yaml.safe_load(config.read_text()) or {}
        _execute_analysis(
            raw_config,
            backend=backend,
            results_root=results_root,
            overwrite=overwrite,
            config_dir=config.parent,
        )
        return

    raise typer.BadParameter(
        "Analyze requires a configuration file when invoked without additional CLI options."
    )


@app.command()
def pipeline(*args: Any, **kwargs: Any) -> None:
    """Deprecated wrapper around :func:`analyze`."""

    typer.echo("`spotlightcurve pipeline` is deprecated; use `spotlightcurve analyze` instead.")
    analyze(*args, **kwargs)


def main():  # pragma: no cover
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
