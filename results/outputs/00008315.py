import cadquery as cq

result = cq.Workplane("XY").box(0.75, 0.0075, 0.075).translate((0, 0, 0))
solid = result.val()
result = cq.Workplane("XY").newObject([solid])
