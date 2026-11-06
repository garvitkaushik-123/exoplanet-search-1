"""Stacked difference-image centroid test from TESScut FFI cutouts (for FFI-only stars).
Usage: python diff_tesscut_stack.py TIC PERIOD T0 DUR_H SECTOR [SECTOR ...]"""
import io, sys, zipfile, numpy as np, requests
from astropy.io import fits
from astropy.wcs import WCS
from astroquery.mast import Catalogs
tic, P, T0, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) / 24
secs = [int(x) for x in sys.argv[5:]]
s = Catalogs.query_criteria(catalog="Tic", ID=tic).to_pandas().iloc[0]
nb = Catalogs.query_region(f"{s.ra} {s.dec}", radius=1.5 / 60, catalog="Tic").to_pandas()
nb = nb[(nb.ID.astype(int) != tic) & (nb.Tmag < s.Tmag + 4)]
rng = np.random.default_rng(1); N = 13; res = []
def cen(img, box):
    v = np.where(box, np.clip(img, 0, None), 0); yy, xx = np.indices(img.shape); return (v * xx).sum() / v.sum(), (v * yy).sum() / v.sum()
for sec in secs:
    r = requests.get("https://mast.stsci.edu/tesscut/api/v0.1/astrocut", params=dict(ra=s.ra, dec=s.dec, y=N, x=N, sector=sec), timeout=900)
    if r.status_code != 200: print("sector", sec, "cutout failed", r.status_code); continue
    z = zipfile.ZipFile(io.BytesIO(r.content))
    with fits.open(io.BytesIO(z.read(z.namelist()[0]))) as h:
        d = h[1].data; w = WCS(h[2].header); t, F, q = d["TIME"], d["FLUX"], d["QUALITY"]
    ok = np.isfinite(t) & (q == 0) & np.isfinite(F).all(axis=(1, 2)); t, F = t[ok], F[ok]
    F = F - np.median(F, axis=(1, 2), keepdims=True) * 0      # keep raw; background already subtracted in TESScut
    def dimg(sh):
        x = (((t - T0) / P + sh + 0.5) % 1 - 0.5) * P
        a = np.abs(x) < 0.35 * dur; b = (np.abs(x) > 0.75 * dur) & (np.abs(x) < 0.75 * dur + 0.25)
        return (np.median(F[b], 0) - np.median(F[a], 0), a.sum()) if a.sum() >= 3 and b.sum() >= 10 else None
    if not np.isfinite(F).all(): F = np.nan_to_num(F)
    D0 = dimg(0)
    if D0 is None: print("sector", sec, "no transits"); continue
    tx, ty = map(float, w.world_to_pixel_values(s.ra, s.dec)); yy, xx = np.indices(D0[0].shape)
    box = (np.abs(xx - tx) <= 2.5) & (np.abs(yy - ty) <= 2.5)
    cx, cy = cen(D0[0], box)
    if not (np.isfinite(cx) and np.isfinite(cy)): print("sector", sec, "centroid undefined (no positive difference flux)"); continue
    x0 = (((t - T0) / P + 0.5) % 1 - 0.5) * P; ox, oy = cen(np.median(F[np.abs(x0) > dur], 0), box)
    noise = [((c := cen(Dr[0], box))[0] - ox, c[1] - oy) for sh in rng.uniform(0.15, 0.85, 80) if (Dr := dimg(sh)) is not None]
    noise = np.array(noise); noise = noise[np.isfinite(noise).all(1)]; sx, sy = noise[:, 0].std(), noise[:, 1].std(); dx, dy = cx - ox, cy - oy
    px, py = w.world_to_pixel_values(nb.ra.values, nb.dec.values)
    print(f"sector {sec}: {D0[1]} in-transit cadences; offset ({dx:+.3f},{dy:+.3f}) px, noise ({sx:.3f},{sy:.3f}) -> {np.hypot(dx/sx, dy/sy):.1f} sigma from target")
    for k in np.argsort(np.hypot(px - tx, py - ty))[:4]:
        ex, ey = px[k] - tx, py[k] - ty
        print(f"    TIC {int(nb.ID.iloc[k])} Tmag {nb.Tmag.iloc[k]:.1f} at ({ex:+.2f},{ey:+.2f}) px: {np.hypot((dx-ex)/sx, (dy-ey)/sy):.1f} sigma")
    res.append((dx, dy, sx, sy))
if res:
    a = np.array(res); wx, wy = 1 / a[:, 2] ** 2, 1 / a[:, 3] ** 2
    mx, my = (a[:, 0] * wx).sum() / wx.sum(), (a[:, 1] * wy).sum() / wy.sum(); ex, ey = wx.sum() ** -0.5, wy.sum() ** -0.5
    print(f"COMBINED ({mx:+.3f} ± {ex:.3f}, {my:+.3f} ± {ey:.3f}) px = {np.hypot(mx/ex, my/ey):.1f} sigma from target")
