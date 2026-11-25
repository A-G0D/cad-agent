import cadquery as cq

inner_d = 0.70248 * 25.4
outer_d = 0.825 * 25.4
pipe_h = 0.75 * 25.4
flange_h = 0.01125 * 25.4

result = (
    cq.Workplane("XY")
    .circle(inner_d / 2)
    .extrude(pipe_h)
    .faces(">Z")
    .workplane()
    .circle(outer_d / 2)
    .extrude(-flange_h)
)
