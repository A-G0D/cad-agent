import cadquery as cq

base = 0.95149
height = 0.15482
thickness = 0.11183

result = (
    cq.Workplane("XY")
    .polyline([(-base / 2, 0), (base / 2, 0), (0, height)])
    .close()
    .extrude(thickness)
)
