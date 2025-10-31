# streamlit_app3.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

import lightkurve as lk
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

# ---------- Optional imports from your package ----------
try:
    from spotlightcurve.model import transit_batman, transit_duration_hours
except Exception:
    transit_batman = None

    # very rough fallback duration (circular, small Rp)
    def transit_duration_hours(a_rs, rp_rs, period_days, inc_deg, ecc, omega_deg):
        inc = np.deg2rad(inc_deg)
        b = a_rs * np.cos(inc)
        term = max(0.0, 1.0 - b**2)
        arg = np.clip(np.sqrt(term) / a_rs, 0.0, 1.0)
        dur_days = (period_days / np.pi) * np.arcsin(arg)
        return float(dur_days * 24.0)

try:
    from spotlightcurve.preprocess import quality_mask
except Exception:
    quality_mask = None

try:
    from scipy.optimize import least_squares
except Exception:
    least_squares = None


# ====================== UI SETUP ======================
st.set_page_config(page_title="TESS Transit Explorer", layout="wide")
st.title("TESS Transit Explorer (per-sector, BLS, shape fit)")

# ---- Sidebar: target & data source ----
st.sidebar.header("Select a TESS Target")
target_name = st.sidebar.text_input("Name or TIC", "WASP-52")

author = st.sidebar.selectbox("Pipeline", ["SPOC", "QLP", "Any"], index=0)
cadence_hint = st.sidebar.selectbox(
    "Cadence (hint)", ["Any", "short (2m)", "fast (20s)", "long (10m)"], index=0
)

st.sidebar.divider()
st.sidebar.header("Processing")
sigma_clip = st.sidebar.slider("Sigma-clip [σ]", 3.0, 10.0, 5.0, 0.5)
flatten_window = st.sidebar.slider("Flatten window (cadences)", 101, 2001, 401, 50)
bin_minutes = st.sidebar.slider("Phase bin [min]", 0.0, 60.0, 10.0, 0.5)

# ---- BLS search controls ----
st.sidebar.header("BLS search")
pmin = st.sidebar.number_input("Min period [d]", 0.10, 100.0, 0.30, 0.01)
pmax = st.sidebar.number_input("Max period [d]", pmin + 0.01, 200.0, 20.0, 0.1)
dmin = st.sidebar.number_input("Min duration [d]", 0.005, 1.0, 0.01, 0.005)
dmax = st.sidebar.number_input("Max duration [d]", dmin + 0.005, 1.0, 0.20, 0.005)
per_grid = np.linspace(pmin, pmax, 6000)
# durations must be < min(period) to satisfy astropy BoxLeastSquares
dur_grid = np.linspace(dmin, min(dmax, 0.9 * pmin), 30)
if dur_grid.size == 0:
    dur_grid = np.array([0.45 * pmin])

st.sidebar.divider()
st.sidebar.header("Model (used for plotting & fitting)")
LD_PRESETS = {"TESS": (0.32, 0.27), "Kepler": (0.36, 0.28), "Sloan r'": (0.36, 0.29), "Custom": None}
band = st.sidebar.selectbox("Bandpass (LD preset)", list(LD_PRESETS.keys()), index=0)
if band != "Custom":
    u1_preset, u2_preset = LD_PRESETS[band]
    u1 = st.sidebar.number_input("u1", value=float(u1_preset), step=0.01, format="%.3f", disabled=True)
    u2 = st.sidebar.number_input("u2", value=float(u2_preset), step=0.01, format="%.3f", disabled=True)
else:
    u1 = st.sidebar.number_input("u1", value=0.30, step=0.01, format="%.3f")
    u2 = st.sidebar.number_input("u2", value=0.20, step=0.01, format="%.3f")

if "rp_rs_slider" not in st.session_state:
    st.session_state["rp_rs_slider"] = 0.10

rp_rs = st.sidebar.slider("Rₚ/R★", 0.01, 0.30, float(st.session_state["rp_rs_slider"]), 0.001)
a_rs   = st.sidebar.slider("a/R★",   3.0, 30.0, 12.0, 0.1)
inc    = st.sidebar.slider("i [deg]", 80.0, 90.0, 88.0, 0.01)
ecc    = st.sidebar.slider("e",       0.0, 0.9, 0.0, 0.01)
omega  = st.sidebar.slider("ω [deg]", 0.0, 360.0, 90.0, 1.0)

plot_ppm = st.sidebar.checkbox("Plot phase zoom in ppm", value=False)


# ====================== HELPERS ======================
def cadence_hint_to_arg(s: str):
    return {"short (2m)": "short", "fast (20s)": "fast", "long (10m)": "long"}.get(s, None)

@st.cache_data(show_spinner=False)
def query_ephemeris(name: str):
    """Return (P, T0) from NASA Exoplanet Archive or (nan, nan)."""
    try:
        q = NasaExoplanetArchive.query_criteria(
            table="pscomppars",
            where=f"hostname like '%{name}%' or pl_name like '%{name}%'"
        )
        if len(q):
            row = None
            for r in q:
                if str(r.get("pl_letter", "")).strip().lower() == "b":
                    row = r; break
            row = row or q[0]
            P = float(row["pl_orbper"]) if row["pl_orbper"] is not None else np.nan
            T0 = float(row["pl_tranmid"]) if row["pl_tranmid"] is not None else np.nan
            return P, T0
    except Exception:
        pass
    return np.nan, np.nan

@st.cache_data(show_spinner=True)
def search_lc(name: str, author: str, cadence_hint: str):
    """Return (SearchResult, [sectors])."""
    kwargs = {"mission": "TESS"}
    if author != "Any":
        kwargs["author"] = author
    exptime = cadence_hint_to_arg(cadence_hint)
    if exptime:
        kwargs["exptime"] = exptime
    sr = lk.search_lightcurve(name, **kwargs)
    if len(sr) == 0 and exptime:
        kwargs.pop("exptime", None)
        sr = lk.search_lightcurve(name, **kwargs)

    # robust sector extraction
    sectors = []
    for row in sr.table:
        s = row.get("sequence_number", None) or row.get("sector", None)
        if s is None:
            desc = str(row.get("description", ""))
            if "Sector" in desc:
                try:
                    s = int(desc.split("Sector")[1].split()[0])
                except Exception:
                    s = None
        sectors.append(s)
    return sr, sectors

def sigma_clip_mask(flux_vals, sigma):
    if quality_mask is not None:
        return quality_mask(np.asarray(flux_vals), sigma=sigma)
    f = np.asarray(flux_vals, dtype=float)
    mu = np.nanmedian(f); sd = np.nanstd(f)
    if not np.isfinite(sd) or sd == 0:
        return np.isfinite(f)
    z = np.abs((f - mu) / sd)
    return np.isfinite(f) & (z < sigma)

def stitch_selected(sr: lk.search.SearchResult, selected_indices: list[int]):
    """Download only selected rows (sectors) and stitch."""
    if not selected_indices:
        return None, []
    lcs = lk.LightCurveCollection([sr[i].download() for i in selected_indices if sr[i] is not None])
    if len(lcs) == 0:
        return None, []
    stitched = lcs.stitch().remove_nans().normalize()
    sec_list = []
    for lc in lcs:
        sec_list.append(getattr(lc, "sector", None) or lc.meta.get("SECTOR"))
    return stitched, sec_list

def safe_batman(time_days, **kwargs):
    """Call transit_batman with exposure/supersample if supported; fallback cleanly."""
    if transit_batman is None:
        return None
    try:
        return transit_batman(
            time_days=time_days, **kwargs,
            exp_time_days=kwargs.get("exp_time_days", None),
            supersample_factor=kwargs.get("supersample_factor", None),
        )
    except TypeError:
        kwargs.pop("exp_time_days", None)
        kwargs.pop("supersample_factor", None)
        return transit_batman(time_days=time_days, **kwargs)


# ====================== DATA FETCH ======================
P_ephem, T0_ephem = query_ephemeris(target_name)

sr, sectors = search_lc(target_name, author, cadence_hint)
if len(sr) == 0:
    st.warning("No TESS light curve found for this target / settings.")
    st.stop()

indices = list(range(len(sr)))
pretty_labels = []
for i, s in zip(indices, sectors):
    lab = f"Row {i}"
    if s is not None:
        lab += f" (Sector {s})"
    pretty_labels.append(lab)

st.subheader("Available sectors")
sel = st.multiselect(
    "Choose sectors to analyze (default: all)",
    options=indices, default=indices,
    format_func=lambda i: pretty_labels[i]
)

with st.spinner("Downloading selected sectors..."):
    lc, selected_sec_list = stitch_selected(sr, sel)

if lc is None:
    st.warning("Could not download selected sectors.")
    st.stop()

st.success(f"Downloaded {len(lc.time)} cadences from {len(sel)} selected row(s).")


# ====================== PREPROCESS ======================
mask = sigma_clip_mask(lc.flux.value, sigma_clip)
lc = lc[mask]
lc_flat = lc.flatten(window_length=int(flatten_window), return_trend=False)

tab1, tab2, tab3 = st.tabs(["Raw (normalized)", "Flattened", "Folded + Model + Fit"])

with tab1:
    st.caption("PDCSAP normalized (sigma-clipped)")
    fig, ax = plt.subplots(figsize=(10, 3))
    lc.scatter(ax=ax, s=1, color="tab:blue")
    ax.set_xlabel("Time [BTJD days]")
    ax.set_ylabel("Relative flux [–]")
    ax.grid(alpha=0.3)
    st.pyplot(fig, clear_figure=True)
    st.download_button("Download RAW CSV", lc.to_pandas().to_csv(index=False), "tess_raw.csv")

with tab2:
    st.caption("Flattened (long-term trends removed)")
    fig, ax = plt.subplots(figsize=(10, 3))
    lc_flat.scatter(ax=ax, s=1, color="tab:green")
    ax.set_xlabel("Time [BTJD days]")
    ax.set_ylabel("Relative flux [–]")
    ax.grid(alpha=0.3)
    st.pyplot(fig, clear_figure=True)
    st.download_button("Download FLAT CSV", lc_flat.to_pandas().to_csv(index=False), "tess_flat.csv")

with tab3:
    # ---------- Ephemeris or BLS ----------
    P, T0 = P_ephem, T0_ephem
    bls = None
    if not np.isfinite(P) or not np.isfinite(T0):
        with st.spinner("No ephemeris found; estimating with BLS..."):
            bls = lc_flat.to_periodogram(
                method="bls",
                period=per_grid,
                duration=dur_grid,
                objective="snr",
                frequency_factor=5,   # astropy kw; oversample_factor is not valid here
            )
            P = bls.period_at_max_power.value
            T0 = bls.transit_time_at_max_power.value

    # Optional: BLS plot
    if bls is not None:
        with st.expander("Show BLS periodogram"):
            figp, axp = plt.subplots(figsize=(10, 3))
            axp.plot(bls.period.value, bls.power, lw=1.2)
            axp.axvline(P, color="tab:red", ls="--", lw=1.5, label=f"P = {P:.5f} d")
            axp.set_xlabel("Period [days]")
            axp.set_ylabel("BLS power [S/N]")
            axp.set_title("BLS periodogram")
            axp.grid(alpha=0.3); axp.legend()
            st.pyplot(figp, clear_figure=True)

    folded = lc_flat.fold(period=P, epoch_time=T0)

    # Bin size in phase units from minutes (if any)
    if bin_minutes > 0:
        bin_phase = (bin_minutes / (60 * 24)) / P
        folded_binned = folded.bin(time_bin_size=bin_phase)
    else:
        folded_binned = folded

    # ---------- Duration-based zoom (prefer BLS duration) ----------
    bls_dur_hr = None
    if bls is not None:
        try:
            bls_dur_hr = float(24.0 * bls.duration_at_max_power.value)
        except Exception:
            bls_dur_hr = None

    dur_hr_est = float(transit_duration_hours(a_rs, rp_rs, P, inc, ecc, omega))
    if bls_dur_hr is not None and np.isfinite(bls_dur_hr):
        dur_hr_est = bls_dur_hr
    dur_hr_est = max(dur_hr_est, 0.5)      # safety floor
    xlim_hr    = max(4.0 * dur_hr_est, 2.0)

    # Model time grid centered on T0
    t_model = np.linspace(T0 - xlim_hr / 24.0, T0 + xlim_hr / 24.0, 1400)
    # exposure guess (smooths model)
    texp_days = (bin_minutes if bin_minutes > 0 else 2.0) / (60.0 * 24.0)

    # Model from sliders (red)
    flux_model = safe_batman(
        time_days=t_model, rp_rs=rp_rs, a_rs=a_rs, inc_deg=inc,
        period_days=P, t0_days=T0, ecc=ecc, omega_deg=omega,
        u1=u1, u2=u2, ld_model="quadratic",
        exp_time_days=texp_days, supersample_factor=7
    )

    # ---------- Shape fit: Rp/R★, a/R★, i, ΔT0 ----------
    st.markdown("### Quick fit (shape: Rp/R★, a/R★, i, ΔT0)")
    run_fit = st.button(
        "Fit shape parameters",
        type="primary",
        disabled=(transit_batman is None or least_squares is None)
    )
    st.caption("Fits Rp/R★, a/R★, i, and a mid-time offset; keeps e, ω fixed.")

    rp_rs_fit = a_rs_fit = inc_fit = T0_fit = None
    fit_msg = ""

    if run_fit:
        if transit_batman is None:
            st.error("batman-package not available.")
        elif least_squares is None:
            st.error("SciPy not available. `pip install scipy`")
        else:
            xb_all = folded_binned.phase.value * P * 24.0
            sel_fit = np.abs(xb_all) < xlim_hr
            x_hours = xb_all[sel_fit]
            t_days  = T0 + (x_hours / 24.0)
            y = folded_binned.flux.value[sel_fit]

            p0 = np.array([rp_rs, a_rs, inc, 0.0])          # rp, aR, inc[deg], dt0[min]
            lb = np.array([0.005,  2.0, 80.0, -90.0])
            ub = np.array([0.500, 40.0, 90.0,  90.0])

            def model_for(params):
                rpr, aR, inc_deg, dt0_min = params
                return safe_batman(
                    time_days=t_days,
                    rp_rs=float(rpr), a_rs=float(aR), inc_deg=float(inc_deg),
                    period_days=float(P), t0_days=float(T0 + dt0_min/1440.0),
                    ecc=float(ecc), omega_deg=float(omega),
                    u1=float(u1), u2=float(u2), ld_model="quadratic",
                    exp_time_days=texp_days, supersample_factor=7
                )

            def resid(params):
                return model_for(params) - y

            try:
                res = least_squares(
                    resid, p0, bounds=(lb, ub),
                    x_scale=[max(rp_rs, 0.1), max(a_rs, 5.0), 1.0, 10.0],
                    ftol=1e-10, xtol=1e-10
                )
                rp_rs_fit, a_rs_fit, inc_fit, dt0_fit_min = res.x
                T0_fit = T0 + dt0_fit_min/1440.0
                fit_msg = (
                    f"Fit ok: Rp/R★={rp_rs_fit:.4f}, a/R★={a_rs_fit:.2f}, "
                    f"i={inc_fit:.2f}°, ΔT0={dt0_fit_min:+.2f} min"
                )
            except Exception as e:
                fit_msg = f"Fit failed: {e}"

    if fit_msg:
        st.info(fit_msg)

    # Buttons to apply best-fit back to sliders (so red curve can match green)
    apply_cols = st.columns(3)
    with apply_cols[0]:
        if (rp_rs_fit is not None) and st.button("Apply Rp/R★"):
            st.session_state["rp_rs_slider"] = float(rp_rs_fit); st.experimental_rerun()
    with apply_cols[1]:
        if (a_rs_fit is not None) and st.button("Apply a/R★"):
            st.warning(f"Set a/R★ slider to {a_rs_fit:.2f}")
    with apply_cols[2]:
        if (inc_fit is not None) and st.button("Apply i"):
            st.warning(f"Set i slider to {inc_fit:.2f}°")

    # Fitted model curve (green)
    flux_model_fit = None
    if (rp_rs_fit is not None) and (a_rs_fit is not None) and (inc_fit is not None) and (T0_fit is not None):
        flux_model_fit = safe_batman(
            time_days=t_model, rp_rs=rp_rs_fit, a_rs=a_rs_fit, inc_deg=inc_fit,
            period_days=P, t0_days=T0_fit, ecc=ecc, omega_deg=omega,
            u1=u1, u2=u2, ld_model="quadratic",
            exp_time_days=texp_days, supersample_factor=7
        )

    # ---------- Metrics ----------
    depth_est = 1.0 - np.nanmin(folded_binned.flux.value)
    mA, mB, mC = st.columns(3)
    mA.metric("P [days]", f"{P:.6f}")
    mB.metric("T0 [BTJD]", f"{T0:.6f}")
    mC.metric("Depth est. [ppm]", f"{depth_est*1e6:.0f}")

    # ---------- Phase plot (duration-zoom) ----------
    x_all = folded.phase.value * P * 24.0
    y_all = folded.flux.value
    sel_zoom = np.abs(x_all) < xlim_hr
    x = x_all[sel_zoom]; y = y_all[sel_zoom]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.scatter(x, (1 - y) * 1e6 if plot_ppm else y, s=4, alpha=0.35,
               color="tab:blue", label="Folded", rasterized=True)

    # binned
    xb = folded_binned.phase.value * P * 24.0
    yb = folded_binned.flux.value
    ax.scatter(xb, (1 - yb) * 1e6 if plot_ppm else yb, s=22, color="k",
               zorder=3, label="Binned")

    # error bars if available
    if hasattr(folded_binned, "flux_err") and (folded_binned.flux_err is not None):
        yerr = folded_binned.flux_err.value
        if plot_ppm:
            yerr = yerr * 1e6
            yplot = (1 - yb) * 1e6
        else:
            yplot = yb
        ax.errorbar(xb, yplot, yerr=yerr, fmt="none", ecolor="0.5",
                    elinewidth=1, capsize=0, alpha=0.6, zorder=2)

    # running-median guide through binned points
    if xb.size > 10:
        order = np.argsort(xb)
        xb_sorted = xb[order]; yb_sorted = yb[order]
        k = max(5, int(0.06 * xb_sorted.size))
        pad = k // 2
        ymed = np.copy(yb_sorted)
        for i in range(xb_sorted.size):
            lo = max(0, i - pad); hi = min(xb_sorted.size, i + pad + 1)
            ymed[i] = np.nanmedian(yb_sorted[lo:hi])
        ax.plot(xb_sorted, (1 - ymed) * 1e6 if plot_ppm else ymed,
                lw=1.2, color="0.25", alpha=0.9, label="Running median")

    # shade T14
    ax.axvspan(-0.5 * dur_hr_est, +0.5 * dur_hr_est, color="tab:red", alpha=0.08, lw=0)

    # models
    if flux_model is not None:
        xm = (t_model - T0) * 24.0
        ym = (1 - flux_model) * 1e6 if plot_ppm else flux_model
        ax.plot(xm, ym, lw=2, color="tab:red", label="Model (sliders)")

    if flux_model_fit is not None:
        xm2 = (t_model - T0_fit) * 24.0
        ym2 = (1 - flux_model_fit) * 1e6 if plot_ppm else flux_model_fit
        ax.plot(xm2, ym2, lw=2, color="tab:green", label="Model (fitted)")

    ax.set_xlim(-xlim_hr, xlim_hr)
    ax.set_xlabel("Hours from mid-transit")
    ax.set_ylabel("Depth [ppm]" if plot_ppm else "Relative flux [–]")
    ax.set_title(f"Folded transit (P={P:.5f} d)")

    # tidy y-range (avoid extreme outliers)
    if not plot_ppm:
        med = np.nanmedian(yb)
        spread = np.nanpercentile(y, 84) - np.nanpercentile(y, 16)
        spread = spread if np.isfinite(spread) and spread > 0 else 0.01
        ax.set_ylim(med - 1.7 * spread, med + 1.7 * spread)

    ax.grid(alpha=0.3); ax.legend()
    st.pyplot(fig, clear_figure=True)

    # ---------- Residuals (centered at 0) ----------
    if (flux_model is not None) or (flux_model_fit is not None):
        if flux_model_fit is not None:
            model_times = (t_model - T0_fit) * 24.0
            model_vals  = flux_model_fit
        else:
            model_times = (t_model - T0) * 24.0
            model_vals  = flux_model

        from numpy import interp
        selb = np.abs(xb) < xlim_hr
        mb   = interp(xb[selb], model_times, model_vals, left=np.nan, right=np.nan)
        resid = yb[selb] - mb

        # robust symmetric limits via MAD
        medr = np.nanmedian(resid)
        mad  = 1.4826 * np.nanmedian(np.abs(resid - medr))
        yl   = 6 * (mad if np.isfinite(mad) and mad > 0 else np.nanstd(resid))
        yl   = float(yl if np.isfinite(yl) and yl > 0 else 0.005)

        figr, axr = plt.subplots(figsize=(10, 2.4))
        axr.axhline(0, color="0.3", lw=1)
        if plot_ppm:
            axr.scatter(xb[selb], -resid * 1e6, s=14, color="tab:purple", alpha=0.9)
            axr.set_ylabel("Residual [ppm]")
            axr.set_ylim(-yl * 1e6, yl * 1e6)
        else:
            axr.scatter(xb[selb], resid, s=14, color="tab:purple", alpha=0.9)
            axr.set_ylabel("Residual [–]")
            axr.set_ylim(-yl, yl)
        axr.set_xlim(-xlim_hr, xlim_hr)
        axr.set_xlabel("Hours from mid-transit")
        axr.grid(alpha=0.3)
        st.pyplot(figr, clear_figure=True)

    # ---------- Quick derived numbers ----------
    depth_ppm = (1 - np.nanmedian(yb)) * 1e6
    oot = np.abs(xb) > 2 * dur_hr_est
    oot_rms = float(np.nanstd(yb[oot])) if np.any(oot) else float("nan")
    n_in = int(np.count_nonzero(np.abs(xb) <= 0.5 * dur_hr_est))
    snr_tr = (depth_ppm / 1e6) / oot_rms * np.sqrt(max(n_in, 1)) if np.isfinite(oot_rms) and oot_rms > 0 else float("nan")
    mD, mE, mF = st.columns(3)
    mD.metric("Binned depth [ppm]", f"{depth_ppm:.0f}")
    mE.metric("OOT RMS [–]", f"{oot_rms:.5f}" if np.isfinite(oot_rms) else "—")
    mF.metric("Single-transit S/N [~]", f"{snr_tr:.1f}" if np.isfinite(snr_tr) else "—")

    # Downloads
    st.download_button("Download FOLDED CSV", folded.to_pandas().to_csv(index=False), "tess_folded.csv")
