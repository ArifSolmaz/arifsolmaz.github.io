"""SpotLightCurve: Tools for analyzing stellar activity in exoplanet light curves."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("spotlightcurve")
except PackageNotFoundError:  # pragma: no cover - during local development
    __version__ = "0.1.0"

__all__ = ["__version__"]
