import cadquery as cq
import math

L = 0.21429
W = 0.75
H = 0.21429
r = 0.05371 / 2
pad = 0.048699

y1 = -W/2 + pad + r
y2 = W/2 - pad - r

result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .faces(">Z").workplane()
    .pushPoints([(0, y1), (0, y2)])
    .circle(r)
    .cutThruAll()
)

volume = L * W * H - 2 * math.pi * r**2 * H
