"""Build M-dwarf target list from TIC (MAST), remove known TOIs/confirmed hosts (NASA Exoplanet Archive)."""
import sys, io, requests, pandas as pd
from astroquery.mast import Catalogs

TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
def tap(q):
    r = requests.get(TAP, params={"query": q, "format": "csv"}, timeout=120); r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

def main(n=500, out="data/targets.csv"):
    tois = tap("select tid from toi")["tid"].astype(int)
    known = tap("select tic_id from pscomppars where tic_id is not null")["tic_id"].str.replace("TIC ", "").astype(int)
    exclude = set(tois) | set(known)
    tic = Catalogs.query_criteria(catalog="Tic", objType="STAR", Teff=[2800, 4000], logg=[4.5, 5.5],
                                  Tmag=[9, 12.5], rad=[0.1, 0.6]).to_pandas()
    tic = tic[~tic["ID"].astype(int).isin(exclude)].sort_values("Tmag").head(n * 3)   # extra: some will have SPOC 2-min
    tic.to_csv(out, index=False); print(len(tic), "candidates ->", out)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 500)
