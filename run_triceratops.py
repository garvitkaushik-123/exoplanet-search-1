"""TRICERATOPS statistical validation for TIC 308184057, adapted to this sandbox's network.

Two adaptations (the method is unchanged):
  1. triceratops resolves the star name through mastresolver (HTTP), which does not resolve here, so
     Catalogs.query_object is replaced by a coordinate cone query on the same TIC catalogue.
  2. Its field-star population comes from a Gaia DR3 TAP query (gea.esac.esa.int is blocked here). Gaia
     launch_job is replaced by the same cone from the TIC (MAST), which carries Gaia DR2 G/BP/RP and
     parallax. triceratops then derives Teff, mass, radius and magnitudes exactly as for DR3.
Light curve: TARS 200-s FFI photometry, sectors 62-90 (results/tic308184057_tars.npz), folded at the
refined ephemeris. Apertures: 3x3 pixels around the target in each sector.
Sanity gate (eumemic's TRICERATOPS setup bug): FPP from independent subsets and seeds must agree within
a factor of a few; otherwise the number is not reported as a result.
Usage: python run_triceratops.py [N]"""
import sys, warnings, numpy as np, pandas as pd
from astropy.table import Table
from astroquery.mast import Catalogs
warnings.filterwarnings("ignore")
TIC, RA, DEC = 308184057, 130.410329720449, -68.9673754253933
P, T0 = 6.119015, 1356.2511
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000

_orig = Catalogs.query_object
def _query_object(name, radius=None, catalog=None, **kw):
    return Catalogs.query_region(f"{RA} {DEC}", radius=radius, catalog=catalog)
Catalogs.query_object = _query_object

from astroquery.gaia import Gaia
class _Job:
    def __init__(self, tbl): self.tbl = tbl
    def get_results(self): return self.tbl
def _gaia_from_tic(adql, verbose=False, **kw):
    import re
    ra, dec, rad, mlim = map(float, re.search(r"CIRCLE\('ICRS', ([-\d.]+), ([-\d.]+), ([-\d.]+)\)\) AND phot_g_mean_mag < ([\d.]+)", adql).groups())
    df = Catalogs.query_region(f"{ra} {dec}", radius=rad, catalog="TIC").to_pandas()
    df = df[(df.GAIAmag < mlim) & df.gaiabp.notna() & df.gaiarp.notna()]
    t = Table({"phot_g_mean_mag": df.GAIAmag.values, "phot_bp_mean_mag": df.gaiabp.values,
               "phot_rp_mean_mag": df.gaiarp.values, "parallax": df.plx.values,
               "parallax_over_error": (df.plx / df.e_plx).values})
    print(f"   [field population from TIC/Gaia DR2: {len(t)} stars within {rad*60:.1f}']")
    return _Job(t)
Gaia.launch_job = _gaia_from_tic; Gaia.launch_job_async = _gaia_from_tic

import lightkurve
from astroquery.mast import Tesscut
class _Cut:
    def __init__(self, hdu): self.hdu = hdu
class _Search:
    def __init__(self, coord, sector): self.coord, self.sector = coord, sector
    def download_all(self, cutout_size=(10, 10), **kw):
        # 3. lightkurve.search_tesscut resolves coordinates through mastresolver (unreachable); the same
        #    TESScut service is called directly through astroquery instead
        hs = Tesscut.get_cutouts(coordinates=self.coord, size=cutout_size[0], sector=self.sector)
        for h in hs:
            # 4. current astrocut cutouts no longer carry the physical-pixel offsets 1CRV4P/2CRV4P. triceratops
            #    only uses them to put stars and apertures in one pixel frame; our apertures are built from
            #    its own pix_coords, so a zero offset leaves all relative geometry unchanged.
            for k in ("1CRV4P", "2CRV4P"):
                if k not in h[1].header: h[1].header[k] = 0
        return [_Cut(h) for h in hs]
lightkurve.search_tesscut = lambda target=None, sector=None, **kw: _Search(target, sector)

import triceratops.triceratops as tr
tr.lightkurve.search_tesscut = lightkurve.search_tesscut

d = np.load("results/tic308184057_tars.npz"); t, f, s = d["t"], d["f"], d["s"]

def run(sectors, seed, n=N):
    np.random.seed(seed)
    m = np.isin(s, sectors)
    x = (((t[m] - T0) / P + 0.5) % 1 - 0.5) * P
    w = np.abs(x) < 0.25
    oot = (np.abs(x) > 0.1) & w
    err = np.std(f[m][oot])
    dep = np.median(f[m][oot]) - np.mean(f[m][np.abs(x) < 0.03])
    tg = tr.target(ID=TIC, sectors=np.array(sorted(set(sectors))), search_radius=10, ra=RA, dec=DEC,
                   background_population_source="gaia")
    aps = []
    for k in range(len(tg.sectors)):
        c0, r0 = tg.pix_coords[k][0] if hasattr(tg, "pix_coords") else (None, None)
        cc, rr = int(round(c0)), int(round(r0))
        aps.append(np.array([[cc + i, rr + j] for i in (-1, 0, 1) for j in (-1, 0, 1)]))
    tg.calc_depths(tdepth=dep, all_ap_pixels=aps)
    tg.calc_probs(time=x[w], flux_0=f[m][w], flux_err_0=err, P_orb=P, N=n, exptime=200 / 86400, verbose=0)
    return tg, dep, err

if __name__ == "__main__":
    runs = [("all 200-s sectors", [62, 63, 64, 65, 69, 89, 90], 1),
            ("all, seed 2", [62, 63, 64, 65, 69, 89, 90], 2),
            ("2022 sectors 62-65", [62, 63, 64, 65], 3),
            ("2023-25 sectors 69,89,90", [69, 89, 90], 4)]
    rows = []
    for name, secs, seed in runs:
        print(f"== {name} (seed {seed}, N={N})", flush=True)
        try:
            tg, dep, err = run(secs, seed)
            rows.append(dict(run=name, depth_ppm=round(dep * 1e6), flux_err_ppm=round(err * 1e6), FPP=tg.FPP, NFPP=tg.NFPP))
            print(f"   depth {dep*1e6:.0f} ppm  FPP = {tg.FPP:.4g}  NFPP = {tg.NFPP:.4g}", flush=True)
            if seed == 1:
                tg.probs.to_csv("results/triceratops_TIC308184057_probs.csv", index=False)
                print(tg.probs.sort_values("prob", ascending=False).head(8)[["ID", "scenario", "prob"]].to_string(index=False))
        except Exception as e:
            import traceback; traceback.print_exc(limit=4); rows.append(dict(run=name, error=str(e)[:200]))
    r = pd.DataFrame(rows); r.to_csv("results/triceratops_TIC308184057.csv", index=False); print("\n", r.to_string(index=False))
