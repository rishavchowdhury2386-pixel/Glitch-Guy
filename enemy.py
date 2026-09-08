import pygame
from settings import *
from rasterization import midpoint_circle
from utils import draw_beveled_rect

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, kind="zombie"):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50
        
        self.image.fill((0,0,0,0))
        # Shadow
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (5, 30, 30, 10))
        
        if kind == "zombie":
            draw_beveled_rect(self.image, (139, 69, 19), pygame.Rect(10, 20, 20, 15)) # brown body
            pygame.draw.circle(self.image, (0, 255, 0), (20, 15), 10) # green head
            # angry eyes
            pygame.draw.line(self.image, BLACK, (15, 12), (18, 14), 2)
            pygame.draw.line(self.image, BLACK, (25, 12), (22, 14), 2)
            pygame.draw.circle(self.image, RED, (16, 15), 2)
            pygame.draw.circle(self.image, RED, (24, 15), 2)
        elif kind == "circle":
            pixels, _ = midpoint_circle(20, 20, 15)
            for px, py in pixels:
                if 0 <= px < 40 and 0 <= py < 40:
                    self.image.set_at((int(px), int(py)), RED)
            # eyes
            pygame.draw.circle(self.image, WHITE, (15, 15), 4)
            pygame.draw.circle(self.image, WHITE, (25, 15), 4)
            pygame.draw.circle(self.image, BLACK, (15, 15), 2)
            pygame.draw.circle(self.image, BLACK, (25, 15), 2)
                    
    def update(self):
        pass
