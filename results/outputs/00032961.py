import cadquery as cq

L = 1.49973
W = 0.16071
T = 0.05357
R = W / 2.0
hole_d = 0.080357

# Stadium profile: rectangle plus two end circles, unioned
rect = (
    cq.Workplane("XY")
    .center(L / 2.0, 0)
    .rect(L - W, W)
    .extrude(T)
)
c1 = cq.Workplane("XY").center(R, 0).circle(R).extrude(T)
c2 = cq.Workplane("XY").center(L - R, 0).circle(R).extrude(T)

body = rect.union(c1).union(c2)

# Cut both holes explicitly as cylinders to guarantee two holes
h1 = cq.Workplane("XY").center(R, 0).circle(hole_d / 2.0).extrude(T)
h2 = cq.Workplane("XY").center(L - R, 0).circle(hole_d / 2.0).extrude(T)

result = body.cut(h1).cut(h2)
