import pygame
import random
from settings import *
from rasterization import dda_line, bresenham_line
from utils import draw_beveled_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(x)
        self.y = float(y)
        self.health = 100
        self.score = 0
        self.weapon_mode = "DDA"
        self.projectiles = []
        self.particles = []
        self.facing_right = True
        self.draw_player()

    def draw_player(self):
        self.image.fill((0,0,0,0))
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (5, 30, 30, 10))
        draw_beveled_rect(self.image, (0, 0, 255), pygame.Rect(10, 20, 20, 15))
        draw_beveled_rect(self.image, (255, 0, 0), pygame.Rect(5, 15, 30, 10))
        pygame.draw.circle(self.image, (255, 204, 153), (20, 12), 8)
        pygame.draw.circle(self.image, (255, 0, 0), (20, 8), 8)
        if self.facing_right:
            pygame.draw.rect(self.image, (255, 0, 0), (20, 4, 12, 4))
            pygame.draw.circle(self.image, (0, 0, 0), (24, 10), 2)
        else:
            pygame.draw.rect(self.image, (255, 0, 0), (8, 4, 12, 4))
            pygame.draw.circle(self.image, (0, 0, 0), (16, 10), 2)

    def get_input(self):
        keys = pygame.key.get_pressed()
        speed = PLAYER_SPEED
        if keys[pygame.K_LSHIFT]:
            speed = PLAYER_RUN_SPEED
        if keys[pygame.K_SPACE]:
            speed = PLAYER_DASH_SPEED

        dx, dy = 0, 0
        if keys[pygame.K_w]: dy = -speed
        if keys[pygame.K_s]: dy = speed
        if keys[pygame.K_a]: 
            dx = -speed
            if self.facing_right:
                self.facing_right = False
                self.draw_player()
        if keys[pygame.K_d]: 
            dx = speed
            if not self.facing_right:
                self.facing_right = True
                self.draw_player()
        
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, MAP_WIDTH - self.rect.width))
        self.y = max(0, min(self.y, MAP_HEIGHT - self.rect.height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def shoot(self, target_x, target_y, camera):
        cam_x, cam_y = camera.camera.x, camera.camera.y
        world_target_x = target_x - cam_x
        world_target_y = target_y - cam_y
        
        if self.weapon_mode == "DDA":
            pixels, info = dda_line(self.rect.centerx, self.rect.centery, world_target_x, world_target_y)
        else:
            pixels, info = bresenham_line(self.rect.centerx, self.rect.centery, world_target_x, world_target_y)
            
        self.projectiles.append({
            "pixels": pixels,
            "current": 0,
            "color": YELLOW if self.weapon_mode == "DDA" else CYAN
        })
        
        # Add particles for high graphic effect
        for _ in range(10):
            self.particles.append([
                self.rect.centerx, self.rect.centery,
                random.uniform(-3, 3), random.uniform(-3, 3),
                random.randint(10, 30)
            ])

    def update(self):
        self.get_input()
        # Update particles
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
        self.particles = [p for p in self.particles if p[4] > 0]
        
    def draw_projectiles(self, surface, camera):
        # Draw particles
        for p in self.particles:
            sx, sy = camera.apply_point((p[0], p[1]))
            pygame.draw.circle(surface, (255, 165, 0), (int(sx), int(sy)), max(1, p[4]//5))
            
        # Draw projectiles
        for proj in self.projectiles:
            if proj["current"] < len(proj["pixels"]):
                proj["current"] += 25 # faster line drawing
                
            draw_limit = min(proj["current"], len(proj["pixels"]))
            for i in range(draw_limit):
                px, py = proj["pixels"][i]
                sx, sy = camera.apply_point((px, py))
                surface.set_at((int(sx), int(sy)), proj["color"])
                
        self.projectiles = [p for p in self.projectiles if p["current"] < len(p["pixels"]) * 2]
