import cadquery as cq
import math

R = 0.18
Ri = 0.18 - 0.0075
angle = 360.0
n = 128

def sector_pts(radius):
    pts = [(0, 0)]
    for i in range(n + 1):
        a = math.radians(angle * i / n)
        pts.append((radius * math.cos(a), radius * math.sin(a)))
    return pts

outer = (
    cq.Workplane("XZ")
    .polyline(sector_pts(R))
    .close()
    .extrude(0.750037)
)

inner = (
    cq.Workplane("XZ")
    .polyline(sector_pts(Ri))
    .close()
    .extrude(0.750037)
)

result = outer.cut(inner)
result = result.translate((0.180047, -0.375015, 0))
result = result.rotate((0, 0, 0), (0, 0, 1), 180)
