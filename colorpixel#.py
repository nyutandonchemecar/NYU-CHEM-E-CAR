# pip install pillow numpy
from PIL import ImageGrab
import numpy as np
from datetime import datetime

def count_white_pixels(tolerance: int = 0, save_png: bool = True) -> None:
    """
    Take a screenshot, count white (or nearly white) pixels, and print a summary.

    tolerance: 0 counts only pure white (255,255,255).
               e.g., 10 counts pixels with R,G,B >= 245 as white.
    save_png : save the screenshot as a PNG with a timestamped filename.
    """
    # Grab the whole screen
    img = ImageGrab.grab()  # works on Windows/macOS/Linux (with X11)
    arr = np.asarray(img)

    # Drop alpha channel if present
    rgb = arr[..., :3]

    # Build mask for white (or near white) pixels
    if tolerance <= 0:
        white_mask = np.all(rgb == 255, axis=2)
    else:
        thr = 255 - int(tolerance)
        white_mask = np.all(rgb >= thr, axis=2)

    white_pixels = int(white_mask.sum())
    total_pixels = int(rgb.shape[0] * rgb.shape[1])
    pct = 100.0 * white_pixels / total_pixels

    if save_png:
        fname = f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
        img.save(fname)

    print(f"White pixels: {white_pixels:,} / {total_pixels:,} "
          f"({pct:.2f}%)  | tolerance={tolerance}")

if __name__ == "__main__":
    # Change tolerance to count "almost white" pixels as white
    count_white_pixels(tolerance=0, save_png=True)

