"""Post-process duo search: common-mode (many stars dipping at once) and shortlist of duo candidates.

An event is common-mode (rejected) if >= 3 OTHER stars have an event within +-0.15 d with a similar duration
(ratio 0.5-2): shared systematics look alike on many stars. Time coincidences without a duration match only set
the soft flag cm_soft. (v1.1 used +-0.3 d with any duration and dropped a real 2-h transit of TIC 355425863
because broad 6-12 h end-of-orbit ramps hit 6 other stars at the same time.)
Stars with >= 3 clean events: the largest subset of mutually consistent events that share one period (>= 10 d)
is reported as a multi-transit candidate (results/duo_multi.csv).
Shortlist rules for duos: both events SNR >= 7, combined SNR >= 10, >= 1 surviving period alias,
neither event common-mode, Rp < 22 R_earth (planet-sized, not a stellar eclipse)."""
import glob, sys, numpy as np, pandas as pd
PFX = sys.argv[1] if len(sys.argv) > 1 else "duo"      # "duo" (QLP FFI search) or "newsec" (new-sector 2-min search)

d = pd.concat([pd.read_csv(f) for f in glob.glob(f"results/{PFX}_[0-9]*.csv")], ignore_index=True)
stars = d.tic.nunique(); err = d[d.kind == "error"].tic.nunique()
s = d[d.kind == "single"].copy()
tc = s.tc.values; tic = s.tic.values
dur = s.dur_h.values
s["n_other_stars"] = [len(set(tic[(np.abs(tc - x) < 0.3)]) - {k}) for x, k in zip(tc, tic)]
s["n_other_match"] = [len(set(tic[(np.abs(tc - x) < 0.15) & (dur / h > 0.5) & (dur / h < 2)]) - {k})
                      for x, k, h in zip(tc, tic, dur)]
s["common_mode"] = s.n_other_match >= 3
s["cm_soft"] = (s.n_other_stars >= 3) & ~s.common_mode

def cm(t, k):
    m = (s.tic == k) & (np.abs(s.tc - t) < 0.01)
    return bool(s[m].common_mode.any()) if m.any() else False

u = d[d.kind == "duo"].copy()
u["cm1"] = [cm(a, k) for a, k in zip(u.tc, u.tic)]
u["cm2"] = [cm(b, k) for b, k in zip(u.tc2, u.tic)]
clean = s[~s.common_mode].groupby("tic").size()
u["n_clean_events"] = u.tic.map(clean).fillna(0).astype(int)
u["short"] = (u.n_clean_events == 2) & (u.snr1 >= 7) & (u.snr2 >= 7) & (u.snr >= 10) & (u.n_aliases >= 1) & ~u.cm1 & ~u.cm2 & (u.rp_earth < 22)
u.to_csv(f"results/{PFX}_all_pairs.csv", index=False)
sl = u[u.short].sort_values("snr", ascending=False)
sl.to_csv(f"results/{PFX}_shortlist.csv", index=False)

# multi-transit: largest subset (>= 3) of consistent clean events sharing one period >= 10 d
multi = []
for k, g in s[~s.common_mode].groupby("tic"):
    if len(g) < 3: continue
    T, Dp, Du, S = g.tc.values, g.depth_ppm.values, g.dur_h.values, g.sector.values
    best = None
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            if abs(T[j] - T[i]) < 10 or not (0.5 < Dp[i] / Dp[j] < 2 and 0.5 < Du[i] / Du[j] < 2): continue
            for n in range(1, int(abs(T[j] - T[i]) // 10) + 1):
                P = abs(T[j] - T[i]) / n
                ph = (T - T[i]) / P
                m = (np.abs(ph - np.round(ph)) * P < 0.1) & (Dp / Dp[i] > 0.5) & (Dp / Dp[i] < 2) & (Du / Du[i] > 0.5) & (Du / Du[i] < 2)
                if m.sum() >= 3 and (best is None or m.sum() > best[0] or (m.sum() == best[0] and P > best[1])):
                    e = np.round((T[m] - T[i]) / P); Pf = np.polyfit(e, T[m], 1)[0] if np.ptp(e) > 0 else P
                    best = (int(m.sum()), Pf, m)
    if best:
        n_ev, Pf, m = best
        multi.append(dict(tic=k, n_events=n_ev, P_max=round(Pf, 4), t0=round(float(T[m].min()), 3),
                          depth_ppm=round(float(np.median(Dp[m]))), dur_h=float(np.median(Du[m])),
                          snr_min=round(float(g.snr.values[m].min()), 1), sectors=";".join(str(int(x)) for x in S[m]),
                          event_times=";".join(f"{x:.3f}" for x in np.sort(T[m])), soft_cm=bool(g.cm_soft.values[m].any())))
mu = pd.DataFrame(multi); mu.to_csv(f"results/{PFX}_multi.csv", index=False)

print(f"stars searched {stars} (errors {err}); single events {len(s)} in {s.tic.nunique()} stars; "
      f"common-mode events {int(s.common_mode.sum())}")
print(f"duo pairs {len(u)}; rejected: no surviving alias {int((u.n_aliases < 1).sum())}, "
      f"common-mode {int((u.cm1 | u.cm2).sum())}, Rp>=22 {int((u.rp_earth >= 22).sum())}, star has >2 clean events (periodic/EB) {int((u.n_clean_events > 2).sum())}; SHORTLIST {len(sl)}")
cols = ["tic", "tmag", "teff", "rad", "tc", "tc2", "dt", "sector", "sector2", "dur_h", "depth_ppm", "rp_earth", "snr1", "snr2", "n_aliases", "aliases"]
cols = [c for c in cols if c != "aliases"]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(sl[cols].round(2).to_string(index=False))
print(f"\nMULTI-TRANSIT candidates (>= 3 consistent events on one period; P_max is the longest fitting period, "
      f"P_max/n may also fit): {len(mu)}")
if len(mu): print(mu.to_string(index=False))
