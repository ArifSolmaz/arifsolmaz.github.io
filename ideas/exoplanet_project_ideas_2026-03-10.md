# Exoplanet Research Project Ideas — March 10, 2026

Three ambitious, potentially underexplored project concepts grounded in publicly available mission data.

---

## 1. Mapping the Tidal Graveyard: A Frequency-Resolved Census of Orbital Decay Signatures Across the TESS Extended Mission

### Scientific Premise

We know hot Jupiters are spiraling into their host stars — the poster children being WASP-12 b and Kepler-1658 b, whose orbital periods are measurably shrinking in real time. But the *population-level statistics* of orbital decay remain remarkably thin. Recent work on 188 hot Jupiters has shown that the stellar tidal quality factor Q'★ climbs sharply with forcing frequency (from ~10⁵ to ~10⁷ across a factor-of-four frequency range), which implies that the efficiency of tidal dissipation is not a single number but a steep function of the planet's orbital frequency relative to the star's spin. Most studies still treat Q'★ as a constant. This project would build a homogeneous transit-timing catalog from all available TESS sectors (now spanning 6+ years of baseline for many fields) and combine it with archival Kepler/K2 data to construct a *frequency-resolved tidal dissipation map* of the short-period giant planet population.

### Target Datasets

- TESS full-frame images and 2-minute cadence light curves (all sectors through Extended Mission 2)
- Kepler and K2 long- and short-cadence photometry (MAST archive)
- Published radial velocity masses from the NASA Exoplanet Archive
- Gaia DR3 stellar parameters and ages

### Novelty

While individual orbital-decay detections exist, no study has systematically measured (or placed upper limits on) period derivatives for the full short-period giant population using a uniform pipeline, then decomposed the resulting Q'★ distribution as a function of tidal forcing frequency, stellar structure (convective envelope depth), and system age. The frequency dependence itself is a direct probe of dissipation physics — distinguishing equilibrium tide theory from dynamical (inertial wave) models — but it has only been studied statistically, not via direct Pdot measurements across the population.

### Concrete Workflow

1. Build a uniform transit-timing pipeline (e.g., using `batman` + nested sampling) applied to every confirmed hot Jupiter with P < 3.5 days observed by both TESS and Kepler/K2.
2. Measure mid-transit times with per-epoch uncertainties; fit linear and quadratic ephemerides.
3. For systems with a significant quadratic term (Pdot), derive Q'★. For non-detections, compute 2σ upper limits on |Pdot|.
4. Bin results by tidal forcing frequency (≈ 2/P_orb − 2/P_rot), stellar T_eff (proxy for convective envelope depth), and gyrochronological age.
5. Compare the observed Q'★(f) relation to predictions from equilibrium-tide and inertial-wave dissipation models.

### Expected Signal / Observable

A measurable period shift of ~1–50 ms over a 10-year Kepler-to-TESS baseline for systems with Q'★ ≲ 10⁶. Even non-detections constrain Q'★ > 10⁷ and are informative. The key deliverable is a Q'★-vs-frequency diagram with actual measurements (not just population inference).

### Possible False Positives

- Apsidal precession in mildly eccentric orbits mimics a quadratic TTV. Mitigation: fit for eccentricity using secondary-eclipse timing or radial velocities.
- Rømer delay from a long-period companion produces a parabolic TTV. Mitigation: include a cubic term and check for radial-velocity trends.
- Stellar activity–induced transit-time shifts at the ~10 s level. Mitigation: model starspot crossing events; compare results across wavelengths if multi-band data exist.

### Why It Matters

This would provide the first direct, frequency-resolved measurement of tidal dissipation in planet-hosting stars — a fundamental input for predicting the fate of close-in planets, understanding angular momentum evolution, and calibrating tidal theory for binary stars and compact objects alike.

---

## 2. Disintegrating Worlds as Mantle Spectrometers: A Dust-Composition Survey of Catastrophically Evaporating Planets

### Scientific Premise

A handful of ultra-short-period planets (USPs) are known to be actively losing mass, producing asymmetric, variable-depth transits caused by a comet-like tail of sublimated rock dust (e.g., KIC 12557548 b from Kepler, and the recently discovered nearest disintegrating planet from TESS). These "disintegrating planets" are literally exposing their interior composition to spectroscopic study — the dust tail carries mineral grains whose wavelength-dependent scattering/absorption signatures encode whether the mantle is iron-rich, silicate-dominated, or enriched in refractory species like corundum or perovskite. Yet only a few individual systems have been modeled in detail, and no systematic survey has attempted to classify the interior mineralogy of all known disintegrating planets using a common forward-modeling framework.

### Target Datasets

- TESS light curves (multi-sector, for transit depth variability and color dependence from FFI vs. 20-s cadence)
- Kepler long-cadence data for KIC 12557548 b (4 years of variable transits)
- JWST Cycle 1–4 public archive: any NIRSpec, MIRI, or NIRCam time-series observations of USPs
- Spitzer 3.6 and 4.5 μm archival secondary eclipse and transit photometry for USPs

### Novelty

Most existing work on disintegrating planets focuses on dynamical modeling of the mass-loss rate or on reproducing the asymmetric transit shape. The mineralogical angle — using multi-wavelength transit depths to constrain the *dust composition* and hence *mantle geochemistry* of rocky exoplanets — is potentially underexplored at the population level. This project would build a Mie-scattering + radiative transfer forward model for the dust tail and apply it uniformly to every known (and candidate) disintegrating system, producing the first comparative mineralogical study of exoplanetary mantles.

### Concrete Workflow

1. Compile all confirmed and candidate disintegrating-planet systems (currently ~5–8 objects) from the literature and from a targeted search of TESS data for variable-depth, asymmetric transits around USPs.
2. For each system, extract multi-band transit depths: optical (TESS/Kepler), near-IR (JWST if available), mid-IR (Spitzer archival).
3. Build a parametric dust-tail model: particle size distribution (power law), composition (mixtures of olivine, pyroxene, iron, corundum, etc.), and optical depth profile.
4. Use Mie theory to compute wavelength-dependent extinction and fit the multi-band transit depths simultaneously.
5. Derive posterior distributions on grain composition fractions; compare across systems and to Solar System meteorite mineralogies.

### Expected Signal / Observable

Wavelength-dependent transit depth variations of ~0.01–0.1% between optical and mid-IR bands, depending on grain size and composition. Iron-rich grains produce a flatter extinction curve; silicate grains show a pronounced ~10 μm feature in MIRI data. Even with only broadband photometry, the optical-to-IR depth ratio constrains the mean grain size and Fe/Si ratio.

### Possible False Positives

- Stellar limb-darkening variations between bands can mimic chromatic transit depth changes. Mitigation: use consistent limb-darkening models (e.g., from `ExoTiC-LD`) and fit for limb-darkening coefficients.
- Variability from starspots produces epoch-to-epoch depth changes that are not dust-related. Mitigation: use contemporaneous out-of-transit flux monitoring to detrend spot modulation.
- Grain size degeneracy with composition in broadband data. Mitigation: use JWST spectroscopy where available; otherwise, clearly report the degeneracy.

### Why It Matters

We have no direct measurement of the mantle composition of any rocky exoplanet. Disintegrating planets offer a unique natural experiment — literally ablating their interiors into observable space. A comparative mineralogical survey could reveal whether rocky planet mantles are universally Earth-like or show significant diversity, with implications for planetary formation, differentiation, and ultimately habitability.

---

## 3. The Nightside Rotation Signal: Detecting Atmospheric Super-Rotation and Jet Structure from TESS Phase Curve Residuals

### Scientific Premise

Full-orbit phase curves from Spitzer and TESS have revealed that many hot Jupiters have their brightest hemisphere shifted eastward from the substellar point — the canonical signature of equatorial super-rotation. But the *amplitude and phase offset of higher-order harmonics* in the phase curve (beyond the fundamental sinusoid) encode information about the latitudinal and vertical structure of atmospheric jets. General circulation models (GCMs) predict that the second harmonic (C₂) should be sensitive to the presence of mid-latitude jets, polar vortices, and day-night asymmetries in cloud coverage. Yet most observational phase-curve analyses stop at the first harmonic (C₁) because the signal-to-noise in individual systems is marginal for higher orders. This project would stack phase curves across the TESS hot Jupiter population to extract the *population-averaged* second-harmonic signal and its dependence on equilibrium temperature and surface gravity.

### Target Datasets

- TESS 2-minute and 20-second cadence light curves for all confirmed transiting hot Jupiters with T_eq > 1500 K and orbital periods < 3 days (estimated ~40–60 systems with sufficient TESS coverage)
- Spitzer 3.6 and 4.5 μm full-orbit phase curves (archival; ~30 systems from the "Ultimate Spitzer Phase Curve Survey")
- Published GCM outputs for comparison (e.g., from the SPARC/MITgcm grid)

### Novelty

Population-level phase-curve stacking to extract higher-order harmonics is, to my knowledge, potentially underexplored. Individual high-SNR systems (WASP-18 b, WASP-121 b) have had their phase curves decomposed into harmonics, but no one has combined the full TESS sample to beat down photon noise and measure the *mean* C₂ amplitude and phase as a function of planetary parameters. This is analogous to what galaxy surveys do with stacking — trading individual detail for statistical power. The result would be a direct, model-independent constraint on the prevalence and structure of non-axisymmetric atmospheric circulation patterns.

### Concrete Workflow

1. Select all hot Jupiters with T_eq > 1500 K, measured masses, and ≥ 2 TESS sectors of continuous coverage.
2. Detrend each light curve for stellar variability and instrument systematics using a Gaussian process with a Matérn-3/2 kernel.
3. Phase-fold each system on its known ephemeris; fit a two-harmonic Fourier model: F(φ) = F₀ + C₁ cos(φ − δ₁) + C₂ cos(2φ − δ₂), where φ is orbital phase.
4. Normalize C₁ and C₂ by the secondary eclipse depth (dayside flux) to obtain fractional harmonic amplitudes.
5. Bin systems by T_eq (1500–2000 K, 2000–2500 K, 2500+ K) and by log(g). Compute the weighted-mean C₂/C₁ ratio and δ₂ offset in each bin.
6. Compare the population-averaged C₂/C₁ and δ₂ to predictions from a grid of GCM simulations spanning the same parameter space.

### Expected Signal / Observable

GCMs predict C₂/C₁ ratios of ~0.05–0.20 for hot Jupiters, with the second harmonic phase offset δ₂ shifting from ~0° (symmetric day-night contrast) to ~45° (jet-driven asymmetry) as T_eq increases and clouds dissipate. In individual TESS systems, C₂ is typically detected at only 1–2σ; stacking ~20 systems per bin should push this to 4–6σ.

### Possible False Positives

- Ellipsoidal variations from tidal distortion produce a C₂ signal at fixed phase. Mitigation: model and subtract the ellipsoidal + Doppler beaming contribution using the known planet mass and stellar density.
- Residual stellar variability at the second harmonic of the orbital period. Mitigation: verify that out-of-transit variability does not show power at 2/P_orb; exclude systems with significant stellar rotation signals near this frequency.
- Inhomogeneous detrending across systems could introduce a spurious stacked signal. Mitigation: use a uniform pipeline and perform a null test by stacking phase curves at a randomized phase offset.

### Why It Matters

Atmospheric circulation is the engine that redistributes energy on tidally locked worlds, governing their climate, chemistry, and observational appearance. The second harmonic of the phase curve is a direct diagnostic of jet structure that GCMs make specific predictions about but that has never been tested at the population level. A detection (or meaningful upper limit) would constrain the physics of atmospheric drag, magnetic braking, and cloud radiative feedback in a regime with no Solar System analog — information that feeds directly into interpreting JWST transmission and emission spectra.

---

*Generated on March 10, 2026. Sources include the NASA Exoplanet Archive, TESS/Kepler/Spitzer archival data holdings, and recent literature.*
