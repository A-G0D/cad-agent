import cadquery as cq
import math

outer_d = 1.5
height = 0.010714
inner_d = outer_d - 0.342858
hole_d = 0.105429
hole_radius_pos = outer_d / 2 - (outer_d - inner_d) / 4

ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .extrude(height)
    .faces(">Z").workplane()
    .circle(inner_d / 2)
    .cutThruAll()
)

hole_pts = [
    (hole_radius_pos * math.cos(math.radians(a)), hole_radius_pos * math.sin(math.radians(a)))
    for a in (90, 210, 330)
]

ring = (
    ring.faces(">Z").workplane()
    .pushPoints(hole_pts)
    .hole(hole_d)
)

result = ring.rotate((0, 0, 0), (0, 0, 1), -90)
