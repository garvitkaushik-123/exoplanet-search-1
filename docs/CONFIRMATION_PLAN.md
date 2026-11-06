# TIC 308184057: plan to confirm the planet and get it recognised

Started 2026-11-06. Owner: Garvit Kaushik. Analysis support: Claude Code.

## Where we are
TIC 308184057 is a K dwarf (Tmag 14.5, 424 pc, Dec −69°) with a P = 6.119 d, ~1.2%-deep, ~2-h transit.

What the evidence shows so far:
- The transit appears in all 17 TESS sectors from 2018 to 2025.
- Odd and even depths match, and there is no secondary eclipse.
- Difference imaging puts the signal on the target.
- Gaia DR3 gives RUWE 0.95, and there is no source within 19.9″.
- ExoFOP lists no TOI or CTOI for this star.
- TRICERATOPS gives FPP 0.19, or ≈ 0.03 once the neighbours excluded by our pixel test are removed.

Status: **likely planet, not validated, not confirmed.** See `results_summary/TIC308184057_status.md`.

## The standard path, and what each step gives
| Level | Required evidence | Who can provide it |
|---|---|---|
| Candidate (public) | Detection plus vetting, published with a timestamp | us (Phase 1) |
| Community TOI (CTOI) on ExoFOP | ExoFOP now asks for a *published* candidate (see the guidelines button on the target page) | us, after Phase 1 |
| **Validated planet** | Statistical FPP < 0.015 and NFPP < 0.001, with high-resolution imaging and on-target ground photometry | TFOP SG1 (photometry), SG3 (speckle/AO), plus our analysis |
| **Confirmed planet** | Radial-velocity mass below 13 M_J (no "planet" without a mass, or a validation paper) | RV team (TFOP SG4 or a southern warm/hot-giant RV program) |
| Archive listing and name | Refereed paper accepted (AJ, MNRAS or A&A) | team paper, with us as discoverers and co-authors |

How credit works: the discoverer's credit comes from (1) the timestamped preprint and DOI, (2) the CTOI submitter field on ExoFOP, and (3) authorship on the discovery paper. Under TFOP publication policy, CTOI submitters are invited as co-authors. The planet's name follows the catalogue ("TOI-xxxx b" if a TOI number is assigned, otherwise "TIC 308184057 b").

## Phase 1: secure priority and make the case (this week)
| # | Task | Owner | Status |
|---|---|---|---|
| 1.1 | MCMC transit fit with uncertainties (P, T0, Rp/R★, a/R★, b, T14, stellar density) | Claude | ✅ `results_summary/fit_308184057_summary.csv` |
| 1.2 | Publication figures: fold and model, per-year depths, odd/even/secondary, difference image, TRICERATOPS | Claude | ✅ `docs/figures/` |
| 1.3 | Observer ephemeris for the next 6 months, with night and altitude at CTIO, La Silla, SAAO, Siding Spring and Las Campanas | Claude | ✅ `results_summary/TIC308184057_ephemeris_observability.csv` |
| 1.4 | Preprint (PDF): methods, all tests, caveats, AI-use statement, data and code availability | Claude drafts, Garvit reviews | ✅ draft `docs/preprint/TIC308184057_preprint.pdf`; **Garvit to review** |
| 1.5 | Data and code package (light curves, scripts, frozen hashes, preregistered ephemeris) | Claude | ✅ built by `make_zenodo_package.py` → `dist/TIC308184057_zenodo_v1.zip` (not in git) |
| 1.6 | **Upload preprint and package to Zenodo to get a DOI** (zenodo.org is not reachable from this session) | **Garvit** | DOI reserved: 10.5281/zenodo.24005247 (draft; publish pending) |
| 1.7 | Decide whether the GitHub repo stays public. It already timestamps the work, but exposes the target before the DOI exists | **Garvit** | |

## Phase 2: get follow-up (weeks 1–6)
| # | Task | Owner |
|---|---|---|
| 2.1 | Read ExoFOP's "Submitting Published Planet Candidate Guidelines" and confirm that a Zenodo or RNAAS publication qualifies | Garvit (ExoFOP is blocked here) |
| 2.2 | Submit the CTOI on ExoFOP with the DOI (needs a free ExoFOP account) | Garvit |
| 2.3 | Email TFOP working groups SG1, SG3 and SG4 with the preprint and ephemeris, offering co-authorship | Garvit sends; drafts ✅ `docs/outreach_emails.md` |
| 2.4 | Email 1–2 southern RV teams that follow warm and hot giants around faint stars (FEROS, HARPS or ESPRESSO users) with the same package | Garvit |
| 2.5 | Optional: post the ephemeris for amateur photometry (AAVSO / Exoplanet Watch). A 1.2% dip on V ≈ 15.5 needs a ≥ 0.4 m telescope in the south | Garvit |

## Phase 3: validation and confirmation (months 1–12, done by collaborators)
- **Ground photometry (≲ 5″) at 1–2 transits:** confirms the dip is on target, refines the ephemeris and checks for chromaticity.
- **Speckle or AO imaging:** gives a contrast curve, which we feed into TRICERATOPS to try for FPP < 0.015 ("validated").
- **Radial velocities (several epochs over about 6 days):** for a 1 M_J planet around a 0.68 M☉ K dwarf at P = 6.12 d, K ≈ 130 m/s.
- **We keep doing:** re-running TRICERATOPS with the contrast curve; checking new TESS sectors; Gaia DR4 epoch photometry from 2 Dec 2026, an independent instrument; and testing the preregistered predictions.

## Phase 4: publication and recognition (months 6–24)
- **Discovery or validation paper** with the team. Garvit is a co-author (likely first or second author as discoverer, depending on the team).
- **arXiv:** unaffiliated authors need endorsement since Jan 2026, which the team's authors can provide.
- **After acceptance,** the NASA Exoplanet Archive lists the planet, and the name becomes official in catalogues.
- **Optional:** an RNAAS note or blog post about the AI-assisted method (Pavel Rabtsevich-style process template).

## Decision points and risks
- **If ground photometry shows the dip on a neighbour,** this is a false positive. We publish a correction note and move on. The preprint must say "candidate".
- **If RV shows a mass above 13 M_J,** it is a brown dwarf or a star. That is still publishable as an EBLM or brown-dwarf discovery, but it is not a planet.
- **Someone else could publish first** now that the repo is public. Mitigation: the Zenodo DOI goes up as soon as possible.
- **Language discipline** until confirmation: "transiting planet candidate". Never "new planet discovered".
