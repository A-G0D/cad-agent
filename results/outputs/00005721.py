import cadquery as cq

# Obtuse scalene triangle: length 1.5 (base), width 0.73113 (height)
# Apex oriented upwards, centered
L = 1.5
W = 0.73113
H = 0.00472

# Triangle vertices (base along X, apex up), centered on centroid-ish
# Base from -L/2 to L/2, apex at (apex_x, W) with apex_x placing it scalene
# Use apex_x = 0.3*L to make it scalene/obtuse
apex_x = 0.3 * L

pts = [(-L/2, 0), (L/2, 0), (apex_x, W)]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(H)
)
