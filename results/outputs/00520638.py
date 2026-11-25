import cadquery as cq

L = 1.10769
W = 0.474725
H = 0.18989
D = L / 2.0
R = D / 2.0
cyl_h = W
conn_h = cyl_h / 2.0
inner_d = 0.194358
inner_r = inner_d / 2.0

base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

cyl = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .center(0, 0)
    .circle(R)
    .extrude(cyl_h)
)

conn = (
    cq.Workplane("XY")
    .workplane(offset=H + cyl_h)
    .center(0, 0)
    .rect(D, D)
    .extrude(conn_h)
)

part = base.union(cyl).union(conn)

inner_cyl = (
    cq.Workplane("XY")
    .workplane(offset=H - 0.001)
    .center(0, 0)
    .circle(inner_r)
    .extrude(cyl_h + conn_h + 0.002)
)

inner_box = (
    cq.Workplane("XY")
    .workplane(offset=H - 0.001)
    .center(0, 0)
    .rect(inner_d, inner_d)
    .extrude(cyl_h + conn_h + 0.002)
)

part = part.cut(inner_cyl).cut(inner_box)

pts = [(0, 0.316484), (-0.056, 0.483119), (L / 2.0, 0.613244), (L / 2.0, 0.434708)]
arm = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(W)
    .translate((0, -W / 2.0, 0))
)

part = part.union(arm)

# Rotate so the assembly's height axis aligns with Z and overall bbox matches spec
part = part.rotate((0, 0, 0), (1, 0, 0), -90)

bb = part.val().BoundingBox()
part = part.translate((-bb.xmin, -bb.ymin, -bb.zmin))

result = part
