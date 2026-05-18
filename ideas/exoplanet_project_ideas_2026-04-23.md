# Exoplanet Research Project Ideas — April 23, 2026

Three ambitious, underexplored project concepts built on publicly available space mission data.

---

## Project 1: Tidally Induced Stellar Oscillation Modes as a Probe of Hot Jupiter Interior Structure

### Scientific Premise

Hot Jupiters in tight orbits raise tidal bulges on their host stars. These tidal interactions should excite or modulate stellar oscillation modes at harmonics of the orbital frequency. While tidal spin-up and orbital decay have received attention (e.g., WASP-12b), the *spectral fingerprint* of tidally forced oscillations in stellar photometry remains largely uncharacterized across the population. By searching Kepler and TESS long-baseline light curves for excess power at exact integer multiples of the orbital frequency (after transit removal), one could detect or constrain the tidal dissipation quality factor Q'★ for dozens of systems simultaneously — and, by extension, back out constraints on the planetary Love number and interior density profile through the coupling efficiency.

### Target Datasets

- **Kepler long-cadence and short-cadence data** for confirmed hot Jupiter hosts (roughly 50–70 systems with P < 5 days and sufficient baseline).
- **TESS Continuous Viewing Zone targets** with multi-sector coverage for independent validation.
- **Gaia DR3/DR4 stellar parameters** for accurate mass/radius to model the expected tidal forcing amplitude.

### Novelty

Most tidal studies focus on orbital period derivatives (timing) or rotational synchronization. Directly detecting the *forced oscillation spectrum* in photometry at orbital harmonics is a distinct observable. A few individual-system searches exist (e.g., WASP-18, HAT-P-13), but no systematic population-level survey of tidally forced stellar pulsation excess has been published using the full Kepler/TESS archive. The population approach is what makes this distinct: non-detections are just as informative as detections for constraining Q'★ distributions.

### Concrete Workflow

1. Assemble a catalog of confirmed hot Jupiters with Kepler or multi-sector TESS photometry. Use the NASA Exoplanet Archive for orbital elements.
2. For each system, flatten the light curve (remove transits, stellar rotation, instrumental trends) using a Gaussian process or spline baseline, preserving frequencies near orbital harmonics.
3. Compute a Lomb-Scargle or Bayesian periodogram of the residuals. Extract power at the first 5–10 integer harmonics of the orbital frequency.
4. Compare the measured harmonic power against a noise model (bootstrap or injection-recovery on phase-shuffled data) to assess significance.
5. For systems with detections, forward-model the expected tidal forcing amplitude as a function of Q'★, planetary mass, and orbital separation. Infer Q'★ posteriors.
6. For non-detections, derive upper limits. Stack non-detections in a meta-analysis to push sensitivity below individual-system thresholds.
7. Correlate inferred Q'★ with stellar type, age (from gyrochronology/isochrones), and planetary mass to look for trends.

### Expected Signal/Observable

Excess photometric power at exact integer multiples of the orbital frequency, at amplitudes of roughly 1–50 ppm for the most favorable systems (massive planets, short periods, solar-type hosts). Stacking could reach sub-ppm sensitivity.

### Possible False Positives

- **Ellipsoidal variations and Doppler beaming** also produce power at orbital harmonics. These are well-modeled and must be subtracted; the residual excess (or lack thereof) is the tidal oscillation signal.
- **Stellar p-mode oscillations** near the orbital harmonic frequencies could contaminate, especially for subgiants. Frequency resolution from long baselines mitigates this.
- **Residual instrumental systematics** at specific frequencies (e.g., Kepler rolling-band artifacts). Cross-validation between Kepler and TESS reduces this risk.

### Why It Matters

Tidal dissipation governs hot Jupiter orbital evolution, survival timescales, and the observed period distribution. Current Q'★ constraints come from a handful of individual systems with measured orbital decay. A population-level photometric approach would provide an independent, complementary constraint and could reveal whether Q'★ varies systematically with stellar or planetary properties — a key open question for understanding why some hot Jupiters survive and others spiral inward.

---

## Project 2: Mapping the Exoplanet "Obliquity Desert" Using Transit Duration Variations in Multi-Planet Kepler Systems

### Scientific Premise

Planetary obliquity (axial tilt) affects climate, habitability, and long-term orbital stability. In multi-planet systems, mutual gravitational perturbations can drive obliquity oscillations, but these are rarely observable. However, a planet's obliquity is dynamically coupled to its orbital inclination evolution: Cassini state transitions and secular spin-orbit resonances can lock obliquity to inclination. Kepler multi-planet systems show measurable transit duration variations (TDVs) caused by orbital plane precession from mutual inclinations. By inverting TDV signals to extract the precession rate and mutual inclination amplitude, and then forward-modeling the spin-orbit coupling, one can identify which planets are likely trapped in Cassini states (with predictable obliquities) versus those in chaotic obliquity regimes. This maps out an "obliquity desert" — regions of parameter space where stable low obliquity is dynamically enforced — versus "obliquity oases" where large, potentially habitable-relevant obliquities are permitted.

### Target Datasets

- **Kepler DR25 light curves** for all confirmed and validated multi-transiting systems (roughly 700+ systems).
- **Transit timing and duration catalogs** (Holczer et al. 2016, Rowe et al. 2015, updated community catalogs).
- **Gaia DR3/DR4 stellar densities** to anchor transit duration modeling.
- **Published TTV/TDV analyses** for cross-validation of mutual inclination estimates.

### Novelty

TDVs have been used to confirm mutual inclinations in a handful of Kepler systems, and obliquity dynamics have been studied theoretically. But the connection — using *observed* TDV-derived precession rates to predict *planetary obliquity regimes* across a population — appears underexplored as a systematic survey. Most obliquity studies are purely theoretical or focus on the Solar System. This project bridges dynamics and observation in a way that produces testable predictions for JWST phase curve observations (which are sensitive to obliquity-driven seasonal thermal signatures).

### Concrete Workflow

1. Measure or compile TDVs for all Kepler multi-transiting systems with sufficient SNR. Use a uniform transit-fitting pipeline (e.g., exoplanet or batman) applied to individual transits.
2. Fit a linear or sinusoidal TDV model to each planet to extract the precession period and amplitude of the inclination oscillation.
3. For systems with detected TDV signals, use the precession rate and planet/star parameters to compute the spin-orbit coupling parameter α (ratio of precession rate to spin-axis precession rate driven by the stellar torque).
4. Map each planet onto the Cassini state diagram: α ≈ 1 indicates proximity to a spin-orbit resonance where obliquity can be large and chaotic; α ≫ 1 or α ≪ 1 indicates stable low or moderate obliquity.
5. Compile a population-level map of obliquity regime versus planet radius, period, multiplicity, and mutual inclination.
6. Identify the most promising targets where large obliquity is dynamically predicted — these are high-priority JWST phase curve targets where seasonal thermal signatures might be detectable.

### Expected Signal/Observable

TDV amplitudes of 1–30 minutes over the 4-year Kepler baseline for systems with mutual inclinations of 1–5 degrees and precession periods of 10–100 years. The derived obliquity regime classification (Cassini state 1, 2, or chaotic) is the primary output.

### Possible False Positives

- **Stellar activity and spot-crossing events** can mimic transit duration changes. Filtering on impact parameter consistency and using even/odd transit comparisons helps.
- **TTVs from eccentricity** can be confused with TDVs if the transit model is insufficiently flexible. Joint TTV+TDV fitting mitigates this.
- **Insufficient baseline** for long precession periods leads to unconstrained slopes rather than periodic signals. These systems yield only upper/lower limits on mutual inclination.

### Why It Matters

Obliquity is one of the least constrained parameters for exoplanets, yet it profoundly affects climate stability and surface habitability. A population-level obliquity regime map — even a probabilistic one — would be a first, directly informing target prioritization for atmospheric characterization missions and adding a dynamical dimension to habitability assessments that is currently missing.

---

## Project 3: Detecting Cometary/Exozodiacal Dust Transits via Asymmetric Ingress-Egress Chromatic Signatures in Kepler and TESS Photometry

### Scientific Premise

Circumstellar dust — from cometary activity, collisional cascades, or exozodiacal clouds — should produce transient, asymmetric, and wavelength-dependent dimming events distinct from planetary transits. A few spectacular cases exist (KIC 8462852 "Tabby's Star," KIC 3542116's exocomet transits), but a systematic search for *low-level* asymmetric chromatic transit-like events across the full Kepler/TESS archive has not been done at scale. The key diagnostic is the *ingress-egress asymmetry*: a dusty tail or extended debris structure produces a sharp ingress (leading edge occults the star) and a gradual egress (diffuse tail clears slowly), or vice versa, with a wavelength-dependent depth ratio (dust scatters/absorbs more at shorter wavelengths). By searching for events with significant ingress-egress asymmetry *and* chromatic depth variation simultaneously, one can build a catalog of candidate dust transit events and constrain the incidence rate of active cometary or collisional dust production as a function of stellar type and age.

### Target Datasets

- **Kepler short-cadence data** for the highest time resolution on ingress/egress shape.
- **TESS 2-minute and 20-second cadence data**, especially for bright stars where photometric precision enables chromatic analysis via comparison with ground-based multicolor follow-up or TESS's own red bandpass versus synthetic blue from Gaia epoch photometry.
- **Kepler's "red" vs. "blue" pixel-level light curves**: Kepler's broad bandpass can be crudely split into redder and bluer channels using the pixel response function and the star's position on the detector, enabling low-resolution chromatic transit analysis.
- **Gaia DR3 epoch photometry** (G, BP, RP) for simultaneous multicolor coverage of TESS targets.

### Novelty

Exocomet transit searches have been done (e.g., Rappaport et al. 2018 for Kepler, Zieba et al. 2019 for TESS), but they primarily used morphological shape-matching to theoretical comet tail profiles. Adding the *chromatic* dimension — requiring both asymmetry and wavelength-dependent depth — as a joint discriminant is underexplored and substantially reduces the false positive rate. The Kepler pixel-level chromatic decomposition technique has been used for eclipsing binary characterization but not systematically applied to asymmetric single-event transits. Combining Gaia epoch photometry with TESS for simultaneous multicolor coverage of transient events is also a relatively untapped approach.

### Concrete Workflow

1. Download Kepler short-cadence and TESS 2-minute cadence light curves for a volume-limited or magnitude-limited stellar sample (e.g., all FGK dwarfs brighter than Kp = 14 or TESS mag < 12).
2. Run a matched-filter search for single or few-repeat asymmetric dipping events. Use a bank of templates: sharp-ingress/slow-egress and slow-ingress/sharp-egress profiles with varying timescales (hours to days).
3. For each candidate event, perform pixel-level photometry on Kepler data to extract a crude "blue" and "red" light curve. For TESS candidates, cross-match with Gaia epoch photometry to check for simultaneous BP/RP dimming.
4. Compute the ingress-egress asymmetry parameter (ratio of ingress to egress duration) and the chromatic depth ratio (blue depth / red depth). Genuine dust transits should show asymmetry > 1.5 and blue/red depth ratio > 1.
5. Vet candidates against known instrumental artifacts (momentum dumps, scattered light, cosmic rays) and astrophysical false positives (grazing eclipsing binaries, starspot crossings).
6. For surviving candidates, fit a physical dust tail model (optical depth, grain size distribution, tail opening angle, velocity) to the light curve shape and chromatic information. Derive dust production rates.
7. Compute occurrence rates as a function of stellar spectral type, age (from Gaia+isochrone or gyrochronology), and presence/absence of known planetary companions.

### Expected Signal/Observable

Asymmetric dimming events with depths of 0.01–1% lasting hours to days, with blue/red depth ratios of 1.1–3 depending on grain size. For Kepler short-cadence bright stars, individual events down to ~0.05% depth should be detectable. Occurrence rates are poorly constrained but could plausibly be 0.1–5% of FGK dwarfs showing at least one event per year of monitoring.

### Possible False Positives

- **Instrumental artifacts** (pointing jitter, thermal transients) can produce asymmetric flux dips but should not be chromatic. The joint asymmetry+chromaticity requirement is the primary filter.
- **Starspot evolution** during a planetary transit can create apparent asymmetry. However, spot-crossing events are periodic (at the rotation period) and not chromatic in the same sense as dust.
- **Grazing eclipsing binaries** can be asymmetric if the companion has a non-spherical shape (e.g., Roche lobe overflow), but these are periodic and achromatic.
- **Background eclipsing binaries** blended in the photometric aperture. Pixel-level centroid analysis (standard Kepler/TESS vetting) addresses this.

### Why It Matters

The prevalence of active dust production around main-sequence stars is a window into the late stages of planetary system evolution — ongoing cometary bombardment, collisional grinding of asteroid belts, and dynamical instability. Current constraints come from infrared excess surveys (which probe warm/hot dust in bulk) and a handful of individual spectacle systems. A systematic photometric census with chromatic discrimination would bridge the gap between infrared-excess statistics and individual dramatic systems, constraining how common "Late Heavy Bombardment"-like episodes are across the galaxy and whether they correlate with planetary system architecture.

---

*Report generated autonomously on April 23, 2026. Choices made: focused on Kepler/TESS/Gaia as the primary public datasets; prioritized ideas where the observational signature is concrete and the workflow is end-to-end feasible with existing data; avoided ideas that require new observations or proprietary data.*
