import cadquery as cq

# Base
base = cq.Workplane("XY").box(1.5, 1.2, 0.147638)

# Hollow cut in center of base
hollow = cq.Workplane("XY").box(0.975, 0.675, 0.11811)
hollow = hollow.translate((0, 0, 0.147638/2 - 0.11811/2))
base = base.cut(hollow)

# Second rectangle on top of base
second = cq.Workplane("XY").box(1.25274, 0.982742, 0.041339)
second = second.translate((0, 0, 0.147638/2 + 0.041339/2))
base = base.union(second)

# Third rectangle on top of second
third = cq.Workplane("XY").box(0.059055, 0.11811, 0.088583)
# Position: 0.390573 from end (X), 0.314204 from side (Y) of second rectangle
x_pos = 1.25274/2 - 0.390573 - 0.059055/2
y_pos = 0.982742/2 - 0.314204 - 0.11811/2
z_pos = 0.147638/2 + 0.041339 + 0.088583/2
third = third.translate((x_pos, y_pos, z_pos))
base = base.union(third)

# Mirror third rectangle on opposite side
third_mirror = cq.Workplane("XY").box(0.059055, 0.11811, 0.088583)
third_mirror = third_mirror.translate((-x_pos, y_pos, z_pos))
base = base.union(third_mirror)

# Translate so base is centered vertically at half height
base = base.translate((0, 0, 0.147638/2))

result = base
