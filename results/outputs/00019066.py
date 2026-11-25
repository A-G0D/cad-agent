import cadquery as cq

# Base rectangle: length 0.345, width 0.0024 (length ~1.5x width), marginally extruded
base = cq.Workplane("XY").rect(0.345, 0.0024).extrude(0.0024)

# Small rectangular rod at one corner, pointing upwards
# dimensions 0.00375 x 0.75 x 0.0075 (height = 3x rectangle length)
rod = (
    cq.Workplane("XY")
    .center(0.345 / 2 - 0.00375 / 2, 0.0024 / 2 - 0.75 / 2)
    .rect(0.00375, 0.75)
    .extrude(0.0075)
)

result = base.union(rod)
