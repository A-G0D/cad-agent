import cadquery as cq
import math

side = 0.929516
dia = 0.619677
h = 0.3

# Equilateral triangle, pointing downwards: apex at bottom, flat edge on top.
tri = (
    cq.Workplane("XY")
    .polyline([(0, 0), (side / 2, side * math.sqrt(3) / 2), (-side / 2, side * math.sqrt(3) / 2)])
    .close()
    .extrude(h)
)

# Semicircular cutout at the bottom corner: only the lower half of the circle,
# keeping the full triangle height intact.
semi = (
    cq.Workplane("XY")
    .moveTo(-dia / 2, 0)
    .threePointArc((0, -dia / 2), (dia / 2, 0))
    .close()
    .extrude(h)
)

result = tri.cut(semi)
