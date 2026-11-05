# exoplanet-search

A transit search for new exoplanets in public NASA TESS data, run by an independent researcher with Claude Code.

**Status (5 Nov 2026): no new planet or credible candidate yet.** See [Results so far](#results-so-far).

## Approach

The method follows the practices in [`docs/Amateur exoplanet discovery methods.md`](docs/Amateur%20exoplanet%20discovery%20methods.md). That research report covers how citizen scientists, small teams and AI-assisted amateurs found planets, and what went wrong in failed claims.

1. **Search where official pipelines are weak.** The current niche is extra planets around stars that already host TOIs or confirmed planets and have six or more SPOC 2-min sectors. Next are duo transits on K and early-M dwarfs, then a Gaia DR4 cross-match (DR4 releases 2 Dec 2026).
2. **Freeze the code before looking.** The thresholds are tagged `v1.0-frozen`, with input hashes in `results_summary/FROZEN_v1.0.sha256`. Any later change gets a new version and a full rerun.
3. **Try to kill every signal.** Each one goes through deep vetting, a duplicate check against public lists, and held-out-year tests before anyone calls it a candidate.
4. **Use careful language.** A signal is a "transit-like signal" or "candidate" until it is validated, never a "planet".

## Pipeline

| File | Purpose |
|---|---|
| `select_hosts.py` | Niche-1 targets: TOI and confirmed hosts (NASA Exoplanet Archive) with at least 6 SPOC 2-min sectors (MAST); also writes known ephemerides to mask |
| `build_manifest.py` | Batch-builds AWS S3 URLs for every 2-min light curve, which downloads much faster than per-star MAST requests |
| `search_hosts.py` | Per star: download → 10-min bins → mask known planets, momentum dumps and segment edges → wotan biweight → iterative BLS (0.5–30 d) → vetting flags (SNR, SDE, transit count, stellar-density duration, per-sector consistency, aliases of known planets, TESS-orbit systematics, rotation) |
| `vet_host_candidate.py` | Deep vetting of one signal: odd/even, secondary, momentum-dump phase, split-half and per-year depth, phase-shuffle false-alarm control, plots |
| `crossmatch_external.py` | Duplicate check against public amateur signal lists ([eumemic/exoplanets](https://github.com/eumemic/exoplanets)); copy their `results_public/*.csv*` into `external/` |
| `test_recovery_hosts.py` | Regression test: unmask TOI-1233.04 and require the frozen pipeline to recover it (passes: P = 3.7959 d, SNR 19.7) |
| `exosearch.py`, `run_search.py`, `vet_candidates.py`, `select_targets*.py`, `prefilter_ffi.py`, `test_injection.py` | Earlier QLP full-frame-image search on M dwarfs (niche 4) and its vetting |

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install numpy scipy pandas astropy astroquery lightkurve transitleastsquares wotan matplotlib batman-package emcee setuptools requests
python select_hosts.py && python build_manifest.py
for k in 0 1 2 3; do python search_hosts.py $k 4 & done      # results/hosts_<k>.csv, resumable
```

The scripts need network access to `mast.stsci.edu`, `exoplanetarchive.ipac.caltech.edu` and `stpubdata.s3.amazonaws.com`. Downloaded light curves (`data/`) and full results (`results/`) are not tracked in git.

## Results so far

- **QLP full-frame-image M dwarfs (about 400 stars, Tmag 11–13.5, old and new sectors):** no credible candidate. Rejections were dominated by stellar rotation, eclipsing binaries, highly variable stars and TESS-orbit (~13.7 d) systematics. The one survivor, TIC 161479114, failed the stellar-density check (`results_summary/TIC161479114_fold.png`).
- **Known hosts (run in progress, 1,645 stars):** TIC 260004324 (LHS 1815) shows a 2.4734 d, ~70 ppm, SNR ~8 signal. It passes odd/even, secondary and momentum-dump checks, but its depth varies from year to year. The eumemic project's signal list already has it, and that project did not promote it, so it is on the watchlist only (`results_summary/vet_260004324.png`).
- **Duo-transit search (1,181 FFI-only K/early-M dwarfs, duo-v1.1):** best signal TIC 355425863. It has two ~1% dips 699.8 d apart, confirmed in three pipelines, with difference imaging on target. Public ESO/FEROS logs show professional radial-velocity monitoring since 2020, so it is **not new** (`results_summary/TIC355425863_status.md`).
- **Duplicate-check lesson:** a GitHub code search of the TIC number found public observatory logs, which revealed prior follow-up that the TOI list and web search missed.
- **Known issue in v1.0:** the odd/even and secondary flags in `search_hosts.py` always pass because their errors come back as NaN. Every passer is re-tested by `vet_host_candidate.py`. The fix is planned for v1.1.

## Acknowledgements

This work uses data from the TESS mission, obtained from MAST at the Space Telescope Science Institute. It also uses the NASA Exoplanet Archive, operated by Caltech under contract with NASA.
