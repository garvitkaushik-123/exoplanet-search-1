"""Faint-star (Tmag 13.5-15.5) search on TGLC PSF light curves (sectors 1-12, 30-min FFIs).

Per star:
  download TGLC files (direct MAST URLs), use cal_psf_flux with TESS_flags == 0 and TGLC_flags == 0
  -> per-sector normalisation, orbit-edge trim, rotation prewhitening and biweight (duo_search.prepare)
  -> (a) periodic: astropy BLS, P = 0.5-13 d, durations 1-6 h  (hot / warm giants, >= 2 transits)
     (b) single events: duo_search.box_events (v1.2 rules)
  -> automatic vetting of the BLS peak: SNR >= 10, SDE >= 9, >= 2 transits with data, depth 0.3-5 %,
     odd/even < 3 sigma, secondary < 3 sigma, duration consistent with the stellar density (0.2-1.5 x max).
Faint stars have more red noise and blending, so the thresholds are stricter than for the bright samples.

Usage: python tglc_search.py <shard> <nshard>
"""
import io, os, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, requests
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares
import duo_search as D

warnings.filterwarnings("ignore")
VERSION = "tglc-v1.0"
CACHE = "data/tglclc"
URL = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
MAN = pd.read_csv("data/tglc_manifest.csv")


def _fetch(uri):
    for i in range(5):
        try:
            r = requests.get(URL + uri, timeout=120); r.raise_for_status(); return r.content
        except Exception:
            if i == 4: raise
            time.sleep(2 ** (i + 1))


def get_lc(tic):
    out = f"{CACHE}/{tic}.npz"
    if os.path.exists(out): return dict(np.load(out))
    os.makedirs(CACHE, exist_ok=True)
    m = MAN[MAN.tid == tic]
    with ThreadPoolExecutor(4) as ex: blobs = list(ex.map(_fetch, m.uri))
    T, F, S = [], [], []
    for b, sec in zip(blobs, m.sector):
        with fits.open(io.BytesIO(b)) as h:
            d = h[1].data; n = [c.lower() for c in d.columns.names]
            g = lambda c: np.array(d[d.columns.names[n.index(c)]], float)
            t, f = g("time"), g("cal_psf_flux")
            ok = np.isfinite(t) & np.isfinite(f) & (f > 0)
            if "tess_flags" in n: ok &= g("tess_flags") == 0
            if "tglc_flags" in n: ok &= g("tglc_flags") == 0
            if ok.sum() < 100: continue
            T.append(t[ok]); F.append(f[ok] / np.nanmedian(f[ok])); S.append(np.full(ok.sum(), sec))
    if not T: raise ValueError("no usable TGLC data")
    o = np.argsort(np.concatenate(T))
    res = dict(t=np.concatenate(T)[o], f=np.concatenate(F)[o], sector=np.concatenate(S)[o])
    np.savez_compressed(out, **res); return res


def search_star(row):
    tic = int(row.tid); R = float(row.rad); M = float(row["mass"]) if row["mass"] == row["mass"] else R
    d = get_lc(tic)
    t, f, sec = D.prepare(d["t"], d["f"], d["sector"])
    if t.size < 300: raise ValueError("too few points after cleaning")
    rms = 1.4826 * np.median(np.abs(f - np.median(f)))
    out = []
    # (a) periodic BLS
    base = t.max() - t.min(); pmax = min(13.0, base / 2)
    durs = np.array([1, 1.5, 2, 3, 4, 6]) / 24
    per = np.exp(np.arange(np.log(0.5), np.log(pmax), durs.min() / (3 * base)))
    bls = BoxLeastSquares(t, f); pw = bls.power(per, durs, objective="snr")
    p = pw.power; tr = pd.Series(p).rolling(501, center=True, min_periods=25).median().values; resid = p - tr
    i = int(np.nanargmax(resid)); sde = (resid[i] - np.nanmean(resid)) / np.nanstd(resid)
    P, T0, dur, dep = pw.period[i], pw.transit_time[i], pw.duration[i], pw.depth[i]
    st = bls.compute_stats(P, dur, T0)
    ph = ((t - T0) / P + 0.5) % 1 - 0.5; inn = np.abs(ph * P) < dur / 2
    snr = dep / (np.std(f[~inn]) / np.sqrt(max(inn.sum(), 1)))
    ntr = int(np.sum(np.array(st["per_transit_count"]) > 0))
    do, de = st["depth_odd"], st["depth_even"]
    oe = abs(do[0] - de[0]) / np.hypot(do[1], de[1]) if (do[1] > 0 and de[1] > 0) else np.nan
    sd = st["depth_phased"]; sec_sig = sd[0] / sd[1] if sd[1] > 0 else np.nan
    t14 = D.t14_max(P, R, M, k=np.sqrt(max(dep, 1e-6)))
    flags = dict(snr_ok=snr >= 10, sde_ok=sde >= 9, ntr_ok=ntr >= 2, depth_ok=0.003 <= dep <= 0.05,
                 oddeven_ok=(oe == oe) and oe < 3, secondary_ok=(sec_sig != sec_sig) or sec_sig < 3,
                 density_ok=0.2 < dur / t14 < 1.5,
                 not_orbit_sys=min(abs(P - 13.7 * m) for m in (0.5, 1)) > 0.3)
    out.append(dict(tic=tic, kind="bls", version=VERSION, tmag=row.Tmag, teff=row.Teff, rad=R, rms_ppm=rms * 1e6,
                    n_sectors=int(len(np.unique(sec))), period=P, t0=T0, dur_h=dur * 24, depth_ppm=dep * 1e6,
                    rp_earth=np.sqrt(max(dep, 0)) * R * 109.1, snr=snr, sde=sde, n_transits=ntr, oddeven_sig=oe,
                    sec_sig=sec_sig, dur_over_t14max=dur / t14, **{f"f_{k}": bool(v) for k, v in flags.items()},
                    passed=bool(all(flags.values()))))
    # (b) single events
    dmax = min(12 / 24, 1.1 * D.t14_max(1000, R, M))
    for e in D.box_events(t, f, sec, [x / 24 for x in (1, 2, 3, 4, 6, 9, 12) if x / 24 <= dmax] or [1 / 24], snr_min=8.0):
        if e["edge_d"] > 0.25:
            out.append(dict(tic=tic, kind="single", version=VERSION, tmag=row.Tmag, teff=row.Teff, rad=R, **e))
    return out


if __name__ == "__main__":
    shard, nshard = int(sys.argv[1]), int(sys.argv[2])
    tg = pd.read_csv("data/tglc_targets.csv").sort_values("tid").iloc[shard::nshard]
    outf = f"results/tglc_{shard}.csv"
    rows = pd.read_csv(outf).to_dict("records") if os.path.exists(outf) else []
    done = {r["tic"] for r in rows}
    for _, r in tg.iterrows():
        if int(r.tid) in done: continue
        s = time.time()
        try:
            res = search_star(r); rows += res
            b = res[0]
            print(f"{r.tid} P={b['period']:.4f} SNR={b['snr']:.1f} SDE={b['sde']:.1f} depth={b['depth_ppm']:.0f} "
                  f"singles={len(res)-1} {'PASS' if b['passed'] else ''} ({time.time()-s:.1f}s)", flush=True)
        except Exception as e:
            print("skip", r.tid, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
            rows.append(dict(tic=int(r.tid), kind="error", version=VERSION, error=str(e)[:200]))
        pd.DataFrame(rows).to_csv(outf, index=False)
