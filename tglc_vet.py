"""Post-filter for tglc_search passers (search code stays frozen at tglc-v1.0).
1) odd/even depth measured directly (BLS compute_stats gave 0.0 for these light curves);
2) out-of-transit flatness: fold at P, bin the out-of-transit phases (20 bins) and require chi2/dof < 3.
   Contact binaries, pulsators and spotted stars fail this; a transiting planet's out-of-transit flux is flat.
3) the same test at 2P (EB with equal eclipses shows up as a non-flat 2P fold).
Usage: python tglc_vet.py  -> results/tglc_vetted.csv"""
import glob, numpy as np, pandas as pd, tglc_search as S, duo_search as D
g = pd.concat([pd.read_csv(f) for f in glob.glob("results/tglc_[0-9]*.csv")]); b = g[(g.kind == "bls") & (g.passed == True)]
rows = []
def depth(t, f, P, T0, dur, mask):
    x = (((t - T0) / P + 0.5) % 1 - 0.5) * P; a = mask & (np.abs(x) < dur / 2); o = mask & (np.abs(x) > dur) & (np.abs(x) < 3 * dur)
    if a.sum() < 3 or o.sum() < 10: return np.nan, np.nan
    return np.median(f[o]) - np.mean(f[a]), np.std(f[o]) / np.sqrt(a.sum())
def oot_chi2(t, f, P, T0, dur):
    x = (((t - T0) / P + 0.5) % 1 - 0.5) * P; o = np.abs(x) > dur
    ph = ((t[o] - T0) / P) % 1; bins = np.linspace(0, 1, 21); i = np.digitize(ph, bins) - 1
    m = np.array([f[o][i == k].mean() if (i == k).sum() > 3 else np.nan for k in range(20)])
    e = np.array([f[o][i == k].std() / np.sqrt((i == k).sum()) if (i == k).sum() > 3 else np.nan for k in range(20)])
    ok = np.isfinite(m) & (e > 0); mu = np.average(m[ok], weights=1 / e[ok] ** 2)
    return float(np.sum(((m[ok] - mu) / e[ok]) ** 2) / max(ok.sum() - 1, 1))
for _, r in b.iterrows():
    d = S.get_lc(int(r.tic)); t, f, sec = D.prepare(d["t"], d["f"], d["sector"])
    P, T0, dur = r.period, r.t0, r.dur_h / 24; n = np.round((t - T0) / P)
    do, eo = depth(t, f, P, T0, dur, n % 2 == 1); de, ee = depth(t, f, P, T0, dur, n % 2 == 0)
    oe = abs(do - de) / np.hypot(eo, ee) if eo == eo and ee == ee else np.nan
    c1, c2 = oot_chi2(t, f, P, T0, dur), oot_chi2(t, f, 2 * P, T0, dur)
    verdict = "pass" if (oe == oe and oe < 3 and c1 < 3 and c2 < 3) else "reject"
    rows.append(dict(tic=int(r.tic), period=r.period, depth_ppm=r.depth_ppm, odd_ppm=do * 1e6, even_ppm=de * 1e6,
                     oddeven_sig=oe, oot_chi2_P=c1, oot_chi2_2P=c2, verdict=verdict))
v = pd.DataFrame(rows); v.to_csv("results/tglc_vetted.csv", index=False); print(v.round(2).to_string(index=False))
