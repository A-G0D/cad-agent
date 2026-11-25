import cadquery as cq
import math

L = 1.16102
W = 0.0729
H = 1.5
d = 0.072899
r = d / 2.0

x_left = -L/2.0 + 0.252909
x_right = L/2.0 - 0.127776
z_hole = H/2.0 - 0.595655

plate = cq.Workplane("XY").box(L, W, H, centered=(True, True, True))
result = (
    plate.faces(">Y").workplane(origin=(0, 0, 0))
    .pushPoints([(x_left, z_hole), (x_right, z_hole)])
    .hole(d)
)
result = result.clean()

vol = L*W*H - 2.0*math.pi*r*r*W
