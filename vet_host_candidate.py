"""Deep vetting of one niche-1 signal: odd/even, secondary, momentum-dump phase, per-year and split-half
recovery, phase-shuffle false-alarm control, plot. Usage: python vet_host_candidate.py TIC PERIOD T0 DUR_H"""
import sys, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import search_hosts as S
from wotan import flatten
tic, P, T0, dur = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) / 24
h = pd.read_csv("data/hosts.csv"); row = h[h.tid == tic].iloc[0]; R = row.rad; M = row.mass if row.mass == row.mass else R
d = S.get_lc(tic); t, f, sec, dumps = d["t"], d["f"], d["sector"], d["dumps"]
km, _ = S.known_mask(t, tic); keep = ~km & S.edges_mask(t)
near = np.abs(t[:, None] - dumps[None, :]).min(1) < 1.5 / 24 if dumps.size else np.zeros(t.size, bool); keep &= ~near
t, f, sec = t[keep], f[keep], sec[keep]
fl = flatten(t, f, method="biweight", window_length=float(np.clip(3 * S.t14_max(15, R, M), 0.5, 1.5)), break_tolerance=0.5)
ok = np.isfinite(fl); t, fl, sec = t[ok], fl[ok], sec[ok]
mad = 1.4826 * np.median(np.abs(fl - np.median(fl))); ok = fl < 1 + 3 * mad; t, fl, sec = t[ok], fl[ok], sec[ok]
def meas(mask, phase0=0.0, T0_=T0):
    ph = (((t - T0_) / P - phase0 + 0.5) % 1 - 0.5) * P
    a = mask & (np.abs(ph) < dur / 2); b = mask & (np.abs(ph) > dur) & (np.abs(ph) < 4 * dur)
    if a.sum() < 5: return np.nan, np.nan, 0
    dep = np.median(fl[b]) - np.mean(fl[a]); err = np.std(fl[b]) / np.sqrt(a.sum()); return dep * 1e6, dep / err, int(a.sum())
allm = np.ones(t.size, bool); n = np.round((t - T0) / P)
print(f"TIC {tic}  P={P}  dur={dur*24:.2f} h  R*={R}  baseline={t.max()-t.min():.0f} d  sectors={len(np.unique(sec))}")
print("ALL        depth %.0f ppm  SNR %.1f  n_in %d" % meas(allm))
o, e = meas(n % 2 == 1), meas(n % 2 == 0); print(f"ODD  {o[0]:.0f} ppm SNR {o[1]:.1f} | EVEN {e[0]:.0f} ppm SNR {e[1]:.1f}")
print("SECONDARY  depth %.0f ppm  SNR %.1f" % meas(allm, 0.5)[:2])
half = np.median(t); print("1st half   depth %.0f ppm SNR %.1f" % meas(t < half)[:2], "| 2nd half depth %.0f ppm SNR %.1f" % meas(t >= half)[:2])
yr = np.floor((t - t.min()) / 365.25)
for y in np.unique(yr): print(f"  year {int(y)} (sectors {sorted(set(sec[yr==y]))[0]}-{sorted(set(sec[yr==y]))[-1]}): depth %.0f ppm SNR %.1f n_in %d" % meas(yr == y))
dph = ((dumps - T0) / P) % 1; w = dur / P
print(f"momentum dumps within transit phase: {np.mean(np.minimum(dph, 1-dph) < w):.3f} (random expectation {2*w:.3f}), n_dumps={dumps.size}")
rng = np.random.default_rng(0); snrs = np.array([meas(allm, rng.uniform(0.1, 0.9))[1] for _ in range(300)])
print(f"phase-shuffle control: SNR>= {meas(allm)[1]:.1f} in {np.mean(snrs >= meas(allm)[1])*100:.1f}% of 300 random phases (median {np.nanmedian(snrs):.1f}, std {np.nanstd(snrs):.2f})")
ph = (((t - T0) / P + 0.5) % 1 - 0.5) * P * 24
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
b = np.linspace(-12, 12, 97); i = np.digitize(ph, b) - 1; c = 0.5 * (b[1:] + b[:-1])
y = [np.mean(fl[i == k]) for k in range(96)]
ax[0].plot(ph, (fl - 1) * 1e6, ",", color="0.7"); ax[0].plot(c, (np.array(y) - 1) * 1e6, "r.-"); ax[0].set_xlim(-12, 12); ax[0].set_ylim(-600, 400)
ax[0].set_xlabel("hours from mid-transit"); ax[0].set_ylabel("ppm"); ax[0].set_title(f"TIC {tic}  P={P:.4f} d")
for par, col in ((0, "b"), (1, "g")):
    m = n % 2 == par; ii = np.digitize(ph[m], b) - 1; ax[1].plot(c, (np.array([np.mean(fl[m][ii == k]) for k in range(96)]) - 1) * 1e6, col + ".-", label=["even", "odd"][par])
ax[1].set_xlim(-6, 6); ax[1].legend(); ax[1].set_title("odd / even (binned)")
plt.tight_layout(); plt.savefig(f"results/vet_{tic}.png", dpi=110); print("plot ->", f"results/vet_{tic}.png")
