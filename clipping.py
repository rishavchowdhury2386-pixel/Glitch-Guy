INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= TOP
    elif y > ymax:
        code |= BOTTOM
    return code

def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x, y = 0.0, 0.0
            code_out = code1 if code1 != 0 else code2

            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None

def liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    dx = x2 - x1
    dy = y2 - y1
    
    p = [-dx, dx, -dy, dy]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]
    
    t1 = 0.0
    t2 = 1.0
    
    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                if t > t2: return None
                if t > t1: t1 = t
            else:
                if t < t1: return None
                if t < t2: t2 = t
                
    if t1 < t2:
        nx1 = x1 + t1 * dx
        ny1 = y1 + t1 * dy
        nx2 = x1 + t2 * dx
        ny2 = y1 + t2 * dy
        return (nx1, ny1, nx2, ny2)
    return None

def sutherland_hodgman(subject_polygon, clip_polygon):
    def inside(p, cp1, cp2):
        return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

    def intersection(cp1, cp2, s, e):
        dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
        dp = [s[0] - e[0], s[1] - e[1]]
        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 = s[0] * e[1] - s[1] * e[0] 
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return ((n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3)

    output_list = subject_polygon
    cp1 = clip_polygon[-1]

    for clip_vertex in clip_polygon:
        cp2 = clip_vertex
        input_list = output_list
        output_list = []
        
        if not input_list:
            break
            
        s = input_list[-1]

        for subject_vertex in input_list:
            e = subject_vertex
            if inside(e, cp1, cp2):
                if not inside(s, cp1, cp2):
                    output_list.append(intersection(cp1, cp2, s, e))
                output_list.append(e)
            elif inside(s, cp1, cp2):
                output_list.append(intersection(cp1, cp2, s, e))
            s = e
        cp1 = cp2
        
    return output_list
