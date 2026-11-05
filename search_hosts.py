"""Niche 1: search known planet/TOI hosts (many SPOC 2-min sectors) for ADDITIONAL transiting planets.

Pipeline per star:
  S3 download of every SPOC 2-min PDCSAP sector -> 10-min bins (cached npz, FITS never hit disk)
  -> mask every known TOI / confirmed-planet transit -> drop momentum dumps and segment edges
  -> wotan biweight (window scaled to the star) -> iterative BLS (0.5-30 d, up to 2 signals)
  -> automatic vetting flags (SNR, SDE, n_transits, odd/even, secondary, stellar density,
     aliases of known planets, TESS-orbit systematics, per-sector consistency, rotation).

Usage: python search_hosts.py <shard> <nshard> [max_stars]
"""
import io, os, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, requests
from astropy.io import fits
from astropy.timeseries import BoxLeastSquares, LombScargle
from wotan import flatten

warnings.filterwarnings("ignore")
CACHE = "data/hostlc"
G, RSUN, MSUN, DAY = 6.674e-11, 6.957e8, 1.989e30, 86400.0
VERSION = "hosts-v1.0"

MAN = pd.read_csv("data/host_manifest.csv")
KNOWN = pd.read_csv("data/known_planets.csv")


# ---------------------------------------------------------------- data
def _fetch(url):
    for i in range(5):
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            return r.content
        except Exception:
            if i == 4:
                raise
            time.sleep(2 ** (i + 1))


def get_lc(tic, bin_min=10.0):
    out = f"{CACHE}/{tic}.npz"
    if os.path.exists(out):
        return dict(np.load(out))
    os.makedirs(CACHE, exist_ok=True)
    urls = MAN[MAN.tid == tic].url.tolist()
    if not urls:
        raise ValueError("not in manifest")
    with ThreadPoolExecutor(8) as ex:
        blobs = list(ex.map(_fetch, urls))
    T, F, S, DUMP = [], [], [], []
    for b in blobs:
        with fits.open(io.BytesIO(b)) as h:
            d, sec = h[1].data, h[0].header["SECTOR"]
            t, fl, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]
            DUMP.append(t[((q & 32) > 0) & np.isfinite(t)])           # reaction-wheel desaturation events
            ok = (q == 0) & np.isfinite(t) & np.isfinite(fl)
            if ok.sum() < 500:
                continue
            t, fl = t[ok], fl[ok] / np.nanmedian(fl[ok])
            nb = np.floor((t - t[0]) / (bin_min / 1440)).astype(int)
            cnt = np.bincount(nb)
            m = cnt > 2
            T.append((np.bincount(nb, t) / np.maximum(cnt, 1))[m])
            F.append((np.bincount(nb, fl) / np.maximum(cnt, 1))[m])
            S.append(np.full(m.sum(), sec))
    if not T:
        raise ValueError("no usable SPOC data")
    o = np.argsort(np.concatenate(T))
    res = dict(t=np.concatenate(T)[o], f=np.concatenate(F)[o], sector=np.concatenate(S)[o],
               dumps=np.concatenate(DUMP) if DUMP else np.array([]))
    np.savez_compressed(out, **res)
    return res


# ---------------------------------------------------------------- physics helpers
def t14_max(P, R, M, k=0.03):
    """Max (central, circular) transit duration in days for period P [d], R [Rsun], M [Msun]."""
    a = (G * M * MSUN * (P * DAY) ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    x = min(1.0, (1 + k) * R * RSUN / a)
    return P / np.pi * np.arcsin(x)


def known_mask(t, tic):
    """True where the point is inside any known TOI / confirmed transit (window: 1x duration each side + 1 h)."""
    k = KNOWN[(KNOWN.tid == tic) & KNOWN.pl_orbper.notna() & KNOWN.pl_tranmid.notna()]
    m = np.zeros(t.size, bool)
    rows = []
    for _, r in k.iterrows():
        P, t0 = r.pl_orbper, r.pl_tranmid - 2457000.0
        dur = (r.dur_h if r.dur_h == r.dur_h and r.dur_h > 0 else 3.0) / 24
        ph = ((t - t0) / P + 0.5) % 1 - 0.5
        m |= np.abs(ph * P) < (dur + 1 / 24)
        rows.append(P)
    return m, sorted(set(np.round(rows, 4)))


def edges_mask(t, gap=0.5, trim=0.25):
    keep = np.ones(t.size, bool)
    idx = np.where(np.diff(t) > gap)[0] + 1
    for seg in np.split(np.arange(t.size), idx):
        if seg.size:
            keep[seg] = (t[seg] > t[seg][0] + trim) & (t[seg] < t[seg][-1] - trim)
    return keep


# ---------------------------------------------------------------- search
def search_star(row, pmin=0.5, pmax=30.0, n_iter=2):
    tic = int(row.tid)
    R = float(row.rad)
    M = float(row.mass) if "mass" in row and row.mass == row.mass else R  # main-sequence M~R fallback
    d = get_lc(tic)
    t, f, sec, dumps = d["t"], d["f"], d["sector"], d["dumps"]

    km, kper = known_mask(t, tic)
    keep = ~km & edges_mask(t)
    if dumps.size:
        near = np.abs(t[:, None] - dumps[None, :]).min(1) < 1.5 / 24 if t.size * dumps.size < 5e7 else np.zeros(t.size, bool)
        keep &= ~near
    t, f, sec = t[keep], f[keep], sec[keep]

    raw = f.copy()
    win = float(np.clip(3 * t14_max(15.0, R, M), 0.5, 1.5))
    flat = flatten(t, f, method="biweight", window_length=win, break_tolerance=0.5)
    ok = np.isfinite(flat)
    t, flat, sec, raw = t[ok], flat[ok], sec[ok], raw[ok]
    mad = 1.4826 * np.median(np.abs(flat - np.median(flat)))
    ok = flat < 1 + 3 * mad
    t, flat, sec, raw = t[ok], flat[ok], sec[ok], raw[ok]

    base = t.max() - t.min()
    dmax = min(0.5, 1.2 * t14_max(pmax, R, M))
    durs = np.unique(np.clip(np.array([1, 1.5, 2.5, 4, 6]) / 24, 0.03, dmax))
    ratio = durs.min() / (2.0 * base)
    periods = np.exp(np.arange(np.log(pmin), np.log(pmax), ratio))

    out = []
    tt, ff, ss = t.copy(), flat.copy(), sec.copy()
    for it in range(n_iter):
        bls = BoxLeastSquares(tt, ff)
        pw = bls.power(periods, durs, objective="snr")
        p = pw.power
        trend = pd.Series(p).rolling(2001, center=True, min_periods=50).median().values
        resid = p - trend
        i = int(np.nanargmax(resid))
        sde = (resid[i] - np.nanmean(resid)) / np.nanstd(resid)
        P, T0, dur, depth = pw.period[i], pw.transit_time[i], pw.duration[i], pw.depth[i]
        st = bls.compute_stats(P, dur, T0)
        ph = ((tt - T0) / P + 0.5) % 1 - 0.5
        intr = np.abs(ph * P) < dur / 2
        sig = np.std(ff[~intr])
        snr = depth / (sig / np.sqrt(max(intr.sum(), 1)))
        n_tr = int(np.sum(np.array(st["per_transit_count"]) > 0))
        do, de = st["depth_odd"], st["depth_even"]
        oe = abs(do[0] - de[0]) / np.hypot(do[1], de[1]) if do[1] > 0 and de[1] > 0 else 0.0
        sec_d = st["depth_phased"]                                     # (depth, err) at phase 0.5
        sec_sig = sec_d[0] / sec_d[1] if sec_d[1] > 0 else 0.0
        # per-sector depth consistency and how many sectors contribute
        sec_depths = []
        for s in np.unique(ss[intr]):
            a, b = intr & (ss == s), (~intr) & (ss == s)
            if a.sum() >= 3:
                sec_depths.append((s, np.median(ff[b]) - np.mean(ff[a]), np.std(ff[b]) / np.sqrt(a.sum())))
        sd = np.array([x[1] for x in sec_depths]) if sec_depths else np.array([0.0])
        se = np.array([x[2] for x in sec_depths]) if sec_depths else np.array([1.0])
        chi2r = float(np.sum(((sd - depth) / se) ** 2) / max(len(sd) - 1, 1))
        frac_top = float(np.max((sd / se) ** 2) / np.sum((sd / se) ** 2)) if np.sum((sd / se) ** 2) > 0 else 1.0
        # rotation (on raw, per-sector normalised flux)
        try:
            fr, pp = LombScargle(t, raw).autopower(minimum_frequency=1 / 15, maximum_frequency=1 / 0.2, samples_per_peak=5)
            prot = 1 / fr[np.argmax(pp)]
        except Exception:
            prot = np.nan
        t14 = t14_max(P, R, M, k=np.sqrt(max(depth, 1e-6)))
        alias = any((1 <= round(P / q) <= 5 and abs(P / q - round(P / q)) < 0.01) or
                    (1 <= round(q / P) <= 5 and abs(q / P - round(q / P)) < 0.01) for q in kper)
        flags = dict(
            snr_ok=snr >= 7.1, sde_ok=sde >= 9, ntr_ok=n_tr >= 3, oddeven_ok=oe < 3, secondary_ok=sec_sig < 3,
            density_ok=0.2 < dur / t14 < 1.5, depth_ok=0 < depth < 0.03, not_alias_known=not alias,
            not_orbit_sys=min(abs(P - 13.7 * m) for m in (0.5, 1, 2)) > 0.5,
            sectors_consistent=(chi2r < 3) and (len(sd) >= 2) and (frac_top < 0.6),
            not_rotation=not any(abs(prot - m * P) / (m * P) < 0.05 for m in (0.5, 1, 2)) if prot == prot else True,
        )
        rp = np.sqrt(max(depth, 0)) * R * 109.1
        out.append(dict(tic=tic, iter=it, version=VERSION, n_sectors=int(len(np.unique(sec))), baseline_d=round(base, 1),
                        n_known=len(kper), known_periods=";".join(map(str, kper)), period=P, t0=T0, dur_h=dur * 24,
                        depth_ppm=depth * 1e6, rp_earth=rp, snr=snr, sde=sde, n_transits=n_tr, oddeven_sig=oe,
                        sec_sig=sec_sig, dur_over_t14max=dur / t14, chi2r_sectors=chi2r, frac_top_sector=frac_top,
                        n_sectors_with_transit=len(sd), prot=prot, rms_ppm=sig * 1e6,
                        **{f"f_{k}": bool(v) for k, v in flags.items()}, passed=bool(all(flags.values()))))
        # mask this signal and look again
        m = np.abs((((tt - T0) / P + 0.5) % 1 - 0.5) * P) < dur
        tt, ff, ss = tt[~m], ff[~m], ss[~m]
        if not (snr >= 7.1 and sde >= 7):
            break
    return out


if __name__ == "__main__":
    shard, nshard = int(sys.argv[1]), int(sys.argv[2])
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    hosts = pd.read_csv("data/hosts.csv")
    hosts = hosts[hosts.tid.isin(MAN.tid)].iloc[:nmax].iloc[shard::nshard]
    outf = f"results/hosts_{shard}.csv"
    done = set(pd.read_csv(outf).tic) if os.path.exists(outf) else set()
    rows = pd.read_csv(outf).to_dict("records") if done else []
    for _, r in hosts.iterrows():
        if int(r.tid) in done:
            continue
        s = time.time()
        try:
            res = search_star(r)
            rows += res
            for x in res:
                print(f"{x['tic']} it{x['iter']} P={x['period']:.4f} SNR={x['snr']:.1f} SDE={x['sde']:.1f} "
                      f"Rp={x['rp_earth']:.2f} {'PASS' if x['passed'] else ''} ({time.time()-s:.0f}s)", flush=True)
        except Exception as e:
            print("skip", r.tid, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
            rows.append(dict(tic=int(r.tid), iter=-1, version=VERSION, error=str(e)[:200]))
        pd.DataFrame(rows).to_csv(outf, index=False)
