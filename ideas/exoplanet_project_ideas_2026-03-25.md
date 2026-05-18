# Ambitious Exoplanet Research Project Ideas

**Generated: March 25, 2026**

---

## Project 1: Starspot Latitude Mapping via Transit Chord Tomography Across Stellar Spectral Types

### Scientific Premise

When a transiting exoplanet crosses a starspot, the resulting photometric "bump" in the transit light curve encodes information about the spot's position, size, and contrast. The transit chord acts as a one-dimensional knife-edge scan of the stellar surface. By aggregating many such crossings for the same system over time, one can reconstruct the latitude distribution of spots along the transit chord — and because the planet's orbital inclination constrains the chord's geometry on the stellar disk, the spot latitudes are physically meaningful.

The key insight is that the *ensemble* of spot-crossing events across many different host stars, binned by spectral type and rotation period, could reveal systematic latitude-dependent activity patterns analogous to the Sun's butterfly diagram — but for stars spanning K0 to M4. While individual spot-crossing detections are well-studied, a homogeneous population-level latitude census tied to stellar Rossby number remains potentially underexplored.

### Target Datasets

- **Kepler** long-cadence and short-cadence light curves for all confirmed transiting planets around K and M dwarfs (~400+ systems).
- **TESS** Sectors 1–83+ (through Extended Mission 2) for bright K/M host stars with known transiting planets.
- **Stellar parameters**: Gaia DR3 effective temperatures, rotation periods from McQuillan et al. (Kepler) or TESS rotation catalogs, and spectroscopic metallicities from LAMOST or GALAH where available.

### Novelty

Recent work (e.g., the 2025 homogeneous search for spot transits across K–M main-sequence stars in Kepler/TESS) has focused on detection frequency and spot property retrieval for individual events. However, a population-level reconstruction of spot latitude distributions as a function of stellar Rossby number — directly testing dynamo theory predictions for fully vs. partially convective stars — would go significantly beyond current analyses. Solar dynamo models predict spots migrate toward the equator over the activity cycle (the butterfly diagram), while fully convective M dwarfs may generate spots at all latitudes via a distributed dynamo. Transit chord tomography can test this.

### Concrete Workflow

1. **Catalog assembly**: Cross-match the NASA Exoplanet Archive with Kepler/TESS light curve catalogs. Select systems with ≥20 observed transits and host star Teff < 5000 K.
2. **Spot-crossing detection**: Fit each transit with a standard limb-darkened model; identify residual bumps exceeding 3σ above photon noise using a matched-filter approach (Gaussian kernel bank of variable width).
3. **Spot parameter extraction**: For each detected event, sample the posterior over spot latitude (along the chord), spot-to-photosphere contrast ratio, and spot angular radius using an MCMC framework that marginalizes over stellar inclination (constrained by v sin i and rotation period).
4. **Population binning**: Aggregate spot latitude posteriors for all events in bins of Rossby number (Ro = P_rot / τ_conv). Construct latitude frequency histograms for each Ro bin.
5. **Dynamo comparison**: Compare observed latitude distributions against predictions from flux-transport dynamo models (for partially convective stars) and mean-field α² dynamo models (for fully convective stars).

### Expected Signal / Observable

- For Sun-like and early-K stars (Ro ~ 0.5–2), expect a concentration of spots at low-to-mid latitudes (10°–30°), consistent with solar-type activity bands.
- For mid-to-late M dwarfs (Ro < 0.1), expect a flatter latitude distribution extending to high latitudes (>50°), reflecting a qualitatively different dynamo regime.
- The transition in latitude distribution shape as a function of Ro would be the primary observable — a "phase diagram" of stellar spot geography.

### Possible False Positives

- **Spot–inclination degeneracy**: A small equatorial spot and a larger high-latitude spot can produce similar bumps. Mitigation: marginalize over inclination using v sin i priors; require systems with well-constrained stellar obliquities.
- **Instrumental systematics**: Kepler long-cadence data smears short-duration bumps. Mitigation: use short-cadence data where available; calibrate bump detectability with injection-recovery tests.
- **Faculae masquerading as spots**: Bright regions crossed during transit produce dips rather than bumps, but could bias contrast estimates. Mitigation: model both spot and facular crossings simultaneously.
- **Planet-induced gravity darkening**: For very close-in planets, tidal distortion of the star can mimic spot signatures. Mitigation: restrict to systems with a/R* > 5.

### Why This Could Matter

This would be one of the first empirical tests of dynamo theory at the level of spot-latitude geography for a statistically meaningful sample of stars other than the Sun. The fully convective boundary (~M3.5) is a critical divide in stellar physics — whether the spot distribution changes qualitatively at this boundary has implications for understanding magnetic braking, angular momentum evolution, and the activity environment experienced by habitable-zone planets around M dwarfs.

---

## Project 2: Tidal Inflation as a Misalignment Fossil — A Radius Anomaly Census of Spin-Orbit-Measured Warm Neptunes

### Scientific Premise

Hot Jupiters on misaligned orbits are thought to have arrived at short periods via high-eccentricity migration (Kozai-Lidov cycles, planet-planet scattering) rather than smooth disk migration. A natural but under-tested prediction is that misaligned planets should have experienced stronger tidal dissipation during orbital circularization, which would deposit energy into the planet interior and inflate its radius. Recent work has begun to confirm this for Neptune-sized planets specifically — suggesting tidal inflation is stronger for misaligned Neptunes than aligned ones. But the sample remains small and the confounders (age, irradiation, composition) are not yet well-controlled.

The proposal here is to build the definitive sample of warm Neptunes and sub-Saturns (R = 3–8 R⊕, P = 3–30 days) with both measured spin-orbit angles (from Rossiter-McLaughlin or Doppler shadow observations) and precise radii (from Kepler/TESS + Gaia), and to test whether the radius anomaly (observed radius minus the radius predicted by standard thermal evolution models at the system's age and irradiation) correlates with obliquity after controlling for all known confounders.

### Target Datasets

- **Obliquity measurements**: TEPCat obliquity catalog (as of 2026, ~250+ systems with projected obliquity λ). Filter for R_p = 3–8 R⊕.
- **Precise radii**: Kepler/TESS transit photometry combined with Gaia DR3 stellar radii.
- **Stellar ages**: Isochrone fitting using spectroscopic Teff, log g, [Fe/H] from literature, plus gyrochronology where rotation periods are available.
- **Mass measurements**: Radial velocity mass determinations from HARPS, HARPS-N, ESPRESSO, NEID archives.

### Novelty

While the tidal-inflation–misalignment connection has been noted for hot Jupiters, extending this to the Neptune/sub-Saturn regime is scientifically distinct because these planets have fundamentally different interior structures (potentially large ice/rock fractions) and different tidal quality factors (Q'). A 2025 study found early evidence that misaligned Neptunes are more inflated, but did not control for age or metallicity in a Bayesian hierarchical framework. This project would do so, and would additionally search for a "memory" timescale — how long after circularization the tidal inflation signature persists — by looking for correlations between radius anomaly, obliquity, and system age.

### Concrete Workflow

1. **Sample construction**: Query TEPCat for all planets with measured λ; cross-match with NASA Exoplanet Archive for R_p, M_p, P, a/R*, and host star parameters. Restrict to 3 < R_p/R⊕ < 8 and P < 30 days. Expected sample: ~40–60 planets.
2. **Radius anomaly computation**: For each planet, run a grid of thermal evolution models (using MESA or the Lopez & Fortney 2014 framework) over a range of core mass fractions and atmospheric hydrogen/helium envelopes. Compute the predicted radius at the system's estimated age and current irradiation level. Define Δ R = R_obs − R_pred.
3. **Hierarchical Bayesian model**: Fit a population-level model where Δ R depends on (a) projected obliquity |λ|, (b) irradiation flux, (c) system age, (d) host star metallicity, and (e) planet mass. Use a latent-variable approach for the true 3D obliquity ψ, marginalizing over the unknown stellar inclination using v sin i and P_rot.
4. **Circularization timescale analysis**: For the subset of systems with well-constrained ages, test whether the obliquity–inflation correlation weakens with age, revealing the Kelvin-Helmholtz "cooling" timescale of tidally deposited energy.
5. **Sensitivity analysis**: Perform injection-recovery to determine the minimum detectable tidal energy deposit given current radius uncertainties.

### Expected Signal / Observable

- Misaligned warm Neptunes (|λ| > 30°) should show Δ R ~ 0.3–1.0 R⊕ larger than aligned counterparts, if tidal inflation is significant.
- A declining Δ R with system age among misaligned planets would indicate a characteristic tidal energy dissipation timescale of ~1–5 Gyr.
- A null result (no correlation) would also be significant: it would imply that Neptune-class interiors respond differently to tidal heating than gas giants, placing constraints on their tidal Q' values.

### Possible False Positives

- **Compositional diversity**: A planet with a thicker H/He envelope will naturally appear inflated relative to a rocky-rich planet of the same mass. Mitigation: include mass and bulk density as covariates; restrict analysis to planets with measured masses (not just upper limits).
- **Age uncertainties**: Stellar ages from isochrone fitting carry ~30–50% uncertainties. Mitigation: use a hierarchical model that propagates age uncertainties; perform analysis both with and without age as a covariate.
- **Selection bias in obliquity measurements**: Obliquities are preferentially measured for planets around bright, slowly-rotating stars. Mitigation: model the selection function explicitly.

### Why This Could Matter

This would directly test whether the orbital migration history of a planet leaves a detectable imprint on its present-day radius — a kind of "tidal fossil record." For the Neptune/sub-Saturn population, which is the most common type of planet found by Kepler yet the least understood structurally, this could provide the first empirical calibration of tidal Q' and constrain whether these planets have rocky cores, icy mantles, or something else entirely.

---

## Project 3: Hunting Ghost Planets in Resonant Chains via Long-Baseline TTV Drift Detection (Kepler-to-TESS)

### Scientific Premise

Many multi-planet systems discovered by Kepler are near (but not exactly in) mean-motion resonances, and some show transit timing variations (TTVs) indicative of gravitational interactions. A 2025 study bridging Kepler and TESS ephemerides identified 5 new systems with periodic TTVs and 17 systems with long-term secular trends in transit times previously unknown. These secular trends — slow, monotonic drifts in transit times — are a smoking gun for gravitational perturbations from unseen (non-transiting) planets in the system.

The ambitious idea: use the ~12-year baseline from Kepler (2009–2013) through K2 (2014–2018) to TESS (2018–2026+) to systematically identify systems with non-linear TTV trends, then perform dynamical inversions to constrain the masses and orbital parameters of the hidden perturbers. These "ghost planets" are invisible in transit photometry but leave gravitational fingerprints on their transiting siblings.

### Target Datasets

- **Kepler transit times**: Holczer et al. (2016) TTV catalog for all Kepler multi-planet systems, plus updated mid-times from Rowe & Thompson.
- **K2 transit times**: For systems in overlapping K2 campaign fields.
- **TESS transit times**: TESS-Kepler overlap from Sectors 14, 26, 40, 41, 53–55, 67–69, and the 2025–2026 extended mission pointings in the Kepler field. Use the 2025 Kokori et al. catalog of updated ephemerides.
- **Radial velocities**: Archival RVs from the California Legacy Survey, HARPS-N, and HIRES for systems where available.

### Novelty

While individual TTV analyses are routine, a systematic population-level search for *secular* TTV drifts using the 12+ year Kepler-to-TESS baseline is a qualitatively new capability that has only recently become possible. Most TTV studies focus on periodic (sinusoidal) signals from known planet pairs near resonance. Secular drifts — caused by long-period perturbers on timescales longer than the Kepler mission — have been largely inaccessible until the TESS extended mission provided the necessary temporal leverage. The goal here is not just detection but dynamical inversion: turning a measured drift rate and curvature into posterior constraints on the perturber's mass and period.

### Concrete Workflow

1. **Ephemeris bridging**: For all Kepler multi-planet systems re-observed by TESS (estimated ~500 systems), compute precise mid-transit times from TESS SPOC or QLP light curves. Combine with Kepler-era mid-times.
2. **Trend detection**: Fit each planet's O−C (observed minus calculated) transit time series with a polynomial model (linear + quadratic + cubic). Identify systems where the Bayesian evidence favors a quadratic or cubic term over a constant-period model (ΔlnZ > 5).
3. **Resonance proximity filter**: For systems with detected secular trends, check whether the drift rate is consistent with perturbation by a planet near a low-order (2:1, 3:2, 5:3, 3:1) resonance with the transiting planet.
4. **Dynamical inversion**: For the most significant detections, run N-body MCMC fits (using TTVFast or REBOUND) over the parameter space of the hidden planet (mass, period, eccentricity, inclination). Combine TTV constraints with any available RV data.
5. **Prediction and validation**: For the best-constrained ghost planets, predict their transit probability and expected transit depth. Flag systems where the perturber has >5% transit probability for targeted TESS or CHEOPS follow-up.

### Expected Signal / Observable

- A quadratic O−C drift of ~1–10 minutes over 12 years is detectable for Earth-to-Neptune-mass perturbers in orbits of 100–500 days.
- For super-Earths near 2:1 resonance with a known transiting planet, the expected TTV drift rate is ~0.5–5 min/decade, well within measurement precision for Kepler-TESS bridged baselines.
- The population-level yield: an estimated 10–30 new "ghost planet" candidates across the Kepler multi-planet sample, with dynamical mass constraints to within a factor of 2–3.

### Possible False Positives

- **Stellar activity-induced timing shifts**: Starspots near the transit chord can shift the apparent mid-time by ~10–30 seconds. Mitigation: correlate O−C residuals with stellar activity indicators (flux modulation amplitude, spot-crossing frequency); exclude systems with strong activity-timing correlations.
- **Orbital decay**: For very short-period planets, tidal orbital decay can produce a quadratic O−C trend. Mitigation: compute the expected decay rate from tidal theory; flag systems where the observed drift matches the tidal prediction.
- **Apsidal precession**: In eccentric systems, apsidal precession produces a periodic O−C signal that over a short baseline can mimic a secular trend. Mitigation: fit precession models alongside hidden-planet models; use Bayesian model comparison.
- **Light-time effect from a stellar binary companion**: An unseen stellar companion causes the system barycenter to move, producing long-term TTV trends. Mitigation: check for Gaia RUWE > 1.4 (indicating astrometric excess noise from a companion); include a linear drift term in the model.

### Why This Could Matter

Kepler revealed that tightly-packed inner planetary systems are common, but the outer architecture of these systems is almost entirely unknown. This project would provide the first statistical census of "cold" planets (P ~ 100–500 days) in Kepler multi-planet systems — a population that is largely invisible to both transit surveys (low geometric probability) and RV surveys (long baselines needed). Understanding the outer boundary conditions of compact inner systems is critical for testing formation theories: did these planets form in situ, or did they migrate inward from a more extended configuration, leaving outer companions behind? The ghost planets hold the answer.

---

## Summary Table

| # | Project | Key Dataset | Primary Observable | Novelty Level |
|---|---------|------------|-------------------|--------------|
| 1 | Starspot Latitude Census | Kepler + TESS transits of K/M hosts | Spot latitude vs. Rossby number | Population-level dynamo test via transit tomography |
| 2 | Tidal Inflation Fossils | TEPCat obliquities + Kepler/TESS radii | Radius anomaly vs. obliquity for warm Neptunes | First controlled test of tidal memory in sub-giants |
| 3 | Ghost Planet Census | Kepler-to-TESS 12-yr TTV baseline | Secular O−C drifts → hidden perturber masses | Systematic dynamical inversion at population scale |

---

*Report generated autonomously. Design choices: focused on projects that leverage the unique 12+ year Kepler-to-TESS baseline or population-scale approaches that were not possible even 2 years ago. All datasets referenced are publicly available.*
