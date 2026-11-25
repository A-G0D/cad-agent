import cadquery as cq

R1 = 0.489821
R2 = 0.319623
dx = 0.260308
h = 0.006808

outer = (
    cq.Workplane("XY")
    .moveTo(-dx / 2, 0)
    .circle(R1)
    .moveTo(dx / 2, 0)
    .circle(R1)
)

inner = (
    cq.Workplane("XY")
    .moveTo(-dx / 2, 0)
    .circle(R2)
    .moveTo(dx / 2, 0)
    .circle(R2)
)

result = outer.extrude(h).cut(inner.extrude(h))
