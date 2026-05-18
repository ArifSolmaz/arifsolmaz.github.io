# Ambitious Exoplanet Research Project Ideas

*Generated: April 29, 2026 — Scheduled Task Output*

---

## Project 1: Tidal Decay Chronometry — Using Hot Jupiter Orbital Period Derivatives as Independent Stellar Age Clocks

### Scientific Premise

Hot Jupiters on very tight orbits (P < 2 days) are expected to undergo measurable tidal orbital decay, where energy dissipation inside the host star causes the planet to spiral inward. The rate of this inspiral is governed by the stellar tidal quality factor Q'★, which itself depends on the star's internal structure — and therefore its evolutionary state and age. The key insight is that if you can measure the period derivative ∂P/∂t for a sample of ultra-short-period hot Jupiters, you can invert the tidal decay rate to obtain an independent, dynamical age estimate for the host star. This would create a wholly new stellar age-dating method, complementary to gyrochronology, isochrone fitting, and asteroseismology.

WASP-12b's confirmed orbital decay (period decreasing at ~29 ms/yr) demonstrated this is measurable. But no one has systematically attempted to build a **calibrated age ladder** from tidal decay rates across a population.

### Target Datasets

- **Kepler/K2 long-baseline photometry** for ultra-short-period giant planets (WASP-18b, WASP-19b, WASP-43b, KELT-16b, and others with P < 2 days)
- **TESS** multi-sector observations extending the time baseline by 6+ years beyond Kepler
- **Archival ground-based transit times** from ETD (Exoplanet Transit Database) and literature, some stretching back 15+ years
- **Gaia DR4** parallaxes and stellar parameters for host star characterization
- **ESPRESSO/HARPS** RV archives for refining orbital eccentricities (needed to disentangle tidal circularization from decay)

### Novelty

While individual period derivative measurements exist for a handful of systems, and tidal theory papers model decay rates, the specific idea of **inverting measured ∂P/∂t values into a population-level stellar age calibration** is underexplored. Most tidal decay papers focus on predicting remaining lifetimes or constraining Q'★. Flipping the problem — treating Q'★ as a known function of stellar type (calibrated on the few well-characterized systems) and then solving for age — has not been systematically pursued as an age-dating technique. This is distinct from mainstream work because it reframes tidal decay from an orbital evolution problem into a stellar astrophysics tool.

### Concrete Workflow

1. Compile a master catalog of all hot Jupiters with P < 2.5 days that have transit timing observations spanning >8 years (combining Kepler, TESS, and ground-based).
2. For each system, perform a uniform O-C (observed minus calculated) transit timing analysis using a quadratic ephemeris model (linear decay) and compare against constant-period and apsidal precession models via Bayesian model selection (BIC/Bayes factors).
3. For systems with significant ∂P/∂t detections (or informative upper limits), compute the implied Q'★ using standard equilibrium tidal theory.
4. Cross-match with independently age-dated host stars (via asteroseismology from Kepler, gyrochronology, or cluster membership) to calibrate the Q'★–age–spectral-type relation.
5. Apply the calibrated relation to the remaining systems to predict ages; compare against isochrone ages to assess systematic offsets and scatter.
6. Quantify the method's precision and identify the stellar parameter regime where tidal decay chronometry is most powerful.

### Expected Signal / Observable

For WASP-12b-like systems, period shifts of ~30 ms/yr accumulate to ~0.5 seconds over a 15-year baseline — easily detectable with modern transit photometry (timing precision ~10–30 seconds for ground-based, ~5 seconds for TESS, sub-second for Kepler). For less extreme systems (WASP-18b, WASP-43b), expected shifts are smaller (a few ms/yr) but may be detectable with the now-available ~10–15 year baselines. The "signal" for the age calibration is a correlation between the measured decay rate residuals (after removing the spectral-type dependence of Q'★) and independently determined stellar ages.

### Possible False Positives

- **Apsidal precession** can mimic a quadratic O-C trend over limited baselines. Mitigation: include precession as an alternative model; use RV eccentricity constraints.
- **Rømer delay** from a long-period companion can produce apparent period changes. Mitigation: check for RV trends and Gaia astrometric acceleration.
- **Stellar magnetic activity cycles** (Applegate mechanism) can modulate transit times quasi-periodically. Mitigation: monitor stellar activity indicators; the Applegate effect is typically periodic, not secular.
- **Systematics in heterogeneous timing datasets** from combining space and ground photometry. Mitigation: use a hierarchical model with per-instrument timing offsets.

### Why It Could Matter

Stellar ages are one of the most poorly constrained fundamental parameters in astrophysics. Gyrochronology breaks down for old and hot stars; isochrone fitting is degenerate on the main sequence; asteroseismology requires specific data. A tidal decay–based age clock would be completely independent of these methods, working best for F- and early G-type stars hosting ultra-short-period giants — a regime where other techniques struggle. Even if the precision is moderate (±1–2 Gyr), the independence of the method makes it valuable for cross-calibrating the stellar age ladder.

---

## Project 2: Exoplanet Obliquity Census via Phase-Curve Asymmetry Systematics in TESS Full-Frame Images

### Scientific Premise

A planet's obliquity (the tilt of its spin axis relative to its orbital axis) profoundly affects its climate and atmospheric circulation, but measuring exoplanet obliquity is extraordinarily difficult. For tidally locked hot Jupiters, obliquity is assumed to be zero — but for warm Jupiters and sub-Neptunes at wider separations, obliquity could be significant and is essentially unconstrained observationally.

Here is the underexplored angle: a planet with nonzero obliquity will have a **seasonally modulated** thermal phase curve. Over the course of its orbit, the substellar point drifts in latitude, changing the planet's disk-integrated thermal emission in a way that breaks the symmetry of the standard (zero-obliquity) phase curve. For eccentric warm Jupiters observed over multiple orbits by TESS, the **orbit-to-orbit variability in phase curve shape** — specifically, the amplitude and phase offset of the thermal peak — encodes obliquity information.

### Target Datasets

- **TESS Full-Frame Images (FFIs)** at 200-second cadence (from Extended Mission onward) for bright (T < 10 mag) warm Jupiters with periods 5–30 days observed across multiple TESS sectors spanning different orbital epochs
- Prime targets: HAT-P-17b, HAT-P-11b, Kepler-419b (if in TESS CVZ), TOI-4600b, and eccentric warm Jupiters from the TESS Objects of Interest catalog
- **Spitzer 4.5 µm archival phase curves** for cross-validation on the few systems with Spitzer full-orbit observations
- **JWST Cycle 1–4 phase curve programs** (publicly available) for high-SNR benchmarking

### Novelty

Phase curve analysis is a mature field, but it has focused almost exclusively on **tidally locked hot Jupiters assumed to have zero obliquity**. The idea of using **multi-epoch phase curve comparisons** to detect obliquity-driven seasonal variability in warm Jupiters is distinct from standard phase curve work. A few theoretical papers (e.g., Rauscher 2017, Ohno & Zhang 2019) have modeled oblique phase curves, but observational searches using TESS's growing multi-year baseline to look for **epoch-dependent phase curve shape changes** as a systematic obliquity signal have not been conducted. This is partly because individual TESS phase curves of warm Jupiters are low-SNR — the key methodological innovation is to treat the problem statistically across a population, looking for excess variance in phase curve parameters relative to the null (zero-obliquity) expectation.

### Concrete Workflow

1. Select all confirmed planets with 5 < P < 30 days, host star T_mag < 10, and TESS observations spanning ≥3 distinct sectors (ideally non-consecutive, to sample different seasonal phases).
2. Extract systematics-corrected photometry from TESS FFIs using established pipelines (eleanor, SPOC, or custom PSF photometry), carefully detrending stellar variability and instrumental systematics.
3. For each planet and each sector, fit a standard sinusoidal phase curve model (with secondary eclipse, ellipsoidal variation, and Doppler boosting components) and record the best-fit thermal amplitude A_therm and phase offset φ.
4. For the zero-obliquity null hypothesis, A_therm and φ should be constant across epochs (modulo noise). Compute the reduced chi-squared of the multi-epoch parameter set against constancy.
5. For systems showing significant epoch-to-epoch scatter in (A_therm, φ) beyond the photometric noise floor, fit an oblique-planet seasonal model parameterized by obliquity ε and precession rate, and compare against the constant model via Bayesian evidence.
6. Stack the population-level results: even if no individual detection is significant, a systematic excess of phase curve variability in warm Jupiters (relative to control hot Jupiters expected to have ε ≈ 0) would constitute a statistical detection of nonzero obliquities in the population.

### Expected Signal / Observable

For a warm Jupiter with obliquity ~30° and a dayside temperature contrast of ~500 K, the seasonal modulation of the thermal phase curve amplitude is expected to be ~10–20% of the mean amplitude. For a bright host (T_mag ~ 8), TESS phase curve amplitudes for warm Jupiters are typically ~50–200 ppm, so the seasonal signal would be ~5–40 ppm — challenging but potentially detectable when stacking multiple sectors. The population-level test (excess variance) is more powerful than individual detections and could reveal obliquity as a class property of warm Jupiters even if no single system yields a confident measurement.

### Possible False Positives

- **Stellar variability** (spots, faculae) evolving between sectors can change the apparent phase curve shape. Mitigation: model stellar variability independently using out-of-phase-curve portions of the light curve; compare against a control sample of planet-free stars with similar variability properties.
- **Instrumental systematics** varying between TESS sectors (different camera, CCD position). Mitigation: use injection-recovery tests on nearby comparison stars to quantify sector-dependent systematic floors.
- **Weather/cloud variability** on the planet could produce epoch-to-epoch phase curve changes unrelated to obliquity. Mitigation: this is actually scientifically interesting in its own right, but can be distinguished from obliquity by its expected timescale (stochastic vs. periodic with the precession period).
- **Eccentricity effects** in systems with poorly constrained orbits. Mitigation: use RV-constrained eccentricities and include eccentric phase curve models.

### Why It Could Matter

Obliquity is a fundamental but almost completely unconstrained property of exoplanets. It directly affects habitability (Earth's 23.4° obliquity is crucial for moderate seasons), atmospheric dynamics, and tidal evolution. A first population-level constraint — even a statistical upper limit — on warm Jupiter obliquities would test tidal evolution theories (which predict rapid obliquity damping for close-in planets but allow nonzero obliquities for wider orbits) and inform GCM modeling of exoplanet climates. It would also pioneer a technique extensible to PLATO-era photometry, where the precision will be much higher.

---

## Project 3: Mapping the Galactic Exoplanet Metallicity Gradient — Do Planet Occurrence Rates Track the Milky Way's Chemical Evolution?

### Scientific Premise

The giant planet–metallicity correlation (stars with higher [Fe/H] are more likely to host giant planets) is one of the strongest results in exoplanet science, but it has been established almost entirely for the **solar neighborhood** (d < 200 pc). Meanwhile, the Milky Way has a well-known radial metallicity gradient (~−0.06 dex/kpc in the disk) and vertical gradient (~−0.3 dex/kpc above the plane). If the planet–metallicity correlation holds universally, then **planet occurrence rates should vary systematically with Galactic position**, with the inner Galaxy being more planet-rich and the outer Galaxy and thick disk being planet-poor.

This has been loosely discussed but never rigorously tested with a uniform dataset. Kepler stared at a single field at l ≈ 76°, b ≈ 13°, sampling a pencil beam through the disk at distances up to ~1 kpc — enough to probe a meaningful range of Galactocentric radii (R_GC ~ 7.5–9 kpc) and scale heights. TESS, being all-sky, samples an even wider range of Galactic environments but with shorter baselines (biasing toward short-period planets). The idea is to combine Kepler's deep, uniform occurrence rates with Gaia-derived Galactic positions and spectroscopic metallicities to map how planet occurrence varies across the Galaxy's chemical structure.

### Target Datasets

- **Kepler DR25** planet candidate catalog and stellar properties table (~200,000 target stars with uniform detection completeness characterization)
- **Gaia DR4** distances, proper motions, and radial velocities for Galactic orbit integration of Kepler host stars
- **LAMOST DR10 / APOGEE DR17 / GALAH DR4** spectroscopic metallicities for Kepler field stars (substantial overlap exists — ~50,000+ Kepler targets have spectroscopic [Fe/H])
- **Kepler completeness maps** (Burke et al., or the Kepler Reliability products) for computing intrinsic occurrence rates corrected for detection efficiency
- **TESS-SPOC planet candidates** for an independent all-sky cross-check at short periods

### Novelty

The giant planet–metallicity correlation has been studied extensively as a function of **stellar** [Fe/H]. The connection to **Galactic chemical evolution** — asking whether planet occurrence rates track the Galaxy's radial and vertical metallicity gradients — has been touched on in a few papers (e.g., Zink et al. 2023 examined Galactic context for Kepler planets), but a full, self-consistent analysis that (a) maps occurrence rates as a joint function of Galactocentric radius R_GC and height |z|, (b) disentangles the "direct" metallicity effect from possible additional Galactic-environment effects (e.g., stellar density, radiation field, birth cluster properties), and (c) tests whether the occurrence–metallicity relation has the same slope in different Galactic zones has not been done. The key distinction from prior work is treating Galactic position not just as a proxy for metallicity, but as an independent variable that might encode additional environmental influences on planet formation.

### Concrete Workflow

1. Cross-match the Kepler stellar catalog with Gaia DR4 (distances, kinematics) and large spectroscopic surveys (LAMOST, APOGEE, GALAH) to obtain [Fe/H], R_GC, |z|, and Galactic orbit parameters (eccentricity, guiding radius) for each Kepler target.
2. Compute planet occurrence rates in bins of R_GC and |z| using the inverse-detection-efficiency method (Hsu et al. 2019 framework), carefully accounting for Kepler's detection completeness and reliability as functions of stellar properties.
3. In each Galactic bin, also compute the occurrence rate as a function of [Fe/H] to test whether the planet–metallicity correlation slope varies with Galactic position.
4. Fit a hierarchical Bayesian model: occurrence = f([Fe/H], R_GC, |z|, ...) to determine whether Galactic position has residual predictive power for planet occurrence beyond what [Fe/H] alone explains.
5. Separate the sample into thin disk, thick disk, and halo membership (using kinematics + chemistry) and compare occurrence rates across populations, controlling for metallicity.
6. Cross-validate short-period planet results using TESS all-sky detections, which sample a much wider range of Galactic environments.

### Expected Signal / Observable

Across the Kepler field, R_GC varies from ~7.5 to ~9 kpc, corresponding to a metallicity gradient of ~0.1 dex. The planet–metallicity correlation predicts ~30–50% variation in giant planet occurrence across this range. For small planets (which have a weaker metallicity dependence), the gradient should be shallower. The key observable is whether the measured occurrence rate gradient with R_GC is **steeper or shallower** than predicted from the metallicity gradient alone — any residual would indicate additional Galactic-environment effects on planet formation. The thin disk vs. thick disk comparison is especially powerful: thick disk stars at the same [Fe/H] as thin disk stars have different α-element abundances and formed in different environments, so any occurrence rate difference at fixed [Fe/H] would point to formation-environment effects beyond bulk metallicity.

### Possible False Positives

- **Selection effects in spectroscopic surveys**: LAMOST/APOGEE target selection is not uniform across the Kepler field, potentially introducing Galactic-position-dependent completeness biases. Mitigation: use only the subset of Kepler stars with spectroscopic coverage and carefully model the spectroscopic selection function; alternatively, use photometric metallicity estimates (less precise but more uniform).
- **Kepler detection efficiency varying with stellar distance** (more distant stars are fainter, reducing detection completeness). Mitigation: this is already accounted for in standard occurrence rate calculations via the completeness maps, but verify that the completeness correction does not introduce spurious Galactic-position trends by running injection-recovery tests stratified by distance.
- **Confounding stellar age–metallicity–Galactic position correlations**: older stars are more metal-poor and at larger |z|, so any age-dependent planet occurrence (e.g., from dynamical erosion of planetary systems) could masquerade as a Galactic gradient. Mitigation: include age estimates (from isochrones or asteroseismology for the subset with Kepler short-cadence data) as a covariate in the hierarchical model.
- **Small number statistics** for giant planets in the Kepler sample when sliced finely by Galactic position. Mitigation: focus the R_GC/|z| gradient analysis on small planets (which are abundant in Kepler) and use giant planets only for the coarser thin-disk vs. thick-disk comparison.

### Why It Could Matter

This project connects two major fields — exoplanet demographics and Galactic archaeology — in a way that could reveal whether planet formation is purely a local (protoplanetary disk) process or is also shaped by the larger Galactic environment. A positive detection of residual Galactic-environment effects (beyond metallicity) would challenge the standard core-accretion picture and suggest that factors like stellar birth cluster density, FUV radiation field, or supernova enrichment patterns influence planetary system architectures. Even a null result (planet occurrence tracks metallicity alone, with no additional Galactic dependence) would be a powerful confirmation that the planet–metallicity correlation is truly fundamental and environment-independent — a strong constraint for planet formation theory. The methodology would also lay groundwork for PLATO, which will observe multiple fields at different Galactic longitudes and could extend this analysis to a much larger volume of the Galaxy.

---

## Summary Table

| # | Project | Key Innovation | Primary Data | Risk Level |
|---|---------|---------------|-------------|------------|
| 1 | Tidal Decay Chronometry | Invert hot Jupiter orbital decay into a stellar age-dating method | Kepler + TESS + ground-based transit times | Medium — requires ≥5 significant ∂P/∂t detections for calibration |
| 2 | Obliquity via Phase Curve Variability | Multi-epoch phase curve comparison to detect seasonal signals from planetary obliquity | TESS FFIs, multi-sector warm Jupiters | High — individual signals are small; statistical population approach is key |
| 3 | Galactic Planet Occurrence Gradient | Map planet occurrence as a function of Galactic position, disentangling metallicity from environment | Kepler + Gaia + spectroscopic surveys | Medium-Low — large existing datasets; main challenge is controlling systematics |

---

*Note: These ideas are assessed as potentially underexplored based on the current literature landscape as of early 2026. Some adjacent work exists in each area; the novelty lies in the specific angles and methodological approaches described above.*
