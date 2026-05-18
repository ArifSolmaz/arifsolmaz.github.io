# Ambitious Exoplanet Research Project Ideas

**Generated: April 7, 2026**
*Automated report from scheduled exoplanet research strategist task*

---

## Project 1: Galactic Chronochemistry of Planet Formation — Do Exoplanet Occurrence Rates Carry a Fossil Record of the Milky Way's Chemical Evolution?

### Scientific Premise

We know that giant planet occurrence scales with host-star metallicity, and that sub-Neptune occurrence may be less metallicity-dependent. But metallicity is only one axis. Thanks to TESS asteroseismology (now delivering ages for >130,000 red giants) and Gaia+APOGEE/GALAH spectroscopic surveys, we can now assign precise ages *and* multi-element abundance patterns ([Ce/Mg], [Zr/Ti], alpha-element ratios) to large samples of planet-hosting stars. The underexplored question: **does the occurrence rate and architecture of planetary systems vary as a function of Galactic birth environment, traced through chemical clocks rather than bulk metallicity alone?** In other words, can we read a "fossil record" of planet formation conditions in the Milky Way's chemodynamical substructure?

### Target Datasets

- **NASA Exoplanet Archive** confirmed planets from Kepler, K2, and TESS
- **TESS asteroseismic catalogs** (~132,000–158,000 red giants with inferred ages from Mackereth et al. 2025, Hon et al. 2025)
- **Gaia DR3** astrometry + radial velocities for kinematic group assignment
- **APOGEE DR17** and **GALAH DR3** for detailed chemical abundances (15–30 elements per star)
- **Kepler stellar properties catalog** cross-matched with the above

### Novelty

Most exoplanet–metallicity studies collapse stellar chemistry to [Fe/H]. A few recent papers have begun exploring alpha-element trends, but the systematic use of *chemical clocks* (s-process-to-alpha ratios like [Ce/Mg]) as age proxies — in tandem with asteroseismic ages — to build a time-resolved, chemically-resolved planet occurrence map across Galactic populations is largely unexplored. This turns exoplanet demographics into a tool for Galactic archaeology, and vice versa.

### Concrete Workflow

1. Cross-match the Kepler/K2/TESS planet host catalogs with APOGEE DR17 and GALAH DR3.
2. Assign stellar ages using (a) asteroseismic scaling relations where oscillations are detected and (b) chemical clock calibrations ([Ce/Mg] vs. age) for the broader sample.
3. Classify stars into chemodynamical populations: thin disk, thick disk, high-alpha metal-poor, Gaia-Enceladus debris, etc., using [alpha/Fe] vs. [Fe/H] and orbital actions from Gaia.
4. Compute completeness-corrected planet occurrence rates (using injection-recovery statistics from Kepler/TESS pipelines) binned by stellar age, birth [Fe/H], [alpha/Fe], and Galactic population membership.
5. Test specific hypotheses: (a) Do thick-disk stars (formed 8–12 Gyr ago in a more turbulent ISM) host fewer close-in sub-Neptunes? (b) Is there an age threshold below which hot Jupiter occurrence drops, potentially reflecting disk migration timescale dependencies? (c) Do stars from accreted satellite populations (Gaia-Enceladus) show anomalous planet occurrence consistent with their distinct chemical enrichment history?

### Expected Signal / Observable

A statistically significant variation in planet occurrence (particularly for giant planets and sub-Neptunes) as a function of stellar age and chemodynamical population, *beyond* what is explained by [Fe/H] alone. Predicted effect size: factor of ~2–3 variation in giant planet occurrence between thin-disk and thick-disk populations at matched metallicity, detectable with the ~4,000+ planet hosts that should have APOGEE/GALAH coverage.

### Possible False Positives

- Systematic age errors from chemical clocks propagating into spurious trends (mitigated by cross-checking against asteroseismic subsample).
- Selection biases: evolved stars in asteroseismic samples may preferentially lose close-in planets to engulfment, creating a fake age–occurrence anti-correlation.
- Completeness correction errors if detection efficiency varies systematically with stellar type across Galactic populations.

### Why It Matters

If planet formation efficiency carries an imprint of the Galaxy's chemical evolution, it would (a) provide a new constraint on planet formation models sensitive to disk composition beyond iron, (b) inform target prioritization for future biosignature searches (should we look at young thin-disk stars or old thick-disk stars?), and (c) establish exoplanet science as a quantitative probe of Galactic archaeology — a genuine cross-disciplinary bridge.

---

## Project 2: Systematic Search for Exoplanetary Ring Systems via Ingress–Egress Morphology Decomposition in Kepler Long-Cadence Data

### Scientific Premise

Despite Saturn being one of our solar system's most visually iconic objects, **no exoplanetary ring system has been confirmed around a transiting planet**. Previous searches have focused on anomalous transit depth (a ringed planet mimics a larger planet) or gross light-curve shape. However, a ring system's most diagnostic signature is subtler: the *morphology* of ingress and egress should differ from a spherical planet because the ring's projected cross-section is not circularly symmetric. A tilted ring produces a characteristic asymmetry — the ingress and egress durations differ, and the curvature of the light curve during these phases departs from the standard limb-darkening model. This has been modeled theoretically but never systematically exploited across a large sample with modern Bayesian inference.

### Target Datasets

- **Kepler DR25** long-cadence and short-cadence light curves for all confirmed and candidate giant planets (R > 6 R_Earth) with well-sampled transits
- **TESS** full-frame image light curves for bright giant planet hosts (for independent validation)
- **Spitzer** secondary eclipse and phase curve data where available (to constrain thermal emission and break ring-vs-oblateness degeneracy)

### Novelty

A 2025 TESS-based search of 308 candidates found 6 statistically favored ringed models, but none was conclusive — partly because TESS's 2-minute cadence and shorter baselines limit ingress/egress sampling. Kepler's 4-year baseline and ~1-minute short-cadence mode for many targets provide far superior ingress/egress morphology constraints. The key novelty here is **not just searching for rings, but building a hierarchical Bayesian framework** that simultaneously fits for planetary oblateness, ring optical depth (as a function of wavelength if multi-band data exist), ring inclination, and ring inner/outer radii — while marginalizing over stellar limb darkening and instrumental systematics. This converts each non-detection into a quantitative *upper limit* on ring size/opacity, enabling population-level statements (e.g., "fewer than X% of warm Jupiters host Saturn-like ring systems").

### Concrete Workflow

1. Select all Kepler giant planets with at least 10 well-observed transits (to enable phase-folding for high-SNR ingress/egress profiles). Expected sample: ~200 systems.
2. Implement a fast analytic transit+ring model (building on Zuluaga et al. 2015's framework) in a differentiable code (JAX/NumPyro) to enable gradient-based Bayesian inference.
3. For each system, fit four nested models: (a) spherical planet, (b) oblate planet, (c) spherical planet + ring, (d) oblate planet + ring. Use Bayesian model comparison (evidence ratios) to rank.
4. For the top candidates, validate against TESS data (different bandpass → different ring opacity if rings are icy/dusty) and check for secondary eclipse depth anomalies (a ring would increase geometric albedo).
5. Compile population-level ring occurrence rate upper limits as a function of planet mass, orbital period, and stellar irradiation.

### Expected Signal / Observable

For a Saturn-analog ring (1.5–2.5 planetary radii, optical depth ~0.5) around a Jupiter-sized planet at 0.1–1 AU, the ingress/egress asymmetry is ~50–200 ppm above the symmetric model — detectable in phase-folded Kepler short-cadence data at 2–5 sigma for bright hosts. Even non-detections constrain ring properties: the population-level statement "warm Jupiters have ring occurrence <5% at 95% confidence" would be a publishable first.

### Possible False Positives

- Starspot crossings during ingress/egress can mimic asymmetry (mitigated by requiring consistent asymmetry across many epochs and checking for spot-induced chromaticity in multi-quarter data).
- Planetary oblateness produces a similar but subtly different ingress/egress signature (mitigated by fitting both oblate and ringed models simultaneously).
- TTVs causing slight epoch-to-epoch transit shape variations that, when phase-folded, produce spurious asymmetries (mitigated by fitting individual transit times before folding).

### Why It Matters

Rings are a natural outcome of tidal disruption, giant impacts, and satellite dynamics — all processes fundamental to planetary system evolution. A population-level constraint on ring occurrence would test theories of ring longevity (are rings transient or stable over Gyr?), inform models of satellite formation around giant exoplanets, and — if a detection is made — open an entirely new phenomenology for characterization with JWST transmission spectroscopy through ring material.

---

## Project 3: Mapping Tidally Driven Weather — Detecting Orbital-Phase-Locked Atmospheric Variability in Eccentric Hot Jupiters Using Multi-Epoch TESS Phase Curves

### Scientific Premise

Most thermal phase curve studies target *circular-orbit* hot Jupiters, where the dayside–nightside temperature contrast is quasi-static. But **eccentric hot Jupiters** experience dramatically time-varying irradiation: at periastron, the planet receives a flash of intense stellar heating, then "relaxes" as it swings to apastron. General circulation models (GCMs) predict that this should drive *transient weather events* — shock fronts, episodic cloud formation/dissipation, and superrotating jet spin-up/spin-down — that repeat every orbit but may vary in amplitude from orbit to orbit due to chaotic atmospheric dynamics. This orbit-to-orbit variability in the phase curve has never been systematically measured.

### Target Datasets

- **TESS Extended Mission** continuous viewing zone data for eccentric (e > 0.1) giant planets observed over multiple sectors (providing dozens of orbital phase curves per target)
- **JWST** NIRSpec/G395H or MIRI/LRS phase curve observations of eccentric systems (HAT-P-2b, HD 80606b, TOI-5800b) for spectroscopic decomposition
- **Spitzer** archival 4.5 µm phase curves for eccentric systems (HAT-P-2b has 3 full orbits)
- **Kepler** long-cadence data for Kepler-419b, Kepler-693b, and other eccentric giants

### Novelty

Existing phase curve analyses treat each orbit as a realization of the same signal and stack them for SNR. The novel angle here is to **treat orbit-to-orbit variations as the signal itself**: measure the *variance* and *covariance structure* of the phase curve amplitude, hotspot offset, and ingress/egress brightness across many orbits. This is a second-order statistic (variability of variability) that GCMs predict but observers have not yet systematically extracted. TOI-5800b, highlighted in 2025 as a tidal-heating laboratory, is an ideal anchor target. The approach is analogous to exoplanet "weather mapping" but uses temporal rather than spatial decomposition.

### Concrete Workflow

1. Identify all eccentric (e > 0.1) transiting giant planets with TESS multi-sector coverage providing >15 full orbital phase curves. Cross-reference with Spitzer and Kepler archives. Expected sample: 8–15 systems.
2. For each system, extract individual-orbit phase curves using a Gaussian process (GP) model to deconvolve stellar variability (rotation, spots) from planetary signal. Key: the planetary signal is periodic at the *orbital* period while stellar variability operates at the *rotation* period — they are generally incommensurable, enabling separation.
3. Fit each individual-orbit phase curve with a low-order spherical harmonic brightness map (2–3 parameters: amplitude, phase offset, asymmetry). Record the posterior distributions per orbit.
4. Compute the orbit-to-orbit scatter in these parameters. Compare against (a) the expected scatter from photon noise + systematics alone (null hypothesis: no atmospheric variability), and (b) GCM predictions for the specific system's orbital parameters.
5. For targets with detected variability, characterize the *autocorrelation timescale* of the variability — is the atmosphere "remembering" its state from one orbit to the next (long radiative timescale) or fully resetting (short radiative timescale)? This directly constrains the atmospheric radiative time constant.

### Expected Signal / Observable

GCMs for eccentric hot Jupiters (e.g., Kataria et al. 2013, Lewis et al. 2014) predict orbit-to-orbit hotspot offset variations of ~5–15 degrees and peak flux variations of ~5–10% of the phase curve amplitude. In TESS bandpass for a system like HAT-P-2b (V~8.7), a single-orbit phase curve semi-amplitude is ~50 ppm; orbit-to-orbit variations of ~5 ppm should be detectable at 2–3 sigma with 20+ orbits from TESS extended mission data. The radiative timescale measurement (from autocorrelation) would be a first-of-its-kind observable.

### Possible False Positives

- Stellar variability at harmonics of the rotation period could mimic orbit-to-orbit changes if the orbital and rotation periods are near-commensurate (mitigated by GP detrending and checking for correlation with stellar activity indicators).
- Instrumental systematics that vary sector-to-sector in TESS (mitigated by restricting analysis to orbits within the same sector, then comparing across sectors).
- Companion-induced orbital precession changing the transit/eclipse geometry on multi-year timescales (mitigated by checking for TTVs and known companions).

### Why It Matters

Detecting orbit-to-orbit atmospheric variability would be the first empirical measurement of exoplanet *weather* (as opposed to *climate*). It would provide a direct, model-independent constraint on atmospheric radiative and advective timescales — quantities that are currently only inferred indirectly from single-epoch phase curve amplitudes and offsets. For eccentric planets specifically, the "flash heating" scenario offers a unique natural experiment in atmospheric response to impulsive forcing, with no solar system analog. Success here would establish a new observational methodology applicable to the growing sample of well-characterized JWST phase curve targets.

---

## Summary Table

| Feature | Project 1: Galactic Chronochemistry | Project 2: Exoplanetary Rings | Project 3: Tidally Driven Weather |
|---|---|---|---|
| **Core dataset** | Kepler/TESS + APOGEE/GALAH + Gaia | Kepler DR25 short-cadence | TESS Extended Mission multi-sector |
| **Key method** | Hierarchical occurrence rate modeling across chemodynamical populations | Bayesian ingress/egress morphology decomposition | Orbit-to-orbit phase curve variance analysis |
| **Novelty axis** | Chemical clocks as planet formation probes | Population-level ring constraints via non-detections | Second-order atmospheric variability statistics |
| **Feasibility** | High (all data public now) | High (all data public, new modeling needed) | Medium-High (requires careful systematics control) |
| **Impact if successful** | Bridges exoplanet science and Galactic archaeology | First ring detection or strongest population constraints | First empirical exoplanet weather detection |

---

*This report was generated as part of an automated exoplanet research strategy session. Ideas are intended as starting points for deeper literature review and feasibility assessment.*
