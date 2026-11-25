import cadquery as cq

od = 0.533654
wall = 0.017308
h = 0.75
hole_d = 0.090144
hole_depth = 0.034616

outer_r = od / 2.0
inner_r = outer_r - wall

# Build the tube explicitly as outer cylinder minus inner bore (bottom closed)
outer = cq.Workplane("XY").circle(outer_r).extrude(h)
inner = cq.Workplane("XY").workplane(offset=hole_depth).circle(inner_r).extrude(h - hole_depth)
tube = outer.cut(inner)

# Tiny blind hole in the middle of the bottom face
result = (
    tube
    .faces("<Z")
    .workplane()
    .circle(hole_d / 2.0)
    .cutBlind(-hole_depth)
)
