import cadquery as cq

length = 0.9
width = 1.5
height = 0.75
hole_d = 0.45
offset_x = -0.075

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .workplane()
    .center(offset_x, 0)
    .hole(hole_d)
)
