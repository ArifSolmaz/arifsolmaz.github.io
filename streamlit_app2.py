import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from spotlightcurve.model import (
    transit_batman, simple_transit_model, impact_parameter, transit_duration_hours
)

# Approximate quadratic LD (u1,u2) presets for a Sun-like star (illustrative only)
LD_PRESETS = {
    "Custom": None,
    "TESS": (0.32, 0.27),
    "Kepler": (0.36, 0.28),
    "Johnson V": (0.43, 0.29),
    "Johnson R": (0.35, 0.30),
    "Johnson I": (0.27, 0.28),
    "Sloan g'": (0.52, 0.22),
    "Sloan r'": (0.36, 0.29),
    "Sloan i'": (0.28, 0.28),
}

st.set_page_config(page_title="Transit Model (Mandel & Agol)", layout="wide")
st.title("Simple Transit Model Demo (with units & limb darkening)")

# --- Sidebar inputs with units ---
st.sidebar.header("Stellar & Orbit (units)")
period = st.sidebar.slider("Orbital period P [days]", 0.2, 50.0, 5.0, 0.1)
t0 = st.sidebar.slider("Mid-transit time t₀ [days]", 0.0, period, 0.0, 0.01)
a_rs = st.sidebar.slider("Scaled semi-major axis a/R★ [–]", 2.0, 40.0, 12.0, 0.1)
inc = st.sidebar.slider("Inclination i [deg]", 80.0, 90.0, 88.0, 0.01)
ecc = st.sidebar.slider("Eccentricity e [–]", 0.0, 0.95, 0.0, 0.01)
omega = st.sidebar.slider("Arg. of periastron ω [deg]", 0.0, 360.0, 90.0, 1.0)

st.sidebar.header("Planet & Limb Darkening")
rp_rs = st.sidebar.slider("Radius ratio Rₚ/R★ [–]", 0.005, 0.3, 0.1, 0.001)

band = st.sidebar.selectbox("Bandpass (presets for u1,u2)", list(LD_PRESETS.keys()), index=1)
manual_ld = (band == "Custom")

if not manual_ld:
    u1_preset, u2_preset = LD_PRESETS[band]
    u1 = st.sidebar.number_input("LD coeff u1 [–]", value=float(u1_preset), step=0.01, format="%.3f", disabled=True)
    u2 = st.sidebar.number_input("LD coeff u2 [–]", value=float(u2_preset), step=0.01, format="%.3f", disabled=True)
else:
    u1 = st.sidebar.number_input("LD coeff u1 [–]", value=0.30, step=0.01, format="%.3f")
    u2 = st.sidebar.number_input("LD coeff u2 [–]", value=0.20, step=0.01, format="%.3f")

ld_model = "quadratic"

st.sidebar.header("Time sampling")
n_periods = st.sidebar.slider("# of periods to show [–]", 1, 5, 2, 1)
cadence_min = st.sidebar.slider("Cadence [minutes]", 0.1, 30.0, 2.0, 0.1)

# --- Build time array (days) ---
t_span_days = n_periods * period
dt_days = cadence_min / (60.0 * 24.0)
t = np.arange(t0 - 0.5 * t_span_days, t0 + 0.5 * t_span_days + dt_days, dt_days)

# --- Compute transit curve ---
use_batman = st.toggle("Use accurate Mandel & Agol (batman)", value=True)
try:
    if use_batman:
        flux = transit_batman(
            t, rp_rs=rp_rs, a_rs=a_rs, inc_deg=inc, period_days=period, t0_days=t0,
            ecc=ecc, omega_deg=omega, u1=u1, u2=u2, ld_model=ld_model
        )
    else:
        # width ~ duration fraction ~ (transit_duration / P)
        approx_width = max(0.002, min(0.15, transit_duration_hours(a_rs, rp_rs, period, inc, ecc, omega) / 24.0 / period))
        flux = simple_transit_model(t, depth=rp_rs**2, period_days=period, t0_days=t0, width_frac=approx_width)
    engine = "batman" if use_batman else "box"
except ImportError:
    st.warning("`batman-package` not installed. Using fallback box model. Run: `pip install batman-package`")
    approx_width = max(0.002, min(0.15, transit_duration_hours(a_rs, rp_rs, period, inc, ecc, omega) / 24.0 / period))
    flux = simple_transit_model(t, depth=rp_rs**2, period_days=period, t0_days=t0, width_frac=approx_width)
    engine = "box"

# --- Derived quantities ---
b = impact_parameter(a_rs, inc, ecc, omega)
depth_ppm = 1e6 * (1.0 - np.min(flux))
dur_hr = transit_duration_hours(a_rs, rp_rs, period, inc, ecc, omega)

colA, colB = st.columns([2, 1])

with colA:
    # Full-view plot
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    ax1.plot(t, flux, lw=1.5)
    ax1.set_xlabel("Time [days]")
    ax1.set_ylabel("Relative flux [–]")
    ax1.set_title(f"Transit light curve ({engine})")
    ax1.grid(alpha=0.3)
    st.pyplot(fig1, clear_figure=True)

    # --- Phase-folded plot (simple ppm toggle) ---
    st.subheader("Phase-folded transit")
    plot_ppm = st.checkbox("Show depth in ppm (instead of relative flux)", value=False)

    phase = ((t - t0 + 0.5 * period) % period) - 0.5 * period  # [-P/2, P/2]
    sel = np.abs(phase) < 0.15 * period  # small window around transit

    fig2, ax2 = plt.subplots(figsize=(8, 3))
    if plot_ppm:
        ax2.plot(phase[sel] * 24.0, (1.0 - flux[sel]) * 1e6, lw=1.5)
        ax2.set_ylabel("Transit depth [ppm]")
        # simple y-zoom around the dip
        depth_est = max(1e-6, 1.0 - np.min(flux))
        ax2.set_ylim(-0.15 * depth_est * 1e6, 1.3 * depth_est * 1e6)
    else:
        ax2.plot(phase[sel] * 24.0, flux[sel], lw=1.5)
        ax2.set_ylabel("Relative flux [–]")
        depth_est = max(1e-6, 1.0 - np.min(flux))
        ax2.set_ylim(1 - 1.3 * depth_est, 1 + 0.15 * depth_est)

    ax2.set_xlabel("Phase [hours from mid-transit]")
    ax2.set_title("Phase-folded transit (zoom)")
    ax2.grid(alpha=0.3)
    st.pyplot(fig2, clear_figure=True)

with colB:
    st.subheader("Derived / Helpful")
    st.metric("Impact parameter b [–]", f"{b:.3f}")
    st.metric("Depth ≈ (Rₚ/R★)² [ppm]", f"{depth_ppm:.0f}")
    st.metric("Duration T₁₄ [hours]", f"{dur_hr:.2f}")
    st.caption("Notes: duration is approximate; accurate values depend on limb darkening and geometry.")
    st.divider()

    # --- Simple, clean parameter list (no code view) ---
    st.subheader("Current parameters")
    st.write(f"**Bandpass:** {band}")
    st.write(f"**Rₚ/R★:** {rp_rs:.3f}")
    st.write(f"**a/R★:** {a_rs:.2f}")
    st.write(f"**Inclination:** {inc:.2f}°")
    st.write(f"**Period:** {period:.3f} days")
    st.write(f"**t₀:** {t0:.3f} days")
    st.write(f"**Eccentricity:** {ecc:.3f}")
    st.write(f"**ω (arg. of periastron):** {omega:.1f}°")
    st.write(f"**Limb darkening (quadratic):** u₁={u1:.3f}, u₂={u2:.3f}")
    st.write(f"**Cadence:** {cadence_min:.1f} min")
