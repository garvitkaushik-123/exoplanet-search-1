"""Post-process duo search: common-mode (many stars dipping at once) and shortlist of duo candidates.

An event is common-mode if >= 3 OTHER stars have an event within +-0.3 d (instrumental: scattered light,
momentum dumps, pointing jitter). Flagged events go to manual review, never auto-accepted.
Shortlist rules for duos: both events SNR >= 7, combined SNR >= 10, >= 1 surviving period alias,
neither event common-mode, Rp < 22 R_earth (planet-sized, not a stellar eclipse)."""
import glob, numpy as np, pandas as pd

d = pd.concat([pd.read_csv(f) for f in glob.glob("results/duo_[0-9]*.csv")], ignore_index=True)
stars = d.tic.nunique(); err = d[d.kind == "error"].tic.nunique()
s = d[d.kind == "single"].copy()
tc = s.tc.values; tic = s.tic.values
s["n_other_stars"] = [len(set(tic[(np.abs(tc - x) < 0.3)]) - {k}) for x, k in zip(tc, tic)]
s["common_mode"] = s.n_other_stars >= 3

def cm(t, k):
    m = (s.tic == k) & (np.abs(s.tc - t) < 0.01)
    return bool(s[m].common_mode.any()) if m.any() else False

u = d[d.kind == "duo"].copy()
u["cm1"] = [cm(a, k) for a, k in zip(u.tc, u.tic)]
u["cm2"] = [cm(b, k) for b, k in zip(u.tc2, u.tic)]
clean = s[~s.common_mode].groupby("tic").size()
u["n_clean_events"] = u.tic.map(clean).fillna(0).astype(int)
u["short"] = (u.n_clean_events == 2) & (u.snr1 >= 7) & (u.snr2 >= 7) & (u.snr >= 10) & (u.n_aliases >= 1) & ~u.cm1 & ~u.cm2 & (u.rp_earth < 22)
u.to_csv("results/duo_all_pairs.csv", index=False)
sl = u[u.short].sort_values("snr", ascending=False)
sl.to_csv("results/duo_shortlist.csv", index=False)

print(f"stars searched {stars} (errors {err}); single events {len(s)} in {s.tic.nunique()} stars; "
      f"common-mode events {int(s.common_mode.sum())}")
print(f"duo pairs {len(u)}; rejected: no surviving alias {int((u.n_aliases < 1).sum())}, "
      f"common-mode {int((u.cm1 | u.cm2).sum())}, Rp>=22 {int((u.rp_earth >= 22).sum())}, star has >2 clean events (periodic/EB) {int((u.n_clean_events > 2).sum())}; SHORTLIST {len(sl)}")
cols = ["tic", "tmag", "teff", "rad", "tc", "tc2", "dt", "sector", "sector2", "dur_h", "depth_ppm", "rp_earth", "snr1", "snr2", "n_aliases", "aliases"]
cols = [c for c in cols if c != "aliases"]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(sl[cols].round(2).to_string(index=False))
