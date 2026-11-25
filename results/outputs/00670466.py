import cadquery as cq

base = 0.150756
height = 1.5
thickness = 0.188445

pts = [(-base / 2, 0), (base / 2, 0), (0, height)]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)
