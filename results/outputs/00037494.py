import cadquery as cq

outer = 0.23077
inner = 0.18462
length = 0.75

result = (
    cq.Workplane("XZ")
    .rect(outer, outer)
    .extrude(length)
    .faces(">Y").workplane()
    .rect(inner, inner)
    .cutBlind(-length)
)
