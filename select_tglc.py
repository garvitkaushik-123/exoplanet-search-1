"""Faint-star targets for the TGLC search: southern dwarfs (Teff 3800-6200 K, R 0.4-1.3 Rsun) with
Tmag 13.5-15.5, i.e. fainter than QLP's 13.5 limit, in TESS sectors 1-12 (the only sectors with TGLC on MAST).
Thin Tmag slices are sampled (1,200 stars each); TOI/CTOI/KOI/confirmed hosts and catalogued EBs are removed.
Writes data/tglc_targets.csv and data/tglc_manifest.csv (MAST data URIs)."""
import re, warnings, numpy as np, pandas as pd
from astroquery.mast import Catalogs, Observations
from hostlc import retry
warnings.filterwarnings("ignore")
known = set(pd.read_csv("data/known_planets.csv").tid.astype(int))
known |= set(pd.read_csv("external/ids_toi_ctoi_kzhu2099.csv").tic.astype(int))
known |= set(pd.read_csv("external/ids_tess_ebs_burakulas.csv").tic.astype(int))
fr = []
for a in np.arange(13.5, 15.5, 0.2):
    t = retry(Catalogs.query_criteria, catalog="Tic", objType="STAR", Tmag=[a, a + 0.002], Teff=[3800, 6200],
              rad=[0.4, 1.3], eclat=[-90, -15]).to_pandas()
    t = t[~t.ID.astype(int).isin(known)]
    fr.append(t.sample(min(len(t), 1200), random_state=int(a * 1000))[["ID", "Tmag", "Teff", "rad", "mass", "d", "contratio", "ra", "dec"]])
    print(f"Tmag {a:.1f}: {len(t)} -> {len(fr[-1])}", flush=True)
t = pd.concat(fr); t["ID"] = t.ID.astype(int); ids = [str(i) for i in t.ID]; rows = []
for k in range(0, len(ids), 100):
    o = retry(Observations.query_criteria, obs_collection="HLSP", provenance_name="TGLC", target_name=ids[k:k + 100])
    for name, uri in zip(o["target_name"], o["dataURL"]):
        m = re.search(r"-s0*(\d+)-", str(uri))
        if m: rows.append(dict(tid=int(name), sector=int(m.group(1)), uri=str(uri)))
    if k % 2000 == 0: print("manifest", k, len(rows), flush=True)
man = pd.DataFrame(rows).drop_duplicates(); man.to_csv("data/tglc_manifest.csv", index=False)
t = t[t.ID.isin(man.tid)].rename(columns={"ID": "tid"}); t["n_sectors"] = man.groupby("tid").size().reindex(t.tid).values
t.to_csv("data/tglc_targets.csv", index=False)
print(len(t), "targets with TGLC light curves;", len(man), "files; median sectors", t.n_sectors.median())
