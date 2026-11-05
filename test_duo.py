"""Synthetic test: K dwarf (0.7 Rsun), 2 transits of a P=212.37 d, 2.8 Re planet, one in an early-sector-like
segment (30-min cadence) and one in a late one (200-s cadence), 1500 ppm/30-min red+white noise + spot trend."""
import numpy as np, batman
import duo_search as D
rng = np.random.default_rng(3)
def sector(t0, cad):
    t = np.concatenate([np.arange(t0, t0 + 12.5, cad), np.arange(t0 + 13.7, t0 + 26.5, cad)]); return t
t1, t2 = sector(1500.0, 30 / 1440), sector(3300.0, 200 / 86400)
t = np.concatenate([t1, t2]); sec = np.concatenate([np.full(t1.size, 10), np.full(t2.size, 95)])
noise = np.where(sec == 10, 400e-6, 1500e-6)
f = 1 + 4e-3 * np.sin(2 * np.pi * t / 7.3) + rng.normal(0, 1, t.size) * noise
f += np.convolve(rng.normal(0, 150e-6, t.size), np.ones(15) / 15, "same")               # red noise
T0 = 1506.2; P = (3310.4 - T0) / 8      # 8th transit lands inside the late sector
p = batman.TransitParams(); p.t0, p.per, p.rp, p.a, p.inc, p.ecc, p.w, p.limb_dark, p.u = T0, P, 0.0367, 155, 89.9, 0, 90, "quadratic", [0.4, 0.2]
f *= batman.TransitModel(p, t, supersample_factor=3, exp_time=0.01).light_curve(p)
true2 = T0 + round((3310 - T0) / P) * P; print("injected transits at", T0, round(true2, 2), "dt", round(true2 - T0, 2), "depth ~", round(0.0367**2 * 1e6), "ppm")
tt, ff, ss = D.prepare(t, f, sec)
durs = [x / 24 for x in (2, 3, 4, 6, 9, 12)]
ev = D.box_events(tt, ff, ss, durs); print("events:", [(round(e["tc"], 2), round(e["snr"], 1), round(e["depth_ppm"])) for e in ev])
hits = [e for e in ev if min(abs(e["tc"] - T0), abs(e["tc"] - true2)) < 0.2]
assert len(hits) == 2, "both transits must be found"
al = D.aliases(tt, ff, hits[0], hits[1], 0.7, 0.75)
print("n aliases", len(al), "true P allowed:", any(abs(a - P) < 0.5 for a in al))
assert any(abs(a - P) < 0.5 for a in al)
print("DUO TEST PASSED")
