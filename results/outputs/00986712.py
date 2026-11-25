import cadquery as cq

L = 0.875
W = 0.15
H = 1.5
r = 0.25
hole_d = 0.3
pad = -0.639071

fillet_r = min(r, W/2 - 1e-6)

base = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(H)
)

base = (
    base.edges("|Z")
    .edges(cq.selectors.BoxSelector(
        (L/2 - 1e-6, -W/2 - 1e-6, -1),
        (L/2 + 1e-6, W/2 + 1e-6, H + 1)
    ))
    .fillet(fillet_r)
)

# Holes must be placed within the material. The padded position lands
# outside the part, so clamp the hole centers to lie inside the body.
hole_x = L/2 + pad
hole_y = W/2 + pad

# Clamp x into the body interior
max_x = L/2 - hole_d/2 - 1e-3
min_x = -L/2 + hole_d/2 + 1e-3
hole_x = max(min(hole_x, max_x), min_x)

# Clamp y into the body interior
max_y = W/2 - hole_d/2 - 1e-3
min_y = -W/2 + hole_d/2 + 1e-3
hole_y = max(min(hole_y, max_y), min_y)

result = (
    base.faces(">Z").workplane()
    .pushPoints([(hole_x, hole_y), (hole_x, -hole_y)])
    .hole(hole_d)
)
