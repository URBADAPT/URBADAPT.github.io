---
title: URBADAPT-HEAT
---

# URBADAPT-HEAT

**URBADAPT-HEAT v1.0** is the urban heat implementation of the
[URBADAPT architecture](index.md): an open-source geospatial framework for
city-level heat risk assessment and public–private adaptation cost-benefit
analysis, built on the [CLIMADA](https://github.com/CLIMADA-project/climada_python)
probabilistic risk engine.

Given a European city, URBADAPT-HEAT:

1. **Maps the heat hazard** at ~100 m resolution using the UrbClim urban climate
   dataset, for a 2020 baseline and climate projections to 2050 across four CMIP6
   scenarios. Two hazard tracks are supported — a standard daily-mean track and
   an extreme-event (heatwave) track for cool and maritime cities.
2. **Quantifies heat-attributable mortality** with age-stratified exposure and
   city- and age-specific epidemiological impact functions.
3. **Evaluates three adaptation pathways** — air conditioning, urban street
   trees, and early warning systems — through their physical mechanisms, and
   represents the interactions between them.
4. **Integrates a 25-year discounted cost-benefit analysis** including
   externalities (air conditioning waste heat), co-benefits (vegetation reducing
   cooling electricity demand), and distributional outcomes across social
   vulnerability quintiles.
5. **Identifies cost-effective adaptation portfolios** via Pareto-frontier budget
   optimisation.

---

## At a glance

| | |
|---|---|
| **Spatial resolution** | ~100 m (UrbClim native grid, EPSG:3035) |
| **Temporal horizon** | 2020 · 2030 · 2040 · 2050 |
| **Climate scenarios** | CurPol, GS, SP, SSP5-8.5 (CMIP6 ensemble) |
| **Demographic scenarios** | SSP1–5, SSP2-DM, SSP2-ZM (Wittgenstein Centre) |
| **Cities configured** | 40+ European functional urban areas |
| **Cities demonstrated end-to-end** | Rome · Athens · Lisbon · Copenhagen |
| **Adaptation pathways** | Air conditioning · urban street trees · early warning systems |
| **Impact functions** | Masselot et al. city- and age-specific (main); Burke et al. (sensitivity) |
| **Risk engine** | [CLIMADA v6.1.0](https://github.com/CLIMADA-project/climada_python) |
| **Configuration** | One city-specific YAML file per city |

<figure markdown>
![URBADAPT-HEAT workflow diagram](assets/figures/workflow_diagram.webp)
<figcaption markdown>
**The URBADAPT-HEAT pipeline.** Ten numbered notebooks carry a city from raw
UrbClim climate fields and WorldPop demographics through hazard, exposure and
vulnerability construction, impact modelling, adaptation-pathway simulation, and
a 25-year discounted cost-benefit analysis to a Pareto-optimal portfolio.
</figcaption>
</figure>

---

## Quick start

URBADAPT-HEAT runs on Python 3.10 in a dedicated conda environment:

```bash
git clone https://github.com/URBADAPT/URBADAPT-HEAT.git
cd URBADAPT-HEAT
conda env create -f urban-heat/environment.yml
conda activate urbanheat
pip install -e urban-heat          # installs the cityheat helper package
jupyter-lab urban-heat/notebooks   # open the notebook pipeline
```

The analysis runs as ten numbered notebooks (`01_setup` → `10_summary`). They are
city-agnostic: select a city with a single line near the top of notebook 01, then
run `01` → `10` in order.

```python
os.environ["CITY"] = "Rome"   # or Athens / Lisbon / Copenhagen
```

See [Installation & usage](heat/installation.md) for the full walkthrough,
including data sync and the one-click Windows launcher, and
[City configuration](heat/city-configuration.md) for how to add a new city.

---

## Documentation

| Page | Description |
|---|---|
| [Installation & usage](heat/installation.md) | Setup, dependencies, data sync, running the notebook pipeline |
| [Framework overview](heat/framework-overview.md) | Architecture, pipeline structure, spatial domain |
| [Hazard](heat/hazard.md) | UrbClim T2M fields, synthetic baseline, climate deltas |
| [Exposure](heat/exposure.md) | Age-stratified population, WorldPop, demographic projections |
| [Vulnerability](heat/vulnerability.md) | Social Vulnerability Index, dynamic projection |
| [Impact functions](heat/impact-functions.md) | Age-specific heat-mortality dose-response curves |
| [Adaptation pathways](heat/adaptation-pathways.md) | Air conditioning, street trees, early warning systems |
| [Cost-benefit analysis](heat/cost-benefit-analysis.md) | 25-year CBA, interactions, budget optimisation |
| [Uncertainty analysis](heat/uncertainty-analysis.md) | Structural, climate, and parametric sensitivity |
| [City configuration](heat/city-configuration.md) | Configuring URBADAPT-HEAT for a new city |
| [Case studies](heat/case-studies.md) | Rome, Athens, Lisbon, Copenhagen results |

---

## Data sources

URBADAPT-HEAT builds on openly available datasets and published epidemiology:

| Component | Source |
|---|---|
| Urban climate fields | [UrbClim](https://www.vito.be/en/urbclim) (VITO), ~100 m urban climate dataset |
| Climate projections | CMIP6 ensemble deltas (CurPol, GS, SP, SSP5-8.5) |
| Population | [WorldPop](https://www.worldpop.org/) gridded population |
| Demographic projections | [Wittgenstein Centre](https://www.oeaw.ac.at/vid/data-and-information-systems/wittgenstein-centre-data-explorer) Human Capital Data Explorer |
| Impact functions | Masselot et al., city- and age-specific (main); [Burke et al. 2025](https://doi.org/10.1038/s41591-024-03094-4) (sensitivity) |
| Risk engine | [CLIMADA v6.1.0](https://github.com/CLIMADA-project/climada_python) |

---

## Citation

Please cite the framework description when using URBADAPT-HEAT:

> Aboudrar-Méda, A. and Falchetta, G.: *URBADAPT-HEAT v1.0: a scalable geospatial
> framework for city-level public–private adaptation infrastructure cost-benefit
> analysis and its urban heat risk implementation*, in preparation, 2026.

```bibtex
@article{aboudrarmeda_urbadapt_heat_2026,
  author  = {Aboudrar-M{\'e}da, Armande and Falchetta, Giacomo},
  title   = {{URBADAPT-HEAT} v1.0: a scalable geospatial framework for
             city-level public--private adaptation infrastructure
             cost-benefit analysis and its urban heat risk implementation},
  year    = {2026},
  note    = {Manuscript in preparation}
}
```
