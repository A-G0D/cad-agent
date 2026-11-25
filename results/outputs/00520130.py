import cadquery as cq

# Main rectangle: 1.05 (X) x 0.375 (Y), extruded 0.9 in +Z
main = cq.Workplane("XY").box(1.05, 0.375, 0.9, centered=(True, True, False))

# Two smaller rectangles 0.6 (X) x 0.15 (Y), height 0.9, protruding outward from left and right sides
# Left tab: attached to left face (x = -0.525), extends outward in -X
left_tab = (
    cq.Workplane("XY")
    .box(0.6, 0.15, 0.9, centered=(True, True, False))
    .translate((-0.525 - 0.3, 0, 0))
)

# Right tab: attached to right face (x = +0.525), extends outward in +X
right_tab = (
    cq.Workplane("XY")
    .box(0.6, 0.15, 0.9, centered=(True, True, False))
    .translate((0.525 + 0.3, 0, 0))
)

result = main.union(left_tab).union(right_tab)
