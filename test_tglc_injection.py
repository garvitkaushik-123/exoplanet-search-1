"""Injection-recovery + false-alarm test for tglc_search on REAL TGLC light curves.
For 30 random targets: run the search as-is (false-alarm check), then inject a giant-planet transit
(depth 0.5-1.5 %, P 1-8 d, duration from the star's density, b = 0.3) and require the BLS peak within 1% of P
with all vetting flags passed."""
import numpy as np, pandas as pd, batman, tglc_search as S
rng = np.random.default_rng(7)
import sys
NS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
tg = pd.read_csv("data/tglc_targets.csv").sample(NS, random_state=3)
G = 6.674e-11; rec = fa = n = 0; rows = []
for _, r in tg.iterrows():
    try:
        d = S.get_lc(int(r.tid))
    except Exception as e:
        continue
    base = S.search_star(r)[0]; fa += base["passed"]
    P = rng.uniform(1, 8); dep = rng.uniform(0.005, 0.015); M = r["mass"] if r["mass"] == r["mass"] else r.rad
    aR = (G * M * 1.989e30 * (P * 86400) ** 2 / (4 * np.pi ** 2)) ** (1 / 3) / (r.rad * 6.957e8)
    p = batman.TransitParams(); p.t0 = d["t"].min() + rng.uniform(0, P); p.per = P; p.rp = np.sqrt(dep); p.a = aR
    p.inc = np.degrees(np.arccos(0.3 / aR)); p.ecc = 0; p.w = 90; p.limb_dark = "quadratic"; p.u = [0.45, 0.2]
    f2 = d["f"] * batman.TransitModel(p, d["t"], supersample_factor=5, exp_time=30 / 1440).light_curve(p)
    orig = S.get_lc
    S.get_lc = lambda tic, _d=dict(t=d["t"], f=f2, sector=d["sector"]): _d
    try: inj = S.search_star(r)[0]
    finally: S.get_lc = orig
    ok = abs(inj["period"] - P) / P < 0.01 or abs(inj["period"] - 2 * P) / (2 * P) < 0.01 or abs(inj["period"] - P / 2) / (P / 2) < 0.01
    hit = ok and inj["passed"]; rec += hit; n += 1
    rows.append(dict(tic=int(r.tid), tmag=r.Tmag, rms=round(base["rms_ppm"]), P=round(P, 3), depth=round(dep * 1e6),
                     found=round(inj["period"], 3), snr=round(inj["snr"], 1), passed=inj["passed"], recovered=hit,
                     fails=[k for k, v in inj.items() if k.startswith("f_") and not v], base_pass=base["passed"],
                     inj_sde=inj["sde"], inj_ok_P=ok, inj_other_ok=all(v for k, v in inj.items() if k.startswith("f_") and k not in ("f_snr_ok", "f_sde_ok")),
                     base_snr=base["snr"], base_sde=base["sde"], base_other_ok=all(v for k, v in base.items() if k.startswith("f_") and k not in ("f_snr_ok", "f_sde_ok"))))
df = pd.DataFrame(rows); pd.set_option("display.width", 220); print(df.to_string(index=False))
df.to_csv("results/tglc_injection.csv", index=False)
print(f"\nRECOVERED {rec}/{n} injected giants; FALSE ALARMS (uninjected stars passing): {fa}/{n}")
