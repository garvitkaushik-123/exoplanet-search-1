"""Difference-image centroid test with TESScut FFI cutouts.
in-transit mean image minus nearby out-of-transit mean image; compare the flux-weighted centroid of the
difference image (where the light was lost) with the target's pixel position and with neighbours.
Usage: python diff_image.py TIC RA DEC SECTOR TC DUR_H"""
import io, sys, zipfile, numpy as np, requests, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astroquery.mast import Catalogs
tic, ra, dec, sec, tc, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]) / 24
N = 15
r = requests.get("https://mast.stsci.edu/tesscut/api/v0.1/astrocut", params=dict(ra=ra, dec=dec, y=N, x=N, sector=sec), timeout=600)
r.raise_for_status()
z = zipfile.ZipFile(io.BytesIO(r.content)); name = z.namelist()[0]
with fits.open(io.BytesIO(z.read(name))) as h:
    d = h[1].data; w = WCS(h[2].header)
    t, flux, q = d["TIME"], d["FLUX"], d["QUALITY"]
ok = np.isfinite(t) & (q == 0) & np.isfinite(flux).all(axis=(1, 2))
t, flux = t[ok], flux[ok]
inn = np.abs(t - tc) < 0.35 * dur
oot = (np.abs(t - tc) > 0.75 * dur) & (np.abs(t - tc) < 0.75 * dur + 0.4)
print(f"sector {sec}: {inn.sum()} in-transit and {oot.sum()} out-of-transit cadences")
img_oot = np.median(flux[oot], 0); img_in = np.median(flux[inn], 0); diff = img_oot - img_in
tx, ty = map(float, w.world_to_pixel_values(ra, dec))
# centroid of positive difference in a 7x7 box around the brightest diff pixel near the target
yy, xx = np.mgrid[0:N, 0:N]
box = (np.abs(xx - tx) <= 3) & (np.abs(yy - ty) <= 3)
dpos = np.where(box, np.clip(diff, 0, None), 0)
cx, cy = (dpos * xx).sum() / dpos.sum(), (dpos * yy).sum() / dpos.sum()
ox, oy = (np.clip(img_oot, 0, None) * box * xx).sum() / (np.clip(img_oot, 0, None) * box).sum(), (np.clip(img_oot, 0, None) * box * yy).sum() / (np.clip(img_oot, 0, None) * box).sum()
# noise: scatter of difference images built at random out-of-transit times
rng = np.random.default_rng(0); offs = []
for _ in range(60):
    t0 = rng.uniform(t.min() + 1, t.max() - 1)
    if abs(t0 - tc) < 1: continue
    a = np.abs(t - t0) < 0.35 * dur; b = (np.abs(t - t0) > 0.75 * dur) & (np.abs(t - t0) < 0.75 * dur + 0.4)
    if a.sum() < 5 or b.sum() < 5: continue
    dd = np.median(flux[b], 0) - np.median(flux[a], 0); dp = np.where(box, np.clip(dd, 0, None), 0)
    if dp.sum() > 0: offs.append(np.hypot((dp * xx).sum() / dp.sum() - ox, (dp * yy).sum() / dp.sum() - oy))
off = np.hypot(cx - tx, cy - ty); off_oot = np.hypot(cx - ox, cy - oy)
print(f"target pixel ({tx:.2f},{ty:.2f}); out-of-transit centroid ({ox:.2f},{oy:.2f}); difference centroid ({cx:.2f},{cy:.2f})")
print(f"offset of loss from target: {off:.2f} px = {off*21:.0f} arcsec; from OOT centroid: {off_oot:.2f} px")
print(f"noise: median random-time centroid offset {np.median(offs):.2f} px (n={len(offs)}); diff peak S/N {diff[int(round(ty)),int(round(tx))]/np.std(diff[~box]):.1f}")
nb = Catalogs.query_region(f"{ra} {dec}", radius=4 / 60, catalog="Tic").to_pandas()
nb = nb[nb.Tmag < 16.5]; px, py = w.world_to_pixel_values(nb.ra.values, nb.dec.values)
dist = np.hypot(px - cx, py - cy); j = np.argsort(dist)[:3]
for k in j: print(f"   closest to loss: TIC {int(nb.ID.iloc[k])} Tmag {nb.Tmag.iloc[k]:.1f} at {dist[k]:.2f} px from difference centroid")
fig, ax = plt.subplots(1, 2, figsize=(10, 4.6))
for a, im, ttl in ((ax[0], img_oot, "out of transit"), (ax[1], diff, "difference (OOT - in)")):
    m = a.imshow(im, origin="lower", cmap="viridis"); plt.colorbar(m, ax=a, fraction=.046)
    a.scatter(px, py, s=18, facecolors="none", edgecolors="w", lw=.8); a.plot(tx, ty, "r+", ms=14, mew=2); a.plot(cx, cy, "cx", ms=10, mew=2)
    a.set_xlim(-.5, N - .5); a.set_ylim(-.5, N - .5); a.set_title(f"TIC {tic} s{sec}: {ttl}")
plt.tight_layout(); plt.savefig(f"results/diffimg_{tic}_s{sec}.png", dpi=100)
