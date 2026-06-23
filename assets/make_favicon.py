"""Generate the site favicons from the pixel font (Press Start 2P).
Run: python assets/make_favicon.py
Writes (at repo root):
  favicon.ico            multi-size raster (16/32/48/64), pixel "JMS" — works everywhere
  apple-touch-icon.png   180x180 for iOS/Android home screens
Regenerate if branding changes."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
PIXEL = os.path.join(HERE, "fonts", "PressStart2P-Regular.ttf")

BG = (10, 10, 18, 255)        # #0a0a12
PURPLE = (168, 85, 247, 255)  # #a855f7
TEXT = "JMS"


def fit_font(text, max_w):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    size = max_w
    while size > 4:
        f = ImageFont.truetype(PIXEL, size)
        if probe.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(PIXEL, 4)


def render(size, radius_ratio=0.19):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=255
    )
    img.paste(Image.new("RGBA", (size, size), BG), (0, 0), mask)
    f = fit_font(TEXT, max_w=int(size * 0.78))
    ImageDraw.Draw(img).text((size / 2, size / 2), TEXT, font=f, fill=PURPLE, anchor="mm")
    return img


# favicon.ico — render large then store the standard tab sizes
ico = render(64)
ico_path = os.path.join(ROOT, "favicon.ico")
ico.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("wrote", ico_path)

# apple-touch-icon — iOS prefers no transparency, so full-bleed tile
touch = render(180, radius_ratio=0.0)
touch_path = os.path.join(ROOT, "apple-touch-icon.png")
touch.convert("RGB").save(touch_path, "PNG")
print("wrote", touch_path)
