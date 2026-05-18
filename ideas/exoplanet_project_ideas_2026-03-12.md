# Exoplanet Research Project Ideas — March 12, 2026

Three ambitious, potentially underexplored project concepts grounded in publicly available mission data. Each is designed to be discovery-driven, methodologically concrete, and publishable if successful.

---

## Project 1: Decade-Baseline TTV Archaeology — Hunting Habitable-Zone Ghosts in the Kepler–TESS Overlap

### Scientific Premise

Transit timing variations (TTVs) reveal unseen companion planets through gravitational perturbations of a transiting world's orbit. The ~decade gap between Kepler/K2 observations (2009–2018) and ongoing TESS coverage of the same fields creates an extraordinarily long timing baseline — long enough that perturbations from companions on *year-scale* orbits, including orbits within stellar habitable zones, could accumulate to detectable amplitudes. Recent work (Kokori et al. 2025, MNRAS 538) refined ephemerides for 111 Kepler/K2 planets re-observed by TESS and found evidence for previously undetected timing anomalies in 22 of them. A separate homogeneous survey (A&A, 2026) examined 423 single-transiting TESS systems for TTV signals from non-transiting companions. But neither study systematically exploited the full Kepler-to-TESS baseline specifically targeting the *habitable-zone period range* for each host star, nor combined TTVs with transit duration variations (TDVs) to break mass–eccentricity degeneracies for those candidate companions.

### What Makes It Distinct

Most TTV studies focus on compact multi-transiting systems or hot-Jupiter companions. This project would flip the target selection: start from the habitable zone of each host star, compute the expected TTV super-period and amplitude for plausible Earth-to-Neptune-mass companions at those separations, and then search the Kepler-to-TESS residuals for signals matching those predictions. It is a targeted, theory-guided search rather than an agnostic signal hunt.

### Target Datasets

- **Kepler DR25 long-cadence and short-cadence light curves** (MAST archive)
- **K2 Campaign light curves** for fields re-observed by TESS
- **TESS 2-min and 30-min cadence FFI light curves** (Sectors covering Kepler/K2 footprints, including TESS Extended Mission sectors through 2025)
- **ExoFOP-TESS** stellar parameters for updated host-star HZ boundaries
- **NASA Exoplanet Archive** composite planet table for known system architectures

### Novelty

Theory-guided TTV+TDV search explicitly optimized for habitable-zone companions using the full decade baseline. Existing TTV catalogues either use short baselines (TESS-only) or long baselines without HZ-targeted sensitivity maps. This fills a specific gap.

### Concrete Workflow

1. **Sample selection.** Cross-match Kepler/K2 confirmed single-transiting planets with TESS observed sectors. Require ≥ 3 TESS transits and ≥ 10 Kepler transits. Compute the habitable-zone inner and outer boundaries for each host using Kopparapu et al. (2013) relations and updated stellar parameters from Gaia DR3 + TIC v8.2.
2. **Uniform transit fitting.** Re-extract individual transit mid-times and durations from both Kepler and TESS photometry using a common GP-detrended model (e.g., `exoplanet` + `celerite2`). Propagate correlated noise into timing uncertainties.
3. **HZ-targeted sensitivity mapping.** For each system, inject synthetic TTV signals from companions at 10 trial periods spanning the HZ, with masses from 1–20 M⊕ and eccentricities 0–0.3. Determine the 3σ detection threshold as a function of companion mass and period.
4. **Residual search.** Fit a linear ephemeris to each planet's combined Kepler+TESS transit times. Compute O–C (observed minus calculated) residuals. Search for periodic signals using a Lomb-Scargle periodogram and a Bayesian sinusoidal model comparison (evidence ratio vs. linear trend vs. quadratic drift).
5. **TDV cross-check.** For any TTV candidate, independently measure transit duration variations. A correlated TTV+TDV signal with the correct phase offset strengthens the companion hypothesis and breaks the mass–eccentricity degeneracy.
6. **Dynamical modeling.** For strong candidates, run full N-body photodynamical fits (e.g., `TTVFast` or `Rebound`) to constrain the companion's mass, period, eccentricity, and mutual inclination.

### Expected Signal / Observable

A companion of ~5 M⊕ at 1 AU around a solar-type star perturbing a hot Jupiter on a 3-day orbit produces TTV amplitudes of ~10–100 seconds over a super-period of years — well within the precision of Kepler (~15 s per transit) and TESS (~30–60 s for bright targets) when accumulated over a decade baseline. The signal is a quasi-sinusoidal O–C pattern with a period related to the companion's orbital period and the near-resonance super-period.

### Possible False Positives

- **Stellar activity (starspot crossing):** Produces asymmetric transit distortions that mimic timing offsets. Mitigated by fitting spot-crossing events and by requiring correlated TTV+TDV signals (spot crossings produce uncorrelated noise in TDVs).
- **Instrumental systematics:** TESS and Kepler have different cadences, bandpasses, and systematics. Mitigated by the uniform detrending framework and by Monte Carlo injection-recovery tests.
- **Apsidal precession:** A single eccentric planet can show quadratic TTVs. Mitigated by the Bayesian model comparison (sinusoidal vs. quadratic).
- **Light-time effect from a distant stellar companion:** Produces long-term TTVs proportional to the binary orbit. Mitigated by checking Gaia RUWE and Hipparcos–Gaia proper-motion anomalies for bound stellar companions.

### Why It Matters

Detecting non-transiting habitable-zone planets around stars *already known to host transiting worlds* would provide direct constraints on the architecture and multiplicity of planetary systems in their temperate regions — a regime where radial-velocity surveys are sensitivity-limited and direct imaging cannot yet reach. It would also produce high-value targets for JWST reflected-light searches and future missions like the Habitable Worlds Observatory.

---

## Project 2: The Phantom Radius Valley — Recharting Exoplanet Demographics After Correcting TESS Flux Dilution

### Scientific Premise

The "radius valley" — the observed dearth of planets between ~1.5 and 2.0 R⊕ — is one of the most important features in exoplanet demographics, interpreted as evidence for atmospheric mass loss (photoevaporation or core-powered mass loss) sculpting the transition from rocky super-Earths to volatile-rich sub-Neptunes. However, a June 2025 study demonstrated that TESS planet radii are systematically underestimated by a weighted median of ~6% due to unresolved flux contamination from background stars, translating to a ~20% overestimation of bulk density. This means a significant fraction of planets currently classified as dense super-Earths sitting just below the valley may actually be lower-density sub-Neptunes sitting *within or above* it. The radius valley's location, depth, and slope with stellar mass may all be artifacts of this uncorrected bias — and by extension, the theoretical models (photoevaporation vs. core-powered mass loss vs. water-world migration) calibrated against the observed valley could be fitting a phantom feature.

### What Makes It Distinct

The June 2025 paper identified and quantified the bias but did not propagate it through the full demographic machinery — occurrence rate calculations, the radius valley's dependence on stellar type, or the Bayesian model comparisons used to distinguish between formation/evolution theories. This project would do exactly that: take the corrected radii, recompute occurrence rates and valley parameters, and re-run the theory discrimination analysis to see which (if any) formation model is actually favored once the systematics are removed.

### Target Datasets

- **TESS-SPOC and QLP light curves** with TGLC-corrected photometry (Bouma et al.)
- **Gaia DR3 + TIC v8.2** for high-resolution imaging constraints and dilution estimates
- **NASA Exoplanet Archive** confirmed planet and candidate tables
- **California-Kepler Survey (CKS)** and **TESS-Keck Survey** for precise stellar parameters and RV masses
- **Kepler DR25** occurrence rate products as the "ground truth" comparison sample (less affected by dilution due to Kepler's smaller pixel scale)

### Novelty

A full end-to-end reassessment of the radius valley's demographics and theoretical implications after correcting a now-documented systematic bias. This goes beyond the original bias paper (which focused on individual planet characterization) to ask: does the radius valley itself change shape, and do our theoretical conclusions about atmospheric loss still hold?

### Concrete Workflow

1. **Dilution correction.** For every confirmed TESS planet with R < 4 R⊕, compute the flux contamination ratio using Gaia DR3 source catalogs within the TESS aperture. Apply the TGLC-calibrated correction to obtain revised transit depths and planet radii. Propagate uncertainties via MCMC.
2. **Revised occurrence rates.** Using the corrected radii, recompute planet occurrence rates as a function of radius and orbital period using the inverse-detection-efficiency method (e.g., Fulton & Petigura 2018 framework). Compare TESS-derived rates to Kepler-derived rates (which serve as a less-contaminated benchmark).
3. **Valley characterization.** Fit the radius distribution with a mixture model (two Gaussians + gap, or a broken power law) to extract the valley center, width, and depth as functions of stellar mass, metallicity, and insolation flux. Compare pre- and post-correction valley parameters.
4. **Theory discrimination.** Generate synthetic planet populations from three competing models: (a) XUV photoevaporation (Owen & Wu), (b) core-powered mass loss (Ginzburg, Gupta & Schlichting), and (c) water-world formation (Venturini et al., Burn et al.). Forward-model each population through TESS detection biases. Compare to the *corrected* observed distribution using hierarchical Bayesian inference.
5. **Stellar-type dependence.** Examine how the corrected valley parameters vary from F to mid-M dwarfs. Recent work (March 2026) shows the valley disappears around mid-to-late M dwarfs in TESS data — does this result survive the dilution correction, or was it partially driven by the larger contamination typical of fainter M-dwarf fields?

### Expected Signal / Observable

If the bias is propagated correctly, the radius valley should shift upward by roughly 0.05–0.15 R⊕ in the TESS sample, narrow or potentially partially fill in. The occurrence rate ratio of super-Earths to sub-Neptunes should decrease (some super-Earths "promoted" to sub-Neptunes). The slope of the valley with stellar mass may change, potentially disfavoring or favoring one atmospheric-loss mechanism over another.

### Possible False Positives

- **Overcorrection of dilution:** If the TGLC contamination model overestimates background flux for some targets (e.g., in sparse fields), radii could be artificially inflated. Mitigated by validating against high-resolution imaging (speckle, AO) and Kepler overlap targets.
- **Selection effects:** Correcting radii changes which planets fall in which bins, potentially introducing Eddington-like bias at bin edges. Mitigated by using a continuous mixture model rather than binned histograms.
- **Sample heterogeneity:** TESS targets span a wider range of stellar types and distances than Kepler. Mitigated by analyzing stellar-type subsamples independently and by including stellar parameter uncertainties in the hierarchical model.

### Why It Matters

The radius valley is the Rosetta Stone of small-planet formation and evolution. If its observed properties are significantly altered by a correctable systematic, then a decade of theoretical interpretation may need revision. This project directly tests whether our leading theories of planetary atmospheric loss survive contact with corrected data — a question with implications for predicting which small planets retain atmospheres and are viable targets for habitability studies with JWST and future observatories.

---

## Project 3: Mapping Stellar Winds in 3D via Time-Resolved Helium Escape Tails

### Scientific Premise

JWST's 2025 observations of WASP-121b and WASP-107b revealed that hot exoplanets shed helium in dramatic, structured tails shaped by the interplay of stellar gravity, radiation pressure, and stellar wind. WASP-121b showed twin helium streams spanning more than half its orbit; WASP-107b showed a leading tail extending nearly 10 planetary radii. These structures are not static — they respond to the instantaneous stellar wind conditions along the planet's orbit. This means the planet acts as a *probe* flying through the stellar wind, and the time-varying morphology of its escape tail encodes the 3D structure of the wind. Stellar winds of cool stars are notoriously difficult to measure directly (they are too tenuous for radio detection and too cool for X-ray emission), yet they govern angular momentum loss, habitability, and planetary atmospheric erosion. Exoplanet escape tails offer a wholly new, indirect method to map these winds.

### What Makes It Distinct

Current atmospheric-escape studies focus on characterizing the *planet's* mass-loss rate and thermosphere. The stellar wind is treated as a nuisance parameter or assumed to be spherically symmetric. This project inverts the problem: treat the planet's escape signature as a *diagnostic tool for the star*. By fitting 3D magnetohydrodynamic (MHD) wind models to multi-epoch helium transit observations, one can constrain the wind's velocity, density, and magnetic field geometry as a function of orbital phase (i.e., position around the star). No existing study has attempted a systematic, multi-target "stellar wind tomography" campaign using exoplanet escape tails.

### Target Datasets

- **JWST NIRSpec G140H** observations of the metastable helium triplet (1083 nm) for WASP-121b, WASP-107b, HAT-P-32b, WASP-69b, and other targets with detected helium escape (publicly available in MAST after proprietary periods)
- **Archival ground-based high-resolution spectroscopy** of helium 1083 nm from CARMENES, SPIRou, and Keck/NIRSPEC for the same targets (ESO archive, CADC)
- **TESS photometric monitoring** of host-star rotational modulation to constrain stellar activity phase
- **XMM-Newton and Chandra X-ray archives** for host-star coronal properties (X-ray luminosity → EUV flux estimates)
- The **SUNSET database** (synthetic atmospheric-escape transmission spectra for nearly every transiting planet, published 2025), which provides baseline escape models to compare against

### Novelty

Using exoplanet atmospheric escape not to study the planet, but to probe the star's wind — inverting the standard analysis framework. Multi-epoch, multi-target stellar wind tomography using helium escape morphology is, to our knowledge, unexplored as a systematic program.

### Concrete Workflow

1. **Target selection.** Identify all transiting exoplanets with published detections of metastable helium absorption at 1083 nm (currently ~15–20 targets). Prioritize those with multi-epoch observations or archival + JWST coverage, and those whose host stars have known rotation periods (from TESS or K2 photometry).
2. **Uniform spectral extraction.** For each target and epoch, extract the helium absorption profile as a function of orbital phase during transit (ingress, mid-transit, egress) and, where data exist, during pre- and post-transit phases that probe the extended tail.
3. **Escape-tail forward model.** Use a 3D Parker-wind + photoionization code (e.g., `p-winds` or `ATES`) to simulate the escaping atmosphere in a prescribed stellar wind. Parameterize the stellar wind by velocity (v_w), mass-loss rate (Ṁ_*), and a dipole+quadrupole magnetic field geometry. Compute synthetic helium absorption spectra via ray-tracing through the 3D simulation domain at each orbital phase.
4. **MCMC inversion.** Fit the multi-epoch, phase-resolved helium profiles to constrain the stellar wind parameters. For targets with observations at different stellar rotation phases (i.e., different epochs where the star's active regions face different directions), separately fit each epoch to probe azimuthal wind asymmetry.
5. **Cross-validation.** Compare inferred stellar mass-loss rates to the predictions of Cranmer & Saar (2011) and Johnstone et al. (2015) wind models calibrated on X-ray and rotation data. Check consistency with the host star's observed X-ray luminosity, age, and Rossby number.
6. **Population synthesis.** Aggregate results across the target sample to build the first empirical stellar-wind parameter distribution for planet-hosting stars, stratified by spectral type, activity level, and age.

### Expected Signal / Observable

The helium absorption line profile changes shape and velocity centroid as a function of orbital phase. A wind-shaped tail produces a characteristic blueshift during ingress (approaching tail material) and redshift during egress (receding material), with amplitudes of ~1–10 km/s depending on wind speed. Multi-epoch observations at different stellar rotation phases should show systematic variations in the absorption depth and velocity structure if the wind is anisotropic (e.g., faster at the poles, slower at the equator, or structured by magnetic topology). Typical expected helium absorption depths are 0.5–5% for hot Neptunes and inflated hot Jupiters.

### Possible False Positives

- **Planetary magnetic field effects:** A planetary magnetosphere can also shape the escape flow. Mitigated by comparing planets with and without expected magnetic fields (e.g., rocky vs. gas giant) and by checking whether the inferred wind parameters are self-consistent across multiple planets orbiting the same star (if any exist).
- **Stellar variability contamination:** The host star's own helium 1083 nm emission/absorption varies with activity. Mitigated by monitoring out-of-transit stellar spectra at each epoch and subtracting the stellar contribution.
- **Model degeneracies:** Wind velocity and density can trade off in the absorption signal. Mitigated by combining the helium line profile (which constrains kinematics) with the absorption depth (which constrains column density), and by using the tail morphology (leading vs. trailing, spatial extent) as an additional constraint.
- **Interstellar medium absorption:** The ISM can produce absorption near 1083 nm. Mitigated by checking the ISM column along each sightline using Na D or Ca K interstellar lines.

### Why It Matters

Stellar winds are a missing piece in exoplanet science: they drive atmospheric erosion, control magnetospheric dynamics, and set the boundary conditions for habitability. Despite their importance, stellar winds of cool main-sequence stars have never been directly measured for any star other than the Sun. This project would provide the first empirical constraints on the 3D wind structure of planet-hosting stars, using their own planets as in-situ probes — a measurement that no existing or planned observatory could achieve by other means.

---

*Generated March 12, 2026. All datasets referenced are publicly available through MAST, the NASA Exoplanet Archive, ESO, and CADC.*
