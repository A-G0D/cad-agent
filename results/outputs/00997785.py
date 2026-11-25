import cadquery as cq

hexagon = cq.Workplane("XY").polygon(6, 1.50001).extrude(0.409382)
square = (
    cq.Workplane("XY")
    .rect(0.867904, 0.867904)
    .extrude(0.272921)
    .rotate((0, 0, 0), (0, 0, 1), 45)
    .translate((0, 0, 0.409382))
)
result = hexagon.union(square)
