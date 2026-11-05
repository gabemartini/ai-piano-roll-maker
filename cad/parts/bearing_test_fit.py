"""Test-fit coupon for the bearings on hand.

Prints one strip per bearing with seats at several offsets around the
nominal OD. Press each bearing in, find the seat that grips without
cracking, and copy that offset into PRESS_FIT in params.py.

Run:  python cad/parts/bearing_test_fit.py   (writes STEP + STL to cad/exports)
"""

from pathlib import Path
import sys

from build123d import (
    Align, Box, Cylinder, Pos, Text, export_step, export_stl, extrude,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from params import BEARING_608, BEARING_MR106, HOLE_COMP  # noqa: E402

OFFSETS = [-0.2, -0.1, 0.0, 0.1, 0.2]  # mm added to nominal OD
WALL = 3.0
FLOOR = 1.0
LABEL_H = 0.6


def coupon(bearing):
    pitch = bearing.od + WALL
    length = pitch * len(OFFSETS) + WALL
    width = bearing.od + 2 * WALL + 6  # room for labels
    height = bearing.width + FLOOR

    part = Box(length, width, height, align=(Align.MIN, Align.MIN, Align.MIN))
    cy = WALL + bearing.od / 2
    for i, off in enumerate(OFFSETS):
        cx = WALL + bearing.od / 2 + i * pitch
        # Bearing seat, open at the top, leaving a floor.
        part -= Pos(cx, cy, FLOOR) * Cylinder(
            (bearing.od + off) / 2, bearing.width,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        # Through hole for the shaft, so the bearing can be pushed out.
        part -= Pos(cx, cy, 0) * Cylinder(
            (bearing.bore + HOLE_COMP) / 2, FLOOR,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        # Engraved offset label.
        label = f"{off:+.1f}"
        text = Pos(cx, width - 3.5, height - LABEL_H) * Text(label, font_size=3.0)
        part -= extrude(text, LABEL_H)
    return part


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "exports"
    out.mkdir(exist_ok=True)
    for b, slug in [(BEARING_608, "608"), (BEARING_MR106, "mr106")]:
        p = coupon(b)
        export_step(p, str(out / f"bearing_test_fit_{slug}.step"))
        export_stl(p, str(out / f"bearing_test_fit_{slug}.stl"))
        print(f"{b.name}: volume {p.volume:.0f} mm^3")
