import cadquery as cq

L = 0.75
W = 0.340821
H = 0.031444
right_margin = 0.16366
left_margin = 0.117823
offset = 0.047166

# Outer trapezoid: bottom edge full length, top edge inset by margins
# Build as polygon in XY plane, extrude in Z
outer_pts = [
    (0.0, 0.0),
    (L, 0.0),
    (L - right_margin, W),
    (left_margin, W),
]

# Inner trapezoid offset inward by 'offset' from all edges
# Approximate by scaling/insetting the polygon
def inset_polygon(pts, d):
    # Compute inward offset polygon using edge normals
    n = len(pts)
    lines = []
    for i in range(n):
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = (dx * dx + dy * dy) ** 0.5
        # inward normal (polygon is CCW, so left normal points inward)
        nx = -dy / length
        ny = dx / length
        lines.append((p1[0] + nx * d, p1[1] + ny * d, dx, dy))
    # Intersect consecutive offset lines
    result = []
    for i in range(n):
        x1, y1, dx1, dy1 = lines[i]
        x2, y2, dx2, dy2 = lines[(i + 1) % n]
        denom = dx1 * dy2 - dy1 * dx2
        t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / denom
        result.append((x1 + t * dx1, y1 + t * dy1))
    return result

inner_pts = inset_polygon(outer_pts, offset)

outer_wire = cq.Workplane("XY").polyline(outer_pts).close()
outer_face = outer_wire.extrude(H)

inner_wire = cq.Workplane("XY").polyline(inner_pts).close()
inner_face = inner_wire.extrude(H)

result = outer_face.cut(inner_face)
