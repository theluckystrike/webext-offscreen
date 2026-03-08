#!/usr/bin/env python3
"""Create a social preview image for webext-offscreen"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
WIDTH = 1280
HEIGHT = 640
OUTPUT_PATH = "/Users/mike/zovo-workspaces/a22/webext-offscreen-temp/social-preview.png"

# Colors
BG_COLOR = (10, 10, 12)  # Near black
ACCENT_COLOR = (0, 255, 136)  # Electric green
SECONDARY_COLOR = (40, 45, 55)  # Dark gray
TEXT_COLOR = (255, 255, 255)
DIM_TEXT_COLOR = (120, 130, 145)

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Load fonts - use default if not available
font_path = "/Users/mike/.local/share/uv/tools/mini-agent/lib/python3.10/site-packages/mini_agent/skills/canvas-design/canvas-fonts/BricolageGrotesque-Bold.ttf"
large_font_path = "/Users/mike/.local/share/uv/tools/mini-agent/lib/python3.10/site-packages/mini_agent/skills/canvas-design/canvas-fonts/BigShoulders-Bold.ttf"

# Try to load custom fonts, fall back to default
try:
    title_font = ImageFont.truetype(large_font_path, 120)
    subtitle_font = ImageFont.truetype(font_path, 36)
    label_font = ImageFont.truetype(font_path, 24)
    small_font = ImageFont.truetype(font_path, 18)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw subtle grid pattern
for i in range(0, WIDTH, 40):
    draw.line([(i, 0), (i, HEIGHT)], fill=(20, 22, 26), width=1)
for i in range(0, HEIGHT, 40):
    draw.line([(0, i), (WIDTH, i)], fill=(20, 22, 26), width=1)

# Draw geometric accent shapes - left side
# Large rounded rectangle for document
doc_x, doc_y = 120, 120
doc_w, doc_h = 400, 420
draw.rounded_rectangle(
    [(doc_x, doc_y), (doc_x + doc_w, doc_y + doc_h)],
    radius=20,
    fill=SECONDARY_COLOR,
    outline=ACCENT_COLOR,
    width=3
)

# Document lines (representing code/text)
line_y = doc_y + 80
for _ in range(6):
    draw.line(
        [(doc_x + 40, line_y), (doc_x + doc_w - 40, line_y)],
        fill=(80, 90, 100),
        width=3
    )
    line_y += 45

# Window chrome at top of document
draw.rectangle(
    [(doc_x + 20, doc_y + 20), (doc_x + 50, doc_y + 35)],
    fill=(255, 80, 80)
)
draw.rectangle(
    [(doc_x + 60, doc_y + 20), (doc_x + 90, doc_y + 35)],
    fill=(255, 200, 80)
)
draw.rectangle(
    [(doc_x + 100, doc_y + 20), (doc_x + 130, doc_y + 35)],
    fill=(80, 200, 100)
)

# Floating elements - connection lines
# Dashed line from document to title
for i in range(doc_x + doc_w + 30, 550, 20):
    draw.line([(i, doc_y + 150), (i + 10, doc_y + 150)], fill=ACCENT_COLOR, width=2)

# Glowing orb accent
orb_x, orb_y = WIDTH - 180, 100
draw.ellipse(
    [(orb_x - 60, orb_y - 60), (orb_x + 60, orb_y + 60)],
    fill=None,
    outline=ACCENT_COLOR,
    width=3
)
draw.ellipse(
    [(orb_x - 40, orb_y - 40), (orb_x + 40, orb_y + 40)],
    fill=None,
    outline=ACCENT_COLOR,
    width=2
)

# Secondary orbs
for i, (ox, oy) in enumerate([(WIDTH - 100, HEIGHT - 80), (WIDTH - 250, HEIGHT - 120)]):
    draw.ellipse(
        [(ox - 15, oy - 15), (ox + 15, oy + 15)],
        fill=None,
        outline=DIM_TEXT_COLOR,
        width=2
    )

# Main title - "webext-offscreen"
title = "webext-offscreen"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_w = title_bbox[2] - title_bbox[0]
title_x = 580
title_y = 180
draw.text((title_x, title_y), title, font=title_font, fill=TEXT_COLOR)

# Subtitle
subtitle = "Typed offscreen documents for Chrome MV3"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
draw.text((title_x, title_y + 140), subtitle, font=subtitle_font, fill=DIM_TEXT_COLOR)

# Feature tags on the right side
tags = [
    ("DOM Parsing", True),
    ("Canvas", True),
    ("Audio", True),
    ("Clipboard", True),
    ("Web Workers", True),
]

tag_y = title_y + 220
for tag, is_accent in tags:
    # Tag background
    tag_w = len(tag) * 16 + 30
    draw.rounded_rectangle(
        [(title_x, tag_y), (title_x + tag_w, tag_y + 40)],
        radius=8,
        fill=(30, 35, 45) if not is_accent else (0, 50, 35),
        outline=ACCENT_COLOR if is_accent else (60, 70, 85),
        width=1
    )
    # Tag text
    draw.text((title_x + 15, tag_y + 8), tag, font=label_font, fill=ACCENT_COLOR if is_accent else (100, 110, 125))
    tag_y += 55

# Bottom bar with Zovo branding
bar_y = HEIGHT - 70
draw.rectangle([(0, bar_y), (WIDTH, HEIGHT)], fill=(8, 8, 10))

# Left: "Part of @zovo/webext"
draw.text((40, bar_y + 20), "Part of", font=small_font, fill=DIM_TEXT_COLOR)
draw.text((120, bar_y + 18), "@zovo/webext", font=label_font, fill=ACCENT_COLOR)

# Right: Zovo logo text
zovo_text = "zovo.one"
zovo_bbox = draw.textbbox((0, 0), zovo_text, font=label_font)
zovo_w = zovo_bbox[2] - zovo_bbox[0]
draw.text((WIDTH - zovo_w - 40, bar_y + 18), zovo_text, font=label_font, fill=TEXT_COLOR)

# Small accent line under zovo
draw.line(
    [(WIDTH - zovo_w - 40, bar_y + 52), (WIDTH - 40, bar_y + 52)],
    fill=ACCENT_COLOR,
    width=2
)

# Save image
img.save(OUTPUT_PATH, "PNG", quality=95)
print(f"Social preview saved to {OUTPUT_PATH}")
