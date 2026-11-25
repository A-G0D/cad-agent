import cadquery as cq

# Base hexagon
h1 = cq.Workplane("XY").polygon(6, 1.15342).extrude(0.249723)

# Second hexagon, rotated slightly
h2 = (
    cq.Workplane("XY")
    .workplane(offset=0.249723)
    .polygon(6, 0.865066)
    .rotate((0, 0, 0), (0, 0, 1), 17)
    .extrude(0.199778)
)

# Third hexagon, rotated differently
h3 = (
    cq.Workplane("XY")
    .workplane(offset=0.249723 + 0.199778)
    .polygon(6, 0.576711)
    .rotate((0, 0, 0), (0, 0, 1), 31)
    .extrude(0.099889)
)

# Triangle on top, rotated differently
tri = (
    cq.Workplane("XY")
    .workplane(offset=0.249723 + 0.199778 + 0.099889)
    .polygon(3, 0.228054)
    .rotate((0, 0, 0), (0, 0, 1), 47)
    .extrude(0.079911)
)

result = h1.union(h2).union(h3).union(tri)
