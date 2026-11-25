import cadquery as cq

outer_r = 0.078575 / 2.0
inner_r = 0.058318 / 2.0
height = 0.75
cut_r = 0.078654 / 2.0

cyl = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)
    .extrude(height)
)

mid_z = height / 2.0
half_cyl = (
    cq.Workplane("XZ")
    .moveTo(0, mid_z)
    .lineTo(cut_r, mid_z)
    .threePointArc((0, mid_z + cut_r), (-cut_r, mid_z))
    .close()
    .extrude(0.078654)
    .translate((0, -0.078654 / 2.0, 0))
)

result = cyl.cut(half_cyl)
