import cadquery as cq

# Base step
base = cq.Workplane("XY").box(0.75, 0.658737, 0.284211, centered=(True, True, False))

# Second step, centered on top of base
step = (
    cq.Workplane("XY")
    .workplane(offset=0.284211)
    .box(0.347368, 0.658737, 0.135789, centered=(True, True, False))
)

result = base.union(step)
