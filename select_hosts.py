"""Niche 1 target list: stars that already host TOIs/confirmed planets and have many SPOC 2-min sectors.
Outputs data/hosts.csv (one row per star) and data/known_planets.csv (ephemerides to mask)."""
import io, warnings, requests, numpy as np, pandas as pd
from astroquery.mast import Observations
warnings.filterwarnings("ignore")
TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
def tap(q):
    r = requests.get(TAP, params={"query": q, "format": "csv"}, timeout=180); r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

toi = tap("select tid,toi,tfopwg_disp,pl_orbper,pl_tranmid,pl_trandurh,pl_trandep,st_tmag,st_rad,st_teff,st_logg from toi")
cp = tap("select tic_id,pl_name,pl_orbper,pl_tranmid,pl_trandur,st_rad,st_mass,st_teff,sy_tmag from pscomppars where tic_id is not null")
cp["tid"] = cp.tic_id.str.replace("TIC ", "").astype(int)

# ephemerides of every known signal (TOIs of any disposition + confirmed planets): these get masked
known = pd.concat([
    toi.rename(columns={"pl_trandurh": "dur_h"})[["tid", "toi", "tfopwg_disp", "pl_orbper", "pl_tranmid", "dur_h"]].assign(src="TOI"),
    cp.rename(columns={"pl_trandur": "dur_h"})[["tid", "pl_name", "pl_orbper", "pl_tranmid", "dur_h"]].assign(src="PS"),
])
known.to_csv("data/known_planets.csv", index=False)

# hosts: at least one TOI that is not FP/FA, or a confirmed planet
good = toi[~toi.tfopwg_disp.isin(["FP", "FA"])]
bad_hosts = set(toi[toi.tfopwg_disp.isin(["FP", "FA"])].tid) - set(good.tid) - set(cp.tid)
star = pd.concat([
    good.groupby("tid").agg(tmag=("st_tmag", "first"), rad=("st_rad", "first"), teff=("st_teff", "first"), logg=("st_logg", "first")),
    cp.groupby("tid").agg(tmag=("sy_tmag", "first"), rad=("st_rad", "first"), teff=("st_teff", "first"), mass=("st_mass", "first")),
]).groupby(level=0).first()
star = star[~star.index.isin(bad_hosts)]
star = star[(star.tmag < 12.5) & (star.rad < 1.8) & (star.rad > 0.1)]          # dwarfs, bright enough for small planets
print(len(star), "dwarf hosts with Tmag<12.5 before sector count", flush=True)

# count SPOC 2-min sectors per star (chunked MAST queries)
ids = [str(i) for i in star.index]; nsec = {}
for k in range(0, len(ids), 200):
    o = Observations.query_criteria(obs_collection="TESS", provenance_name="SPOC", dataproduct_type="timeseries",
                                    target_name=ids[k:k+200], t_exptime=[100, 130])
    df = o.to_pandas()[["target_name", "sequence_number"]]
    for t, g in df.groupby("target_name"): nsec[int(t)] = sorted(set(g.sequence_number.astype(int)))
    print(k, flush=True) if k % 1000 == 0 else None
star["sectors"] = [nsec.get(i, []) for i in star.index]
star["n_sectors"] = star.sectors.str.len()
star["n_known"] = known.groupby("tid").size().reindex(star.index).fillna(0).astype(int)
star = star[star.n_sectors >= 6].sort_values("n_sectors", ascending=False)
star.reset_index().rename(columns={"index": "tid"}).to_csv("data/hosts.csv", index=False)
print(len(star), "hosts with >=6 SPOC 2-min sectors"); print(star.n_sectors.describe().round(1).to_string())
