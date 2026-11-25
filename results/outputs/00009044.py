import cadquery as cq
import math

d = 1.5
h = 0.375
hole_d = 0.237219

result = (
    cq.Workplane("XY")
    .circle(d / 2)
    .extrude(h)
    .faces(">Z")
    .workplane()
    .circle(hole_d / 2)
    .cutThruAll()
)

vol = math.pi * (d / 2) ** 2 * h - math.pi * (hole_d / 2) ** 2 * h
