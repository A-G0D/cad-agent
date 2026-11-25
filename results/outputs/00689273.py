import cadquery as cq

# Cylinder: diameter 0.651607, width (height) 0.325804
cyl_d = 0.651607
cyl_h = 0.325804

# Rectangular block: width 0.201998, height 0.065161, length 0.839006
blk_w = 0.201998
blk_h = 0.065161
blk_l = 0.839006

# Cylinder centered at origin, sitting from z=0 to z=cyl_h
cyl = cq.Workplane("XY").circle(cyl_d / 2.0).extrude(cyl_h)

# Block centered on top of cylinder, raised slightly above top surface
# "slightly raised relative to the top surface" -> place block base at top of cylinder
blk = (
    cq.Workplane("XY")
    .box(blk_w, blk_l, blk_h)
    .translate((0, 0, cyl_h + blk_h / 2.0))
)

result = cyl.union(blk)
