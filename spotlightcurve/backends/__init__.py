"""Backend selection utilities for SpotLightCurve."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Literal

BackendName = Literal["pymc", "numpyro"]

_BACKEND_MODULES = {
    "pymc": "spotlightcurve.backends.pymc_backend",
    "numpyro": "spotlightcurve.backends.numpyro_backend",
}


def get_backend(name: BackendName | str) -> ModuleType:
    """Return the backend module corresponding to ``name``.

    Parameters
    ----------
    name:
        Name of the backend to load. Supported values are ``"pymc"`` and
        ``"numpyro"`` (case insensitive).

    Returns
    -------
    ModuleType
        The imported backend module.

    Raises
    ------
    KeyError
        If ``name`` does not match a supported backend.
    ImportError
        If the backend's optional dependencies are missing.
    """

    key = str(name).lower()
    if key not in _BACKEND_MODULES:
        raise KeyError(f"Unsupported backend '{name}'.")

    module_path = _BACKEND_MODULES[key]
    return import_module(module_path)


__all__ = ["BackendName", "get_backend"]
