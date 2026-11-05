"""For each target: get FFI-based light curves (QLP / TESS-SPOC), skip stars already on SPOC 2-min list."""
import os, sys, json, warnings, numpy as np, pandas as pd, lightkurve as lk
from exosearch import prepare, search, vetting_flags
warnings.filterwarnings("ignore")

def load_qlp(ffi):
    """Download QLP FITS and read directly; flux column differs by sector (KSPSAP_FLUX old, SYS_RM_FLUX/DET_FLUX new)."""
    import os
    from astropy.io import fits
    from astroquery.mast import Observations
    ts, fs = [], []
    for uri in ffi.table["dataURI"]:
        path = os.path.join("data", "qlp", os.path.basename(str(uri)))
        if not os.path.exists(path):
            os.makedirs("data/qlp", exist_ok=True)
            Observations.download_file(str(uri), local_path=path)
        with fits.open(path) as h:
            d = h[1].data; names = d.columns.names
            col = next(c for c in ("KSPSAP_FLUX", "SYS_RM_FLUX", "DET_FLUX") if c in names)
            ok = (d["QUALITY"] == 0) & np.isfinite(d["TIME"]) & np.isfinite(d[col])
            if ok.sum() < 100: continue
            f = d[col][ok].astype(float); ts.append(d["TIME"][ok].astype(float)); fs.append(f / np.nanmedian(f))
    if not ts: raise ValueError("no usable QLP data")
    return lk.LightCurve(time=np.concatenate(ts), flux=np.concatenate(fs))

def process(row):
    tic = int(row["ID"]); q = f"TIC {tic}"
    res = lk.search_lightcurve(q, mission="TESS")
    if len(res) == 0 or "SPOC" in set(res.author): return None      # SPOC = already 2-min target
    ffi = res[[a == "QLP" for a in res.author]]                      # QLP: FFI light curves, one author -> no duplicate sectors
    if len(ffi) == 0: return None
    import re
    secs = np.array([int(re.search(r"_s0*(\d+)-", str(u)).group(1)) for u in ffi.table["dataURI"]])
    NEW = int(os.environ.get("MIN_SECTOR", 90))
    ffi = ffi[secs >= NEW]                                            # NEW data only: not yet searched by other pipelines/teams
    if len(ffi) == 0: return None
    ffi = ffi[np.argsort([int(re.search(r"_s0*(\d+)-", str(u)).group(1)) for u in ffi.table["dataURI"]])[::-1][:4]]   # latest 4
    lc = load_qlp(ffi)
    t, f, mad = prepare(lc)
    if (np.percentile(lc.flux.value, 95) - np.percentile(lc.flux.value, 5)) > 0.03 or mad > 0.004: return None   # too variable/noisy to search for shallow transits
    r = search(t, f, rstar=float(row["rad"]), mstar=float(row["mass"]) if row["mass"] == row["mass"] else 0.4)
    fl = vetting_flags(r, rms=mad)
    return dict(tic=tic, tmag=row["Tmag"], n_sectors=len(ffi), n_pts=len(t), rms_ppm=mad*1e6, period=r.period, sde=r.SDE, snr=r.snr,
                depth_ppm=(1-r.depth)*1e6, duration_d=r.duration, t0=r.T0, n_transits=r.distinct_transit_count,
                odd_even_sigma=r.odd_even_mismatch, **{f"flag_{k}": v for k, v in fl.items()})

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    targets = pd.read_csv(os.environ.get("TARGETS", "data/targets_wide_ffi.csv")); out = []
    shard, nshard = int(sys.argv[2]), int(sys.argv[3]); targets = targets.iloc[shard::nshard]
    import os
    prev = f"results/none/{shard}.csv"
    if os.path.exists(prev):
        out = pd.read_csv(prev).to_dict("records"); targets = targets[~targets.ID.isin([o["tic"] for o in out])]
    for _, row in targets.iterrows():
        if len(out) >= n: break
        try:
            d = process(row)
            if d: out.append(d); print(d["tic"], f"P={d['period']:.3f} SDE={d['sde']:.1f}", "PASS" if d["flag_pass"] else "", flush=True)
        except Exception as e:
            print("skip", row["ID"], type(e).__name__, e, file=sys.stderr)
        pd.DataFrame(out).to_csv(f"results/new_{shard}.csv", index=False)
