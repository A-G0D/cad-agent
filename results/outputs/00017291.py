import cadquery as cq

L = 0.747683
t = 0.498375

cube = cq.Workplane("XY").box(L, L, L, centered=False)

tri = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(t, 0)
    .lineTo(0, t)
    .close()
    .extrude(L)
)

result = cube.union(tri)
