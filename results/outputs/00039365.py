import cadquery as cq

pts = [(0.6147, 0), (1.500795, 0), (0.886095, 0.354438), (0, 0.354438)]
height = 0.425326
sq_w = 0.306589
sq_h = 0.25874

# Parallelogram centroid
cx = sum(p[0] for p in pts) / 4.0
cy = sum(p[1] for p in pts) / 4.0

base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

hole = (
    cq.Workplane("XY")
    .center(cx, cy)
    .rect(sq_w, sq_h)
    .extrude(height)
)

result = base.cut(hole)
