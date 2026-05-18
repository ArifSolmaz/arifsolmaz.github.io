# Exoplanet Research Project Ideas — March 9, 2026

Three ambitious, potentially underexplored project concepts grounded in publicly available mission data.

---

## 1. Systematic Exotrojan Census Across the Kepler/K2 and TESS Archives

### Scientific Premise

Co-orbital (Trojan) companions — objects sharing an orbit with a known planet at the L4 or L5 Lagrange points — are ubiquitous in our Solar System (Jupiter alone has thousands of Trojans) yet no exotrojan has ever been confirmed. Theoretical work predicts that Trojans should form naturally in protoplanetary disks and can remain dynamically stable for billions of years, including in the habitable zone. A positive detection would be a landmark result; even robust upper limits would constrain planet formation and migration models far more tightly than current data allow.

Recent computational advances have introduced dynamical-signature-based detection methods distinct from the standard transit search, yet no large-scale, uniform survey of existing space-based photometry has been published using these newer techniques. This makes the project potentially underexplored relative to the volume of available data.

### Target Datasets

- **Kepler DR25 long-cadence and short-cadence light curves** (~200,000 stars, 4 years of nearly continuous coverage) via MAST.
- **K2 Campaigns 0–19** light curves, particularly campaigns overlapping known multi-planet systems.
- **TESS Full-Frame Images (FFIs)** and 2-minute cadence data through Extended Mission 2 (Sectors 1–83+), accessed via MAST/TIKE.
- **NASA Exoplanet Archive** confirmed-planet and candidate tables for selecting systems with favorable geometry.

### Novelty

Most prior exotrojan searches looked for secondary transit dips at ±60° orbital phase from the known transiting planet — a photometric approach that is signal-starved for small companions. The distinct angle here is to combine three complementary detection channels simultaneously: (a) the classical photometric search for a secondary transit offset by ±T/6 in time (where T is the orbital period); (b) a transit-timing-variation (TTV) signal induced by a massive co-orbital perturber, which produces a characteristic libration signature distinguishable from planet–planet TTVs; and (c) a transit-duration-variation (TDV) modulation produced by the co-orbital's gravitational influence on the transiting planet's velocity at inferior conjunction. Running all three channels in a joint Bayesian framework on the same light curve has not, to my knowledge, been done at scale.

### Concrete Workflow

1. **Sample selection.** From the NASA Exoplanet Archive, select confirmed transiting planets and high-reliability candidates with periods < 100 days (to ensure multiple transits) and host star magnitudes bright enough for 100-ppm-class photometry.
2. **Light-curve preparation.** Download detrended PDC-MAP (Kepler) and SPOC (TESS) light curves. Apply a custom stellar variability filter (e.g., Gaussian-process regression with a Matérn-3/2 kernel) that preserves transit-timescale signals while suppressing rotation and granulation.
3. **Phase-folded secondary search.** Phase-fold each system's light curve at the known planet period and search for excess absorption at orbital phases offset by ±1/6 period from mid-transit, using a box-least-squares variant tuned for shallow, V-shaped profiles.
4. **TTV/TDV extraction.** Fit individual transits with a Mandel–Agol model to extract mid-times and durations. Construct O–C diagrams and fit co-orbital libration models (horseshoe and tadpole families) as well as standard planet–planet interaction models for comparison.
5. **Joint inference.** For candidates passing any single channel at >3σ, run a joint MCMC model incorporating all three channels to estimate the co-orbital mass, libration amplitude, and inclination.
6. **Injection-recovery tests.** Inject synthetic co-orbital signals into real light curves to calibrate detection efficiency as a function of companion size, libration amplitude, and stellar noise level.

### Expected Signal / Observable

For a co-orbital Earth-sized body sharing an orbit with a hot Jupiter (e.g., WASP-12b-class), the secondary transit depth would be ~100 ppm and the TTV amplitude ~30 seconds over the libration period. For a co-orbital Neptune sharing an orbit with a warm Jupiter, TTV amplitudes could reach minutes. Kepler's 4-year baseline and TESS's growing multi-sector coverage make both regimes accessible.

### Possible False Positives

- **Starspot crossing events** can mimic shallow secondary dips at specific phases. Mitigation: check for chromatic dependence and correlation with stellar rotation period.
- **Background eclipsing binaries** diluted into the target aperture. Mitigation: pixel-level centroid analysis and Gaia DR3 contamination checks.
- **Standard planet–planet TTVs** misidentified as co-orbital libration. Mitigation: the co-orbital TTV waveform (sinusoidal at the libration frequency, typically much longer than the orbital period) is qualitatively different from near-resonance TTVs, which produce superpositions of short-period "chopping" and long-period "super-period" terms.

### Why It Could Matter

A confirmed exotrojan would open an entirely new class of object for comparative planetology. Even non-detections, translated into mass upper limits across hundreds of systems, would be the first empirical constraints on co-orbital survival through disk-driven migration — a question that current N-body simulations answer very differently depending on assumed disk parameters.

---

## 2. Population-Level Atmospheric Mass-Loss Demographics Across the Radius Valley Using TESS + Archival UV/X-ray Data

### Scientific Premise

The "radius valley" — the observed dearth of planets between ~1.5 and 2.0 Earth radii — is one of the most important features in the exoplanet size distribution. Two leading hypotheses explain it: photoevaporation (XUV-driven atmospheric escape) and core-powered mass loss (residual heat from formation driving envelope loss). Both predict the valley's location should shift with stellar mass, age, and irradiation level, but in subtly different ways. Distinguishing them requires mapping the valley's dependence on these parameters across large samples. While individual atmospheric escape detections are now being made with JWST (e.g., the helium outflows from WASP-121b), no one has yet attempted a statistical, population-level study correlating observed escape signatures with the planet's position relative to the radius valley.

### Target Datasets

- **TESS confirmed and candidate planet catalog** with updated radii from TESS-SPOC and community follow-up.
- **XMM-Newton Serendipitous Source Catalogue (4XMM-DR14)** and **Chandra Source Catalog (CSC 2.1)** for X-ray luminosities of planet host stars.
- **GALEX GR7** archive for near-UV and far-UV fluxes.
- **Gaia DR3** for precise stellar parameters (T_eff, luminosity, age proxies via gyrochronology and isochrone fitting).
- **JWST archival spectra** (where available) from GO programs targeting helium 10830 Å absorption in sub-Neptune atmospheres.

### Novelty

Individual atmospheric escape studies focus on one system at a time. Radius-valley studies focus on occurrence rates from transit surveys without incorporating direct mass-loss observables. This project bridges the two by constructing, for the first time, a "mass-loss landscape" — a two-dimensional map of XUV irradiation environment versus planetary radius — and populating it with both the statistical radius distribution and the handful of systems with direct escape measurements, then using the combined constraints to discriminate between photoevaporation and core-powered mass loss at the population level.

### Concrete Workflow

1. **Build the parent sample.** Cross-match the TESS Objects of Interest (TOI) catalog against Gaia DR3 to obtain homogeneous stellar parameters. Apply quality cuts (RUWE < 1.4, parallax S/N > 20).
2. **Estimate XUV irradiation.** Cross-match host stars with 4XMM-DR14 and CSC 2.1. For the majority without X-ray detections, estimate X-ray luminosity from age-activity relations calibrated on Gaia-derived gyrochronological ages. Use GALEX FUV/NUV to fill in the EUV regime via empirical scaling laws.
3. **Construct the mass-loss landscape.** Place every planet on a (log L_XUV / a², R_p) plane, where L_XUV is the stellar high-energy luminosity and a is the semi-major axis. Bin and smooth to construct the empirical radius distribution as a function of irradiation.
4. **Forward-model both hypotheses.** Run photoevaporation (using the Owen & Wu or Rogers & Owen frameworks) and core-powered mass loss (Gupta & Schlichting) evolutionary tracks across the same parameter space. Generate predicted radius distributions at each irradiation level.
5. **Statistical comparison.** Use hierarchical Bayesian inference (e.g., via PyMC or NumPyro) to determine which mass-loss mechanism (or mixture) best reproduces the observed two-dimensional distribution. Incorporate the ~15–20 systems with direct helium escape detections as additional likelihood terms.
6. **Predict JWST targets.** Identify planets sitting precisely on the predicted "stripping boundary" where the two models diverge most — these are the highest-value targets for future JWST helium surveys.

### Expected Signal / Observable

The photoevaporation model predicts the radius valley should shift to larger radii at higher XUV irradiation, while core-powered mass loss predicts a weaker irradiation dependence but a stronger dependence on stellar mass. With ~5,000 TESS planets and candidates, the sample should be large enough to detect the differential slope of the valley boundary at 3–5σ significance.

### Possible False Positives

- **Systematic radius errors** from imprecise stellar radii could blur the valley. Mitigation: restrict to the Gaia-calibrated subsample with radius uncertainties < 10%.
- **Age estimation biases** from gyrochronology, particularly for M dwarfs. Mitigation: use age only as a secondary variable; the primary test (valley slope versus irradiation) is age-independent.
- **Selection effects** in X-ray catalogs (only active stars detected). Mitigation: use upper limits via survival analysis for non-detections and validate with the GALEX-based EUV estimates.

### Why It Could Matter

Resolving the physical origin of the radius valley would fundamentally clarify how close-in planets evolve after formation. The "mass-loss landscape" framework could become a standard diagnostic tool, and the predicted JWST target list would directly enable follow-up observations during Cycles 5–6.

---

## 3. Stellar Surface Contamination Mapping via Multi-Epoch JWST Transmission Spectra of TRAPPIST-1 Planets

### Scientific Premise

JWST transmission spectroscopy of the TRAPPIST-1 system — the highest-priority target for rocky-planet atmosphere detection — has been repeatedly complicated by stellar contamination. Active regions (spots, faculae) on the host M dwarf imprint spectral features into the transit spectrum that can mimic or mask planetary atmospheric signatures. Recent analyses of TRAPPIST-1d and TRAPPIST-1e have found that stellar contamination is present in essentially all observations, and the data do not yet clearly distinguish between "no atmosphere" and "atmosphere hidden by stellar noise."

Rather than treating stellar contamination as a nuisance to be marginalized, this project proposes to invert the problem: use the multi-epoch, multi-planet TRAPPIST-1 transmission spectra to reconstruct a time-variable map of the stellar surface itself, then subtract it to recover the planetary signal — or, at minimum, derive the tightest possible joint constraints on both the stellar heterogeneity and any planetary atmosphere.

### Target Datasets

- **JWST GO and GTO program data** for TRAPPIST-1b, c, d, e, f, and g across Cycles 1–4 (NIRSpec G395H, NIRISS SOSS, NIRSpec PRISM). Multiple epochs per planet are now available or scheduled.
- **Spitzer/IRAC archival phase curves and transits** of TRAPPIST-1 planets (3.6 and 4.5 μm) for long-baseline stellar variability characterization.
- **TESS Sector 85+ data** (2-minute cadence) for contemporaneous optical monitoring of stellar rotation and flare activity.
- **Ground-based photometric monitoring** from SPECULOOS and TRAPPIST-South/North, publicly archived.

### Novelty

Current approaches fit each planet's transmission spectrum independently and include a parametric stellar contamination model (e.g., a two-temperature photosphere model) as a nuisance component. The underexplored angle is to fit all planets jointly across all epochs simultaneously, exploiting the fact that each planet transits a different chord of the stellar disk at a different time, thereby sampling the stellar surface at different latitudes and rotational phases. This multi-chord, multi-epoch tomographic approach can break degeneracies that are intractable with single-planet fits. The concept is analogous to Doppler imaging of rapidly rotating stars, but applied to transmission spectroscopy for the first time.

### Concrete Workflow

1. **Data compilation.** Gather all publicly released JWST transmission spectra of TRAPPIST-1 planets (reduced spectra from the MAST JWST archive and community reductions). Compile contemporaneous ground-based and TESS photometry to constrain the stellar rotational phase at each transit epoch.
2. **Stellar surface model.** Parameterize the TRAPPIST-1 surface as a grid of tiles (e.g., HEALPix with N_side = 4, giving 192 tiles). Each tile has a temperature drawn from a prior informed by M-dwarf spot/faculae contrast measurements. The stellar spectrum at each tile is interpolated from PHOENIX model grids.
3. **Transit geometry engine.** For each observed transit, compute the stellar disk region occulted by the planet as a function of time using the known orbital parameters and impact parameters. This defines which tiles contribute to the transmission spectrum at each epoch.
4. **Joint retrieval.** Implement a hierarchical Bayesian retrieval where: (a) the stellar surface map is shared across all transits and evolves slowly (with a Gaussian-process prior on temporal evolution tied to the ~3.3-day rotation period); (b) each planet has its own atmospheric model (flat line, or parameterized absorbers). Use nested sampling (e.g., MultiNest or dynesty) to explore the joint posterior.
5. **Atmosphere detectability.** Compute the Bayesian evidence for "atmosphere + stellar contamination" versus "stellar contamination only" for each planet. Report detection significances and upper limits on atmospheric column densities.
6. **Validation.** Apply the framework to synthetic JWST spectra generated from known stellar maps and known atmospheric models to verify that the tomographic inversion recovers both correctly.

### Expected Signal / Observable

The stellar contamination signal in TRAPPIST-1 transmission spectra is on the order of 50–200 ppm across the NIR, comparable to or larger than expected planetary atmospheric features (~20–100 ppm for a thin secondary atmosphere). By fitting 6 planets × 3–5 epochs × 2–3 instrument modes jointly, the framework leverages ~50+ independent spectral datasets to constrain a single stellar map, dramatically reducing per-planet contamination uncertainty. Simulations suggest a factor of 3–5 improvement in atmospheric upper limits compared to single-epoch, single-planet analyses.

### Possible False Positives

- **Degeneracy between stellar spots and planetary hazes.** Both produce wavelength-dependent slopes. Mitigation: the multi-chord tomography constrains the spatial distribution of stellar features independently of the planetary spectrum, partially breaking this degeneracy.
- **Stellar surface evolution faster than assumed.** If flares or rapid spot emergence alter the surface between transits within the same rotation, the GP prior may smooth over real changes. Mitigation: allow the GP lengthscale to be inferred from the data; flag epochs with contemporaneous flare detections for separate treatment.
- **Systematic offsets between JWST instrument modes.** NIRSpec and NIRISS may have different absolute flux calibrations. Mitigation: include instrument-specific offset parameters in the retrieval.

### Why It Could Matter

TRAPPIST-1 is the cornerstone system for rocky exoplanet atmospheric characterization, and stellar contamination is the single biggest obstacle. A framework that turns the contamination into a jointly solved component — rather than a marginalized nuisance — could be the key to unlocking atmospheric detections (or definitive non-detections) for habitable-zone rocky worlds with existing JWST data. The tomographic stellar map itself would also be a novel data product, providing the first spatially resolved view of an ultracool dwarf's surface derived from exoplanet transits.

---

*Generated March 9, 2026. All proposed datasets are publicly available through MAST, the NASA Exoplanet Archive, ESA archives, and community data releases.*
