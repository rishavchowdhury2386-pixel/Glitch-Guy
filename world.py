import pygame
import math
from settings import *
from rasterization import midpoint_ellipse
from transformations import apply_3d_rotation, project_3d_to_2d
from utils import draw_beveled_rect

class World:
    def __init__(self):
        self.tiles = []
        for x in range(0, MAP_WIDTH, TILE_SIZE):
            for y in range(0, MAP_HEIGHT, TILE_SIZE):
                is_road = False
                if 800 <= x <= 1000 or 800 <= y <= 1000:
                    is_road = True
                
                if is_road:
                    color = (120, 120, 120)
                else:
                    base_g = 180 if (x + y) % (TILE_SIZE * 2) == 0 else 160
                    color = (34, base_g, 34)
                
                self.tiles.append({
                    "rect": pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 
                    "color": color,
                    "is_road": is_road
                })
                
        self.tree_pixels = []
        pixels, _ = midpoint_ellipse(0, 0, 30, 45)
        for px, py in pixels:
            self.tree_pixels.append((px, py))
            
        self.tree_locations = [(300, 300), (400, 200), (1000, 1500), (1600, 600), (700, 1200)]
        
        # 3D Cube Data
        self.cube_vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        self.cube_edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        self.cube_locations = [(500, 600), (1300, 300), (200, 1400), (1800, 800)]
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def draw(self, surface, camera):
        # Update 3D rotation angles
        self.angle_x += 0.02
        self.angle_y += 0.03
        self.angle_z += 0.01
        
        # Draw ground
        for tile in self.tiles:
            rect = camera.apply_rect(tile["rect"])
            if rect.colliderect(surface.get_rect()):
                draw_beveled_rect(surface, tile["color"], rect, border_radius=5)
                if not tile["is_road"]:
                    pygame.draw.line(surface, (0, 100, 0), (rect.x + 10, rect.y + 10), (rect.x + 15, rect.y + 5), 3)

        # Draw 3D Floating Glitch Cubes
        for cx, cy in self.cube_locations:
            scx, scy = camera.apply_point((cx, cy))
            if -100 < scx < WIDTH + 100 and -100 < scy < HEIGHT + 100:
                projected_points = []
                for v in self.cube_vertices:
                    # Apply 3D Rotation
                    rotated = apply_3d_rotation(v, self.angle_x, self.angle_y, self.angle_z)
                    # Apply Perspective Projection
                    px, py = project_3d_to_2d(rotated[0], rotated[1], rotated[2], fov=400, viewer_distance=4)
                    projected_points.append((int(px + scx), int(py + scy - 30))) # Offset Y slightly for floating effect
                
                # Draw Cube Edges
                for edge in self.cube_edges:
                    p1 = projected_points[edge[0]]
                    p2 = projected_points[edge[1]]
                    pygame.draw.line(surface, (0, 255, 255), p1, p2, 2)
                    
                # Draw glowing nodes on vertices
                for pt in projected_points:
                    pygame.draw.circle(surface, (255, 0, 255), pt, 4)

        # Draw Trees (with fake 3D depth shadows)
        for tx, ty in self.tree_locations:
            trunk_rect = camera.apply_rect(pygame.Rect(tx - 10, ty + 20, 20, 40))
            if trunk_rect.colliderect(surface.get_rect()):
                # Drop shadow
                shadow_rect = pygame.Rect(trunk_rect.x + 10, trunk_rect.y + 30, 40, 20)
                pygame.draw.ellipse(surface, (0, 0, 0, 80), shadow_rect)
                
                draw_beveled_rect(surface, (101, 67, 33), trunk_rect, border_radius=8)
                
                for px, py in self.tree_pixels:
                    sx, sy = camera.apply_point((tx + px, ty + py))
                    surface.set_at((int(sx), int(sy)), (34, 139, 34))
                    surface.set_at((int(sx+1), int(sy)), (50, 200, 50))
