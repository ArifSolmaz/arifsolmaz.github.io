# spotlightcurve

A light-curve analysis and starspot modeling toolkit.

## Install (from GitHub)

```python
%pip install --no-build-isolation "git+https://github.com/ArifSolmaz/arifsolmaz.github.io@main"
```

Then:

```python
import spotlightcurve as sc
print(sc.__version__)
```

## Local dev

```bash
git clone https://github.com/ArifSolmaz/arifsolmaz.github.io
cd arifsolmaz.github.io
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -e .
pytest -q
```

## Minimal example

```python
import numpy as np
import matplotlib.pyplot as plt
from spotlightcurve import simulate_spot_curve

t = np.linspace(0, 10, 2000)
flux = simulate_spot_curve(t, period=3.2, amplitude=0.01, noise=5e-4)
plt.plot(t, flux); plt.xlabel("time [d]"); plt.ylabel("relative flux"); plt.show()
```

## License

MIT
