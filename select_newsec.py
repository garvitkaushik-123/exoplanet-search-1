"""New-sector search, targets: SPOC 2-min stars observed in the newest sectors (105-107) that are NOT TOI or
confirmed-planet hosts, are FGKM dwarfs (Teff 3000-6500 K, R 0.2-1.5 Rsun, Tmag < 12.5) and also have at
least one earlier SPOC 2-min sector (<= 104), so new single events can pair with old ones.
Writes data/newsec_targets.csv and data/newsec_manifest.csv (AWS S3 URLs of every SPOC 2-min LC)."""
import re, warnings, numpy as np, pandas as pd
from astroquery.mast import Observations, Catalogs
from hostlc import retry
warnings.filterwarnings("ignore")
NEW = [105, 106, 107]
S3 = "https://stpubdata.s3.amazonaws.com/tess/public/tid"
ids = set()
for s in NEW:
    o = retry(Observations.query_criteria, obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
              sequence_number=s, t_exptime=[100, 130])
    ids |= set(int(x) for x in o["target_name"] if str(x).isdigit()); print("sector", s, len(o), "-> union", len(ids), flush=True)
known = set(pd.read_csv("data/known_planets.csv").tid.astype(int))
ids = sorted(ids - known); print(len(ids), "after removing TOI / confirmed hosts", flush=True)
fr = []
for k in range(0, len(ids), 500):
    fr.append(retry(Catalogs.query_criteria, catalog="Tic", ID=ids[k:k+500]).to_pandas()[["ID", "Tmag", "Teff", "rad", "mass", "d", "contratio", "lumclass"]])
    if k % 5000 == 0: print("TIC", k, flush=True)
t = pd.concat(fr); t["ID"] = t.ID.astype(int)
t = t[(t.Teff.between(3000, 6500)) & (t.rad.between(0.2, 1.5)) & (t.Tmag < 12.5) & (t.contratio.fillna(0) < 0.2)]
print(len(t), "FGKM dwarfs Tmag<12.5", flush=True)
rows = []; tids = [str(i) for i in t.ID]
for k in range(0, len(tids), 100):
    obs = retry(Observations.query_criteria, obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
                target_name=tids[k:k+100], t_exptime=[100, 130])
    prods = Observations.filter_products(retry(Observations.get_product_list, obs), productSubGroupDescription="LC")
    for fn in prods["productFilename"]:
        m = re.match(r"tess\d+-s(\d{4})-(\d{16})-\d{4}-s_lc\.fits", str(fn))
        if m: rows.append(dict(tid=int(m.group(2)), sector=int(m.group(1)),
                              url=f"{S3}/s{m.group(1)}/{m.group(2)[:4]}/{m.group(2)[4:8]}/{m.group(2)[8:12]}/{m.group(2)[12:]}/{fn}"))
    if k % 2000 == 0: print("manifest", k, len(rows), flush=True)
man = pd.DataFrame(rows).drop_duplicates("url")
g = man.groupby("tid").sector.agg(lambda s: (s.max() >= min(NEW)) and (s.min() <= 104))
keep = g[g].index; man = man[man.tid.isin(keep)]
t = t[t.ID.isin(keep)].rename(columns={"ID": "tid"}); t["n_sectors"] = man.groupby("tid").size().reindex(t.tid).values
man.to_csv("data/newsec_manifest.csv", index=False); t.to_csv("data/newsec_targets.csv", index=False)
print(len(t), "targets with new (105-107) AND old (<=104) sectors;", len(man), "light curves")
