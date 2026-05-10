#!/usr/bin/env python3
"""Render code/og-image.png (1200x630) for Open Graph + Twitter Card.

Pillow-only — no rsvg/cairo required. Uses bundled DejaVu fonts that ship
with Debian's fontconfig (matches the container baseline).
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "code" / "og-image.png"

W, H = 1200, 630

BG = (11, 16, 32)            # #0b1020
PANEL = (14, 20, 36)          # #0e1424
BORDER = (30, 39, 64)         # #1e2740
TEXT = (230, 236, 255)        # #e6ecff
DIM = (138, 147, 184)         # #8a93b8
ACCENT = (120, 220, 232)      # #78dce8 (cyan — JSON, types)
ACCENT2 = (199, 146, 234)     # #c792ea (purple — TypeScript, kw)
GOOD = (166, 227, 161)        # #a6e3a1 (strings)
ORANGE = (224, 164, 88)       # #e0a458 (primitives/numbers)


def _load_font(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont:
    last_err: Exception | None = None
    for path, size in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError as e:  # pragma: no cover
            last_err = e
            continue
    raise RuntimeError(f"no usable font found: {last_err}")


def font_sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return _load_font(
        [
            (f"/usr/share/fonts/truetype/liberation/{name}", size),
            (f"/usr/share/fonts/liberation/{name}", size),
        ]
    )


def font_mono(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "LiberationMono-Bold.ttf" if bold else "LiberationMono-Regular.ttf"
    return _load_font(
        [
            (f"/usr/share/fonts/truetype/liberation/{name}", size),
            (f"/usr/share/fonts/liberation/{name}", size),
        ]
    )


def draw_runs(draw: ImageDraw.ImageDraw, x: int, y: int, runs, font) -> None:
    """runs = [(text, color), ...] drawn left-to-right starting at (x, y)."""
    cursor = x
    for text, color in runs:
        draw.text((cursor, y), text, fill=color, font=font)
        bbox = draw.textbbox((cursor, y), text, font=font)
        cursor = bbox[2]


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Subtle vignette band — solid bg keeps it clean across mail-client previews.

    # Title row: JSON → TypeScript
    title_font = font_mono(96, bold=True)
    draw_runs(
        d,
        80,
        90,
        [
            ("JSON", ACCENT),
            (" → ", DIM),
            ("TypeScript", ACCENT2),
        ],
        title_font,
    )

    # Tagline + sub-tagline
    d.text((80, 220), "paste JSON, get TS types instantly", fill=TEXT, font=font_sans(36))
    d.text(
        (80, 270),
        "runs in your browser  ·  no signup  ·  no upload",
        fill=DIM,
        font=font_sans(24),
    )

    # Two-pane mockup
    pane_y = 330
    pane_h = 230
    left_x, left_w = 80, 480
    right_x, right_w = 640, 480

    for px, pw in [(left_x, left_w), (right_x, right_w)]:
        d.rounded_rectangle(
            [(px, pane_y), (px + pw, pane_y + pane_h)],
            radius=14,
            fill=PANEL,
            outline=BORDER,
            width=2,
        )

    label_font = font_mono(15, bold=True)
    d.text((left_x + 18, pane_y + 14), "JSON INPUT", fill=DIM, font=label_font)
    d.text((right_x + 18, pane_y + 14), "TYPESCRIPT OUTPUT", fill=DIM, font=label_font)

    code_font = font_mono(22)
    code_font_bold = font_mono(22, bold=True)

    # Left pane — JSON sample
    base_x = left_x + 24
    base_y = pane_y + 60
    line_h = 30
    d.text((base_x, base_y + 0 * line_h), "{", fill=TEXT, font=code_font)
    draw_runs(
        d,
        base_x + 24,
        base_y + 1 * line_h,
        [('"id"', GOOD), (": ", TEXT), ("1", ORANGE), (",", DIM)],
        code_font,
    )
    draw_runs(
        d,
        base_x + 24,
        base_y + 2 * line_h,
        [('"name"', GOOD), (": ", TEXT), ('"Alice"', GOOD), (",", DIM)],
        code_font,
    )
    draw_runs(
        d,
        base_x + 24,
        base_y + 3 * line_h,
        [('"posts"', GOOD), (": [{", DIM)],
        code_font,
    )
    draw_runs(
        d,
        base_x + 48,
        base_y + 4 * line_h,
        [('"title"', GOOD), (": ", TEXT), ('"hi"', GOOD)],
        code_font,
    )
    d.text((base_x + 24, base_y + 5 * line_h), "}]", fill=DIM, font=code_font)
    d.text((base_x, base_y + 6 * line_h - 2), "}", fill=TEXT, font=code_font)

    # Arrow between panes
    arrow_font = font_mono(76, bold=True)
    d.text((565, pane_y + 80), "→", fill=ACCENT, font=arrow_font)

    # Right pane — TypeScript output
    base_rx = right_x + 24
    base_ry = pane_y + 60
    draw_runs(
        d,
        base_rx,
        base_ry + 0 * line_h,
        [("interface", ACCENT2), (" ", TEXT), ("Root", ACCENT), (" {", DIM)],
        code_font_bold,
    )
    draw_runs(
        d,
        base_rx + 24,
        base_ry + 1 * line_h,
        [("id", TEXT), (": ", DIM), ("number", ORANGE), (";", DIM)],
        code_font,
    )
    draw_runs(
        d,
        base_rx + 24,
        base_ry + 2 * line_h,
        [("name", TEXT), (": ", DIM), ("string", ORANGE), (";", DIM)],
        code_font,
    )
    draw_runs(
        d,
        base_rx + 24,
        base_ry + 3 * line_h,
        [("posts", TEXT), (": ", DIM), ("Post", ACCENT), ("[];", DIM)],
        code_font,
    )
    d.text((base_rx, base_ry + 4 * line_h), "}", fill=DIM, font=code_font)
    draw_runs(
        d,
        base_rx,
        base_ry + 5 * line_h,
        [
            ("interface", ACCENT2),
            (" ", TEXT),
            ("Post", ACCENT),
            (" { ", DIM),
            ("title", TEXT),
            (": ", DIM),
            ("string", ORANGE),
            ("; }", DIM),
        ],
        code_font_bold,
    )

    # Footer URL
    d.text(
        (80, 580),
        "json-to-ts-app.netlify.app",
        fill=ACCENT,
        font=font_mono(26, bold=True),
    )

    img.save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH.relative_to(ROOT)} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
