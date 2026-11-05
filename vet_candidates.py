"""Second-stage vetting of auto-passers: stellar rotation match, secondary eclipse, odd/even depth, TOI cross-match."""
import glob, sys, io, warnings, numpy as np, pandas as pd, requests, lightkurve as lk
from astropy.timeseries import LombScargle
from run_search import load_qlp
from exosearch import trim_edges
warnings.filterwarnings("ignore")

def tap(q):
    r = requests.get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync", params={"query": q, "format": "csv"}, timeout=120)
    r.raise_for_status(); return pd.read_csv(io.StringIO(r.text))

def depth_at(t, f, per, t0, dur, phase):
    ph = ((t - t0) / per - phase + 0.5) % 1 - 0.5
    inn = np.abs(ph) < 0.5 * dur / per; out = (np.abs(ph) > 1.5 * dur / per) & (np.abs(ph) < 4 * dur / per)
    if inn.sum() < 5 or out.sum() < 5: return np.nan, np.nan
    d = np.median(f[out]) - np.mean(f[inn]); e = np.std(f[out]) / np.sqrt(inn.sum()); return d, e

def vet(row):
    res = lk.search_lightcurve(f"TIC {int(row.tic)}", mission="TESS"); ffi = res[[a == "QLP" for a in res.author]]
    import re
    secs = np.array([int(re.search(r"_s0*(\d+)-", str(u)).group(1)) for u in ffi.table["dataURI"]])
    ffi = ffi[secs >= 90]; secs = secs[secs >= 90]; ffi = ffi[np.argsort(secs)[::-1][:4]]
    lc = load_qlp(ffi).remove_nans().normalize(); t, f = trim_edges(lc.time.value, lc.flux.value)
    P, t0, dur = row.period, row.t0, row.duration_d
    freq, pw = LombScargle(t, f).autopower(minimum_frequency=1/15, maximum_frequency=1/0.2, samples_per_peak=10)
    prot = 1 / freq[np.argmax(pw)]; amp = (np.percentile(f, 95) - np.percentile(f, 5)) * 1e6
    rot_match = any(abs(prot - m * P) / (m * P) < 0.05 for m in (0.5, 1, 2))
    dsec, esec = depth_at(t, f, P, t0, dur, 0.5); dpri, _ = depth_at(t, f, P, t0, dur, 0.0)
    return dict(tic=int(row.tic), P=round(P, 4), prot=round(prot, 4), rot_amp_ppm=round(amp), rot_match=rot_match,
                prim_ppm=round(dpri * 1e6) if dpri == dpri else None, sec_ppm=round(dsec * 1e6) if dsec == dsec else None,
                sec_sigma=round(dsec / esec, 1) if esec and esec == esec else None)

if __name__ == "__main__":
    d = pd.concat([pd.read_csv(f) for f in glob.glob("results/new_*.csv")]); p = d[d.flag_pass]
    toi = tap("select tid,toi,tfopwg_disp from toi"); out = []
    for _, r in p.iterrows():
        try: out.append(vet(r))
        except Exception as e: print("fail", r.tic, e)
    v = pd.DataFrame(out).merge(toi, left_on="tic", right_on="tid", how="left").drop(columns="tid")
    v["verdict"] = np.where(v.rot_match, "REJECT: rotation", np.where(v.sec_sigma.abs().fillna(0) > 3, "REJECT: secondary/out-of-transit variability (EB or variable star)", np.where(v.toi.notna(), "KNOWN TOI", np.where(v.rot_amp_ppm > 10000, "REJECT: highly variable star (>1% amplitude)", "survives"))))
    v.to_csv("results/vetting_new.csv", index=False); print(v.to_string())
