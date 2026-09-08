def flood_fill(surface, x, y, fill_color, boundary_color):
    # This is meant to be a conceptual demonstration.
    # In a real pygame app without surface direct access this could be slow,
    # but we will just return a list of pixels or do surface.set_at directly if needed.
    # We will simulate returning the pixels that need to be colored.
    pass

def scanline_fill(polygon_points):
    # A simple scanline fill implementation that returns all points inside polygon
    pixels = []
    
    if not polygon_points:
        return pixels
        
    min_y = int(min(p[1] for p in polygon_points))
    max_y = int(max(p[1] for p in polygon_points))
    
    for y in range(min_y, max_y + 1):
        intersections = []
        j = len(polygon_points) - 1
        for i in range(len(polygon_points)):
            pi = polygon_points[i]
            pj = polygon_points[j]
            
            if (pi[1] < y and pj[1] >= y) or (pj[1] < y and pi[1] >= y):
                # Calculate x intersection
                if pi[1] != pj[1]:
                    x = pi[0] + (y - pi[1]) * (pj[0] - pi[0]) / (pj[1] - pi[1])
                    intersections.append(x)
            j = i
            
        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            x_start = int(intersections[i])
            x_end = int(intersections[i+1])
            for x in range(x_start, x_end + 1):
                pixels.append((x, y))
                
    return pixels
