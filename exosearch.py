"""Core transit-search functions: clean -> detrend -> TLS -> basic vetting metrics."""
import numpy as np
from wotan import flatten
from transitleastsquares import transitleastsquares

def trim_edges(t, f, gap=0.4, trim=0.5):
    """Drop `trim` days at both ends of every continuous segment (TESS orbit-start ramps / scattered light)."""
    idx = np.where(np.diff(t) > gap)[0] + 1
    keep = np.ones(t.size, bool)
    for seg in np.split(np.arange(t.size), idx):
        if seg.size:
            keep[seg] = (t[seg] > t[seg][0] + trim) & (t[seg] < t[seg][-1] - trim)
    return t[keep], f[keep]

def prepare(lc, window=0.75, flare_sigma=3.0):
    """Normalise, drop NaNs/outliers (upper only: flares), biweight detrend."""
    lc = lc.remove_nans().normalize()
    t, f = lc.time.value, lc.flux.value
    t, f = trim_edges(t, f)
    flat, trend = flatten(t, f, method="biweight", window_length=window, return_trend=True, break_tolerance=0.5)
    ok = np.isfinite(flat)
    t, flat = t[ok], flat[ok]
    mad = 1.4826 * np.median(np.abs(flat - np.median(flat)))
    keep = flat < 1 + flare_sigma * mad          # clip flares/upward outliers only
    return t[keep], flat[keep], mad

def search(t, f, rstar=0.4, mstar=0.4, period_min=0.5, period_max=None, threads=1):
    span = t.max() - t.min()
    period_max = min(period_max or span / 2.0, 15.0)
    m = transitleastsquares(t, f)
    r = m.power(R_star=rstar, M_star=mstar, R_star_min=0.08, R_star_max=0.8,
                M_star_min=0.08, M_star_max=0.8, period_min=period_min,
                period_max=period_max, use_threads=threads,
                show_progress_bar=False, oversampling_factor=3, duration_grid_step=1.1)
    return r

def vetting_flags(r, sde_min=9.0, rms=None):
    """First-pass automatic cuts; anything passing still needs human + centroid vetting."""
    flags = {
        "sde_ok": r.SDE >= sde_min,
        "n_transits_ok": r.distinct_transit_count >= 3,
        "odd_even_ok": r.odd_even_mismatch < 3.0,       # sigma
        "snr_ok": r.snr >= 7.0,
        "depth_ok": 0 < (1 - r.depth) < 0.03,                # <3%: deeper is almost surely an eclipsing binary
        "duration_ok": 0.02 < r.duration / r.period < 0.15 and r.duration > 0.04,
    }
    if rms is not None: flags["noise_ok"] = rms < 0.006   # reject light curves too noisy to trust
    flags["not_orbit_systematic"] = not (abs(r.period - 13.7) < 1.0 or abs(r.period - 6.85) < 0.3 or abs(r.period - 27.4) < 1.0)
    flags["pass"] = all(flags.values())
    return flags
