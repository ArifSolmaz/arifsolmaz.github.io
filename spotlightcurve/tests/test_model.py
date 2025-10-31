import numpy as np
from spotlightcurve.model import simple_transit_model

def test_simple_transit_model_drops_flux():
    t = np.linspace(0, 10, 100)
    f = simple_transit_model(t, depth=0.02, period=5.0, t0=0.0)
    # flux should stay near 1 outside transit
    assert np.isclose(f.max(), 1.0)
    # and dip to roughly 1-depth during transit
    assert np.isclose(f.min(), 1 - 0.02)
