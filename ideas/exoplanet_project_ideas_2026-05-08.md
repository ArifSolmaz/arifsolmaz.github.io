# Ambitious Exoplanet Research Project Ideas

*Generated May 8, 2026 — grounded in the current literature and publicly available mission data*

---

## Project 1: Eclipse-Depth Variability as a Probe of Surface Geology on Rocky Exoplanets

### Scientific Premise

JWST's "Hot Rocks Survey" is now delivering secondary-eclipse photometry for a growing sample of rocky exoplanets around M dwarfs (TRAPPIST-1 b/c, GJ 3473 b, LHS 3844 b, and others). A striking but underexplored signal has emerged: visit-to-visit variability in eclipse depth. For GJ 3473 b, the MIRI F1500W eclipse depth swings from roughly 33 to 371 ppm across visits. The community has largely treated this scatter as systematic noise or weather. But if these planets are airless (as the data increasingly suggest), there is no weather — so what is changing? One plausible answer is that we are seeing the thermal signature of heterogeneous surface geology on a synchronously rotating world whose sub-observer longitude shifts slightly due to libration or slight orbital eccentricity. Different mineral assemblages (basalt, feldspar, iron oxide, sulfur deposits) have dramatically different thermal inertias and emissivities at 15 µm, meaning the hemisphere-integrated dayside flux genuinely changes as the planet rocks back and forth.

### Target Datasets

- All public JWST/MIRI secondary-eclipse photometry of rocky exoplanets (currently ~8–10 targets with at least two visits each), available via MAST.
- Complementary Spitzer/IRAC 4.5 µm archival photometry of the same or similar targets for cross-wavelength comparison.
- Laboratory reflectance/emissivity spectra of planetary analog minerals from the RELAB and ECOSTRESS spectral libraries.

### Novelty

The 2026 "Uniform Reinterpretation" paper by Ih et al. reanalyzed rocky-planet eclipses but focused on systematic offsets from stellar/orbital uncertainties, not on the temporal scatter itself. No published study has yet built a forward model connecting surface mineralogy heterogeneity + forced libration to predicted eclipse-depth variability amplitudes and timescales. This project would be the first to treat visit-to-visit eclipse scatter as signal rather than noise.

### Concrete Workflow

1. Compile all multi-visit MIRI eclipse depths and uncertainties from published reductions and, where possible, re-extract from the Stage 2 JWST pipeline products.
2. Compute the expected libration amplitude for each target from its measured or constrained eccentricity (using values from the NASA Exoplanet Archive and radial-velocity constraints).
3. Build a hemispherically resolved thermal model: tile the dayside into ~100 facets, assign each facet a mineral class drawn from a parameterized spatial distribution, propagate the mineral's thermal inertia and 15 µm emissivity through a 1D heat conduction model, and integrate the emergent flux over the visible hemisphere at each libration phase.
4. For each target, run an MCMC over the mineral mixture fractions and spatial correlation length, fitting the observed eclipse-depth distribution (mean and variance).
5. Perform model comparison (BIC/evidence) against the null hypothesis that all scatter is Gaussian noise with no physical origin.

### Expected Signal / Observable

For a planet with eccentricity ~0.01 (giving ~2° of optical libration) and a surface split between low-inertia regolith and high-inertia basalt, the model predicts eclipse-depth modulations of 30–80 ppm at 15 µm — consistent with the scatter already seen in GJ 3473 b. A positive detection would manifest as eclipse-depth variance significantly exceeding the per-visit measurement uncertainty, with the excess variance correlating with the predicted libration amplitude across the sample.

### Possible False Positives

- Uncorrected JWST detector systematics (ramp effects, charge migration) that differ between visits.
- Stellar variability of the M-dwarf host imprinting at 15 µm (though M-dwarf flux variability at these wavelengths is expected to be very small).
- Residual pointing jitter placing the PSF on different detector regions with slightly different flat-field responses.
- Mitigation: the libration hypothesis makes a specific prediction — that the eclipse-depth modulation amplitude should scale with orbital eccentricity across the sample, while systematics would not.

### Why It Could Matter

If eclipse-depth variability encodes surface composition, it would be the first remote detection of geology on an exoplanet — a fundamentally new observable. It would also inform whether these worlds are primordial bare rocks, lava-resurfaced, or mantled in impact regolith, connecting directly to questions about interior evolution and volatile delivery.

---

## Project 2: Mining Kepler–TESS Transit Timing Baselines for Unseen Giant Companions on Saturn-like Orbits

### Scientific Premise

The Kepler mission ended in 2018, and TESS has now been observing for over seven years. For the ~200 Kepler transiting planets that also fall in TESS's continuous viewing zone, we now have a transit-timing baseline of 12+ years. This baseline is long enough to detect gravitational perturbations from unseen outer companions on orbits of 5–15 years — the Saturn-analog regime — via long-period transit timing variations (TTVs). Recent catalog work (Kokori et al. 2025) found 22 new TTV signals in a sample of 111 Kepler/K2 planets, but their analysis focused on refining ephemerides rather than performing a systematic, injection-recovery-calibrated search for outer giant planets. The Saturn-analog occurrence rate around Sun-like stars is poorly constrained by radial velocity surveys (incomplete at long periods) and direct imaging (sensitive only to young, massive planets at wide separations). TTVs over a decade-plus baseline could fill this gap in a regime no other method currently probes well.

### Target Datasets

- Kepler long-cadence and short-cadence light curves (DR25) for all confirmed single-transiting planets in the Kepler field.
- TESS Full-Frame Image (FFI) light curves from Sectors 14–83+ (the Kepler field is in TESS's northern continuous viewing zone), extracted via publicly available pipelines (Eleanor, TESS-SPOC, QLP).
- NASA Exoplanet Archive for system parameters, and ExoClock/ETD for additional ground-based transit times.

### Novelty

Most TTV studies target near-resonant multi-planet systems where signals are large and short-period. The idea of using decade-long baselines to detect non-resonant, wide-orbit perturbers has been discussed theoretically but never executed as a uniform survey across the full Kepler single-transiter sample with TESS follow-up incorporated. The key insight is that even a Jupiter- or Saturn-mass planet at 5–10 AU induces a slowly varying, quasi-linear trend in transit times of the inner planet — a signal that looks like a simple ephemeris drift over short baselines but reveals curvature (the hallmark of a Keplerian perturbation) over 12+ years.

### Concrete Workflow

1. Select all Kepler single-transiters with at least 30 well-measured Kepler transit times and at least 3 TESS transit detections (estimated sample: ~150 systems).
2. Extract individual transit times from both missions using a uniform transit-fitting pipeline (e.g., batman + emcee), carefully accounting for the different cadences and noise properties.
3. Fit a linear ephemeris (constant period) and a quadratic ephemeris (linearly changing period) to each system's O–C diagram. Flag systems where the quadratic model is preferred at >3σ.
4. For flagged systems, fit a full two-body dynamical model: the known transiter plus an outer companion with free mass, period, eccentricity, and longitude of pericenter. Use the TTVFast code for speed.
5. Run a parallel injection-recovery campaign: inject synthetic TTV signals from outer companions with known parameters into the real data, re-run the detection pipeline, and map the completeness as a function of companion mass and orbital period.
6. Convert the detections (or upper limits) and the completeness map into an occurrence rate for giant planets at 5–15 AU around FGK stars — directly comparable to, and complementary with, radial-velocity occurrence rates.

### Expected Signal / Observable

A Saturn-mass planet at 8 AU perturbing an inner hot Jupiter produces O–C deviations of roughly 10–60 seconds over a 12-year baseline, depending on mutual inclination and eccentricity. This is well within the timing precision achievable from Kepler short-cadence data (~5–15 seconds per transit for bright targets) and TESS 2-minute cadence (~30–90 seconds), provided the TESS transits are stacked or modeled jointly. The signal would appear as a smooth, low-frequency curvature in the O–C diagram that cannot be explained by apsidal precession or stellar activity-induced transit-time noise.

### Possible False Positives

- Stellar activity (spot-crossing events) causing apparent transit-time shifts, particularly in TESS data where the photometric precision is lower.
- Apsidal precession in systems with non-zero eccentricity, which also produces a quadratic O–C trend but with a specific relationship to the known eccentricity and Love number.
- Light-travel-time effect (Roemer delay) from a stellar-mass binary companion, which mimics a planetary TTV signal but at larger amplitude.
- Mitigation: the dynamical model distinguishes these because the perturber's Keplerian signature has a characteristic shape (not purely quadratic), and radial-velocity constraints can rule out stellar-mass companions.

### Why It Could Matter

The occurrence rate of cold giant planets is a critical input to theories of planetary system architecture and the delivery of volatiles to inner rocky planets. Current constraints come almost entirely from radial velocities (biased toward metal-rich, quiet stars) and microlensing (statistical, no host-star characterization). A TTV-based measurement using Kepler+TESS would be the first to probe this population around a well-characterized sample of transiting-planet hosts, directly testing whether inner transiting planets and outer cold giants are correlated — a prediction of the "Grand Tack" and "peas in a pod" formation models.

---

## Project 3: Stellar Granulation Flicker as an Astrophysical Calibrator for JWST Transmission Spectra

### Scientific Premise

The biggest systematic threat to JWST transmission spectroscopy of small exoplanets is stellar contamination: unocculted starspots and faculae imprint a wavelength-dependent bias on the measured transit depth that can mimic or mask planetary atmospheric features. The standard correction (the Rackham/TLSE model) treats the stellar surface as a two-component mixture (quiet photosphere + active regions) and estimates filling factors from photometric variability. But a 2026 study showed this simplified model fails by up to 400 ppm in the optical for active hosts, and the correction depends sensitively on parameters (spot temperature, size distribution, spatial clustering) that are poorly constrained for most planet-hosting M and K dwarfs.

Here is the twist: stellar granulation — the convective pattern on the stellar surface — produces a broadband photometric "flicker" on timescales of minutes to hours that is directly measurable from the out-of-transit portions of JWST time-series observations. Crucially, the amplitude and spectral slope of granulation flicker depend on the same stellar surface properties (effective temperature, surface gravity, metallicity, convective velocity) that determine the spot-to-photosphere contrast and hence the contamination spectrum. In other words, granulation flicker is an independent, contemporaneous probe of the stellar surface physics that drives the contamination, available for free in every JWST transit observation.

### Target Datasets

- All public JWST NIRSpec and NIRISS/SOSS transit time-series observations (currently ~40–50 targets), focusing on the out-of-transit baseline segments.
- Kepler short-cadence (1-minute) light curves for the subset of targets in the Kepler field, providing high-precision flicker measurements at optical wavelengths.
- TESS 20-second and 2-minute cadence data for the broader sample.
- 3D magnetohydrodynamic (MHD) stellar atmosphere simulations from the Stagger grid and MURaM code, which predict both the granulation power spectrum and the spot/facula contrast as a function of stellar parameters.

### Novelty

Granulation flicker has been studied in the context of radial-velocity noise ("jitter") and asteroseismology, and recent 2025 work isolated granulation signals in synthetic spectral lines. But no one has yet used the measured granulation flicker in JWST transit baselines as a diagnostic constraint on the stellar contamination correction applied to the same observation. This project would close that loop: use the flicker to inform the contamination model, rather than treating them as separate problems.

### Concrete Workflow

1. For each public JWST transit observation, extract the white-light and spectroscopic (per-wavelength-bin) out-of-transit light curves at native time resolution.
2. Compute the granulation flicker amplitude (the RMS on 10-minute to 2-hour timescales after removing instrumental trends and any residual stellar rotation signal) in each wavelength bin.
3. Fit the observed flicker spectrum (amplitude vs. wavelength) with predictions from the Stagger 3D atmosphere grid, retrieving effective temperature, log(g), and a "granulation activity index."
4. Use the same 3D atmosphere grid to predict the spot-to-photosphere contrast spectrum and the expected stellar contamination signal for a given spot filling factor.
5. Combine the flicker-derived stellar surface constraint with the standard transit-depth fitting (using a retrieval code like POSEIDON or petitRADTRANS), marginalizing over the stellar contamination parameters with the flicker-informed prior rather than a flat prior.
6. Compare the retrieved atmospheric properties (H₂O, CO₂, CH₄ abundances, cloud-top pressure) with and without the flicker-informed prior. Quantify the reduction in degeneracy between stellar contamination and planetary atmosphere.

### Expected Signal / Observable

For a typical M3 dwarf host, granulation flicker at ~1 µm has an RMS of ~100–300 ppm on 30-minute timescales, measurable at high significance in a single JWST visit. The spectral slope of the flicker (bluer = larger amplitude) constrains the effective temperature of the granulation contrast to ~50 K, which in turn constrains the spot-photosphere temperature contrast to ~100 K — a factor of 3–5 improvement over the current uncertainty from broadband photometric monitoring alone. This tighter prior propagates into a ~30–50% reduction in the posterior uncertainty on retrieved molecular abundances for small planets around active stars.

### Possible False Positives

- Instrumental red noise (1/f noise, detector persistence) on similar timescales to granulation, which could inflate or suppress the measured flicker amplitude.
- Residual starspot modulation (rotation-timescale variability leaking into the flicker band) if the observation spans a significant fraction of the stellar rotation period.
- The 3D atmosphere grids may not perfectly represent the surface of real M dwarfs (magnetic effects, metallicity extremes), leading to biased stellar parameter retrievals from the flicker.
- Mitigation: the wavelength dependence of granulation flicker is distinct from instrumental systematics (which are typically grey or have detector-specific spectral signatures), and cross-validation with Kepler/TESS flicker measurements for overlapping targets can calibrate the 3D grid predictions.

### Why It Could Matter

Stellar contamination is arguably the single largest barrier to interpreting transmission spectra of potentially habitable planets around M dwarfs — the prime targets for JWST and future missions like the Habitable Worlds Observatory. If granulation flicker can be harnessed as a self-calibrating diagnostic, it would improve every JWST transmission spectrum retroactively (since the flicker information is already in the data) and provide a physically motivated framework for contamination correction that scales to future, even more precise observatories. It transforms a nuisance signal (stellar noise) into an asset.

---

## Summary Table

| # | Project | Key Data | Core Observable | Novelty Angle |
|---|---------|----------|----------------|---------------|
| 1 | Eclipse-depth variability as surface geology | JWST/MIRI multi-visit eclipses | Visit-to-visit scatter in 15 µm depth | Treating scatter as signal, not noise; linking to libration + mineralogy |
| 2 | Decade-baseline TTVs for Saturn analogs | Kepler + TESS transit times (12+ yr) | Low-frequency O–C curvature | First uniform survey for non-resonant cold giants via TTVs |
| 3 | Granulation flicker as contamination calibrator | JWST out-of-transit baselines + 3D stellar models | Flicker amplitude vs. wavelength | Using in-observation stellar noise to self-correct the stellar contamination |

---

*All datasets referenced are publicly available via MAST, the NASA Exoplanet Archive, and the respective mission data portals. No proprietary data is required for any of these projects.*
