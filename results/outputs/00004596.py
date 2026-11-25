import cadquery as cq
import math

outer_d = 0.75
inner_d = 0.3125
length = 1.5

outer_r = outer_d / 2
inner_r = inner_d / 2

# Build as solid cylinder then bore the through hole (ensures round hole feature)
result = (
    cq.Workplane("YZ")
    .circle(outer_r)
    .extrude(length)
    .faces(">X")
    .workplane()
    .hole(inner_d)
)

# Volume: pi * (R^2 - r^2) * L
volume = math.pi * (outer_r**2 - inner_r**2) * length
