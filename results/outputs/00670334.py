import cadquery as cq
import math

L = 0.75
W = 0.4
H = 0.2375
D = 0.11875

result = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(H)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(D / 2)
    .cutThruAll()
)

volume = L * W * H - math.pi * (D / 2) ** 2 * H
