"""Niche 2: single- and duo-transit search on FFI-only K / early-M dwarfs (QLP light curves).

Per star:
  download every QLP sector (direct MAST URLs from data/duo_manifest.csv, cached as npz)
  -> per orbit segment: trim 0.5 d edges, biweight (1.5 d), clip upward outliers
  -> box matched filter over durations 2-12 h (capped by stellar density for P <= 1000 d),
     SNR measured against the RED-noise scatter of window means at that duration
  -> events: local maxima with SNR >= 7, depth 0.1-3 %, >= 4 points, not one-point outliers
  -> duos: event pairs in DIFFERENT sectors with consistent depth (x0.5-2) and duration (x0.67-1.5)
  -> for each duo: period aliases P = dt/n (P >= 10 d) not excluded by data at predicted times,
     and consistent with the stellar-density duration limit.
Common-mode (many stars dipping at once) is checked afterwards by duo_common_mode.py.

Usage: python duo_search.py <shard> <nshard>
"""
import io, os, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, requests
from astropy.io import fits
from wotan import flatten
from astropy.timeseries import LombScargle

warnings.filterwarnings("ignore")
VERSION = "duo-v1.1"   # v1.1: gap-edge trimming + in-window coverage check (v1.0 events sat on data gaps)
CACHE = "data/duolc"
URL = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
G, RSUN, MSUN, DAY = 6.674e-11, 6.957e8, 1.989e30, 86400.0
MAN = pd.read_csv("data/duo_manifest.csv") if os.path.exists("data/duo_manifest.csv") else None


def t14_max(P, R, M, k=0.05):
    a = (G * M * MSUN * (P * DAY) ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    return P / np.pi * np.arcsin(min(1.0, (1 + k) * R * RSUN / a))


def _fetch(uri):
    for i in range(5):
        try:
            r = requests.get(URL + uri, timeout=120); r.raise_for_status(); return r.content
        except Exception:
            if i == 4: raise
            time.sleep(2 ** (i + 1))


def get_lc(tic):
    out = f"{CACHE}/{tic}.npz"
    if os.path.exists(out):
        return dict(np.load(out))
    os.makedirs(CACHE, exist_ok=True)
    m = MAN[MAN.tid == tic]
    with ThreadPoolExecutor(6) as ex:
        blobs = list(ex.map(_fetch, m.uri))
    T, F, S = [], [], []
    for b, sec in zip(blobs, m.sector):
        with fits.open(io.BytesIO(b)) as h:
            d = h[1].data; names = d.columns.names
            col = next(c for c in ("KSPSAP_FLUX", "SYS_RM_FLUX", "DET_FLUX", "SAP_FLUX") if c in names)
            ok = (d["QUALITY"] == 0) & np.isfinite(d["TIME"]) & np.isfinite(d[col])
            if ok.sum() < 100: continue
            f = d[col][ok].astype(float)
            T.append(d["TIME"][ok].astype(float)); F.append(f / np.nanmedian(f)); S.append(np.full(ok.sum(), sec))
    if not T: raise ValueError("no usable QLP data")
    o = np.argsort(np.concatenate(T))
    res = dict(t=np.concatenate(T)[o], f=np.concatenate(F)[o], sector=np.concatenate(S)[o])
    np.savez_compressed(out, **res)
    return res


def segments(t, gap=0.5):
    idx = np.where(np.diff(t) > gap)[0] + 1
    return np.split(np.arange(t.size), idx)


def prewhiten(t, f, sec, nharm=3, pmin=0.3, pmax=12.0):
    """Per sector: if a Lomb-Scargle rotation peak is significant, subtract a 3-harmonic fit (spot modulation).
    A box transit of a few hours barely projects onto day-scale sinusoids, so transits survive."""
    f = f.copy()
    for s in np.unique(sec):
        m = sec == s
        if m.sum() < 200: continue
        ls = LombScargle(t[m], f[m], nterms=1)
        fr, pw = ls.autopower(minimum_frequency=1 / pmax, maximum_frequency=1 / pmin, samples_per_peak=5)
        if pw.max() < 0.1: continue
        model = LombScargle(t[m], f[m], nterms=nharm).model(t[m], fr[np.argmax(pw)])
        f[m] = f[m] / model * np.median(model)
    return f


def prepare(t, f, sec, trim=0.5):
    keep = np.zeros(t.size, bool)
    for s in segments(t):
        if s.size: keep[s] = (t[s] > t[s][0] + trim) & (t[s] < t[s][-1] - trim)
    t, f, sec = t[keep], f[keep], sec[keep]
    # also trim around SHORT gaps (> 1 h): post-gap thermal ramps mimic transits (TIC 70796793 in v1.0)
    g = np.where(np.diff(t) > 1 / 24)[0]
    bad = np.zeros(t.size, bool)
    for i in g:
        bad |= ((t >= t[i] - 0.1) & (t <= t[i])) | ((t >= t[i + 1]) & (t <= t[i + 1] + 0.3))
    t, f, sec = t[~bad], f[~bad], sec[~bad]
    f = prewhiten(t, f, sec)
    fl = flatten(t, f, method="biweight", window_length=1.5, break_tolerance=0.5)
    ok = np.isfinite(fl); t, fl, sec = t[ok], fl[ok], sec[ok]
    mad = 1.4826 * np.median(np.abs(fl - np.median(fl)))
    ok = fl < 1 + 4 * mad
    return t[ok], fl[ok], sec[ok]


def box_events(t, f, sec, durs, snr_min=7.0):
    """Red-noise box filter per segment; returns list of event dicts (one per local maximum)."""
    ev = []
    for s in segments(t):
        if s.size < 50: continue
        ts, fs = t[s], 1 - f[s]                       # positive = dimming
        cs = np.concatenate([[0], np.cumsum(fs)])
        parts = []
        for D in durs:
            centers = np.arange(ts[0] + D / 2, ts[-1] - D / 2, D / 4)
            if centers.size < 8: continue
            lo = np.searchsorted(ts, centers - D / 2); hi = np.searchsorted(ts, centers + D / 2)
            n = hi - lo; ok = n >= 4
            mean = np.where(ok, (cs[hi] - cs[lo]) / np.maximum(n, 1), np.nan)
            sig = 1.4826 * np.nanmedian(np.abs(mean - np.nanmedian(mean)))     # red-noise scatter at scale D
            snr = (mean - np.nanmedian(mean)) / sig if sig > 0 else np.zeros_like(mean)
            parts.append(pd.DataFrame(dict(tc=centers, dur=D, depth=mean, snr=snr, n=n)))
        if not parts: continue
        best = pd.concat(parts).dropna(subset=["snr"]).sort_values("snr", ascending=False)
        taken = []
        for r in best.itertuples():
            if r.snr < snr_min: break
            if any(abs(r.tc - x) < max(r.dur, 0.5) for x in taken): continue
            taken.append(r.tc)
            inn = np.abs(ts - r.tc) < r.dur / 2
            frac_low = np.mean(fs[inn] > r.depth / 2)
            win = ts[np.abs(ts - r.tc) < r.dur / 2 + 1 / 24]
            cad = np.median(np.diff(ts))
            coverage = inn.sum() * cad / r.dur
            maxgap = np.max(np.diff(win)) if win.size > 1 else 1.0
            if coverage < 0.7 or maxgap > 0.5 / 24: continue           # incomplete window or gap inside it
            ev.append(dict(tc=float(r.tc), dur_h=float(r.dur * 24), depth_ppm=float(r.depth * 1e6), snr=float(r.snr),
                           n_in=int(r.n), frac_low=float(frac_low), sector=int(sec[s][0]),
                           edge_d=float(min(r.tc - ts[0], ts[-1] - r.tc))))
            if len(taken) >= 5: break
    return [e for e in ev if 1000 <= e["depth_ppm"] <= 30000 and e["frac_low"] >= 0.5 and e["n_in"] >= 4]


def aliases(t, f, e1, e2, R, M, pmin=10.0):
    """Periods dt/n not excluded by data at predicted times, and duration-consistent."""
    dt = abs(e2["tc"] - e1["tc"]); D = 0.5 * (e1["dur_h"] + e2["dur_h"]) / 24; dep = 0.5 * (e1["depth_ppm"] + e2["depth_ppm"]) / 1e6
    t0 = min(e1["tc"], e2["tc"]); allowed = []
    sig = 1.4826 * np.median(np.abs(f - np.median(f)))
    for n in range(1, int(dt // pmin) + 1):
        P = dt / n
        if t14_max(P, R, M) < 0.7 * D: continue
        k = np.arange(np.floor((t.min() - t0) / P), np.ceil((t.max() - t0) / P) + 1)
        excluded = False
        for tc in t0 + k * P:
            if abs(tc - e1["tc"]) < D or abs(tc - e2["tc"]) < D: continue
            inn = np.abs(t - tc) < D / 2
            if inn.sum() >= 4:                                        # data exist at a predicted transit
                d = 1 - np.mean(f[inn]); err = sig / np.sqrt(inn.sum())
                if d < dep - 3 * err: excluded = True; break
        if not excluded: allowed.append(round(P, 4))
    return allowed


def search_star(row):
    tic = int(row.tid); R = float(row.rad); M = float(row["mass"]) if row["mass"] == row["mass"] else R
    d = get_lc(tic)
    t, f, sec = prepare(d["t"], d["f"], d["sector"])
    dmax = min(12 / 24, 1.1 * t14_max(1000, R, M)); durs = [x / 24 for x in (2, 3, 4, 6, 9, 12) if x / 24 <= dmax] or [2 / 24]
    ev = [e for e in box_events(t, f, sec, durs) if e["edge_d"] > 0.25]
    out = []
    for e in ev:
        out.append(dict(tic=tic, kind="single", version=VERSION, tmag=row.Tmag, teff=row.Teff, rad=R, **e,
                        sectors=";".join(map(str, sorted(set(d["sector"]))))))
    for i in range(len(ev)):
        for j in range(i + 1, len(ev)):
            a, b = ev[i], ev[j]
            if a["sector"] == b["sector"]: continue
            if not (0.5 < a["depth_ppm"] / b["depth_ppm"] < 2 and 0.67 < a["dur_h"] / b["dur_h"] < 1.5): continue
            al = aliases(t, f, a, b, R, M)
            out.append(dict(tic=tic, kind="duo", version=VERSION, tmag=row.Tmag, teff=row.Teff, rad=R,
                            tc=a["tc"], tc2=b["tc"], dt=abs(b["tc"] - a["tc"]), sector=a["sector"], sector2=b["sector"],
                            dur_h=0.5 * (a["dur_h"] + b["dur_h"]), depth_ppm=0.5 * (a["depth_ppm"] + b["depth_ppm"]),
                            snr=float(np.hypot(a["snr"], b["snr"])), snr1=a["snr"], snr2=b["snr"],
                            rp_earth=float(np.sqrt(0.5 * (a["depth_ppm"] + b["depth_ppm"]) / 1e6) * R * 109.1),
                            n_aliases=len(al), aliases=";".join(map(str, al[:40])),
                            sectors=";".join(map(str, sorted(set(d["sector"]))))))
    return out


if __name__ == "__main__":
    shard, nshard = int(sys.argv[1]), int(sys.argv[2])
    tg = pd.read_csv("data/duo_targets.csv").sort_values("tid").iloc[shard::nshard]
    outf = f"results/duo_{shard}.csv"
    rows = pd.read_csv(outf).to_dict("records") if os.path.exists(outf) else []
    done = {r["tic"] for r in rows}
    for _, r in tg.iterrows():
        if int(r.tid) in done: continue
        s = time.time()
        try:
            res = search_star(r)
            rows += res if res else [dict(tic=int(r.tid), kind="none", version=VERSION)]
            duos = [x for x in res if x["kind"] == "duo"]
            print(f"{r.tid} events={sum(x['kind']=='single' for x in res)} duos={len(duos)} "
                  + " ".join(f"DUO dt={x['dt']:.1f} d depth={x['depth_ppm']:.0f} SNR={x['snr']:.1f} aliases={x['n_aliases']}" for x in duos)
                  + f" ({time.time()-s:.0f}s)", flush=True)
        except Exception as e:
            print("skip", r.tid, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
            rows.append(dict(tic=int(r.tid), kind="error", version=VERSION, error=str(e)[:200]))
        pd.DataFrame(rows).to_csv(outf, index=False)
