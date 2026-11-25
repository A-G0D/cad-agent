import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(1.5, 0.83721, 0.07849, centered=(True, True, False))
)
