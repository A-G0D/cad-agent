import cadquery as cq

outer_d = 1.0

h1 = 0.242143
d1 = 0.332143

h2 = 0.321568
d2 = 0.728571

# First section: outer cylinder with small bore
sec1 = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .extrude(h1)
    .faces(">Z")
    .workplane()
    .hole(d1)
)

# Second section: outer cylinder with large bore, stacked on top
sec2 = (
    cq.Workplane("XY")
    .workplane(offset=h1)
    .circle(outer_d / 2)
    .extrude(h2)
    .faces(">Z")
    .workplane()
    .hole(d2)
)

result = sec1.union(sec2)
