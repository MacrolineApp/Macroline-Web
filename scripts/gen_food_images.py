#!/usr/bin/env python3
"""
Generate the 5 warm-refresh food photos via the OpenAI Images API and write
them over the placeholders in public/food/.

Key: reads OPENAI_API_KEY from the environment or from a gitignored
`.env.local` in the repo root. The key is never printed or committed.

Tries gpt-image-1 first; on access error falls back to dall-e-3. Hero is
requested portrait then center-cropped to 4:5; grid items are square 1:1.
Output sizes (1024 long edge) comfortably cover the rendered display sizes
at 2x DPR (hero ~380px, grid ~250px), so no fake upscaling.

Usage:  python scripts/gen_food_images.py
"""
import os, sys, json, base64, io, urllib.request, urllib.error
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "food"
OUT.mkdir(parents=True, exist_ok=True)

# --- key ---
key = os.environ.get("OPENAI_API_KEY")
if not key:
    envf = ROOT / ".env.local"
    if envf.exists():
        for line in envf.read_text().splitlines():
            if line.startswith("OPENAI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    sys.exit("OPENAI_API_KEY not set (env or .env.local). Aborting.")

SHARED = (
    "Bright, airy food photography in natural daylight. Fresh, appetizing, "
    "premium-but-approachable — modern healthy-eating brand, not a diet ad. "
    "Soft natural shadows, shallow depth of field, clean light surface (warm "
    "white oak, pale stone, or soft linen). Vibrant but natural color, no heavy "
    "filters, no text, no hands, minimal utensils. Slight top-down or 3/4 angle. "
    "Warm palette with fresh-green accents (matches a warm-white + emerald-green "
    "brand). Photorealistic, high detail, 35mm look. Avoid: dark moody "
    "backgrounds, clinical lighting, text/watermarks, plastic food, HDR "
    "oversaturation, busy backgrounds."
)

JOBS = [
    ("hero-salmon.jpg", "portrait", (4, 5),
     "A beautifully plated grilled salmon fillet with a vibrant green salad — "
     "baby spinach, avocado, cherry tomatoes — and a lemon wedge, on a pale "
     "ceramic plate, bright morning daylight from the left, fresh herbs "
     "scattered. Subject weighted to the upper-right with soft negative space "
     "in the lower-left. 4:5 vertical."),
    ("oats.jpg", "square", (1, 1),
     "Overnight oats in a clear glass jar topped with blueberries, raspberries, "
     "and a honey drizzle, on warm white oak, bright daylight, a few loose "
     "berries beside the jar. Top-down, centered, room at top-left for a label "
     "chip. 1:1."),
    ("salad.jpg", "square", (1, 1),
     "A big colorful grain salad bowl — kale, roasted sweet potato, chickpeas, "
     "red cabbage, cherry tomato, tahini drizzle — in light stoneware, vivid "
     "fresh colors, bright daylight, top-down centered. 1:1."),
    ("chicken.jpg", "square", (1, 1),
     "Grilled chicken breast sliced over fluffy rice with steamed broccoli and "
     "roasted peppers, pale plate, balanced 'meal-prep done right' look, bright "
     "daylight, 3/4 angle. 1:1."),
    ("smoothie.jpg", "square", (1, 1),
     "A green smoothie in a tall glass beside a small protein snack (almonds, a "
     "banana), spinach and a halved kiwi nearby, bright daylight, warm white "
     "surface, refreshing and energetic; the green echoes a fresh emerald brand "
     "accent. 1:1."),
]

def call_openai(model, prompt, size, want_b64_format):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    if want_b64_format:
        body["response_format"] = "b64_json"  # dall-e-3; gpt-image-1 is always b64
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    return base64.b64decode(data["data"][0]["b64_json"])

def crop_to(img, ratio):
    w, h = img.size
    tw, th = ratio
    target = tw / th
    cur = w / h
    if cur > target:  # too wide -> crop sides
        nw = int(h * target); x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(w / target); y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))

# Probe which model we can use (gpt-image-1 preferred).
USE = None
for model, size, fmt in (("gpt-image-1", "1024x1024", False), ("dall-e-3", "1024x1024", True)):
    try:
        call_openai(model, "a single ripe red apple on a white surface", size, fmt)
        USE = (model, fmt)
        print(f"using model: {model}")
        break
    except urllib.error.HTTPError as e:
        print(f"  {model} unavailable: {e.code} {e.read().decode()[:160]}")
if not USE:
    sys.exit("No usable OpenAI image model for this key.")
model, fmt = USE
PORTRAIT = "1024x1536" if model == "gpt-image-1" else "1024x1792"

for fname, shape, ratio, prompt in JOBS:
    size = PORTRAIT if shape == "portrait" else "1024x1024"
    print(f"generating {fname} ({size}) ...")
    raw = call_openai(model, f"{SHARED}\n\n{prompt}", size, fmt)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    if ratio != (1, 1):
        img = crop_to(img, ratio)
    img.save(OUT / fname, "JPEG", quality=86, optimize=True)
    print(f"  wrote {OUT / fname}  {img.size}")

print("done.")
