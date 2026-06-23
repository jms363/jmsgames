"""Generate the social/OG preview image (1200x630) for jmsgames.com.
Run: python assets/make_og.py  ->  writes assets/og.png
Regenerate this if the hub branding changes."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
BG = (10, 10, 18)
PURPLE = (168, 85, 247)
CYAN = (34, 211, 238)
PINK = (244, 114, 182)
DIM = (168, 168, 192)

FONTS = "C:/Windows/Fonts/"
title_font = ImageFont.truetype(FONTS + "consolab.ttf", 150)
sub_font = ImageFont.truetype(FONTS + "segoeui.ttf", 34)
cta_font = ImageFont.truetype(FONTS + "consolab.ttf", 40)

# --- background: radial-ish glow via large blurred blobs on dark base ---
img = Image.new("RGB", (W, H), BG)

glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([300, -260, 900, 220], fill=(40, 20, 70))      # purple top
gd.ellipse([850, -200, 1400, 200], fill=(10, 45, 60))     # cyan top-right
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.blend(img, glow, 0.9)

draw = ImageDraw.Draw(img)

# subtle grid
for x in range(0, W, 48):
    draw.line([(x, 0), (x, H)], fill=(22, 22, 34), width=1)
for y in range(0, H, 48):
    draw.line([(0, y), (W, y)], fill=(22, 22, 34), width=1)


def draw_glow_text(base, xy, text, font, fill, glow_color, anchor="mm", blur=18):
    """Draw text with a colored neon glow behind it."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text(xy, text, font=font, fill=glow_color + (255,), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.paste(Image.new("RGB", base.size, glow_color), (0, 0), layer)
    d = ImageDraw.Draw(base)
    d.text(xy, text, font=font, fill=fill, anchor=anchor)


# --- title: JMS GAMES (two-color) ---
cx, cy = W // 2, 250
jms = "JMS "
studios = "STUDIOS"
jms_w = draw.textlength(jms, font=title_font)
studios_w = draw.textlength(studios, font=title_font)
total = jms_w + studios_w
start = cx - total / 2
draw_glow_text(img, (start + jms_w / 2, cy), jms, title_font, (244, 244, 251), PURPLE, anchor="mm")
draw_glow_text(img, (start + jms_w + studios_w / 2, cy), studios, title_font, (244, 244, 251), CYAN, anchor="mm")

# --- subtitle ---
draw = ImageDraw.Draw(img)
draw.text((cx, 400), "Free web games. No download. Just press start.",
          font=sub_font, fill=DIM, anchor="mm")

# --- CTA accent ---
draw_glow_text(img, (cx, 500), "> PLAY NOW", cta_font, PINK, PINK, anchor="mm", blur=14)

out = os.path.join(os.path.dirname(__file__), "og.png")
img.save(out, "PNG")
print("wrote", out)
