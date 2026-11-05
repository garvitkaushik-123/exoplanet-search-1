# New-sector search (SPOC 2-min, sectors 105–107): results (2026-11-05)

**Data situation.** MAST had QLP FFI light curves only up to sector 104 and no TESS-SPOC or TGLC FFI products for sectors 103–114. SPOC 2-min light curves exist up to sector 107. Sectors 108–109 have only 16 stars each.

**Sample.** 2,543 non-host FGKM dwarfs (Tmag < 12.5) with 2-min data in sectors 105–107 plus older sectors (10,990 light curves). Duo-v1.2 event detection; events within 1.5 h of a momentum dump were dropped. No errors.

**Raw output.** 759 single events in 178 stars (251 of them in sectors 105–107), 3 shortlisted duos and 36 multi-transit groups. The multi-transit groups are mostly deep (1–3%), short-period (10–20 d) EBs or TESS-orbit systematics. Periodic signals like these would already be SPOC TCEs or TOIs if they were planets.

## Shortlisted duos: all already known
| TIC | Signal | Our vetting | Prior knowledge (verdict) |
|---|---|---|---|
| 214517366 | 2.8% dips, 3 h, sectors 1 and 106 | SNR ~185 | **EB**: TESS EB catalogue (P = 24.953 d) and listed as a CTOI |
| 159730525 | 0.93% flat-bottomed, ~10.5 h, sectors 68 and 105 | difference image on target (0.9σ, neighbours excluded at 6–8σ); Rp/R★ = 0.094 (≈ 13 R⊕); density-consistent P ≈ 115–148 d | **CTOI.** Also a target of TESS GI G05024 ("F/G/K + M eclipsing binaries", PI D. Martin) and G08058 (circumbinary planets around EBs), so almost certainly an F/G + M-dwarf eclipsing binary (EBLM-type) |
| 232060270 | 0.3%, 6 h, sectors 103 and 105, P = 52.2 or 17.4 d | SNR 10–12 | **CTOI** |

**Lesson.** M dwarfs and Jupiters are the same size, so a clean, flat-bottomed ~1% transit on a G star is as likely an EBLM as a giant planet. Only RVs separate them.

**New duplicate-check sources** (fetched into `external/`, git-ignored):
- `kzhu2099/Exoplanets` all_planets.csv: TOI, CTOI and KOI ids. This is the only CTOI source reachable here, since ExoFOP is blocked.
- `burakulas/detocs` tess_ebs_data.csv: 4,572 TESS EBs with periods.
- TESS GI target lists (`tessgi/TessGiWebsite`): show which programs requested a star, and why.

`crossmatch_external.py` now reports id-only list hits as `LISTED`.

**Net result: no new candidate in the newest sectors either.**
