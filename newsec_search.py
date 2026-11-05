"""New-sector single / duo / multi-transit search on SPOC 2-min PDCSAP light curves.

Targets: data/newsec_targets.csv (select_newsec.py): non-host FGKM dwarfs observed in sectors 105-107 that also
have older 2-min data. SPOC's own TPS needs >= 2 transits, so single events in the newest sectors, and their
pairing with older events, are the least-searched part of these data.

Per star: S3 download of all 2-min sectors -> 10-min bins (cached npz, momentum dumps kept)
  -> duo_search.prepare (orbit-edge trim, rotation prewhitening, biweight) -> duo_search.box_events (v1.2 rules)
  -> events within 1.5 h of a momentum dump are dropped (2-min data tells us exactly when they happened)
  -> duos (different sectors, consistent depth/duration) with data-excluded period aliases.
Rows go to results/newsec_<shard>.csv in the same format as duo_search, so duo_common_mode.py can post-process
them (python duo_common_mode.py newsec).

Usage: python newsec_search.py <shard> <nshard>
"""
import io, os, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, requests
from astropy.io import fits
import duo_search as D

warnings.filterwarnings("ignore")
VERSION = "newsec-v1.0 (duo-v1.2 events)"
CACHE = "data/newseclc"
MAN = pd.read_csv("data/newsec_manifest.csv")
NEW = 105


def _fetch(url):
    for i in range(5):
        try:
            r = requests.get(url, timeout=120); r.raise_for_status(); return r.content
        except Exception:
            if i == 4: raise
            time.sleep(2 ** (i + 1))


def get_lc(tic, bin_min=10.0):
    out = f"{CACHE}/{tic}.npz"
    if os.path.exists(out):
        return dict(np.load(out))
    os.makedirs(CACHE, exist_ok=True)
    m = MAN[MAN.tid == tic]
    with ThreadPoolExecutor(8) as ex:
        blobs = list(ex.map(_fetch, m.url))
    T, F, S, DUMP = [], [], [], []
    for b in blobs:
        with fits.open(io.BytesIO(b)) as h:
            d, sec = h[1].data, h[0].header["SECTOR"]
            t, fl, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]
            DUMP.append(t[((q & 32) > 0) & np.isfinite(t)])
            ok = (q == 0) & np.isfinite(t) & np.isfinite(fl)
            if ok.sum() < 500: continue
            t, fl = t[ok], fl[ok] / np.nanmedian(fl[ok])
            nb = np.floor((t - t[0]) / (bin_min / 1440)).astype(int); cnt = np.bincount(nb); mm = cnt > 2
            T.append((np.bincount(nb, t) / np.maximum(cnt, 1))[mm]); F.append((np.bincount(nb, fl) / np.maximum(cnt, 1))[mm])
            S.append(np.full(mm.sum(), sec))
    if not T: raise ValueError("no usable SPOC data")
    o = np.argsort(np.concatenate(T))
    res = dict(t=np.concatenate(T)[o], f=np.concatenate(F)[o], sector=np.concatenate(S)[o],
               dumps=np.concatenate(DUMP) if DUMP else np.array([]))
    np.savez_compressed(out, **res)
    return res


def search_star(row):
    tic = int(row.tid); R = float(row.rad); M = float(row["mass"]) if row["mass"] == row["mass"] else R
    d = get_lc(tic)
    t, f, sec = D.prepare(d["t"], d["f"], d["sector"])
    dmax = min(12 / 24, 1.1 * D.t14_max(1000, R, M))
    durs = [x / 24 for x in (1, 1.5, 2, 3, 4, 6, 9, 12) if x / 24 <= dmax] or [1 / 24]
    ev = [e for e in D.box_events(t, f, sec, durs) if e["edge_d"] > 0.25]
    dumps = d["dumps"]
    if dumps.size:
        ev = [e for e in ev if np.min(np.abs(dumps - e["tc"])) > 1.5 / 24]
    base = dict(tic=tic, version=VERSION, tmag=row.Tmag, teff=row.Teff, rad=R,
                sectors=";".join(map(str, sorted(set(d["sector"].astype(int))))))
    out = [dict(base, kind="single", new_sector=e["sector"] >= NEW, **e) for e in ev]
    for i in range(len(ev)):
        for j in range(i + 1, len(ev)):
            a, b = ev[i], ev[j]
            if a["sector"] == b["sector"]: continue
            if not (0.5 < a["depth_ppm"] / b["depth_ppm"] < 2 and 0.67 < a["dur_h"] / b["dur_h"] < 1.5): continue
            al = D.aliases(t, f, a, b, R, M)
            out.append(dict(base, kind="duo", tc=a["tc"], tc2=b["tc"], dt=abs(b["tc"] - a["tc"]),
                            sector=a["sector"], sector2=b["sector"], new_sector=max(a["sector"], b["sector"]) >= NEW,
                            dur_h=0.5 * (a["dur_h"] + b["dur_h"]), depth_ppm=0.5 * (a["depth_ppm"] + b["depth_ppm"]),
                            snr=float(np.hypot(a["snr"], b["snr"])), snr1=a["snr"], snr2=b["snr"],
                            rp_earth=float(np.sqrt(0.5 * (a["depth_ppm"] + b["depth_ppm"]) / 1e6) * R * 109.1),
                            n_aliases=len(al), aliases=";".join(map(str, al[:40]))))
    return out


if __name__ == "__main__":
    shard, nshard = int(sys.argv[1]), int(sys.argv[2])
    tg = pd.read_csv("data/newsec_targets.csv").sort_values(["Tmag", "tid"]).iloc[shard::nshard]   # brightest first
    outf = f"results/newsec_{shard}.csv"
    rows = pd.read_csv(outf).to_dict("records") if os.path.exists(outf) else []
    done = {r["tic"] for r in rows}
    for _, r in tg.iterrows():
        if int(r.tid) in done: continue
        s = time.time()
        try:
            res = search_star(r)
            rows += res if res else [dict(tic=int(r.tid), kind="none", version=VERSION)]
            n1 = sum(x["kind"] == "single" for x in res); nnew = sum(x["kind"] == "single" and x["new_sector"] for x in res)
            duos = [x for x in res if x["kind"] == "duo"]
            print(f"{r.tid} events={n1} new={nnew} duos={len(duos)} "
                  + " ".join(f"DUO dt={x['dt']:.1f} depth={x['depth_ppm']:.0f} SNR={x['snr']:.1f} al={x['n_aliases']}" for x in duos)
                  + f" ({time.time()-s:.0f}s)", flush=True)
        except Exception as e:
            print("skip", r.tid, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
            rows.append(dict(tic=int(r.tid), kind="error", version=VERSION, error=str(e)[:200]))
        if len(rows) % 20 == 0 or True:
            pd.DataFrame(rows).to_csv(outf, index=False)
