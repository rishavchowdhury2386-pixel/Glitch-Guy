import pygame
from settings import *
from utils import draw_beveled_rect

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, name, dialogue):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.dialogue = dialogue
        
        self.image.fill((0,0,0,0))
        # Shadow
        pygame.draw.ellipse(self.image, (0, 0, 0, 100), (5, 30, 30, 10))
        # Body
        draw_beveled_rect(self.image, PURPLE, pygame.Rect(10, 15, 20, 20), border_radius=4)
        # Head
        pygame.draw.circle(self.image, (255, 200, 200), (20, 10), 10)
        # Glasses/eyes
        pygame.draw.circle(self.image, WHITE, (16, 10), 4)
        pygame.draw.circle(self.image, WHITE, (24, 10), 4)
        pygame.draw.circle(self.image, BLACK, (16, 10), 2)
        pygame.draw.circle(self.image, BLACK, (24, 10), 2)
