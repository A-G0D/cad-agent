import cadquery as cq
import math

R = 0.75
H = 0.375
r_center = 0.1875 / 2
r_small = 0.1125 / 2
offset = 0.24375

body = cq.Workplane("XY").circle(R).extrude(H)

body = body.faces(">Z").workplane().hole(2 * r_center)

pts = []
for i in range(3):
    a = math.radians(90 + i * 120)
    pts.append((offset * math.cos(a), offset * math.sin(a)))

body = (
    body.faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(2 * r_small)
)

vol = math.pi * (R * R * H - r_center * r_center * H - 3 * r_small * r_small * H)
result = body
