"""Publication figures for TIC 308184057 (docs/figures/)."""
import re, numpy as np, pandas as pd, batman, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 10, "axes.labelsize": 10, "figure.dpi": 150})
d = np.load("results/tic308184057_tars.npz"); t, f, s = d["t"], d["f"], d["s"]
ch = np.load("results/fit_308184057_posterior.npz")["chain"]; med = np.median(ch, 0)
T0, P, k, b, rho, q1, q2 = med[:7]
G = 6.674e-8; aR = (G * rho * (P * 86400) ** 2 / (3 * np.pi)) ** (1 / 3); inc = np.degrees(np.arccos(b / aR))
u1, u2 = 2 * np.sqrt(q1) * q2, np.sqrt(q1) * (1 - 2 * q2)
x = (((t - T0) / P + 0.5) % 1 - 0.5) * P
# Fig 1: phase-folded transit, all data, binned, with model
p = batman.TransitParams(); p.t0 = 0; p.per = P; p.rp = k; p.a = aR; p.inc = inc; p.ecc = 0; p.w = 90; p.limb_dark = "quadratic"; p.u = [u1, u2]
xm = np.linspace(-0.25, 0.25, 2000); mdl = batman.TransitModel(p, xm, supersample_factor=3, exp_time=200 / 86400).light_curve(p)
fig, ax = plt.subplots(2, 1, figsize=(6.5, 5.5), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
w = np.abs(x) < 0.25; ax[0].plot(x[w] * 24, (f[w] - 1) * 1e3, ".", ms=1, color="0.75", rasterized=True)
bb = np.linspace(-6, 6, 97); i = np.digitize(x * 24, bb); xc = 0.5 * (bb[1:] + bb[:-1])
yb = np.array([np.mean(f[i == j]) for j in range(1, 97)]); eb = np.array([np.std(f[i == j]) / np.sqrt((i == j).sum()) for j in range(1, 97)])
ax[0].errorbar(xc, (yb - 1) * 1e3, eb * 1e3, fmt="o", ms=3, color="k", label="TARS, 17 sectors, 7.5-min bins")
ax[0].plot(xm * 24, (mdl - 1) * 1e3, "r-", lw=1.5, label="median MCMC model"); ax[0].set_ylim(-20, 8); ax[0].set_ylabel("Relative flux (ppt)"); ax[0].legend(loc="lower left", fontsize=8)
ax[0].set_title(f"TIC 308184057: P = {P:.5f} d, Rp/R$_\\star$ = {k:.3f}")
mb = np.interp(xc / 24, xm, mdl); ax[1].errorbar(xc, (yb - mb) * 1e3, eb * 1e3, fmt="o", ms=3, color="k"); ax[1].axhline(0, color="r")
ax[1].set_xlabel("Hours from mid-transit"); ax[1].set_ylabel("Resid. (ppt)"); ax[1].set_xlim(-6, 6)
plt.tight_layout(); plt.savefig("docs/figures/fig1_fold_model.png"); plt.close()
# Fig 2: per-sector depths and odd/even/secondary
dd = 2.33 / 24
def dep(m, xx=x):
    a = m & (np.abs(xx) < dd / 2); o = m & (np.abs(xx) > dd) & (np.abs(xx) < 0.5)
    return ((np.median(f[o]) - np.mean(f[a])) * 1e6, np.std(f[o]) / np.sqrt(a.sum()) * 1e6) if a.sum() >= 3 else (np.nan, np.nan)
secs = sorted(set(s.astype(int))); D = np.array([dep(s == q) for q in secs]); yr = np.array([2018 + (q - 1) / 13.0 for q in secs])
n = np.round((t - T0) / P); od, ev = dep(n % 2 == 1), dep(n % 2 == 0); xs = (((t - T0) / P) % 1 - 0.5) * P; sc = dep(np.ones(t.size, bool), xs)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), gridspec_kw=dict(width_ratios=[2.2, 1]))
ax[0].errorbar(secs, D[:, 0], D[:, 1], fmt="o", color="k"); wm = np.average(D[:, 0], weights=D[:, 1] ** -2)
ax[0].axhline(wm, color="r", ls="--", label=f"weighted mean {wm:.0f} ppm"); ax[0].set_xlabel("TESS sector (2018 to 2025)"); ax[0].set_ylabel("Transit depth (ppm)"); ax[0].legend(fontsize=8)
ax[1].errorbar([0, 1, 2], [od[0], ev[0], sc[0]], [od[1], ev[1], sc[1]], fmt="o", color="k"); ax[1].axhline(0, color="0.6", lw=0.8)
ax[1].set_xticks([0, 1, 2]); ax[1].set_xticklabels(["odd", "even", "phase 0.5"]); ax[1].set_ylabel("Depth (ppm)")
plt.tight_layout(); plt.savefig("docs/figures/fig2_depths_oddeven_secondary.png"); plt.close()
# Fig 3: difference-image centroid offsets per sector
L = open("results/diff_308184057.log").read()
r = re.findall(r"sector (\d+): \d+ in-transit cadences; offset \(([-+.\d]+),([-+.\d]+)\) px, noise \(([.\d]+),([.\d]+)\)", L)
nb = re.findall(r"sector (\d+):[^\n]*\n    TIC 308184061 Tmag 15.8 at \(([-+.\d]+),([-+.\d]+)\)", L)
fig, ax = plt.subplots(figsize=(4.6, 4.4))
for sec, dx, dy, sx, sy in r: ax.errorbar(float(dx), float(dy), xerr=float(sx), yerr=float(sy), fmt="o", color="k", ms=3, alpha=0.6, lw=0.8)
for sec, ex, ey in nb: ax.plot(float(ex), float(ey), "x", color="tab:orange", ms=6)
ax.plot(0, 0, "r*", ms=14, label="target"); ax.plot([], [], "x", color="tab:orange", label="TIC 308184061 (22\", per sector)")
ax.errorbar(-0.017, -0.195, xerr=0.114, yerr=0.121, fmt="s", color="tab:blue", ms=6, label="combined (16 sectors)")
ax.set_xlabel("Column offset (px)"); ax.set_ylabel("Row offset (px)"); ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5); ax.set_aspect("equal"); ax.legend(fontsize=7, loc="upper left")
ax.set_title("Difference-image centroid vs out-of-transit"); plt.tight_layout(); plt.savefig("docs/figures/fig3_diffimage_centroids.png"); plt.close()
print("figures written; weighted mean depth", round(wm), "odd", [round(v) for v in od], "even", [round(v) for v in ev], "secondary", [round(v) for v in sc])
