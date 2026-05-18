# Exoplanet Research Project Ideas — May 6, 2026

Three ambitious, potentially underexplored project proposals based on publicly available space mission data.

---

## Project 1: Transit Duration Variation Archaeology — Detecting Orbital Precession and Hidden Mutual Inclinations in TESS Multi-Planet Systems

### Scientific Premise

Transit duration variations (TDVs) are the neglected sibling of transit timing variations (TTVs). While TTV analysis has matured into a standard tool for mass measurement (especially near mean-motion resonances), TDVs encode different and complementary dynamical information: they are sensitive to changes in the orbital impact parameter over time, which traces nodal precession driven by mutual inclinations between planets. A precessing orbit changes how the planet's chord crosses the stellar disk, altering the transit duration on timescales of years to decades. In multi-planet systems, even modest mutual inclinations (a few degrees) can produce measurable TDV signals, and these mutual inclinations are a fossil record of the system's dynamical history — whether planets migrated smoothly in a disk, were scattered, or were torqued by an external companion.

Despite theoretical predictions dating back over a decade, systematic TDV searches across large samples remain sparse. The recent homogeneous TTV survey of 423 single-transiting TESS systems (A&A, 2026) focused primarily on timing shifts. TDV signals in these same lightcurves — and in the longer-baseline Kepler/K2 systems now supplemented by TESS re-observations — are largely unmined at population scale.

### Target Datasets

- **Kepler DR25 long-cadence and short-cadence lightcurves** (17 quarters, ~4 years baseline) for ~700 multi-planet candidate systems.
- **TESS Full-Frame Images and 2-minute cadence data** from Sectors 1–83+ (ongoing extended mission), providing a second epoch 6–10 years after Kepler for overlap targets.
- **K2 campaigns** covering ecliptic fields with multi-planet systems.
- **NASA Exoplanet Archive** cumulative planet table and TTV/TDV catalogs for cross-referencing.

### Novelty

Most TTV papers either ignore TDVs entirely or treat them as nuisance parameters. A handful of individual case studies exist (e.g., Kepler-117, Kepler-108), but no one has conducted a population-level TDV survey that combines Kepler-era and TESS-era baselines to measure long-term orbital precession rates across hundreds of systems. The key innovation is leveraging the ~10-year time lever between Kepler and TESS to detect slow precession that was invisible within Kepler's 4-year window alone.

### Concrete Workflow

1. **Sample construction.** Cross-match Kepler/K2 multi-planet systems with TESS observed sectors using TIC/KIC identifiers. Prioritize systems with ≥2 transiting planets and sufficient TESS coverage for at least 3 transits per planet.
2. **Uniform transit fitting.** Fit individual transits in both Kepler and TESS data using a consistent model (e.g., `batman` + Gaussian process stellar variability model) to extract per-transit duration, depth, and mid-time with MCMC uncertainties.
3. **TDV time series construction.** For each planet, construct the duration time series spanning the combined Kepler+TESS baseline. Fit a linear trend and sinusoidal precession model to the TDV series.
4. **Dynamical interpretation.** For systems with significant TDV trends, use N-body integrations (e.g., `REBOUND` with `REBOUNDx`) to constrain the mutual inclination required to produce the observed precession rate, marginalizing over companion masses from TTV constraints or RV data.
5. **Population statistics.** Compile the mutual inclination distribution across the sample and compare to predictions from smooth disk migration (low mutual inclinations, <2°) vs. post-disk dynamical excitation (broader distribution).

### Expected Signal/Observable

Nodal precession periods for typical compact Kepler multis are ~50–500 years. Over a 10-year baseline, this produces transit duration changes of ~10–60 seconds for mutual inclinations of 1–5°, depending on orbital periods and planet masses. Kepler short-cadence data achieves transit duration precision of ~5–20 seconds per transit; stacking multiple transits and comparing epoch-averaged durations between Kepler and TESS should reach sensitivity to changes of ~10 seconds.

### Possible False Positives

- **Stellar variability and spot-crossing events** can distort transit shapes and bias duration measurements. Mitigation: use Gaussian process detrending and flag transits with obvious spot anomalies.
- **Instrumental systematics** — differences in Kepler vs. TESS bandpass and cadence can introduce apparent duration offsets. Mitigation: inject synthetic transits into both datasets and verify recovery consistency.
- **TTVs masquerading as TDVs** — strong TTVs can shift the ingress/egress timing asymmetrically, mimicking a duration change. Mitigation: simultaneously fit TTVs and TDVs in a coupled model.
- **Apsidal precession** in eccentric orbits also produces TDVs; distinguishing nodal from apsidal precession requires joint TTV+TDV modeling.

### Why It Matters

The mutual inclination distribution of planetary systems is one of the most direct diagnostics of post-formation dynamical evolution, but it is extremely difficult to measure — transit surveys are geometrically biased toward coplanar systems, and astrometric measurements remain limited. TDV-based precession detection offers a unique channel to measure this quantity for hundreds of systems simultaneously, using data that already exists. A discovery that compact multis harbor hidden mutual inclinations of several degrees would challenge the prevailing "flat as a pancake" narrative and point toward late-stage dynamical sculpting.

---

## Project 2: Mapping the Neptunian Desert's Shoreline with TESS Phase Curves — Constraining Atmospheric Mass Loss Through Day-Night Temperature Contrasts

### Scientific Premise

The "Neptunian desert" — the observed deficit of Neptune-sized planets (roughly 3–10 R⊕) at very short orbital periods (P < 3–5 days) — is thought to arise from intense atmospheric photoevaporation and/or Roche-lobe overflow stripping away volatile envelopes. Yet the desert has fuzzy boundaries, and a growing population of planets perch right at its edges: the so-called "Neptunian savanna" or "desert oasis" planets. These border-dwellers are caught in the act of losing (or retaining) their atmospheres and may represent a snapshot of ongoing envelope erosion.

Phase curve analysis — measuring the planet's thermal emission and reflected light as it orbits — can reveal the day-night temperature contrast, which is sensitive to atmospheric composition, mass, and recirculation efficiency. A planet actively losing its upper atmosphere should show a hotter, more asymmetric phase curve (poor heat redistribution due to a thinner, higher-mean-molecular-weight atmosphere) compared to a "healthy" Neptune with a thick H/He envelope. This signature has not been systematically searched for across the Neptunian desert boundary population.

### Target Datasets

- **TESS 2-minute and 20-second cadence data** for the ~30–50 confirmed and validated planets within or at the boundary of the Neptunian desert (e.g., LTT 9779 b, TOI-849 b, GJ 3470 b, TOI-332 b, GJ 436 b).
- **TESS Full-Frame Images** for longer-period desert-edge planets with lower-cadence but multi-sector coverage.
- **Spitzer/IRAC 3.6 and 4.5 μm archival phase curves** for calibration targets (handful of hot Jupiters and hot Neptunes observed pre-decommissioning).
- **JWST Cycle 1–4 public phase curve and eclipse data** (e.g., GJ 1214 b, GJ 3470 b) as anchor points for atmospheric models.

### Novelty

Phase curves have been extensively studied for hot Jupiters, and a few individual hot Neptunes have JWST observations, but there has been no systematic phase curve survey targeting the Neptunian desert boundary as a population. The key insight is that TESS's continuous staring at many of these targets across multiple sectors (some now observed in 10+ sectors) provides enough photometric precision — when phase-folded — to detect phase curve amplitudes of ~20–50 ppm for moderately bright host stars, even though individual TESS phase curves are typically too noisy. The project connects atmospheric diagnostics (day-night contrast) to mass-loss theory (envelope stripping) in a way that neither field has pursued in a unified sample.

### Concrete Workflow

1. **Target selection.** Use the NASA Exoplanet Archive to identify all confirmed/validated planets with Rp = 3–10 R⊕ and P < 5 days. Extend to P < 10 days for the "savanna" population. Cross-match with TESS observation logs to find targets with ≥4 sectors of coverage.
2. **Lightcurve preparation.** Download TESS PDCSAP lightcurves (or extract from FFIs using `eleanor` or `TESS-point`). Detrend stellar variability using a spline or Gaussian process model, masking transits and occultations.
3. **Phase curve extraction.** Phase-fold each planet's full out-of-transit lightcurve on its orbital period. Fit a sinusoidal + second-harmonic phase curve model to extract: (a) thermal emission amplitude (eclipse depth proxy), (b) phase offset of the brightness peak (hot-spot shift), (c) day-night amplitude ratio.
4. **Atmospheric modeling.** Use a 1D radiative-convective model (e.g., `HELIOS` or `PICASO`) to generate predicted phase curve shapes for a grid of atmospheric compositions (H/He-dominated, H₂O-dominated, high-μ post-evaporation remnant). Compare observed phase curve metrics to the grid.
5. **Population analysis.** Plot day-night contrast and phase offset against the planet's position in (Rp, P, insolation) space relative to the desert boundary. Test the hypothesis that planets deeper inside the desert show larger day-night contrasts (thinner atmospheres) than those at the savanna.

### Expected Signal/Observable

For a hot Neptune at Teq ~ 1500–2000 K orbiting a K-dwarf, the TESS-band eclipse depth is ~30–100 ppm (thermal + reflected). Phase curve semi-amplitudes of ~15–50 ppm are expected. With 10 sectors of TESS data (~270 days), phase-folding ~100 orbits yields per-bin scatter of ~5–10 ppm for hosts brighter than T = 10, sufficient to detect these signals at 3–5σ.

### Possible False Positives

- **Ellipsoidal variations and Doppler boosting** contribute to the phase curve shape and must be modeled jointly; these depend on the planet's mass and the star's properties, not the atmosphere.
- **Stellar variability residuals** at the orbital period (e.g., if the planet tidally induces spots) could mimic a phase curve signal. Mitigation: check for period harmonics and compare even/odd sector phase curves for consistency.
- **Reflected light vs. thermal emission degeneracy** — in the TESS bandpass (600–1000 nm), both contribute. This limits compositional inference but can be broken by combining with Spitzer or JWST eclipse depths at longer wavelengths for the subset with archival IR data.
- **Clouds and hazes** on the dayside can increase albedo and mimic the signature of a thin atmosphere. Mitigation: the phase offset diagnostic (shifted hotspot implies advection, ruling out a purely reflective cloud deck) provides a cross-check.

### Why It Matters

Understanding the Neptunian desert is central to the theory of planetary evolution — it defines the boundary conditions for which planets survive intense irradiation. Currently, mass-loss models are primarily calibrated against radius and mass measurements (the radius valley). Phase curves offer an independent, atmospheric-level diagnostic: they probe the *current state* of the atmosphere (composition, mass, circulation) rather than its integrated history. If the data reveal a gradient in atmospheric properties across the desert boundary, it would be the first observational confirmation that the desert is actively being sculpted in real time, not just a relic of early evolution.

---

## Project 3: The Exoplanet Obliquity–Multiplicity Connection — Testing Whether Spin-Orbit Misalignment Predicts Hidden Companions via Combined RM + TTV Analysis

### Scientific Premise

Spin-orbit misalignment (stellar obliquity) is now measured for ~265 exoplanets, primarily hot Jupiters, via the Rossiter-McLaughlin (RM) effect. Recent population analysis (A&A, 2026) confirms no simple clustering pattern — misaligned planets span a wide range of obliquities. The leading explanations for misalignment involve dynamical interactions: planet-planet scattering, Kozai-Lidov oscillations from an inclined companion, or primordial disk-star misalignment. Each mechanism makes distinct predictions about whether misaligned planets should have detectable companions, and what those companions' orbital properties should be.

Yet the link between obliquity and the presence (or absence) of additional planets in the same system has never been tested systematically with a large, uniformly analyzed sample. The hypothesis is simple and falsifiable: if high-eccentricity migration via a companion is the dominant pathway, then misaligned hot Jupiters should show evidence of massive companions (either transiting or through TTVs/RV trends) at higher rates than well-aligned hot Jupiters.

### Target Datasets

- **TEPCat catalog** of published spin-orbit measurements (~265 planets with projected obliquity λ and, for ~116, true obliquity ψ).
- **TESS lightcurves** for all RM-measured planets with TESS coverage: search for TTVs indicating additional dynamical companions, and for additional transiting planets.
- **Gaia DR3/DR4 astrometric acceleration catalog** (HIPPARCOS–Gaia proper motion anomaly) to flag long-period massive companions.
- **Archival radial velocity data** from HARPS, HIRES, SOPHIE, ESPRESSO (publicly archived on DACE, ESO, Keck archives) to identify long-term RV trends.
- **High-contrast imaging surveys** (archived direct imaging data from VLT/SPHERE, Gemini/GPI) for outer stellar or substellar companions.

### Novelty

Individual studies have noted correlations between misalignment and companion presence in small samples or for specific sub-populations (e.g., WASP-8, HAT-P-11). The 2026 obliquity population paper analyzed the obliquity distribution itself but did not cross-correlate with companion demographics. No study has built a comprehensive, multi-technique companion census (TTVs + RV trends + astrometry + imaging) for the full obliquity sample and performed a rigorous statistical test of the obliquity-multiplicity connection. The innovation is the synthesis: using four independent companion-detection methods with complementary sensitivity ranges (TTVs for close-in resonant companions, RV trends for intermediate-period planets, Gaia astrometry for wide Jupiters, imaging for stellar companions) to construct a nearly complete companion occurrence picture for each obliquity-measured system.

### Concrete Workflow

1. **Master catalog assembly.** Merge TEPCat obliquity measurements with NASA Exoplanet Archive system parameters. For each system, compile: (a) projected obliquity λ and uncertainty, (b) true obliquity ψ where available, (c) stellar Teff (to control for the known tidal realignment effect — cool stars realign faster), (d) planet orbital eccentricity.
2. **TESS TTV search.** For all targets observed by TESS, fit individual transit mid-times and construct a TTV time series. Flag systems with TTV amplitudes > 30 seconds (indicative of nearby companions). For Kepler-overlap targets, combine baselines.
3. **RV trend search.** Download public RV time series from DACE and observatory archives. Fit Keplerian orbit of known planet + linear/quadratic trend. Flag systems with significant acceleration (> 3σ).
4. **Astrometric companion search.** Cross-match with Gaia DR3/DR4 proper motion anomaly catalogs (e.g., Kervella et al., Brandt et al.). Flag systems with significant astrometric acceleration.
5. **Imaging companion search.** Cross-match with published high-contrast imaging surveys. Record detected companions and upper limits on companion mass at relevant separations.
6. **Statistical analysis.** For the sample split by obliquity (aligned: |λ| < 20°; misaligned: |λ| > 20°; retrograde: |λ| > 100°), compute the companion occurrence rate from each detection method. Use a hierarchical Bayesian model to account for varying detection sensitivities across systems. Test the null hypothesis that companion occurrence is independent of obliquity. Control for confounders: stellar effective temperature, planet mass, orbital period, system age.

### Expected Signal/Observable

If Kozai-Lidov migration is the dominant misalignment channel, we expect misaligned hot Jupiters to show companion occurrence rates 2–5× higher than aligned systems, with companions preferentially at periods of tens to hundreds of days (the "Kozai perturber" regime) or as wide stellar binaries. Planet-planet scattering predicts a different signature: companions should be massive and on eccentric, mutually inclined orbits, potentially detectable as large-TTV or large-RV-trend signals. Disk-torquing predicts no companion excess at all — the misalignment is primordial. The statistical power of the test depends on sample size; with ~265 systems and ~50% companion detection completeness, a 3× difference in companion rates would be detectable at ~3σ.

### Possible False Positives

- **Selection bias in obliquity measurements** — RM measurements require bright, rapidly rotating stars with large transit depths (mostly hot Jupiters around F/A stars), biasing the sample toward specific stellar populations that may independently correlate with companion rates.  Mitigation: restrict analysis to a volume-limited or magnitude-limited sub-sample and model selection effects.
- **Tidal realignment masking true obliquities** — cool stars (Teff < 6100 K) can tidally erase primordial misalignment, making originally misaligned systems appear aligned. Mitigation: analyze cool and hot host stars separately; use the tidal efficiency factor from recent literature to model the probability of realignment.
- **Incomplete companion census** — each detection method has blind spots (TTVs miss non-resonant companions; RVs miss face-on systems; imaging misses close separations). Mitigation: the hierarchical Bayesian framework marginalizes over detection completeness maps for each method.
- **Small-number statistics** — the misaligned sub-sample may be small enough that Poisson noise dominates. Mitigation: report posterior distributions on occurrence rate ratios rather than point estimates; use the full obliquity distribution rather than a binary cut.

### Why It Matters

Distinguishing between misalignment mechanisms is one of the central open questions in planetary dynamics. Each mechanism implies a fundamentally different story about how giant planets reach short-period orbits. A definitive statistical correlation (or lack thereof) between obliquity and companion presence would collapse the space of viable formation theories and inform the interpretation of every future obliquity measurement — including those expected from PLATO (launching 2026) and the growing ESPRESSO sample. If the null result holds (no correlation), it would strongly favor primordial disk-star misalignment, shifting the focus of formation theory from dynamical violence to conditions in the protoplanetary disk environment.

---

## Summary Table

| # | Title | Primary Data | Key Observable | Timescale |
|---|-------|-------------|----------------|-----------|
| 1 | TDV Archaeology | Kepler + TESS lightcurves | Transit duration changes (~10–60 s over 10 yr) | ~6 months analysis |
| 2 | Neptunian Desert Phase Curves | TESS multi-sector photometry | Day-night brightness contrast (~20–50 ppm) | ~4–6 months analysis |
| 3 | Obliquity–Multiplicity Connection | TEPCat + TESS + Gaia + archival RV/imaging | Companion occurrence vs. obliquity | ~6–9 months analysis |

---

*Generated May 6, 2026. These ideas are framed as potentially underexplored rather than completely unstudied — literature review recommended before committing to any project.*
