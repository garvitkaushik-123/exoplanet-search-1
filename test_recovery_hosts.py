"""Regression: unmask TOI-1233.04 (P=3.7959 d) on TIC 260647166 and require the frozen pipeline to recover it."""
import numpy as np, pandas as pd, search_hosts as S
h = pd.read_csv("data/hosts.csv"); K = S.KNOWN; tic, hide = 260647166, 3.795890
S.KNOWN = K[~((K.tid == tic) & (abs(K.pl_orbper - hide) < 0.01 * hide))]
res = S.search_star(h[h.tid == tic].iloc[0])
r = res[0]; ok = abs(r["period"] - hide) / hide < 0.001 and r["passed"]
print(f"P={r['period']:.4f} SNR={r['snr']:.1f} SDE={r['sde']:.1f} passed={r['passed']} -> {'RECOVERED' if ok else 'FAILED'}")
