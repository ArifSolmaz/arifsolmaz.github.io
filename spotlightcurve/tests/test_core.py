import numpy as np
from spotlightcurve import simulate_spot_curve, phase_fold

def test_simulate_spot_curve_shapes():
    t = np.linspace(0, 5, 100)
    f = simulate_spot_curve(t)
    assert f.shape == t.shape

def test_phase_fold_range():
    t = np.linspace(0, 5, 100)
    y = np.zeros_like(t)
    ph, _ = phase_fold(t, y, period=1.0)
    assert np.all(ph >= -0.5) and np.all(ph < 0.5)
