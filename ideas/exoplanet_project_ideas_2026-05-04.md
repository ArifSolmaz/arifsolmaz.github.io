# Three Ambitious Exoplanet Research Project Ideas

*Generated May 4, 2026 — Scheduled task output*

---

## Project 1: Poor Person's Doppler Imaging — Reconstructing Stellar Surface Activity Maps from Starspot-Transit Crossings Across the Kepler–TESS Baseline

### Scientific Premise

When a transiting exoplanet crosses a starspot, it produces a brief brightening "bump" in the transit light curve. Each bump encodes the spot's position along the transit chord, its contrast (temperature), and its approximate size. A single crossing is a curiosity; dozens of crossings of the *same star* over months or years become a tomographic probe of the stellar surface. With Kepler's 4-year baseline and TESS's ongoing multi-sector coverage, some active planet-hosting stars now have **10+ years of transit-resolved spot-crossing data**. This project would systematically invert those crossings into time-resolved latitude–longitude activity maps — effectively a photometry-only analog of Doppler imaging, but for planet-hosting stars that are often too faint for spectropolarimetric mapping.

A recent homogeneous survey (A&A, 2025) cataloged ~102 spot-crossing candidates across 6 planets from 3,273 Kepler/TESS transits, estimating detection frequencies of ~4% (TESS) to ~37% (Kepler) for K-dwarf hosts. This catalog exists, but no one has yet used it (or an expanded version) to do *longitudinal surface reconstruction* across the full Kepler+TESS time baseline.

### Target Datasets

- **Kepler short-cadence light curves** for active planet hosts (e.g., Kepler-17, Kepler-71, HAT-P-11, Kepler-411).
- **TESS 2-minute and 20-second cadence data** for the same targets in overlapping sectors.
- **Ground-based multicolor transit photometry** (MuSCAT2/3 archives) to constrain spot temperatures via chromaticity of the bump amplitude.
- The spot-crossing catalog from the 2025 A&A homogeneous survey as a starting point.

### Novelty

Starspot-crossing events have been studied individually or in small batches to measure stellar differential rotation rates. But a *systematic inversion across the full decade-long Kepler+TESS baseline* to produce time-evolving surface maps has not been done. This bridges a gap between (a) the Doppler imaging community, which maps stellar surfaces spectroscopically but rarely for planet hosts, and (b) the exoplanet community, which catalogs spot crossings but rarely synthesizes them into stellar physics. The key insight is that the planet acts as a scanning probe whose chord is fixed by orbital geometry — successive transits at slightly different spot longitudes (due to stellar rotation) raster-scan a latitude band.

### Concrete Workflow

1. **Expand the spot-crossing catalog.** Re-analyze all Kepler short-cadence and TESS high-cadence transits for the ~15 most active planet hosts using a Gaussian-process detrending + spot-bump fitting pipeline (e.g., building on `spotrod` or `starsim`).
2. **Map each crossing to stellar coordinates.** Use the known orbital geometry (impact parameter, planet-to-star radius ratio, orbital period) and the crossing time within the transit to assign each spot a position on the stellar disk. Stellar rotation period and inclination (from out-of-transit modulation and v sin i) provide the longitude axis.
3. **Time-evolve the map.** Bin crossings into rolling windows (e.g., 1 stellar rotation period wide) and build maximum-entropy or Bayesian surface brightness maps at each epoch.
4. **Extract differential rotation and activity cycle signatures.** Fit a solar-like differential rotation law (Ω(lat) = Ω_eq − ΔΩ sin²θ) to the spot latitude drift. Look for long-term modulations in spot filling factor that could indicate magnetic cycles analogous to the Sun's 11-year cycle.
5. **Cross-validate** against out-of-transit rotational modulation amplitudes and published v sin i / Rossiter-McLaughlin measurements.

### Expected Signal / Observable

- Differential rotation ΔΩ/Ω_eq measurable to ~5–10% for stars with ≥20 spot crossings, competitive with spectroscopic methods.
- Secular trends in mean spot latitude ("butterfly diagram" analogs) over the 10-year baseline for the best-sampled systems.
- Spot temperature contrasts (from multicolor bump amplitudes) that constrain the magnetic field strength–temperature relation on other stars.

### Possible False Positives / Pitfalls

- **Faculae mimicking spots.** Facular crossings produce dips rather than bumps and could be confused with instrumental systematics. Multicolor photometry helps distinguish them (faculae have lower contrast in red bands).
- **Spot evolution between transits.** Spots grow, shrink, and migrate. If the spot lifetime is shorter than the transit interval, successive crossings do not probe the same spot, degrading the map. Mitigation: focus on stars with short orbital periods (< 3 days) and long spot lifetimes.
- **Degeneracy between spot size and contrast.** A small, dark spot and a large, warm spot can produce similar bumps in a single band. Multicolor data partially breaks this degeneracy.
- **Transit chord bias.** The planet only scans a narrow latitude band (set by the impact parameter). Surface features at other latitudes are invisible. This is a fundamental limitation but can be acknowledged and modeled.

### Why This Could Matter

Stellar activity is the dominant noise source contaminating exoplanet atmosphere characterization (the "transit light source effect"). Understanding where spots are, how they evolve, and how they differ from solar spots is critical for interpreting JWST transmission spectra. This project would deliver the first photometry-derived, time-resolved stellar surface maps for active planet hosts — a direct input for correcting JWST spectra and for testing stellar dynamo models on stars other than the Sun.

---

## Project 2: Secular Transit Depth Drift as a Probe of Circumplanetary Rings, Obliquity Precession, and Atmospheric Mass Loss Over Decadal Baselines

### Scientific Premise

The apparent transit depth of an exoplanet should be constant if the planet is a static sphere. But several physical processes can cause the *measured* depth to change slowly over years or decades:

- **Circumplanetary ring precession.** A ringed planet's projected cross-section changes as the ring plane precesses relative to our line of sight, modulating the transit depth on timescales of years to decades. Theoretical estimates suggest ~10–13 systems in the Kepler/TESS archive could show detectable depth variations from this effect.
- **Planetary obliquity precession.** An oblate, tilted planet presents a varying projected area as its spin axis precesses.
- **Atmospheric escape / mass loss.** Young, close-in planets actively losing their atmospheres (e.g., sub-Neptunes in the "radius valley") could show a *shrinking* transit depth over decades as the opaque atmospheric envelope deflates.

A recent systematic search (arXiv 2505.05948, May 2025) examined 308 close-in TESS planets for ring signatures in individual transits and found no clear detections. However, the *decadal baseline* approach — comparing Kepler-era depths to TESS-era depths for the same planet — has not been exploited as a blind survey. The 8–12 year lever arm between Kepler (2009–2013) and TESS extended mission (2021–2026+) is now long enough to be sensitive to precession periods of ~50–200 years.

### Target Datasets

- **Kepler long-cadence and short-cadence light curves** for all confirmed transiting planets.
- **TESS light curves** (2-minute cadence, extended mission) for overlapping Kepler targets — roughly 500+ planets observed by both missions.
- **CHEOPS pointed observations** for high-priority targets with apparent depth changes.
- **Spitzer 4.5μm archival transits** (where available) to separate chromatic effects from geometric ones.

### Novelty

Individual ring searches (fitting asymmetric transit models to single light curves) have been tried and have come up empty for close-in planets, consistent with tidal stripping of rings at small orbital separations. But the *depth drift* approach is geometrically distinct: it does not require resolving the ring in a single transit. Instead, it detects the integrated change in projected area over time. This makes it sensitive to rings (or obliquity) even when the ring signal is below the noise floor in any single epoch. Additionally, using depth drift to flag atmospheric mass loss in real time is a genuinely novel observable — current mass-loss studies rely on spectroscopic proxies (Lyα, He 10830 Å) rather than photometric shrinkage.

### Concrete Workflow

1. **Homogeneous re-reduction.** Uniformly extract transit depths for all ~500 Kepler/TESS overlap planets using identical detrending and fitting pipelines (e.g., `juliet` or `exoplanet` with the same limb-darkening treatment and stellar parameters) to eliminate systematic depth offsets between missions.
2. **Bandpass correction.** The Kepler and TESS bandpasses differ (430–890 nm vs. 600–1000 nm). Compute expected chromatic depth differences using stellar models + planetary atmosphere models and subtract them, isolating the *achromatic* (geometric) depth change.
3. **Statistical screen.** Flag all planets whose Kepler-to-TESS depth change exceeds 3σ after corrections. Separate the sample into close-in (a < 0.1 AU, rings unlikely) and longer-period (a > 0.1 AU, rings plausible) subsamples.
4. **Physical modeling of flagged systems.** For each outlier, fit three competing models: (a) ringed planet with precessing ring plane, (b) oblate planet with precessing spin axis, (c) atmospheric radius evolution (mass loss or inflation). Use Bayesian model comparison.
5. **Population-level upper limits.** Even non-detections constrain the prevalence and geometry of exoplanetary ring systems, obliquity distributions, and atmospheric loss timescales.

### Expected Signal / Observable

- Ring precession: depth changes of ~100–500 ppm over a decade for Saturn-analog rings at moderate inclinations, detectable for ~10 favorable systems.
- Atmospheric shrinkage: depth decreases of ~50–200 ppm per decade for young sub-Neptunes undergoing photoevaporation (e.g., Kepler-36c-like planets around young stars).
- Null results still yield the first population-level upper limits on ring prevalence beyond the tidal disruption radius.

### Possible False Positives / Pitfalls

- **Stellar variability.** Evolving starspot coverage changes the apparent transit depth (the transit light source effect). This is chromatic and can be partially corrected using the bandpass difference, but it remains the dominant systematic.
- **Instrumental systematics.** Kepler and TESS have different pixel scales, PSFs, and contamination levels. Imperfect dilution corrections could create spurious depth changes. Mitigation: use high-resolution imaging (Gaia, speckle) to update dilution corrections.
- **Third-light contamination evolution.** A background eclipsing binary blended with the target could produce depth changes if its own eclipse depth varies. Cross-check with Gaia astrometry and centroid analysis.

### Why This Could Matter

The detection of a circumplanetary ring system would be a landmark discovery — no exoplanet ring has been confirmed despite decades of searching. Even upper limits would constrain theories of ring formation, tidal disruption, and satellite accretion. The atmospheric mass-loss channel connects to one of the hottest topics in exoplanet science (the radius valley and its origins), and a photometric detection of real-time atmospheric shrinkage would provide a direct, model-independent constraint on mass-loss rates.

---

## Project 3: A Blind Census of Asymmetric, Non-Periodic Single-Transit Events in the TESS Full-Frame Image Archive — Hunting Exocomets, Disintegrating Bodies, and Hill Sphere Transients

### Scientific Premise

The overwhelming majority of exoplanet transit searches are optimized for *periodic* signals — phase-folding is the foundational technique. This optimization is blind to an entire class of astrophysically rich phenomena that produce *single, non-repeating, asymmetric* dips in stellar brightness:

- **Exocometary transits.** Evaporating comets on eccentric orbits produce asymmetric dips (sharp ingress from the nucleus, extended egress from the dust tail) that occur once or a few times and never repeat on convenient timescales. The iconic case is β Pictoris, but systematic searches in Kepler found only a handful of candidates, and TESS's full-frame images (FFIs) — covering ~85% of the sky with 200-second cadence in the extended mission — are largely untapped for this.
- **Disintegrating planetesimals.** Objects like KIC 12557548b (the "disintegrating planet") show variable, asymmetric transits. Similar but non-periodic events could come from tidally disrupted asteroids or planetesimals on plunging orbits.
- **Hill sphere transients.** Material orbiting within a planet's Hill sphere (circumplanetary disks, ring arcs, irregular satellite swarms) can produce irregular, low-level dips that accompany or surround a planetary transit but are not captured by standard symmetric transit models.

A 2025 archival Kepler study (arXiv 2510.14687) searched for exocomet transits and found candidates, but the TESS FFI archive — now spanning 6+ years and containing light curves for ~20 million stars — has not been subjected to a comparable blind, asymmetry-focused survey.

### Target Datasets

- **TESS FFI light curves** from the MIT QLP (Quick-Look Pipeline) and SPOC pipelines, covering all observed sectors (currently ~70+ sectors). Prioritize bright stars (T < 12 mag) for signal-to-noise.
- **Kepler/K2 long-cadence light curves** for cross-referencing any TESS candidates that fall in the Kepler field.
- **Gaia DR3/DR4 stellar parameters** to classify host stars (age, spectral type, debris-disk indicators).
- **WISE/2MASS infrared excess catalogs** to identify stars with known debris disks (higher prior probability of cometary activity).

### Novelty

Transit searches are engineered around periodicity — BLS, TLS, and neural-network classifiers all assume or benefit from repeated events. This project inverts the paradigm: it specifically targets the *reject pile* of standard pipelines. The few exocomet searches that exist (Kepler-focused, or targeted at known debris-disk hosts like β Pic) have not attempted a blind, all-sky, asymmetry-first survey of the TESS FFI archive. The combination of (a) a morphological classifier tuned to asymmetric single dips, (b) applied to 20M+ TESS light curves, (c) cross-matched with debris-disk and young-star catalogs, is — to the best of current literature — unexplored at this scale.

### Concrete Workflow

1. **Build an asymmetric dip detector.** Train a 1D convolutional neural network (or use a wavelet-based matched filter) on synthetic exocomet transit shapes (sharp ingress + exponential egress tail, variable depth/duration) injected into real TESS FFI light curves. The key distinction from standard transit classifiers: the model is trained to *reject* symmetric box-shaped dips and *select* asymmetric ones.
2. **Run the detector on the full TESS FFI archive.** Process all QLP light curves (T < 12 mag, ~5M stars) sector by sector. Flag single-event candidates with asymmetry index > threshold and SNR > 5.
3. **Classify and vet candidates.** Cross-match with:
   - Known eclipsing binary catalogs (to reject grazing EB events).
   - Gaia astrometry (to reject background blends).
   - Debris-disk catalogs (IR excess from WISE) to prioritize cometary candidates.
   - Stellar youth indicators (Li 6708 Å, rotation period, cluster membership) to identify young systems where cometary/planetesimal activity is expected.
4. **Morphological taxonomy.** Cluster the vetted candidates by light-curve shape into subclasses: (a) classic comet tails (sharp-then-gradual), (b) variable-depth disintegrating bodies, (c) broad, shallow Hill-sphere transients, (d) unclassified.
5. **Follow-up prioritization.** Publish a ranked target list for spectroscopic follow-up (Ca II, Na I absorption during transit for gas-tail confirmation) and high-cadence photometric monitoring.

### Expected Signal / Observable

- Exocomet transits: dips of 0.01–0.5% lasting 0.5–2 days with ingress/egress asymmetry ratios > 2:1. Expected yield: ~10–50 high-confidence candidates across the full TESS archive, based on extrapolation from Kepler detection rates and TESS's broader sky coverage.
- Disintegrating bodies: variable-depth dips (0.1–1%) with dusty tails, potentially recurring quasi-periodically. Expected: ~1–5 new systems.
- Hill sphere transients: shallow (< 0.05%), broad (hours-long) features flanking known planetary transits. Expected: upper limits for most systems, possible detections around young giant planets.

### Possible False Positives / Pitfalls

- **Instrumental artifacts.** TESS scattered light, momentum dumps, and spacecraft pointing jitter produce single-event dips. Mitigation: require that the event not coincide with known systematic timestamps and that it appear in the target pixel file centroid as on-source.
- **Stellar flares (inverted).** Flare decays are asymmetric *brightenings*, but post-flare dips (from coronal rain or prominence transits) could mimic cometary shapes. Mitigation: check for simultaneous brightening; cross-match with flare catalogs.
- **Grazing eclipsing binaries.** A single observed eclipse of a long-period EB can look like a deep, slightly asymmetric single transit. Mitigation: Gaia RUWE and radial velocity constraints; require asymmetry index above EB-typical values.
- **Cosmic ray / hot pixel events.** These are generally sharp spikes rather than extended dips but could trigger false positives in noisy light curves. Mitigation: require multi-pixel consistency in the target pixel files.

### Why This Could Matter

Exocomets are the missing link between debris disks and planetary systems. Detecting them in transit constrains the volatile content, orbital architecture, and dynamical excitation of the outer regions of planetary systems — regions invisible to radial velocity and standard transit surveys. A TESS-based census would also provide the first population statistics on exocometary activity as a function of stellar age and spectral type, directly informing models of late-stage planetary system evolution and volatile delivery to inner rocky planets. The discovery of new disintegrating bodies would probe the end-states of planetary material in ways that connect to white dwarf pollution studies.

---

## Summary Table

| # | Project | Primary Data | Key Observable | Timescale to First Results |
|---|---------|-------------|---------------|---------------------------|
| 1 | Starspot Tomography via Transit Crossings | Kepler SC + TESS 20s | Spot maps, differential rotation, activity cycles | ~6–9 months |
| 2 | Secular Transit Depth Drift Survey | Kepler + TESS overlap (~500 planets) | Depth changes > 100 ppm over 8–12 years | ~9–12 months |
| 3 | Blind Asymmetric Single-Transit Census | TESS FFI archive (~5M+ stars) | Exocomet tails, disintegrating bodies, Hill sphere transients | ~12–18 months |

---

*Note: These ideas are identified as potentially underexplored based on current literature as of May 2025. Elements of each have precedent in the literature; the novelty lies in the specific combination of approach, scale, and cross-mission baseline described here.*
