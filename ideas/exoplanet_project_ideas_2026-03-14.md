# Three Ambitious Exoplanet Research Project Ideas

*Generated: March 14, 2026*

---

## Project 1: A Mantle Taxonomy for Ultra-Short-Period Rocky Worlds via Comparative JWST Emission Spectroscopy

### Scientific Premise

Ultra-short-period (USP) rocky planets — those with orbital periods under ~1 day — are natural laboratories for planetary interior science. Their extreme surface temperatures (1500–3000 K) drive vigorous outgassing from molten or partially molten mantles, producing mineral-vapor atmospheres whose composition directly reflects the underlying mantle geochemistry. JWST has now detected thermal emission and possible atmospheric signatures from several of these worlds (TOI-561 b, 55 Cancri e, K2-141 b, K2-22b), but each has been studied largely in isolation. No systematic comparative framework exists to classify USP rocky planets by their inferred mantle compositions — effectively building a "mantle taxonomy" analogous to stellar spectral classification.

The central hypothesis is that USP rocky planets fall into distinct geochemical families (e.g., silicate-dominated, iron-enriched, carbon-bearing, or alkali-rich mantles) that can be distinguished through their outgassed emission spectra, and that these families correlate with host-star composition and bulk planetary density in predictable ways.

### Target Datasets

- **JWST MIRI and NIRSpec emission observations** of USP rocky planets: TOI-561 b, 55 Cancri e, K2-141 b, K2-22b, GJ 367 b, and any newly observed targets through Cycle 3/4 programs
- **NASA Exoplanet Archive** bulk parameters (mass, radius, density, orbital period, equilibrium temperature)
- **Hypatia Catalog and GALAH DR3** for host-star elemental abundances (Fe/H, Mg/Si, C/O ratios)
- **Theoretical outgassing models** from the MAGMA code (Schaefer & Fegley) and VapoRock (Wolf et al.)

### Novelty

While individual lava-world atmospheric detections have been reported, no published work has attempted a population-level geochemical classification of USP rocky planet mantles from emission spectroscopy. Existing theoretical work (e.g., Ito et al. 2015, Zilinskas et al. 2022) predicts that different mantle compositions produce distinctive spectral signatures — SiO, SiO₂, MgO, FeO, Na, K features at 4–12 μm — but these predictions have not been systematically tested against the growing JWST dataset. The project's distinguishing contribution is the comparative, population-level approach: instead of asking "does this planet have an atmosphere?", it asks "what kind of mantle does this planet have, and does it fit into a broader pattern?"

### Concrete Workflow

1. **Compile the sample:** Assemble all USP rocky planets (P < 1 day, R < 2 R⊕) with existing or scheduled JWST emission photometry or spectroscopy. Cross-match with stellar abundance catalogs.
2. **Uniform data reduction:** Re-reduce all JWST emission data using a consistent pipeline (Eureka! or ExoTiC-JEDI) to eliminate systematics differences between published analyses.
3. **Forward-model grid:** Generate a grid of outgassed atmosphere emission spectra using VapoRock + MAGMA, spanning a range of oxygen fugacities (IW-4 to IW+4), bulk compositions (Earth-like, Mercury-like, enstatite-chondrite-like, carbonaceous), and surface temperatures.
4. **Bayesian retrieval:** Fit each planet's emission spectrum with an atmospheric retrieval framework (e.g., petitRADTRANS or CHIMERA adapted for mineral vapor atmospheres) to constrain mantle composition.
5. **Population analysis:** Test for correlations between inferred mantle type and (a) host-star Mg/Si and C/O ratios, (b) bulk planetary density, (c) irradiation level.
6. **Prediction for PLATO targets:** Use the taxonomy to predict which future USP planet discoveries are most promising for mantle characterization.

### Expected Signal/Observable

The key observables are secondary eclipse depths at MIRI wavelengths (5–12 μm), where SiO (~ 9 μm), Na/K (visible/near-IR emission), and MgO features appear. A silicate-rich mantle produces strong SiO emission; an iron-rich mantle suppresses SiO and enhances FeO; a carbon-rich mantle (if it exists around main-sequence stars) would show CO and possibly C₂. Differences of 20–100 ppm between mantle compositions are expected in favorable cases, detectable with 2–4 JWST eclipse observations per target.

### Possible False Positives

- **Clouds and hazes** in the mineral vapor atmosphere could mute spectral features, making diverse mantle compositions appear similar (a "flat spectrum" degeneracy).
- **Non-equilibrium chemistry** from extreme day-night circulation could shift outgassed species ratios away from thermochemical equilibrium predictions.
- **Stellar variability** from spots/faculae could introduce systematic offsets in secondary eclipse measurements, especially for active M-dwarf hosts.
- **Density-composition degeneracy:** Similar bulk densities can arise from different interior structures (e.g., large iron core + thin silicate mantle vs. smaller core + thicker mantle), complicating the density-mantle correlation.

### Why It Matters

This project would establish the first empirical classification of rocky planet interiors beyond the Solar System. If USP rocky mantles do cluster into geochemical families that track stellar composition, it would provide direct evidence for nebular-inheritance models of planet formation and constrain the diversity of rocky planet interiors — a question with implications for habitability, since mantle composition governs volcanic outgassing, which in turn controls atmospheric evolution on longer-period, potentially habitable worlds.

---

## Project 2: A Gaia-Informed Census of Single-Transit Habitable Zone Candidates in the Kepler/K2 Archive

### Scientific Premise

The Kepler mission's greatest unfulfilled promise lies in the detection of Earth-analog planets: rocky worlds on ~1-year orbits in the habitable zones of Sun-like stars. The 4-year Kepler baseline should have captured 3–4 transits of such planets, but most automated pipelines (BLS, TLS, even ExoMiner++) require at least 3 periodic transits for reliable detection. Planets showing only 1–2 transits — due to TTVs, grazing geometry, instrumental gaps, or genuinely long periods — are systematically lost. A recent reassessment found that of 47 proposed habitable-zone Earth-like candidates, only 29 survive modern vetting, and newer pipelines fail to independently recover many candidates at low SNR and long periods. Meanwhile, K2's 75-day campaigns are even more prone to yielding single-transit events for HZ planets.

The key insight is that Gaia DR3 now provides precise stellar radii, masses, and luminosities for nearly all Kepler/K2 targets, enabling much tighter constraints on planetary parameters from single-transit events than was possible when these data were first collected.

### Target Datasets

- **Kepler long-cadence light curves** (Q0–Q17) from MAST, including the DR25 pixel-level data
- **K2 light curves** from Campaigns 1–19 (EVEREST or K2SFF detrended)
- **Gaia DR3 stellar parameters** cross-matched to the Kepler Input Catalog and EPIC
- **TESS Sector overlaps** with the Kepler/K2 fields for additional transit epoch constraints
- **NASA Exoplanet Archive** dispositions and threshold crossing events

### Novelty

Prior single-transit searches in K2 (e.g., Osborn et al. 2016) were conducted before Gaia DR3 was available, meaning stellar parameters had large uncertainties that propagated into planetary radius estimates. Furthermore, no published work has systematically combined single-transit Kepler events with Gaia-informed priors and TESS overlap data to constrain orbital periods. The recent development of transformer-based transit detection that does not require phase folding opens a new avenue for identifying aperiodic signals. This project would be the first to apply these three advances jointly — Gaia priors, transformer detection, and TESS cross-matching — to build a complete census of long-period HZ candidates in the Kepler/K2 archive, explicitly targeting the population that PLATO is designed to confirm.

### Concrete Workflow

1. **Stellar parameter update:** Cross-match all Kepler and K2 targets with Gaia DR3 to obtain precise R★, M★, L★, and distances. Recompute habitable zone boundaries for each star using the Kopparapu et al. (2013) parameterization.
2. **Single-transit search:** Apply a modified BLS and the new transformer-based algorithm (Pérez-González et al. 2025) to all Kepler long-cadence and K2 light curves, optimized for single-event detection rather than periodic signals. Set a detection threshold based on injection-recovery tests.
3. **Vetting cascade:** For each candidate single-transit event, apply centroid analysis, odd/even depth tests (where applicable), ghost diagnostic tests, and the Kepler DR25 data validation suite to reject instrumental artifacts, eclipsing binaries, and background blends.
4. **Gaia-constrained parameter estimation:** Use a Bayesian transit-fitting framework (e.g., juliet or allesfitter) with Gaia stellar priors to derive posterior distributions on R_p, a/R★, impact parameter, and allowed period ranges from the single-transit duration.
5. **TESS cross-match:** For candidates in TESS-observed sectors, search for additional transit epochs that could constrain the period. Even a non-detection provides an upper limit on transit probability for certain period ranges.
6. **HZ candidate catalog:** Compile a ranked list of single-transit HZ candidates with period posteriors, planetary radii, and predicted transit times for PLATO and ground-based follow-up.

### Expected Signal/Observable

An Earth-sized planet transiting a Sun-like star at 1 AU produces a ~84 ppm transit lasting ~13 hours. In Kepler long-cadence data (30-min integration), this is detectable at SNR ~7–10 for quiet stars with Kp < 14. The expected yield from single-transit events is 5–20 new HZ candidates in Kepler and 2–10 in K2, based on occurrence rate extrapolations from known shorter-period planets and the geometric transit probability (~0.5% at 1 AU).

### Possible False Positives

- **Instrumental systematics:** Kepler's pointing jitter, especially after reaction wheel failures, produces single-event artifacts that can mimic shallow, long-duration transits. Rigorous injection-recovery testing is essential.
- **Stellar variability:** Starspot crossings during transit can distort the light curve shape, and granulation-driven red noise can create spurious dips on ~10-hour timescales.
- **Background eclipsing binaries:** Without a second epoch, confirming that the signal is on-target (not a blended background EB) relies on centroid analysis and Gaia-informed dilution modeling.
- **Grazing eclipsing binaries:** A grazing EB can produce a shallow, V-shaped dip resembling a planetary transit; the single-event nature makes it harder to distinguish from a planet with a high impact parameter.

### Why It Matters

Every confirmed exoplanet catalog is biased toward short-period planets because they transit more frequently. The most scientifically valuable planets — temperate, potentially habitable worlds on year-long orbits around Sun-like stars — are precisely those most likely to appear as single-transit events. This project would provide the first comprehensive target list for PLATO's primary science goal, potentially identifying the next generation of Earth-analog candidates years before PLATO launches. It also provides ground truth for occurrence rate estimates of η⊕, one of the most important numbers in exoplanet science.

---

## Project 3: Transfer-Learned Stellar Contamination Correction for M-Dwarf Transmission Spectroscopy

### Scientific Premise

JWST transmission spectroscopy of planets around M dwarfs — the most common targets for atmospheric characterization of small, potentially habitable worlds — is fundamentally limited by stellar contamination from unocculted spots and faculae. The TRAPPIST-1 system has become a worst-case exemplar: strong contamination features dominate the transmission spectra of planets b, c, and e, and current stellar models cannot fully explain the observed contamination patterns. A recent breakthrough used back-to-back transits of TRAPPIST-1 b and c (observed quasi-simultaneously) as mutual calibrators, since both planets have similar radii and impact parameters, making them ideal for isolating stellar contamination.

However, this multi-planet calibration technique is a luxury available only in compact multi-transiting systems. For the majority of M-dwarf planets (LHS 1140 b, TOI-700 d, GJ 1214 b), no sibling planet provides a convenient calibrator. The project proposes training a neural network on the rich, multi-planet, multi-epoch TRAPPIST-1 contamination dataset, then transfer-learning to other M-dwarf systems where contamination cannot be directly calibrated.

### Target Datasets

- **JWST NIRSpec and NIRISS transmission spectra** of all TRAPPIST-1 planets (b, c, d, e, f, g) across multiple epochs (JWST Cycles 1–3)
- **JWST transmission spectra** of other M-dwarf planets: LHS 1140 b, GJ 1214 b, TOI-700 d, LP 791-18 d, TOI-1452 b
- **Contemporaneous stellar monitoring:** TRAPPIST-1 out-of-transit photometry from JWST, Spitzer (archival), and ground-based telescopes for stellar variability characterization
- **Stellar models:** PHOENIX, SPHINX, and STAGGER grid spectra for M-dwarf heterogeneity modeling
- **Published spot/faculae covering fractions** from TTV, photometric variability, and spectral decomposition analyses

### Novelty

The back-to-back transit calibration for TRAPPIST-1 b/c has been demonstrated in one study (Radica et al. 2024), and neural networks for stellar contamination reduction have been proposed in early 2026 (arXiv:2602.10330). However, no published work has attempted to combine these approaches into a transfer-learning framework: using TRAPPIST-1 as a "training star" whose contamination is well-characterized through multi-planet differential spectroscopy, then applying the learned contamination patterns to other M-dwarf hosts. The project's distinct contribution is treating TRAPPIST-1's contamination not as a nuisance to be removed, but as a Rosetta Stone for understanding M-dwarf heterogeneity at spectroscopic resolution.

### Concrete Workflow

1. **Build the TRAPPIST-1 contamination atlas:** Collect all JWST transmission spectra of TRAPPIST-1 planets across all available epochs. For each epoch, compute the "contamination spectrum" by differencing spectra of planet pairs with known (negligible) atmospheres (b and c) from epochs with different stellar activity states.
2. **Parameterize the contamination:** Decompose each contamination spectrum into a basis set of stellar heterogeneity components (spot temperature, faculae temperature, covering fractions) using a combination of PHOENIX model grids and data-driven decomposition (PCA/NMF).
3. **Train the neural network:** Train a variational autoencoder (VAE) or normalizing flow on the TRAPPIST-1 contamination spectra, conditioned on stellar activity indicators (out-of-transit flux level, photometric variability amplitude, spectral slope). The network learns the mapping: (stellar activity indicators, wavelength) → contamination spectrum shape.
4. **Transfer to other systems:** For each non-TRAPPIST-1 M-dwarf target, use the target's stellar activity indicators (from out-of-transit JWST data and ground-based monitoring) as input to the trained network. The network predicts the expected contamination spectrum, which is then subtracted from the observed transmission spectrum before atmospheric retrieval.
5. **Validation:** Test the framework on TRAPPIST-1 e and f — planets with possible atmospheres — by comparing retrieval results with and without the neural contamination correction. Also apply leave-one-out cross-validation within the TRAPPIST-1 system.
6. **Application to high-priority targets:** Apply the correction to GJ 1214 b (where high-altitude clouds/hazes and stellar contamination are entangled), LHS 1140 b (a promising HZ super-Earth), and TOI-700 d.

### Expected Signal/Observable

Stellar contamination in TRAPPIST-1 transmission spectra produces wavelength-dependent offsets of 50–200 ppm that vary between epochs. The neural network should capture the dominant modes of this variation (expected to be described by 3–5 latent dimensions based on the dimensionality of spot/faculae parameter space). For transfer targets, the correction is expected to reduce systematic residuals by a factor of 2–5, potentially revealing atmospheric features (H₂O, CO₂, CH₄ at 10–50 ppm) that are currently buried under contamination noise.

### Possible False Positives

- **Overfitting to TRAPPIST-1:** The contamination patterns of TRAPPIST-1 (spectral type M8V, very active) may not transfer well to earlier M dwarfs (M2–M5V) with different spot/faculae properties. The transfer learning could introduce systematic biases rather than removing them.
- **Activity indicator degeneracies:** Photometric variability amplitude is a crude proxy for the spatial distribution of heterogeneities on the stellar disk, and the same variability amplitude can arise from very different spot configurations.
- **Confounding atmospheric signals:** If TRAPPIST-1 b and c do have thin atmospheres (which cannot be fully excluded), the "pure contamination" training set would be slightly contaminated by atmospheric features, propagating errors to other systems.
- **Temporal non-stationarity:** M-dwarf activity evolves on timescales of months to years; contamination patterns learned at one epoch may not apply at another, requiring ongoing recalibration.

### Why It Matters

M dwarfs host the most observationally accessible potentially habitable planets, but stellar contamination is the single largest obstacle to characterizing their atmospheres with JWST. If this transfer-learning approach works, it would transform every M-dwarf atmospheric observation by providing a principled, data-driven contamination correction — turning TRAPPIST-1 from a cautionary tale into a calibration standard. The approach also has direct implications for the interpretation of biosignature claims: dimethyl sulfide and other potential biosignatures on K2-18b-like planets cannot be confidently identified until stellar contamination is controlled at the ~10 ppm level, which current methods cannot achieve.

---

*These ideas draw on the rapidly evolving 2025–2026 landscape of JWST atmospheric characterization, archival Kepler/K2 data mining, and stellar contamination mitigation. Each project leverages publicly available data and addresses a gap identified in the NASA ExEP Science Gap List or recent literature.*
