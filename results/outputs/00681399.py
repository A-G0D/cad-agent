import cadquery as cq

# Square block
block = cq.Workplane("XY").box(0.990099, 0.415842, 0.990099)

# Circular hole through the block (negative extrusion)
hole = (
    cq.Workplane("XY")
    .circle(0.471867 / 2.0)
    .extrude(0.990099)
)
block = block.cut(hole)

# Annulus (hollow pipe) on the top surface
outer_r = 0.517113 / 2.0
inner_r = 0.471867 / 2.0
pipe = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)
    .extrude(0.334158)
)

# Align pipe base to top of block, then combine
pipe = pipe.translate((0, 0, 0.990099 / 2.0))
result = block.union(pipe)

# Final translation
result = result.translate((0, -0.207921, 0.025308))
