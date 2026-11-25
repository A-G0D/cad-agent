import cadquery as cq

d = 0.955953
w = 0.295686
base = 0.163062
h = d - 0.698688

r = d / 2.0
# Isosceles trapezium with equal base/top lengths (rectangle) centered, top edge at y = r
# base/top length = base, height = h, cut from top of circle
y_bottom = r - h
y_top = r

# Build a rectangle (trapezium with base == top) representing the cut
cut = (
    cq.Workplane("XY")
    .rect(base, h)
    .extrude(w + 1.0)
    .translate((0, y_bottom + h / 2.0, -0.5))
)

cyl = cq.Workplane("XY").circle(r).extrude(w)
result = cyl.cut(cut).translate((0, w / 2.0, -0.272116))
