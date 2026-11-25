import cadquery as cq

outer_d = 0.503822
outer_r = outer_d / 2
height = 0.75
inner_d = 0.426316
inner_r = inner_d / 2
inner_depth = 0.710526
rod_d = 0.05921
rod_r = rod_d / 2
rod_len = 0.631579
margin = 0.049342

# Outer cylinder
body = cq.Workplane("XY").circle(outer_r).extrude(height)

# Hollow pocket from top, not through
body = (
    body.faces(">Z").workplane()
    .circle(inner_r)
    .cutBlind(-inner_depth)
)

# Horizontal rod through the sides (along X)
rod_z = height - margin - rod_r
rod = (
    cq.Workplane("YZ")
    .center(0, rod_z)
    .circle(rod_r)
    .extrude(rod_len / 2, both=True)
)

body = body.cut(rod)

result = body
