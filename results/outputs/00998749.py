import cadquery as cq

W = 0.440093
H = 0.143395
base_t = 0.143395
wall_h = 0.131228
inner_w = 0.382387
inner_l = 0.721321
fil_r = 0.017381

# Base
base = cq.Workplane("XY").rect(W, H).extrude(base_t)

# Walls: outer rect = base, inner rect = given, fillet inner corners
outer_hx = W / 2
outer_hy = H / 2
inner_hx = inner_w / 2
inner_hy = inner_l / 2

# Build wall profile as a face on top of base
wall_sk = (
    cq.Workplane("XY")
    .workplane(offset=base_t)
    .rect(W, H)
    .rect(inner_w, inner_l)
)

# Create a face with a hole by extruding outer rect and cutting inner
outer_solid = cq.Workplane("XY").workplane(offset=base_t).rect(W, H).extrude(wall_h)
inner_solid = cq.Workplane("XY").workplane(offset=base_t).rect(inner_w, inner_l).extrude(wall_h + 1)
walls = outer_solid.cut(inner_solid)

# Fillet the inner vertical edges
inner_edges = walls.edges("|Z").edges(cq.selectors.BoxSelector(
    (-inner_hx - 0.001, -inner_hy - 0.001, base_t + 0.001),
    (inner_hx + 0.001, inner_hy + 0.001, base_t + wall_h + 0.001)
))
# Select only edges near inner rectangle corners
def near_inner(e):
    c = e.Center()
    return abs(abs(c.x) - inner_hx) < 0.01 and abs(abs(c.y) - inner_hy) < 0.01

sel = [e for e in walls.edges("|Z").vals() if near_inner(e)]
if sel:
    walls = walls.newObject(sel).fillet(fil_r)

box = base.union(walls)

# Translate to center
dx = W / 2 - 0.030417
dy = H / 2 - 0.030417 + 0.001564
dz = (base_t + wall_h) / 2
result = box.translate((dx, dy, dz))
