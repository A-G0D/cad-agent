import cadquery as cq

L = 0.333333
W = 0.066667
H = 0.083333
R = 0.022222
CH = 0.666667

# Rectangle extruded upward from z=0
base = cq.Workplane("XY").box(L, W, H, centered=(False, True, False))

# Cylinder near one end (edge), protruding from top surface
# Total height from z=0 to top = CH
cx = L / 2.0
cyl = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(cx, 0)
    .circle(R)
    .extrude(CH)
)

result = base.union(cyl)
