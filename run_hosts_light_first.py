"""Run the frozen search_hosts.search_star (v1.0, unchanged) on hosts ordered by FEWEST sectors first.
Only the processing order differs from search_hosts.py; thresholds and code are untouched.
Skips any star already present in any results/hosts_*.csv. Usage: python run_hosts_light_first.py <shard> <nshard>"""
import glob, os, sys, time, pandas as pd
import search_hosts as S
shard, nshard = int(sys.argv[1]), int(sys.argv[2])
done = set()
for f in glob.glob("results/hosts_*.csv"):
    try: done |= set(pd.read_csv(f).tic)
    except Exception: pass
hosts = pd.read_csv("data/hosts.csv")
hosts = hosts[hosts.tid.isin(S.MAN.tid) & ~hosts.tid.isin(done)].sort_values(["n_sectors", "tid"]).iloc[shard::nshard]
outf = f"results/hosts_light_{shard}.csv"
rows = pd.read_csv(outf).to_dict("records") if os.path.exists(outf) else []
mine = {r["tic"] for r in rows}
print(f"{len(hosts)} stars queued in shard {shard}", flush=True)
for _, r in hosts.iterrows():
    if int(r.tid) in mine: continue
    s = time.time()
    try:
        res = S.search_star(r); rows += res
        for x in res:
            print(f"{x['tic']} it{x['iter']} P={x['period']:.4f} SNR={x['snr']:.1f} SDE={x['sde']:.1f} "
                  f"Rp={x['rp_earth']:.2f} {'PASS' if x['passed'] else ''} ({time.time()-s:.0f}s)", flush=True)
    except Exception as e:
        print("skip", r.tid, type(e).__name__, str(e)[:120], file=sys.stderr, flush=True)
        rows.append(dict(tic=int(r.tid), iter=-1, version=S.VERSION, error=str(e)[:200]))
    pd.DataFrame(rows).to_csv(outf, index=False)
