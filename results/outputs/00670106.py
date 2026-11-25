import cadquery as cq
import math

d = 1.5
h = 0.440903
r = d / 2.0

result = (
    cq.Workplane("YZ")
    .circle(r)
    .extrude(h)
)

volume = math.pi * r * r * h
