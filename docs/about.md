---
title: About
---

# About URBADAPT

URBADAPT is a modular open-source architecture for **city-level climate risk
assessment and adaptation investment appraisal**, developed at the
[CMCC Foundation](https://www.cmcc.it) and the
[European Institute on Economics and the Environment (EIEE)](https://www.eiee.org),
with contributions from [IIASA](https://iiasa.ac.at).

The design goal is that the same analytical code runs unchanged across cities and,
increasingly, across hazards. Everything city-specific — climate inputs,
demographics, cost parameters, policy assumptions — lives in a YAML configuration
file and a data manifest, never in the model code.

## Implementations

| Implementation | Hazard | Status |
|---|---|---|
| [URBADAPT-HEAT](heat/index.md) | Urban heat | v1.0, public |
| URBADAPT-FLOOD | Flooding | In development, not yet public |

## Authors

- **Armande Aboudrar-Méda** — CMCC · EIEE
- **Giacomo Falchetta** — CMCC · EIEE, IIASA — [giacomo.falchetta@cmcc.it](mailto:giacomo.falchetta@cmcc.it)

## Citation

Please cite the framework description when using URBADAPT-HEAT:

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

## Licence

The URBADAPT-HEAT code is released under
[CC0 1.0](https://github.com/URBADAPT/URBADAPT-HEAT/blob/main/LICENSE) — public
domain dedication. Input datasets carry their own licences; consult each provider
before redistribution.

## About this website

Documentation pages are the
[URBADAPT-HEAT GitHub wiki](https://github.com/URBADAPT/URBADAPT-HEAT/wiki),
synced into this site automatically on every build — the wiki remains the single
source of truth, so **documentation edits belong there**, not in the website
repository. The site itself is built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) from
[URBADAPT/URBADAPT.github.io](https://github.com/URBADAPT/URBADAPT.github.io).
