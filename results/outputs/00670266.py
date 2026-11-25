import cadquery as cq

L = 1.08869
W = 0.870954
H = 0.108869
R = 0.217746
D = 0.195965
X = 0.228625

# Rectangle centered on origin in XY, extruded upward from z=0
rect = cq.Workplane("XY").rect(L, W).extrude(H)

# Fillet the vertical corner edges (top edges in plan view) with radius R
solid = rect.edges("|Z").fillet(R)

# Circular through-hole centered just below the top edges, exact diameter D
cx = -L / 2 + X
solid = (
    solid.faces(">Z")
    .workplane()
    .center(cx, 0)
    .circle(D / 2.0)
    .cutThruAll()
)

result = solid
