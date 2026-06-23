"""Generate the social/OG preview image (1200x630) for jmsgames.com.
Run: python assets/make_og.py  ->  writes assets/og.png
Uses the site's pixel font (Press Start 2P, bundled in assets/fonts/).
Regenerate this if the hub branding changes."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(__file__)
PIXEL = os.path.join(HERE, "fonts", "PressStart2P-Regular.ttf")

W, H = 1200, 630
BG = (10, 10, 18)
PURPLE = (168, 85, 247)
CYAN = (34, 211, 238)
PINK = (244, 114, 182)
DIM = (168, 168, 192)
WHITE = (244, 244, 251)

sub_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 34)
cta_font = ImageFont.truetype(PIXEL, 30)


def fit_font(text, max_w, start=140):
    """Largest Press Start 2P size whose `text` fits within max_w."""
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    size = start
    while size > 10:
        f = ImageFont.truetype(PIXEL, size)
        if probe.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(PIXEL, 10)


# --- background: dark base + soft color glows + grid ---
img = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([300, -260, 900, 220], fill=(40, 20, 70))      # purple top
gd.ellipse([850, -200, 1400, 200], fill=(10, 45, 60))     # cyan top-right
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.blend(img, glow, 0.9)

draw = ImageDraw.Draw(img)
for x in range(0, W, 48):
    draw.line([(x, 0), (x, H)], fill=(22, 22, 34), width=1)
for y in range(0, H, 48):
    draw.line([(0, y), (W, y)], fill=(22, 22, 34), width=1)


def draw_glow_text(base, xy, text, font, fill, glow_color, anchor="mm", blur=20):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=glow_color + (255,), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.paste(Image.new("RGB", base.size, glow_color), (0, 0), layer)
    ImageDraw.Draw(base).text(xy, text, font=font, fill=fill, anchor=anchor)


# --- title lockup: JMS over STUDIOS (pixel font) ---
title_font = fit_font("STUDIOS", max_w=1000, start=130)
cx = W // 2
draw_glow_text(img, (cx, 200), "JMS", title_font, WHITE, PURPLE)
draw_glow_text(img, (cx, 330), "STUDIOS", title_font, WHITE, CYAN)

# --- subtitle (readable sans) + CTA (pixel) ---
draw = ImageDraw.Draw(img)
draw.text((cx, 460), "Free web games. No download. Just press start.",
          font=sub_font, fill=DIM, anchor="mm")
draw_glow_text(img, (cx, 540), "> PLAY NOW", cta_font, PINK, PINK, blur=14)

out = os.path.join(HERE, "og.png")
img.save(out, "PNG")
print("wrote", out)
