import cadquery as cq
import math

outer_d = 0.85714
inner_d = 0.535714
h = 0.75

outer_r = outer_d / 2.0
inner_r = inner_d / 2.0

result = (
    cq.Workplane("XY")
    .circle(outer_r)
    .extrude(h)
    .faces(">Z")
    .workplane()
    .hole(inner_d)
)

volume = math.pi * (outer_r**2 - inner_r**2) * h
