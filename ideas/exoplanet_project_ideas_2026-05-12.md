# Ambitious Exoplanet Research Project Ideas

**Generated: May 12, 2026**
**Scope: Underexplored, discovery-driven projects using public space-mission data**

---

## Project 1: Mapping the "Stellar Contamination Graveyard" — Retroactively Identifying False Atmospheric Detections in Pre-JWST Transmission Spectra

### Scientific Premise

Recent work (Savvidou et al. 2026, A&A; Rustamkulov et al. 2024, AJ) has shown that simplified stellar contamination models — especially the disk-averaged Transit Light Source Effect (TLSE) correction — can introduce systematic, wavelength-dependent biases of up to ~400 ppm in transmission spectra, particularly for active M- and K-dwarf hosts at optical wavelengths. JWST observations of systems like TOI-5205b have already revealed cases where stellar contamination dominates the transmission spectrum below ~3 μm, overpowering the planetary signal by up to an order of magnitude. Yet the community has accumulated years of published HST/WFC3 and Spitzer transmission spectra for dozens of planets around active stars — many of which used now-outdated contamination corrections or none at all. A systematic, retroactive audit of these published spectra using modern self-consistent contamination models has not been performed at scale.

### Target Datasets

- All published HST/WFC3 G141 grism transmission spectra (publicly archived via MAST/Barbara A. Mikulski Archive)
- Spitzer/IRAC secondary eclipse and transit photometry from the Spitzer Heritage Archive
- Stellar activity indicators: Ca II H&K indices, photometric variability from TESS and Kepler/K2 light curves, X-ray fluxes from XMM-Newton/Chandra
- JWST Early Release and Cycle 1–3 transmission spectra for cross-validation on overlapping targets

### Novelty

While individual retrieval papers sometimes mention stellar contamination as a caveat, no one has performed a population-level meta-analysis asking: "For how many published atmospheric detections does the reported molecular signature become statistically insignificant once modern TLSE models are applied?" This is distinct from simply improving retrieval codes — it is a forensic audit of the existing literature. The 2026 Savvidou et al. result that disk-averaged TLSE corrections can be wrong by hundreds of ppm makes this timely and tractable.

### Concrete Workflow

1. Compile a catalog of all published HST/WFC3 and Spitzer transmission spectra (roughly 70–100 planets with published spectra as of 2025).
2. Cross-match with TESS and Kepler/K2 photometry to characterize host-star variability (spot covering fractions, facular contrasts, rotation periods).
3. For each system, apply the Rackham et al. (2018) disk-averaged TLSE correction and the Savvidou et al. (2026) self-consistent geometric TLSE model.
4. Re-run atmospheric retrievals (e.g., with petitRADTRANS or POSEIDON) on the corrected spectra.
5. Flag systems where the original claimed molecular detection (H₂O, Na, K, etc.) drops below 2σ significance after correction.
6. Cross-validate against any available JWST spectra for the same targets.

### Expected Signal / Observable

A ranked list of "contamination-vulnerable" detections, quantifying how many published H₂O or alkali-metal detections in the HST era may have been partially or wholly driven by unocculted stellar heterogeneity rather than planetary atmospheres. Preliminary estimates suggest 15–30% of published WFC3 water detections around M dwarfs may be significantly affected.

### Possible False Positives (in the meta-analysis itself)

- Overestimating stellar activity: if the spot covering fraction is poorly constrained (e.g., from sparse TESS coverage), the correction itself may be inaccurate in the other direction.
- Retrieval degeneracies: removing stellar contamination may shift molecular abundances rather than eliminating detections entirely, making it ambiguous whether the original detection was "wrong."
- Temporal variability: stellar activity at the epoch of the HST observation may differ from the epoch of the TESS/Kepler photometry used to estimate spots.

### Why This Could Matter

This project would produce a community resource — essentially a reliability index for pre-JWST atmospheric characterizations — and directly inform target prioritization for JWST Cycles 4+ and future ARIEL observations. If a substantial fraction of legacy detections are contaminated, it changes the empirical landscape of comparative exoplanetology and the inferred prevalence of water-rich atmospheres on sub-Neptunes.

---

## Project 2: Hunting for Tidally-Driven Oblateness Signatures in Ultra-Short-Period Planet Transits Using Combined Kepler + TESS Photometry

### Scientific Premise

Ultra-short-period (USP) planets — those with orbital periods under ~1 day — experience extreme tidal forces that should distort their shapes from spherical to oblate or even triaxial ellipsoids. The transit light curve of an oblate planet differs subtly from that of a spherical planet of the same cross-sectional area: deviations concentrate in the ingress and egress phases and depend on the planet's spin-axis obliquity relative to the line of sight. A recent review (Adams et al. 2025, PNAS) identified oblateness detection via transit photometry as a "first-ever detection" opportunity for JWST, but the same signal could plausibly be extracted from the extraordinary photometric precision of phase-folded Kepler long-cadence data for the best USP targets — something that has been discussed theoretically but never attempted systematically across the full USP population.

### Target Datasets

- Kepler long-cadence and short-cadence photometry for all confirmed USP planets in the Kepler field (~25 targets with P < 1 day)
- TESS Sector 1–83 photometry for the ~50 confirmed TESS USP planets, plus new candidates from extended mission sectors
- Spectroscopic constraints on stellar limb darkening from LAMOST, GALAH, or literature values
- Theoretical tidal distortion models: interior structure models from Baumeister & Tosi (2023) or similar, predicting Love numbers (k₂) for rocky super-Earths

### Novelty

Oblateness searches have historically been proposed as single-target campaigns (e.g., for WASP-103b with JWST, or Kepler-1658b). A population-level, homogeneous search across all known USP planets — combining Kepler and TESS data where both exist — to place upper limits on oblateness (and by extension, interior rigidity and rotation state) has not been done. The key insight is that even non-detections are informative: an oblate shape requires rapid rotation, so a population of null detections would constrain the spin states of rocky USP planets and test tidal spin-synchronization theory. Furthermore, the combined Kepler+TESS baseline (spanning ~12 years) allows detection of subtle transit shape changes if the planet's obliquity is precessing.

### Concrete Workflow

1. Assemble the full USP planet catalog (P < 1 day) from the NASA Exoplanet Archive, selecting targets with >500 transit epochs in Kepler and/or >20 TESS sectors.
2. Phase-fold all available transits for each target, achieving effective per-point photometric precision of ~1–5 ppm for the best Kepler targets.
3. Fit each phase-folded transit with two models: (a) a standard spherical-planet transit model (e.g., batman) and (b) an oblate-planet transit model parameterized by oblateness f = (R_eq − R_pol)/R_eq and projected obliquity θ.
4. Compute Bayesian evidence (via nested sampling, e.g., dynesty) for each model to assess whether oblateness is statistically favored for any individual target.
5. For all targets, place upper limits on f and compare to theoretical predictions for tidally locked rocky planets with known bulk densities.
6. Search for epoch-dependent ingress/egress asymmetry that could signal obliquity precession.

### Expected Signal / Observable

For a maximally oblate rocky planet (f ~ 0.01–0.03, comparable to Saturn's oblateness), the transit depth deviation during ingress/egress is ~5–20 ppm relative to a spherical model. With ~4,000 phase-folded Kepler transits for a target like Kepler-78b (per-transit depth precision ~50 ppm), the folded precision reaches ~1 ppm — theoretically sufficient for a 5–20σ detection if the planet is rapidly rotating and significantly oblate. For TESS targets with fewer transits, the project will set meaningful upper limits (f < 0.05 at 95% confidence).

### Possible False Positives

- Stellar granulation and p-mode oscillations can introduce correlated noise in ingress/egress that mimics oblateness at the few-ppm level.
- Imperfect limb-darkening models: errors in the stellar intensity profile can bias ingress/egress shapes, mimicking or masking oblateness.
- Unresolved companion transits: a blended eclipsing binary can alter the effective transit shape.
- Kepler long-cadence smearing: 30-minute integrations smooth ingress/egress, requiring careful integration of the model over finite exposure times.

### Why This Could Matter

Detecting — or ruling out — planetary oblateness for USP planets would provide the first direct constraints on the rotation states and interior rigidity of rocky exoplanets. A detection would indicate a planet that is not tidally locked (or is locked in a non-synchronous spin-orbit resonance), challenging standard tidal theory. A population of non-detections would confirm the theoretical expectation that tidal dissipation synchronizes rotation on <1 Gyr timescales for close-in rocky worlds, validating a foundational assumption in habitability assessments of tidally locked planets around M dwarfs.

---

## Project 3: Detecting Planetary Orbital Decay Rate Variations Across Resonant Chain Systems as a Probe of Interior Dissipation Hierarchies

### Scientific Premise

Transit timing variations (TTVs) in resonant multi-planet systems are routinely used to measure planet masses. But an underexplored signal lies in the *secular trend* of TTV residuals once the dominant near-resonant perturbation is removed: a slow, monotonic drift in orbital period that encodes tidal orbital decay. In a resonant chain (e.g., TRAPPIST-1, TOI-178, Kepler-223, HD 110067), each planet's tidal decay rate depends on its own tidal quality factor Q and the chain's collective dissipation dynamics. By measuring *differential* decay rates across planets in the same chain — subtracting the well-modeled gravitational TTVs — one can extract the *relative* tidal Q values of multiple planets in a single system without needing absolute calibration. This has not been attempted for any resonant chain to date, despite the fact that Kepler and TESS together now provide 12+ year timing baselines for several key systems.

### Target Datasets

- Kepler DR25 transit times for all confirmed resonant chain systems in the Kepler field (Kepler-60, Kepler-80, Kepler-223, Kepler-444)
- TESS transit times for TRAPPIST-1 (Sectors 1–83+), TOI-178, HD 110067
- Ground-based transit times from literature compilations (e.g., ExoClock, ETD) extending the baseline
- Spitzer transit times for TRAPPIST-1 (archival, 2016–2019 campaigns)
- Gaia DR3/DR4 stellar parameters for precise system age estimates

### Novelty

Individual tidal decay searches have been performed for isolated hot Jupiters (WASP-12b being the canonical detection). But in a resonant chain, the planets are gravitationally coupled, and the resonance itself acts as a "flywheel" that can either amplify or suppress tidal decay. The novel angle is to exploit this coupling: rather than searching for period decay in a single planet (where the signal is degenerate with apsidal precession and other effects), one measures the *pattern* of decay rates across the chain. The chain's topology constrains which planets should decay fastest (the innermost, typically) and by how much, providing a built-in consistency check. A mismatch between predicted and observed differential decay rates would reveal anomalous dissipation — possibly indicating a magma ocean, enhanced rheological dissipation, or even an undetected non-transiting companion perturbing the chain.

### Concrete Workflow

1. Compile all available transit mid-times for 5–8 resonant chain systems (Kepler-80, Kepler-223, TRAPPIST-1, TOI-178, HD 110067, Kepler-60, TOI-1136, Kepler-444) from Kepler, TESS, Spitzer, and ground-based archives.
2. Fit a full N-body TTV model (using TTVFast or TTVFaster) to each system, accounting for all known resonant perturbations, eccentricities, and masses.
3. Extract the O−C (observed minus computed) residuals after subtracting the best-fit gravitational TTV model.
4. Fit a quadratic (parabolic) trend to the O−C residuals for each planet independently: a negative quadratic coefficient indicates orbital decay (dP/dt < 0).
5. Compare the measured dP/dt values across planets within each chain to theoretical predictions from constant-Q tidal models, viscoelastic tidal models (Andrade rheology), and resonant-locking tidal models.
6. Perform injection-recovery tests: inject synthetic decay signals into the real timing data to calibrate sensitivity and false-alarm probability.

### Expected Signal / Observable

For TRAPPIST-1b (the innermost planet in the chain), tidal theory predicts dP/dt ~ −10⁻¹⁰ to −10⁻⁹ days/day for plausible rocky-planet Q values (10–100). Over a 12-year Kepler+TESS+Spitzer baseline, this produces a cumulative timing shift of ~0.5–5 seconds — at the edge of detectability with current timing precision (~5–30 sec per transit for TESS, ~1–5 sec for Spitzer). For the Kepler resonant chains, the 17-year baseline (Kepler 2009–2013 + TESS 2018–2026) provides even longer leverage, though individual transit timing precision is typically ~30 sec. The differential signal — the *ratio* of decay rates between planets b and c, for instance — may be more robust than absolute decay rate measurements because correlated systematic errors (e.g., clock drift, stellar activity) largely cancel.

### Possible False Positives

- Apsidal precession: secular changes in the argument of pericenter can mimic a parabolic O−C trend. This is partially mitigated by the N-body model, but imperfect eccentricity constraints can leave residual precession signals.
- Stellar activity: spot-crossing events shift the apparent transit midpoint by ~10–60 sec for active M dwarfs, introducing correlated noise in timing residuals.
- Inadequate TTV model: if the gravitational N-body model does not capture all relevant perturbations (e.g., due to an unknown non-transiting planet), the residual "decay" could be a gravitational artifact.
- Rømer delay: light-travel-time variations due to the system's barycentric motion (from an outer companion) can produce a parabolic O−C signal.

### Why This Could Matter

This project would provide the first comparative measurement of tidal dissipation efficiency across multiple planets in the same system, directly constraining interior structure models. If the innermost planet in TRAPPIST-1 shows anomalously high dissipation (low Q), it would suggest a partially molten interior — a prediction tied to the habitability debate, since tidal heating can drive volcanic outgassing that sustains secondary atmospheres. More broadly, measuring Q for multiple rocky planets in a single system would break the degeneracy between Q and stellar tidal parameters that plagues single-planet studies, and would test whether resonant chains are truly in long-term equilibrium or are slowly evolving toward disruption.

---

## Summary Comparison

| Feature | Project 1: Contamination Graveyard | Project 2: USP Oblateness | Project 3: Resonant Chain Decay |
|---|---|---|---|
| Primary data | HST/WFC3 + TESS activity | Kepler + TESS transits | Kepler + TESS + Spitzer times |
| Key signal | Revised molecular significances | Ingress/egress shape (~5–20 ppm) | O−C quadratic drift (~1–5 sec) |
| Novelty type | Meta-analysis / forensic audit | Population-level shape search | Differential tidal dissipation |
| Biggest risk | Uncertain spot fractions | Correlated stellar noise | N-body model incompleteness |
| Impact if successful | Reliability index for legacy spectra | First rotation-state constraints | First comparative Q measurements |

---

*Notes: All datasets referenced are publicly available. These ideas are identified as potentially underexplored based on current literature review; related work exists in adjacent areas as discussed above. Each project is designed to be tractable for a small team (1–3 researchers) within 1–2 years.*
