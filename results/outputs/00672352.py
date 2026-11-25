import cadquery as cq
import math

L = 0.75
W = 0.375
H = 0.015611
D = 0.09375
P = 0.015625

result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .center(L/2 - D/2 - P, W/2 - D/2 - P)
    .hole(D)
)

vol = L * W * H - math.pi * (D/2)**2 * H
