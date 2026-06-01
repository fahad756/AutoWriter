"""
Generate autowriter.ico — multi-resolution Windows icon.
Uses manual ICO binary writing so it works across all Pillow versions.
"""
from PIL import Image, ImageDraw
import struct, io, os, sys


# ── Draw one frame ────────────────────────────────────────────────────────────

def _render(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    m  = max(1, round(size * 0.055))
    cr = max(2, round(size * 0.18))

    # Blue rounded-rectangle background
    d.rounded_rectangle([m, m, size - m - 1, size - m - 1], radius=cr, fill="#1355d4")

    if size <= 16:
        # Tiny: 2×2 white dots
        s = max(1, size // 7)
        for row in range(2):
            for col in range(2):
                x = round(size * (0.28 + col * 0.30))
                y = round(size * (0.30 + row * 0.30))
                d.ellipse([x, y, x + s, y + s], fill="white")
        return img

    # 3 rows × 4 key blocks
    kd = max(2, round(size * 0.105))
    kr = max(1, kd // 3)
    n_cols = 4 if size >= 48 else 3

    for ry in [round(size * y) for y in [0.26, 0.43, 0.60]]:
        for c in range(n_cols):
            x = round(size * (0.17 + c * 0.20))
            d.rounded_rectangle([x, ry, x + kd, ry + kd], radius=kr, fill="white")

    # Spacebar
    sb_y  = round(size * 0.77)
    sb_h  = max(2, round(size * 0.09))
    d.rounded_rectangle(
        [round(size * 0.24), sb_y, round(size * 0.76), sb_y + sb_h],
        radius=max(1, sb_h // 3), fill="white"
    )
    return img


# ── Multi-size ICO writer (manual, works on all Pillow versions) ──────────────

def _write_ico(images: list, path: str) -> None:
    """
    Write a list of RGBA PIL Images into a Windows .ico file.
    Each frame is stored as a PNG blob (Vista+ ICO format).
    """
    n = len(images)
    header   = struct.pack("<HHH", 0, 1, n)   # reserved=0, type=1 (icon), count
    dir_size = 6 + 16 * n                      # header + directory

    entries  = []
    blobs    = []
    offset   = dir_size

    for img in images:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        w, h = img.size

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png = buf.getvalue()
        blobs.append(png)

        # ICONDIRENTRY: w, h, colorCount, reserved, planes, bitCount, size, offset
        entries.append(struct.pack(
            "<BBBBHHII",
            w if w < 256 else 0,
            h if h < 256 else 0,
            0, 0,       # colorCount, reserved
            1, 32,      # planes, bits-per-pixel
            len(png),
            offset,
        ))
        offset += len(png)

    with open(path, "wb") as f:
        f.write(header)
        for e in entries:
            f.write(e)
        for b in blobs:
            f.write(b)


# ── Public entry point ────────────────────────────────────────────────────────

def generate(out_dir: str = None) -> str:
    out_dir = out_dir or os.path.dirname(os.path.abspath(__file__))
    out     = os.path.join(out_dir, "autowriter.ico")

    sizes  = [16, 24, 32, 48, 64, 128, 256]
    base   = _render(256)
    images = [base.resize((s, s), Image.LANCZOS) if s < 256 else base
              for s in sizes]

    _write_ico(images, out)
    print(f"  [OK] Icon saved: {out}  ({len(sizes)} sizes)")
    return out


if __name__ == "__main__":
    generate()
