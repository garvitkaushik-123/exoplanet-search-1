"""Offline sanity test: synthetic M-dwarf light curve (noise + spots + flares) with injected transit; check TLS recovers it."""
import numpy as np, batman
from wotan import flatten
from exosearch import search, vetting_flags
rng = np.random.default_rng(1)
t = np.arange(0, 54, 2/1440.)                      # ~2 sectors at 2-min cadence
f = 1 + 3e-3*np.sin(2*np.pi*t/3.1) + rng.normal(0, 1.5e-3, t.size)    # spots + 1500 ppm noise
fl = rng.random(t.size) < 2e-4; f[fl] += rng.uniform(0.005, 0.03, fl.sum())  # flares
p = batman.TransitParams(); p.t0, p.per, p.rp, p.a, p.inc, p.ecc, p.w, p.limb_dark, p.u = 1.3, 2.7, 0.045, 14, 89.5, 0, 90, "quadratic", [0.3, 0.3]
f *= batman.TransitModel(p, t).light_curve(p)
from exosearch import prepare
import lightkurve as lk
t2, f2, mad = prepare(lk.LightCurve(time=t, flux=f))
r = search(t2, f2, rstar=0.4, mstar=0.4, threads=4)
print(f"true P=2.700  found P={r.period:.4f}  SDE={r.SDE:.1f}  SNR={r.snr:.1f}  depth={(1-r.depth)*1e6:.0f} ppm (true ~{0.045**2*1e6:.0f})")
print(vetting_flags(r))
