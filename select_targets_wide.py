"""Wider M-dwarf list: Tmag 11-13.5 in 0.25-mag bins, random subsample per bin, minus known TOIs/hosts."""
import pandas as pd, numpy as np, warnings
from astroquery.mast import Catalogs
from select_targets import tap
warnings.filterwarnings("ignore")
tois = set(tap("select tid from toi")["tid"].astype(int))
known = set(tap("select tic_id from pscomppars where tic_id is not null")["tic_id"].str.replace("TIC ", "").astype(int))
parts = []
for lo in np.arange(11.0, 13.5, 0.25):
    hi = lo + 0.25; frames = []
    for a in np.arange(lo, hi, 0.05):          # 0.05-mag slices keep each MAST query small
        frames.append(Catalogs.query_criteria(catalog="Tic", objType="STAR", Teff=[2800, 4000], logg=[4.5, 5.5],
                                              Tmag=[a, a + 0.05], rad=[0.1, 0.6]).to_pandas())
    d = pd.concat(frames); d = d[~d.ID.astype(int).isin(tois | known)]
    parts.append(d.sample(min(len(d), 200), random_state=0)); print(f"{lo:.2f}-{hi:.2f}: {len(d)} avail", flush=True)
t = pd.concat(parts).drop_duplicates("ID"); t.to_csv("data/targets_wide.csv", index=False); print(len(t), "targets")
