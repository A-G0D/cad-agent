import cadquery as cq

# Rectangle: width 0.120604 along X, length 0.051687 along Y
# Trapezium base = 0.051687 attached to the shorter edge (length 0.051687)
# The shorter edge is the one along X? No: rectangle X=0.120604, Y=0.051687.
# Shorter edge has length 0.051687 -> that edge runs along X at y=0 and y=0.051687.
# Attach trapezium base (0.051687) to that edge, extending in -Y.
# To keep overall bbox Y = 0.051687, the trapezium must not extend beyond the rectangle.
# So the trapezium is cut INTO the rectangle: base at y=0, apex inside toward +Y.
# Overall bbox stays [0.120604, 0.051687, 0.75].

base = 0.051687
top = base / 2.0
trap_h = 0.03  # inside the rectangle (less than 0.051687)
rect_w = 0.120604

# Rectangle profile
rect_pts = [
    (-rect_w/2, 0.0),
    ( rect_w/2, 0.0),
    ( rect_w/2, base),
    (-rect_w/2, base),
]

# Trapezium attached at y=0, base along X, apex pointing into +Y (inside rectangle)
trap_pts = [
    (-base/2, 0.0),
    ( base/2, 0.0),
    ( top/2, trap_h),
    (-top/2, trap_h),
]

result = (
    cq.Workplane("XY")
    .polyline(rect_pts).close()
    .extrude(0.75)
    .faces(">Z").workplane()
    .polyline(trap_pts).close()
    .cutThruAll()
)
