import numpy as np
import matplotlib.pyplot as plt
from lightkurve import search_lightcurve
from lightkurve.correctors import DesignMatrix, PLDCorrector
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

# Your package
from spotlightcurve.preprocess import quality_mask
from spotlightcurve.model import transit_batman, transit_duration_hours

# -------- Choose any target here --------
TARGET = "WASP-52"           # e.g., "HAT-P-36", "HD 209458", or TIC number like "TIC 358936352"
AUTHOR = "SPOC"              # SPOC PDCSAP is easiest to start with
EXPTIME = "short"            # "short"=2m; use "fast"/"long"/None to allow other cadences
# ---------------------------------------

print(f"Searching TESS light curves for: {TARGET}")
sr = search_lightcurve(TARGET, mission="TESS", author=AUTHOR, exptime=EXPTIME)
if len(sr) == 0:
    # fallback without exptime filter
    sr = search_lightcurve(TARGET, mission="TESS", author=AUTHOR)
    if len(sr) == 0:
        raise SystemExit("No TESS light curves found for this target.")

print(sr)

# Download all sectors and stitch
lcs = sr.download_all()
lc = lcs.stitch().remove_nans()
print(f"Downloaded {len(lcs)} light curves; stitched length = {len(lc.flux)}")

# Normalize & basic sigma-clipping on flux
mask = quality_mask(lc.flux.value, sigma=5.0)
lc = lc[mask].normalize()

# Optional: additional flattening to remove long-term trends
lc_flat = lc.flatten(window_length=401)

# Try to get ephemeris (P, T0) from NASA Exoplanet Archive; fallback to BLS if missing
P = T0 = None
try:
    cat = NasaExoplanetArchive.query_criteria(table="pscomppars", where=f"pl_name like '{TARGET} b'")
    if len(cat) == 0:
        cat = NasaExoplanetArchive.query_criteria(table="ps", where=f"pl_name like '{TARGET} b'")
    if len(cat):
        P = float(cat["pl_orbper"][0])            # days
        T0 = float(cat["pl_tranmid"][0])          # days (BJD_TDB)
        print(f"Ephemeris from NASA Exoplanet Archive: P={P:.6f} d, T0={T0:.6f} (BJD_TDB)")
except Exception as e:
    print("Exoplanet Archive query failed; will try BLS. Reason:", e)

if P is None or not np.isfinite(P):
    print("Running BLS to estimate period (this may take a bit)...")
    bls = lc_flat.to_periodogram(method="bls", period=np.linspace(0.3, 20, 5000))
    P = bls.period_at_max_power.value
    T0 = bls.transit_time_at_max_power.value
    print(f"BLS estimate: P={P:.6f} d, T0={T0:.6f}")

# Phase-fold and quick look
folded = lc_flat.fold(period=P, epoch_time=T0)
fig, ax = plt.subplots(figsize=(7,3))
folded.scatter(ax=ax, s=2, alpha=0.5, color="tab:blue")
ax.set_title(f"{TARGET}: Folded PDCSAP (P={P:.5f} d)")
ax.set_xlabel("Phase [cycles]")
ax.set_ylabel("Relative flux [–]")
ax.grid(alpha=0.3)
plt.show()

# Bin for a cleaner profile (optional)
binned = folded.bin(time_bin_size=0.001)  # in phase units if folded
fig, ax = plt.subplots(figsize=(7,3))
folded.scatter(ax=ax, s=2, alpha=0.3, color="tab:blue", label="Unbinned")
binned.scatter(ax=ax, s=10, color="k", label="Binned")
ax.legend()
ax.grid(alpha=0.3); plt.show()

# --- Simple physical model overlay with batman ---
# Crude first guesses from common ranges; refine later with fitting
rp_rs_guess = max(0.03, np.sqrt(1 - np.nanmin(binned.flux.value)))  # depth≈(Rp/Rs)^2
a_rs_guess  = 10.0
inc_guess   = 88.0
ecc_guess   = 0.0
omega_guess = 90.0
u1, u2      = 0.3, 0.2

# Build a model time grid in days around one transit window
# Convert phase to time using t = T0 + phase*P
phase_zoom = (-0.05, 0.05)  # ±5% of period window
phase_grid = np.linspace(phase_zoom[0], phase_zoom[1], 600)
t_model = T0 + phase_grid * P

try:
    flux_model = transit_batman(
        time_days=t_model,
        rp_rs=rp_rs_guess,
        a_rs=a_rs_guess,
        inc_deg=inc_guess,
        period_days=P,
        t0_days=T0,
        ecc=ecc_guess,
        omega_deg=omega_guess,
        u1=u1, u2=u2,
        ld_model="quadratic"
    )
except ImportError:
    print("batman-package not installed; skipping model overlay.")
    flux_model = None

# Plot data (in time) with model
fig, ax = plt.subplots(figsize=(7,3))
# Select only points within the same time window
t_obs = folded.time.value * P + T0  # back to days
sel = (folded.phase.value > phase_zoom[0]) & (folded.phase.value < phase_zoom[1])
ax.scatter((t_obs[sel] - T0)*24, folded.flux.value[sel], s=6, alpha=0.5, label="PDCSAP (folded→time)")
if flux_model is not None:
    ax.plot((t_model - T0)*24, flux_model, lw=2, label="batman model")
ax.set_xlabel("Hours from mid-transit")
ax.set_ylabel("Relative flux [–]")
ax.set_title(f"{TARGET}: Transit window")
ax.grid(alpha=0.3); ax.legend()
plt.show()

# Compute and print some handy numbers
dur_hr = transit_duration_hours(a_rs_guess, rp_rs_guess, P, inc_guess, ecc_guess, omega_guess)
depth_ppm = 1e6 * (1 - np.nanmin(folded.flux.value))
print(f"Approx. depth ~ {depth_ppm:.0f} ppm, duration ~ {dur_hr:.2f} hours (from current guesses)")
