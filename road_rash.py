import pygame
import math
import sys

# Screen Settings
WIDTH, HEIGHT = 1024, 768
FPS = 60

# Colors
GRASS_LIGHT = (34, 139, 34)
GRASS_DARK = (0, 100, 0)
ROAD_LIGHT = (100, 100, 100)
ROAD_DARK = (80, 80, 80)
RUMBLE_LIGHT = (255, 255, 255)
RUMBLE_DARK = (255, 0, 0)
SKY = (135, 206, 235)

def project(cam_x, cam_y, cam_z, cam_depth, world_x, world_y, world_z, road_width):
    # Map world coordinates to camera coordinates
    dx = world_x - cam_x
    dy = world_y - cam_y
    dz = world_z - cam_z
    
    if dz == 0: dz = 1
    
    # Perspective projection
    proj_x = int(WIDTH / 2 + (dx / dz) * cam_depth)
    proj_y = int(HEIGHT / 2 - (dy / dz) * cam_depth)
    proj_w = int((road_width / dz) * cam_depth)
    
    return proj_x, proj_y, proj_w

def main():
    pygame.init()
    flags = pygame.SCALED | pygame.RESIZABLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("GLITCH GUY: Road Rash Raster Engine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30, bold=True)

    # Road generation
    road_segments = []
    segment_length = 200
    total_segments = 2000
    
    for i in range(total_segments):
        curve = 0
        if 300 < i < 700: curve = 0.5
        elif 900 < i < 1400: curve = -0.5
        
        y_hill = math.sin(i / 30.0) * 1500
        
        road_segments.append({
            'z': i * segment_length,
            'curve': curve,
            'y': y_hill
        })

    cam_z = 0
    cam_x = 0
    speed = 0
    max_speed = 300
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            speed += 5
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            speed -= 5
        else:
            speed *= 0.95 # friction
            
        speed = max(0, min(speed, max_speed))
        cam_z += speed
        
        # Loop track
        if cam_z >= (total_segments * segment_length):
            cam_z = 0
            
        start_pos = int(cam_z / segment_length)
        cam_y = 1500 + road_segments[start_pos % total_segments]['y']
        
        # Steering
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            cam_x -= 200 + (speed * 0.5)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            cam_x += 200 + (speed * 0.5)

        # Draw Sky
        screen.fill(SKY)
        
        # Render Road
        max_y = HEIGHT
        dx = 0
        x = 0
        
        for i in range(start_pos, start_pos + 300):
            idx = i % total_segments
            seg = road_segments[idx]
            
            # Add curve
            x += dx
            dx += seg['curve']
            
            p_x, p_y, p_w = project(
                cam_x - x, cam_y, cam_z, 
                cam_depth=800, 
                world_x=0, world_y=seg['y'], world_z=seg['z'], 
                road_width=2000
            )
            
            # Check clipping
            if p_y >= max_y or p_y < 0:
                continue
            max_y = p_y
            
            # Checkerboard colors
            grass_col = GRASS_LIGHT if (i // 3) % 2 else GRASS_DARK
            rumble_col = RUMBLE_LIGHT if (i // 3) % 2 else RUMBLE_DARK
            road_col = ROAD_LIGHT if (i // 3) % 2 else ROAD_DARK
            
            # Grass
            pygame.draw.rect(screen, grass_col, (0, p_y, WIDTH, HEIGHT - p_y))
            
            # Rumble strips
            rumble_w = int(p_w * 1.2)
            pygame.draw.polygon(screen, rumble_col, [
                (p_x - rumble_w, p_y),
                (p_x + rumble_w, p_y),
                (p_x + rumble_w, p_y + 10), # Simplified height
                (p_x - rumble_w, p_y + 10)
            ])
            
            # Road
            pygame.draw.polygon(screen, road_col, [
                (p_x - p_w, p_y),
                (p_x + p_w, p_y),
                (p_x + p_w, p_y + 10),
                (p_x - p_w, p_y + 10)
            ])

        # Draw speed
        speed_text = font.render(f"SPEED: {int(speed)} MPH", True, (255, 255, 0))
        screen.blit(speed_text, (20, 20))
        
        # Fake Player Bike (Rectangle for now)
        pygame.draw.rect(screen, (0, 0, 255), (WIDTH//2 - 25, HEIGHT - 150, 50, 100))
        pygame.draw.circle(screen, (0,0,0), (WIDTH//2, HEIGHT-160), 20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
