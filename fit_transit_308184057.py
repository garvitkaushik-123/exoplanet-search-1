"""MCMC transit fit of TIC 308184057 on TARS FFI photometry (17 sectors, 2018-2025).
Free: T0 (reference epoch near mid-baseline), P, k = Rp/R*, b, rho* [g/cc], q1, q2 (Kipping LD), a baseline offset c,
and a jitter term per cadence group. Each cadence (30 min, 10 min, 200 s) is supersampled.
Outputs results/fit_308184057_posterior.npz and results/fit_308184057_summary.csv."""
import numpy as np, batman, emcee, pandas as pd
d = np.load("results/tic308184057_tars.npz"); t, f, s = d["t"], d["f"], d["s"]
P0, T00 = 6.119020, 3051.2200
n_mid = np.round((np.median(t) - T00) / P0); Tref0 = T00 + n_mid * P0
x = (((t - Tref0) / P0 + 0.5) % 1 - 0.5) * P0
w = np.abs(x) < 0.3; t, f, s = t[w], f[w], s[w]
cad = np.where(s <= 26, 30, np.where(s <= 55, 10, 200 / 60))           # minutes
groups = [(c, cad == c) for c in (30, 10, 200 / 60)]
models = {}
G = 6.674e-8
def lc(theta):
    T0, P, k, b, rho, q1, q2 = theta[:7]
    aR = (G * rho * (P * 86400) ** 2 / (3 * np.pi)) ** (1 / 3)
    if b >= aR: return None
    inc = np.degrees(np.arccos(b / aR)); u1, u2 = 2 * np.sqrt(q1) * q2, np.sqrt(q1) * (1 - 2 * q2)
    out = np.empty_like(f)
    for c, m in groups:
        p = batman.TransitParams(); p.t0 = T0; p.per = P; p.rp = k; p.a = aR; p.inc = inc; p.ecc = 0; p.w = 90
        p.limb_dark = "quadratic"; p.u = [u1, u2]
        key = c
        if key not in models:
            models[key] = batman.TransitModel(p, t[m], supersample_factor=max(1, int(c / 2)), exp_time=c / 1440)
        out[m] = models[key].light_curve(p)
    return out
def lnp(theta):
    T0, P, k, b, rho, q1, q2, j1, j2, j3, c = theta
    if abs(c) > 0.005: return -np.inf
    if not (0.02 < k < 0.4 and 0 <= b < 1 + k and 0.1 < rho < 20 and 0 < q1 < 1 and 0 < q2 < 1 and abs(P - P0) < 0.002
            and abs(T0 - Tref0) < 0.05 and all(-12 < j < -3 for j in (j1, j2, j3))): return -np.inf
    m = lc(theta)
    if m is None: return -np.inf
    m = m * (1 + c)
    ll = 0
    for (c, msk), j in zip(groups, (j1, j2, j3)):
        sig2 = np.exp(2 * j); r = f[msk] - m[msk]; ll += -0.5 * np.sum(r ** 2 / sig2 + np.log(2 * np.pi * sig2))
    return ll
p0 = np.array([Tref0, P0, 0.11, 0.6, 2.4, 0.4, 0.3, np.log(0.008), np.log(0.006), np.log(0.006), 0.0])
nw, nd = 40, len(p0)
pos = p0 + np.array([5e-4, 2e-6, 3e-3, 0.05, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 1e-4]) * np.random.default_rng(1).normal(size=(nw, nd))
pos[:, 3] = np.abs(pos[:, 3])
sam = emcee.EnsembleSampler(nw, nd, lnp)
sam.run_mcmc(pos, 6000, progress=False)
ch = sam.get_chain(discard=2000, thin=10, flat=True)
names = ["T0_BTJD", "P_d", "k=Rp/R*", "b", "rho_star_gcc", "q1", "q2", "lnjit30", "lnjit10", "lnjit200", "baseline_c"]
G2 = 6.674e-8
aR = (G2 * ch[:, 4] * (ch[:, 1] * 86400) ** 2 / (3 * np.pi)) ** (1 / 3)
inc = np.arccos(ch[:, 3] / aR)
T14 = ch[:, 1] / np.pi * np.arcsin(np.sqrt((1 + ch[:, 2]) ** 2 - ch[:, 3] ** 2) / (aR * np.sin(inc))) * 24
R, Rerr = 0.7307, 0.05
rp_RJ = ch[:, 2] * np.random.default_rng(2).normal(R, Rerr, len(ch)) * 9.731
der = {"a/R*": aR, "inc_deg": np.degrees(inc), "T14_h": T14, "depth_ppm(k^2)": ch[:, 2] ** 2 * 1e6, "Rp_RJ (R*=0.73±0.05)": rp_RJ}
rows = [(n, *np.percentile(ch[:, i], [16, 50, 84])) for i, n in enumerate(names)] + [(n, *np.percentile(v, [16, 50, 84])) for n, v in der.items()]
df = pd.DataFrame(rows, columns=["param", "p16", "p50", "p84"]); df["minus"] = df.p50 - df.p16; df["plus"] = df.p84 - df.p50
df.to_csv("results/fit_308184057_summary.csv", index=False)
np.savez("results/fit_308184057_posterior.npz", chain=ch, names=names)
print("acceptance", np.mean(sam.acceptance_fraction).round(3)); print(df[["param", "p50", "minus", "plus"]].to_string(index=False, float_format=lambda v: f"{v:.6g}"))
rho_tic = 0.68 * 1.989e33 / (4 / 3 * np.pi * (0.7307 * 6.957e10) ** 3)
print(f"TIC stellar density {rho_tic:.2f} g/cc (M=0.68, R=0.73) vs fitted {np.median(ch[:,4]):.2f} +{np.percentile(ch[:,4],84)-np.median(ch[:,4]):.2f}/-{np.median(ch[:,4])-np.percentile(ch[:,4],16):.2f}")
