import cadquery as cq

# Large square plate 1.5 x 1.5, thickness 0.09375
plate = cq.Workplane("XY").rect(1.5, 1.5).extrude(0.09375)

# Right triangle cut at bottom-right corner
# Right angle at (0.75, -0.75), legs along bottom edge (1.125) and right edge (1.3125)
tri = (
    cq.Workplane("XY")
    .polyline([(0.75, -0.75), (0.75 - 1.125, -0.75), (0.75, -0.75 + 1.3125)])
    .close()
    .extrude(0.09375)
)

result = plate.cut(tri)
