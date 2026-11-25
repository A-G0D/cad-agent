import cadquery as cq

# Base block: 0.5 (X) x 0.75 (Y) x 0.15 (Z)
base = cq.Workplane("XY").box(0.5, 0.75, 0.15, centered=(True, True, False))

# Upper block: 0.5 (X) x 0.35 (Y) x 0.15 (Z), positioned at one end in Y
upper = (
    cq.Workplane("XY")
    .workplane(offset=0.15)
    .center(0, 0.75 / 2 - 0.35 / 2)
    .box(0.5, 0.35, 0.15, centered=(True, True, False))
)

model = base.union(upper)

# Hole through both blocks, centered on the upper block
hole_y = 0.75 / 2 - 0.35 / 2
model = (
    model.faces(">Z").workplane()
    .center(0, hole_y)
    .hole(0.2)
)

# Center the model's bounding box at the origin
bb = model.val().BoundingBox()
model = model.translate((-bb.center.x, -bb.center.y, -bb.center.z))

result = model
