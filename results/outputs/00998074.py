import cadquery as cq

# Parameters
circle_d = 0.358436
circle_r = circle_d / 2.0

rect_len = 0.192347
rect_w = 0.592709
rect_h = 7.0 * rect_w
overlap = 0.02193
hole_d = 0.052367
hole_offset = 0.048552
thickness = 0.029536

# Circle center at origin. Rectangle at right edge of circle.
rect_left = circle_r - overlap
rect_center_x = rect_left + rect_len / 2.0
rect_bottom = -circle_r
rect_center_y = rect_bottom + rect_h / 2.0

# Build circle solid
circle_body = cq.Workplane("XY").circle(circle_r).extrude(thickness)

# Build rectangle solid
rect_body = (
    cq.Workplane("XY")
    .center(rect_center_x, rect_center_y)
    .rect(rect_len, rect_h)
    .extrude(thickness)
)

# Union the two solids
body = circle_body.union(rect_body)

# Hole near top edge of rectangle
hole_x = rect_center_x
hole_y = rect_bottom + rect_h - hole_offset
body = (
    body.faces(">Z").workplane()
    .center(hole_x, hole_y)
    .hole(hole_d)
)

result = body
