import cadquery as cq
import math

outer_d = 1.5
hole_d = 0.93038
h = 0.09494

result = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .extrude(h)
    .faces(">Z")
    .workplane()
    .hole(hole_d)
)

vol = math.pi * ((outer_d / 2) ** 2 - (hole_d / 2) ** 2) * h
