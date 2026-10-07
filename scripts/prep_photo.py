"""Preserve facial tones using gentle CLAHE; optional rembg has a safe fallback."""
from pathlib import Path
import argparse
import io
import warnings
import numpy as np
import cv2
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-rembg', action='store_true')
    args = parser.parse_args()
    image = ImageOps.exif_transpose(Image.open(ROOT/'assets/source-photo.png')).convert('RGBA')
    if not args.skip_rembg:
        try:
            from rembg import remove, new_session
            # Explicit lightweight model avoids changing rembg defaults / large downloads.
            image = remove(image, session=new_session('u2netp'))
        except Exception as exc:
            warnings.warn(f'Background removal unavailable ({type(exc).__name__}); retaining original.')
    canvas = Image.new('RGBA', image.size, 'white'); canvas.alpha_composite(image)
    gray = np.asarray(canvas.convert('L'))
    local = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8,8)).apply(gray)
    result = cv2.addWeighted(gray, .45, local, .55, 0)
    Image.fromarray(result).save(ROOT/'assets/source-prepped.png')
if __name__ == '__main__': main()
