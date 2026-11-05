"""Shared design parameters for the piano roll cutter.

Every part imports from here, so changing ROLL (or a clearance) and
re-running the part scripts regenerates the whole machine.
All lengths are in millimetres; imperial source values are converted
with the IN constant so the original spec stays readable.
"""

from dataclasses import dataclass
from typing import Optional

IN = 25.4  # mm per inch


# ---------------------------------------------------------------------------
# Roll formats
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RollFormat:
    name: str
    paper_width: float          # mm
    holes_per_inch: int
    track_count: int            # note tracks the edge offset is derived from
    min_hole_width: float       # mm
    # Drive (take-up) end of the spool.
    drive_style: str            # "socket" or "pins"
    drive_socket_dia: Optional[float] = None
    drive_socket_depth: Optional[float] = None
    drive_slot_min: Optional[tuple] = None  # (width, length) mm

    @property
    def hole_pitch(self) -> float:
        """Centre-to-centre spacing between adjacent tracks, mm."""
        return IN / self.holes_per_inch

    @property
    def edge_offset(self) -> float:
        """Paper edge to first track centre, mm.

        Derived by centring track_count tracks on the paper; not a
        published figure, so check it against a real roll.
        """
        span = (self.track_count - 1) * self.hole_pitch
        return (self.paper_width - span) / 2


ROLL_88 = RollFormat(
    name="88-note",
    paper_width=11.25 * IN,
    holes_per_inch=9,
    track_count=88,              # edge offset ~0.792 in
    min_hole_width=0.0595 * IN,
    drive_style="socket",
    drive_socket_dia=7 / 16 * IN,
    drive_socket_depth=5 / 16 * IN,
    drive_slot_min=(1 / 8 * IN, 1 / 4 * IN),
)

ROLL_65 = RollFormat(
    name="65-note",
    paper_width=11.25 * IN,
    holes_per_inch=6,
    track_count=65,              # edge offset ~0.29 in
    min_hole_width=0.0595 * IN,
    drive_style="pins",          # protruding pins: needs a swappable drive dog
    # Pin dimensions still to be measured from a real 65-note spool.
)

# The one switch for the whole machine.
ROLL = ROLL_88


# ---------------------------------------------------------------------------
# Bearings on hand
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Bearing:
    name: str
    bore: float     # mm
    od: float       # mm
    width: float    # mm


BEARING_608 = Bearing("608 (skateboard)", bore=8.0, od=22.0, width=7.0)
BEARING_MR106 = Bearing("MR106ZZ", bore=6.0, od=10.0, width=3.0)


# ---------------------------------------------------------------------------
# FDM print tolerances (tune after printing parts/bearing_test_fit.py)
# ---------------------------------------------------------------------------

PRESS_FIT = -0.10   # added to bearing OD for a press-fit seat, mm
SLIDE_FIT = 0.20    # clearance for parts that must slide or rotate, mm
HOLE_COMP = 0.15    # extra diameter added to printed holes, mm
