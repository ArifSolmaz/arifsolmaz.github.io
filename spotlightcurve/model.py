# --- Scientific transit model helpers (Mandel & Agol via batman) ---
import numpy as np

def impact_parameter(a_rs: float, inc_deg: float, ecc: float = 0.0, omega_deg: float = 90.0) -> float:
    """Impact parameter b = (a/Rs) cos i * (1 - e^2) / (1 + e sin ω)."""
    inc = np.deg2rad(inc_deg)
    omega = np.deg2rad(omega_deg)
    return (a_rs * np.cos(inc)) * (1.0 - ecc**2) / (1.0 + ecc * np.sin(omega))

def transit_duration_hours(
    a_rs: float, rp_rs: float, period_days: float, inc_deg: float, ecc: float = 0.0, omega_deg: float = 90.0
) -> float:
    """
    Approximate total duration T14 in hours.
    Uses standard small-angle/Keplerian geometry; valid for non-grazing transits.
    """
    b = impact_parameter(a_rs, inc_deg, ecc, omega_deg)
    # guard invalid domain
    inside = (1.0 + rp_rs) ** 2 - b**2
    inside = max(inside, 0.0)
    inc = np.deg2rad(inc_deg)
    omega = np.deg2rad(omega_deg)
    num = np.sqrt(inside)
    den = a_rs * np.sin(inc)
    if den <= 0 or num <= 0:
        return 0.0
    k = np.sqrt(1.0 - ecc**2) / (1.0 + ecc * np.sin(omega))
    dur_days = (period_days / np.pi) * np.arcsin(np.clip(num / den, 0.0, 1.0)) * k
    return float(24.0 * dur_days)

def transit_batman(
    time_days: np.ndarray,
    rp_rs: float = 0.1,
    a_rs: float = 10.0,
    inc_deg: float = 88.0,
    period_days: float = 5.0,
    t0_days: float = 0.0,
    ecc: float = 0.0,
    omega_deg: float = 90.0,
    u1: float = 0.3,
    u2: float = 0.2,
    ld_model: str = "quadratic",
) -> np.ndarray:
    """
    High-fidelity transit flux using batman (Mandel & Agol 2002) with quadratic limb darkening.
    Returns relative flux (1.0 out of transit).
    """
    try:
        import batman  # type: ignore
    except Exception as e:
        raise ImportError("batman-package is required: pip install batman-package") from e

    params = batman.TransitParams()
    params.t0 = t0_days
    params.per = period_days
    params.rp = rp_rs
    params.a = a_rs
    params.inc = inc_deg
    params.ecc = ecc
    params.w = omega_deg
    params.u = [u1, u2]
    params.limb_dark = ld_model
    m = batman.TransitModel(params, time_days)
    return m.light_curve(params)

# --- Simple fallback box model (used if batman is unavailable) ---
def simple_transit_model(time_days, depth=0.01, period_days=5.0, t0_days=0.0, width_frac=0.02):
    """
    Minimal box model: a drop of 'depth' for a fixed width_frac of the period around t0.
    """
    phase = ((time_days - t0_days) % period_days) / period_days
    halfw = 0.5 * width_frac
    in_tr = (phase > 0.5 - halfw) & (phase < 0.5 + halfw)
    flux = np.ones_like(time_days, dtype=float)
    flux[in_tr] -= depth
    return flux
