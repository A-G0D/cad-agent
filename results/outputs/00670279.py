import cadquery as cq

outer_d = 1.5
height = 0.26068
hole_d = outer_d - 2 * 0.013033

result = (
    cq.Workplane("XZ")
    .circle(outer_d / 2)
    .circle(hole_d / 2)
    .extrude(height)
)
