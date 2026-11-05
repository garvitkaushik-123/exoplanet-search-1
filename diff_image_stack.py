"""Stacked difference-image centroid test on SPOC 2-min target pixel files (all transits in each sector).
Usage: python diff_image_stack.py TIC PERIOD T0 DUR_H
Reports, per sector and combined, the difference-image centroid offset from the target and from each
neighbour, with an uncertainty from difference images built at random (out-of-transit) phases."""
import io, sys, numpy as np, pandas as pd, requests, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astroquery.mast import Catalogs
tic, P, T0, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) / 24
import os
m = pd.read_csv(os.environ.get("MANIFEST", "data/host_manifest.csv")); urls = m[m.tid == tic].sort_values("sector")
s = Catalogs.query_criteria(catalog="Tic", ID=tic).to_pandas().iloc[0]
nb = Catalogs.query_region(f"{s.ra} {s.dec}", radius=2.5 / 60, catalog="Tic").to_pandas()
nb = nb[(nb.ID.astype(int) != tic) & (nb.Tmag < s.Tmag + 7.5)]
rng = np.random.default_rng(1)
def centroid(img, box):
    v = np.where(box, np.clip(img, 0, None), 0); yy, xx = np.indices(img.shape)
    return (v * xx).sum() / v.sum(), (v * yy).sum() / v.sum()
res = []
for _, u in urls.iterrows():
    url = u.url.replace("_lc.fits", "_tp.fits")
    r = requests.get(url, timeout=600)
    if r.status_code != 200: print("no TPF for sector", u.sector); continue
    with fits.open(io.BytesIO(r.content)) as h:
        d = h[1].data; w = WCS(h[2].header); ap = h[2].data
        t, F, q = d["TIME"], d["FLUX"], d["QUALITY"]
    ok = np.isfinite(t) & (q == 0) & np.isfinite(F).all(axis=(1, 2)); t, F = t[ok], F[ok]
    ph = ((t - T0) / P + 0.5) % 1 - 0.5; x = ph * P
    def dimg(shift):
        xs = (((t - T0) / P + shift + 0.5) % 1 - 0.5) * P
        a = np.abs(xs) < 0.35 * dur; b = (np.abs(xs) > 0.75 * dur) & (np.abs(xs) < 0.75 * dur + 0.3)
        if a.sum() < 10 or b.sum() < 30: return None
        return np.median(F[b], 0) - np.median(F[a], 0), a.sum()
    D = dimg(0.0)
    if D is None: print("sector", u.sector, "no transits covered"); continue
    diff, nin = D
    tx, ty = map(float, w.world_to_pixel_values(s.ra, s.dec))
    yy, xx = np.indices(diff.shape); box = (np.abs(xx - tx) <= 2.5) & (np.abs(yy - ty) <= 2.5)
    cx, cy = centroid(diff, box)
    oot = np.median(F[np.abs(x) > dur], 0); ox, oy = centroid(oot, box)
    noise = []
    if P < 0.5 * (t.max() - t.min()):
        shifts = rng.uniform(0.15, 0.85, 80)                   # short period: fake transits at other phases
    else:                                                      # long period / single event: other times in sector
        tc_here = T0 + np.round((np.median(t[np.abs(x) < dur]) - T0) / P) * P
        fake = rng.uniform(t.min() + 1, t.max() - 1, 200); fake = fake[np.abs(fake - tc_here) > 1.5][:80]
        shifts = (tc_here - fake) / P
    for sh in shifts:
        Dr = dimg(sh)
        if Dr is not None:
            c = centroid(Dr[0], box); noise.append((c[0] - ox, c[1] - oy))
    if len(noise) < 10: print("sector", u.sector, "too few noise samples"); continue
    noise = np.array(noise); sx, sy = noise[:, 0].std(), noise[:, 1].std()
    dx, dy = cx - ox, cy - oy
    px, py = w.world_to_pixel_values(nb.ra.values, nb.dec.values)
    sig = np.hypot(dx / sx, dy / sy)
    print(f"sector {int(u.sector)}: {nin} in-transit cadences; diff-centroid offset from OOT centroid "
          f"({dx:+.3f}, {dy:+.3f}) px  noise ({sx:.3f}, {sy:.3f}) px  -> {sig:.1f} sigma")
    for k in np.argsort(np.hypot(px - tx, py - ty))[:3]:
        ex, ey = px[k] - tx, py[k] - ty
        print(f"     neighbour TIC {int(nb.ID.iloc[k])} Tmag {nb.Tmag.iloc[k]:.1f} at ({ex:+.2f},{ey:+.2f}) px: "
              f"diff centroid is {np.hypot((dx-ex)/sx,(dy-ey)/sy):.1f} sigma from it")
    res.append((int(u.sector), dx, dy, sx, sy))
if res:
    a = np.array(res); wx, wy = 1 / a[:, 3] ** 2, 1 / a[:, 4] ** 2
    mx, my = (a[:, 1] * wx).sum() / wx.sum(), (a[:, 2] * wy).sum() / wy.sum(); ex, ey = 1 / np.sqrt(wx.sum()), 1 / np.sqrt(wy.sum())
    print(f"\nCOMBINED offset ({mx:+.3f} ± {ex:.3f}, {my:+.3f} ± {ey:.3f}) px = ({mx*21:+.1f}, {my*21:+.1f}) arcsec; "
          f"{np.hypot(mx/ex, my/ey):.1f} sigma from target")
