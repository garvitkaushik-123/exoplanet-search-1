"""Niche 2 targets: FFI-only K / early-M dwarfs observed in an early sector (<=55) AND a new sector (>=90).
Writes data/duo_targets.csv and data/duo_manifest.csv (direct MAST download URLs of QLP light curves)."""
import re, warnings, numpy as np, pandas as pd
from astroquery.mast import Catalogs, Observations
from hostlc import retry
from select_targets import tap
warnings.filterwarnings("ignore")
rng = np.random.default_rng(42)
tois = set(tap("select tid from toi")["tid"].astype(int))
known = set(tap("select tic_id from pscomppars where tic_id is not null")["tic_id"].str.replace("TIC ", "").astype(int))
frames = []
for a in np.arange(10.0, 12.5, 0.1):
    d = retry(Catalogs.query_criteria, catalog="Tic", objType="STAR", Teff=[3500, 5300], logg=[4.3, 5.2],
              Tmag=[a, a + 0.1], d=[50, 200], rad=[0.4, 1.0]).to_pandas()
    d = d[~d.ID.astype(int).isin(tois | known)]
    frames.append(d.sample(min(len(d), 400), random_state=int(a * 100)))
    print(f"T {a:.1f}: {len(d)} avail", flush=True)
t = pd.concat(frames).drop_duplicates("ID")[["ID", "Tmag", "Teff", "rad", "mass", "d", "ra", "dec", "contratio"]]
t = t[(t.contratio.fillna(0) < 0.1)]
print(len(t), "after contamination cut", flush=True)
ids = [str(i) for i in t.ID]; rows = []; spoc = set()
for k in range(0, len(ids), 100):
    o = retry(Observations.query_criteria, obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
              target_name=ids[k:k+100], t_exptime=[100, 130])
    spoc |= set(o["target_name"].astype(str))
    q = retry(Observations.query_criteria, obs_collection="HLSP", provenance_name="QLP", target_name=ids[k:k+100])
    for name, uri in zip(q["target_name"], q["dataURL"] if "dataURL" in q.colnames else q["dataURI"]):
        m = re.search(r"_s0*(\d+)-", str(uri))
        if m: rows.append(dict(tid=int(name), sector=int(m.group(1)), uri=str(uri)))
    if k % 1000 == 0: print(k, len(rows), flush=True)
man = pd.DataFrame(rows).drop_duplicates()
man = man[~man.tid.astype(str).isin(spoc)]
g = man.groupby("tid").sector.agg(lambda s: (s.min() <= 55) and (s.max() >= 90))
keep = g[g].index
man = man[man.tid.isin(keep)]
man.to_csv("data/duo_manifest.csv", index=False)
t["ID"] = t.ID.astype(int)
t = t[t.ID.isin(keep)].rename(columns={"ID": "tid"})
t["n_sectors"] = man.groupby("tid").size().reindex(t.tid).values
t.to_csv("data/duo_targets.csv", index=False)
print(len(t), "FFI-only stars with early + new QLP sectors;", len(man), "light curves")
