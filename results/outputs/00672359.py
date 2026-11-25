import cadquery as cq

s = 0.32592
h = 0.023387

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(s, 0)
    .lineTo(s, s)
    .lineTo(0, s)
    .close()
    .moveTo(0, s)
    .lineTo(s, s)
    .lineTo(0, 2 * s)
    .close()
    .extrude(h)
)
