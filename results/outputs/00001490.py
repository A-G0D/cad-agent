import cadquery as cq
import math

R = 0.75
H = 0.48649
D = 0.243243243243244

result = (
    cq.Workplane("XY")
    .circle(R)
    .extrude(H)
    .faces(">Z")
    .workplane()
    .circle(D / 2)
    .cutThruAll()
)

vol = math.pi * (R * R - (D / 2) ** 2) * H
