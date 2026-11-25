import cadquery as cq

result = cq.Workplane("XY").rect(0.25, 0.25).extrude(0.5)
