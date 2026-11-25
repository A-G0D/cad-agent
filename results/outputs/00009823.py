import cadquery as cq

side = 1.5
height = 0.016238

result = (
    cq.Workplane("XY")
    .polygon(6, side * 2)
    .extrude(height)
)
