import cadquery as cq
import math

L = 0.75
W = 0.1875
H = 0.00391
D = 0.12512

result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .hole(D)
)

vol = L * W * H - math.pi * (D / 2) ** 2 * H
