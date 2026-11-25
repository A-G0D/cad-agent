import cadquery as cq

# Dimensions (mm)
vert_len = 36.0      # vertical rectangle length (X)
vert_wid = 13.5      # vertical rectangle width (Y)
height = 900.0       # extrusion height (Z)
horiz_len = 240.0    # horizontal rectangle length (X)
horiz_wid = 13.5     # horizontal rectangle width (Y)
horiz_extrude = 36.0 # horizontal extrusion (Z)
offset_from_top = 150.0

# Vertical bar: centered on origin in X/Y, extruded along Z
vertical = (
    cq.Workplane("XY")
    .rect(vert_len, vert_wid)
    .extrude(height)
)

# Horizontal bar: top of horizontal is 150 below top of vertical
horiz_top_z = height - offset_from_top
horiz_bottom_z = horiz_top_z - horiz_extrude

# Horizontal bar centered at origin in X/Y, extruded in Z
horizontal = (
    cq.Workplane("XY")
    .rect(horiz_len, horiz_wid)
    .extrude(horiz_extrude)
    .translate((0, 0, horiz_bottom_z))
)

result = vertical.union(horizontal)
