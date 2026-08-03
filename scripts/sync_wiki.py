#!/usr/bin/env python3
"""Sync the URBADAPT-HEAT GitHub wiki into docs/heat/ for the MkDocs build.

The wiki (https://github.com/URBADAPT/URBADAPT-HEAT/wiki) is the single source
of truth for documentation content. This script clones it and rewrites its
links so the pages work as a MkDocs site:

  * ``[Text](Page-Name)``      -> ``[Text](page-name.md)``   (wiki page links)
  * ``[Text](Home)``           -> ``[Text](../index.md)``    (wiki home -> landing)
  * ``[Text](../blob/main/X)`` -> absolute github.com URL    (repo-relative links)
  * ``[[Page]]``               -> ``[Page](page.md)``        (wikilink syntax)

Any wiki link that does not resolve to a known page is a hard error, so a
renamed or deleted wiki page fails the build loudly instead of shipping a dead
link. Run it before ``mkdocs serve`` / ``mkdocs build``:

    python scripts/sync_wiki.py                     # clone from GitHub
    python scripts/sync_wiki.py --wiki-path ../URBADAPT-HEAT.wiki   # local clone
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SITE_ROOT / "docs" / "heat"

WIKI_URL = "https://github.com/URBADAPT/URBADAPT-HEAT.wiki.git"
WIKI_WEB = "https://github.com/URBADAPT/URBADAPT-HEAT/wiki"
REPO_WEB = "https://github.com/URBADAPT/URBADAPT-HEAT"

# Wiki page name -> output filename under docs/heat/.
# Every page must be listed here and every entry must appear in mkdocs.yml nav;
# both directions are checked below, so adding a wiki page without wiring it
# into the nav is caught at build time rather than silently dropped.
PAGE_MAP: dict[str, str] = {
    "Home": "index.md",
    "Installation": "installation.md",
    "Framework-Overview": "framework-overview.md",
    "Hazard": "hazard.md",
    "Exposure": "exposure.md",
    "Vulnerability": "vulnerability.md",
    "Impact-Functions": "impact-functions.md",
    "Adaptation-Pathways": "adaptation-pathways.md",
    "Cost-Benefit-Analysis": "cost-benefit-analysis.md",
    "Uncertainty-Analysis": "uncertainty-analysis.md",
    "City-Configuration": "city-configuration.md",
    "Case-Studies": "case-studies.md",
}

# Markdown inline links whose target has no scheme and no leading slash — i.e.
# the bare-page-name style the GitHub wiki uses. The lookbehind skips image
# embeds (![alt](src)), whose targets are asset paths rather than wiki pages.
INLINE_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\((?!https?://|mailto:|#|/)([^)\s]+)\)")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


class SyncError(Exception):
    """A wiki link could not be resolved, or the wiki is out of sync."""


def resolve_target(target: str, source_page: str) -> str:
    """Rewrite one wiki link target to a MkDocs-relative path."""
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    target = target.strip()

    if not target:  # pure anchor, e.g. [Text](#section)
        return anchor

    # Repo-relative links out of the wiki, e.g. ../blob/main/LICENSE
    if target.startswith("../"):
        return f"{REPO_WEB}/{target.removeprefix('../')}{anchor}"

    # Already a relative file link (rare in the wiki, but pass it through).
    if target.endswith(".md"):
        return target + anchor

    if target not in PAGE_MAP:
        raise SyncError(
            f"{source_page}: link to unknown wiki page {target!r}.\n"
            f"    Either the page was renamed in the wiki, or PAGE_MAP in "
            f"scripts/sync_wiki.py needs updating."
        )

    # All pages, including Home, resolve within docs/heat/. The wiki Home
    # becomes the documentation section's overview page; the site's own landing
    # page (docs/index.md) is hand-written and separate.
    return PAGE_MAP[target] + anchor


def rewrite(text: str, source_page: str) -> str:
    """Apply all link rewrites to one page's markdown."""

    def inline(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        return f"[{label}]({resolve_target(target, source_page)})"

    def wikilink(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = (match.group(2) or target).strip()
        return f"[{label}]({resolve_target(target, source_page)})"

    text = WIKILINK.sub(wikilink, text)
    text = INLINE_LINK.sub(inline, text)
    return text


def add_source_footer(text: str, page: str) -> str:
    """Append a provenance note pointing back at the canonical wiki page."""
    return text.rstrip() + (
        "\n\n"
        '<div class="urb-source" markdown>\n'
        f"This page is maintained in the "
        f"[URBADAPT-HEAT wiki]({WIKI_WEB}/{page}) and synced automatically. "
        f"Edit it there, not in the website repository.\n"
        "</div>\n"
    )


def clone_wiki(dest: Path) -> None:
    print(f"Cloning {WIKI_URL}")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", "--quiet", WIKI_URL, str(dest)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SyncError(f"git clone failed:\n{result.stderr.strip()}")


def check_nav_coverage() -> list[str]:
    """Warn if mkdocs.yml nav and PAGE_MAP have drifted apart.

    Parsed textually rather than with a YAML loader: mkdocs.yml uses
    ``!!python/name:`` tags that safe_load rejects.
    """
    nav_text = (SITE_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    problems = []
    for page, filename in PAGE_MAP.items():
        if f"heat/{filename}" not in nav_text:
            problems.append(
                f"wiki page {page!r} -> heat/{filename} is synced but missing "
                f"from the mkdocs.yml nav"
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wiki-path",
        help="Use an existing local wiki clone instead of cloning from GitHub",
    )
    args = parser.parse_args()

    tmpdir = None
    try:
        if args.wiki_path:
            wiki = Path(args.wiki_path).resolve()
            if not wiki.is_dir():
                raise SyncError(f"{wiki} is not a directory")
            print(f"Using local wiki clone at {wiki}")
        else:
            tmpdir = tempfile.mkdtemp(prefix="urbadapt-wiki-")
            wiki = Path(tmpdir) / "wiki"
            clone_wiki(wiki)

        # Fail loudly if the wiki gained or lost pages.
        found = {p.stem for p in wiki.glob("*.md")}
        expected = set(PAGE_MAP)
        if missing := sorted(expected - found):
            raise SyncError(
                "wiki pages listed in PAGE_MAP but absent from the wiki: "
                + ", ".join(missing)
            )
        if extra := sorted(found - expected):
            raise SyncError(
                "wiki has pages not listed in PAGE_MAP (add them there and to "
                "the mkdocs.yml nav): " + ", ".join(extra)
            )

        # Rewrite every page up front so a bad link aborts before anything is
        # written — a half-synced docs/heat/ would still build, just wrong.
        rendered: dict[str, str] = {}
        for page, filename in sorted(PAGE_MAP.items()):
            text = (wiki / f"{page}.md").read_text(encoding="utf-8")
            text = rewrite(text, page)
            rendered[filename] = add_source_footer(text, page)

        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
        OUTPUT_DIR.mkdir(parents=True)

        print(f"\nSyncing {len(PAGE_MAP)} pages into docs/heat/")
        for page, filename in sorted(PAGE_MAP.items()):
            (OUTPUT_DIR / filename).write_text(rendered[filename], encoding="utf-8")
            print(f"  {page:<24} -> heat/{filename}")

        for problem in check_nav_coverage():
            print(f"\nWARNING: {problem}", file=sys.stderr)

        print("\nWiki sync complete.")
        return 0

    except SyncError as exc:
        print(f"\nerror: {exc}", file=sys.stderr)
        return 1
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
