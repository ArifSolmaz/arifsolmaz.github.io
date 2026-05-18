# Ambitious Exoplanet Research Project Ideas

**Generated: April 2, 2026** | Automated report from scheduled task

---

## Project 1: Sulfur Geochemistry as a Planetary Classification Axis — Mining JWST Transmission Spectra for a "Sulfur Sequence"

### Scientific Premise

JWST has recently revealed sulfur-bearing species (H₂S, SO₂, and exotic sulfur compounds) in a growing but heterogeneous set of exoplanet atmospheres — from the ultra-hot Jupiters where SO₂ is photochemically produced, to the strange sulfur-dominated world L 98-59 d, to the carbon-and-sulfur chemistry of pulsar planets. Yet there is no systematic framework that treats sulfur abundance and speciation as a *classification axis* for planets the way metallicity or C/O ratio is used. The idea: construct a "sulfur sequence" — an empirical ordering of planets by their sulfur chemistry regime — and test whether it correlates with interior structure, formation pathway, or host-star properties in ways that C/O and metallicity alone do not capture.

### Target Datasets

- **JWST transmission and emission spectra** from Cycle 1–4 GO and GTO programs (publicly available via MAST). Key targets: WASP-39b (SO₂ detection), WASP-107b, WASP-18b (3D atmospheric map now available), L 98-59 d, HR 8799 bcde, and the growing list of sub-Neptune atmospheric detections.
- **NASA Exoplanet Archive** bulk parameters (mass, radius, equilibrium temperature, host-star metallicity, age).
- **Published photochemical model grids** (e.g., Tsai et al. 2023; Polman et al. 2024) as theoretical comparison points.

### Novelty

Most atmospheric retrieval papers treat sulfur detections on a target-by-target basis. A cross-sample, population-level study of sulfur chemistry regimes is largely absent from the literature. The closest work is the SO₂ photochemistry modeling for hot Jupiters, but nobody has attempted to unify the sulfur signatures across the mass–temperature–metallicity space into a single empirical framework and test it as an independent classification dimension.

### Concrete Workflow

1. Compile all publicly available JWST spectra with sulfur-species detections or meaningful upper limits (expect ~20–30 targets by mid-2026).
2. Run uniform atmospheric retrievals (e.g., using open-source codes like POSEIDON or petitRADTRANS) with a sulfur-inclusive chemical network to extract sulfur abundance ratios (S/O, S/H) and dominant sulfur species for each target.
3. Construct a sulfur-regime diagram: plot dominant sulfur species and total sulfur abundance against equilibrium temperature, surface gravity, and host-star [Fe/H].
4. Test for clustering: do planets separate into distinct sulfur-chemistry regimes (e.g., "SO₂-dominated," "H₂S-dominated," "sulfur-depleted")? Use unsupervised clustering methods (e.g., Gaussian mixture models).
5. Compare the sulfur sequence to predictions from photochemical models to determine whether the observed regimes can be explained purely by irradiation chemistry or whether interior outgassing (i.e., formation-pathway-dependent bulk sulfur content) is required.

### Expected Signal / Observable

A statistically meaningful separation of planets into 2–4 sulfur chemistry regimes on the temperature–gravity plane, with residual scatter that correlates with host-star metallicity or planetary bulk density — implying formation-pathway information encoded in sulfur.

### Possible False Positives / Pitfalls

- Small sample size may not yet support robust clustering; this improves as more JWST cycles release data.
- Retrieval degeneracies between sulfur species and other absorbers (especially in the 3–5 µm window where H₂O, CO₂, and SO₂ features overlap).
- Non-equilibrium photochemistry can dominate over bulk composition signals, making it hard to disentangle irradiation effects from formation signatures.

### Why It Matters

If sulfur chemistry encodes formation-pathway information independently of C/O and metallicity, it provides a new empirical tool for linking atmospheric composition to planet formation — directly relevant to the field's central goal of connecting observed exoplanet diversity to formation theory.

---

## Project 2: Transit Timing Variation Archaeology in Kepler's Long-Baseline Data — Hunting Unseen Companions via Decade-Long TTV Drift

### Scientific Premise

Kepler observed many multi-planet systems for ~4 years (2009–2013). TESS has since re-observed many of these systems, creating a baseline of 13–17 years. Over such long baselines, even very small transit timing variations (TTVs) caused by distant, non-transiting perturbers — planets in the 1–10 AU range that are invisible to both transit surveys and current radial velocity precision for faint Kepler stars — could accumulate into measurable timing drifts. This is a regime that is almost entirely unexplored: most TTV studies focus on near-resonant pairs with short-period oscillations, not on slow secular drifts caused by distant companions. This project proposes a systematic search for *monotonic or long-period TTV trends* in Kepler systems using the Kepler+TESS combined baseline.

### Target Datasets

- **Kepler DR25 light curves** and the associated transit timing catalogs (Holczer et al. 2016; Rowe et al. 2015).
- **TESS FFI light curves** from Sectors 1–83+ (QLP and SPOC pipelines, publicly available via MAST).
- **ExoFOP-TESS** for supplementary stellar characterization.
- **Gaia DR3** astrometric excess noise and RUWE for independent evidence of massive companions.

### Novelty

The vast majority of TTV analyses focus on short-period oscillatory signals from near-resonant planet pairs. The secular, long-timescale drift signal caused by distant perturbers has been discussed theoretically (e.g., Agol et al. 2005; Nesvorný 2009) but has almost never been systematically exploited with real data, primarily because sufficient baselines didn't exist until TESS revisited the Kepler field. A few individual systems have been studied (e.g., Kepler-88), but no population-level survey of long-baseline TTV drifts has been published.

### Concrete Workflow

1. Cross-match the Kepler planet candidate catalog with TESS observed targets; identify systems with ≥3 Kepler transits and ≥2 TESS transits (expect ~500–1000 systems).
2. Extract precise transit times from TESS FFI photometry using template-matching or MCMC fitting of individual transits.
3. For each system, construct an O-C (observed minus calculated) timing diagram spanning the full ~15-year baseline.
4. Fit the O-C diagrams with: (a) a constant-period model, (b) a linear drift model (indicative of a period derivative from a distant perturber), and (c) a quadratic/sinusoidal model.
5. Identify statistically significant non-constant O-C trends using Bayesian model comparison (e.g., Bayes factors).
6. For systems with significant drifts, perform N-body dynamical modeling to constrain the mass and orbital period of the unseen perturber.
7. Cross-validate against Gaia DR3 astrometric excess noise: systems with TTV-inferred massive companions should show elevated RUWE or astrometric excess noise.

### Expected Signal / Observable

A Jupiter-mass planet at 3 AU perturbing an inner transiting planet at 0.1 AU produces a TTV drift of ~10–100 seconds over 15 years, depending on geometry. TESS FFI transit timing precision for bright Kepler targets is ~30–120 seconds for individual transits but can be beaten down with multiple transits. Detection of ~10–50 systems with statistically significant long-period TTV drifts, a subset of which will have Gaia astrometric corroboration.

### Possible False Positives / Pitfalls

- Stellar activity (spot crossings) can introduce quasi-random timing offsets, particularly for active stars; careful treatment with Gaussian process noise models is needed.
- Instrumental systematics between Kepler and TESS (different bandpasses, different apertures, different pixel scales) can introduce apparent timing offsets; careful detrending and aperture selection is critical.
- Apsidal precession in eccentric inner orbits can mimic a secular drift without requiring an external companion; this can be tested by looking for correlated transit duration changes.
- Period decay from tidal dissipation (relevant for ultra-short-period planets) is a physical signal that must be distinguished from companion-induced drift.

### Why It Matters

This would represent the first systematic census of giant planets in the 1–10 AU range around Kepler host stars — a population that is extremely difficult to probe by any other method for these typically faint (Kp 12–16) stars. It directly constrains the "cold Jupiter" occurrence rate around hosts of inner small planets, a key parameter for understanding system architecture and the role of giant planets in shaping inner planetary systems. It also demonstrates a novel use of the Kepler+TESS temporal baseline that will only improve as TESS continues operating.

---

## Project 3: Obliquity Constraints from Phase Curve Asymmetries — Do Tidally Unlocked Warm Jupiters Show Seasonal Atmospheric Signatures?

### Scientific Premise

Hot Jupiters on very tight orbits are expected to be tidally locked, producing a fixed day-night temperature contrast visible as a thermal phase curve with maximum brightness near secondary eclipse. But "warm Jupiters" — gas giants on slightly wider orbits (periods ~10–100 days) — may not be fully synchronised. If they retain non-zero obliquity or non-synchronous rotation, their atmospheric temperature patterns should evolve over the orbit, producing *asymmetric or time-variable phase curves* that differ qualitatively from the locked case. This project proposes to use Spitzer archival data and TESS continuous-viewing-zone (CVZ) photometry to search for phase curve anomalies in warm Jupiters that could indicate non-synchronous rotation or non-zero obliquity — effectively probing the spin state of exoplanets, a quantity that is almost never measured.

### Target Datasets

- **Spitzer IRAC 3.6 and 4.5 µm full-orbit phase curve observations** from the archive (a dozen warm/hot Jupiters with multi-orbit coverage).
- **TESS CVZ light curves**: planets in the continuous viewing zones have ~1 year of nearly uninterrupted photometry per TESS hemisphere — sufficient to detect phase curve evolution over multiple orbits.
- **Kepler long-cadence photometry** for the ~10 warm Jupiters observed by Kepler with periods >10 days (e.g., Kepler-17b, HAT-P-7b at the hot end).

### Novelty

Phase curve studies overwhelmingly focus on ultra-hot and hot Jupiters (P < 5 days), where tidal locking is a safe assumption. The warm Jupiter regime has been largely neglected for phase curve analysis because signals are smaller and orbital periods are longer. Almost no published work has searched for *orbit-to-orbit phase curve variability* as a diagnostic of non-synchronous rotation or obliquity. Rauscher & Kempton (2014) and others have modeled what oblique phase curves would look like, but observational searches are essentially absent. The recent JWST 3D mapping of WASP-18b demonstrates that spatially resolved atmospheric structure is now detectable — extending this thinking to temporal variability is a natural but unexplored step.

### Concrete Workflow

1. Identify all warm Jupiters (P = 10–100 days) with multi-orbit continuous photometry from Kepler, TESS CVZ, or Spitzer (~20–40 targets).
2. Extract individual-orbit phase curves by folding photometry on the orbital period but keeping each orbit separate.
3. Characterize each orbit's phase curve with a low-order Fourier decomposition (amplitude, phase offset, asymmetry coefficient).
4. Test for statistically significant orbit-to-orbit variability in these parameters using hierarchical Bayesian models that account for instrumental red noise.
5. For systems showing variability, compare the observed variability pattern (timescale, amplitude modulation) to GCM predictions for non-synchronous rotators and oblique planets (using published model grids or running simplified GCMs).
6. Cross-reference with measured orbital eccentricity and predicted tidal synchronization timescales to assess physical plausibility.

### Expected Signal / Observable

For a warm Jupiter with ~30° obliquity and non-synchronous rotation, theory predicts orbit-to-orbit phase curve amplitude variations of ~50–200 ppm in the optical (Kepler/TESS) and ~500–2000 ppm at 4.5 µm (Spitzer). The phase offset (hot-spot longitude) should shift by several degrees between orbits. TESS single-orbit phase curve precision for bright warm Jupiters is ~50–100 ppm, marginal for individual detections but powerful when stacking evidence across orbits and targets.

### Possible False Positives / Pitfalls

- Stellar variability (spots, faculae) can modulate the apparent phase curve at timescales similar to the orbital period; careful stellar variability modeling (e.g., Gaussian processes trained on out-of-transit data) is essential.
- Weather-like stochastic atmospheric variability in a tidally locked planet could mimic the signal of non-synchronous rotation; distinguishing periodic (obliquity-driven) modulation from stochastic variability is key.
- Instrumental systematics in Spitzer (intrapixel sensitivity variations) and TESS (scattered light, momentum dumps) can introduce orbit-to-orbit variability; careful systematics modeling with pixel-level decorrelation is required.
- Low signal-to-noise for individual orbits means this may be a statistical/population-level detection rather than robust individual detections.

### Why It Matters

Measuring or constraining the spin states of exoplanets is one of the most difficult observational challenges in the field, yet spin state is a fundamental physical property that affects climate, atmospheric circulation, and even habitability. This project would provide the first observational constraints on obliquity and rotation for a population of exoplanets, opening an entirely new parameter space. For warm Jupiters specifically, spin-orbit misalignment probes tidal dissipation efficiency and dynamical history (e.g., past high-eccentricity migration), connecting atmospheric observations to orbital dynamics.

---

## Summary Table

| Project | Key Data | Primary Observable | Timescale to First Result |
|---|---|---|---|
| Sulfur Sequence | JWST spectra (Cycles 1–4) | Sulfur abundance clustering across planet population | ~6–12 months (retrieval-intensive) |
| TTV Archaeology | Kepler + TESS timing | Long-baseline O-C drifts from unseen companions | ~6–9 months (data-intensive) |
| Obliquity from Phase Curves | TESS CVZ + Spitzer + Kepler | Orbit-to-orbit phase curve variability | ~9–12 months (careful systematics work) |

---

*This report was generated autonomously as part of a scheduled exoplanet research brainstorming task.*
