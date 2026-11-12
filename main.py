#!/usr/bin/env python3
"""Baby panda with bamboo - cutest-picture-01 entry.

Draws a 1024x1024 RGB PNG of a chubby baby panda sitting front-on, head
tilted 8 degrees, huge sparkling eyes, blush cheeks, a tiny bamboo sprig
behind the right ear and one clumsy paw holding a green bamboo stalk.
Warm cream background, one pale pink ground shadow. No text.

Pure Python standard library, deterministic: no clock, no network, no
unseeded randomness. Same bytes every run.
"""
import math
import os
import struct
import zlib

W = 1024
H = 1024

CREAM = (0xFF, 0xF6, 0xE9)
GROUND = (0xF3, 0xD9, 0xCF)
OUTLINE = (0xE3, 0xDC, 0xD2)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x1A, 0x1A, 0x1A)
BLUSH = (0xF6, 0xA8, 0xB8)
GREEN = (0x5B, 0xAE, 0x4A)
DGREEN = (0x4A, 0x9A, 0x3E)
LGREEN = (0x6F, 0xBF, 0x5A)

HEAD = (512, 420)
COS8 = math.cos(math.radians(8))
SIN8 = math.sin(math.radians(8))


def tilt(x, y):
    """Rotate a face-feature point around the head centre by 8 deg clockwise."""
    dx = x - HEAD[0]
    dy = y - HEAD[1]
    return (HEAD[0] + dx * COS8 - dy * SIN8,
            HEAD[1] + dx * SIN8 + dy * COS8)


# ---------------------------------------------------------------- canvas
rows = [bytearray(bytes(CREAM) * W) for _ in range(H)]


def span(y, x0, x1, color):
    """Fill a horizontal run of row y (inclusive, float bounds) with color."""
    if y < 0 or y >= H:
        return
    lo = max(0, int(math.ceil(x0)))
    hi = min(W - 1, int(math.floor(x1)))
    if hi < lo:
        return
    row = rows[y]
    row[lo * 3:(hi + 1) * 3] = bytes(color) * (hi - lo + 1)


def disc(cx, cy, r, color):
    y0 = max(0, int(math.ceil(cy - r)))
    y1 = min(H - 1, int(math.floor(cy + r)))
    r2 = r * r
    for y in range(y0, y1 + 1):
        dy = y - cy
        h = math.sqrt(max(0.0, r2 - dy * dy))
        span(y, cx - h, cx + h, color)


def ellipse(cx, cy, rx, ry, color):
    y0 = max(0, int(math.ceil(cy - ry)))
    y1 = min(H - 1, int(math.floor(cy + ry)))
    for y in range(y0, y1 + 1):
        t = (y - cy) / ry
        h = rx * math.sqrt(max(0.0, 1.0 - t * t))
        span(y, cx - h, cx + h, color)


def rot_ellipse(cx, cy, rx, ry, phi_deg, color):
    """Ellipse rotated by phi_deg (rotation of the rx-axis, clockwise in
    screen coordinates). Solved per row as a quadratic in x."""
    phi = math.radians(phi_deg)
    c = math.cos(phi)
    s = math.sin(phi)
    irx2 = 1.0 / (rx * rx)
    iry2 = 1.0 / (ry * ry)
    a = c * c * irx2 + s * s * iry2
    extent = math.sqrt(rx * rx * s * s + ry * ry * c * c)
    y0 = max(0, int(math.ceil(cy - extent)))
    y1 = min(H - 1, int(math.floor(cy + extent)))
    for y in range(y0, y1 + 1):
        dy = y - cy
        b = 2.0 * dy * s * c * (irx2 - iry2)
        cc = dy * dy * (s * s * irx2 + c * c * iry2) - 1.0
        det = b * b - 4.0 * a * cc
        if det < 0.0:
            continue
        sq = math.sqrt(det)
        span(y, cx + (-b - sq) / (2.0 * a), cx + (-b + sq) / (2.0 * a), color)


def rect(x0, y0, x1, y1, color):
    for y in range(max(0, int(math.ceil(y0))),
                   min(H, int(math.floor(y1)) + 1)):
        span(y, x0, x1, color)


def thick_line(x0, y0, x1, y1, width, color):
    """Short thick segment drawn as stamped discs along its length."""
    r = width / 2.0
    dist = math.hypot(x1 - x0, y1 - y0)
    steps = max(1, int(dist / max(1.0, r)) + 1)
    for i in range(steps + 1):
        t = i / steps
        disc(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, color)


def bezier_arc(p0, ctrl, p2, width, color):
    """Quadratic bezier arc stamped with discs (the smile)."""
    steps = 28
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = mt * mt * p0[0] + 2 * mt * t * ctrl[0] + t * t * p2[0]
        y = mt * mt * p0[1] + 2 * mt * t * ctrl[1] + t * t * p2[1]
        disc(x, y, width / 2.0, color)


# ---------------------------------------------------------------- drawing
# 2. Ground shadow
ellipse(512, 895, 310, 48, GROUND)

# 3. Bamboo sprig behind the right ear (tilted with the head group)
sx1, sy1 = tilt(668, 232)
sx2, sy2 = tilt(690, 248)
rot_ellipse(sx1, sy1, 20, 8, -25, LGREEN)
rot_ellipse(sx2, sy2, 20, 8, 20, LGREEN)
st0 = tilt(660, 255)
st1 = tilt(672, 235)
thick_line(st0[0], st0[1], st1[0], st1[1], 3, GREEN)

# 4. Body: grey outline ring, then white
ellipse(512, 700, 215, 195, OUTLINE)
ellipse(512, 700, 208, 188, WHITE)

# 5. Arms (tops lean outward)
rot_ellipse(335, 680, 52, 92, -18, BLACK)
rot_ellipse(689, 680, 52, 92, 18, BLACK)

# 6. Feet
ellipse(375, 875, 62, 38, BLACK)
ellipse(649, 875, 62, 38, BLACK)

# 7. Bamboo stalk held in the right paw (before the paws). Made wider and
# taller than the first pass so it reads as a stalk, not a sprout: the
# visible part above the paw is now ~120 px tall and 22 px wide, with
# bigger leaves, still a thin green accent against the white body.
rot_ellipse(588, 728, 26, 11, -30, LGREEN)
rot_ellipse(640, 732, 26, 11, 30, LGREEN)
rect(600, 728, 622, 850, GREEN)
rect(600, 778, 622, 784, DGREEN)

# 8. Front paws (right one ~7 px higher, holding the stalk)
ellipse(425, 845, 52, 38, BLACK)
ellipse(610, 838, 52, 38, BLACK)

# 9. Head: grey outline ring, then white
disc(512, 420, 190, OUTLINE)
disc(512, 420, 185, WHITE)

# 10. Ears (tilted with the head)
ex1, ey1 = tilt(380, 268)
ex2, ey2 = tilt(644, 268)
disc(ex1, ey1, 55, BLACK)
disc(ex2, ey2, 55, BLACK)

# 11. Eye patches (tall black ovals, long axis angled toward the nose at
# the bottom; head tilt adds 8 deg to each patch's own angle)
lp = tilt(440, 400)
rp = tilt(584, 400)
rot_ellipse(lp[0], lp[1], 42, 58, -15 + 8, BLACK)
rot_ellipse(rp[0], rp[1], 42, 58, 15 + 8, BLACK)

# 12. Eyes: white sclera, dark pupil, big highlight + small highlight
for (sx, sy, px, py) in ((440, 400, 440, 402), (584, 400, 584, 402)):
    sc = tilt(sx, sy)
    pc = tilt(px, py)
    h1 = tilt(sx - 6, sy - 5)
    h2 = tilt(sx + 7, sy + 8)
    ellipse(sc[0], sc[1], 26, 32, WHITE)
    disc(pc[0], pc[1], 16, BLACK)
    disc(h1[0], h1[1], 7, WHITE)
    disc(h2[0], h2[1], 3, WHITE)

# 13. Nose, philtrum, smile
nc = tilt(512, 470)
ellipse(nc[0], nc[1], 22, 16, BLACK)
ph0 = tilt(512, 486)
ph1 = tilt(512, 497)
thick_line(ph0[0], ph0[1], ph1[0], ph1[1], 3, BLACK)
sm0 = tilt(494, 498)
sm2 = tilt(530, 498)
dip = tilt(512, 510)
ctrl = (2 * dip[0] - 0.5 * (sm0[0] + sm2[0]),
        2 * dip[1] - 0.5 * (sm0[1] + sm2[1]))
bezier_arc(sm0, ctrl, sm2, 4, BLACK)

# 14. Blush cheeks
b1 = tilt(400, 470)
b2 = tilt(624, 470)
ellipse(b1[0], b1[1], 28, 16, BLUSH)
ellipse(b2[0], b2[1], 28, 16, BLUSH)


# ---------------------------------------------------------------- PNG out
_ABS = bytes(min(b, 256 - b) for b in range(256))


def _png():
    raw = bytearray()
    prev = bytes(W * 3)
    for row in rows:
        rb = bytes(row)
        if rb == prev:
            raw.append(2)
            raw.extend(b"\x00" * (W * 3))
            continue
        s_none = sum(rb.translate(_ABS))
        s_up = 0
        for a, b in zip(rb, prev):
            d = (a - b) & 0xFF
            s_up += d if d < 128 else 256 - d
        if s_up < s_none:
            raw.append(2)
            raw.extend((a - b) & 0xFF for a, b in zip(rb, prev))
        else:
            raw.append(0)
            raw.extend(rb)
        prev = rb
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(_png())


if __name__ == "__main__":
    main()
