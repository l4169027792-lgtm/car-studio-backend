from io import BytesIO
from typing import Tuple

from PIL import Image, ImageFilter
from rembg import new_session, remove

MODEL_NAME = "u2netp"
MODEL_SESSION = new_session(MODEL_NAME)


def remove_background_from_bytes(image_bytes: bytes) -> Image.Image:
    """
    Remove the background from the provided image bytes using rembg.
    Returns a RGBA Pillow image.
    """
    output_bytes = remove(image_bytes, session=MODEL_SESSION)
    return Image.open(BytesIO(output_bytes)).convert("RGBA")


def add_shadow(
    foreground: Image.Image,
    shadow_offset: Tuple[int, int] = (40, 40),
    shadow_color=(0, 0, 0, 140),
    background_color=(255, 255, 255, 255),
    blur_radius: int = 30,
    padding: int = 60,
) -> Image.Image:
    """
    Apply a drop shadow to the provided RGBA image and place it on a background.

    Args:
        foreground: RGBA Pillow image.
        shadow_offset: (x, y) offset for the shadow relative to the foreground.
        shadow_color: RGBA color for the shadow.
        background_color: RGBA background color.
        blur_radius: Gaussian blur radius for the shadow softness.
        padding: Extra space around the image to give the shadow room.
    """
    fg = foreground.convert("RGBA")
    alpha = fg.split()[-1]

    shadow = Image.new("RGBA", fg.size, shadow_color)
    shadow.putalpha(alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    total_width = fg.width + abs(shadow_offset[0]) + padding * 2
    total_height = fg.height + abs(shadow_offset[1]) + padding * 2

    shadow_x = padding + max(shadow_offset[0], 0)
    shadow_y = padding + max(shadow_offset[1], 0)
    fg_x = padding + max(-shadow_offset[0], 0)
    fg_y = padding + max(-shadow_offset[1], 0)

    canvas = Image.new("RGBA", (total_width, total_height), background_color)
    canvas.paste(shadow, (shadow_x, shadow_y), shadow)
    canvas.paste(fg, (fg_x, fg_y), fg)

    return canvas


def image_to_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
