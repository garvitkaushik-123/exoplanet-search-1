# Hunt where pipelines are blind, then prove it

**Hinglish summary (TL;DR)**
- Amateurs aur citizen scientists ne asli planets tab dhoondhe jab unhone pipelines ke "blind spots" target kiye: single/duo transits, long periods, circumbinary systems, faint FFI-only stars. Har confirmed case mein ek professional "sponsor" tha jisne follow-up (RV, imaging, photometry) karwaya.
- Pavel Rabtsevich (TIC 4206066) ka asli kamaal "discovery" nahi, balki discipline tha: held-out sector prediction, fresh AI sessions se adversarial review, frozen code, preregistration, aur TESS DDT se naya 2-min data maangna. Woh abhi bhi "candidate" hai, "planet" nahi. Sector 110 ka result abhi aaya nahi hai.
- Hamare ~400 M dwarfs mein zero candidate aana normal hai: LEO-vetter ke rate (172 PCs / ~2 lakh M-dwarf light curves) se ~0.3 expected the. Humein 10,000+ stars aur ek better niche chahiye.
- Plan: (1) multi-sector/CVZ known-host stars mein extra planets dhoondo, (2) FFI-only K/early-M stars mein duo-transits, (3) 2 Dec 2026 ko Gaia DR4 cross-match, (4) periodic FFI search sirf naye sectors par, kyunki yeh niche bahut crowded hai (eumemic ne ~40 lakh stars search kiye).
- Pipeline fixes: stellar-density duration check, rotation prewhitening, saare sectors use karo, TESS-SPOC/TGLC light curves, centroid + per-sector depth checks, aur TRICERATOPS ka sanity check.
- 2026 ka (unverified) ExoFOP rule: CTOI upload se pehle peer-reviewed publication chahiye. Isliye pehle pro collaborator dhoondo aur methods paper (JOSS) likho. "Discovery" ka claim kabhi mat karo.

Independent and amateur exoplanet finders have succeeded in public data by exploiting a **specific, documented gap in an official pipeline**, and then handing the signal to professionals who could run pixel-level vetting and get new observations. The gaps include single and duo transits, long periods, circumbinary timing, faint stars that were never manually vetted, signals a vetter rejected on one marginal metric, and low-SNR signals in known multi-planet systems. Every confirmed citizen-science TESS planet in these notes (TOI-813 b, HD 152843 b/c, TOI-2180 b, TOI-4633 c, TOI-1338 b) is long-period, few-transit, circumbinary, or around a bright star. Every one had a professional sponsor. Pavel Rabtsevich's October 2026 TESS candidate TIC 4206066 adds something new: a **process template for AI-assisted work**. It combines leave-one-sector-out prediction, independent clean-session and Codex review, a self-audit that removed an overclaim, preregistration, and a successful request for TESS Director's Discretionary Time (Sector 110). It is still explicitly "not statistically validated and not confirmed". The wave of imitators that followed shows the failure modes in public: rediscovered eclipsing binaries and TOIs, duplicate TIC entries, a TRICERATOPS configuration bug, QLP edge artefacts, and priority collisions with other amateurs. The professional route is also tightening. A reported (unverified) ExoFOP rule from 19 Aug 2026 requires published candidates before CTOI upload, and arXiv now requires personal endorsement for unaffiliated authors. For our team, the math says our null result on ~400 M dwarfs is expected. The recommended plan therefore moves to less crowded niches with lower false-positive priors, fixes the specific weaknesses that killed our candidates, and builds the publication and sponsor route in parallel with the search.

**How to read the evidence labels.** **[Verified]** means the claim was read directly from a primary page in the research (Pavel's gist, the eumemic and xaviercallens GitHub repos, the ESA Gaia DR4 date) or comes from a peer-reviewed or official page cited in the notes. **[Snippet]** means the claim came only from a search-engine summary of a page the researchers could not open (Scientific American, Gizmodo, ExoFOP news, X). **[Inferred]** is our reasoning. **[Unverified]** is background knowledge with no source in this session.

## Pipelines miss five kinds of signal, and humans found planets in all five

The citizen-science record is a map of pipeline blind spots. Planet Hunters volunteers found PH1b (Kepler-64b), the first transiting planet in a quadruple star system. Its transits across an eclipsing binary recur about every 137 days and could be seen "by visual inspection", but they were aperiodic in timing and duration, which defeats folded searches ([Schwamb et al., arXiv 1210.3612](https://arxiv.org/pdf/1210.3612)). Planet Hunters TESS (PHT) had **more than 22,000 volunteers inspect Sectors 1-26** and produced 90 strong new candidates, and **73 of those 90 showed only a single transit** ([Eisner et al. 2021, MNRAS](https://academic.oup.com/mnras/article/501/4/4669/6027708)). The same paper gives the counterpoint that matters for us: volunteers recovered only **51% of 3-4 R⊕ TOIs**, so human eyes lose to pipelines on small, shallow, multi-transit signals. Nora Eisner put the asymmetry plainly for TOI-4633 c, a 272-day mini-Neptune: "While our algorithms struggle to identify these longer-period planets, the citizen scientists don't" ([phys.org](https://phys.org/news/2024-04-citizen-scientists-exoplanet-binary-star.pdf)).

The Visual Survey Group (VSG) is the closest model for a small independent team. It is a pro-am group that has inspected **nearly 10 million light curves with LcTools and authored 69 peer-reviewed papers** ([Kristiansen et al. 2022, arXiv 2205.07832](https://arxiv.org/pdf/2205.07832)). Its member Tom Jacobs spotted a single, roughly 24-hour, sub-0.5% dip in TESS data from February 2020. The VSG alerted Paul Dalba and Diana Dragomir, who arranged Automated Planet Finder radial velocities and a 14-site ground campaign. The result was TOI-2180 b, a 2.8 MJ planet with P ≈ 261 d, published about two years later with Jacobs as co-author ([Dalba et al. 2022, arXiv 2201.04146](https://pdf.arxiv.org/pdf/2201.04146)). TOI-1338 b, TESS's first circumbinary planet, followed the same pattern. High-school intern Wolf Cukier noticed a transit that did not line up with the binary's eclipses. The three transits had equal depths but different durations, and photodynamics rather than RV closed the case ([sci.news](https://www.sci.news/astronomy/tess-circumbinary-planet-toi-1338b-07989.html); [Wikipedia](https://en.wikipedia.org/wiki/TOI-1338_b)).

Machine learning and archival re-analysis exploit the other gaps. Shallue and Vanderburg's AstroNet was a CNN trained on about 15,000 human-vetted Kepler signals, and it found **Kepler-90i and Kepler-80g** ([UT News](https://news.utexas.edu/2017/12/14/using-ai-to-discover-new-worlds); [Google Research](https://research.google/pubs/identifying-exoplanets-with-deep-learning-a-five-planet-resonant-chain-around-kepler-80-and-an-eighth-planet-around-kepler-90/)). The notes report (not verified) that it did so by pushing below the official SNR threshold on stars already known to host several planets. Those stars have a low false-positive prior, which the ExoMiner "multiplicity boost" later formalised to validate 69 more planets ([astrobiology.com](https://astrobiology.com/2023/05/multiplicity-boost-of-transit-signal-classifiers-validation-of-69-new-exoplanets-using-the-multiplicity-boost-of-exominer.html)). An undergraduate, Anne Dattilo, adapted the public AstroNet code to K2 and found two super-Earths ([NASA](https://science.nasa.gov/universe/exoplanets/discovery-alert-two-new-planets-found-by-ai)). Kepler-1649c, an Earth-size habitable-zone planet, had been thrown out by the Robovetter because it failed one test (Model-Shift Uniqueness). The test failed because of pipeline-induced noise, and humans re-inspecting the false-positive list rescued it ([AAS Nova](https://aasnova.org/2020/04/22/rescuing-an-overlooked-planet/)). ExoMiner++ scored public TESS TCEs and produced **50 new CTOIs** ([arXiv 2502.09790](https://arxiv.org/abs/2502.09790)).

The faint-star gap is real but now heavily fished. QLP searched every star to T = 13.5 but was manually vetted only to T = 10.5. Kunimoto's independent vetting of that gap produced **1,617 new TOIs** ([Kunimoto et al. 2022](https://research.usq.edu.au/download/80dbc8eb535184c01efad8ed6dc46a801fcb9319a018b62fb8203b0badd6b665/889074/Kunimoto_2022_ApJS_259_33.pdf)). DIAmante added **842 new candidates from 1.4 million FFI light curves** ([arXiv 2210.14559](https://arxiv.org/abs/2210.14559)). TGLC PSF photometry de-blends neighbours using Gaia priors, and QLP adopted TGLC photometry in a 2026 release ([Han & Brandt 2023](https://arxiv.org/pdf/2301.03704); [QLP DRN 004](https://arxiv.org/pdf/2603.22236)).

Single and duo transits are a professional programme in their own right. CHEOPS observes the discrete period aliases of TESS transits separated by about two years, which resolved HIP 9618 c and HD 15906 c (the latter had 36 allowed periods) ([EPSC2022](https://meetingorganizer.copernicus.org/EPSC2022/EPSC2022-499.html); [arXiv 2306.04450](https://web3.arxiv.org/pdf/2306.04450)). Outside transits, Gaia-4b was the first Gaia astrometric planet, and it **needed RV to be confirmed** ([Penn State HPF](https://hpf.psu.edu/2025/02/04/gaia-4-5)). Archival RV mining produced the cautionary Barnard's Star 233-d candidate, which ESPRESSO did not support ([IAC](https://www.iac.es/en/science-and-technology/publications/sub-earth-mass-planet-orbiting-barnards-star)). KMTNet's "hidden" microlensing planets are found inside the collaboration, not by outsiders ([arXiv 2401.04256](https://arxiv.org/pdf/2401.04256)).

| Case | Gap exploited | Who closed it | Time to paper |
|---|---|---|---|
| PH1b, TOI-1338 b | Circumbinary, aperiodic transits | Pro team, photodynamics | ~6 months (TOI-1338) [Verified] |
| TOI-813 b, PHT catalogue | Single and long-period transits | Eisner/PHT, CTOI, validation | ~9 months [Verified] |
| TOI-2180 b (VSG) | One TESS transit | Dalba/Dragomir, APF RV, 14-site campaign | ~2 years [Verified] |
| Kepler-90i (AstroNet) | Sub-threshold signals in multis | Google + UT Austin, statistical validation | Months [Verified]; method details [Unverified] |
| Kepler-1649c | Vetter false rejection | Kepler FPWG re-inspection | Data from 2013, paper 2020 [Verified] |
| Faint-star TOIs | QLP vetted only to T = 10.5 | MIT team | arXiv Dec 2021 to ApJS Mar 2022 [Verified] |
| TIC 4206066 (Pavel) | New sector plus archival stacking | Self, with TESS DDT | Candidate only, no refereed paper yet [Verified] |

## Pavel's TIC 4206066 is a process template, not yet a planet

Pavel's own gist is the primary source, and it was read directly **[Verified]**. Signal A (P ≈ 3.18 d, depth about 0.04-0.05%, about 1.4 R⊕ if it is on the target) was **first noticed in TESS Sector 98 and then traced back to Sectors 32 and 6**, around "a nearby late-K dwarf about 116 light-years away". Signal B (11.13 d, about 2.2 R⊕) is "explicitly treated as tentative". Claude Code downloaded and parsed the data, wrote the search, fitting and false-positive code, and made the plots. Codex and "separate clean agent sessions" served as independent reviewers. The vetting included leave-one-sector-out prediction (fit the other data, predict the hidden transit times, then look only at those windows), nearby-star and pixel checks, Gaia astrometry, photometry and RV, **TRICERATOPS FPP of about 0.03-0.04**, and a duplicate check against 36 catalogs and **340,505 automated TESS alerts**. An internal audit removed "at least one overstrong statistical claim". The gist also records the decisive move: TESS approved **DDT Program 100 for 2-min data in Sector 110 (2026-10-31 to 2026-11-26)**, with 9 transits of Signal A and 3 of Signal B expected, preregistered outcome categories, and frozen code with checksums ([gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba)).

Several points cut against the hype. The FPP of 0.03-0.04 is **above the TRICERATOPS validation threshold of FPP < 0.015 and NFPP < 10⁻³** ([Giacalone et al. 2021](https://dspace.mit.edu/bitstream/1721.1/134566/2/Giacalone_2021_AJ_161_24.pdf)). Pavel himself names an unresolved bound companion as the main surviving alternative, which needs high-resolution imaging and RV to test. Press summaries say the 2018 (Sector 6) dips "tended to align with moments where TESS fired its thrusters" ([Scientific American](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/), **[Snippet]**), so one of the three sectors coincides with momentum dumps. NExScI's Kevin Hardegree-Ullman said ruling out false-positive scenarios is the hard part, and that AI mainly helps chain together search and basic-vetting code rather than confirm planets ([Gizmodo](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393), **[Snippet]**). Yale's Greg Laughlin called the potential for at least one planet "solid" (**[Snippet]**). The "126,000 stars" and "22 additional dips" figures appear only in press summaries, not in the gist, and the exact data product, search algorithm and thresholds remain unknown because the Zenodo preprint was unreachable. **No Sector 110 result exists as of 4 Nov 2026**. The sector ends on 26 Nov and data release follows some weeks later [Inferred].

The best public proxy for his pipeline is eumemic/exoplanets, which says it "follows" his method and blindly recovered 3.18278 d and 11.13274 d ([repo](https://github.com/eumemic/exoplanets), **[Verified]**). Its stack is SPOC 2-min PDCSAP, then TESS-SPOC FFI PDCSAP, then QLP; wotan biweight detrending; BLS over 0.5-30 d with SNR ≥ 9, MES ≥ 7.1 and at least 3 transits; then LEO-Vetter, difference-image centroids, Gaia RUWE and RV, EB catalogs, TRICERATOPS and MOLUSC. Whether Pavel used this exact stack is unconfirmed. On 20 Oct 2026, Pavel reported a second candidate from a single/duo-transit search of about **20,000 nearby red dwarfs**. He said NASA's pipeline had seen the 2020 dips but discarded the stretch containing the second one because many stars dimmed at once there, which led to a wrong ~11.5 d period. The candidate is about 2.5 R⊕, and PHT volunteers had already flagged the dips by eye ([X post](https://x.com/p_rabtsevich/status/2112644366934446574), **[Snippet]**). Those two details matter for our plan. Single and duo transits on nearby red dwarfs are now being actively searched by others, and "someone already flagged it" is a real risk.

## The 2026 follow-on wave failed in seven repeatable ways

eumemic/exoplanets began on Pavel's posting day and grew from 10 signals to **639 "candidates"**. It searched TIC dwarfs to T ≤ 11.5 in QLP Sectors 97-105, plus 6,430 TOI hosts, and later about **4.04 million FGKM dwarfs to T ≤ 13.5** and periods of 20-100 d. Its injection recovery was only **52-62% at SNR 10** ([repo](https://github.com/eumemic/exoplanets), **[Verified]**). Its public corrections log is the most useful pitfall list available:

1. TIC 143168991 overlapped an existing TOI-7580.01.
2. TIC 9994636 is a double-lined spectroscopic binary.
3. TIC 235005571 is a known Algol-type eclipsing binary.
4. A duplicate-TIC fault hid a likely nearby false positive.
5. A **TRICERATOPS setup bug gave FPP < 1e-7** to a target whose 200-s data alone gave about 0.4.
6. QLP orbit-edge artefacts in Sectors 94-104 forced a data fix.
7. Six candidates had already been posted by other amateurs on Zenodo.

The project's tier counts (22 + 290 + 158 + 111 = 581) also do not match its 639 headline. Outside reviewers opened false-positive issues, and the tiers were renamed after review of an AJ draft. The project's README does not state that it used LLM agents, so its "AI-assisted" status is **[Unverified]**.

Our own run hit the same walls. Rejections were dominated by rotation and spots, eclipsing binaries, highly variable stars and ~13.7-day orbit systematics. Our QLP light curves show 1-2% orbit-scale trends, which matches eumemic's QLP-edge fix. Our lone survivor, TIC 161479114 (P = 0.863 d, ~400 ppm), failed because its ~2.4 h duration is about **2.5x the ~0.9 h maximum expected for a central transit** of a 0.4 R☉/0.4 M☉ star at that period [Inferred, our calculation]. In the current code, `vetting_flags()` in `exosearch.py` only tests `0.02 < duration/period < 0.15`, which cannot catch this. Two other cautionary cases are worth remembering. The Barnard 2018 RV candidate shows that heterogeneous archives produce fragile small-planet claims. Kepler-1649c shows the opposite error, a real planet killed by one noisy metric. Search results also produced fabricated items, a "KOI-456.04 found with Claude Code by Dr. Sarah Chen" and a "TypeSafe's Jev" tool, so every agent-gathered fact must be traced to a primary page.

The base rate explains our null result. LEO-vetter reduced about **20,000 detections among ~200,000 M-dwarf light curves to 172 planet candidates** ([Kunimoto et al., arXiv 2509.10619](https://arxiv.org/abs/2509.10619)). That is about 1 candidate per 1,160 light curves, so about 0.3 expected in our ~400 stars, and most of those would already be TOIs [Inferred]. About 25% of TESS prime-mission TOIs turned out to be false positives ([arXiv 2205.05073](https://arxiv.org/pdf/2205.05073)). At our measured ~70 s per star per core for TLS, 4 cores process about **4,900 stars per day**. Reaching tens of thousands of stars is a matter of days, but in the plain M-dwarf periodic niche we are now competing with a 4-million-star search [Inferred].

## The professional route now runs through publication and a sponsor

The standard ladder is: signal, vetting, CTOI, TOI, TFOP follow-up, then validation or confirmation, then a refereed paper and inclusion in the Archive. What changed in 2026 is the CTOI step. A secondary source quotes an **ExoFOP news item dated 2026-08-19**. According to that quote, community candidates must first be published in a peer-reviewed online journal, uploads require approval through a request form, and an RNAAS qualifies only if it cites an already peer-reviewed methods paper. The issue thread proposes the sequence JOSS software paper, then methods paper, then one RNAAS per candidate, then ExoFOP upload ([klucilla/refute #18](https://github.com/klucilla/refute/issues/18), **[Unverified: secondary quote of an ExoFOP page we could not open]**). Other rules hold regardless. CTOIs should not duplicate an existing TOI at the same period ([Guerrero et al. 2021](https://iopscience.iop.org/article/10.3847/1538-4365/abefe1)). A promoted CTOI gets a TOI number after TOI-team review ([TOI FAQ](https://tess.mit.edu/toi-releases/toi-release-faqs/)). TFOP policy invites the CTOI provider to co-author the first paper ([TFOP publication policy v17](https://tess.mit.edu/wp-content/uploads/TFOPWG_PublicationPolicyv17.pdf)).

TFOP's five subgroups cover SG1 seeing-limited photometry (clearing nearby EBs), SG2 reconnaissance spectroscopy, SG3 high-resolution imaging, SG4 precise RVs and SG5 space photometry ([tess.mit.edu/followup](https://tess.mit.edu/followup)). They mostly serve TOIs. That means a candidate that has not become a TOI depends on a personal collaborator, which is the Dalba/Dragomir pattern [Inferred]. The AAVSO trains amateurs for SG1 ([AAVSO](https://astrodennis.com/AAVSOSupportofTESS.pdf)). Statistical validation means **TRICERATOPS FPP < 0.015 and NFPP < 10⁻³**. "Likely planet" means FPP < 0.5 with NFPP < 10⁻³, and NFPP > 0.1 means a likely nearby false positive ([Giacalone et al. 2021](https://dspace.mit.edu/bitstream/1721.1/134566/2/Giacalone_2021_AJ_161_24.pdf)). Reaching "validated" in practice needs imaging contrast curves and ground photometry [Inferred].

New TESS data come through two routes. **DDT** takes a 2-page request about six weeks before the sector starts, allows up to 500 two-minute targets per sector, has no proprietary period, and expects visibility to be checked with tess-point. The **GI Cycle 9** deadline (10 Mar 2026) has passed, and no Cycle 10 call was found ([MIT DDT page](https://tess.mit.edu/science/ddt); [Cycle 9 text](https://heasarc.gsfc.nasa.gov/docs/tess/docs/TESS_Cycle9_D3CS.pdf)). The publication route has its own constraints. RNAAS is free, moderated rather than refereed, limited to 1,500 words and one figure, and usually out in about 72 hours ([AAS guidelines](https://journals.aas.org/research-note-preparation-guidelines)). The NASA Exoplanet Archive requires an accepted peer-reviewed paper ([criteria](https://exoplanetarchive.ipac.caltech.edu/docs/exoplanet_criteria.html)). Since 21 Jan 2026, arXiv requires unaffiliated new authors to get a **personal endorsement** from an established author ([arXiv blog](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/)). MAST changed its acknowledgement wording on 2 Jul 2026 ([STScI](https://archive.stsci.edu/contents/newsletters/july-2026/changes-to-attributions)).

## Our plan: four niches, frozen code, preregistered tests

### Niche ranking by expected credible yield for 4 cores

The ranking below weighs four things: false-positive prior, how crowded the niche is after the 2026 wave, compute cost on our 4 cores, and how easily a professional can follow up. **All rankings are [Inferred].**

| Rank | Niche | Why it should yield | Compute | Main risk |
|---|---|---|---|---|
| 1 | **Additional planets in known TOI and confirmed multi hosts with many SPOC 2-min sectors**, especially CVZ stars with 10-40 sectors | Multiplicity lowers the false-positive prior (AstroNet/Kepler-90i lesson, multiplicity boost). 2-min PDCSAP is cleaner than QLP. Many sectors make small, long-period signals reachable. Hosts already have TFOP follow-up, so a sponsor exists by construction. eumemic searched TOI hosts only in QLP Sectors 97-105. | Moderate. Use BLS on 10-min binned data, or TLS on fewer stars. About 2,000 stars ≈ 1-2 days. | SPOC multi-TCE search has already looked for extra planets [Unverified]. Edge comes from more sectors and a lower threshold. |
| 2 | **Duo transits across years on FFI-only K and early-M dwarfs**, pairing Cycle 1-3 sectors with sectors ≥ 90 | A verified pipeline blind spot (PHT 73/90 single transits; Pavel's second candidate). A cheap single-event matched filter. Period aliases can be predicted and tested against future sectors with tess-point. | Very cheap, about 1-3 s per star apart from download, so 20,000+ stars in about 1 day | Nearby red dwarfs are already being searched (Pavel's ~20k). Follow-up is hard. Steer toward K and early-M dwarfs at 50-200 pc and Tmag 10-12.5. |
| 3 | **Gaia DR4 (2 Dec 2026) cross-match**: DR4 orbital and acceleration solutions × TESS hosts, our duo list and TOIs | DR4 brings epoch astrometry from 66 months of data ([ESA](https://www.cosmos.esa.int/web/gaia/news-2026)). Gaia-4b is the template. A transit plus an astrometric orbit pins the period and mass. Also a strong false-positive filter (RUWE and orbits flag binaries). | Light: table joins | Expect a race in the first weeks. Astrometric companions need RV. |
| 4 | **Periodic FFI search on M dwarfs**, only on sectors released after eumemic's coverage, with fixed systematics | Our existing pipeline. New sectors are the only edge left. | About 4,900 stars per day | The most crowded niche (4.04M-star search). High duplicate risk. |
| Skip | Archival RV, microlensing, direct imaging, by-eye circumbinary search | Notes show low small-team yield, or collaboration-internal work | | Fragile claims (Barnard 2018) |

### Exact pipeline changes

**`select_targets.py` / `select_targets_wide.py`**
- Add a `--mode` flag with three options:
  - `hosts`: invert the exclusion and keep TOI and `pscomppars` hosts with at least 6 SPOC sectors.
  - `duo`: Teff 3500-5300 K, Tmag 10-12.5, distance 50-200 pc.
  - `mdwarf`: the current behaviour.
- Pull the TIC `contratio` and `d` fields and cut `contratio > 0.1`.
- Join Gaia DR3 RUWE through MAST and flag RUWE > 1.4 (that cutoff is a convention, **[Unverified]**).
- Write each star's sector list and count so stars with only 1 sector are dropped early.

**`prefilter_ffi.py`**
- Keep the current SPOC filter only for modes `duo` and `mdwarf`. In `hosts` mode, *require* SPOC data.
- The dead `if False` line can be removed.

**`run_search.py`**
- Drop the `MIN_SECTOR=90` and latest-4 limits for niches 1-2. Use all sectors, and keep the ≥ 90 limit only for niche 4.
- Prefer `author in ("SPOC", "TESS-SPOC")` PDCSAP over QLP, and add a TGLC HLSP loader from MAST, following eumemic's priority order.
- Keep QLP only as a cross-check, applying the Sector 94-104 orbit-edge exclusion.
- Record the QUALITY bitmask instead of using `QUALITY==0` alone, and keep momentum-dump times so they can be tested later.
- Fix the resume bug. `prev = f"results/none/{shard}.csv"` never matches the file the script writes (`results/new_{shard}.csv`), so resuming never works.
- Replace the hard 3% amplitude / 0.4% scatter skip with a flag, and let the stronger detrending below handle active stars, so spotted M dwarfs are not silently discarded.

**`exosearch.py`**
- Before the biweight, add rotation prewhitening: fit and subtract 3-harmonic Lomb-Scargle sinusoids when P_rot < 3 d, as eumemic does.
- Set the wotan window to 3× the maximum expected duration for the star, not a fixed 0.75 d.
- Replace `duration_ok` with a stellar-density test. Compute T14,max(P, R★, M★) for b = 0 and e = 0, and reject when T_obs > 1.5 × T14,max or T_obs < 0.2 × T14,max. This is the test that killed TIC 161479114 by hand.
- Raise `period_max` to 40 d for multi-sector stars.
- Iterate TLS or BLS: mask each detection and search again, up to 3 signals.
- Add `single_event_search()`: a box matched filter over durations of 1-12 h scaled by stellar density, with SNR ≥ 8 per event and depth 0.1-3%. Reject events within 0.5 d of segment edges or within ±2 h of a momentum dump.

**New `common_mode.py`**
- For each event time, compute the fraction of other targets on the same camera/CCD that dip by more than 3σ at the same time.
- Flag events where more than 5% of stars dip. Do not auto-reject them; route them to manual review.
- Pavel's second candidate shows that SPOC discarded a real-looking event exactly this way, so this check must be applied with judgement in both directions.

**`vet_candidates.py`**
- Use the same sector set as the search; it is currently hard-coded to sectors ≥ 90.
- Add per-sector depth consistency (< 3σ scatter) and a leave-one-sector-out test that predicts transit times and requires recovery at the expected SNR ± 50%.
- Run rotation-alias matching on the *detrended-by-segment* flux, so orbit trends do not dominate `prot`.
- Add TESScut difference-image centroids (MAST is reachable).
- List Gaia neighbours within 2.5′ and compute the depth each neighbour would need to produce the signal (if it would need more than 100%, that neighbour is ruled out).
- Add `pip install leo-vetter` (reachability **[Unverified]**) and record each LEO metric.
- Run TRICERATOPS only with a sanity gate: rerun on each sector separately and on a shuffled-ephemeris control, and reject any FPP that changes by more than 10x between subsets (the eumemic bug).

**`test_injection.py`**
- Expand to a grid: 300 injections per (P, Rp) cell, over P = 1-40 d and Rp = 1-4 R⊕, on real light curves from each niche.
- Freeze the thresholds only after recovery is at least 80% at SNR 10. That beats eumemic's 52-62% and gives a completeness number the paper can report.

### Vetting checklist with thresholds

Thresholds marked [Verified] are cited in the notes. The others are our choices [Inferred]. In every write-up, report the threshold actually used.

| Gate | Pass condition |
|---|---|
| Duplicate | No match within 1% in period and 0.5 d in epoch (or a harmonic) in the NASA Exoplanet Archive `toi` and `pscomppars` tables, eumemic/exoplanets tables, Pavel's gist and the xaviercallens repo. Check ExoFOP CTOIs and Zenodo posts by hand from an unblocked network. |
| Detection | SDE ≥ 9 and SNR ≥ 7.1 for periodic signals (eumemic MES ≥ 7.1 [Verified]). SNR ≥ 8 per event for single and duo events. At least 3 transits for periodic signals. |
| Odd/even | Depth difference < 3σ ([Nigraha](https://arxiv.org/html/2101.09227) [Verified]) |
| Secondary | Depth ratio < 0.10 and < 3σ ([Nigraha](https://arxiv.org/html/2101.09227) [Verified]) |
| Density/duration | 0.2 < T_obs / T14,max < 1.5 |
| Rotation | Prot not within 5% of P, P/2 or 2P. Amplitude flag above 1%. |
| Systematics | Not within ±1 d of 13.7 d (or its harmonics); not on momentum dumps or segment edges; common-mode fraction < 5% |
| Sector consistency | Per-sector depth scatter < 3σ, and leave-one-sector-out prediction recovered |
| Centroid | Difference-image offset < 3σ and < 1 px (21″) ([arXiv 2109.08790](https://arxiv.org/pdf/2109.08790) [Verified]) |
| Neighbours | No Gaia neighbour could produce the depth (required eclipse depth ≤ 100%), or that neighbour is listed for SG1 clearing |
| Binarity | RUWE < 1.4 [Unverified convention]. No EB-catalog or VSX match. No Gaia RV-variability flag. |
| Validation | TRICERATOPS FPP < 0.015 and NFPP < 10⁻³ counts as "validated" only after imaging. FPP < 0.5 is "likely planet". The FPP must pass the sanity gate. |

### Using AI agents responsibly

Pavel's template plus eumemic's errors give five rules [Inferred from both]:

1. **Freeze before you look.** Tag the code (`git tag v1.0-frozen`), hash the light-curve files and thresholds, and only then run the full sample. Any later change creates v1.1, reruns everything, and is logged.
2. **Preregister held-out predictions.** For each surviving candidate, publish predicted transit windows (T0 ± 3σ) for a sector that has not been released yet, or for withheld archival sectors, in a timestamped public commit before the data are opened. Use Pavel's four outcome labels: recovered, inconsistent, excluded, insufficient data.
3. **Adversarial fresh-session review.** Give a new Claude session, and separately a different model, only the candidate packet (light curves, folds, centroid images, the claimed numbers) with this instruction: "Your job is to kill this candidate. List every false-positive scenario and the test that would distinguish it." Track the number of candidates each reviewer kills, and treat any unresolved objection as blocking.
4. **The human makes every call.** Agents write code and run tests. A person signs off on each disposition and on every public statement, and every external fact must link to a primary page (fabricated "KOI-456.04/Dr. Sarah Chen" items have already appeared).
5. **Language discipline.** Use "transit-like signal" or "candidate" until refereed validation, and never assign a lowercase planet letter.

### Engaging professionals under the (possible) new CTOI rule

1. **Verify the rule.** From a network that can reach ExoFOP, read the 2026-08-19 news item and the upload-request form.
2. **Prepare a 2-page packet per candidate**, written in the DDT template style: folds, the checklist table, the preregistration link and the frozen-code DOI.
3. **For niche-1 candidates, write to the authors of the host's existing TOI or validation paper.** They already hold TFOP data, imaging and sometimes RVs, and they are the natural sponsor (Dalba/Dragomir pattern).
4. **For FFI candidates, contact the teams behind FFI vetting tools** (LEO-vetter, QLP faint-star) or TFOP SG chairs. Offer co-authorship and the full packet, and ask for an arXiv endorsement.
5. **In parallel, write a JOSS software paper on the frozen pipeline.** That creates the peer-reviewed methods citation the reported rule needs, then RNAAS notes can follow per candidate.
6. **Request DDT** for any candidate whose next TESS visit (checked with tess-point) is at least 6 weeks away.
7. **Ground photometry.** For transits deeper than about 1%, ask Exoplanet Watch, ExoClock, Unistellar or AAVSO/SG1 observers. Unistellar networks routinely measure 1% depths ([Peluso et al. 2023](https://research.usq.edu.au/download/6b85401bb00c5cb1f8b2e38fa4806b50920273e1504b8dc49e50c61f955925e6/2000373/O%E2%80%99Conner_Peluso_2023_PASP_135_015001.pdf)). Shallower M-dwarf signals need 0.4 m-class telescopes or larger [Inferred].

### Milestones

| Dates (2026-27) | Milestone |
|---|---|
| 4-10 Nov | Implement the pipeline changes above. Run the injection grid. Freeze v1.0. Rerun the old ~400 stars as a regression test (all should still be rejected). |
| 11-18 Nov | Niche 1: about 2,000 multi-sector hosts. Niche 2: 20,000-30,000 duo-search stars. |
| 19-30 Nov | Vetting checklist, duplicate checks, adversarial reviews. Preregister predictions for survivors. Track Pavel's Sector 110 outcome when it is released (as a calibration of the method). |
| 1-2 Dec | Existing reminder. Gaia DR4 opens 2 Dec at 12:00 CET. Run the niche-3 joins within 72 h. |
| Dec | Niche 4 on newest sectors only, if compute allows. Draft the JOSS paper. Send sponsor emails. |
| Jan-Mar 2027 | DDT requests, RNAAS (if the rule allows), watch for a GI Cycle 10 call (by analogy with Cycle 9's March deadline [Inferred]), and test the preregistered predictions as new sectors arrive. |

The **stop rules** are just as important. If niche 1 produces nothing credible from 2,000 hosts at at least 80% injection completeness, publish that null result with completeness limits rather than lowering thresholds. That is a legitimate JOSS/RNAAS-scale result, and it is the honest version of what the 2026 wave did not do [Inferred].

## Conclusion

The question has changed from "can amateurs find exoplanets?" to "can amateurs produce candidates that a professional wants to spend telescope time on?" Search code is now commodity infrastructure. An AI agent writes the search in hours, and dozens of hobbyists ran near-identical BLS searches over the same QLP sectors within weeks of Pavel's post. Scarce value now sits in three places: a niche with a low false-positive prior that others are not fishing, evidence a skeptic cannot dismiss (preregistered held-out recovery, density-consistent durations, clean centroids, sane FPPs), and a relationship with someone who can get imaging and RVs. Pavel's case works not because Claude found a dip, but because he turned the dip into a falsifiable prediction that TESS agreed to test.

For our team, the null result on 400 M dwarfs is useful calibration, not failure. At published candidate rates we should have expected about zero. The dominant rejections (spots, EBs, orbit trends, an impossible duration) point straight at the fixes above. The best odds come from moving to multi-sector known hosts and duo transits now, being ready for Gaia DR4 on 2 December, and building the publication and sponsor pipeline in parallel rather than after a candidate appears. Under the reported 2026 ExoFOP rule, that route will take months even for a perfect signal.
