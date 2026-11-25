import cadquery as cq

height = 0.00656
outer_d = 1.5
inner_d = outer_d - 2 * 0.203459

result = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(height)
    .translate((0, 0, -height / 2))
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((height / 2, 0, 0))
)
