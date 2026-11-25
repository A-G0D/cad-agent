import cadquery as cq

# Build the L-shaped profile in the XZ plane, then extrude in Y.
# Horizontal leg: length 0.024896 along X at the bottom.
# Vertical leg: spline from end of horizontal section curving up to ~0.752339, then straight line.

h_len = 0.024896
v_len = 0.752339
depth = 0.018672

# Thickness of the L arms (chosen so the shape is a valid L)
t = 0.012

# Profile points (in XZ plane, Z up):
# Start at origin (0,0)
# Horizontal bottom edge to (h_len, 0)
# Up the outer edge of vertical leg to (h_len, v_len) with a slight spline curve
# Across the top to (h_len - t, v_len)
# Down the inner edge to (h_len - t, t)
# Back to (0, t)
# Close to (0,0)

# Slight curve on the vertical section: outer edge bows outward slightly.
# Use a spline from (h_len, 0) to (h_len, v_len) with a control point bulging in +X.
bulge = 0.004

pts_outer = [
    (h_len, 0.0),
    (h_len + bulge, v_len * 0.5),
    (h_len, v_len),
]

# Build wire in XZ plane using Workplane("XZ")
wp = cq.Workplane("XZ")

# Create the profile as a closed wire
# Points in local XZ coordinates (x, z)
profile_pts = [
    (0.0, 0.0),
    (h_len, 0.0),
]

# Spline for outer vertical edge
spline = cq.Edge.makeSpline(
    [
        cq.Vector(h_len, 0.0, 0.0),
        cq.Vector(h_len + bulge, 0.0, v_len * 0.5),
        cq.Vector(h_len, 0.0, v_len),
    ]
)

# Straight segments
e1 = cq.Edge.makeLine(cq.Vector(0.0, 0.0, 0.0), cq.Vector(h_len, 0.0, 0.0))
e2 = spline
e3 = cq.Edge.makeLine(cq.Vector(h_len, 0.0, v_len), cq.Vector(h_len - t, 0.0, v_len))
e4 = cq.Edge.makeLine(cq.Vector(h_len - t, 0.0, v_len), cq.Vector(h_len - t, 0.0, t))
e5 = cq.Edge.makeLine(cq.Vector(h_len - t, 0.0, t), cq.Vector(0.0, 0.0, t))
e6 = cq.Edge.makeLine(cq.Vector(0.0, 0.0, t), cq.Vector(0.0, 0.0, 0.0))

wire = cq.Wire.assembleEdges([e1, e2, e3, e4, e5, e6])
face = cq.Face.makeFromWires(wire)

# Extrude the face along Y by depth
solid = cq.Solid.extrudeLinear(face, cq.Vector(0.0, depth, 0.0))

result = cq.Workplane("XY").add(solid)
