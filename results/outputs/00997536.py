import cadquery as cq

outer_d = 0.988192
height = 0.75
oct_d = 0.79436

result = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .polygon(8, oct_d, forConstruction=False)
    .cutThruAll()
)
