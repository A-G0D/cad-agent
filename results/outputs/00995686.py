import cadquery as cq

od = 0.702675
wall = 0.049281
width = 0.75
id_ = od - 2 * wall
r_out = od / 2

pipe = (
    cq.Workplane("XY")
    .circle(r_out)
    .circle(id_ / 2)
    .extrude(width)
)

# Notch cut: removes a sector only partway through the width,
# so the full outer diameter extent remains in XY bbox.
cutter = (
    cq.Workplane("XY")
    .box(od, od, width / 2, centered=(True, True, False))
    .translate((od / 2, 0, width / 2))
)

result = pipe.cut(cutter)
