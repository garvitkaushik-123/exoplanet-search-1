"""Plot + checks for each shortlisted duo: raw and detrended flux around both events, data gaps near events,
duplicate check (TOI table, eumemic lists). Usage: python duo_vet.py  (reads results/duo_shortlist.csv)"""
import glob, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import duo_search as D

toi = set(pd.read_csv("data/known_planets.csv").tid.astype(int))   # TOIs + confirmed hosts (local copy)
ext = {}
for f in glob.glob("external/*.csv*"):
    d = pd.read_csv(f); c = "tic" if "tic" in d.columns else ("TIC" if "TIC" in d.columns else None)
    if c: ext[f.split("/")[-1]] = set(pd.to_numeric(d[c], errors="coerce").dropna().astype(int))
sl = pd.read_csv("results/duo_shortlist.csv").drop_duplicates(["tic", "tc", "tc2"])
for _, r in sl.iterrows():
    tic = int(r.tic); d = D.get_lc(tic); t, f, sec = d["t"], d["f"], d["sector"]; tt, ff, ss = D.prepare(t, f, sec)
    print(f"\n=== TIC {tic}  dt={r["dt"]:.2f} d  depth {r.depth_ppm:.0f} ppm  dur {r.dur_h:.0f} h  Rp {r.rp_earth:.1f} Re  "
          f"SNR {r.snr1:.1f}/{r.snr2:.1f}  aliases {r.aliases}")
    print("  TOI host:", tic in toi, "| in external lists:", [k for k, v in ext.items() if tic in v] or "none")
    fig, ax = plt.subplots(2, 2, figsize=(14, 7))
    for j, tc in enumerate((r.tc, r.tc2)):
        m = np.abs(t - tc) < 2.5; mm = np.abs(tt - tc) < 2.5
        gaps = np.diff(t[m]); big = gaps.max() * 24 if gaps.size else np.nan
        x = tt[mm] - tc; y = ff[mm]; inn = np.abs(x) < r.dur_h / 48
        oot = (np.abs(x) > r.dur_h / 24) & (np.abs(x) < 1.0)
        print(f"  event {j+1}: sector {int(sec[m][0]) if m.any() else '?'}  largest gap within +-2.5 d: {big:.1f} h  "
              f"in-transit pts {inn.sum()}  depth {(np.median(y[oot]) - np.mean(y[inn])) * 1e6:.0f} ppm")
        ax[0, j].plot(t[m] - tc, f[m], ".", ms=2, color="0.5"); ax[0, j].set_title(f"TIC {tic} raw QLP, event {j+1}")
        ax[1, j].plot(x * 24, (y - 1) * 1e6, ".", ms=2, color="0.6")
        b = np.arange(-60, 61, 1.0); i = np.digitize(x * 24, b)
        ax[1, j].plot(b[:-1] + 0.5, [(np.mean(y[i == k]) - 1) * 1e6 if (i == k).sum() > 1 else np.nan for k in range(1, len(b))], "r.-")
        ax[1, j].axvspan(-r.dur_h / 2, r.dur_h / 2, color="y", alpha=.2); ax[1, j].set_xlabel("hours from event")
        ax[1, j].set_ylim(-3 * r.depth_ppm, 1.5 * r.depth_ppm)
    plt.tight_layout(); plt.savefig(f"results/duo_vet_{tic}.png", dpi=90); plt.close()
