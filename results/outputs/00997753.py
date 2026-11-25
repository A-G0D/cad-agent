import cadquery as cq

outer = (
    cq.Workplane("XY")
    .rect(1.5, 1.5)
    .extrude(0.655147)
    .edges("|Z")
    .fillet(0.157235)
)

inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=0.655147)
    .rect(1.44759, 1.44759)
    .extrude(-0.655147)
    .edges("|Z")
    .fillet(0.13103)
)

result = outer.cut(inner_cut).translate((0, 0, 0.655147 / 2))
