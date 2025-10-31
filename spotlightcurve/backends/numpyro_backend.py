"""NumPyro backend using tinygp for quasi-periodic stellar variability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import arviz as az
import numpy as np

try:  # pragma: no cover - optional dependency import guard
    import jax
    import jax.numpy as jnp
    import numpyro
    import numpyro.distributions as dist
    from numpyro.infer import MCMC, NUTS, Predictive
    from tinygp import GaussianProcess, kernels
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "The NumPyro backend requires `jax`, `numpyro`, and `tinygp`. Install the 'numpyro' "
        "extra via `pip install spotlightcurve[numpyro]`."
    ) from exc


@dataclass
class BackendResult:
    """Outputs from the NumPyro backend run."""

    inference: az.InferenceData
    predictive_mean: np.ndarray


def _quasi_periodic_kernel(amplitude: float, timescale: float, period: float, gamma: float):
    base = kernels.ExpSquared(scale=timescale)
    periodic = kernels.ExpSineSquared(scale=period, gamma=gamma)
    return amplitude**2 * base * periodic


def _box_transit(time: jnp.ndarray, depth: float, duration: float, period: float, t0: float) -> jnp.ndarray:
    phase = jnp.mod(time - t0 + 0.5 * period, period) - 0.5 * period
    in_transit = jnp.abs(phase) <= 0.5 * duration
    return 1.0 - depth * in_transit.astype(jnp.float64)


def _model(
    time: jnp.ndarray,
    flux: jnp.ndarray,
    flux_err: jnp.ndarray,
    *,
    period_prior: float,
    t0_prior: float,
    rot_period_prior: Optional[float],
):
    log_amp = numpyro.sample("log_amp", dist.Normal(jnp.log(jnp.var(flux) + 1e-6), 5.0))
    log_sigma = numpyro.sample("log_sigma", dist.Normal(jnp.log(jnp.std(flux) + 1e-6), 5.0))

    if rot_period_prior is None:
        rot_period = numpyro.sample(
            "rot_period", dist.LogNormal(jnp.log(jnp.maximum(period_prior, 0.1)), 0.5)
        )
    else:
        rot_period = numpyro.sample(
            "rot_period",
            dist.TruncatedNormal(
                loc=rot_period_prior,
                scale=0.2 * jnp.maximum(rot_period_prior, 1e-3),
                low=1e-3,
                high=1e3,
            ),
        )

    kernel = _quasi_periodic_kernel(
        amplitude=jnp.exp(log_amp),
        timescale=numpyro.sample("timescale", dist.LogNormal(jnp.log(5.0), 0.5)),
        period=rot_period,
        gamma=numpyro.sample("gamma", dist.LogNormal(jnp.log(1.0), 0.5)),
    )

    depth = numpyro.sample("depth", dist.Uniform(0.0005, 0.1))
    duration = numpyro.sample("duration", dist.Uniform(0.01, 0.5))
    period = numpyro.sample("period", dist.Normal(period_prior, 1e-3))
    t0 = numpyro.sample("t0", dist.Normal(t0_prior, 1e-3))

    mean_flux = _box_transit(time, depth, duration, period, t0)

    gp = GaussianProcess(kernel, time, diag=flux_err**2 + jnp.exp(2.0 * log_sigma))
    numpyro.sample("obs", gp.numpyro_dist(loc=mean_flux), obs=flux)


def run(
    time: np.ndarray,
    flux: np.ndarray,
    flux_err: np.ndarray,
    *,
    period: float,
    t0: float,
    rot_period_prior: Optional[float] = None,
    draws: int = 2000,
    tune: int = 2000,
    chains: int = 2,
    target_accept: float = 0.9,
    random_seed: Optional[int] = None,
    progressbar: bool = True,
) -> BackendResult:
    """Run NumPyro + tinygp inference for the spotless transit model."""

    time_jnp = jnp.asarray(time)
    flux_jnp = jnp.asarray(flux)
    flux_err_jnp = jnp.asarray(flux_err)

    nuts = NUTS(
        _model,
        target_accept_prob=target_accept,
    )
    mcmc = MCMC(nuts, num_warmup=tune, num_samples=draws, num_chains=chains, progress_bar=progressbar)
    mcmc.run(
        jax.random.PRNGKey(0 if random_seed is None else int(random_seed)),
        time=time_jnp,
        flux=flux_jnp,
        flux_err=flux_err_jnp,
        period_prior=period,
        t0_prior=t0,
        rot_period_prior=rot_period_prior,
    )

    samples = mcmc.get_samples(group_by_chain=True)
    predictive = Predictive(
        _model,
        samples=samples,
        return_sites=["obs"],
        parallel=progressbar,
    )
    posterior_predictive = predictive(
        jax.random.PRNGKey(1 if random_seed is None else int(random_seed) + 1),
        time=time_jnp,
        flux=flux_jnp,
        flux_err=flux_err_jnp,
        period_prior=period,
        t0_prior=t0,
        rot_period_prior=rot_period_prior,
    )

    inference = az.from_numpyro(mcmc, posterior_predictive=posterior_predictive)
    obs_pred = np.asarray(posterior_predictive["obs"]).mean(axis=0)

    return BackendResult(inference=inference, predictive_mean=obs_pred)


__all__ = ["BackendResult", "run"]
