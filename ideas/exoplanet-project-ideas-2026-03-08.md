# Exoplanet Research Project Ideas — March 8, 2026

Three ambitious, potentially underexplored project concepts grounded in publicly available mission data.

---

## 1. Stroboscopic Exomoon Fingerprints in Archival Kepler Multi-Transit Systems

### Scientific Premise

When a planet hosts a moon, the planet orbits the planet–moon barycenter, imprinting a characteristic pattern onto successive transit times (TTVs) and transit durations (TDVs). For a single-moon system, the TTV–TDV diagram traces a predictable ellipse whose shape and orientation encode the moon's mass, orbital period, and inclination. This "stroboscopic" pattern is analytically deterministic after just three consecutive transits — yet it has barely been exploited as a systematic detection tool across the full Kepler long-cadence catalog.

Most TTV-based exomoon searches have focused on a handful of spectacular candidates (e.g., Kepler-1625b, Kepler-1708b) and relied on photodynamical forward-modeling, which is computationally expensive and biases searches toward large moons. A complementary, lighter-weight approach would be to construct TTV–TDV phase portraits for every multi-transit Kepler planet and search for the distinctive elliptical topology predicted by the analytic theory, flagging candidates for deeper photodynamical follow-up.

### Target Datasets

- **Kepler DR25** long-cadence light curves (publicly available via MAST).
- **Kepler TTV catalog** from Holczer et al. (2016) and Rowe et al. updates.
- Supplementary **TESS** transits for overlapping targets (to extend the time baseline by ~8 years).

### Novelty

Existing exomoon searches are overwhelmingly individual-target, photodynamical-model-driven efforts. This project inverts the approach: a population-level, model-light geometric screen applied uniformly to thousands of planets. The stroboscopic ellipse criterion was described theoretically (Heller et al. 2016) but has not been deployed as a bulk survey tool.

### Concrete Workflow

1. Extract or compile per-transit midtimes and durations for all Kepler planets with ≥6 transits.
2. For each planet, construct the TTV vs. TDV scatter and fit a 2D ellipse model vs. a null (random scatter) model using Bayesian Information Criterion.
3. Rank candidates by ellipse significance; cross-check against known TTV planet–planet interaction signals (using N-body posteriors from Hadden & Lithwick catalogs) to remove false positives.
4. For top candidates, perform injection-recovery tests on synthetic light curves with injected moons to calibrate detection sensitivity.
5. Submit the strongest candidates for photodynamical modeling or JWST white-light transit follow-up.

### Expected Signal / Observable

A statistically significant elliptical pattern in the TTV–TDV plane, with the ellipse semi-axes yielding the moon-to-planet mass ratio and orbital period ratio. For a Ganymede-mass moon around a Neptune-sized planet, expected TTV amplitudes are ~1–5 minutes, within reach of Kepler's timing precision for high-SNR transits.

### Possible False Positives

- Planet–planet gravitational perturbations can produce correlated TTV–TDV signals, but these typically evolve on much longer (super-orbital) timescales and do not trace closed ellipses in phase space.
- Stellar activity (spot-crossing events) can shift apparent midtimes; mitigated by using only white-light midtimes derived from full-transit fits rather than ingress/egress timing.
- Instrumental systematics in Kepler long-cadence data can introduce correlated noise; the injection-recovery step calibrates this.

### Why It Could Matter

No exomoon has been confirmed to date. A bulk geometric survey could either (a) surface a population of credible candidates that escaped individual searches, or (b) place the first meaningful upper limits on the occurrence rate of large moons across a broad parameter space — either outcome is publishable and high-impact.

---

## 2. Tidal Spin-Up Archaeology: Using Kepler/TESS Rotation Periods to Date Planet-Induced Stellar Rejuvenation

### Scientific Premise

Stars spin down over time via magnetic braking (gyrochronology). But a sufficiently massive, close-in planet can tidally transfer orbital angular momentum into the star, spinning it up and making it appear younger than its true age. This "tidal rejuvenation" has been theoretically predicted and tentatively observed in a few individual hot-Jupiter hosts, but no one has conducted a controlled, population-level test across a large uniform sample.

The idea: compare the photometric rotation periods of confirmed hot-Jupiter host stars to those of a control sample of similar stars *without* close-in giant planets, drawn from the same Kepler/TESS fields and matched in effective temperature, metallicity, and galactic kinematics (as a proxy for age). A systematic offset toward faster rotation in the hot-Jupiter hosts would constitute population-level evidence for tidal spin-up, and the magnitude of the offset as a function of planet mass and orbital period would constrain tidal dissipation efficiency (the stellar tidal quality factor Q'★).

### Target Datasets

- **Kepler stellar rotation period catalogs** (McQuillan et al. 2014; Santos et al. 2019, 2021) — ~34,000 FGK dwarfs with measured P_rot.
- **TESS rotation periods** from ongoing community catalogs for southern-sky hosts.
- **NASA Exoplanet Archive** for confirmed planet parameters (mass, period, eccentricity).
- **Gaia DR3** astrometry and radial velocities for kinematic age proxies (UVW velocities, galactic action-angle variables).
- **LAMOST / GALAH / APOGEE** spectroscopic surveys for T_eff, [Fe/H], and [α/Fe] matching.

### Novelty

Individual tidal-interaction case studies exist (e.g., WASP-18, τ Boo), and some theoretical population-synthesis work has been done. But a clean, observationally controlled comparison — hot-Jupiter hosts vs. matched non-hosts, with kinematic age control — has not been carried out at scale using the now-mature Kepler rotation catalogs and Gaia kinematics together. The key advance is using galactic kinematics as an age proxy independent of gyrochronology itself, breaking the circularity.

### Concrete Workflow

1. Cross-match Kepler rotation period catalogs with the confirmed planet catalog; identify ~200–400 hot-Jupiter hosts (P_orb < 10 d, M_p > 0.3 M_Jup) with measured stellar P_rot.
2. For each host, select 5–10 control stars from the same Kepler rotation catalog matched in T_eff (±100 K), [Fe/H] (±0.1 dex), and Gaia-derived galactic velocity dispersion (as age proxy).
3. Compare the P_rot distributions of hosts vs. controls using a hierarchical Bayesian model that accounts for measurement uncertainties and selection effects.
4. Parameterize the tidal spin-up signal as a function of planet mass, orbital period, and stellar convective envelope depth; infer Q'★ posteriors.
5. Validate by checking that the signal disappears for long-period giant planets (P_orb > 100 d), which should produce negligible tidal torque.

### Expected Signal / Observable

A statistically significant shift (perhaps 10–30%) toward shorter rotation periods in hot-Jupiter hosts relative to controls of the same kinematic age. The shift should scale with the tidal forcing parameter (M_p / a^3), providing a functional form that can be compared to theoretical tidal models.

### Possible False Positives

- Selection bias: stars with shorter rotation periods have less stellar jitter, making planet detection easier. Mitigated by using only confirmed (not candidate) planets and by including jitter-based detection-efficiency corrections.
- Metallicity–rotation correlations: higher metallicity stars may have different angular momentum histories. Mitigated by tight [Fe/H] matching.
- Binarity: unresolved binary companions can bias rotation measurements. Mitigated by excluding known binaries and flagging anomalous Gaia RUWE values.

### Why It Could Matter

Tidal dissipation in stars is one of the least constrained parameters in all of stellar/planetary astrophysics. An empirical, population-level measurement of Q'★ from rotation period offsets would provide a calibration point that feeds into models of tidal orbital decay (relevant to the inspiral of hot Jupiters), spin–orbit alignment evolution, and the long-term fate of close-in planets — topics central to current JWST and upcoming PLATO science.

---

## 3. Sulfur as a Tracer of Giant Planet Formation Location: A Systematic JWST Archival Spectroscopy Survey

### Scientific Premise

JWST has begun detecting sulfur-bearing molecules (SO₂, H₂S) in transiting exoplanet atmospheres, most notably SO₂ in the warm Neptune WASP-39b. Sulfur is scientifically interesting because it has a dramatically different condensation behavior than carbon or oxygen: sulfur species remain volatile at much higher temperatures and condense into refractory sulfides (like FeS, troilite) only deep in protoplanetary disks near the soot line (~700 K). This means that a planet's atmospheric sulfur abundance relative to carbon and oxygen (the S/C and S/O ratios) is a sensitive probe of *where* in the disk the planet accreted its solids — much more diagnostic than C/O alone, which is degenerate between ice-line and gas-accretion effects.

Despite this, most atmospheric retrieval studies report C/O and overall metallicity but do not systematically extract or interpret sulfur abundances, largely because the relevant spectral features (SO₂ at 4.0 and 7.3 μm; H₂S at 2.5 and 3.8 μm) overlap with water and CO₂ bands and require careful treatment.

### Target Datasets

- **JWST public archive** (MAST): NIRSpec G395H and MIRI LRS transmission and emission spectra of transiting giant planets from Cycle 1–3 GTO/GO programs. As of early 2026 there should be ~30–50 giant planets with published or archivable spectra in the relevant wavelength range.
- **Complementary ground-based high-resolution spectra** (e.g., VLT/CRIRES+, Gemini/IGRINS) for cross-validation of H₂S detections.

### Novelty

Individual sulfur detections have been reported (WASP-39b, WASP-107b, and a few others), but no one has yet performed a uniform, self-consistent retrieval of sulfur abundances across the full sample of JWST-observed giant planets and interpreted the resulting S/C and S/O population trends in the context of disk chemistry models. This would be among the first "demographic" studies of sulfur in exoplanet atmospheres.

### Concrete Workflow

1. Compile all publicly available JWST transmission/emission spectra of giant exoplanets (M_p > 0.05 M_Jup) with wavelength coverage spanning at least 2.5–5.0 μm.
2. Perform uniform atmospheric retrievals using an open-source framework (e.g., petitRADTRANS, POSEIDON, or TauREx) with a chemical model that includes H₂O, CO, CO₂, CH₄, SO₂, H₂S, and clouds/hazes.
3. Extract posterior distributions for S/H, C/H, O/H, and the derived ratios S/C, S/O, and C/O for each planet.
4. Plot these ratios against planet mass, equilibrium temperature, orbital period, and host-star metallicity. Compare to predictions from disk chemistry models (e.g., Turrini et al. 2021; Pacetti et al. 2022) that predict distinct S/C–C/O tracks for planets forming inside vs. outside the soot line and water ice line.
5. Test the hypothesis that planets with high S/O and near-solar C/O accreted most of their heavy elements from refractory-rich material inside the soot line (i.e., formed in situ or migrated from warm disk regions), while planets with low S/O formed beyond the ice line.

### Expected Signal / Observable

A bimodal or gradient distribution in the S/C–C/O plane across the sample, with the two clusters mapping onto distinct formation pathways. Specifically, hot Jupiters that formed via disk migration from beyond the ice line should show subsolar S/C, while those that formed in situ or scattered inward should show near-solar or supersolar S/C.

### Possible False Positives

- **Photochemistry**: UV irradiation can convert H₂S to SO₂ in the upper atmosphere, altering observable sulfur speciation without changing total sulfur abundance. Mitigated by retrieving total sulfur (H₂S + SO₂) rather than individual species.
- **Cloud opacity**: Sulfide clouds (MnS, ZnS) can sequester sulfur below the photosphere, reducing apparent atmospheric S/H. This is a real physical effect but can be modeled as a lower limit on true S/H.
- **Retrieval degeneracies**: SO₂ features overlap with H₂O at 4 μm. Mitigated by requiring multi-instrument or broad-wavelength coverage and reporting detection significances.
- **Small sample statistics**: With ~30–50 planets, population trends may have limited statistical power. The project's value partly lies in establishing the framework and identifying the most diagnostic targets for future follow-up.

### Why It Could Matter

C/O has been the flagship atmospheric ratio for constraining formation, but it is now recognized as insufficient on its own due to degeneracies. Sulfur breaks those degeneracies and offers a genuinely new axis of information. A systematic sulfur census from the growing JWST archive could reshape how the community interprets atmospheric abundances in the context of planet formation — and would directly inform target prioritization for JWST Cycle 5+ and the Ariel mission.

---

*Generated on March 8, 2026. Sources consulted include the NASA Exoplanet Archive, ExEP Science Gap List, recent arXiv preprints, and JWST public data holdings.*
