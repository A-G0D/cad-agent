import cadquery as cq

# Cylinder axis along Z, diameter 0.249945, height (width) 0.75
r = 0.249945 / 2.0
h = 0.75
c1 = cq.Workplane("XY").circle(r).extrude(h)

# Second cylinder: same dimensions, translated by 0.125404 along Z
c2 = cq.Workplane("XY").workplane(offset=0.125404).circle(r).extrude(h)

# Subtract second from first to form crescent
crescent = c1.cut(c2)

# Translate by half the width in the negative Y direction
result = crescent.translate((0, -h / 2.0, 0))
