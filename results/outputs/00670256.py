import cadquery as cq

length = 0.1875
width = 0.1875
height = 0.75
pad = 0.014063

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z").workplane()
    .rect(length - 2*pad, width - 2*pad)
    .cutBlind(-height)
    .rotate((0,0,0), (1,0,0), 90)
)
