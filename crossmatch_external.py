"""Duplicate check: match our signals against eumemic/exoplanets public signal lists and candidate catalogue.
Match = same TIC and period within 0.1% (or a 1/2, 2x harmonic). Usage: python crossmatch_external.py TIC PERIOD"""
import sys, glob, pandas as pd
tic, P = int(sys.argv[1]), float(sys.argv[2])
for f in sorted(glob.glob("external/*.csv*")):
    d = pd.read_csv(f)
    tcol = "tic" if "tic" in d.columns else ("TIC" if "TIC" in d.columns else None)
    pcol = "period" if "period" in d.columns else ("P_d" if "P_d" in d.columns else None)
    if not tcol: continue
    s = d[d[tcol] == tic]
    if not pcol or "type" in d.columns:                      # id-only lists (TOI/CTOI ids, EB catalogue)
        for _, r in s.iterrows():
            print(f"LISTED {f.split('/')[-1]}: type={r.get('type', '?')}" + (f" P={r[pcol]}" if pcol and r[pcol] == r[pcol] else ""))
        if not pcol: continue
    for _, r in s.iterrows():
        for m in (0.5, 1, 2):
            if abs(r[pcol] - m * P) / (m * P) < 1e-3:
                extra = {k: r[k] for k in ("snr", "sde", "status", "label", "rank") if k in r and r[k] == r[k]}
                print(f"MATCH {f.split('/')[-1]}: P={r[pcol]:.5f} (x{m}) {extra}")
print("done")
