def dda_line(x1, y1, x2, y2):
    pixels = []
    steps_info = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x1, y1)], []
        
    xinc = dx / steps
    yinc = dy / steps
    
    x = float(x1)
    y = float(y1)
    
    for i in range(int(steps) + 1):
        px, py = round(x), round(y)
        pixels.append((px, py))
        steps_info.append({"x": x, "y": y, "px": px, "py": py})
        x += xinc
        y += yinc
        
    return pixels, {"dx": dx, "dy": dy, "steps": steps, "xinc": xinc, "yinc": yinc, "steps_info": steps_info}

def bresenham_line(x1, y1, x2, y2):
    pixels = []
    steps_info = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    err = dx - dy
    
    x, y = x1, y1
    
    while True:
        pixels.append((x, y))
        steps_info.append({"x": x, "y": y, "err": err})
        
        if x == x2 and y == y2:
            break
            
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
            
    return pixels, {"dx": dx, "dy": dy, "steps_info": steps_info}

def midpoint_circle(xc, yc, r):
    pixels = []
    steps_info = []
    x = 0
    y = r
    p = 1 - r
    
    def add_circle_points(xc, yc, x, y):
        pts = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ]
        for pt in pts:
            if pt not in pixels:
                pixels.append(pt)
                
    add_circle_points(xc, yc, x, y)
    
    while x < y:
        steps_info.append({"x": x, "y": y, "p": p})
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        add_circle_points(xc, yc, x, y)
        
    return pixels, {"r": r, "steps_info": steps_info}

def midpoint_ellipse(xc, yc, rx, ry):
    pixels = []
    
    def add_ellipse_points(xc, yc, x, y):
        pts = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y)
        ]
        for pt in pts:
            if pt not in pixels:
                pixels.append(pt)
                
    # Region 1
    x = 0
    y = ry
    p1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    
    while dx < dy:
        add_ellipse_points(xc, yc, round(x), round(y))
        if p1 < 0:
            x += 1
            dx += (2 * ry * ry)
            p1 += dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx += (2 * ry * ry)
            dy -= (2 * rx * rx)
            p1 += dx - dy + (ry * ry)
            
    # Region 2
    p2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)
    while y >= 0:
        add_ellipse_points(xc, yc, round(x), round(y))
        if p2 > 0:
            y -= 1
            dy -= (2 * rx * rx)
            p2 += (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx += (2 * ry * ry)
            dy -= (2 * rx * rx)
            p2 += dx - dy + (rx * rx)
            
    return pixels, {}
