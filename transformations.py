import math

def multiply_matrices(m1, m2):
    res = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                res[i][j] += m1[i][k] * m2[k][j]
    return res

def multiply_matrix_vector(m, v):
    res = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            res[i] += m[i][j] * v[j]
    return res

def translation_matrix(tx, ty):
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]

def rotation_matrix(theta_deg):
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return [[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]]

def scaling_matrix(sx, sy):
    return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]

def reflection_matrix_x():
    return [[1, 0, 0], [0, -1, 0], [0, 0, 1]]

def reflection_matrix_y():
    return [[-1, 0, 0], [0, 1, 0], [0, 0, 1]]

def shear_matrix_x(shx):
    return [[1, shx, 0], [0, 1, 0], [0, 0, 1]]

def shear_matrix_y(shy):
    return [[1, 0, 0], [shy, 1, 0], [0, 0, 1]]

def transform_point(x, y, matrix):
    vec = [x, y, 1]
    res = multiply_matrix_vector(matrix, vec)
    return res[0], res[1]

def transform_polygon(points, matrix):
    return [transform_point(p[0], p[1], matrix) for p in points]

def rotate_about_point(x, y, theta_deg, px, py):
    t1 = translation_matrix(-px, -py)
    r = rotation_matrix(theta_deg)
    t2 = translation_matrix(px, py)
    m = multiply_matrices(t2, multiply_matrices(r, t1))
    return transform_point(x, y, m)

# ---------------------------------------------------------
# NEW: 3D PROJECTION ENGINE
# ---------------------------------------------------------
def rotate_3d_x(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ]

def rotate_3d_y(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ]

def rotate_3d_z(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ]

def project_3d_to_2d(x, y, z, fov=256, viewer_distance=4):
    """Applies perspective projection to map 3D coordinates to 2D screen."""
    # Prevent division by zero
    z = max(0.1, z + viewer_distance)
    
    # x' = f * x / z
    # y' = f * y / z
    px = (fov * x) / z
    py = (fov * y) / z
    
    return px, py

def apply_3d_rotation(point_3d, angle_x, angle_y, angle_z):
    x, y, z = point_3d
    # Rotate Y
    rx = x * math.cos(angle_y) + z * math.sin(angle_y)
    rz = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = rx, rz
    
    # Rotate X
    ry = y * math.cos(angle_x) - z * math.sin(angle_x)
    rz = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = ry, rz
    
    # Rotate Z
    rx = x * math.cos(angle_z) - y * math.sin(angle_z)
    ry = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = rx, ry
    
    return [x, y, z]
