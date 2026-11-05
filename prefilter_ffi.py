"""Keep only stars with TESS observations but NO SPOC 2-min/20-s light curve (i.e. FFI-only)."""
import pandas as pd, warnings
from astroquery.mast import Observations
warnings.filterwarnings("ignore")
t = pd.read_csv("data/targets_wide.csv"); ids = [str(i) for i in t.ID]
spoc = set(); anytess = set()
for k in range(0, len(ids), 100):
    chunk = ids[k:k+100]
    o = Observations.query_criteria(obs_collection="TESS", target_name=chunk, dataproduct_type="timeseries")
    spoc |= set(o["target_name"].astype(str)); print(k, len(spoc), flush=True)
    o2 = Observations.query_criteria(obs_collection="HLSP", target_name=chunk) if False else None
t["has_spoc"] = t.ID.astype(str).isin(spoc)
ffi = t[~t.has_spoc]; ffi.to_csv("data/targets_wide_ffi.csv", index=False)
print(len(t), "total;", len(ffi), "without SPOC 2-min")
