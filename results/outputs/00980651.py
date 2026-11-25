import cadquery as cq

side = 1.47802
hex_h = 0.5
cyl_d = 1.2
cyl_h = 0.25

hexagon = cq.Workplane("XY").polygon(6, side).extrude(hex_h)
cylinder = cq.Workplane("XY").workplane(offset=hex_h).circle(cyl_d / 2).extrude(cyl_h)

result = hexagon.union(cylinder)
