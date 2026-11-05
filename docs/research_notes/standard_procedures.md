# Standard Procedures: TESS Signal -> Candidate -> Validated/Confirmed Planet (Independent Researcher, as of 2026-11-04)

> Method note: In this session, direct page fetches to exofop.ipac.caltech.edu, arxiv.org and heasarc.gsfc.nasa.gov were blocked by network policy. All findings below come from web-search result snippets and summaries of the cited pages. They were not read in full. Items marked **[UNVERIFIED]** come from a single secondary source, or from background knowledge with no source in this session. Check them on the live official page before you put them in a checklist.

## 1. ExoFOP-TESS Community TOI (CTOI) submission

### Takeaway
The biggest 2026 change is unconfirmed. A secondary source quotes an ExoFOP home-page news item dated 2026-08-19. According to that quote, community planet candidates must now be published first, in a peer-reviewed journal or (with conditions) an RNAAS, and uploads need prior approval. If this is true, the old pattern of "upload a CTOI first, publish later" no longer works for independent researchers. Once a CTOI is on ExoFOP, the TESS TOI team reviews it, and if it meets their standard it can be promoted to a TOI number.

### Cited Findings
- **2026 policy change [UNVERIFIED, secondary source only]:** A GitHub issue (klucilla/refute #18, citing the ExoFOP-TESS home page, read 2026-10-08) quotes ExoFOP news from **2026-08-19**. The quoted rules: community planet candidates must first be published in a peer-reviewed journal with online access before upload, and approval to upload candidates is required through a request form. — [GitHub issue klucilla/refute #18](https://github.com/klucilla/refute/issues/18)
- **RNAAS route [UNVERIFIED, same source]:** The same issue quotes ExoFOP's "Guidelines for Submitting Published Planet Candidates". Under those guidelines, candidates may appear in an AAS Research Note only if the detection and vetting methods were already published in a peer-reviewed, online journal and the note cites that paper. The issue's suggested path is a JOSS software paper, then a methodology paper, then one RNAAS per candidate, then the ExoFOP upload. — [GitHub issue #18](https://github.com/klucilla/refute/issues/18)
- **Required upload fields [UNVERIFIED, same source]:** the published paper's URL, a tag, the discovery data source, and an initial note. At least two of period, epoch and depth are needed for a cTOI, and the values must be > 0. Do not assign a lowercase planet letter until the planet is confirmed in refereed literature. — [GitHub issue #18](https://github.com/klucilla/refute/issues/18)
- **Promotion to TOI:** The TESS TOI team reviews a submitted cTOI. If it meets the team's standard, it gets a TOI number. — [TOI Release FAQs, tess.mit.edu](https://tess.mit.edu/toi-releases/toi-release-faqs/)
- **Do not duplicate TOIs:** ExoFOP says CTOIs should only be reported when no TOI with the same period exists. — [Guerrero et al. 2021, ApJS (TOI catalog)](https://iopscience.iop.org/article/10.3847/1538-4365/abefe1)
- **Authorship norm (TFOP policy v17, 2020):** The person or team that provided a cTOI should be invited to join as an author on the first publication about that cTOI, unless the candidate had already been announced as a TOI. Uploading to ExoFOP-TESS **does not count as a refereed publication**. — [TFOP WG Publication Policy v17 (2020)](https://tess.mit.edu/wp-content/uploads/TFOPWG_PublicationPolicyv17.pdf)
- ExoFOP data have citable DOIs (e.g., 10.26134/ExoFOP… series). — [IPAC ExoFOP DOIs](https://www.ipac.caltech.edu/dois/exofop); [ExoFOP-Kepler DOI page](https://www.ipac.caltech.edu/doi/10.26134/ExoFOP1)
- The NASA Exoplanet Archive and ExoFOP overview paper (2025) describes the current tools and usage. — [arXiv:2506.03299](https://arxiv.org/pdf/2506.03299)

### Inferences
- If the August 2026 rule is real, the practical order of steps for an unaffiliated person in late 2026 is:
  1. Publish the methods (peer reviewed).
  2. Publish the candidate (paper or RNAAS that cites the methods).
  3. Request upload approval.
  4. Upload the CTOI.
  5. Wait for TOI-team review.
- Before the change, a CTOI could be uploaded with an account plus vetting evidence. That is no longer enough on its own.
- The "no existing TOI at the same period" check (via the ExoFOP TOI table) should be step 0 of any checklist.

### Gaps
- I could not read the official ExoFOP CTOI help page or the 2026-08-19 news item, so the policy, form fields, account rules and file format are unverified.
- I found no source for typical CTOI-to-TOI turnaround times.
- Account requirements: ExoFOP needs a login for uploads (background knowledge). Whether accounts are open to unaffiliated users in 2026 is unverified.

## 2. TFOP working groups SG1–SG5, dispositions, and amateur participation

### Takeaway
TFOP has five sub-groups, one per technique:
- **SG1:** seeing-limited photometry
- **SG2:** reconnaissance spectroscopy
- **SG3:** high-resolution imaging
- **SG4:** precise radial velocities
- **SG5:** space photometry

Amateurs usually join through SG1. The application is on the MIT TFOP page, and the AAVSO offers training and qualification. Members agree to the TFOP charter and publication policy.

### Cited Findings
- **SG1, seeing-limited photometry:** finds false positives caused by nearby eclipsing binaries that contaminate the TESS aperture. Chair: Karen Collins (CfA). — [HEASARC TFOP page](https://heasarc.gsfc.nasa.gov/docs/tess/tfop.html); [MIT TFOP page](https://tess.mit.edu/followup)
- **SG2, recon spectroscopy:** measures stellar parameters to constrain host mass and radius, and detects spectroscopic binaries. Chair: Sam Quinn (CfA). — [tess.mit.edu/followup](https://tess.mit.edu/followup)
- **SG3, high-resolution imaging:** uses AO, speckle and lucky imaging to find companions not resolved in the TIC or by SG1. Chair: David Ciardi. — [tess.mit.edu/followup](https://tess.mit.edu/followup)
- **SG4, precise RVs:** derives orbits and masses. Chair: David Latham. — [tess.mit.edu/followup](https://tess.mit.edu/followup)
- **SG5, space-based photometry:** Chair: Diana Dragomir (UNM). — [tess.mit.edu/followup](https://tess.mit.edu/followup)
- Chair lists differ slightly between charter versions (v10, v16, v19). — [TFOPWG Charter v16](https://tess.mit.edu/wp-content/uploads/TFOPWG_CharterV16.pdf)
- **TFOP goal:** support the Level One requirement of measuring masses for 50 planets smaller than 4 R⊕. Observations use committed LCOGT time and other facilities, and results are stored on ExoFOP-TESS. — [tess.mit.edu/followup](https://tess.mit.edu/followup)
- **Dispositions:** The TFOPWG disposition codes are CP, PC, FP, FA and KP, and they are updated on TEV with each TOI release. — [Guerrero et al. 2021 (arXiv:2103.12538)](https://arxiv.org/pdf/2103.12538)
  - CP = confirmed planet
  - PC = planet candidate
  - FP = false positive
  - FA = false alarm
  - KP = known planet
  - **APC (ambiguous planet candidate)** was not defined in any source I found. It is in current ExoFOP usage per background knowledge **[UNVERIFIED]**.
- **How to join:** The MIT TFOP page links to an application for membership in the working group. — [HEASARC TFOP](https://heasarc.gsfc.nasa.gov/docs/tess/tfop.html)
- **AAVSO path:** The AAVSO calls itself the primary organization for training and qualifying amateurs for TESS. The certification steps are:
  1. Analyze a simulated TESS observation.
  2. Certify compliance with the TFOP charter and publication policy.
  3. Be admitted to SG1.
  — [AAVSO Support of TFOP (Rev 1.2)](https://astrodennis.com/AAVSOSupportofTESS.pdf); [AAVSO TESS poster](https://www.aavso.org/sites/default/files/AAVSO%20Poster%20-%20TESS%202019%20Science%20Meeting%20copy.pdf); [JAAVSO abstract](https://apps.aavso.org/jaavso/article/3526)
- **Small-telescope training group:** The MSRO team joined TFOP SG1 in May 2019. — [MSRO research](https://www.msroscience.org/research)
- **SG1 observation guidelines (Rev 6.4, Sept 2020):** cover the technical standards for observing and reporting. Observations are uploaded to ExoFOP. — [TFOP SG1 Guidelines Rev 6.4](https://astrodennis.com/TFOP_SG1_Guidelines_Latest.pdf)

### Inferences
- An independent researcher's own candidate usually reaches SG1–SG4 only after it becomes a TOI. TFOP prioritizes TOIs.
- Before that point, the researcher must rely on their own or collaborators' follow-up.
- Joining SG1 (with a ~0.3–1 m class telescope and AstroImageJ) is the most realistic way into TFOP.

### Gaps
- I found no sources on the "TESS Transit Finder" tool (the SG1 scheduling tool on ExoFOP, per background knowledge), Exoplanet Watch, ExoClock or Unistellar in relation to TOI follow-up. These need separate checks.
- I found no current (2026) chair roster or a documented process to "request follow-up" of a specific target. As far as I know this is informal, through SG chairs or the TFOP mailing list **[UNVERIFIED]**.

## 3. Vetting tests and thresholds; tools

### Takeaway
The standard tests are odd/even depth, secondary eclipse, centroid / difference-image offset, nearby-star contamination, stellar density versus duration, and SNR consistency. Thresholds differ between pipelines:
- odd/even: 3σ to 5σ
- centroid: >1 px flag or >5σ
- secondary depth ratio: >0.10

LEO-vetter (Kunimoto et al. 2025, AJ) is the current open, rule-based, Robovetter-like reference. Its thresholds can be adjusted.

### Cited Findings
- **LEO-vetter (Kunimoto et al., arXiv:2509.10619; AJ, Nov 2025):**
  - Fully automated flux- and pixel-level vetting, modelled on the Kepler Robovetter.
  - Rule-based, not machine learning. Each metric is compared to a pass/fail threshold.
  - 91% completeness and 97% reliability against noise/systematics on simulated data.
  - Recovered 125 of 135 known TOIs (~93%).
  - Reduced ~20,000 detections among ~200,000 M-dwarf light curves to 172 planet candidates.
  - The unphysical-duration and SNR-consistency tests removed ~63–64% of spurious signals.
  - Available on PyPI as `leo-vetter`.
  — [arXiv:2509.10619](https://arxiv.org/abs/2509.10619); [arXiv HTML](https://arxiv.org/html/2509.10619v1); [TESS Weekly Bulletin Oct 6](https://heasarc.gsfc.nasa.gov/docs/tess/tess-weekly-bulletin-oct-6th.html); [PyPI mkuni](https://pypi.org/user/mkuni/)
- **DAVE:**
  - Light-curve tests: odd–even comparison, modulation, secondary eclipse.
  - Image tests: photocenter shift during transit.
  - Flags a false positive if there is a significant secondary at any non-zero phase or an odd–even difference.
  — [TESS Triple-9 Catalog (MNRAS 513, 102)](https://academic.oup.com/mnras/article/513/1/102/6548905); [Triple-9 II](https://arxiv.org/pdf/2303.00624)
- **Odd/even thresholds in use:** >3σ rejects EBs (citing Batalha et al. 2013); some studies use <5σ to avoid an EB classification. — [Nigraha (arXiv:2101.09227)](https://arxiv.org/html/2101.09227); [Young-planet occurrence, AJ (ad3108)](https://iopscience.iop.org/article/10.3847/1538-3881/ad3108)
- **Centroid thresholds in use:** a >5σ offset rejects blends; one study flags offsets >1 pixel for visual inspection. — [Nigraha](https://arxiv.org/pdf/2101.09227); [Hot Jupiters still lonely (arXiv:2109.08790)](https://arxiv.org/pdf/2109.08790)
- **Secondary eclipse:** a depth ratio >0.10 rejects EBs, and the S/N requirement is waived for ratios >0.15 (one pipeline). — [Nigraha](https://arxiv.org/html/2101.09227)
- **RUWE:** ≈1.0 for single stars. Values well above 1 suggest binarity. One 2026 A&A M-dwarf survey classifies candidates by aperture contamination (G_max) and RUWE. No search result confirmed the common "RUWE > 1.4" cutoff **[UNVERIFIED in this session]**. — [A&A 2026, transit survey of 121 TESS M3–M6 dwarfs](https://www.aanda.org/articles/aa/full_html/2026/06/aa59754-26/aa59754-26.html)
- **tess-point:** recommended for checking whether a target falls on silicon (also used for DDT requests). — [MIT TESS DDT page](https://tess.mit.edu/science/ddt)

### Inferences
Suggested checklist thresholds, taken from the cited pipelines and conservative:
- odd/even depth difference < 3σ
- no significant secondary (or depth ratio < 0.1)
- centroid / difference-image offset < 3σ and < ~1 px (21″ TESS pixels)
- SNR ≥ 7.1–7.3 per the SPOC convention (background knowledge **[UNVERIFIED]**)
- transit duration consistent with stellar density from the TIC/Gaia
- consistent depth across sectors and cameras
- RUWE < 1.4 (convention, **[UNVERIFIED]**)

Report the threshold you actually used in each case, because the community does not use one fixed set.

### Gaps
- I could not find sources for the SWEET test threshold, ghost/halo diagnostics, momentum-dump and scattered-light flags, TIC contratio use, LATTE, TEC (TESS-ExoClass), the `vetting` package (Hedges), TESS-plots, or SPOC DV report metrics. Fetch access to arXiv and GitHub would be needed.
- LEO-vetter's numeric thresholds are in the paper tables, which I could not read.

## 4. Statistical validation (TRICERATOPS, vespa)

### Takeaway
Under TRICERATOPS (Giacalone et al. 2021, AJ 161, 24), a planet is "validated" if FPP < 0.015 and NFPP < 10⁻³. Under vespa (Morton et al. 2016), the bar is FPP < 1%. Both are normally run together with high-resolution imaging contrast curves and ground-based photometry that rules out nearby EBs.

### Cited Findings
- **TRICERATOPS categories:**
  - Validated: FPP < 0.015 and NFPP < 10⁻³
  - Likely planet: FPP < 0.5 and NFPP < 10⁻³
  - Likely nearby false positive: NFPP > 10⁻¹
  - Applied to 384 TOIs: 12 validated, 125 likely planets, 52 likely nearby false positives.
  - The only TESS validation tool that models transits on nearby contaminant stars.
  — [Giacalone et al. 2021, AJ 161, 24 (MIT DSpace PDF)](https://dspace.mit.edu/bitstream/1721.1/134566/2/Giacalone_2021_AJ_161_24.pdf); [Princeton record](https://collaborate.princeton.edu/en/publications/vetting-of-384-tess-objects-of-interest-with-triceratops-and-stat/)
- **Same thresholds still in use in 2026:** e.g., TOI 7475.01 (arXiv:2602.14840) and TOI-181b (VaTEST I). — [arXiv:2602.14840](https://arxiv.org/pdf/2602.14840); [arXiv:2211.07957](https://arxiv.org/pdf/2211.07957)
- **vespa:** Morton et al. 2016 validated 1,935 KOIs at FPP < 1%. vespa has also been applied to 158 TOIs. — [arXiv:1605.02825](https://arxiv.org/abs/1605.02825v1); [Astrobites summary](https://astrobites.org/2016/05/18/the-gruntwork-behind-keplers-new-batch-of-exoplanets/); [arXiv:2008.10516](https://arxiv.org/pdf/2008.10516)
- I found no source saying vespa is officially deprecated. TRICERATOPS is cited as the newer alternative. — [arXiv:2002.00691](https://arxiv.org/pdf/2002.00691v1)

### Inferences
- TRICERATOPS accepts high-resolution imaging contrast curves, which lower FPP and NFPP (background knowledge).
- Without SG3 imaging and SG1 photometry clearing nearby stars, "validated" status is hard to reach.
- An independent researcher usually needs TFOP data, which become usable once the target is a TOI, or their own collaborators.

### Gaps
- Exact input requirements (contrast curve format, the "clearing" of Gaia neighbors by ground photometry) were not confirmed from primary pages in this session.
- I found no sources on injection-recovery or completeness standards beyond LEO-vetter's 91% completeness figure. Field practice (inject synthetic transits into the light curves, measure recovery fraction against period and radius) is background knowledge **[UNVERIFIED]**.

## 5. Getting new observations (TESS GI, DDT, ground-based, RV)

### Takeaway
The TESS GI Cycle 9 Phase-1 deadline was 10 March 2026, so it has passed. Cycle 9 covers Sector 108 (starting 7 Sep 2026) through Sector 121 (ending 19 Sep 2027). The Cycle 10 call has not been confirmed. The DDT program is the fast route: a 2-page request sent about 6 weeks before the sector starts, with up to 500 two-minute and 200 twenty-second targets per sector, and no proprietary period.

### Cited Findings
- **GI Cycle 9:**
  - Phase-1 due **10 March 2026**, 4:30 pm ET, via ARK/RPS (ROSES-25 Amendment 33, program D.3D/D.3C).
  - Covers Sectors 108–121.
  - About 10K two-minute GI targets per cycle, plus FFIs.
  - Ground-based work is allowed if it directly supports TESS analysis.
  - Phase 2 budgets go through NSPIRES.
  — [Cycle 9 D.3C(S) text](https://heasarc.gsfc.nasa.gov/docs/tess/docs/TESS_Cycle9_D3CS.pdf); [Astrobiology.com update](https://astrobiology.com/2025/12/transiting-exoplanet-survey-satellite-tess-cycle-9-proposals-update.html); [tess.mit.edu GI page](https://tess.mit.edu/science/tess-guest-investigator-program/)
- **Who can be PI / be funded:** not confirmed. NASA ROSES generally lets non-US PIs propose for data but not funding. **[UNVERIFIED]**
- **DDT:**
  - Send the template to tess-ddt@mit.edu about 6 weeks before the sector starts. The HEASARC page mentions a web form instead, so the sources conflict.
  - Up to 500 two-minute and 200 twenty-second DDT targets per sector.
  - Must be re-proposed each year.
  - 2-page limit, which must justify the cadence.
  - Check targets with tess-point.
  - Reviewed by the TESS PI, a science expert and the operations team.
  - No proprietary period.
  - Every 20 s target is also observed at 2 min.
  — [MIT DDT page](https://tess.mit.edu/science/ddt); [DDT template](https://tess.mit.edu/wp-content/uploads/tess-ddt-template.txt); [HEASARC DDT](https://heasarc.gsfc.nasa.gov/docs/tess/ddt.html); [DDT list](https://tess.mit.edu/public/DDTs/DDT_list.html)
- **TESS target selection procedure** (how 2-min targets are chosen) — [arXiv:2109.02665](https://arxiv.org/pdf/2109.02665)
- **LCOGT time** is committed to TFOP (so it is available via TOI status, not directly). — [tess.mit.edu/followup](https://tess.mit.edu/followup)

### Inferences
- For an independent researcher, a DDT request is the most realistic way to get 2-min or 20-s data on their candidate in an upcoming sector. They need to check tess-point visibility first.
- RV time (HARPS-N, NEID) is only reachable through collaborators or TFOP SG4 once a target is a TOI. Open proposals require institutional PIs in practice (**[UNVERIFIED]**; no source found).

### Gaps
- I did not find a Cycle 10 call or timeline, a 2026 extended-mission status, or details on Exoplanet Watch, ExoClock or Unistellar programs.
- I found no source on how independent (non-US, unaffiliated) researchers can serve as GI PIs.

## 6. NASA Exoplanet Archive criteria, IAU definition, naming

### Takeaway
The Archive includes an object only if it has a mass or minimum mass ≤ 30 MJup, is not free-floating, has had enough follow-up and validation that a false positive is unlikely, and is described in an accepted peer-reviewed paper. The IAU's 2018 working definition uses ~13 MJup (deuterium burning) plus a mass ratio to the host below ~1/25.

### Cited Findings
- **Archive criteria:**
  - mass (or minimum mass) ≤ 30 MJup
  - not free-floating
  - sufficient follow-up and validation to deem a false positive unlikely
  - results peer reviewed and accepted for publication
  - Criteria page last updated 6 Dec 2024.
  — [NASA Exoplanet Archive: Exoplanet Criteria for Inclusion](https://exoplanetarchive.ipac.caltech.edu/docs/exoplanet_criteria.html)
- **Excluded targets list** (e.g., the SCR 1845 companion, which is above 30 MJup); the list was updated April 2026. — [Targets Excluded from the Archive](https://exoplanetarchive.ipac.caltech.edu/docs/removed_targets.html)
- **IAU working definition (amended Aug 2018, Commission F2):** deuterium-fusion limit of ~13 MJup at solar metallicity, plus a star–planet mass ratio below the L4/L5 instability limit (~1/25). — [Lecavelier des Etangs & Lissauer 2022 (arXiv:2203.09520)](https://ar5iv.labs.arxiv.org/html/2203.09520); [HAL](https://hal.sorbonne-universite.fr/hal-03631543)
- **Naming convention:** do not assign a lowercase planet letter until the planet is confirmed in refereed literature (ExoFOP guideline as quoted, **[UNVERIFIED]**). — [GitHub issue #18](https://github.com/klucilla/refute/issues/18)

### Inferences
- RNAAS is not peer reviewed (see section 7), so a planet announced only in an RNAAS would likely **not** meet the Archive's "peer reviewed and accepted" criterion. A refereed AJ, MNRAS or A&A paper is needed to get into the Archive.

### Gaps
- I did not find documented naming conventions (TOI-XXXX b vs. TIC-based names) beyond the ExoFOP quote.

## 7. Publication routes and arXiv endorsement

### Takeaway
RNAAS rules:
- free to publish
- moderated, not peer reviewed
- 1,500 words including references, with a 150-word abstract
- one figure or table
- usually published within ~72 h

arXiv changed its rules on 21 Jan 2026, across all sections. An institutional email alone no longer qualifies a new author for automatic endorsement; prior accepted authorship in the category is also needed. Unaffiliated authors therefore need a **personal endorsement** from an established arXiv author in the field, and arXiv staff cannot grant one.

### Cited Findings
- **RNAAS:**
  - 1,500-word cap (including title, headers, captions, references; 150-word abstract)
  - one figure *or* table, which with its caption must fit on one page
  - not peer reviewed; moderated by an editor
  - currently no author charges
  - at most 20 Notes per first author per 12 months
  - typically published within 72 h
  — [AAS Research Note Preparation Guidelines](https://journals.aas.org/research-note-preparation-guidelines); [RNAAS scope](https://journals.aas.org/scope-of-research-notes-of-the-american-astronomical-society/); [RNAAS home](https://journals.aas.org/research-notes/)
- Older templates show a 1,000-word limit, which is outdated. — [example RNAAS (ar5iv)](https://ar5iv.arxiv.org/html/1809.05539)
- **arXiv:**
  - From 21 Jan 2026 (after a Mathematics pilot starting 10 Dec 2025), an institutional email is no longer the sole qualifier.
  - Automatic endorsement needs both an institutional email and previous accepted authorship in the endorsement domain.
  - Anyone else needs a personal endorsement from an established author in the same area.
  - arXiv staff cannot personally endorse.
  — [arXiv blog, 2026-01-21](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/); [arXiv blog, Math pilot 2025-12-10](https://blog.arxiv.org/2025/12/10/updated-endorsement-policy-for-arxiv-mathematics/); [CASRAI summary](https://casrai.org/news/arxiv-2026-endorsement-english-ai-policy-changes)
- **Returning authors:** a returning author entering a new category is treated as new there (secondary source). — [CASRAI](https://casrai.org/news/arxiv-2026-endorsement-english-ai-policy-changes)

### Inferences
- A workable independent route is:
  1. JOSS or a refereed methods paper (AJ, MNRAS, A&A, or PASP / JAAVSO for smaller work).
  2. RNAAS per candidate, citing the methods paper. This also fits the reported ExoFOP 2026 rule.
  3. A refereed discovery or validation paper for the Archive.
  4. Find an arXiv endorser early, ideally a TFOP collaborator.

### Gaps
- I did not verify AJ/MNRAS/A&A page charges and rules for unaffiliated authors, or JAAVSO scope for exoplanet work.

## 8. Reproducibility and data acknowledgement

### Takeaway
Cite MAST data with a DOI (10.17909/…) and use the TESS funding acknowledgement. MAST **updated its acknowledgement and attribution pages on 2 July 2026**, so take the wording from the live page, not from older papers.

### Cited Findings
- MAST updated its Mission Acknowledgement and Data Attribution pages on 2 July 2026, and TESS is affected. — [STScI newsletter July 2026](https://archive.stsci.edu/contents/newsletters/july-2026/changes-to-attributions); [MAST acknowledgments](https://archive.stsci.edu/acknowledgments.html); [MAST publishing / DOIs](https://archive.stsci.edu/publishing)
- **Past wording varies:**
  - "Funding for the TESS mission is provided by NASA's Science Mission Directorate" (2026 paper)
  - "...by the NASA Explorer Program" (2023 paper)
  - "This paper includes data collected with the TESS mission, obtained from the MAST data archive at STScI", plus a DOI 10.17909/…
  — [arXiv:2607.01853](https://arxiv.org/pdf/2607.01853); [arXiv:2305.09687](https://arxiv.org/pdf/2305.09687)
- ExoFOP data have DOIs that can be cited. — [IPAC ExoFOP DOIs](https://www.ipac.caltech.edu/dois/exofop)
- Gaia DR3 IDs for TIC targets (2026) help with reproducible cross-matching. — [arXiv:2603.28850](https://arxiv.org/pdf/2603.28850)

### Inferences
- Reproducibility checklist:
  - MAST DOI for the exact products used
  - software versions (lightkurve, TLS/BLS, LEO-vetter, TRICERATOPS) with Zenodo/JOSS DOIs
  - public notebooks
  - ExoFOP DOI for follow-up data
  - updated MAST acknowledgement text

### Gaps
- The exact post-July-2026 TESS acknowledgement wording was not retrieved.
