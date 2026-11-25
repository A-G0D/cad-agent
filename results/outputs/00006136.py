import cadquery as cq

base = 1.04094
height = 0.465517
extrude = 0.75

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (base, 0), (0, height)])
    .close()
    .extrude(extrude)
)
