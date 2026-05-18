# Exoplanet Research Strategy Brief — April 2026

Three underexplored, discovery-driven project proposals grounded in publicly available mission data.

---

## Project 1: Lava World Atmosphere Demographics — Mining the Ultra-Short-Period Population for Magma-Ocean Volatile Fingerprints

### Scientific Premise

JWST recently detected a thick atmosphere on TOI-561b, a small, scorching-hot rocky planet orbiting one of the oldest stars in the Milky Way — a planet that, under prevailing models, should have been stripped bare long ago. This discovery, alongside the confirmed atmosphere on 55 Cancri e, suggests that magma-ocean outgassing can sustain secondary atmospheres even under extreme irradiation. Yet no systematic demographic study has asked: across the full population of known ultra-short-period (USP) planets, which ones should harbor magma-ocean atmospheres, and what does the presence or absence of such atmospheres tell us about interior composition and mantle volatile budgets?

The idea is to build a predictive framework — grounded in bulk density, irradiation environment, and host-star age/activity — and test it against JWST secondary eclipse and phase curve observations as they accumulate. The key scientific leverage is that magma-ocean atmospheres are not primordial. Their composition (SiO, Na, K, SiO₂, FeO vapors) is set by the rock vapor equilibrium of the mantle, making them direct probes of interior mineralogy in a way that no other technique currently achieves.

### Target Datasets

- **NASA Exoplanet Archive** for the full USP planet catalog (P < 1 day): masses, radii, densities, host-star properties.
- **JWST Cycle 1–4 archival spectra** (NIRSpec, MIRI) for secondary eclipses and thermal emission of USP rocky planets (55 Cnc e, TOI-561b, GJ 367b, K2-141b, LHS 3844b, and others observed as part of GO programs).
- **TESS phase curves** of USP planets — even non-detections constrain dayside brightness temperatures and therefore surface/atmospheric thermal budgets.
- **Spitzer 4.5 μm archival eclipses** for supplementary thermal constraints.

### Novelty

Individual lava-world atmosphere detections are being published one at a time. What is missing is a population-level analysis that asks: given interior structure models and magma-ocean thermochemistry, can we predict which USP planets should retain rock-vapor atmospheres and which should not? The detection of an atmosphere on TOI-561b (an ancient, metal-poor star) immediately challenges the expectation that old, heavily irradiated planets lose atmospheres. A systematic census would turn individual surprises into a testable demographic trend linking mantle composition, stellar environment, and atmospheric retention.

### Concrete Workflow

1. Compile the complete USP planet sample (~40–50 planets with measured masses and radii) from the NASA Exoplanet Archive.
2. For each planet, compute the expected magma-ocean vapor pressure and atmospheric scale height using published rock-vapor-equilibrium codes (e.g., MAGMA, VapoRock), parameterized by plausible mantle compositions (Earth-like BSE, Mg-rich, Fe-rich).
3. Model atmospheric escape rates under each planet's XUV environment using host-star activity proxies (rotation period, X-ray luminosity from eROSITA or archival XMM/Chandra).
4. Predict a binary outcome (atmosphere-retaining vs. stripped) for each target and rank by observational accessibility (emission signal-to-noise in MIRI/NIRSpec).
5. Cross-match predictions against existing JWST and Spitzer secondary eclipse detections and non-detections.
6. Perform a Bayesian hierarchical analysis: what mantle composition distribution across the USP population best explains the observed detection/non-detection pattern?

### Expected Signal / Observable

Secondary eclipse depths of 50–200 ppm in MIRI bands for planets with rock-vapor atmospheres (SiO, Na features), versus bare-rock blackbody emission for stripped surfaces. The key discriminant is the ratio of optical (TESS) to infrared (MIRI 15 μm) eclipse depths: a planet with a greenhouse atmosphere will show a steeper spectral slope than a bare rock.

### Possible False Positives

- Residual stellar variability mimicking shallow eclipse depth variations.
- Instrumental systematics in MIRI at the ~50 ppm level for faint targets.
- Degeneracy between thin rock-vapor atmospheres and high-albedo bare surfaces (both reduce dayside brightness temperature relative to a zero-albedo blackbody).
- Uncertainty in XUV flux histories, which propagates into escape-rate predictions.

### Why This Matters

This would be the first population-level test of magma-ocean atmospheric theory. It directly constrains mantle volatile inventories — a fundamental unknown in rocky planet geophysics — using only photometric data. If the detection pattern correlates with host-star metallicity or age, it opens a window into how rocky planet interiors evolve on Gyr timescales, which is central to understanding habitability.

---

## Project 2: Transit Timing Variation Archaeology for Hidden Tidal Heating — Identifying "Exo-Ios" in the Kepler Multi-Planet Archive

### Scientific Premise

Io is the most volcanically active body in the solar system because Jupiter and Europa force a non-zero eccentricity through orbital resonance, and tidal dissipation converts that forced eccentricity into internal heat. The same mechanism should operate in compact multi-planet systems, many of which were discovered by Kepler and are now being monitored by TESS. Transit timing variations (TTVs) encode the gravitational interactions between planets, including the forced eccentricities responsible for tidal heating. Yet almost no one has systematically mined the Kepler TTV catalog specifically to compute tidal heating budgets and identify which rocky planets are likely experiencing Io-like or even super-Io-level volcanism.

Recent work on LP 791-18 d demonstrated this approach for a single system — forced eccentricity from TTV modeling yielded a tidal heat flux potentially exceeding Io's. The question is whether this is a rare curiosity or the tip of a population. The Kepler multi-planet sample contains hundreds of compact systems where inner rocky planets could be tidally heated by outer companions.

### Target Datasets

- **Kepler DR25 long-cadence light curves** and the Holczer et al. (2016) TTV catalog (~2,600 KOIs with measured TTVs), supplemented by the more recent Hadden & Lithwick updated TTV fits.
- **TESS extended-mission light curves** for Kepler-field targets observed in TESS Sectors 40+, providing a new temporal baseline to refine TTV periods and amplitudes.
- **NASA Exoplanet Archive** confirmed/validated multi-planet systems for masses, radii, and orbital parameters.
- **Published radial velocity masses** (California-Kepler Survey, HARPS-N) to break the mass-eccentricity degeneracy in TTV inversions where available.

### Novelty

TTV analyses have traditionally focused on extracting planet masses and testing dynamical stability. The tidal-heating angle — using TTVs to compute forced eccentricities and then estimating internal heat fluxes — has only been applied to a handful of individual systems (LP 791-18, TRAPPIST-1). A systematic survey across the full Kepler multi-planet catalog, ranking hundreds of rocky planets by predicted tidal heat flux, would be genuinely new. It connects exoplanet dynamics to geophysics in a way that is rarely attempted at population scale.

Additionally, a 2025 reanalysis of Kepler data for KOI-134 revealed that previously missed planets produce TTVs that confused earlier analyses. This suggests that the existing TTV catalog may contain unrecognized signals from additional unseen companions whose gravitational influence drives tidal heating in known planets.

### Concrete Workflow

1. Select all Kepler multi-planet systems (N ≥ 2) where at least one planet has R < 2 R⊕ (likely rocky) and measured TTVs with signal-to-noise > 3.
2. For each system, perform N-body TTV inversions (using TTVFast or TTVFaster) to extract the posterior distributions of planet masses and free + forced eccentricities.
3. Where RV masses exist, use them as priors to tighten eccentricity constraints.
4. Compute tidal heat flux for each rocky planet using the standard tidal dissipation formula: Ė_tidal = (21/2) × (k₂/Q) × (n⁵R⁵e²)/G, parameterized by plausible tidal quality factors Q (10–1000) and Love numbers k₂.
5. Rank the population by predicted tidal heat flux. Identify the top 20 "exo-Io" candidates.
6. Cross-reference with JWST and TESS phase curve observations to see if any candidates show anomalous thermal emission or atmospheric signatures consistent with volcanism (SO₂, SiO outgassing).

### Expected Signal / Observable

The direct observable is the TTV signal itself, which constrains forced eccentricity. The derived quantity — tidal heat flux in W/m² — can then be compared to Io (~2 W/m²) and Earth (~0.09 W/m²). Planets with predicted heat fluxes exceeding 1 W/m² are strong exo-Io candidates. Secondary observables include anomalous thermal phase curve amplitudes (excess nightside flux from internal heating) and potential volcanic atmospheric signatures (SO₂ at 7.3 μm with JWST/MIRI).

### Possible False Positives

- TTVs caused by stellar activity or instrumental systematics rather than true gravitational perturbations (mitigated by restricting to systems with correlated TTVs in multiple planets).
- Eccentricity-inclination degeneracy in TTV inversions: some solutions trade eccentricity for mutual inclination, which does not drive tidal heating.
- Uncertainty in tidal Q: the dissipation factor for rocky exoplanets is unconstrained and could vary by orders of magnitude, making absolute heat flux predictions uncertain (though relative rankings within the population are more robust).
- Undetected additional planets whose gravitational influence is misattributed, inflating or deflating eccentricity estimates.

### Why This Matters

Tidal heating may be one of the most important drivers of geological activity — and potentially habitability — on rocky exoplanets, especially those orbiting M dwarfs where compact resonant chains are common. Identifying a population of tidally heated worlds would establish a new category of geophysically active planets, provide targets for JWST volcanic atmosphere searches, and test whether the Solar System's Io is an outlier or a common outcome of multi-planet dynamics.

---

## Project 3: Stellar Butterfly Diagrams from Multi-Epoch Transmission Spectra — Turning Stellar Contamination into Starspot Science

### Scientific Premise

Stellar surface heterogeneity — starspots and faculae — is one of the dominant systematic errors in exoplanet transmission spectroscopy, particularly for planets transiting K and M dwarfs. An enormous amount of effort is being invested in removing or correcting this contamination signal. But the contamination itself encodes information about the host star's surface: as a planet transits, it occults a specific chord of the stellar disk, and the difference between the in-transit and out-of-transit spectrum reveals the spatially resolved properties of that chord relative to the disk-integrated star.

The underexplored idea is to flip the problem: instead of treating stellar contamination as noise to subtract, use multi-epoch transit observations — where the starspot pattern evolves over months to years — to reconstruct the latitude-dependent spot coverage and its temporal migration. On the Sun, this produces the famous "butterfly diagram" showing how sunspot latitudes migrate toward the equator over the ~11-year solar cycle. No such diagram has ever been constructed for another star using transit-chord tomography, yet the data to attempt it may already exist in the JWST and HST archives for the most frequently observed exoplanet host stars.

A January 2026 study in Astronomy & Astrophysics showed that the simplified stellar contamination model can produce errors of 80–100 ppm in the optical for sub-Neptunes — comparable to the atmospheric features themselves. This means the stellar signal is strong and detectable, not buried in noise. The Pandora SmallSat mission, launched January 2026, is specifically designed to monitor stellar heterogeneity for 20 exoplanet host stars, providing an ideal complementary dataset.

### Target Datasets

- **HST/WFC3 and STIS transmission spectra archives** for repeatedly observed systems: HD 189733b (~20+ transits over 15 years), WASP-107b, GJ 1214b, GJ 436b, HAT-P-11b.
- **JWST NIRSpec/NIRISS/G395H multi-epoch transit spectra** from Cycles 1–4 (many GO programs observe multiple transits of the same target).
- **TESS continuous photometry** for the same host stars to track rotational modulation and starspot evolution between transit epochs.
- **Pandora SmallSat monitoring data** (beginning 2026) for simultaneous visible photometry and NIR spectroscopy of active host stars.
- **Ground-based photometric monitoring** (e.g., MEarth, SPECULOOS) providing long-baseline spot modulation histories.

### Novelty

Photometric butterfly diagrams have been constructed for a small number of stars — notably Kepler-63 via spot-crossing events in broadband Kepler photometry, and one Sun-like star via asteroseismology. However, these photometric approaches measure only spot position and approximate size. What has not been done is to use multi-epoch *spectroscopic* transit observations (transmission spectra from HST and JWST) to extract both the spatial distribution and the temperature/composition of spot regions as a function of time. Spectroscopic transit tomography adds a wavelength dimension that photometric spot mapping cannot access: the contamination spectrum's shape constrains the spot temperature, while its amplitude constrains the covering fraction, breaking the degeneracy that plagues broadband methods.

This project bridges two communities (exoplanet atmospheres and stellar physics) in a way that benefits both: exoplanet scientists get physically motivated, time-evolving contamination corrections grounded in the actual spot cycle phase, and stellar physicists get temperature-resolved activity cycle maps for M/K dwarfs — a regime where photometric spot-crossing methods are most limited by the faintness of individual crossing events.

### Concrete Workflow

1. Identify the 5–10 K/M dwarf exoplanet hosts with the largest number of archival transit spectral observations spanning ≥2 years (HD 189733, GJ 1214, WASP-107, HAT-P-11, GJ 436 are strong candidates).
2. For each epoch, fit the transmission spectrum jointly for the planetary atmosphere and the stellar contamination spectrum using a two-component (spot + photosphere) model, extracting the spot covering fraction and effective temperature of the occulted chord.
3. Combine the transit geometry (known impact parameter, transit chord latitude on the stellar disk) with the epoch-dependent spot fraction to assign a spot coverage to a specific stellar latitude band at each observation epoch.
4. Construct a time-latitude diagram of spot coverage — the stellar butterfly diagram — from the ensemble of transit epochs.
5. Compare to predictions from mean-field dynamo models for K/M dwarfs and to photometric activity cycle periods measured from long-baseline monitoring.
6. Quantify how the spot evolution propagates into time-variable biases on retrieved planetary atmospheric parameters (e.g., does the apparent H₂O abundance of HD 189733b correlate with the host star's activity cycle phase?).

### Expected Signal / Observable

Spot covering fractions of 1–30% for active K/M dwarfs, producing wavelength-dependent contamination signals of 50–500 ppm in the optical and 10–100 ppm in the NIR. The temporal evolution of these signals over years should reveal systematic latitude migration if the star has a solar-like activity cycle. For HD 189733 (known ~12-year photometric cycle), the transit archive spans long enough to potentially capture a full spot migration cycle.

### Possible False Positives

- Spot evolution on timescales shorter than the transit cadence (days–weeks) could produce scatter that mimics latitude migration rather than reflecting a coherent cycle.
- Degeneracy between spot temperature and covering fraction: a few hot spots and many cool spots can produce similar contamination spectra.
- Impact parameter uncertainties propagate into stellar latitude assignments, blurring the butterfly diagram.
- If the stellar inclination is low (star viewed pole-on), different latitudes project onto similar disk positions, reducing spatial discrimination.
- Faculae (bright regions) can partially cancel spot signals, complicating the two-component model.

### Why This Matters

Understanding stellar magnetic activity cycles is a fundamental problem in stellar astrophysics, with direct implications for planetary habitability (stellar flares, UV environment). Spectroscopic transit-chord tomography would provide temperature-resolved spot maps that go beyond what photometric crossing events or asteroseismology can achieve, particularly for the M and K dwarfs that host the most observationally accessible rocky planets. If successful, this project would produce the first spectrally informed butterfly diagrams for cool dwarfs, while simultaneously delivering physically motivated, epoch-specific stellar contamination corrections for JWST transmission spectra — directly improving the reliability of atmospheric retrievals for potentially habitable worlds.

---

## Summary Table

| # | Project | Primary Data | Key Output | Risk Level |
|---|---------|-------------|------------|------------|
| 1 | Lava World Atmosphere Demographics | JWST + TESS + Spitzer eclipses | Population-level test of magma-ocean atmosphere theory | Medium — requires sufficient JWST archival targets |
| 2 | TTV-Derived Tidal Heating Census | Kepler TTVs + TESS baselines | Ranked catalog of "exo-Io" candidates | Medium-Low — well-constrained dynamical method |
| 3 | Stellar Butterfly Diagrams via Transit Tomography | HST + JWST multi-epoch spectra + Pandora | First stellar activity cycle maps from transit data | High — novel technique, unclear signal strength |

---

*Report generated April 1, 2026. All datasets referenced are publicly available through MAST, the NASA Exoplanet Archive, and mission-specific data portals.*
