---
hide:
  - navigation
  - toc
---

<div class="urb-hero" markdown>

![URBADAPT](assets/logo_urbadapt.png){ .urb-hero__logo }

<p class="urb-hero__tagline">
Open-source geospatial frameworks for <strong>city-level climate risk assessment</strong>
and <strong>public–private adaptation cost-benefit analysis</strong> — reproducible
and city-agnostic.
</p>

<div class="urb-hero__buttons" markdown>
[Explore URBADAPT-HEAT](urbadapt-heat.md){ .md-button .md-button--primary }
[Code on GitHub](https://github.com/URBADAPT){ .md-button }
[Team](team.md){ .md-button }
</div>

</div>

---

## What URBADAPT does

URBADAPT is a modular architecture for assessing urban climate risk and appraising
adaptation investment. Each hazard-specific implementation shares the same
structure — hazard, exposure, vulnerability, impact functions, adaptation
pathways, cost-benefit analysis — so that methods and results stay comparable
across hazards and across cities.

Two commitments shape the design:

- **City-agnostic by construction.** Everything city-specific — climate inputs,
  demographics, cost parameters, policy assumptions — lives in a YAML
  configuration file and a data manifest. The analytical code runs unchanged
  everywhere, so adding a city means adding a config, not editing the model.
- **Adaptation is appraised, not assumed.** Adaptation options are represented
  through their physical mechanisms and carried through a discounted
  cost-benefit analysis with externalities, co-benefits, and distributional
  outcomes — rather than applied as headline percentage-reduction factors.

---

## Implementations

<div class="grid cards" markdown>

-   :material-thermometer-high:{ .lg .middle } __URBADAPT-HEAT__

    ---

    **v1.0 — available.** Urban heat risk and adaptation appraisal at ~100 m
    resolution for European functional urban areas. Quantifies heat-attributable
    mortality to 2050 and evaluates air conditioning, urban street trees, and
    early warning systems.

    [:octicons-arrow-right-24: Overview and documentation](urbadapt-heat.md)

-   :material-waves:{ .lg .middle } __URBADAPT-FLOOD__

    ---

    **In development.** The flood-hazard implementation of the same
    architecture, not yet publicly released. This page will link to its
    documentation when it is.

</div>

---

## Development

URBADAPT is developed in the
[ECIP Division](https://www.cmcc.it/what-we-do/institutes/european-institute-on-economics-and-the-environment-eiee/economic-analysis-of-climate-impacts-and-policy-division)
(Economic analysis of Climate Impacts and Policy) of the
[CMCC Foundation](https://www.cmcc.it), part of the
[European Institute on Economics and the Environment](https://www.eiee.org).

See [Team](team.md) for the people behind the framework and how to reach them.

## Licence

URBADAPT-HEAT is released under
[CC0 1.0](https://github.com/URBADAPT/URBADAPT-HEAT/blob/main/LICENSE) — a public
domain dedication. Input datasets carry their own licences; consult each provider
before redistribution.

## About this website

Documentation pages are the
[URBADAPT-HEAT GitHub wiki](https://github.com/URBADAPT/URBADAPT-HEAT/wiki),
synced into this site automatically on every build — the wiki remains the single
source of truth, so **documentation edits belong there**, not in the website
repository. The site is built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) from
[URBADAPT/URBADAPT.github.io](https://github.com/URBADAPT/URBADAPT.github.io).
