import cadquery as cq
import math

outer_d = 1.5
height = 0.381001
hole_d = 0.060198

result = (
    cq.Workplane("XY")
    .circle(outer_d/2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(hole_d/2)
    .cutThruAll()
)
