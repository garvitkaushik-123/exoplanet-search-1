# Pavel Rabtsevich (TIC 4206066) and other AI-assisted amateur exoplanet claims, 2025-2026

**Source access note (read first):** The environment's network policy blocked these sites, which returned DNS failures: scientificamerican.com, zenodo.org, exofop.ipac.caltech.edu, gizmodo.com, cybernews.com, techtimes.com, reddit.com, medium.com, tess.mit.edu, arxiv.org, news.ycombinator.com and explainx.ai. I could read pages directly only on github.com and gist.github.com. Everything attributed below to Gizmodo, Scientific American, Cybernews, X or Reddit comes from search-engine summaries, not from reading the page. Those claims are marked **[search-snippet only]** and should be checked against the originals. The search engine also produced at least one doubtful attribution, noted where it appears.

Read directly:
- Pavel's own gist (primary): https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba
- Two third-party GitHub repos that reproduce or extend his work:
  - https://github.com/xaviercallens/TIC4206066-Exoplanet-Verification
  - https://github.com/eumemic/exoplanets

## Q1. How exactly did Pavel find the candidate? (data, star selection, search, vetting, use of AI)

### Takeaway
The broad steps are documented in Pavel's own gist:
1. He saw a signal in TESS Sector 98.
2. He traced it back to Sectors 32 (2020) and 6 (2018).
3. He used leave-one-sector-out "predict the hidden transits" tests.
4. He ran pixel-level checks on nearby stars, Gaia vetting, TRICERATOPS (FPP about 0.03-0.04) and a cross-match against 36 catalogs and 340,505 TESS alerts.
5. He used Codex and fresh "clean" agent sessions as independent reviewers.
6. He preregistered a Sector 110 test.

I could not verify the exact light-curve product, the search algorithm or the thresholds, because the Zenodo preprint was unreachable. The best proxy is a third-party pipeline that says it "follows" his method and blindly recovered both of his signals: BLS on SPOC, then TESS-SPOC, then QLP light curves, with wotan detrending.

### Cited Findings
**Identity and scale**
- Pavel Rabtsevich is an independent researcher with no astronomy training — [Gizmodo via search](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393) **[search-snippet only]**.
- Sources describe him differently:
  - "Spain-based product manager and space science hobbyist" — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/) **[search-snippet only]**
  - "28-year-old product manager" — Medium summary, https://medium.com/data-science-collective/a-guy-found-a-possible-new-planet-using-claude-1ac935ed822e (unreachable; age unverified)
- He searched TESS data on "more than 126,000 target stars", which flagged TIC 4206066. He then "found an additional 22 instances of dimming" in the archives — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/) **[search-snippet only]**.
  - The 126,000 figure does not appear in his gist — [gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba).
  - I found no source giving the selection criteria for the 126,000 stars (magnitude cut, spectral type, sky region). **Gap.**
- "74 distinct analyses" and "more than 1,000 scripts" testing alternative explanations — [Journal du Geek (French), via search](https://www.journaldugeek.com/2026/10/11/claude-code-internaute-affirme-avoir-trouve-planete-dont-personne-soupconnait-lexistence-lenquete-archives-nasa-secoue-reddit/) **[search-snippet only]**.

**Pavel's own account (gist created 2026-10-07)** — [gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba)
- **Target:** TIC 4206066, "a nearby late-K dwarf about 116 light-years away".
- **Signal A:** P ≈ 3.18 d, depth about 0.04-0.05%, about 1.4 R⊕ if it is on the target.
- **Signal B:** P = 11.13 d, about 2.2 R⊕, "explicitly treated as tentative".
- **Order of discovery:** Signal A was first noticed in TESS Sector 98, then traced back to Sectors 32 and 6.
- **Claude Code's role:** downloading and parsing data, transit-search code, fitting, nearby-star checks, false-positive checks, plotting and reruns.
- **Codex's role:** Codex and "separate clean agent sessions" were used for independent review. This is the adversarial or second-opinion step.
- **Vetting steps he lists:**
  - Leave-one-observation/year-out prediction: fit the other data, predict the hidden transit times, then examine only those windows.
  - Nearby-star and pixel-localization checks.
  - Gaia vetting using astrometry, photometry and radial velocity.
  - TRICERATOPS runs, giving FPP "around 0.03 to 0.04".
  - A search across 36 catalogs or literature sources and 340,505 automated TESS alerts, to rule out prior reports.
- **Self-audit:** an internal audit removed "at least one overstrong statistical claim".
- **Status:** "not statistically validated and not confirmed". The main remaining alternative is an unresolved bound companion, which needs high-resolution imaging and RVs to test.

**Pavel's framing of the AI's role** [search-snippet only]
- Multiple agents "wrote the code, ran it and checked each other's work" — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/).
- "The research itself was mine: the question, the plan, the rules, the computing, the decisions on every candidate and what to publish" — [Gizmodo via search](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393).
- One search summary also said he used "TypeSafe's Jev" alongside Claude Code and Codex. **This looks garbled or hallucinated and I could not verify it. Do not use it.**

**Momentum dumps.** He noticed that the 2018 (Sector 6) dips "tended to align with moments where TESS fired its thrusters, which may have skewed the results" — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/) **[search-snippet only]**. This is an important caveat: momentum-dump systematics coinciding with the transits in one of the three sectors.

**Publications**
- Preprint "Two Transit-like Signals in TESS Photometry of the Nearby K Dwarf TIC 4206066", Zenodo, late Sept 2026:
  - Preprint: doi:10.5281/zenodo.22967456
  - Code and data: doi:10.5281/zenodo.22967099
  - Preregistration: doi:10.5281/zenodo.23175179
  - Source for all three: [gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba). The Zenodo records themselves were unreachable.
  - A search summary cites another DOI, 10.5281/zenodo.22999133, possibly a later version — [search result](https://datasetcatalog.nlm.nih.gov/dataset?q=0003340121) (unverified).
- Reddit post on r/ClaudeAI, 2026-10-07 (thread id 1wzw8zd) — [gist link](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba). The thread was unreachable.

**Independent reproduction: xaviercallens repo** — [repo](https://github.com/xaviercallens/TIC4206066-Exoplanet-Verification)
- Lists Signal A as P = 3.182785 d, about 498 ppm, about 1.4 R⊕, and Signal B as 11.13274 d, about 1000 ppm, about 2.2 R⊕, about 3σ.
- Host star is listed as StKM 1-561.
- Data: MAST TESS FITS for S6, S32 and S98.
- Tests: Mandel-Agol model, odd-even depth, secondary eclipse, centroid decorrelation, stellar-density prior, injection controls (100% recovery reported), leave-one-sector-out timing, and even Lean 4 proofs.
- It reports gate pass/fail verdicts rather than a blind period search.
- It notes `WINDOW_VERIFIED = False` and a status of "AWAITING_SECTOR_110_DATA".

**Proxy for the pipeline: eumemic/exoplanets** — [repo](https://github.com/eumemic/exoplanets)
- The README says its method "follows" Rabtsevich's search, and reports blind recovery of 3.18278 d (vs. his 3.182785 d) and 11.13274 d, Rp = 1.41 R⊕, with a neighbour at 44.6″.
- Light curves: SPOC 2-min PDCSAP, then TESS-SPOC FFI PDCSAP, then QLP.
- Detrending: wotan biweight.
- Search: astropy BLS over 0.5-30 d.
- Thresholds: SNR ≥ 9, at least 3 transits, MES ≥ 7.1.
- Vetting: LEO-Vetter, difference-image centroids, Gaia RUWE and RV, EB catalogs, TRICERATOPS and MOLUSC.
- I could not confirm that Pavel used this exact stack.

### Inferences
- **Probable operating procedure.** The likely workflow was:
  1. Bulk-download public TESS light curves for a large target list, with Claude Code writing the scripts.
  2. Run a periodic-dip (BLS-style) search.
  3. Hand-triage hits.
  4. For the chosen target, stitch archival sectors and do leave-one-out ephemeris prediction.
  5. Run pixel and centroid, Gaia, TRICERATOPS and catalog checks.
  6. Have independent AI sessions (Codex, fresh Claude contexts) audit the claims.
  7. Write up on Zenodo with frozen code and checksums.
  8. Preregister the decisive test and request DDT time.

  The process discipline (preregistration, held-out prediction, adversarial review, audit removing overclaims) is what distinguishes this case.
- The FPP of 0.03-0.04 is above the usual validation threshold of FPP < 0.015. That is consistent with Pavel saying it is "not statistically validated".

### Gaps
- Exact data product (SPOC 2-min vs. FFI/QLP/TGLC; Sector 6 at 30-min cadence would have to be FFI), search algorithm, detrending, and SNR/SDE thresholds: Zenodo and Medium were unreachable.
- The selection criteria for the 126,000 stars are unknown.
- Whether odd-even and secondary-eclipse tests were in Pavel's own analysis (they are in the xaviercallens reproduction).
- Injection-recovery in his own work is unconfirmed.

## Q2. ExoFOP/CTOI status and how the TESS observation was approved

### Takeaway
The TESS observation came through **Director's Discretionary Time (DDT) Program 100**, 2-min cadence in **Sector 110** (2026-10-31 to 2026-11-26). ExoFOP could not be checked, so whether a CTOI or TOI exists is unknown.

### Cited Findings
- "TESS approved DDT Program 100 for 2-minute cadence observations of TIC 4206066 in Sector 110", window 2026-10-31 to 2026-11-26 — [gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba).
  - Expected transits: 9 for Signal A and 3 for Signal B.
  - Preregistered outcomes: recovered, inconsistent, excluded, or insufficient data.
  - Frozen code and checksums are included.
  - Official list: tess.mit.edu/science/ddt/ (unreachable).
- The xaviercallens repo labels the signals "TIC 4206066.01" and ".02" — [repo](https://github.com/xaviercallens/TIC4206066-Exoplanet-Verification). This is TOI/CTOI-style numbering, but it may be the repo's own convention; it is not evidence of an official CTOI.
- The eumemic project uses ExoFOP TOIs/CTOIs only as a catalog for matching and describes no CTOI submissions of its own — [repo](https://github.com/eumemic/exoplanets).

### Inferences
- Pavel took the route a self-funded amateur can take without a telescope: a DDT request to the TESS mission for 2-min data, not a Guest Investigator (GI) cycle proposal.

### Gaps
- ExoFOP page (exofop.ipac.caltech.edu/tess/target.php?id=4206066) was unreachable, so CTOI or TOI status is unknown.
- Any contact with TFOP or professional collaborators is unknown, apart from Laughlin's public comment.
- The text of the DDT justification is unknown.

## Q3. What did experts say, and are there any results from Sector 110?

### Takeaway
The expert reaction was cautiously positive. Laughlin (Yale) called the candidate "solid". Hardegree-Ullman (NASA Exoplanet Science Institute, NExScI) stressed that ruling out false positives is the hard part, and that AI is more useful for chaining together search and vetting code than for confirmation. As of 2026-11-04 I found no reported Sector 110 result. That is expected: TESS data are typically released some weeks after a sector ends, and Sector 110 runs until 2026-11-26.

### Cited Findings
- Kevin Hardegree-Ullman, NExScI: "The biggest challenge with confirming planets is that we have to rule out false-positive scenarios." He said AI tools won't necessarily help with confirmation, but will likely keep being used to chain together public code for searching and basic vetting — [Gizmodo via search](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393) **[search-snippet only; exact wording unverified]**.
- Greg Laughlin (Yale) called the potential for at least one planet "solid" and the work "a great example of human-AI teamwork" — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/) **[search-snippet only]**.
- Gizmodo noted that binary stars can mimic transits and that false-positive checks are still pending — [Gizmodo via search](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393) **[search-snippet only]**.
- Pavel's own caveats:
  - An unresolved bound companion is the main alternative — [gist](https://gist.github.com/MrBoostie/b7a34b9ec96fbfb37e8fd250ba6debba).
  - "Recovering a signal alone would not prove a planet caused it" — [Gizmodo via search](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393).
  - Momentum-dump alignment in the 2018 data — [Scientific American via search](https://www.scientificamerican.com/article/amateur-astronomer-harnesses-ai-to-find-a-possible-hidden-exoplanet/).
- Hype, for context: Ian Nuttall on X, "Holy shit, this guy found an exoplanet using Claude Code! Turns out you can vibe code astronomy now…" — [X](https://x.com/iannuttall/status/2107865515129446467) **[search-snippet only]**. Headlines such as "Don't get too excited, but Claude Code may have just helped discover a new planet" — [daily.dev](https://daily.dev/posts/don-t-get-too-excited-but-claude-code-may-have-just-helped-discover-a-new-planet-mamkaspaw).
- Other coverage I did not read: [Cybernews](https://cybernews.com/tech/claude-code-possible-exoplanet-found-in-nasa-data/), [TechTimes, 2026-10-15](https://www.techtimes.com/articles/329085/20261015/could-ai-discover-new-planet-amateur-astronomer-finds-promising-signal-nasa-data.htm), [The420.in](https://the420.in/pavel-rabtsevich-claude-codex-nasa-exoplanet-discovery-candidate/), [Canaltech](https://canaltech.com.br/inteligencia-artificial/claude-code-pode-ter-sido-usado-para-descobrir-novo-planeta-nasa-analisa/), [Journal du Geek](https://www.journaldugeek.com/2026/10/11/claude-code-internaute-affirme-avoir-trouve-planete-dont-personne-soupconnait-lexistence-lenquete-archives-nasa-secoue-reddit/), [AOL syndication of Gizmodo](https://www.aol.com/articles/did-claude-help-amateur-astronomer-205509000.html).

### Gaps
- No Sector 110 outcome is available as of 2026-11-04.
- No Reddit or Hacker News expert comment threads could be read.
- I found no Anthropic or OpenAI blog post about the case.

## Q4. Pavel's follow-up work: a second candidate (single and duo transits)

### Cited Findings
- X post by @p_rabtsevich, 2026-10-20: "I think I found another planet candidate. And this time, I wanted to figure out why it had been missed." — [X](https://x.com/p_rabtsevich/status/2112644366934446574) **[search-snippet only; thread not read]**. The snippets also say:
  - **Search:** he searched TESS data for about 20k nearby red dwarfs, looking for stars that dimmed only once or twice. Long-period planets look like that and standard searches tend to skip them.
  - **Why it was missed:** NASA's pipeline saw the 2020 dips but discarded the stretch containing the second one, because many stars dimmed at once there (usually a systematic). That led to a wrong period of about 11.5 d.
  - **Size:** about 2.5 R⊕ if it is a planet.
  - **Status:** still a candidate. A hidden close companion is not excluded.
  - **Prior flags:** volunteers "Tonay" and "mhuten" had already flagged the dips by eye (probably Planet Hunters TESS — inference).
  - Source for the size estimate and companion caveat: [Gizmodo-related search summary](https://gizmodo.com/did-claude-help-an-amateur-astronomer-discover-a-new-planet-2000824393).

### Inferences
- Pavel's second approach targets a known blind spot of SPOC and TPS: data flagged or excluded during spacecraft events, plus single and duo transits. The same momentum-dump and quality-flag territory is also a classic source of false positives.

## Q5. Other AI-assisted amateur exoplanet claims, 2025-2026: what worked and what went wrong

### Takeaway
The clearest follow-on case is the **eumemic/exoplanets** project. It began on 2026-10-07, the same day as Pavel's post, explicitly following his method, and grew from 10 signals to 639 "candidates". Its public corrections log is a catalog of the typical failure modes:
- known eclipsing binaries and spectroscopic binaries
- overlap with existing TOIs
- duplicate TIC entries
- a TRICERATOPS setup bug that produced an absurdly low FPP
- data-product artefacts (QLP edges)
- candidates already posted by others on Zenodo

I found no well-documented case of a fully retracted, publicized ChatGPT/Claude exoplanet "discovery" in 2025-2026. Searches for one returned nothing.

### Cited Findings (eumemic/exoplanets) — [repo](https://github.com/eumemic/exoplanets)
- **AI use:** the README does not state that LLM agents were used. The link to Pavel's method and the timing make it part of the same wave, but its AI-assisted status is **unverified**.
- **Sample:**
  - TIC 8.2 dwarfs with T ≤ 11.5, 0.1 < R★ ≤ 0.75 R☉, Teff ≤ 5300 K, observed by QLP in Sectors 97-105: 9,979 stars.
  - Plus 6,430 TOI hosts.
  - Later extended to about 4.04M FGKM dwarfs with T ≤ 13.5, and to periods of 20-100 d.
- **Methods:**
  - 73,226 light curves.
  - wotan biweight detrending, with Lomb-Scargle prewhitening for P_rot < 3 d.
  - Coherent, semi-coherent and stack-slide BLS.
  - Injection recovery of only 52-62% at SNR 10.
- **Vetting:**
  - LEO-Vetter (13 false-alarm and 4 false-positive tests).
  - Per-sector depth consistency.
  - Matching against ExoFOP TOIs/CTOIs, the NASA Exoplanet Archive and SPOC TCEs.
  - Literature check (RAVEN, T16, ExoMiner++).
  - Difference-image centroids.
  - Gaia RUWE and RVs, EB catalogs, VSX and APOGEE.
  - TRICERATOPS plus MOLUSC.
  - Validation threshold: FPP < 0.015 and NFPP < 0.001.
- **Failures and corrections:**
  - TIC 143168991 overlapped TOI-7580.01.
  - TIC 9994636 is a double-lined spectroscopic binary.
  - TIC 235005571 is an Algol-type EB, per an RNAAS note.
  - TIC 212350442 is a likely nearby false positive after a duplicate-TIC fault was fixed.
  - A TRICERATOPS setup bug was found on Oct 15. TIC 160420269 had FPP < 1e-7, but its 200-s data alone gave about 0.4.
  - The QLP artefact fix drops orbit edges in Sectors 94-104.
  - Six candidates had already been posted by others on Zenodo (B. Murray, P. Chopra).
  - Tier letters were renamed (A/B to M/S) on Oct 27, and corrections were made after review of an AJ draft.
  - The tier counts given (M 22, S 290, N 158, L1 111) sum to 581, not the headline 639. This internal inconsistency was not reconciled in the text I read.
- **Community response:** outside reviewers (Josh Gold, Antoine Olivier) opened issues about false positives.

### Other cases
- **Pavel's influence:** a search summary says Pavel's post "pulled other amateurs into planet hunting", raising concern about a flood of amateur candidates. Example: a hobbyist planning a "TESS transit search with Claude Code" — [GitHub issue JohnGavin/llm#1505](https://github.com/JohnGavin/llm/issues/1505) (returned 404 when fetched; content only via search).
- **Probable misinformation:** a search result described a Kepler "KOI-456.04 found with Claude Code" by a "Dr. Sarah Chen". This looks fabricated or unreliable. KOI-456.04 was a 2020 professional (Heller et al.) candidate, and I am stating that from background knowledge, not from a source fetched here. **Do not use.**
- **Base rates for context:**
  - Around 25% false-positive rate for TESS prime-mission TOIs — [arXiv 2205.05073](https://arxiv.org/pdf/2205.05073).
  - 1,185 TESS candidates labelled false positive and 97 false alarms, vs. 666 confirmed — [RAVEN, arXiv 2509.17645](https://arxiv.org/pdf/2509.17645).
  - Professional ML pipelines (RAVEN with over 100 validated planets and over 2000 candidates; ExoMiner++ 2.0) set the bar these amateurs must clear — [RAVEN 2026](https://arxiv.org/pdf/2603.22597), [ExoMiner++ 2.0](https://arxiv.org/html/2601.14877).
- **Unrelated demotions:** 2025 NASA Exoplanet Archive demotions to False Positive (HD 20794 c, 42 Dra b, YSES 2 b) were professional, not AI or amateur — [NASA Exoplanet Archive 2025 news](https://exoplanetarchive.ipac.caltech.edu/docs/2025news.html).

### Inferences
- **What worked:**
  - Preregistered held-out predictions.
  - Explicit "candidate, not planet" language.
  - Public frozen code.
  - Adversarial AI review plus human decision-making.
  - Asking TESS for new data rather than claiming a discovery.
- **What went wrong in the follow-on wave:**
  - Rapid, mass candidate releases with frequently revised counts.
  - Tool-configuration bugs, such as TRICERATOPS producing implausibly confident FPPs.
  - Rediscovered known EBs and TOIs.
  - Duplicate catalog entries.
  - Pipeline artefacts.
  - Priority overlap with other amateurs posting on Zenodo.

### Gaps
- No primary source found for any formally retracted LLM-assisted exoplanet claim in 2025-2026.
- Reddit, Hacker News, ExoFOP and Zenodo were unreachable, so community or TFOP pushback could not be checked.
