import cadquery as cq

length = 0.59437
width = 0.44577
height = 0.37148

result = cq.Workplane("XY").box(length, width, height)
