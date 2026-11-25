import cadquery as cq

extrude_length = 0.75
mid_length = 0.234841
bottom_length = 0.11742
mid_height = 0.280088
top_height = 0.204477
bottom_height = 0.279461
mid_shift = 0.004644
bottom_shift = 0.002349

top_vertex = (0, top_height)
mid_left = (-mid_length / 2 + mid_shift, 0)
bot_left = (-bottom_length / 2 + bottom_shift, -bottom_height)
bot_right = (bottom_length / 2 + bottom_shift, -bottom_height)
mid_right = (mid_length / 2 + mid_shift, 0)

pts = [top_vertex, mid_left, bot_left, bot_right, mid_right]

result = cq.Workplane("XY").polyline(pts).close().extrude(extrude_length)
