import cadquery as cq

# Main rectangular prism: 1 x 0.1 x 1.25
prism = cq.Workplane("XY").box(1.0, 0.1, 1.25, centered=(True, True, False))

# Rectangular through-hole (slot) in the width direction:
# length 0.5 (X), height 0.075 (Z), bottom padding 0.25 from base
hole = (
    cq.Workplane("XZ")
    .center(0, 0.25 + 0.075 / 2.0)
    .rect(0.5, 0.075)
    .extrude(0.1, both=True)
)

result = prism.cut(hole).translate((0.0, 0.0, 0.0))
