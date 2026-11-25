import cadquery as cq

# Base square plate
plate = cq.Workplane("XY").rect(1.3125, 1.3125).extrude(0.0625)

# Four tiny holes near corners
hole_d = 0.05
inset = 0.15
plate = (
    plate.faces(">Z").workplane()
    .pushPoints([
        (1.3125/2 - inset, 1.3125/2 - inset),
        (-(1.3125/2 - inset), 1.3125/2 - inset),
        (-(1.3125/2 - inset), -(1.3125/2 - inset)),
        (1.3125/2 - inset, -(1.3125/2 - inset)),
    ])
    .hole(hole_d)
)

# Hollow cylinder (tube) through the middle
outer_r = 1.0 / 2
inner_r = 0.9375 / 2
tube_h = 0.6875
tube = (
    cq.Workplane("XY")
    .circle(outer_r).extrude(tube_h)
    .faces(">Z").workplane()
    .circle(inner_r).cutThruAll()
)

# Position tube centered on plate, extending through it
tube = tube.translate((0, 0, -0.0625))

assembly = plate.union(tube)
assembly = assembly.translate((0, 0, 0.03125))

result = assembly
