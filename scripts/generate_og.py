"""
Generate OG (Open Graph) images for Macroline social sharing.

Standard: 1200x630, optimized for Twitter/Facebook/iMessage/Slack previews.

Outputs:
- public/og.png            (default — homepage)
- public/og-features.png   (features page variant)
- public/og-pricing.png    (pricing page variant)
- public/og-blog.png       (blog default — overridden per-post via frontmatter)

Run: python scripts/generate_og.py
Requires: pip install Pillow
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public"
OUT.mkdir(parents=True, exist_ok=True)

# Brand
BG_TOP = (24, 36, 64)
BG_BOTTOM = (10, 16, 32)
PROTEIN = (249, 115, 22)
CARBS = (234, 179, 8)
FAT = (139, 92, 246)
TEXT = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
ACCENT = (96, 165, 250)

WIDTH, HEIGHT = 1200, 630


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        img.paste(lerp(top, bottom, t), (0, y, w, y + 1))
    return img.convert("RGBA")


def vertical_bar(w, h, color, radius):
    bottom = lerp(color, (0, 0, 0), 0.28)
    grad = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.paste(lerp(color, bottom, t), (0, y, w, y + 1))
    grad = grad.convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    md.rectangle((0, h - radius, w, h), fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Best-effort: Inter -> Segoe UI -> Helvetica -> system default."""
    candidates = [
        "Inter-Bold.ttf" if bold else "Inter-Regular.ttf",
        "InterDisplay-Bold.ttf" if bold else "InterDisplay-Regular.ttf",
        "segoeui.ttf" if not bold else "segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf" if not bold else "C:/Windows/Fonts/segoeuib.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def draw_bar_chart_icon(img: Image.Image, x: int, y: int, size: int) -> None:
    """Mini bar-chart icon — same design as the app icon."""
    grad = vertical_gradient(size, size, BG_TOP, BG_BOTTOM)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, size, size), radius=int(size * 0.22), fill=255)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(grad, (0, 0), mask)

    # Bars
    bar_w = int(size * 0.16)
    cluster_w = int(size * 0.62)
    gap = (cluster_w - 3 * bar_w) // 2
    cluster_x = (size - cluster_w) // 2
    baseline_y = int(size * 0.78)
    max_h = int(size * 0.58)
    radius = bar_w // 2
    heights = (0.62, 1.00, 0.78)
    colors = (PROTEIN, CARBS, FAT)
    for i, (hp, color) in enumerate(zip(heights, colors)):
        h = int(max_h * hp)
        bx = cluster_x + i * (bar_w + gap)
        by = baseline_y - h
        bar = vertical_bar(bar_w, h, color, radius)
        bg.paste(bar, (bx, by), bar)
    # Baseline
    d = ImageDraw.Draw(bg)
    line_w = max(2, int(size * 0.005))
    line_inset = int(size * 0.04)
    d.rectangle(
        (cluster_x - line_inset, baseline_y, cluster_x + cluster_w + line_inset, baseline_y + line_w),
        fill=(120, 130, 160, 90),
    )
    img.paste(bg, (x, y), bg)


def make_og(headline: str, subhead: str, eyebrow: str | None = None) -> Image.Image:
    img = vertical_gradient(WIDTH, HEIGHT, BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    # Soft accent glow in top-right
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((WIDTH - 600, -200, WIDTH + 100, 400), fill=(96, 165, 250, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=120))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)

    # Icon top-left
    icon_size = 88
    margin_x, margin_y = 64, 56
    draw_bar_chart_icon(img, margin_x, margin_y, icon_size)

    # Wordmark next to icon
    wordmark_font = find_font(40, bold=True)
    d.text((margin_x + icon_size + 18, margin_y + 22), "macroline", fill=TEXT, font=wordmark_font)

    # Eyebrow (optional small text above headline)
    text_x = margin_x
    text_y = 220
    if eyebrow:
        eyebrow_font = find_font(22, bold=True)
        d.text((text_x, text_y), eyebrow.upper(), fill=ACCENT, font=eyebrow_font)
        text_y += 36

    # Headline
    headline_font = find_font(72, bold=True)
    d.text((text_x, text_y), headline, fill=TEXT, font=headline_font)

    # Subhead — wrap manually at ~50 chars
    subhead_font = find_font(28)
    sub_y = text_y + 110
    line_h = 38
    words = subhead.split()
    line, lines = [], []
    for w in words:
        line.append(w)
        if len(" ".join(line)) > 60:
            line.pop()
            lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    for i, ln in enumerate(lines[:3]):
        d.text((text_x, sub_y + i * line_h), ln, fill=TEXT_MUTED, font=subhead_font)

    # URL bottom-right
    url_font = find_font(22, bold=True)
    url_text = "macroline.app"
    bbox = d.textbbox((0, 0), url_text, font=url_font)
    url_w = bbox[2] - bbox[0]
    d.text((WIDTH - url_w - margin_x, HEIGHT - 56), url_text, fill=TEXT_MUTED, font=url_font)

    return img


VARIANTS = {
    "og.png": ("Just say what you ate.", "AI-native macro tracking with verified sources. Built for the AI era.", None),
    "og-features.png": ("Built for honesty.", "Every food has a verified source. Every number is sourced.", "Features"),
    "og-pricing.png": ("$4.99 a month. No nags.", "Free tier with everything that matters. Pro unlocks AI input + Claude integration.", "Pricing"),
    "og-blog.png": ("The Macroline Blog", "Notes on AI macro tracking, GLP-1, and food data done right.", "Blog"),
}


def main():
    print("Generating OG images...")
    for filename, (headline, sub, eyebrow) in VARIANTS.items():
        img = make_og(headline, sub, eyebrow).convert("RGB")
        img.save(OUT / filename, "PNG", optimize=True)
        print(f"  {filename}")
    print(f"Wrote to {OUT}")


if __name__ == "__main__":
    main()
