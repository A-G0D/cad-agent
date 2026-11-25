import cadquery as cq

# First right trapezoidal prism
b1, t1, h1, w1 = 1.11043, 0.55953, 0.625913, 1.0011
pts1 = [(0, 0), (b1, 0), (t1, h1), (0, h1)]
trap1 = cq.Workplane("XZ").polyline(pts1).close().extrude(w1)

# Second right trapezoidal prism
b2, t2, h2, w2 = 1.27908, 0.619642, 0.75, 0.201835
pts2 = [(0, 0), (b2, 0), (t2, h2), (0, h2)]
trap2 = cq.Workplane("XZ").polyline(pts2).close().extrude(w2)

# Align second trapezoid to one side of the first (front face, y=0)
trap2 = trap2.translate((0, -w2, 0))

result = trap1.union(trap2)
