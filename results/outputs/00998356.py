import cadquery as cq

base = 1.19143
height = 0.85714
thickness = 0.085714
hole_d = 0.094286
fillet_r = 0.094286

# Isosceles triangle vertices (base centered at origin)
p_left = (-base / 2.0, 0.0)
p_right = (base / 2.0, 0.0)
p_top = (0.0, height)

# Build triangle
tri = (
    cq.Workplane("XY")
    .moveTo(p_left[0], p_left[1])
    .lineTo(p_right[0], p_right[1])
    .lineTo(p_top[0], p_top[1])
    .close()
)

body = tri.extrude(thickness)

# Fillet the two bottom vertical edges
def near(pt, target, tol=1e-3):
    return abs(pt.x - target[0]) < tol and abs(pt.y - target[1]) < tol

sel = []
for e in body.edges("|Z").vals():
    c = e.Center()
    if near(c, p_left) or near(c, p_right):
        sel.append(e)

if sel:
    body = body.newObject(sel).fillet(fillet_r).end()

# Cut off top corner with a flat edge near the top (small truncation)
cut_y = height - 0.05
cutter = (
    cq.Workplane("XY")
    .box(base * 2, base * 2, thickness * 2, centered=(True, True, False))
    .translate((0, cut_y + base, 0))
)
body = body.cut(cutter)

# Three small circular holes near each corner
inset = 0.12
left_hole_pos = (p_left[0] + inset, p_left[1] + inset)
right_hole_pos = (p_right[0] - inset, p_right[1] + inset)
top_hole_pos = (0.0, cut_y - inset)

for pos in [left_hole_pos, right_hole_pos, top_hole_pos]:
    body = (
        body.faces(">Z").workplane()
        .center(pos[0], pos[1])
        .hole(hole_d)
    )

# Rectangular notch from top flat edge
notch_w = 0.25
notch_d = 0.08
notch = (
    cq.Workplane("XY")
    .box(notch_w, notch_d * 2, thickness * 2, centered=(True, True, False))
    .translate((0, cut_y, 0))
)
body = body.cut(notch)

# Cylindrical hole near base center
base_hole_d = 0.12
body = (
    body.faces(">Z").workplane()
    .center(0, 0.15)
    .hole(base_hole_d)
)

result = body
