import cadquery as cq

L = 0.5
W = 0.5
H = 0.633333
cyl_h = 0.116667
cyl_d = 0.316667
cav_L = 0.411666
cav_W = 0.411666
cav_depth = 0.533333
recess = 0.05

block = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))
cyl = cq.Workplane("XY").workplane(offset=H).circle(cyl_d / 2).extrude(cyl_h)
solid = block.union(cyl)
cavity = (
    cq.Workplane("XY")
    .workplane(offset=recess)
    .rect(cav_L, cav_W)
    .extrude(cav_depth)
)
result = solid.cut(cavity)
