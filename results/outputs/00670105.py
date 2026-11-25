import cadquery as cq
import math

L = 0.477273
H = 0.2727275
B = 0.204545
W = 0.75

# Total pentagon height must be 0.477273; rectangle height H, so triangle height t = total - H
total_h = 0.477273
t = total_h - H

pts = [
    (0.0, 0.0),
    (L, 0.0),
    (L, H),
    (L/2.0, H + t),
    (0.0, H),
]

wp = cq.Workplane("XZ")
wp = wp.polyline(pts).close()
result = wp.extrude(W)
