# ML, archival-reanalysis and non-transit-method exoplanet discoveries from public data (2014-2026): operating procedures

Research note conventions: every bullet in "Cited Findings" has a URL. Items marked **[UNVERIFIED]** come from the researcher's background knowledge and could not be confirmed in this session (arxiv.org was not reachable from the research environment; only search snippets and mirrors were available). Treat them as leads to check, not facts. Date of notes: 2026-11-04.

## Case files: who, when, data, method, vetting, validation, venue, lesson

### Takeaway
The cases that reliably produced new planets from free data shared one procedure: (1) take an existing public product (Kepler/K2/TESS light curves, KOI/TCE lists, HARPS spectra, Gaia epoch astrometry, KMTNet photometry); (2) attack a population the official pipeline under-served (weak multi-planet signals, faint stars, Robovetter-rejected signals, single/duo transits, low-mass-ratio microlensing anomalies); (3) apply a systematic, documented search plus aggressive automated and by-eye vetting; (4) close with a recognised validation step (vespa/TRICERATOPS FPP thresholds, RV, or follow-up photometry).

### Cited Findings

**1. Shallue & Vanderburg / Google AstroNet: Kepler-90i and Kepler-80g (Dec 2017 announcement; AJ 2018)**
- Who/venue: Christopher Shallue (Google) and Andrew Vanderburg (UT Austin), "Identifying Exoplanets with Deep Learning: A Five-planet Resonant Chain around Kepler-80 and an Eighth Planet around Kepler-90", AJ 155, 94 (2018), DOI 10.3847/1538-3881/aa9e09 — [Google Research](https://research.google/pubs/identifying-exoplanets-with-deep-learning-a-five-planet-resonant-chain-around-kepler-80-and-an-eighth-planet-around-kepler-90/); [UT News 14 Dec 2017](https://news.utexas.edu/2017/12/14/using-ai-to-discover-new-worlds)
- Method: convolutional neural network trained on ~15,000 previously human-vetted Kepler signals (TCEs) to classify planet vs false positive; ~96% correct on test set — [UT News](https://news.utexas.edu/2017/12/14/using-ai-to-discover-new-worlds); [NASA](https://science.nasa.gov/universe/exoplanets/discovery-of-eight-planets-makes-alien-system-the-first-to-tie-with-our-solar-system)
- Results: Kepler-90i (~1.3 R_Earth, 14.4 d) made Kepler-90 the first 8-planet system tying the Solar System; Kepler-80g completes a five-planet resonant chain — [NASA](https://science.nasa.gov/universe/exoplanets/discovery-of-eight-planets-makes-alien-system-the-first-to-tie-with-our-solar-system); [AAS Nova](https://aasnova.org/?p=4628)
- Code released openly in March 2018 (AstroNet on GitHub) — [YourStory](https://yourstory.com/2018/03/google-ai-nasa-exoplanets-now-open)
- [UNVERIFIED] Niche: they re-ran a BLS-style search at lower SNR on ~670 stars already known to host multiple transiting candidates (multis have low FP rates), then ranked new signals with the CNN; Kepler-90i was validated statistically with vespa (FPP ~1%) and Kepler-80g via a TTV-consistency / dynamical argument plus multiplicity boost. Check the paper's Sections 6-7.
- Lesson: target the population with the lowest prior false-positive rate (multi-planet hosts) and push the detection threshold just below the official pipeline's.

**2. AstroNet-K2 (Dattilo et al. 2019) and AstroNet-TESS triage/vetting (Yu et al. 2019)**
- Anne Dattilo (UT Austin undergraduate at the time) with Vanderburg, Shallue et al.: "Identifying Exoplanets with Deep Learning. II. Two New Super-Earths Uncovered by a Neural Network in K2 Data" — K2-293b (~2.5 R_E) and K2-294b (~1.7 R_E) — [NASA Discovery Alert](https://science.nasa.gov/universe/exoplanets/discovery-alert-two-new-planets-found-by-ai); [NPR/KUNC](https://www.kunc.org/npr-news/2019-04-01/young-astronomer-uses-artificial-intelligence-to-discover-2-exoplanets); [OUCI record](https://ouci.dntb.gov.ua/works/4OZgAnz7)
- Yu et al. 2019, "Identifying Exoplanets with Deep Learning III: Automated Triage and Vetting of TESS Candidates" (AJ 158, 25): CNN triage (removing obvious FPs, which takes a few humans up to a few days per sector) and vetting; on Sector 6 it presented 288 new signals scored highest by both triage and vetting that human vetters also called PCs — [ar5iv 1904.02726](https://ar5iv.arxiv.org/html/1904.02726)
- AstroNet triage was folded into MIT's Quick Look Pipeline (QLP) — [Kunimoto et al. 2022 PDF](https://research.usq.edu.au/download/80dbc8eb535184c01efad8ed6dc46a801fcb9319a018b62fb8203b0badd6b665/889074/Kunimoto_2022_ApJS_259_33.pdf)
- Lesson: a student with public code and public labels (the training set *is* the past vetting catalogue) can adapt an ML model to a new mission and produce validated planets.

**3. NASA ExoMiner (Valizadegan et al. 2022) and successors**
- ExoMiner: deep neural network, run on NASA's Pleiades supercomputer, trained on Kepler/K2 labels; validated 301 new planets among existing Kepler candidates; paper "ExoMiner: A Highly Accurate and Explainable Deep Learning Classifier that Validates 301 New Exoplanets" (ApJ 2022); announced ~23 Nov 2021; none Earth-like/habitable — [SpaceRef repost of NASA release](https://spaceref.com/?p=22217); [EarthSky](https://earthsky.org/space/new-exoplanets-kepler-data/)
- 301 planets were already pipeline-flagged KOIs nobody had validated — [EarthSky](https://earthsky.org/space/new-exoplanets-kepler-data/)
- Multiplicity boost (Valizadegan et al. 2023, AJ 166, 28): adds multi-KOI system information to ExoMiner V1.2 scores, validating 69 more planets; builds on Rowe et al. 2014 multiplicity framework — [astrobiology.com](https://astrobiology.com/2023/05/multiplicity-boost-of-transit-signal-classifiers-validation-of-69-new-exoplanets-using-the-multiplicity-boost-of-exominer.html); [arXiv html mirror listing](https://arxiv.org/html/2305.02470v2)
- ExoMiner++ (Valizadegan et al. 2025, AJ; arXiv 2502.09790, v4 May 2025): transfer learning from Kepler to TESS 2-min data; of 147,568 unlabelled TCEs, 7,330 classified PCs, mapping to 1,868 existing TOIs, 69 existing CTOIs and **50 new CTOIs**; 1,797 of 2,506 ExoFOP PC TOIs recovered; full vetting catalogue with scores released — [arXiv abs 2502.09790](https://arxiv.org/abs/2502.09790); [IAC publication page](https://iac.es/en/science-and-technology/publications/exominer-enhanced-transit-classification-and-new-vetting-catalog-2-minute-tess-data)
- [UNVERIFIED] ExoMiner validation threshold: score > 0.99 for validation, excluding KOIs with known issues (e.g. flagged contamination, giant-planet radii). Check paper.
- Note: this is institutional (NASA Ames) work, but the released catalogue is a free target list for small teams.

**4. Kepler-1649c: rescuing a Robovetter false positive (Vanderburg et al. 2020)**
- Paper: Vanderburg et al. 2020, ApJL 893, L27, DOI 10.3847/2041-8213/ab84e5 — [ApJL](https://dx.doi.org/10.3847/2041-8213/AB84E5); [ScienceDaily Apr 2020](https://www.sciencedaily.com/releases/2020/04/200416105650.htm)
- Procedure: the Kepler False Positive Working Group visually re-inspected signals the Robovetter had dispositioned as FPs — [AAS Nova](https://aasnova.org/2020/04/22/rescuing-an-overlooked-planet/)
- Failure mode found: signal failed Robovetter's Model-Shift Uniqueness test; the team argued pipeline-induced unusual noise caused the failure, because a true systematic rarely gives a short period with dozens of consistent transits — [AAS Nova](https://aasnova.org/2020/04/22/rescuing-an-overlooked-planet/); [Sky & Telescope](https://skyandtelescope.org/astronomy-news/rescuing-an-overlooked-planet/)
- Result: ~Earth-size planet in the habitable zone of an M dwarf, P ~19.5 d — [Open University](https://www.open.ac.uk/blogs/news/science-mct/new-earth-sized-planet-found-in-habitable-zone/); [McDonald Obs.](https://mcdonaldobservatory.org/node/6481)
- Authors note hundreds more planets may lurk in Kepler data — [Sky & Telescope](https://skyandtelescope.org/astronomy-news/rescuing-an-overlooked-planet/)
- Lesson: automated vetter failures on a single metric are a mine; read the per-metric Robovetter flags (DR25 tables) and re-check those failing one marginal test.

**5. Single- and duo-transit planets; period recovery**
- CHEOPS Duotransit Program (Osborn et al.): pipeline on TESS light curves finds stars with two transits ~2 yr apart (Year 1 + Year 3); ~40,000 stars searched; CHEOPS observes the discrete period aliases to find the true period; five new systems with confirmed periods early on; a later summary counts 19 long-period planets with P > 20 d, Rp < 5 R_E, G < 12 — [EPSC2022 abstract](https://meetingorganizer.copernicus.org/EPSC2022/EPSC2022-499.html); [BAAS 2025](https://baas.aas.org/pub/2025n2i334p07)
- HIP 9618 c: two transits 680 d apart; CHEOPS targeted aliases, P = 52.56349 d (Osborn et al. 2023). HD 15906 c: two transits ~734 d apart, 36 allowed periods, resolved with CHEOPS (Tuson et al. 2023, MNRAS). HD 22946 d: TESS duo, aliases computed then CHEOPS gave P = 47.42489 d (Garai et al. 2023, A&A) — [arXiv 2306.04511 mirror](https://web3.arxiv.org/pdf/2306.04511); [arXiv 2306.04450 mirror](https://web3.arxiv.org/pdf/2306.04450); [DLR elib](https://elib.dlr.de/195694/)
- GOT 'EM survey (Dalba et al.): RV/photometric follow-up of single-transit cool giants; Paper III TOI-2010 b (temperate single-transit Jupiter recovered; Mann, Dalba et al. 2023 AJ); Paper IV long-term Doppler of 11 stars (Dalba et al. 2024 ApJS 271, 16); Paper VI TOI-4465 b from a single Sector 40 transit — [arXiv 2311.10232](https://arxiv.org/pdf/2311.10232); [IPAC](https://ipac.caltech.edu/publication/2024ApJS..271...16D); [astrobiology.com](https://astrobiology.com/2024/01/giant-outer-transiting-exoplanet-mass-got-em-survey-iv-long-term-doppler-spectroscopy-for-11-stars-thought-to-host-cool-giant-exoplanets.html)
- [UNVERIFIED] Foreman-Mackey et al. 2016 (AJ 152, 206) automated search for single/double transits of long-period (2-25 yr) planets in Kepler; ~16 candidates. Not confirmed in this session.
- [UNVERIFIED] TESS Single Transit Planet Candidate (TSTPC) working group: coordinates ground-based photometric/RV recovery of TESS monotransits. Not confirmed.
- Lesson: a single transit is not publishable as a planet alone; the procedure is alias enumeration -> targeted photometry (CHEOPS, ground) or RV. Small teams can find duos in TESS FFIs but need a follow-up partner.

**6. Independent searches of TESS FFIs (faint stars, alternate photometry)**
- TESS Faint-star Search (Kunimoto et al. 2022, ApJS 259, 33): QLP searched all stars T < 13.5 but manual vetting was only done to T = 10.5; an independent vetting pipeline (automated tests + AstroNet triage + manual inspection) on Sectors 1-26 yielded 1,617 new TOIs — [arXiv 2112.02176 (PDF via USQ)](https://research.usq.edu.au/download/80dbc8eb535184c01efad8ed6dc46a801fcb9319a018b62fb8203b0badd6b665/889074/Kunimoto_2022_ApJS_259_33.pdf); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/142259)
- Population: 41 small (< 4 R_E) candidates and 949 hot Jupiters among new TOIs; e.g. TOI-4010 came from this search — [NASA ExoExplorers summary](https://exoplanets.nasa.gov/internal_resources/2728/ExoExplorers_Kunimoto.pdf)
- DIAmante (Montalto et al. 2020 MNRAS 498, 1726): difference-imaging multi-sector FFI photometry + Random Forest; ~977,000 southern FGKM dwarfs in least crowded fields; 396 candidates, 252 new; 39 small (< 4 R_E), 15 new. 2022 follow-up (MNRAS Letters, arXiv 2210.14559): 1.4 million light curves, BLS + RF, 1,160 candidates, 842 new; validation report per candidate; data on CDS/ExoFOP/MAST — [arXiv 2008.09832](https://arxiv.org/abs/2008.09832); [arXiv 2210.14559](https://arxiv.org/abs/2210.14559); [VO resource](https://dc.g-vo.org/rr/q/lp/custom/CDS.VizieR/J/MNRAS/498/1726)
- DTARPS (Melton, Feigelson, Montalto et al.): further ML analysis of ~0.9 million DIAmante light curves — [INAF open access](https://openaccess.inaf.it/handle/20.500.12386/36254)
- TGLC (Han & Brandt 2023, AJ): PSF forward-modelling of FFIs with Gaia DR3 priors to de-blend neighbours; ~0.2% precision at T = 16 in crowded fields; HLSP on MAST and AWS Open Data to T = 16; light curves to T ~ 18 used for M-dwarf giant-planet searches (2025); QLP adopted TGLC photometry (2026 release note) — [arXiv 2301.03704](https://arxiv.org/pdf/2301.03704); [MAST HLSP](https://archive.stsci.edu/hlsp/tglc); [AWS registry](https://registry.opendata.aws/mast-tglc/); [arXiv 2509.08773](https://arxiv.org/pdf/2509.08773); [QLP DRN 004 arXiv 2603.22236](https://arxiv.org/pdf/2603.22236)
- Lesson: the official pipelines vet only the bright end; free HLSPs (QLP, TGLC, DIAmante, eleanor) let a laptop team search fainter stars and submit CTOIs to ExoFOP.

**7. Transit-timing variations (TTV): non-transiting planets**
- Kepler-19c: inferred in 2011 from ~5-min TTVs of Kepler-19b (P = 9.29 d) with ambiguous period (5 d or 100 d) — [CfA](https://www.cfa.harvard.edu/news/invisible-world-discovered); Malavolta et al. 2017 (AJ) combined full-Kepler TTVs + HARPS-N RVs: Kepler-19c P = 28.7 d, 13.1 +/- 2.7 M_E, plus new RV planet Kepler-19d (20.3 M_E, 63 d); warns that ignoring planet-planet interactions biases multi-year fits — [St Andrews portal](https://research-portal.st-andrews.ac.uk/en/publications/the-kepler-19-system-a-thick-envelope-super-earth-with-two-neptun/)
- [UNVERIFIED] KOI-142c (Kepler-88c): Nesvorny et al. 2013 (ApJ 777, 3) predicted a non-transiting ~0.6 M_Jup planet from ~12-h TTVs of KOI-142b; confirmed by SOPHIE RV (Barros et al. 2014). Holczer et al. 2016 / Rowe et al. 2015 published public Kepler TTV catalogues that enable reanalysis.
- Lesson: TTV detections of non-transiting planets are typically degenerate (period/mass) and need either long baselines or RV to close; but public TTV catalogues let a small team search for unrecognised perturbers at near-zero data cost.

**8. Gaia astrometry**
- Gaia-4b and Gaia-5b (Stefansson et al., AJ, announced 4 Feb 2025): first Gaia astrometric companions confirmed with RV (HPF, NEID, and others). Gaia-4b: 11.8 +/- 0.7 M_J, P = 571.3 d around a low-mass star ~244 ly away. Gaia-5b: 20.9 M_J brown dwarf, P = 358.6 d, e = 0.64, ~134 ly. Astrometry alone was insufficient; RV needed for definitive confirmation — [Penn State HPF](https://hpf.psu.edu/2025/02/04/gaia-4-5); [astrobiology.com/NOIRLab](https://astrobiology.com/2025/02/high-precision-neid-spectrograph-helps-confirm-first-gaia-astrometric-planet-discovery.html); [DOAJ abstract](https://doaj.org/article/c95a0f7d662a42fdb00d82891a6e4103)
- Note: a source (Aarhus) attributes the paper to ApJ; the abstract record says AJ — [Aarhus](https://phys.au.dk/en/news/item/artikel/aarhusastronomer-er-med-til-at-bekraefte-en-enorm-exoplanet-1)
- Gaia DR4: **VERIFIED** release date Wednesday 2 December 2026 (announced by ESA 7 May 2026), archive access from 12:00 CET; based on 66 months of data; includes epoch astrometry; ~500 TB, >140 tables; a preview of astrometric time-series data was released June 2026 — [ESA Gaia news 2026](https://www.cosmos.esa.int/web/gaia/news-2026); [TU Dresden](https://tu-dresden.de/bu/umwelt/geo/ipg/astro/observatorium/news/gaia-data-release-4); [NASA Exoplanet Archive Gaia page](https://exoplanetarchive.ipac.caltech.edu/docs/GaiaMission.html)
- Lesson: DR4 epoch astrometry (Dec 2026) is the single biggest new free dataset; the Gaia-4b procedure (astrometric orbit -> RV confirmation) is the template; expect a race in the first weeks after release.

**9. Archival radial-velocity reanalysis**
- HARPS-RVBank (Trifonov et al. 2020, A&A 636, A74): >212,000 systematics-corrected RVs from public HARPS spectra, used by the community to confirm/discover candidates; 2023 update to Jan 2022: 252,615 RVs of 5,239 stars plus Ca II H&K activity — [arXiv 2311.12438](https://arxiv.org/html/2311.12438v2)
- A study mining RVBank for long-period (>1000 d) massive companions of FGK dwarfs reported two Jovian candidates (HD 103891, HD 105779) — [Ariel Univ. preprint ar5iv 2112.09029](https://ar5iv.labs.arxiv.org/html/2112.09029) (authors/venue not confirmed in session)
- Trifonov, Rybizki & Kurster 2019: archival HARPS RVs used to confirm TESS TOI-186 = GJ 143 b (~2 Neptune masses, eccentric) — [arXiv 1812.04501](https://arxiv.org/abs/1812.04501v1)
- Barnard's Star: 2018 233-d candidate (built on combined archival RVs) not supported by ESPRESSO; Barnard b (P = 3.1533 d, m sin i = 0.37 M_E, K = 55 cm/s) published Oct 2024 (Gonzalez Hernandez et al., A&A 690), interior to the habitable zone, with three further candidates — [IAC](https://www.iac.es/en/science-and-technology/publications/sub-earth-mass-planet-orbiting-barnards-star); [ESO PDF](https://eso.org/public/archives/releases/sciencepapers/eso2414/eso2414a.pdf). Basant et al. 2025 (ApJL 982, L1, March 2025) combined 112 MAROON-X RVs (~30 cm/s) with *published* ESPRESSO RVs to confirm four sub-Earths (b, c, d, e; e at 6.739 d confirmed by the combination; c less robust) — [ADS](https://ui.adsabs.harvard.edu/abs/2025ApJ...982L...1B/abstract); [AAS Nova](https://aasnova.org/2025/03/11/confirmed-at-last-barnards-star-hosts-four-tiny-planets/)
- [UNVERIFIED] Proxima d (Faria et al. 2022, A&A) came from ESPRESSO GTO data, not archival reanalysis; not checked.
- Lesson: archival RV mining yields long-period giant candidates cheaply, but small-planet claims from heterogeneous archives are fragile (Barnard 2018); public RVs are best used to confirm or combine, not to claim Earth-mass planets alone.

**10. Microlensing archive (KMTNet)**
- KMTNet AnomalyFinder: semi-automated re-search of each season's photometry; finds planets missed by eye (e.g. only 1 of 5 non-caustic q < 1e-3 anomalies found by eye); 112 unambiguous planets from 2016-2019; ~45 "hidden" planets (~1/3 of 2016-2022 microlensing planets); series up to Paper XIII (2021 prime fields, arXiv 2605.17053); separate "Systematic Reanalysis" series with improved photometry found four new planet-like anomalies — [arXiv 2401.04256](https://arxiv.org/pdf/2401.04256); [arXiv 2605.17053](https://arxiv.org/pdf/2605.17053); [NSF PAR reanalysis II](https://par.nsf.gov/biblio/10654669-systematic-reanalysis-kmtnet-microlensing-events-ii-two-new-planets-giant-source-events)
- No small/independent-team microlensing discovery from public KMTNet/OGLE/MOA data was found; this work is done by the KMTNet collaboration itself.

**11. Direct-imaging archive**
- Lafreniere et al. 2009 (ApJ 694, L148) detected HR 8799 b in 1998 HST/NICMOS archival images with LOCI-type PSF subtraction — [ADS](https://ui.adsabs.harvard.edu/abs/2009ApJ...694L.148L/abstract)
- Soummer et al. 2011 recovered three HR 8799 planets in 1998 NICMOS data using a ~466-image archival PSF reference library (ALICE program); planned ~400 more archival stars — [phys.org](https://phys.org/news/2011-10-astronomers-elusive-planets-decade-old-hubble.pdf); [enewspf](https://enewspf.com/?p=77878)
- These are recoveries of known planets (pre-2014), useful for orbit baselines; no new planet discovered by a small team from archival imaging was found in this session.

### Inferences
- Pattern: almost every success here exploited a documented gap in an official pipeline (vetting depth limit T = 10.5 in QLP; Robovetter single-metric failures; BLS SNR threshold in Kepler; by-eye microlensing review; single transits excluded from period-folded searches).
- Training labels for ML come free from the mission's own disposition tables; the expensive part is follow-up, not computation.

### Gaps
- Exact validation statistics for Kepler-90i / Kepler-80g and ExoMiner thresholds could not be verified (arxiv.org unreachable).
- No sources found on TSTPC working group procedures or on Foreman-Mackey 2016 in this session.

## Which niches had the best discovery yield per effort for non-institutional teams?

### Takeaway
Highest yield per effort: (a) independent searches/vetting of TESS FFI light curves for faint or crowded stars, submitted as CTOIs; (b) re-examining Kepler/TESS automated false-positive dispositions and low-SNR signals in known multi-planet systems; (c) running public ML classifiers (AstroNet, ExoMiner++ catalogue) over public TCE lists. Gaia DR4 (2 Dec 2026) is the newest opportunity. RV, microlensing and imaging archives yield little to small teams without partner facilities.

### Cited Findings
- One team's independent vetting of QLP FFI signals produced 1,617 new TOIs — [Kunimoto 2022](https://research.usq.edu.au/download/80dbc8eb535184c01efad8ed6dc46a801fcb9319a018b62fb8203b0badd6b665/889074/Kunimoto_2022_ApJS_259_33.pdf)
- DIAmante: 842 new candidates from 1.4M light curves — [arXiv 2210.14559](https://arxiv.org/abs/2210.14559)
- ExoMiner++ yielded 50 new CTOIs from already-public TCEs — [arXiv 2502.09790](https://arxiv.org/abs/2502.09790)
- An undergraduate's AstroNet-K2 work produced two validated planets — [NASA](https://science.nasa.gov/universe/exoplanets/discovery-alert-two-new-planets-found-by-ai)
- Re-inspection of Robovetter FPs produced Kepler-1649c — [AAS Nova](https://aasnova.org/2020/04/22/rescuing-an-overlooked-planet/)
- Gaia DR4 on 2 Dec 2026 with epoch astrometry — [ESA](https://www.cosmos.esa.int/web/gaia/news-2026)
- KMTNet hidden-planet yield is high (~1/3 of planets) but is done in-collaboration — [arXiv 2401.04256](https://arxiv.org/pdf/2401.04256)

### Inferences
- Candidate yield (CTOIs) is cheap; *validated planet* yield needs either a statistical-validation pipeline (TRICERATOPS + high-resolution imaging from ExoFOP) or partner RV time. Small teams should plan for candidates -> CTOIs -> collaboration.
- Note that most "small team" cases above are small groups inside institutions (UT Austin, MIT, NASA Ames); truly non-institutional discoveries in these niches were not found here.

### Gaps
- No quantitative "planets per person-hour" comparison exists in the literature found.

## What validation thresholds and tools did they use?

### Takeaway
TRICERATOPS: validated if FPP < 0.015 and NFPP < 0.001; vespa-era Kepler convention FPP < 1% [unverified in-session]; ML scores (ExoMiner) treated as probabilities with a high cutoff; multiplicity boost for multi-planet systems; single/duo transits and astrometric/TTV signals need RV or targeted photometry.

### Cited Findings
- TRICERATOPS (Giacalone et al. 2021, AJ 161): validated planet FPP < 0.015 and NFPP < 1e-3; likely planet FPP < 0.5 and NFPP < 1e-3; likely nearby FP NFPP > 0.1; on 384 TOIs: 12 validated, 125 likely planets, 52 likely NFPs — [arXiv 2002.00691](https://arxiv.org/abs/2002.00691v2); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/134566?show=full)
- TRICERATOPS+ adds multi-colour transit photometry (2025) — [arXiv 2508.02782](https://arxiv.org/abs/2508.02782)
- Multiplicity boost, Rowe et al. 2014 framework applied to ExoMiner — [astrobiology.com](https://astrobiology.com/2023/05/multiplicity-boost-of-transit-signal-classifiers-validation-of-69-new-exoplanets-using-the-multiplicity-boost-of-exominer.html)
- Robovetter metric (Model-Shift Uniqueness) can wrongly reject — [AAS Nova](https://aasnova.org/2020/04/22/rescuing-an-overlooked-planet/)
- Gaia companions: RV required for definitive confirmation — [DOAJ abstract](https://doaj.org/article/c95a0f7d662a42fdb00d82891a6e4103)
- Duotransits: CHEOPS alias observations — [EPSC2022](https://meetingorganizer.copernicus.org/EPSC2022/EPSC2022-499.html)

### Inferences
- The "0.15%" figure in the brief likely corresponds to 0.0015 or confusion with TRICERATOPS's 1.5%; no source found for a 0.15% standard.

### Gaps
- vespa threshold (FPP < 1%) and DAVE usage not verified in-session; [UNVERIFIED] Morton et al. 2016 used FPP < 1% for 1,284 Kepler validations; DAVE (Kostov et al. 2019) is a centroid/odd-even vetting tool for K2/TESS.

## What false positives plagued them and how were they removed?

### Takeaway
Main contaminants: eclipsing binaries (on-target and nearby/blended, especially with 21" TESS pixels), instrumental systematics and pipeline-induced noise, stellar variability, period aliases (duo transits), and stellar activity in RV.

### Cited Findings
- Triage removes obvious FPs; manual triage costs humans days per sector — [Yu et al. 2019](https://ar5iv.arxiv.org/html/1904.02726)
- Faint stars / crowded fields: 21" TESS pixels cause contamination; TGLC PSF fitting with Gaia priors removes neighbour flux — [Han & Brandt 2023](https://arxiv.org/pdf/2301.03704)
- DIAmante restricted to least-crowded regions to limit blends — [arXiv 2008.09832](https://arxiv.org/abs/2008.09832)
- NFPP (nearby false positive) as separate criterion — [Giacalone 2021](https://arxiv.org/abs/2002.00691v2)
- Pipeline noise causing false *rejection* (Kepler-1649c) — [Sky & Telescope](https://skyandtelescope.org/astronomy-news/rescuing-an-overlooked-planet/)
- Period aliases in duotransits (e.g. 36 allowed periods for HD 15906 c) — [arXiv 2306.04450](https://web3.arxiv.org/pdf/2306.04450)
- RV activity false positives: Barnard 233-d candidate not supported by ESPRESSO — [IAC](https://www.iac.es/en/science-and-technology/publications/sub-earth-mass-planet-orbiting-barnards-star); RVBank 2023 adds activity indicators — [arXiv 2311.12438](https://arxiv.org/html/2311.12438v2)
- TTV degeneracy (Kepler-19c period ambiguous 5 vs 100 d until RV) — [CfA](https://www.cfa.harvard.edu/news/invisible-world-discovered)

### Inferences
- A laptop team's essential checks: odd/even depth, secondary eclipse, centroid offset / difference image, Gaia neighbour contamination, period-alias analysis, then TRICERATOPS.

### Gaps
- Fraction of CTOIs from small FFI searches later found to be FPs was not found.

## How long from first signal to accepted paper?

### Takeaway
ML-on-archive papers: months to ~1 year from submission to acceptance; validation-by-follow-up cases take years (TTV 2011 -> 2017; Barnard 2024 -> 2025; duotransit 2 yr baseline + CHEOPS).

### Cited Findings
- AstroNet: announced 14 Dec 2017; AJ 155, 94 (2018) — [UT News](https://news.utexas.edu/2017/12/14/using-ai-to-discover-new-worlds)
- TRICERATOPS: arXiv Feb 2020 -> AJ 2021 — [arXiv 2002.00691](https://arxiv.org/abs/2002.00691v2)
- Kunimoto faint-star: arXiv Dec 2021 (2112.02176) -> ApJS March 2022 — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/142259)
- ExoMiner++: arXiv Feb 2025 (2502.09790) -> v4 May 2025, AJ — [arXiv](https://arxiv.org/abs/2502.09790)
- Kepler-19c: TTV inference 2011 -> period/mass with RV in 2017 — [CfA](https://www.cfa.harvard.edu/news/invisible-world-discovered); [St Andrews](https://research-portal.st-andrews.ac.uk/en/publications/the-kepler-19-system-a-thick-envelope-super-earth-with-two-neptun/)
- Barnard: Oct 2024 (one planet + 3 candidates) -> March 2025 four confirmed — [IAC](https://www.iac.es/en/science-and-technology/publications/sub-earth-mass-planet-orbiting-barnards-star); [ADS](https://ui.adsabs.harvard.edu/abs/2025ApJ...982L...1B/abstract)
- Duotransits require ~2 yr gap between TESS visits then CHEOPS season(s) — [EPSC2022](https://meetingorganizer.copernicus.org/EPSC2022/EPSC2022-499.html)
- Kepler-1649: Kepler data (2009-2013) -> planet paper April 2020 — [ScienceDaily](https://www.sciencedaily.com/releases/2020/04/200416105650.htm)

### Inferences
- Statistical-validation papers on public data can go from search to submission in a few months; anything needing RV adds 1-3+ years.

### Gaps
- Internal "first signal" dates for most cases are not published.
