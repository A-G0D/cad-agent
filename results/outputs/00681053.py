import cadquery as cq
import math

L = 0.46077
W = 0.75
H = 0.048077

# Each cover is a flat plate of length L (along X), width W (along Y), thickness H (Z).
# Two covers meet at the spine (Y axis) forming an obtuse angle.
# To keep overall bbox = [L, 2W, H], lay covers flat side by side and only
# tilt them slightly so the total Z stays within H.
# Simplest valid interpretation: two flat plates joined at spine, coplanar,
# giving bbox [L, 2W, H] with a single shared edge at the spine.

right = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(False, True, False))
)
left = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(False, True, False))
    .translate((0, -W, 0))
)

result = right.union(left)
