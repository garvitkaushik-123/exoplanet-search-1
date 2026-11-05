"""Batch-build S3 URLs for every SPOC 2-min LC of every host (fast path, avoids per-star MAST downloads)."""
import re, warnings, numpy as np, pandas as pd
from astroquery.mast import Observations
from hostlc import retry
warnings.filterwarnings("ignore")
S3 = "https://stpubdata.s3.amazonaws.com/tess/public/tid"
h = pd.read_csv("data/hosts.csv"); ids = [str(i) for i in h.tid]; rows = []
for k in range(0, len(ids), 100):
    obs = retry(Observations.query_criteria, obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
                target_name=ids[k:k+100], t_exptime=[100, 130])
    prods = retry(Observations.get_product_list, obs)
    prods = Observations.filter_products(prods, productSubGroupDescription="LC")
    for fn in prods["productFilename"]:
        m = re.match(r"tess\d+-s(\d{4})-(\d{16})-\d{4}-s_lc\.fits", str(fn))
        if not m: continue
        sec, tic16 = m.group(1), m.group(2)
        rows.append(dict(tid=int(tic16), sector=int(sec), url=f"{S3}/s{sec}/{tic16[:4]}/{tic16[4:8]}/{tic16[8:12]}/{tic16[12:]}/{fn}"))
    print(k, len(rows), flush=True)
pd.DataFrame(rows).drop_duplicates("url").to_csv("data/host_manifest.csv", index=False)
