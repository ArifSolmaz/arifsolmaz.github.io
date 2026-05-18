# Ambitious Exoplanet Research Project Ideas

**Generated: May 11, 2026** | Scheduled task: *exoplanet research strategist*

---

## Project 1: Chromatic Transit Asymmetries as Probes of Circumplanetary Ring Systems in the Kepler Long-Cadence Archive

### Scientific Premise

Despite thousands of confirmed transiting exoplanets, no circumplanetary ring system has been unambiguously detected beyond the solar system (the J1407b "super-ring" candidate remains debated and orbits far from its star). Rings around close-in planets are theoretically unstable due to tidal forces and sublimation, but at intermediate separations (roughly 0.3–2 AU) rings of icy or rocky debris could persist. A ringed planet produces a transit light curve that differs subtly from a bare sphere: the ingress/egress profile becomes shallower and more extended, the effective transit depth is wavelength-dependent (because ring particles scatter and absorb differently at different wavelengths), and the transit shape can be slightly asymmetric if the rings are inclined to the orbital plane.

The key insight is that most ring searches have targeted individual high-profile systems or used single-band photometry. A *systematic, population-level* search across the full Kepler long-cadence archive — looking not for individual detections but for a *statistical excess* of transit-shape anomalies correlated with orbital and stellar parameters — is potentially underexplored and could yield either detections or the strongest upper limits to date on ring occurrence rates.

### Target Datasets

- **Kepler DR25 long-cadence light curves** (MAST archive): ~2,600 confirmed planets and ~4,000 KOIs. The 4-year baseline gives superb phase-folded signal-to-noise for planets with P < 300 d.
- **Kepler short-cadence data** for the ~200 brightest targets with candidate anomalies (for confirmation and ingress/egress timing).
- **TESS FFI light curves** (SPOC or QLP pipelines) for any Kepler targets re-observed, providing a second epoch and slightly different bandpass.
- **NASA Exoplanet Archive** composite planet parameters for filtering by semi-major axis, planet radius, and equilibrium temperature.

### Novelty

Individual ring searches exist (e.g., Heising et al. 2015 on Kepler; Akinsanmi et al. 2020 on selected targets), but they typically fit ring models to single systems. This project would be distinct in three ways: (1) it operates at the population level, seeking a *statistical* ring signal across hundreds of warm sub-Saturns and Jupiters simultaneously; (2) it uses the *residuals* of standard transit fits as the data product, rather than re-fitting full ring models to every system; (3) it correlates anomaly metrics with physical parameters (Roche limit proximity, equilibrium temperature, stellar metallicity) to test ring formation/survival theory.

### Concrete Workflow

1. Download phase-folded, detrended Kepler light curves for all confirmed planets and vetted KOIs with Rp > 4 R⊕ and a/R★ > 5 (to exclude ultra-close-in planets where rings cannot survive).
2. Fit each phase-folded transit with a standard Mandel & Agol (2002) limb-darkened model using a fast fitter (e.g., batman + emcee or dynesty).
3. Compute three anomaly metrics on the residuals: (a) ingress–egress asymmetry (difference in best-fit ingress vs. egress duration), (b) "shoulder excess" (integrated residual flux in the 15-minute windows flanking first and fourth contact), and (c) transit depth ratio between Kepler's blue and red halves of the bandpass (using the Kepler pixel-level data or the multi-quarter PDC corrections to construct quasi-chromatic light curves, following the method of Désert et al. 2015).
4. Build a hierarchical Bayesian model that treats the ring occurrence rate and typical ring optical depth as population-level hyperparameters, with per-planet anomaly metrics as observations. Include nuisance terms for starspot crossings, TTVs, and limb-darkening misspecification.
5. Inject synthetic ring transits (using the Zuluaga et al. 2015 ring transit code) into real Kepler light curves to calibrate detection efficiency as a function of ring size, tilt, and optical depth.
6. Report either a detection (with posterior on ring properties) or a 95% upper limit on the ring occurrence rate as a function of planet class and orbital separation.

### Expected Signal / Observable

For a Saturn-like ring system (ring outer radius ~2× planet radius, optical depth ~0.5) around a Jupiter-sized planet orbiting a Sun-like star at 0.5 AU, the ingress/egress duration changes by ~5–15% and the shoulder excess is ~50–200 ppm in the phase-folded Kepler light curve. Individual detections are marginal (2–3σ) but the population stack across ~100 warm Jupiters/sub-Saturns could reach 5σ+ if rings are common (~10% occurrence).

### Possible False Positives

- **Starspot crossings** during ingress/egress mimic asymmetric residuals. Mitigation: correlate anomaly metrics with stellar variability amplitude; exclude epochs with obvious spot-crossing bumps.
- **Limb-darkening misspecification** produces systematic ingress/egress residuals. Mitigation: use flexible limb-darkening (quadratic + Gaussian process) and check that anomaly metrics do not correlate with impact parameter.
- **Transit timing variations** from unseen companions shift individual transits and smear the phase-folded profile. Mitigation: fit per-epoch mid-transit times and remove TTV signal before phase-folding.
- **Blended eclipsing binaries** can produce asymmetric-looking transits. Mitigation: restrict to confirmed planets with centroid validation or Gaia DR3 RUWE < 1.4.

### Why It Could Matter

Circumplanetary rings constrain the collisional and tidal environment around giant planets — their presence or absence at different orbital separations directly tests models of ring formation (captured debris vs. disrupted moons) and ring lifetimes (Poynting-Robertson drag, plasma sputtering). A population-level constraint would be the first of its kind and would be immediately relevant to planning future direct-imaging missions (HWO/LUVOIR) that could spatially resolve ring systems.

---

## Project 2: Mining Planet-Induced Stellar Flares to Map Exoplanetary Magnetic Fields Across the Hot Jupiter Population

### Scientific Premise

Star-planet magnetic interactions (SPI) have been theorized for two decades: a close-in planet orbiting inside its host star's sub-Alfvénic radius can channel energy along magnetic field lines connecting the planet to the stellar surface, triggering localized chromospheric hot spots and, in some cases, flares that are phase-locked to the planet's orbit. Recent work has confirmed this phenomenon in the young system HIP 67522 (Nature, 2025), where flares are statistically concentrated at specific orbital phases of the inner planet. Earlier, Cauley et al. (2019) inferred magnetic field strengths of 20–120 G for four hot Jupiters via Ca II K emission modulated at the planetary orbital period.

Despite these breakthroughs, no one has performed a *systematic, blind survey* of the full TESS short-cadence archive to identify phase-correlated flare excesses across the entire hot Jupiter population. The TESS dataset now spans 6+ years and covers most known hot Jupiter hosts at 2-minute or 20-second cadence. A population-level search could (a) dramatically expand the sample of SPI detections, (b) measure or constrain planetary magnetic field strengths as a function of planet mass, age, and orbital separation, and (c) test whether SPI scales with the sub-Alfvénic condition as theory predicts.

### Target Datasets

- **TESS 2-minute and 20-second cadence light curves** (MAST/SPOC) for all confirmed hot Jupiter hosts (~500 systems with a < 0.1 AU).
- **TESS Full-Frame Images** (30 min / 10 min / 200 s cadence depending on sector) for fainter hosts not observed at short cadence.
- **Ephemerides** from the NASA Exoplanet Archive (orbital period, epoch, eccentricity).
- **Stellar activity indicators**: TESS light curve variability (rotation period, spot modulation amplitude), plus archival Ca II H&K and Hα indices from spectroscopic surveys (LAMOST, GALAH DR4, California Legacy Survey) where available.

### Novelty

The HIP 67522 detection was a single-system study of an unusually young star. Cauley et al. (2019) used spectroscopic monitoring of four hand-picked systems. This project would be distinct because it: (1) is a *blind, population-level* flare-phase analysis of hundreds of hot Jupiter systems simultaneously; (2) uses photometric flare detection on TESS data (which is far more abundant than spectroscopic time series); (3) builds a hierarchical model that treats the SPI flare rate enhancement as a function of physical parameters (planet mass, semi-major axis, stellar B-field proxy, sub-Alfvénic radius), enabling the first empirical scaling relation for star-planet magnetic coupling.

### Concrete Workflow

1. Compile a target list of all confirmed transiting hot Jupiters with TESS short-cadence data (expected ~300–400 systems with adequate coverage).
2. Apply an automated flare detection pipeline (e.g., AltaiPony or stella, both open-source and trained on TESS data) to every light curve. Record flare start times, durations, and energies.
3. Phase-fold flare occurrence times to the planetary orbital period for each system. For each system, compute the Rayleigh statistic (Z²) to test whether flare times are uniformly distributed in orbital phase or clustered.
4. At the population level, stack the phase-folded flare distributions across all systems (weighted by the number of flares per system). Test for a global excess at the expected SPI phase (near the sub-planetary longitude or shifted by the Parker spiral angle, depending on the Alfvén travel time).
5. Bin the sample by planet mass, orbital period, and stellar activity level. Fit a hierarchical Bayesian model: the SPI flare rate enhancement Δf is parameterized as Δf ∝ (Bp × Rp²) / (a² × v_sw), where Bp is the planetary magnetic field, Rp is planet radius, a is separation, and v_sw is stellar wind speed (proxied by stellar activity). This lets you solve for Bp (or its distribution) as the key latent variable.
6. Validate by checking that the signal disappears for a control sample of planets at a > 0.3 AU (where sub-Alfvénic interaction should be negligible).

### Expected Signal / Observable

In HIP 67522, the planet-correlated flare rate was roughly 2–3× the baseline rate at specific orbital phases. For the broader hot Jupiter population, a more modest enhancement (~20–50% in phase-binned flare rate) would be expected, detectable at 3–5σ when stacking across ~100+ active host stars. Systems with young, active hosts and massive, close-in planets should show the strongest signal.

### Possible False Positives

- **Stellar rotation aliasing**: If the stellar rotation period is close to the planetary orbital period (tidal synchronization), activity modulation mimics orbital-phase-locked flaring. Mitigation: measure the stellar rotation period from the light curve; exclude systems where P_rot/P_orb is within 5% of an integer ratio; test whether the flare-phase signal persists after removing the rotational modulation.
- **Small-number statistics**: Many systems will have few flares. Mitigation: the hierarchical model properly handles low-count systems by shrinking toward the population mean; the detection is made at the population level, not per-system.
- **Flare detection false positives**: Instrumental artifacts or cosmic rays flagged as flares. Mitigation: use injection-recovery tests to characterize the flare pipeline's false positive rate; require flares to span at least 3 consecutive cadences.

### Why It Could Matter

Exoplanetary magnetic fields are among the most important yet poorly constrained properties in exoplanet science. Magnetic fields govern atmospheric escape rates (and thus long-term atmospheric evolution), control the interaction between planetary magnetospheres and stellar winds, and may be a prerequisite for surface habitability. A population-level measurement of hot Jupiter magnetic field strengths as a function of mass and age would be the first empirical constraint on the planetary magnetic dynamo scaling law beyond our solar system — directly relevant to understanding whether terrestrial planets in habitable zones retain protective magnetospheres.

---

## Project 3: Secular Transit Duration Drift as a Direct Probe of Orbital Precession and Planetary Oblateness

### Scientific Premise

When a planet's orbit precesses (due to general relativity, tidal bulges, rotational oblateness of the planet, or perturbations from other bodies), the transit duration changes secularly over time. For a planet with significant oblateness (J₂), the quadrupole moment of its gravitational field causes apsidal precession at a rate proportional to J₂ × (R_p/a)⁵. This precession shifts the argument of pericenter, which in turn changes the impact parameter and transit duration on timescales of years to decades. The Kepler mission observed many systems for 4 years; TESS has now been operating for 6+ years. For systems observed by both, the baseline extends to 12–15 years — long enough that transit duration changes of ~10–60 seconds should be measurable for close-in giant planets with significant oblateness.

Transit duration variations (TDVs) have been discussed theoretically but measured in very few systems. Most TTV studies focus on mid-transit *timing* and ignore the complementary information in transit *duration*. A systematic search for secular TDV trends across the full Kepler+TESS overlap sample is potentially underexplored and could yield the first measurements of exoplanetary J₂ (oblateness), which encodes information about the planet's interior structure, rotation rate, and tidal state.

### Target Datasets

- **Kepler long-cadence and short-cadence light curves** (DR25): provide the early-epoch transit durations (2009–2013).
- **TESS light curves** (Sectors 1–83+): provide late-epoch transit durations (2018–2026). For Kepler-field targets, TESS observed them primarily in Sectors 14, 26, 40, 41, 54, 55, etc.
- **Ground-based transit photometry** from ExoClock, ETD (Exoplanet Transit Database), and EXOTIC archives: fill in the gap between Kepler and TESS and extend the baseline.
- **NASA Exoplanet Archive**: orbital elements, planet radii, stellar parameters.

### Novelty

TTV analyses are abundant; TDV analyses are rare. Existing TDV work has been limited to a handful of individual systems (e.g., Kepler-9, WASP-12). This project would be the first *systematic survey* of secular TDV trends across the Kepler+TESS overlap sample (~1,000+ planets), with the explicit goal of measuring or constraining J₂ for giant planets. It is distinct from transit-duration studies aimed at detecting exomoons (which look for periodic TDVs, not secular trends) and from TTV studies (which measure timing, not duration). The combination of Kepler precision with the long TESS baseline creates a unique opportunity that did not exist even three years ago, as the TESS extended missions have now accumulated enough sectors over the Kepler field.

### Concrete Workflow

1. Identify all Kepler confirmed planets and KOIs that have been re-observed by TESS with sufficient photometric precision to measure individual transit durations to <2-minute accuracy. Expected sample: ~200–400 planets (mostly Jupiters and sub-Saturns around bright hosts).
2. For each system, fit individual transits in both the Kepler and TESS light curves using a uniform transit model (e.g., batman), extracting posterior distributions on transit duration (T₁₄ = total duration, T₂₃ = full duration) and mid-transit time for each epoch.
3. Fit a linear trend to T₁₄ as a function of epoch number. Compute the secular drift rate dT₁₄/dt for each planet, with uncertainties propagated from the individual transit fits.
4. Compare measured drift rates to theoretical predictions for different precession mechanisms:
   - General relativistic precession: dω/dt ∝ (GM★)^(3/2) / (a^(5/2) c² (1-e²)). Predictable from known orbital elements.
   - Planetary oblateness (J₂): dω/dt ∝ J₂ (R_p/a)² n / (1-e²)². The free parameter is J₂.
   - Companion-induced precession: dω/dt depends on the perturber's mass and orbit. Can be jointly constrained with TTVs.
5. For planets with detected TDV trends that exceed the GR prediction, fit for J₂ (or J₂ + companion mass). Use the inferred J₂ to constrain the planet's rotation rate and Love number via interior structure models (e.g., MESA + planetary interior codes).
6. For non-detections, report 2σ upper limits on J₂, which still constrain models (e.g., ruling out rapid rotation or low-density inflated interiors).

### Expected Signal / Observable

For a hot Jupiter with J₂ ~ 0.01 (comparable to Saturn's 0.016) at a = 0.05 AU, the apsidal precession rate from oblateness alone is ~0.01–0.1 deg/yr, producing a transit duration change of ~5–30 seconds over a 12-year Kepler-to-TESS baseline. Kepler short-cadence data can measure individual transit durations to ~10–30 s precision; phase-folding multiple TESS transits further improves the late-epoch measurement. A 3σ detection of a 20-second drift is feasible for ~10–30 of the brightest, most favorable systems.

### Possible False Positives

- **Stellar variability**: Starspot-induced asymmetries in the transit profile can bias the fitted transit duration. Mitigation: fit for spot-crossing events explicitly; compare results using different detrending methods (GP vs. polynomial vs. CBV); check that TDV trends are independent of stellar activity cycle phase.
- **Systematic differences between Kepler and TESS**: Different bandpasses, pixel scales, and detrending pipelines introduce instrument-dependent biases in measured transit shape. Mitigation: inject synthetic transits with known durations into both Kepler and TESS data; calibrate any instrument-dependent offset in recovered T₁₄; include an instrument offset term in the TDV fit.
- **Eccentricity–argument of pericenter degeneracy**: If the orbit is slightly eccentric and the argument of pericenter is poorly constrained, precession is degenerate with the initial orbital orientation. Mitigation: use radial velocity data (from archival surveys) to independently constrain e and ω; focus on systems with well-characterized orbits.
- **Long-term TTVs**: A massive outer companion can induce both TTVs and TDVs simultaneously. Mitigation: jointly fit TTVs and TDVs; an outer companion produces correlated, quasi-periodic variations in both, while oblateness produces a smooth, secular TDV trend with no TTV counterpart.

### Why It Could Matter

Measuring J₂ for exoplanets would open a new window into their interior structure: oblateness encodes the planet's rotation rate, density profile, and response to tidal forces. For hot Jupiters, which are expected to be tidally synchronized (slowly rotating, low J₂) but are often observed to be anomalously inflated, J₂ measurements could distinguish between different inflation mechanisms (ohmic dissipation, tidal heating, delayed cooling) that predict different internal density distributions. This would represent one of the few ways to probe exoplanet interiors without relying on atmospheric spectroscopy.

---

## Summary Table

| # | Project | Key Dataset | Primary Observable | What You'd Measure |
|---|---------|------------|-------------------|-------------------|
| 1 | Population-level exoring search | Kepler DR25 + TESS | Ingress/egress asymmetry, shoulder excess | Ring occurrence rate vs. orbital separation |
| 2 | Star-planet magnetic interaction survey | TESS short-cadence | Phase-correlated flare rate | Planetary magnetic field strength distribution |
| 3 | Secular transit duration drift | Kepler + TESS (12-yr baseline) | dT₁₄/dt | Planetary J₂ (oblateness / interior structure) |

---

*Note: These ideas are identified as potentially underexplored rather than completely unstudied. Each builds on existing theoretical frameworks and pilot studies but proposes a scale or methodology that has not been systematically applied. Literature review prior to proposal development is recommended to confirm the current state of each subfield.*
