"""Build the Zenodo upload package for TIC 308184057.01: preprint PDF, figures, light curve (CSV), fit posterior
summary, TRICERATOPS outputs, ephemeris, evidence (ExoFOP screenshot, Gaia query), the exact code used, and SHA-256 hashes."""
import hashlib, json, os, shutil, zipfile, numpy as np, pandas as pd
out = "dist/TIC308184057_zenodo"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out + "/code"); os.makedirs(out + "/data"); os.makedirs(out + "/figures")
d = np.load("results/tic308184057_tars.npz")
pd.DataFrame(dict(btjd=d["t"], flux_detrended=d["f"], flux_raw_norm=d["raw"], sector=d["s"].astype(int))).to_csv(out + "/data/TIC308184057_TARS_lightcurve.csv", index=False)
for f in ["results_summary/fit_308184057_summary.csv", "results_summary/triceratops_TIC308184057_probs.csv", "results/triceratops_TIC308184057.csv",
          "results_summary/TIC308184057_ephemeris_observability.csv", "results_summary/diff_308184057.log", "results_summary/tglc_vetted.csv",
          "results_summary/evidence/gaia_dr3_TIC308184057_1arcmin.csv", "results_summary/evidence/exofop_TIC308184057_2026-11-06.png",
          "results_summary/TIC308184057_status.md", "results/tglc_injection.csv"]:
    if os.path.exists(f): shutil.copy(f, out + "/data/")
for f in os.listdir("docs/figures"): shutil.copy("docs/figures/" + f, out + "/figures/")
shutil.copy("docs/preprint/TIC308184057_preprint.pdf", out + "/")
for f in ["select_tglc.py", "tglc_search.py", "tglc_vet.py", "test_tglc_injection.py", "duo_search.py", "prep_tars_308184057.py",
          "fit_transit_308184057.py", "make_figures_308184057.py", "observability_308184057.py", "diff_tesscut_stack.py",
          "run_triceratops.py", "tars_check.py", "crossmatch_external.py", "README.md"]:
    shutil.copy(f, out + "/code/")
meta = {"metadata": {"title": "TIC 308184057.01: a candidate warm sub-Saturn transiting a faint K dwarf (TESS FFI search below the QLP limit)",
        "upload_type": "publication", "publication_type": "preprint",
        "description": "Preprint, data products and code for the planet candidate TIC 308184057.01 (P = 6.1190153 d, Rp/R* = 0.106). Not peer reviewed; candidate status only.",
        "creators": [{"name": "Kaushik, Garvit", "affiliation": "Independent researcher"}],
        "keywords": ["exoplanets", "TESS", "transit", "planet candidate", "TIC 308184057"], "license": "cc-by-4.0", "access_right": "open",
        "related_identifiers": [{"identifier": "https://github.com/garvitkaushik-123/exoplanet-search.", "relation": "isSupplementTo"}]}}
json.dump(meta, open(out + "/zenodo_metadata.json", "w"), indent=2)
with open(out + "/SHA256SUMS.txt", "w") as h:
    for root, _, files in os.walk(out):
        for f in sorted(files):
            if f == "SHA256SUMS.txt": continue
            pth = os.path.join(root, f); h.write(f"{hashlib.sha256(open(pth, 'rb').read()).hexdigest()}  {os.path.relpath(pth, out)}\n")
zp = "dist/TIC308184057_zenodo_v1.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(out):
        for f in files: z.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), "dist"))
print(zp, round(os.path.getsize(zp) / 1e6, 1), "MB;", sum(len(fs) for _, _, fs in os.walk(out)), "files")
