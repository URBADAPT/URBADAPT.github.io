# URBADAPT.github.io

Source for the URBADAPT project website: **<https://urbadapt.github.io>**

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and
deployed to GitHub Pages by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

## Where the content comes from

| Content | Source | How it gets here |
|---|---|---|
| Documentation pages | [URBADAPT-HEAT wiki](https://github.com/URBADAPT/URBADAPT-HEAT/wiki) | Cloned and link-rewritten at build time by `scripts/sync_wiki.py`. **Never committed** — `docs/heat/` is gitignored. |
| Figures | [URBADAPT-HEAT](https://github.com/URBADAPT/URBADAPT-HEAT) (`reporting` branch) | Imported and downscaled once by `scripts/import_figures.py`. **Committed**, because the figures live on a research branch that may be merged away. |
| Landing page, gallery, about | This repository | Hand-written: `docs/index.md`, `docs/gallery.md`, `docs/about.md`. |

> [!IMPORTANT]
> The wiki is the single source of truth for documentation. To change a
> documentation page, **edit the wiki**, not `docs/heat/` — anything written
> there is deleted on the next sync.

## Local development

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows;  source .venv/bin/activate on Unix
pip install -r requirements.txt

python scripts/sync_wiki.py     # populate docs/heat/ from the wiki
mkdocs serve                    # http://127.0.0.1:8000
```

To iterate without hitting the network, point the sync at a local wiki clone:

```bash
python scripts/sync_wiki.py --wiki-path ../URBADAPT-HEAT.wiki
```

Reproduce the CI build exactly, including strict link checking:

```bash
mkdocs build --strict
```

## Updating figures

After regenerating figures in URBADAPT-HEAT, re-import and commit them:

```bash
python scripts/import_figures.py --source ../URBADAPT-HEAT
git add docs/assets && git commit -m "Update figures"
```

The script downscales to 1600 px and re-encodes as WebP (~11 MB of source PNGs
becomes ~2.4 MB). It also rebuilds the logo assets and favicon from
`logo_urbadapt.png`, keying out the white background.

## Adding or renaming a wiki page

`scripts/sync_wiki.py` fails the build if the wiki and the site disagree, rather
than shipping dead links. When you add or rename a wiki page:

1. Add it to `PAGE_MAP` in `scripts/sync_wiki.py`.
2. Add it to the `nav:` block in `mkdocs.yml`.

The sync errors out on a wiki page missing from `PAGE_MAP`, on a `PAGE_MAP` entry
missing from the wiki, and on any link pointing at an unknown page; it warns on a
page that is synced but absent from the nav.

## Publishing cadence

The site rebuilds on every push to `main`, daily at 05:17 UTC (to pick up wiki
edits), and on manual dispatch. For near-instant publishing of wiki edits, install
[`.github/wiki-watcher.yml.example`](.github/wiki-watcher.yml.example) in the
URBADAPT-HEAT repository.
