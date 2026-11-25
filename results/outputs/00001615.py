import cadquery as cq

d = 0.6
h = 1.5
cut_len = 0.235
cut_w = 0.6
cut_h = 0.292

cyl = cq.Workplane("XY").circle(d / 2).extrude(h)

# Rectangular cut from top center, extending downward
cut = (
    cq.Workplane("XY")
    .box(cut_len, cut_w, cut_h, centered=(True, True, False))
    .translate((0, 0, h - cut_h))
)

result = cyl.cut(cut)
