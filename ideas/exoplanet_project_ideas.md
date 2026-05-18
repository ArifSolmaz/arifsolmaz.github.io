# Ambitious Exoplanet Research Project Ideas

*Generated: May 13, 2026*

---

## Project 1: Mapping Stellar Surface Heterogeneity via Repeated Starspot Occultation Events in Archival Kepler Long-Cadence Data

### Scientific Premise

When a transiting planet crosses a starspot (or facula), it produces a brief brightening (or dimming) bump in the transit light curve. These "spot-crossing events" are routinely flagged as nuisances and masked out during standard transit fitting. But each crossing is actually a spatially resolved probe of the stellar photosphere at a known latitude (set by the transit chord) and a known longitude (set by the timing within the transit). Over hundreds of transits observed by Kepler across 4 years, a single planet repeatedly scans a narrow band of its host star's surface. The idea is to invert this information: reconstruct a longitude-resolved map of spot coverage along the transit chord as a function of time, yielding a "butterfly diagram" analog for stars other than the Sun.

Solar butterfly diagrams (showing how sunspot latitudes migrate over the ~11-year cycle) are foundational to understanding stellar dynamos, yet we have essentially zero equivalent data for other stars. Doppler imaging works only for rapid rotators; starspot modulation in broadband photometry gives rotation periods but no spatial information. Transit-chord spot tomography is the only technique that gives spatially localized spot information on slow-rotating Sun-like stars, and it has been applied in only a handful of individual case studies rather than as a systematic survey.

### Target Datasets

- **Kepler long-cadence (30-min) photometry** for all confirmed transiting planet hosts with orbital periods short enough to yield >50 transits (roughly P < 30 days). This gives ~200-400 systems.
- **Kepler short-cadence (1-min) data** where available, for higher-fidelity bump characterization.
- **Stellar parameters** from Kepler DR25, Gaia DR3 (for effective temperature, radius, and inclination priors).
- **Rotation periods** from McQuillan et al. (2014) and subsequent catalogs, to connect spot evolution to activity cycles.

### Novelty

Individual spot-crossing analyses exist (e.g., Sanchis-Ojeda et al. 2011 on HAT-P-11, Morris et al. 2017 on Kepler-17), but no one has conducted a population-level, homogeneous survey that reconstructs time-resolved spot-coverage maps for hundreds of systems simultaneously. The mainstream approach treats spot crossings as contaminants. Flipping this into a stellar-astrophysics dataset is the key reframing. Furthermore, recent work (2025-2026) on stellar contamination in transmission spectroscopy has highlighted how poorly we understand spot distributions, making this directly relevant to JWST atmospheric retrievals.

### Concrete Workflow

1. Download all Kepler PDC-SAP light curves for systems with >50 transits from MAST.
2. Perform a standard transit model fit (Mandel & Agol) to each transit individually, using the planet's known parameters as priors.
3. Subtract the best-fit transit model to produce residual light curves for each transit epoch.
4. Apply a matched-filter or Gaussian-process bump detector to the residuals to identify spot-crossing events, recording their in-transit phase (which maps to stellar longitude modulo the star's rotation), amplitude (proxy for spot contrast and size), and sign (brightening = dark spot, dimming = bright facula).
5. For each system, build a 2D map: x-axis = stellar longitude (from in-transit timing + known rotation period), y-axis = time (transit epoch). This is the "transit-chord butterfly diagram."
6. Measure spot lifetimes, differential rotation (if the planet's orbital plane precesses or if multiple planets at different impact parameters exist), and any long-term trends suggestive of magnetic cycles.
7. Stack the population to look for statistical trends: do spot-coverage patterns correlate with spectral type, rotation period, or age?

### Expected Signal/Observable

Spot-crossing bumps in Kepler long-cadence data have typical amplitudes of 100-500 ppm for active stars, well above photon noise for Kepler-magnitude targets (Kp < 14). For a system with 100+ transits of a hot Jupiter (transit duration ~2-3 hours, giving ~5-6 long-cadence points in transit), one expects to detect spot crossings in 10-40% of transits for moderately active hosts (log R'HK ~ -4.5). The "butterfly diagram" would show spot-longitude clustering that drifts in phase with the stellar rotation and evolves on timescales of months to years.

### Possible False Positives

- **Instrumental systematics**: Kepler's rolling-band artifact and focus changes can mimic in-transit bumps. Mitigation: use the PDC-corrected data, and require that bumps appear at consistent in-transit phases across nearby epochs (instrumental artifacts would not respect the transit geometry).
- **Planetary atmospheric variability**: For hot Jupiters, changing atmospheric albedo could modulate transit depth, but this would affect the entire transit, not produce localized bumps.
- **TTVs and transit-shape changes from orbital dynamics**: These change ingress/egress shape, not in-transit residuals. Distinguishable by morphology.

### Why It Could Matter

This would be the first systematic "stellar weather map" survey for Sun-like stars, directly constraining dynamo models that currently extrapolate wildly from solar data. It also has immediate practical value: the JWST transmission-spectroscopy community urgently needs empirical spot-distribution priors to correct for stellar contamination (as highlighted by NASA's SAG 21 report). A catalog of spot-coverage statistics as a function of spectral type and activity level would be directly usable as priors in atmospheric retrieval codes.

---

## Project 2: Transit Depth Variation Periodograms as a Blind Survey for Exoplanetary Ring Precession

### Scientific Premise

A ringed exoplanet produces a transit depth that depends on the projected area of the ring system as seen from our line of sight. If the ring plane is tilted relative to the orbital plane (as Saturn's rings are tilted 26.7 degrees relative to its orbit), then the ring undergoes nodal precession driven by the planet's oblate gravitational field and stellar tidal torques. This precession changes the apparent cross-section of the ring+planet system over time, producing a periodic variation in the measured transit depth. The precession period depends on the planet's oblateness (J2), the ring's semi-major axis, and the orbital distance, but for typical hot-to-warm Jupiters it ranges from years to decades, squarely within the combined Kepler+TESS baseline.

A May 2025 study (Umetani et al.) searched 308 TESS candidates for static ring signatures in individual transit shapes and found no convincing detections. But that approach looks for the subtle ingress/egress asymmetry of a ring in a single epoch. The precession-induced depth variation is a fundamentally different observable: it accumulates over many epochs and is detectable as a periodic signal in a time series of transit depths, even when no single transit looks anomalous. This complementary approach appears to be largely untried at population scale.

### Target Datasets

- **Kepler DR25 transit depth measurements** for all confirmed planets with >30 transits (providing a ~4-year baseline).
- **TESS transit depth measurements** from the primary mission through Extended Mission 2 (2018-2026), extending the baseline to ~12 years for targets in the Kepler field that TESS also observed.
- **Combined Kepler + TESS depth time series** for the ~100+ systems observed by both, giving the longest possible baseline.
- **Supplementary**: Ground-based transit surveys (e.g., WASP archival photometry) for even longer baselines on bright targets.

### Novelty

The theoretical framework for ring-precession depth variations was laid out by Ohta et al. (2009) and revisited by Akinsanmi et al. (2020), who estimated that 10-13 systems might be detectable in Kepler/TESS data. Yet no one has actually performed a systematic periodogram search on measured transit-depth time series for hundreds of planets. The Umetani et al. (2025) single-epoch ring search and this precession search are complementary and non-overlapping in methodology. This project would be the first blind survey for ring precession signatures.

### Concrete Workflow

1. For every Kepler planet with >30 transits, extract individual transit depths by fitting each transit epoch independently (allowing depth to float while holding limb-darkening and orbital parameters fixed at their catalog values).
2. Build a time series of transit depths {d_i, t_i} for each planet.
3. Compute a Lomb-Scargle periodogram of {d_i} for each system, searching for periodic signals with periods from ~50 days to ~4 years (the Kepler baseline).
4. For systems also observed by TESS, extend the depth time series and recompute periodograms with the longer baseline, now sensitive to periods up to ~12 years.
5. Assess significance via bootstrapping: shuffle the depth values randomly among the epochs 10,000 times and recompute periodograms to establish a false-alarm probability.
6. For any significant detections, fit a physical ring-precession model (parameterized by ring inner/outer radius, ring optical depth, obliquity, and precession rate) to the depth time series.
7. Cross-check: do the required J2 values and ring parameters fall in physically plausible ranges? Is the precession period consistent with the planet's known mass and orbital distance?

### Expected Signal/Observable

For a Saturn-analog ring system around a warm Jupiter, the peak-to-trough transit depth variation due to ring precession is ~5-15% of the base transit depth (Akinsanmi et al. 2020). For a Jupiter-sized planet with a transit depth of ~1% (10,000 ppm), this corresponds to depth variations of 500-1500 ppm, which is readily detectable in Kepler photometry (typical per-transit depth precision ~50-200 ppm for bright hosts). The signal would appear as a clean sinusoid in the depth time series with a period set by the precession rate.

### Possible False Positives

- **Stellar activity cycles**: Spots and faculae change the effective stellar luminosity and limb-darkening profile, modulating apparent transit depth on timescales of the stellar activity cycle (years). Mitigation: simultaneously fit for a linear or quadratic trend in out-of-transit flux and for correlations between depth and stellar activity indicators (e.g., photometric variability amplitude).
- **Instrumental systematics**: Kepler's quarterly roll changes can introduce depth offsets. Mitigation: include quarter-dependent offsets as nuisance parameters.
- **Blended eclipsing binaries**: Background eclipsing binaries with their own period can produce periodic depth-like variations. Mitigation: check Kepler pixel-level centroid shifts; these would already be flagged in the DR25 vetting.
- **Actual TTVs**: Transit timing variations shift the transit in time but shouldn't change depth unless the impact parameter also varies. Transit duration variations (TDVs) from inclination changes could mimic depth changes; fitting both depth and duration simultaneously can disentangle these.

### Why It Could Matter

Rings are a missing piece of the exoplanet census. We know rings are common in our Solar System (all four giant planets have them), yet zero confirmed exoplanetary rings exist despite thousands of known exoplanets. A detection, or even a strong upper limit from a population-level survey, would constrain ring survival timescales around close-in giants (where tidal forces and Roche limits predict ring destruction) and inform theories of giant planet formation and satellite accretion. The methodology is cheap (archival data only) and the tools (periodograms, transit fitting) are standard, making this highly accessible.

---

## Project 3: A Systematic Census of Anomalous Transit Duration Ratios in Multi-Planet Systems as Probes of Mutual Inclination and Undetected Companions

### Scientific Premise

In a multi-transiting system, the ratio of transit durations between two planets is a strong diagnostic of the system's geometry. For coplanar, circular orbits, the duration ratio depends only on the period ratio and the stellar density (both well-measured). Deviations from this expected ratio directly encode information about mutual orbital inclinations, eccentricities, and the gravitational influence of undetected non-transiting companions.

This "duration ratio" diagnostic was introduced by Fabrycky et al. (2014) and used in early Kepler statistical analyses to show that multi-planet systems are generally quite flat (mutual inclinations ~1-2 degrees). But it has not been revisited with the dramatically improved stellar parameters from Gaia DR3, the extended TESS baseline, or modern N-body dynamical modeling. More importantly, individual systems with anomalous duration ratios have never been systematically followed up as targets of interest for hidden companions. The idea is to perform a population-level screen for "duration ratio outliers" and then use those outliers as a target list for detailed dynamical modeling to predict the masses and orbits of unseen perturbing bodies.

### Target Datasets

- **Kepler DR25 multi-planet systems**: ~700 systems with 2+ transiting planets, with individually measured transit durations.
- **TESS multi-planet systems**: The growing catalog of TESS multi-planet systems (now ~150+), with independent duration measurements.
- **Gaia DR3 stellar parameters**: Precise stellar radii and densities, which are essential to compute the expected duration ratios.
- **Radial velocity archives** (California Legacy Survey, HARPS, ESPRESSO public data): For cross-checking predicted companions against existing RV data.

### Novelty

The original Fabrycky et al. (2014) analysis used Kepler Q1-Q8 data with pre-Gaia stellar parameters (often uncertain by 30-50% in stellar radius). Gaia DR3 has reduced radius uncertainties to ~2-5% for most Kepler hosts, which propagates directly into tighter predicted duration ratios and therefore greater sensitivity to anomalies. No one has re-done this analysis with Gaia-era stellar parameters. Additionally, the original work focused on population statistics (the overall inclination distribution), not on identifying individual outlier systems as dynamically interesting targets. The key innovation is using the duration-ratio diagnostic as a "discovery tool" for hidden planets, rather than merely a population statistic.

### Concrete Workflow

1. Compile transit durations (T14) for all planet pairs in Kepler and TESS multi-planet systems from the NASA Exoplanet Archive.
2. For each pair, compute the expected duration ratio assuming coplanar circular orbits, using Gaia DR3 stellar densities.
3. Compute the observed/expected duration ratio and its uncertainty for every pair.
4. Identify outliers: systems where the duration ratio deviates by >3-sigma from the coplanar-circular prediction.
5. For each outlier, run a grid of N-body simulations exploring: (a) mutual inclination between the known planets, (b) eccentricity of either planet, and (c) the presence of an additional non-transiting planet with a range of masses and periods.
6. Determine which scenario(s) can reproduce the observed duration ratio anomaly while remaining dynamically stable over Gyr timescales (using SPOCK or MEGNO stability maps).
7. For each outlier with a compelling "hidden companion" solution, predict the companion's RV semi-amplitude and check against archival RV data. Flag systems where the predicted companion is detectable with current instruments but hasn't been looked for.
8. Publish a target list of "dynamically interesting" multi-planet systems ranked by the predicted mass and detectability of their hidden companions.

### Expected Signal/Observable

For a system where a non-transiting planet inclines the known planets by ~5 degrees relative to each other, the duration ratio anomaly is typically 5-15% (Fabrycky et al. 2014). With Gaia-era stellar parameters, the expected duration ratio is now known to ~3-5% precision for most Kepler systems, so 5-15% anomalies would stand out at 2-5 sigma. Based on the known Kepler mutual-inclination distribution, one expects roughly 10-30 systems with significant anomalies attributable to undetected companions, out of ~700 multi-planet systems.

### Possible False Positives

- **Residual stellar parameter errors**: Even Gaia DR3 radii have systematics for evolved or spotted stars. Mitigation: use only dwarf stars with well-characterized spectroscopic parameters (logg > 4.0, Teff uncertainties < 100 K).
- **Impact parameter degeneracies**: Transit duration depends on impact parameter, which can be poorly constrained for small planets with grazing transits. Mitigation: restrict to planets with well-measured ingress/egress durations (SNR > 10 per transit) so that impact parameter is independently constrained.
- **Eccentricity mimicking inclination**: An eccentric orbit changes transit duration and can mimic an inclination anomaly. This is not really a "false positive" but rather an alternative explanation that is itself scientifically interesting (eccentric orbits in compact multis also suggest dynamical perturbation). The N-body modeling in step 5 jointly fits both possibilities.
- **Systematics in the transit catalog**: Some durations in the DR25 catalog are measured with automated pipelines that may have biases for shallow or V-shaped transits. Mitigation: re-fit transits independently for all outlier candidates using the raw Kepler pixel data.

### Why It Could Matter

Finding hidden planets via dynamical inference is one of the oldest and most celebrated methods in astronomy (Neptune was predicted this way). Applying it systematically to the Kepler multi-planet population with modern stellar parameters could yield a catalog of predicted companions that are immediately testable with radial velocities or JWST transit searches. It also directly probes the three-dimensional architecture of planetary systems, which is a key observable for planet formation models (e.g., did systems form in a flat disk, or were they dynamically excited by giant planet migration?). This is a "low-hanging fruit" project in the sense that all the data exist and the methodology is straightforward, yet the specific combination of Gaia-era parameters + outlier identification + dynamical follow-up has not been executed.

---

## Summary Table

| Project | Key Data | Primary Observable | Detection Threshold | Estimated Targets |
|---|---|---|---|---|
| Starspot Transit Tomography | Kepler LC/SC | In-transit residual bumps (100-500 ppm) | SNR > 3 per bump | ~200-400 systems |
| Ring Precession Periodograms | Kepler + TESS depths | Periodic depth variation (500-1500 ppm) | FAP < 1% in periodogram | ~10-13 plausible detections |
| Duration Ratio Outlier Census | Kepler/TESS multis + Gaia DR3 | Duration ratio anomaly (5-15%) | >3-sigma deviation | ~10-30 outliers from ~700 systems |

---

## Key References and Resources

- Sanchis-Ojeda et al. (2011) - Starspot occultations in HAT-P-11b transits
- Morris et al. (2017) - Starspot characterization from Kepler-17 transits
- Ohta et al. (2009) - Theoretical framework for ringed planet transits
- Akinsanmi et al. (2020) - Ring precession detectability estimates
- Umetani et al. (2025) - TESS ring search via single-epoch transit shape ([arXiv:2505.05948](https://arxiv.org/html/2505.05948))
- Fabrycky et al. (2014) - Transit duration ratios in Kepler multis
- NASA Exoplanet Archive - [https://exoplanetarchive.ipac.caltech.edu](https://exoplanetarchive.ipac.caltech.edu)
- Rackham et al. (2023) - SAG 21 stellar contamination report ([Oxford Academic](https://academic.oup.com/rasti/article/2/1/148/7081330))
- Lam et al. (2025) - JWST oblateness detection for Kepler-167e ([IOPscience](https://iopscience.iop.org/article/10.3847/1538-3881/ae3a81))
- de Wit & Seager (2025) - Exploring exoplanet dynamics with JWST ([PNAS](https://www.pnas.org/doi/10.1073/pnas.2416189122))
