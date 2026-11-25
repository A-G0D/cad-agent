import cadquery as cq

# Base cylinder
cylinder = cq.Workplane("XY").circle(0.95 / 2).extrude(0.475)

# Thin rectangular prism on top, centered, extruded upward
rect = (
    cq.Workplane("XY")
    .workplane(offset=0.475)
    .rect(0.76, 0.7)
    .extrude(0.2375)
)

result = cylinder.union(rect)
