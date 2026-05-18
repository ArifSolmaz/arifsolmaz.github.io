# Ambitious Exoplanet Research Project Ideas

**Generated: April 8, 2026** | Strategy Report — 3 Underexplored, Discovery-Driven Proposals

---

## Project 1: Tidal Oblateness Archaeology — Mining Kepler/TESS for Planetary Shape Signatures to Constrain Interior States

### Scientific Premise

A planet's shape encodes its rotational state and interior density profile. A rapidly rotating or tidally distorted planet is oblate, and that oblateness subtly alters the ingress and egress morphology of its transit light curve. Theoretical predictions have long suggested that Kepler-class photometry should be sensitive to oblateness at the level of a few percent for inflated hot Jupiters, and recent results are finally beginning to deliver: HIP 41378f yielded the first robust oblateness constraint in 2025 (f ≤ 0.889 at 95% confidence), and Kepler-427b shows depth variations consistent with f = 0.19 at ~90% significance. A recent PNAS review (Ragozzine et al., 2025) highlighted that tidal distortion, rotational oblateness, and obliquity remain among the least-explored dynamical signals accessible to JWST and existing photometric archives — the community has been so focused on atmospheric characterization that shape-based science has been left on the table.

These early detections demonstrate that the signal is *there*, but the field remains in a one-planet-at-a-time mode. The key insight is that oblateness is not just a curiosity — it is a *direct probe of interior rotation and tidal dissipation efficiency*, two quantities that are extremely difficult to measure by any other means. A systematic oblateness census across the known hot Jupiter population could distinguish between tidal synchronization models, constrain the tidal quality factor Q', and identify planets with anomalously high obliquities (potentially maintained by secular spin-orbit resonances in multi-planet systems).

### Target Datasets

- **Kepler long-cadence and short-cadence light curves** for ~300 confirmed hot Jupiters and inflated sub-Saturns (MAST archive)
- **TESS 2-minute and 20-second cadence data** for the brightest transit hosts observed across multiple sectors
- **JWST NIRSpec/NIRISS transit observations** already in the archive (GO Cycles 1–3) where ingress/egress are well-sampled at high SNR
- **Spitzer 4.5 µm phase curves** (archival) for thermal emission asymmetry cross-checks

### Novelty

While individual studies have now achieved detections for a small number of planets (e.g., HIP 41378f, Kepler-427b), and earlier work placed upper limits on systems like Kepler-7b, no one has performed a *population-level* oblateness survey using uniform methodology across hundreds of planets. The statistical power of a population approach is that even non-detections become informative: an ensemble of upper limits on oblateness across a range of orbital periods, planetary radii, and stellar types would place the tightest constraints to date on tidal synchronization timescales and interior viscosity models. This is distinct from the one-planet-at-a-time paradigm that has dominated so far.

### Concrete Workflow

1. Construct a target list of all transiting planets with Rp > 0.5 RJ and P < 10 days from the NASA Exoplanet Archive, cross-matched with Kepler, TESS, and JWST archival coverage.
2. Develop a custom transit model incorporating planetary oblateness (parameterized as f = (Req - Rpole)/Req) and projected obliquity (θ), building on the Seager & Hui (2002) and Carter & Winn (2010) formalisms.
3. Fit each system's phase-folded light curve with both a spherical model and an oblate model using nested sampling (e.g., dynesty) to compute Bayesian evidence ratios.
4. For systems with marginal detections (ΔlnZ > 2), stack residuals from similar-parameter planets to search for a population-level signal.
5. Compare the resulting oblateness–period distribution against tidal evolution models (e.g., Leconte et al. 2010; Millholland & Laughlin 2019) to constrain Q' as a function of planet mass and radius.

### Expected Signal / Observable

For a planet with f ~ 0.05 (comparable to Saturn) and an obliquity of 30°, the transit depth asymmetry between ingress and egress is on the order of 50–100 ppm for a Jupiter-sized planet around a Sun-like star. This is below the noise floor for individual Kepler long-cadence transits, but *stacking 50+ transits for the best-observed planets* (or using TESS 20-second cadence for bright hosts) brings the effective sensitivity into the 10–30 ppm range, where detections become plausible for the most inflated, rapidly rotating cases.

### Possible False Positives

- **Starspot crossings** during ingress/egress can mimic asymmetric transit shapes. Mitigation: multi-epoch analysis (spot patterns change, oblateness does not), and infrared observations where spot contrast is reduced.
- **Gravity darkening** of the host star (if rapidly rotating or tidally distorted by the planet) can produce asymmetric transits. Mitigation: restrict the sample to slow rotators (v sin i < 5 km/s) or model gravity darkening jointly.
- **Transit timing variations (TTVs)** can shift ingress/egress if not properly detrended. Mitigation: fit individual transits rather than relying solely on phase-folded data.

### Why This Could Matter

A population-level constraint on planetary oblateness would be a *first*. It would directly measure how efficiently tidal forces synchronize planetary rotation — a process that is central to understanding the thermal evolution, atmospheric dynamics (day-night circulation is rotation-dependent), and long-term stability of close-in planets. It could also identify "smoking gun" cases of planets in spin-orbit resonance with obliquities preserved at high values, opening a new window on multi-planet dynamical histories.

---

## Project 2: Disintegrating Planet Mineralogy — Reconstructing Rocky Interior Compositions from Dusty Transit Tails with JWST + TESS

### Scientific Premise

A handful of ultra-short-period planets (USPs) are actively disintegrating, producing asymmetric, variable-depth transits caused by trailing dust clouds. The canonical systems include KIC 12557548b (Kepler), K2-22b, and the recently discovered BD+054868Ab — a TESS-discovered disintegrating planet with a host star ~100× brighter than K2-22b's, both leading and trailing dust tails extending ~9 million km, and by far the most favorable target for detailed spectroscopy. JWST is beginning to probe these systems: K2-22b was observed with MIRI spectroscopy in early 2025, revealing magnesium silicate minerals in the dust. The extraordinary opportunity here is that these disintegrating planets are *naturally performing destructive spectroscopy of their own interiors* — the dust particles sublimating off the surface carry mineralogical information about the mantle and crust composition that is otherwise completely inaccessible for exoplanets.

A 2025 study in Astrobiology highlighted that TESS and JWST together are now "unveiling disintegrating planetary interiors," but the field is still in its infancy: only a few systems have been studied, the wavelength-dependent transit depth (which encodes grain composition and size) has barely been mapped, and no one has attempted a systematic mineral identification campaign across all known disintegrating systems.

### Target Datasets

- **TESS continuous monitoring** of known and candidate disintegrating planets (KIC 12557548b, K2-22b, TOI candidates) to track transit depth variability and constrain mass-loss rates
- **JWST MIRI/LRS and NIRSpec/G395H transit spectroscopy** — the 8–12 µm silicate feature is diagnostic of olivine vs. pyroxene vs. quartz composition; 2–5 µm probes iron oxides and sulfides
- **Kepler archival photometry** for long-baseline variability studies of KIC 12557548b
- **Spitzer 3.6/4.5 µm archival transits** for wavelength-dependent depth constraints

### Novelty

Existing work has established that dust tails exist and that transit depths vary. What has *not* been done systematically is: (a) forward-modeling the wavelength-dependent transit depth across UV-to-MIR using Mie scattering theory for candidate mineral compositions, (b) fitting this against multi-instrument spectrophotometry to identify specific minerals, and (c) comparing the inferred mantle compositions against predictions from planet formation models (e.g., the Mg/Si and Fe/Mg ratios expected from different stellar compositions). This project would be the first attempt at "exoplanet geochemistry from transit spectroscopy of disintegrating worlds."

### Concrete Workflow

1. Compile all known and candidate disintegrating planet systems from the literature and TESS alerts (at least 4 confirmed plus candidates as of 2026, with BD+054868Ab as the prime new target).
2. For each system, gather all available photometric transit observations across wavelengths (Kepler, TESS, Spitzer, JWST, ground-based).
3. Build a forward model: (a) parameterize dust composition as a mixture of olivine, pyroxene, iron, corundum, and quartz; (b) compute grain opacity using Mie theory for a log-normal grain size distribution; (c) model the dusty tail geometry using a radiation-pressure-driven outflow model (Rappaport et al. 2012 formalism); (d) compute wavelength-dependent transit depth.
4. Fit the model to the observed multi-wavelength transit depth spectrum using MCMC, recovering posterior distributions on mineral fractions and grain size.
5. Compare inferred Mg/Si, Fe/Mg ratios to host star abundances (from spectroscopic surveys) to test whether the planet's bulk composition reflects its natal disk chemistry.

### Expected Signal / Observable

The silicate 10 µm feature produces a transit depth enhancement of ~100–500 ppm for a moderately dusty tail around a K-dwarf host. The NIR (2–5 µm) slope of the transit depth spectrum discriminates between iron-rich and magnesium-silicate-rich dust, with expected variations of ~50–200 ppm depending on grain composition. JWST MIRI can achieve ~50 ppm precision per transit for bright hosts, making mineral identification feasible with 3–5 transit observations per target.

### Possible False Positives

- **Grain size degeneracy**: Large grains produce grey (wavelength-independent) opacity, mimicking a different composition. Mitigation: use transit depth variability over time (smaller grains produce more variable transits) as an independent grain size constraint.
- **Circumstellar gas contamination**: Sublimated metals (Na, K, Fe, Ca) produce narrow absorption features that could be confused with dust features. Mitigation: high-resolution spectroscopy can resolve gas lines vs. broad dust features.
- **Stellar variability**: Active K/M dwarf hosts can introduce chromatic transit depth variations. Mitigation: out-of-transit stellar spectra to model and subtract spot/faculae contributions.

### Why This Could Matter

This would establish "exoplanet geochemistry" as an observational field. Knowing what rocky planets are actually *made of* — not just their bulk density — is essential for understanding planetary differentiation, magnetic field generation, plate tectonics potential, and ultimately habitability. Disintegrating planets are rare and ephemeral, but they offer a unique and time-limited window into rocky planet interiors that no other technique can provide.

---

## Project 3: Secular Brightness Trends in Hot Jupiters — Hunting for Real-Time Orbital Decay and Tidal Inflation Using Decade-Long Phase Curve Baselines

### Scientific Premise

Hot Jupiters on very short-period orbits are expected to undergo orbital decay via tidal dissipation in the host star, spiraling inward on timescales of ~10 Myr to ~1 Gyr depending on the stellar tidal quality factor Q'*. WASP-12b is the only confirmed case where a period decrease has been measured, now refined to −30.23 ± 0.82 ms/yr by CHEOPS observations (2025). However, orbital decay should also produce a *secular change in the planet's thermal emission* — as the orbit shrinks, tidal heating increases, the planet inflates, and its dayside brightness temperature rises. This is a second observable of the same physical process, and it has never been searched for systematically.

The idea is to leverage the extraordinary baseline now available — Spitzer observed hot Jupiter phase curves from 2005–2020, TESS has been monitoring many of the same targets since 2018, and JWST has added high-precision eclipse measurements from 2022 onward. For the most tidally stressed systems, the predicted brightness change over a 15–20 year baseline may be measurable.

### Target Datasets

- **Spitzer 3.6 and 4.5 µm secondary eclipse and phase curve measurements** (2005–2020) from the full Spitzer archive for ~50 hot Jupiters
- **TESS secondary eclipse depths** measured from stacked 2-minute cadence photometry (2018–2026, multiple sectors)
- **JWST MIRI and NIRCam eclipse photometry** (Cycles 1–4, archival) for overlap targets
- **Transit timing databases** (ETD, ExoClock) for independent orbital period derivative constraints

### Novelty

The transit timing approach to detecting orbital decay is well-established but measures only the period change. This project adds a *completely independent observable* — the secular trend in thermal emission — which probes a different aspect of the physics (tidal heating and radius inflation rather than just angular momentum transfer). No one has performed a systematic search for long-term brightness trends in hot Jupiter eclipses across the Spitzer-to-JWST era. The 15+ year baseline available for the brightest systems (HD 189733b, HD 209458b, WASP-12b, WASP-43b, WASP-18b) is unprecedented and will never be available again at these wavelengths (Spitzer is retired).

Furthermore, this project can detect tidal heating even in systems where period decay is too slow to measure via transit timing — because the brightness change depends on the *rate of tidal energy dissipation in the planet* (related to Q'p), while the orbital decay rate depends on dissipation in the *star* (Q'*). These are independent quantities, so a brightness trend without a timing trend (or vice versa) would break a fundamental degeneracy in tidal theory.

### Concrete Workflow

1. Compile a master list of hot Jupiters with both Spitzer-era (pre-2020) and TESS/JWST-era (post-2020) secondary eclipse measurements at overlapping or comparable wavelengths.
2. Perform homogeneous re-reduction of Spitzer 3.6/4.5 µm eclipse photometry using state-of-the-art detector models (BLISS, PLD) to minimize systematic offsets between epochs.
3. Measure TESS-band eclipse depths from stacked sector data, and compile JWST eclipse depths from the literature and archive.
4. For each planet, fit a linear trend (dTb/dt) to the brightness temperature time series, accounting for systematic offsets between instruments using a hierarchical Bayesian framework.
5. Compare measured dTb/dt against predictions from coupled tidal-thermal evolution models (Leconte et al. 2010, Millholland 2019) as a function of assumed Q'p, and cross-reference with transit timing constraints on Q'*.
6. Identify outlier systems where brightness is changing faster or slower than expected, flagging candidates for enhanced tidal dissipation or recent dynamical perturbations.

### Expected Signal / Observable

For WASP-12b (the strongest case), the predicted brightness temperature increase due to tidal heating as the orbit decays requires careful modeling: the secular component from changing orbital distance is modest (~5–20 K over 15 years), but note that observed eclipse depth variations for WASP-12b already span ~3σ between different Spitzer epochs (0.97 ± 0.14 vs. 0.44 ± 0.21 mmag), with attributions split between systematic errors and genuine atmospheric variability. The challenge — and the opportunity — is to disentangle the *monotonic secular trend* from stochastic atmospheric and instrumental variability. This requires careful epoch-binned analysis: averaging over the ~10 eclipses observed at each Spitzer epoch yields ~50 ppm effective precision, and the JWST-era measurements provide an independent anchor at the long-baseline end. For less extreme systems, the signal will be smaller, but the population approach (stacking non-detections) constrains the average Q'p.

### Possible False Positives

- **Spitzer detector systematics**: The InSb and Si:As detectors had well-documented intrapixel sensitivity variations and ramp effects that evolved over the mission. Mitigation: use multiple independent reduction pipelines (BLISS, PLD, BiLinearly-Interpolated Subpixel Sensitivity) and check for pipeline-dependent trends.
- **Stellar magnetic activity cycles**: G/K star hosts may have brightness variations at the ~0.1% level over decade timescales due to magnetic cycles, altering the eclipse depth baseline. Mitigation: use long-baseline ground-based photometric monitoring to track stellar variability independently.
- **Weather variability on the planet**: GCM simulations predict stochastic dayside temperature fluctuations at the ~50–100 ppm level in broadband photometry. Mitigation: averaging over multiple eclipses at each epoch suppresses stochastic variability; the key test is whether the trend is monotonic (as expected for tidal heating) rather than random.

### Why This Could Matter

Detecting a secular brightness trend in a hot Jupiter would be a landmark result — the first real-time observation of tidal heating reshaping a planet. It would provide a direct measurement of the planetary tidal quality factor Q'p, a quantity that is essentially unconstrained observationally but is central to understanding the thermal histories, radii, and survival of close-in planets. Combined with transit timing, it would allow simultaneous constraints on both stellar and planetary tidal dissipation — disentangling a degeneracy that has plagued the field for two decades. The Spitzer archive is a non-renewable resource; this analysis should be done before the community loses institutional knowledge of Spitzer systematics.

---

## Summary Comparison

| Criterion | Project 1: Oblateness Archaeology | Project 2: Disintegrating Mineralogy | Project 3: Secular Brightness Trends |
|---|---|---|---|
| **Primary observable** | Ingress/egress asymmetry | Wavelength-dependent transit depth | Eclipse depth time series |
| **Key instrument(s)** | Kepler, TESS, JWST | JWST MIRI + NIRSpec, TESS | Spitzer archive + TESS + JWST |
| **Population or individual** | Population survey | Individual systems (5–8) | Population + flagship individuals |
| **Physical quantity probed** | Rotation, interior viscosity, Q'p | Mantle mineralogy, Mg/Si, Fe/Mg | Tidal heating rate, Q'p, Q'* |
| **Novelty level** | First population oblateness survey | First exoplanet mineral identification | First brightness trend search across eras |
| **Risk level** | Medium (signals may be below threshold) | Medium-high (few targets, complex models) | Medium (systematic offsets between instruments) |
| **Publishability** | High even with non-detections | High if any mineral ID succeeds | High — unique use of Spitzer legacy |

---

*Note: All three projects rely entirely on public archival data (Kepler, TESS, Spitzer, JWST) accessible through MAST, the NASA Exoplanet Archive, and the IRSA Spitzer Heritage Archive. No new observations are required to begin.*
