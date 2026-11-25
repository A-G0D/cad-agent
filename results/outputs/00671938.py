import cadquery as cq

height = 0.75
d = 0.419231
r = d / 2.0

c1 = cq.Workplane("XY").circle(r).extrude(height).translate((-0.09259, -0.022198, 0.0))
c2 = cq.Workplane("XY").circle(r).extrude(height).translate((0.082574, 0.01872, 0.0))

result = c1.union(c2).translate((0, 0, height / 2.0))
