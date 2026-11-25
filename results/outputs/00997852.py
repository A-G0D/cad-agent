import cadquery as cq

base = cq.Workplane("XY").box(1.5, 0.153061, 0.918367)

top = (
    cq.Workplane("XY")
    .workplane(offset=0.918367 / 2)
    .rect(1.43878, 0.841837)
    .extrude(0.229592)
)

result = base.union(top)
