import cadquery as cq
import math

r = 0.014425
h = 1.5
result = cq.Workplane("XY").circle(r).extrude(h)
