import cadquery as cq

result = (
    cq.Workplane("XY")
    .polygon(8, 1.00328)
    .extrude(0.271665)
    .rotate((0, 0, 0), (0, 0, 1), 22.4)
    .rotate((0, 0, 0), (1, 0, 0), -90)
    .translate((-0.176576, 0, 0.286546))
)
