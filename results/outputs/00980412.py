import cadquery as cq

base = 0.037173
height = 0.759401
thickness = 0.015931
wall = min(base, height) * 0.1

outer = (
    cq.Workplane("XY")
    .polyline([(0, 0), (base, 0), (0, height)])
    .close()
    .extrude(thickness)
)

inner = (
    cq.Workplane("XY")
    .polyline([(wall, wall), (base - wall, wall), (wall, height - wall)])
    .close()
    .extrude(thickness)
)

result = outer.cut(inner)
