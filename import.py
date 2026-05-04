"""One-shot: import + resize Repin portfolio images into ./images/."""
from pathlib import Path
from PIL import Image, ImageOps
import re

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

SRC = Path(r"C:\Users\Alla\Documents\2 -Финал Портфолио Репин")
DST = Path(__file__).parent / "images"
DST.mkdir(exist_ok=True)
MAX = 1800
QUALITY = 85
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}

def safe_name(stem: str) -> str:
    s = re.sub(r"[^\w\-]+", "_", stem.lower()).strip("_")
    return s or "image"

manifest = []
for p in sorted(SRC.iterdir()):
    if p.suffix.lower() not in EXTS:
        continue
    try:
        img = Image.open(p)
        img = ImageOps.exif_transpose(img)
        w, h = img.size
        if max(w, h) > MAX:
            scale = MAX / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        img = img.convert("RGB")
        out = DST / f"{safe_name(p.stem)}.jpg"
        img.save(out, "JPEG", quality=QUALITY, optimize=True)
        manifest.append(out.name)
        print(f"  {out.name:<40} {out.stat().st_size:>10,} bytes  {img.size}")
    except Exception as e:
        print(f"  SKIPPED {p.name}: {e}")

print(f"\n{len(manifest)} images written to {DST}")
