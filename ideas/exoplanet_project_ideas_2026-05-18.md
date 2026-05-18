# Exoplanet Research Project Ideas — May 2026

*Three ambitious, underexplored proposals grounded in public space-mission data*

---

## Project 1: Phantom Rings — A Systematic Search for Exoplanetary Ring Systems Masquerading as Inflated Radii

### Scientific Premise

A long-standing puzzle in exoplanet science is the population of anomalously low-density ("super-puff") planets — worlds whose measured transit radii imply bulk densities well below 0.1 g/cm³, sometimes lower than aerogel. The standard explanation invokes high-altitude photochemical hazes or dusty outflows, but an alternative hypothesis has never been tested at population scale: **some fraction of these objects may be normal-density planets surrounded by optically thick ring systems** that inflate the apparent transit depth. A Saturn-like ring viewed at moderate inclination can increase the effective transit cross-section by 50–200%, converting a Neptune-mass planet into an apparent super-puff. Despite theoretical predictions dating back over a decade, no confirmed exoplanetary ring has ever been detected, and systematic application of ring-transit models to archival photometry remains sparse.

### Target Datasets

- **Kepler long-cadence and short-cadence photometry** (DR25): ~4,700 confirmed/candidate planets, with emphasis on the ~60 known super-puffs and low-density outliers (ρ < 0.3 g/cm³).
- **TESS Full-Frame Images and 2-minute cadence data** (Sectors 1–83): Especially planets with TESS re-observations of Kepler targets, providing a multi-epoch baseline to search for changing ring geometry.
- **Spitzer 4.5 µm secondary eclipse photometry** where available, to constrain thermal emission independently of transit-derived radius.
- **NASA Exoplanet Archive composite planet parameters table** for mass estimates from RV/TTV.

### Novelty

While individual papers have proposed ring models for specific systems (e.g., HIP 41378 f, Kepler-51 b/d), no study has conducted a **uniform Bayesian model comparison** across the full catalog of low-density transiting planets, simultaneously fitting for ring inner/outer radii, inclination, opacity, and planetary radius. The key innovation is treating the ring hypothesis as a competing model against the standard spherical-planet model and computing Bayes factors across the population. This is distinct from previous work that either (a) searched for ring signatures in high-precision individual light curves, or (b) studied the theoretical detectability of rings. The population-level approach could reveal whether the super-puff phenomenon is partially or wholly an observational artifact of unresolved ring systems.

### Concrete Workflow

1. **Sample construction**: Query the NASA Exoplanet Archive for all confirmed/candidate planets with measured mass (RV or TTV) and transit-derived radius, selecting those with bulk density below 0.5 g/cm³ (expected ~80–120 targets). Include a control sample of normal-density planets matched in stellar type and orbital period.
2. **Light curve extraction**: Download detrended Kepler PDC-SAP and TESS SPOC light curves from MAST. For Kepler targets, use the full ~4-year baseline; for TESS, stitch available sectors.
3. **Model fitting**: Implement two transit models — (a) standard Mandel & Agol limb-darkened spherical planet, (b) ringed-planet model using the Zuluaga et al. (2015) or Akinsanmi et al. (2019) fast ring-transit code. Fit both models to phase-folded transits using nested sampling (e.g., `dynesty` or `ultranest`) to obtain Bayesian evidence for each.
4. **Bayes factor ranking**: Compute ln(B_ring / B_sphere) for each target. Flag systems where the ring model is preferred at >3σ equivalent.
5. **Multi-epoch test**: For flagged candidates with multi-year baselines, fit individual epochs to search for secular changes in transit shape consistent with ring precession (expected timescale: years to decades for close-in planets).
6. **Cross-validation**: Compare ring-model-derived "true" planetary radii against mass-radius relations. If the ring hypothesis is correct, the corrected radii should fall on known mass-radius tracks for sub-Neptunes or gas dwarfs.

### Expected Signal / Observable

A ringed planet produces a transit light curve with subtle but diagnostic features: (a) ingress/egress asymmetry if the ring is tilted relative to the transit chord, (b) a slightly flattened transit floor compared to the U-shaped profile of a spherical planet, and (c) wavelength-dependent transit depth if the ring material has chromatic opacity (testable with multi-band Kepler/TESS vs. Spitzer photometry). The most detectable cases are long-period planets (P > 10 days) with high impact parameters (b > 0.5), where the projected ring geometry is most asymmetric.

### Possible False Positives

- **Stellar variability** during transit can mimic ingress/egress asymmetry. Mitigation: use out-of-transit flux as a variability prior; restrict analysis to photometrically quiet stars.
- **Spot-crossing events** produce bumps in transit light curves that could be confused with ring features. Mitigation: model spot crossings explicitly; flag transits with obvious spot signatures.
- **Circumplanetary dust or debris** (not organized into a coherent ring) could produce similar photometric signatures. This is actually scientifically interesting rather than a true false positive — it probes the same physics of circumplanetary material.
- **Systematic noise** in Kepler/TESS photometry at the ~100 ppm level where ring signatures live. Mitigation: injection-recovery tests with synthetic ring transits injected into real light curves.

### Why This Matters

The detection of even one exoplanetary ring system would be a landmark discovery, opening an entirely new subfield of comparative ring science beyond our solar system. At the population level, if rings explain a significant fraction of super-puffs, it would fundamentally revise our understanding of the sub-Neptune mass-radius relation and the physics of atmospheric inflation. It would also constrain the timescales of ring survival under tidal and radiation forces, feeding back into models of satellite formation and planetary obliquity evolution.

---

## Project 2: Tidal Spin-Up Forensics — Mapping the Graveyard of Engulfed Planets via Gyrochronological Anomalies

### Scientific Premise

Gyrochronology — aging stars by their rotation periods — rests on the assumption that stellar spin-down is driven solely by magnetized winds. But tidal interactions with close-in massive planets can **transfer orbital angular momentum to the star**, spinning it up and making it appear younger than its true (isochrone) age. In the extreme case, a planet that spirals inward and is engulfed deposits its entire orbital angular momentum into the stellar convective envelope. This process leaves a forensic signature: **a star that rotates anomalously fast for its independently determined age**. By systematically comparing gyrochronological ages (from rotation periods) to isochrone ages (from spectroscopic T_eff, log g, [Fe/H]) across planet-hosting and non-hosting stars, one could identify a population of stars that have been tidally "rejuvenated" — and by inference, map the demographics of planet engulfment and orbital decay.

### Target Datasets

- **Kepler stellar rotation period catalogs**: McQuillan et al. (2014) catalog of ~34,000 main-sequence rotation periods; Santos et al. (2019, 2021) extended catalogs.
- **TESS rotation periods**: Lu et al. (2024) catalog of ~7,200 cool dwarf rotation periods from the southern CVZ; emerging catalogs from extended mission sectors.
- **Gaia DR3 astrophysical parameters**: T_eff, log g, [Fe/H], luminosity, parallax for isochrone age estimation.
- **LAMOST / APOGEE / GALAH spectroscopic surveys**: Independent spectroscopic parameters and chemical abundances (especially lithium, which is destroyed during main-sequence evolution but could be replenished by planet engulfment).
- **NASA Exoplanet Archive**: Confirmed planet parameters for the subset of stars with known planets.

### Novelty

Previous work has noted the tidal spin-up problem for individual systems (e.g., WASP-18, τ Boo) and shown that gyrochronology breaks down for hot-Jupiter hosts. A 2019 study systematically identified the issue but the analysis was limited to ~20 known hot-Jupiter systems. A 2025 Kepler study found no significant trend between planet occurrence and gyrochronological age but noted anomalies in metal-rich stars. **What has not been done** is a large-scale differential analysis treating the gyro–isochrone age discrepancy itself as the observable of interest, applied to tens of thousands of stars (both with and without known planets), to quantify the statistical excess of "rejuvenated" stars and correlate it with stellar mass, metallicity, and galactic environment. This reframes tidal spin-up from a nuisance parameter into a discovery tool.

### Concrete Workflow

1. **Cross-match catalogs**: Merge Kepler/TESS rotation period catalogs with Gaia DR3 astrophysical parameters and spectroscopic surveys. Require measured P_rot, T_eff (±100 K), log g (±0.1 dex), [Fe/H] (±0.1 dex). Expected sample: ~15,000–25,000 FGK dwarfs.
2. **Compute dual ages**: For each star, derive (a) gyrochronological age using calibrated relations (e.g., Angus et al. 2019; Bouma et al. 2023 stalled spin-down model), and (b) isochrone age using MIST/PARSEC isochrones fit via `isochrones` or `stardate`.
3. **Define the anomaly metric**: Δ_age = log(t_iso) − log(t_gyro). Positive Δ_age indicates the star rotates faster than expected — i.e., it appears gyrochronologically younger.
4. **Population statistics**: Construct Δ_age distributions for (a) confirmed planet hosts (subdivided by planet type: hot Jupiter, warm Neptune, super-Earth, etc.), (b) stars with no detected planets, (c) binary stars (as a control for tidal spin-up from stellar companions).
5. **Regression analysis**: Model Δ_age as a function of stellar mass, [Fe/H], presence/type of planet, orbital period of innermost planet, and galactic kinematics (thin disk vs. thick disk as an age proxy).
6. **Lithium cross-check**: For stars with GALAH/APOGEE lithium abundances, test whether anomalously fast rotators also show lithium enrichment — a predicted signature of recent planet engulfment (Spina et al. 2021).
7. **Forward modeling**: Use tidal evolution codes (e.g., `posidonius`, `ESPEM`) to simulate the expected Δ_age distribution for different planet engulfment rates, comparing to the observed distribution.

### Expected Signal / Observable

Stars that have tidally interacted with or engulfed close-in planets should show a systematic positive Δ_age (rotating faster than their isochrone age predicts). The effect is largest for F-type stars with thin convective envelopes (where a given angular momentum injection produces the greatest spin-up) and for stars whose innermost planet is massive and close-in. The engulfment population should appear as a tail in the Δ_age distribution extending to Δ_age > 0.3 dex (factor of ~2 age discrepancy). A secondary signal is lithium enhancement correlated with the rotation anomaly.

### Possible False Positives

- **Magnetic braking saturation / stalled spin-down**: Stars may naturally maintain rapid rotation longer than classical gyrochronology predicts, particularly for mid-K and M dwarfs. Mitigation: restrict the core analysis to FG dwarfs where gyrochronology is best calibrated; use the Bouma et al. stalled model.
- **Unresolved binary companions**: A close stellar binary can tidally spin up both components. Mitigation: use Gaia RUWE and radial velocity scatter to flag binaries; include binary fraction as a covariate.
- **Stellar youth**: Genuinely young field stars will rotate fast and have consistent gyro/isochrone ages. The anomaly metric specifically isolates discrepancies — stars that are isochrone-old but gyro-young.
- **Isochrone age uncertainties**: Isochrone ages for main-sequence FGK stars are notoriously uncertain (±30–50%). Mitigation: use hierarchical Bayesian modeling to propagate uncertainties; validate on benchmark clusters.

### Why This Matters

This project would provide the first population-level constraint on the **planet engulfment rate** — a critical but poorly measured quantity in planetary system evolution. It connects exoplanet demographics to stellar astrophysics in a novel way, using the star itself as a fossil record of past planetary architecture. The results would constrain tidal dissipation efficiencies (the stellar tidal quality factor Q'★), inform models of hot-Jupiter orbital decay (relevant to TESS detection biases), and potentially identify individual engulfment candidates for detailed follow-up with JWST (atmospheric chemical anomalies) or asteroseismology (interior angular momentum distribution).

---

## Project 3: The Evaporation Cartography Project — Mapping Real-Time Mass Loss Across the Radius Gap Using Archival He 10830 Å and Lyman-α Transit Spectroscopy

### Scientific Premise

The "radius gap" near 1.8 R⊕ is one of the most striking features of the exoplanet population, separating super-Earths from sub-Neptunes. The leading explanation is atmospheric photoevaporation: intense XUV radiation from the host star strips hydrogen/helium envelopes from close-in planets, eroding sub-Neptunes into bare super-Earths. But this hypothesis has been tested primarily through population-level demographics (the distribution of radii and orbital periods), not through **direct measurement of ongoing mass loss** across the gap. The metastable helium triplet at 10830 Å and the hydrogen Lyman-α line are now established tracers of atmospheric escape, and a growing database of detections (and non-detections) exists from ground-based spectrographs and HST. The question no one has systematically answered is: **does the measured mass-loss rate correlate with a planet's position relative to the radius gap in the way photoevaporation theory predicts?**

### Target Datasets

- **He I 10830 Å transit spectroscopy archive**: Compiled from published observations with CARMENES, SPIRou, GIANO-B, NIRSPEC, and JWST NIRSpec/NIRISS. As of early 2026, ~48 systems have reported He I planetary absorption studies (detections and non-detections), with robust equivalent-width or absorption-depth measurements.
- **Lyman-α transit spectroscopy archive**: HST STIS/COS observations of ~15–20 systems with Lyman-α transit detections or upper limits.
- **`sunbather` synthetic spectra database** (Linssen & Oklopčić 2025): A publicly available grid of synthetic atmospheric-escape transmission spectra for nearly every known transiting exoplanet, computed with a self-consistent 1D escape model.
- **NASA Exoplanet Archive**: Planetary radius, mass, orbital period, stellar XUV luminosity estimates.
- **Gaia DR3 + X-ray catalogs (eROSITA, XMM-Newton)**: Stellar XUV flux estimates for normalization.

### Novelty

Individual He 10830 Å and Lyman-α detections have been analyzed case-by-case, but only one study (Dos Santos et al. 2023) attempted a population-level correlation, focusing on the stellar XUV–planetary He I absorption connection. A 2025 study established a robust relationship between the He I feature and stellar EUV emission. **No published work has explicitly constructed the "evaporation landscape"** — the measured mass-loss rate (or its proxy, He I / Ly-α absorption depth) as a function of the planet's position in the radius–insolation plane, overlaid on the theoretical radius gap.** This project would produce the first empirical map of where, exactly, evaporation is actively sculpting the planet population, and test quantitative predictions of photoevaporation vs. core-powered mass loss models.

### Concrete Workflow

1. **Literature compilation**: Build a uniform database of all published He I 10830 Å and Lyman-α transit observations, recording: planet name, R_p, M_p, P_orb, T_eq, measured absorption depth or equivalent width, upper limits for non-detections, stellar spectral type, estimated F_XUV.
2. **Theoretical predictions**: Use the `sunbather` synthetic spectra grid to compute predicted He I absorption for each target in the database, given its known planetary and stellar parameters. This provides a model-dependent mass-loss rate estimate for comparison.
3. **Construct the evaporation map**: Plot measured He I / Ly-α absorption strength as a function of (R_p, F_XUV) — the same parameter space where the radius gap is defined. Color-code by detection significance. Overlay theoretical radius-gap boundaries from the Owen & Wu (2017) photoevaporation model and the Gupta & Schlichting (2019) core-powered mass-loss model.
4. **Statistical tests**: (a) Is there a significant increase in He I absorption depth for planets sitting just above the radius gap compared to those below it? (b) Does the measured absorption correlate more strongly with the photoevaporation or core-powered mass-loss prediction? (c) Are there outliers — planets that should be actively evaporating but show no He I signal (suggesting magnetic shielding or compositional effects)?
5. **Survival analysis**: Many observations yield upper limits (non-detections). Use survival analysis techniques (Kaplan-Meier estimator, Cox proportional hazards) to properly incorporate censored data into the population statistics.
6. **Forward simulation**: Run a Monte Carlo population synthesis of planets evolving under photoevaporation (using `photoevolver` or `EvapMass`), predicting the He I absorption distribution at the current epoch. Compare the simulated distribution to the observed one to constrain the mass-loss efficiency η.

### Expected Signal / Observable

Photoevaporation theory predicts a sharp gradient in mass-loss rate across the radius gap: planets just above it (R ~ 2–3 R⊕, "actively evaporating sub-Neptunes") should show strong He I absorption (equivalent width >5 mÅ), while planets below it (R < 1.5 R⊕, "stripped cores") should show no detectable signal. The gradient should steepen with increasing insolation flux. Core-powered mass loss makes subtly different predictions for the dependence on stellar XUV flux versus bolometric flux, offering a discriminating test. Outlier planets — those above the gap with no He I signal — would point to additional physics like magnetic confinement of the escaping wind.

### Possible False Positives

- **Stellar contamination of He I 10830 Å**: The host star's own chromospheric He I absorption varies with activity, potentially contaminating the planetary signal. Mitigation: use out-of-transit baselines to characterize stellar He I variability; restrict to stars with stable He I profiles.
- **Stellar wind interactions**: The stellar wind can shape the escaping planetary atmosphere, altering the He I transit signature in ways not captured by 1D models. Mitigation: flag planets with evidence of cometary-tail morphology (asymmetric transit signatures) and treat separately.
- **Incomplete XUV flux estimates**: Stellar EUV flux (the primary driver of He I excitation) cannot be measured directly due to ISM absorption and must be inferred from X-ray or UV proxies. Mitigation: use eROSITA X-ray fluxes where available; propagate XUV uncertainty into the analysis.
- **Small sample size**: ~48 systems with He I observations is modest for population statistics. Mitigation: properly account for selection effects (most observations target favorable systems); use the `sunbather` grid to predict what unobserved systems would show, testing for consistency.

### Why This Matters

This project directly tests the physical mechanism responsible for one of the most important features of the exoplanet census — the radius gap — using observational data that already exist. If the evaporation map matches photoevaporation predictions, it would be the strongest evidence to date that XUV-driven mass loss actively sculpts the small-planet population. If it doesn't — if, for example, mass loss is weaker than predicted or shows no correlation with XUV flux — it would strongly favor core-powered mass loss or other mechanisms, redirecting theoretical efforts. Either outcome is a high-impact result. The framework also identifies the most valuable targets for future He I observations with JWST, ANDES/ELT, and other next-generation facilities, maximizing the science return of expensive telescope time.

---

## Summary Table

| # | Project | Key Data | Core Technique | Discovery Potential |
|---|---------|----------|---------------|-------------------|
| 1 | Phantom Rings | Kepler/TESS photometry | Bayesian ring-transit model comparison | First exoring detection; revise super-puff demographics |
| 2 | Tidal Spin-Up Forensics | Kepler/TESS P_rot + Gaia + spectroscopic surveys | Gyro–isochrone age discrepancy analysis | First population constraint on planet engulfment rate |
| 3 | Evaporation Cartography | He I 10830 Å + Ly-α archive + sunbather grid | Mass-loss mapping across radius gap | Empirical test of photoevaporation vs. core-powered mass loss |

---

*Report generated 2026-05-18. All datasets referenced are publicly available through NASA MAST, the NASA Exoplanet Archive, ESA Gaia Archive, and published literature.*
