#!/usr/bin/env python3
"""Generate social preview image for webext-offscreen"""

from PIL import Image, ImageDraw, ImageFont
import os

# Dimensions
WIDTH = 1280
HEIGHT = 640

# Colors - Dark background with green accent
BG_COLOR = (18, 18, 24)  # Very dark blue-black
ACCENT_COLOR = (52, 211, 153)  # Bright green (Tailwind teal-400)
TEXT_COLOR = (255, 255, 255)  # White
SUBTEXT_COLOR = (160, 174, 192)  # Gray

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Create abstract geometric pattern - subtle grid lines
for i in range(0, WIDTH, 40):
    draw.line([(i, 0), (i, HEIGHT)], fill=(30, 30, 40), width=1)
for i in range(0, HEIGHT, 40):
    draw.line([(0, i), (WIDTH, i)], fill=(30, 30, 40), width=1)

# Draw large decorative circle in background
draw.ellipse([800, -200, 1200, 400], fill=(40, 40, 55), outline=None)
draw.ellipse([850, -150, 1150, 350], fill=(35, 35, 50), outline=None)

# Draw document/window icon - stylized
icon_x, icon_y = 150, 180
icon_w, icon_h = 280, 320

# Document shape
draw.rectangle([icon_x, icon_y, icon_x + icon_w, icon_y + icon_h], 
               fill=(30, 30, 40), outline=ACCENT_COLOR, width=4)

# Document fold corner
fold_size = 50
draw.polygon([
    (icon_x + icon_w - fold_size, icon_y),
    (icon_x + icon_w, icon_y + fold_size),
    (icon_x + icon_w - fold_size, icon_y + fold_size)
], fill=(25, 25, 35))

# Inner content lines representing code/text
line_y = icon_y + 80
line_widths = [180, 200, 160, 190, 170, 185, 150]
for lw in line_widths:
    draw.line([(icon_x + 30, line_y), (icon_x + 30 + lw, line_y)], 
              fill=ACCENT_COLOR if lw == line_widths[0] else SUBTEXT_COLOR, width=4)
    line_y += 35

# Glowing accent - vertical line
draw.line([(icon_x + icon_w + 60, 100), (icon_x + icon_w + 60, HEIGHT - 100)], 
          fill=ACCENT_COLOR, width=3)

# Main title
try:
    # Try to use a nice font
    title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
except:
    # Fallback to default
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Title text
title = "webext-offscreen"
subtitle = "Typed offscreen documents for Chrome MV3"
package = "@theluckystrike/webext-offscreen"

# Position text
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_w = title_bbox[2] - title_bbox[0]
title_x = 550
title_y = 200

draw.text((title_x, title_y), title, font=title_font, fill=TEXT_COLOR)

# Subtitle
draw.text((title_x, title_y + 85), subtitle, font=subtitle_font, fill=SUBTEXT_COLOR)

# Package name with accent
draw.text((title_x, title_y + 145), package, font=small_font, fill=ACCENT_COLOR)

# Bottom section - decorative dots
dot_y = HEIGHT - 80
for i in range(5):
    dot_x = 550 + i * 30
    draw.ellipse([dot_x, dot_y, dot_x + 8, dot_y + 8], fill=ACCENT_COLOR)

# Zovo logo text
draw.text((WIDTH - 180, HEIGHT - 50), "zovo.one", font=small_font, fill=SUBTEXT_COLOR)

# Save
output_path = os.path.join(os.path.dirname(__file__), "social-preview.png")
img.save(output_path, "PNG", quality=95)
print(f"Social preview saved to: {output_path}")
