import cadquery as cq

L = 0.25
W = 0.75
H = 0.02
D = 0.07
CH = 0.04

# Base plate: length along X, width along Y, height along Z
base = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Two cylinders on one end (near +X end), side by side along Y
r = D / 2
y_off = W / 4
x_pos = L / 2 - r - 0.02

cyl1 = cq.Workplane("XY").center(x_pos, y_off).circle(r).extrude(CH).translate((0, 0, H))
cyl2 = cq.Workplane("XY").center(x_pos, -y_off).circle(r).extrude(CH).translate((0, 0, H))

result = base.union(cyl1).union(cyl2)
