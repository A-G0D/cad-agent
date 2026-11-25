import cadquery as cq

length = 1.5
width = 1.02857
height = 0.17143
hole_d = 0.095635
inset_l = 0.263507
inset_w = 0.219429

result = (
    cq.Workplane("XY")
    .box(length, width, height, centered=(False, False, False))
    .faces(">Z")
    .workplane()
    .pushPoints([
        (inset_l, inset_w),
        (length - inset_l, inset_w),
        (inset_l, width - inset_w),
        (length - inset_l, width - inset_w),
    ])
    .circle(hole_d / 2.0)
    .cutThruAll()
)
