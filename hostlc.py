"""Download all SPOC 2-min PDCSAP sectors for a star, keep a compact 10-min binned copy, delete the FITS."""
import os, shutil, glob, warnings, numpy as np
from astropy.io import fits
from astroquery.mast import Observations
warnings.filterwarnings("ignore")
CACHE = "data/hostlc"

def momentum_dumps(q):            # TESS QUALITY bit 6 (32) = reaction-wheel desaturation, bit 8 (128) = manual exclude
    return (q & 32) > 0

def retry(fn, *a, tries=5, **k):
    import time
    for i in range(tries):
        try: return fn(*a, **k)
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 ** (i + 1))

def get_lc(tic, bin_min=10.0):
    out = f"{CACHE}/{tic}.npz"
    if os.path.exists(out): return dict(np.load(out))
    os.makedirs(CACHE, exist_ok=True); tmp = f"data/tmp_{tic}"
    obs = retry(Observations.query_criteria, obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
                                      target_name=str(tic), t_exptime=[100, 130])
    prods = Observations.filter_products(retry(Observations.get_product_list, obs), productSubGroupDescription="LC")
    retry(Observations.download_products, prods, download_dir=tmp, cache=False)
    T, F, S, DUMP = [], [], [], []
    for f in sorted(glob.glob(f"{tmp}/**/*lc.fits", recursive=True)):
        with fits.open(f) as h:
            d = h[1].data; sec = h[0].header["SECTOR"]
            t, fl, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]
            DUMP.append(t[momentum_dumps(q) & np.isfinite(t)])
            ok = (q == 0) & np.isfinite(t) & np.isfinite(fl)
            if ok.sum() < 500: continue
            t, fl = t[ok], fl[ok] / np.nanmedian(fl[ok])
            nb = np.floor((t - t[0]) / (bin_min / 1440)).astype(int)          # bin to 10 min
            cnt = np.bincount(nb); m = cnt > 2
            T.append((np.bincount(nb, t) / np.maximum(cnt, 1))[m]); F.append((np.bincount(nb, fl) / np.maximum(cnt, 1))[m])
            S.append(np.full(m.sum(), sec))
    shutil.rmtree(tmp, ignore_errors=True)
    if not T: raise ValueError("no SPOC data")
    o = np.argsort(np.concatenate(T))
    res = dict(t=np.concatenate(T)[o], f=np.concatenate(F)[o], sector=np.concatenate(S)[o], dumps=np.concatenate(DUMP))
    np.savez_compressed(out, **res); return res
