"""Multi-year consistency check of a TGLC signal with independent TARS FFI light curves (all sectors).
Usage: python tars_check.py TIC PERIOD T0 DUR_H"""
import io, sys, numpy as np, requests, warnings, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.io import fits
from astroquery.mast import Observations
from wotan import flatten
from astropy.timeseries import BoxLeastSquares
warnings.filterwarnings("ignore")
tic, P0, T00, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) / 24
o = Observations.query_criteria(target_name=str(tic), provenance_name="TARS")
if len(o) == 0: print(f"TIC {tic}: no TARS light curves"); sys.exit()
p = Observations.get_product_list(o); T, F, S = [], [], []
for uri, fn in zip(p["dataURI"], p["productFilename"]):
    if not str(fn).endswith(".fits"): continue
    b = requests.get("https://mast.stsci.edu/api/v0.1/Download/file?uri=" + str(uri), timeout=180).content
    with fits.open(io.BytesIO(b)) as h:
        sec = h[0].header.get("SECTOR", -1); d = h[1].data; t = np.array(d["TIME"], float); f = np.array(d["FLUX"], float)
        ok = np.isfinite(t) & np.isfinite(f) & (f > 0); T.append(t[ok]); F.append(f[ok] / np.nanmedian(f[ok])); S.append(np.full(ok.sum(), sec))
t = np.concatenate(T); f = np.concatenate(F); s = np.concatenate(S); o_ = np.argsort(t); t, f, s = t[o_], f[o_], s[o_]
fl = flatten(t, f, method="biweight", window_length=0.75, break_tolerance=0.5); ok = np.isfinite(fl); t, fl, s = t[ok], fl[ok], s[ok]
mad = 1.4826 * np.median(np.abs(fl - np.median(fl))); ok = fl < 1 + 4 * mad; t, fl, s = t[ok], fl[ok], s[ok]
per = np.linspace(P0 * (1 - 1e-3), P0 * (1 + 1e-3), 4001)
pw = BoxLeastSquares(t, fl).power(per, [0.75 * dur, dur, 1.25 * dur], objective="likelihood"); i = np.argmax(pw.power)
P, T0, dd = pw.period[i], pw.transit_time[i], pw.duration[i]
x = (((t - T0) / P + 0.5) % 1 - 0.5) * P
def dep(m, xx=x):
    a = m & (np.abs(xx) < dd / 2); b = m & (np.abs(xx) > dd) & (np.abs(xx) < 0.5)
    return ((np.median(fl[b]) - np.mean(fl[a])) * 1e6, np.std(fl[b]) / np.sqrt(a.sum()) * 1e6, int(a.sum())) if a.sum() >= 3 else (np.nan, np.nan, 0)
print(f"TIC {tic}: TARS sectors {sorted(set(s.astype(int)))}; refined P = {P:.6f} d (TGLC {P0:.6f}), T0 = {T0:.4f}, dur {dd*24:.1f} h")
D = [(sec, *dep(s == sec)) for sec in sorted(set(s.astype(int)))]
for sec, a, e, n in D: print(f"   sector {sec:3d}: {a:8.0f} ± {e:5.0f} ppm (n_in {n})")
v = np.array([(a, e) for _, a, e, n in D if n >= 3]); w = 1 / v[:, 1] ** 2; mu = (v[:, 0] * w).sum() / w.sum()
chi = ((v[:, 0] - mu) ** 2 * w).sum() / max(len(v) - 1, 1); nsig = mu / w.sum() ** -0.5
n = np.round((t - T0) / P); od, ev = dep(n % 2 == 1), dep(n % 2 == 0)
xs = (((t - T0) / P) % 1 - 0.5) * P; sc = dep(np.ones(t.size, bool), xs)
print(f"   weighted depth {mu:.0f} ppm ({nsig:.1f} sigma), per-sector chi2/dof {chi:.2f}; odd {od[0]:.0f}±{od[1]:.0f}, even {ev[0]:.0f}±{ev[1]:.0f} "
      f"({abs(od[0]-ev[0])/np.hypot(od[1],ev[1]):.1f} sigma); secondary {sc[0]:.0f}±{sc[1]:.0f}")
fig, ax = plt.subplots(figsize=(7, 3.5)); bb = np.linspace(-3 * dd * 24, 3 * dd * 24, 49); ii = np.digitize(x * 24, bb)
ax.plot(bb[:-1], [np.mean(fl[ii == k] - 1) * 1e3 if (ii == k).sum() > 3 else np.nan for k in range(1, 49)], "k.-")
ax.set_title(f"TIC {tic} TARS fold P={P:.5f} d"); ax.set_xlabel("hours"); ax.set_ylabel("ppt"); plt.tight_layout(); plt.savefig(f"results/tars_{tic}.png", dpi=90)
