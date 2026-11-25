import cadquery as cq

pts = [(-0.05430806, 0.05735744), (-0.05430806, -0.05851911), (-0.04704762, -0.05851911),
       (-0.0383351, -0.00217813), (0.00232334, -0.00217813), (0.0116167, -0.06200412),
       (0.01742505, -0.06200412), (0.01452087, 0.01030982), (-0.02875133, 0.01030982),
       (-0.0450147, 0.05735744), (-0.05430806, 0.05735744)]

s = 7.38186180173805

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(0.1016)
    .val()
)

result = result.scale(s)
result = result.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), -90)
result = result.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -90)

result = cq.Workplane("XY").add(result)
