"""Download TARS light curves of TIC 308184057 and detrend them with the transits MASKED (wotan biweight 0.75 d),
so the trend is not pulled down by the transit. Saves results/tic308184057_tars.npz (t, f, s, raw)."""
import io, numpy as np, requests, warnings
from astropy.io import fits
from astroquery.mast import Observations
from wotan import flatten, transit_mask
warnings.filterwarnings("ignore")
P, T0, T14 = 6.119020, 3051.2200, 2.33 / 24
o = Observations.query_criteria(target_name="308184057", provenance_name="TARS"); p = Observations.get_product_list(o)
T, F, S = [], [], []
for uri, fn in zip(p["dataURI"], p["productFilename"]):
    if not str(fn).endswith(".fits"): continue
    b = requests.get("https://mast.stsci.edu/api/v0.1/Download/file?uri=" + str(uri), timeout=180).content
    with fits.open(io.BytesIO(b)) as h:
        sec = h[0].header.get("SECTOR", -1); d = h[1].data; t = np.array(d["TIME"], float); f = np.array(d["FLUX"], float)
        ok = np.isfinite(t) & np.isfinite(f) & (f > 0); T.append(t[ok]); F.append(f[ok] / np.nanmedian(f[ok])); S.append(np.full(ok.sum(), sec))
t = np.concatenate(T); f = np.concatenate(F); s = np.concatenate(S); o_ = np.argsort(t); t, f, s = t[o_], f[o_], s[o_]
mask = transit_mask(time=t, period=P, duration=2.5 * T14, T0=T0)
fl = flatten(t, f, method="biweight", window_length=0.75, break_tolerance=0.5, mask=mask)
ok = np.isfinite(fl); t, fl, s, f = t[ok], fl[ok], s[ok], f[ok]
oot = ~transit_mask(time=t, period=P, duration=2.5 * T14, T0=T0)
mad = 1.4826 * np.median(np.abs(fl[oot] - np.median(fl[oot]))); ok = fl < 1 + 4 * mad
np.savez("results/tic308184057_tars.npz", t=t[ok], f=fl[ok], s=s[ok], raw=f[ok])
x = (((t[ok] - T0) / P + 0.5) % 1 - 0.5) * P; inn = np.abs(x) < T14 / 2.5; near = (np.abs(x) > T14) & (np.abs(x) < 0.3)
print(f"{ok.sum()} points; out-of-transit median near transit {(np.median(fl[ok][near])-1)*1e6:.0f} ppm; in-transit depth {(np.median(fl[ok][near])-np.mean(fl[ok][inn]))*1e6:.0f} ppm")
