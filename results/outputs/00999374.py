import cadquery as cq

pts = [
    (-0.215997, -0.071707),
    (0.283196/2 - 0.086266, -0.571139/2 + 0.128415),
    (0.283196/2 + 0.154673, 0.571139/2 - 0.103869),
    (0.283196/3 - 0.094331, 0.571139 - 0.45031),
]

body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(0.493701)
)

prism = (
    cq.Workplane("XY")
    .rect(0.1323, 0.78659)
    .extrude(0.203642)
    .rotate((0, 0, 0), (0, 0, 1), -41.7)
    .translate((0.223543, -0.361526, 0.301748))
)

# Move prism down so it clearly overlaps the body in Z, then union
prism = prism.translate((0, 0, -0.15))

result = body.union(prism).clean()
