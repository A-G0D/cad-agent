import cadquery as cq

base_d = 1.5
base_h = 0.114796
top_d = 1.17857
top_h = 0.306123

base = cq.Workplane("XY").circle(base_d / 2.0).extrude(base_h)
top = cq.Workplane("XY").circle(top_d / 2.0).extrude(top_h).translate((0, 0, base_h))

result = base.union(top)
