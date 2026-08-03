#!/usr/bin/env python3
"""Import branding and publication figures from a local URBADAPT-HEAT checkout.

The figures live on the ``reporting`` branch of URBADAPT/URBADAPT-HEAT, not on
``main``, so fetching them at build time would break the site the moment that
branch is merged or deleted. Instead we import web-optimized copies once and
commit them. Re-run this script whenever the figures are regenerated:

    python scripts/import_figures.py --source ../URBADAPT-HEAT

Requires Pillow (``pip install -r requirements.txt``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: pip install -r requirements.txt")

SITE_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SITE_ROOT / "docs" / "assets"
FIGURES = ASSETS / "figures"

# Max width in CSS pixels; figures are displayed at most ~1000px wide, so 1600
# still covers HiDPI screens while cutting multi-MB publication figures down hard.
MAX_WIDTH = 1600

# Figures are emitted as WebP. The source PNGs are 3000 px flat-colour raster
# maps that PNG happens to compress well; resampling them introduces
# intermediate tones and a downscaled PNG comes out *larger* than the original.
# WebP handles both those maps and the vector-ish dashboards at a fraction of
# the size. The lossless originals stay in URBADAPT-HEAT for the manuscripts.
WEBP_QUALITY = 90

# (source path relative to URBADAPT-HEAT, destination stem)
FIGURE_SOURCES: list[tuple[str, str]] = [
    # Framework / methods figures (GMD manuscript)
    ("diagram.png", "workflow_diagram"),
    ("gmd_visual_items/fig_hazard_t2m_maps_rome.png", "gmd_hazard_t2m_rome"),
    ("gmd_visual_items/fig_exposure_population_rome.png", "gmd_exposure_rome"),
    ("gmd_visual_items/fig_svi_components_rome.png", "gmd_svi_rome"),
    ("gmd_visual_items/fig_ac_penetration_maps_rome.png", "gmd_ac_penetration_rome"),
    ("gmd_visual_items/fig_policy_levers.png", "gmd_policy_levers"),
    ("gmd_visual_items/fig_cba_dashboard.png", "gmd_cba_dashboard"),
    # Cross-city results figures (Nature Cities manuscript)
    ("natcities_visual_items/figures/fig1_risk_effectiveness.png", "nc_fig1_risk_effectiveness"),
    ("natcities_visual_items/figures/fig2_distribution.png", "nc_fig2_distribution"),
    ("natcities_visual_items/figures/fig3_synergies.png", "nc_fig3_synergies"),
    ("natcities_visual_items/figures/exemplar_amsterdam.png", "nc_exemplar_amsterdam"),
    ("natcities_visual_items/figures/exemplar_budapest.png", "nc_exemplar_budapest"),
    ("natcities_visual_items/figures/exemplar_palermo.png", "nc_exemplar_palermo"),
]

LOGO_SOURCE = "logo_urbadapt.png"


def optimize(src: Path, dest: Path, max_width: int = MAX_WIDTH) -> None:
    """Downscale to max_width and re-encode as WebP."""
    with Image.open(src) as im:
        im = im.convert("RGBA")
        # Flatten onto white: publication figures are drawn on a white canvas,
        # and a transparent background reads as black in dark mode.
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[3])
        im = flat
        if im.width > max_width:
            height = round(im.height * max_width / im.width)
            im = im.resize((max_width, height), Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)

    before = src.stat().st_size / 1024
    after = dest.stat().st_size / 1024
    print(f"  {dest.name:<34} {before:>8.0f} KB -> {after:>7.0f} KB")


def make_logo_assets(src: Path) -> None:
    """Build transparent header/hero logos and a favicon from the source logo.

    The source logo sits on an opaque white background, which shows as a white
    block against the navy header bar, so we key out the white and trim.
    """
    with Image.open(src) as im:
        rgba = im.convert("RGBA")

    # Key out near-white pixels.
    pixels = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            if r > 244 and g > 244 and b > 244:
                pixels[x, y] = (r, g, b, 0)

    trimmed = rgba.crop(rgba.getbbox())

    # Full lockup (emblem + wordmark) for the landing hero.
    hero = trimmed.copy()
    hero.thumbnail((640, 640), Image.LANCZOS)
    hero.save(ASSETS / "logo_urbadapt.png", "PNG", optimize=True)
    print(f"  {'logo_urbadapt.png':<34} hero lockup {hero.width}x{hero.height}")

    # Emblem only for the header and favicon — the site name already renders
    # the "URBADAPT" wordmark next to it, so the lockup would read twice.
    #
    # The wordmark occupies roughly the bottom quarter of the lockup.
    mark = trimmed.crop((0, 0, trimmed.width, int(trimmed.height * 0.72)))
    mark = mark.crop(mark.getbbox())

    header = mark.copy()
    header.thumbnail((256, 256), Image.LANCZOS)
    header.save(ASSETS / "logo_mark.png", "PNG", optimize=True)
    print(f"  {'logo_mark.png':<34} header mark {header.width}x{header.height}")

    # Square favicon, emblem centred on a transparent canvas.
    side = max(mark.width, mark.height)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
    square = square.resize((180, 180), Image.LANCZOS)
    square.save(ASSETS / "favicon.png", "PNG", optimize=True)
    print(f"  {'favicon.png':<34} 180x180")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=str(SITE_ROOT.parent / "URBADAPT-HEAT"),
        help="Path to a local URBADAPT-HEAT checkout (default: sibling directory)",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not (source / "urban-heat").is_dir():
        return fail(f"{source} does not look like an URBADAPT-HEAT checkout")

    print(f"Importing assets from {source}\n")

    logo = source / LOGO_SOURCE
    if not logo.is_file():
        return fail(f"missing {LOGO_SOURCE} in {source}")
    print("Branding:")
    make_logo_assets(logo)

    print("\nFigures:")
    missing = []
    for rel, stem in FIGURE_SOURCES:
        src = source / rel
        if not src.is_file():
            missing.append(rel)
            continue
        optimize(src, FIGURES / f"{stem}.webp")

    if missing:
        print(
            "\nWARNING: not imported (are you on the `reporting` branch of "
            "URBADAPT-HEAT?):",
            file=sys.stderr,
        )
        for rel in missing:
            print(f"  - {rel}", file=sys.stderr)
        return 1

    total = sum(p.stat().st_size for p in FIGURES.glob("*.webp")) / 1024 / 1024
    print(f"\nDone. {len(FIGURE_SOURCES)} figures, {total:.1f} MB total.")
    return 0


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
