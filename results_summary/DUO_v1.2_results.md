# Duo-transit search v1.2: results (2026-11-05)

Sample: 1,181 FFI-only K / early-M dwarfs (Tmag 10–12.5, 50–200 pc), QLP light curves. No errors.
Totals: 462 single events in 257 stars (112 common-mode with duration match), 171 duo pairs, 2 shortlisted duos and 9 multi-transit groups.

**Validation of the v1.2 fix:** TIC 355425863 is now found automatically with all four transits (2018, 2020, 2023, 2025) and P = 139.9606 d. v1.1 found only 2 of them.

## Triage (`duo_v12_triage.csv`, `multi_vet.png`)
| TIC | Type | P (d) | Verdict | Reason |
|---|---|---|---|---|
| 355425863 | multi (4) | 139.961 | real transiting object, **not new** | ESO/FEROS RV follow-up since 2020 (see `TIC355425863_status.md`) |
| 73304157 | multi (6) | 15.657 | **EB** | secondary eclipse at phase 0.5: 2,533 ± 362 ppm (7σ); predicted eclipses missing in sector 100 (timing variations?) |
| 375033375 | multi (3) | 16.615 | **noise** | folding all ~30 covered epochs gives 66 ± 31 ppm, not the 1,396 ppm of the three events |
| 439466626 | multi (3) | 13.721 | systematic | ≈ TESS orbit; all events 1.1–1.3 d after orbit start |
| 238067847 | multi (4) | 13.670 | systematic | ≈ TESS orbit; events at the same orbit phase (spread 0.7 d) |
| 176985273 | multi (4) | 13.523 | systematic | ≈ TESS orbit; 3 of 4 events within 1.4 d of orbit start |
| 41360602 | multi (3) | 13.274 | systematic | ≈ TESS orbit; one event 0.9 d after orbit start |
| 141866573 | multi (3) | 20.479 | systematic (likely) | one event 1.25 d after orbit start; 9-h events |
| 347594070 | multi (3) | 24.065 | systematic (likely) | one event 1.0 d after orbit start; sectors 9/36/63 have the same pointing |
| 354900220 | duo | ≤ 1825 | systematic (likely) | second event 0.8 d after orbit start; 10.5-h duration |
| 277837330 | duo | ≤ 1028 | systematic (likely) | second event 0.9 d after orbit start; dt near an orbit multiple |

**Lesson for v1.3:** start-of-orbit ramps (events 0.5–1.5 d after a segment starts) are the main remaining false-positive source. Add an "orbit-start" flag with a stricter ramp test there, and reject multi-transit periods within 5% of n × 13.7 d.

**Net result: no new planet candidate in this sample.**
