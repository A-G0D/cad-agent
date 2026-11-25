import cadquery as cq

main_d = 1.5
main_r = main_d / 2
height = 0.1

hole_d = 0.1124
hole_r = hole_d / 2
padding = 0.041187
offset = main_r / 2 - hole_r - padding

result = cq.Workplane("XY").circle(main_r).extrude(height)

positions = [
    (offset, offset),
    (-offset, offset),
    (-offset, -offset),
    (offset, -offset),
]

result = (
    result.faces(">Z").workplane()
    .pushPoints(positions)
    .hole(hole_d)
)

result = result.rotate((0, 0, 0), (0, 0, 1), 45)
result = result.rotate((0, 0, 0), (0, 1, 0), 90)

bb = result.val().BoundingBox()
center = bb.center
result = result.translate((-center.x, -center.y, -center.z))
